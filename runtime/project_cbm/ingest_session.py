"""Bounded USB review protocol. Invoked only after the broker drops privileges."""
import fcntl
import json
import os
from pathlib import Path
import select
import time
from .data import loads
from .ingestion import IngestError, directory, plan, save
from .usb_discovery import Discovery
from . import library

STATE = Path('/home/pcbm/.local/state/project-cbm/ingestion')
IDLE_SECONDS = 300


def receive(timeout=IDLE_SECONDS):
    deadline = time.monotonic() + timeout
    raw = bytearray()
    while len(raw) <= 4096:
        wait = max(0, deadline - time.monotonic())
        if not select.select([0], [], [], wait)[0]:
            raise IngestError('expired')
        char = os.read(0, 1)
        if not char:
            raise IngestError('disconnected')
        if char == b'\n':
            value = loads(bytes(raw))
            if not isinstance(value, dict):
                raise IngestError('request')
            return value
        raw.extend(char)
    raise IngestError('request')


def emit(value):
    raw = json.dumps({'schema_version': 2, **value}, ensure_ascii=False)
    if len(raw.encode('utf-8')) > 8192:
        raise IngestError('reply_size')
    print(raw, flush=True)


def cancellation():
    if not select.select([0], [], [], 0)[0]:
        return False
    request = receive(1)
    if request != {'operation': 'cancel'}:
        raise IngestError('request')
    return True


class Session:
    def __init__(self, source, root=library.ROOT, state=STATE):
        self.discovery = Discovery(source)
        self.root, self.state = Path(root), Path(state)
        self.planned = None
        self.finished = False

    def handle(self, request, cancelled=lambda: False):
        op = request.get('operation')
        allowed = {
            'folders': {'operation', 'folder', 'offset'}, 'scan': {'operation', 'folder'},
            'page': {'operation', 'offset'}, 'detail': {'operation', 'id'}, 'select': {'operation', 'mode', 'ids', 'selected'},
            'plan': {'operation', 'category', 'family'}, 'import': {'operation'},
            'cancel': {'operation'},
        }
        if op not in allowed or set(request) - allowed[op]:
            raise IngestError('request')
        offset = request.get('offset', 0)
        if type(offset) is not int or not 0 <= offset <= 10000:
            raise IngestError('request')
        folder = request.get('folder', 'root')
        if not isinstance(folder, str) or folder not in self.discovery.folders:
            raise IngestError('request')
        if op == 'cancel':
            self.finished = True
            return {'status': 'cancelled'}
        if op == 'folders':
            return self.discovery.folders_page(folder, offset)
        if op == 'scan':
            self.planned = None
            return self.discovery.scan(folder, cancelled)
        if op == 'page':
            return self.discovery.page(offset)
        if op == 'detail':
            item = self.discovery.items[request.get('id')]
            return {**item.summary(), 'name': item.path}
        if op == 'select':
            self.planned = None
            ids = request.get('ids', [])
            selected = request.get('selected', True)
            if not isinstance(ids, list) or not all(isinstance(i, str) for i in ids) or type(selected) is not bool:
                raise IngestError('request')
            return self.discovery.select(request.get('mode'), ids, selected)
        if op == 'plan':
            items = [i for i in self.discovery.items.values() if i.id in self.discovery.selected]
            collection = self.discovery.scope[-1] if self.discovery.scope else 'USB Import'
            self.planned = plan(items, self.root, self.discovery.open, request.get('category'),
                                request.get('family'), collection, cancelled)
            return self.planned.summary()
        if not self.planned:
            raise IngestError('review_required')
        # No creation of state, destination directories or payload before Import.
        # The fixed user-state trust chain is checked with no-follow descriptors.
        with directory(self.state.anchor, self.state.parts[1:], create=True) as state:
            lock = os.open('lock', os.O_WRONLY | os.O_CREAT | os.O_NOFOLLOW, 0o600, dir_fd=state)
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                import secrets
                journal = os.open(secrets.token_hex(16) + '.jsonl', os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=state)
                with os.fdopen(journal, 'w') as stream:
                    def record(event):
                        stream.write(json.dumps(event, ensure_ascii=False) + '\n')
                        stream.flush()
                        os.fsync(stream.fileno())
                    result = save(self.planned, self.root, self.discovery.open, record, cancelled)
                    record({'event': 'finished', **result})
            finally:
                os.close(lock)
        self.finished = True
        return result


def run(source):
    if os.geteuid() != 1000:
        raise IngestError('identity')
    session = Session(source)
    emit({'status': 'ready'})
    while not session.finished:
        try:
            request = receive()
            answer = session.handle(request, cancellation)
            if session.finished:
                return answer  # Broker emits final result only AFTER release.
            emit({'status': 'ok', **answer})
        except (OSError, ValueError, KeyError, TypeError) as error:
            code = str(error) if isinstance(error, IngestError) else 'source_unavailable'
            if code in ('expired', 'disconnected', 'cancelled'):
                return {'status': 'cancelled', 'error': code}
            emit({'status': 'failed', 'error': code})
    return {'status': 'cancelled'}
