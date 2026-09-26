"""Unprivileged, on-demand Online Library session and shared-ingestion coordinator."""
from contextlib import ExitStack, contextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path
import secrets
import signal
import stat
import sys

from . import ingestion, library
from .config_backend import policy
from .ingest_session import receive, emit, cancellation, STATE
from .online_backend import Backend, OnlineError, PAGE, MAX_SELECTION, integer


def key(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()[:16]


def friendly(value, limit=180):
    # Names are untrusted text. Never let dialog interpret their backslash escapes.
    return value.replace('\\', '/')[:limit]


class Session:
    def __init__(self, backend=None, root=library.ROOT, state=STATE):
        self.backend = backend or Backend()
        self.root, self.state = Path(root), Path(state)
        self.results, self.items, self.selected = {}, {}, set()
        self.release = None
        self.prepared = None
        self.resources = ExitStack()
        self.staged = {}
        self.finished = False

    def close(self):
        self.resources.close()
        self.resources = ExitStack()
        self.staged = {}
        self.prepared = None

    def rows(self, offset):
        integer(offset, 1000)
        values = list(self.items.items())
        return {'rows': [{'id': k, 'name': friendly(i.path), 'bytes': i.size, 'selected': k in self.selected}
                         for k,i in values[offset:offset+PAGE]], 'total':len(values), 'selected':len(self.selected),
                'bytes':sum(self.items[k].size for k in self.selected)}

    @contextmanager
    def opener(self, item):
        stream = self.staged[item.id]
        stream.seek(0)
        yield stream

    def prepare(self, category, family, cancelled):
        self.close()
        items = [i for k,i in self.items.items() if k in self.selected]
        total = sum(i.size for i in items)
        if not items or len(items) > 100 or total > MAX_SELECTION: raise OnlineError('selection_limit')
        # Validate destination before any transfer. Machine/category are explicit.
        if category not in ('games','demos','programs','music') or family not in library.FAMILIES:
            raise OnlineError('classification')
        collection = ''.join(c if c.isprintable() and c not in '/\\' else '_' for c in self.release['name'])[:60].strip()
        if collection in ('','.','..'): collection = 'Assembly64 download'
        try:
            state = self.resources.enter_context(ingestion.directory(self.state.anchor, self.state.parts[1:], create=True))
            if os.fstat(state).st_uid != os.getuid(): raise OnlineError('local_unavailable')
            os.fchmod(state, 0o700)
            lock = os.open('lock', os.O_WRONLY | os.O_CREAT | os.O_NOFOLLOW | os.O_NONBLOCK, 0o600, dir_fd=state)
            self.resources.callback(os.close, lock)
            if not stat.S_ISREG(os.fstat(lock).st_mode): raise OnlineError('local_unavailable')
            try: fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError: raise OnlineError('busy') from None
            space = os.fstatvfs(state)
            if space.f_bavail * space.f_frsize < total * 2 + ingestion.MARGIN: raise OnlineError('space')
            for item in items:
                if cancelled(): raise OnlineError('cancelled')
                fd = os.open('.', os.O_RDWR | os.O_TMPFILE | os.O_CLOEXEC, 0o600, dir_fd=state)
                stream = self.resources.enter_context(os.fdopen(fd, 'w+b'))
                data = self.backend.download(self.release, item, cancelled)
                stream.write(data); stream.flush(); del data
                self.staged[item.id] = stream
            self.prepared = ingestion.plan(items, self.root, self.opener, category, family, collection, cancelled, origin='Downloaded')
            return self.prepared.summary()
        except BaseException:
            self.close()
            raise

    def save(self, cancelled):
        if self.prepared is None: raise OnlineError('review_required')
        try:
            with ingestion.directory(self.state.anchor, self.state.parts[1:]) as state:
                journal = os.open(secrets.token_hex(16)+'.jsonl',os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600,dir_fd=state)
                with os.fdopen(journal,'w') as output:
                    def record(value):
                        output.write(json.dumps(value,ensure_ascii=False)+'\n');output.flush();os.fsync(output.fileno())
                    record({'event':'started','source':'online','backend':self.backend.profile.key,
                            'release':self.release,'selected':[{'id':i.id,'path':i.path,'bytes':i.size} for i,_,_,_ in self.prepared.rows]})
                    result = ingestion.save(self.prepared,self.root,self.opener,record,cancelled)
                    try:record({'event':'finished',**result})
                    except OSError:result.update(status='partial' if result['saved'] else 'failed',error='write_failed')
            return result
        finally:
            self.close()

    def handle(self, request, cancelled=lambda: False):
        if not isinstance(request,dict): raise OnlineError('request')
        op = request.get('operation')
        allowed = {'search':{'operation','fields','offset'},'presets':{'operation'},'servers':{'operation'},
                   'release':{'operation','id'},'files':{'operation','offset'},'select':{'operation','id','mode'},
                   'prepare':{'operation','category','family'},'save':{'operation'},'cancel':{'operation'}}
        if op not in allowed or set(request)-allowed[op]: raise OnlineError('request')
        if op == 'cancel': self.close();self.finished=True;return {'status':'cancelled'}
        if op == 'presets': return {'presets':self.backend.presets(cancelled)}
        if op == 'servers': return {'servers':self.backend.discovery(cancelled),'backend':self.backend.profile.label}
        if op == 'search':
            self.close();self.release=None;self.items={};self.selected=set();self.results={}
            fields=request.get('fields');offset=request.get('offset',0)
            if not isinstance(fields,dict):raise OnlineError('query')
            rows = self.backend.search(fields,offset,cancelled)
            self.results={key([self.backend.profile.key,r['id'],r['category']]):r for r in rows}
            return {'rows':[{'id':k,'name':friendly(r['name']) + (f" ({r['year']})" if r.get('year') else '')}
                            for k,r in self.results.items()], 'total':len(rows), 'more':len(rows)==PAGE and offset<1000}
        if op == 'release':
            selected=self.results.get(request.get('id'))
            if selected is None: raise OnlineError('selection')
            self.close();self.release=None;self.items={};self.selected=set()
            release=self.backend.metadata(selected,cancelled)
            items,unsupported=self.backend.files(release,cancelled)
            self.release=release
            self.items={key([self.backend.profile.key,release['id'],release['category'],i.id]):i for i in items}
            return {'name':friendly(release['name']), 'group':friendly(release.get('group','Unknown')),
                    'year':release.get('year',0), 'unsupported':unsupported, **self.rows(0)}
        if self.release is None:raise OnlineError('selection')
        if op == 'files': return self.rows(request.get('offset',0))
        if op == 'select':
            self.close()
            mode=request.get('mode');selected=request.get('id')
            if mode == 'clear':self.selected.clear()
            elif mode == 'all':self.selected=set(self.items)
            elif mode == 'toggle' and selected in self.items:
                if selected in self.selected:self.selected.remove(selected)
                else:self.selected.add(selected)
            else:raise OnlineError('selection')
            return {'selected':len(self.selected)}
        if op == 'prepare':return self.prepare(request.get('category'),request.get('family'),cancelled)
        if op == 'save':return self.save(cancelled)
        raise OnlineError('request')


def run():
    # No sudo, arbitrary command, imported shell environment or configurable URL.
    if os.getuid()!=1000 or os.geteuid()!=1000 or not policy()['system_ready']:
        raise OnlineError('setup')
    session=Session()
    try:
        # Global per-user lock covers catalog requests as well as downloads.
        with ingestion.directory(STATE.anchor,STATE.parts[1:],create=True) as state:
            if os.fstat(state).st_uid!=1000:raise OnlineError('setup')
            os.fchmod(state,0o700)
            fd=os.open('online.lock',os.O_WRONLY|os.O_CREAT|os.O_NOFOLLOW|os.O_NONBLOCK,0o600,dir_fd=state)
            try:
                if not stat.S_ISREG(os.fstat(fd).st_mode):raise OnlineError('setup')
                try:fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
                except BlockingIOError:raise OnlineError('busy') from None
                emit({'status':'ready','backend':session.backend.profile.label})
                while not session.finished:
                    try:
                        request=receive()
                        signal.alarm(180)  # Includes resolver, all transfers and staging.
                        try:answer=session.handle(request,cancellation)
                        finally:signal.alarm(0)
                        emit({'status':'ok',**answer})
                    except (OnlineError,ingestion.IngestError) as ex:
                        code=str(ex)
                        session.close()
                        if code in ('expired','disconnected','cancelled'):
                            session.close();session.finished=True
                        emit({'status':'failed','error':code})
                    except (ValueError,TypeError,KeyError,AttributeError,RecursionError):
                        session.close();emit({'status':'failed','error':'incompatible'})
                    except OSError:
                        session.close();emit({'status':'failed','error':'local_unavailable'})
            finally:os.close(fd)
    finally:session.close()


def main():
    def interrupted(*_):raise OnlineError('cancelled')
    for sig in (signal.SIGTERM,signal.SIGHUP,signal.SIGINT):signal.signal(sig,interrupted)
    def timed_out(*_):raise OnlineError('timeout')
    signal.signal(signal.SIGALRM,timed_out)
    try:run();return 0
    except (OnlineError,ingestion.IngestError) as ex:
        try:emit({'status':'failed','error':str(ex)})
        except (OSError,ValueError):pass
        return 1
    except (OSError,ValueError,KeyError):
        try:emit({'status':'failed','error':'setup'})
        except OSError:pass
        return 1
