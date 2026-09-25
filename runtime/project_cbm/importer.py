"""Constrained removable-media import; root mounts, UID 1000 copies regular files.

No caller-supplied device, filesystem, mount options or destination paths. Discovery
tokens bind a USB partition to its kernel disk sequence, not a reusable /dev name.
"""
import json
import os
from pathlib import Path
import re
import secrets
import signal
import stat
import subprocess
import sys
import time
from .config_backend import ENV, trusted
from .data import loads
from . import library

WORK = Path('/run/project-cbm/import')
CONTENT = library.ROOT
FILESYSTEMS = {'vfat','exfat','ext4'}
CATEGORIES = {'games','demos','programs','music'}
# Shared policy constants; legacy copy semantics remain compatible.
from .ingestion import EXTENSIONS, MAX_BYTES, MARGIN
from .usb_discovery import HOST_METADATA, host_metadata


class ImportFailure(ValueError):
    def __init__(self,code,source_unmounted=None,result=None):
        super().__init__(code)
        self.result=result
        self.code=code
        self.source_unmounted=source_unmounted


def copy_failure(error):
    # No exception messages, filenames or contents cross the privileged boundary.
    if isinstance(error,PermissionError):return 'access_denied'
    if isinstance(error,ValueError) and str(error) in ('space','limit','depth','entries'):
        return str(error)
    return 'copy_failed'


def mount_options(filesystem):
    """Fixed read-only policy; FAT ownership is synthetic, never inherited root-only.

    The broker's 0077 umask protects its state. FAT/exFAT otherwise inherit that
    mask and root ownership, making the source unreadable after the copy worker
    drops privileges. Expose only the runtime UID/GID; never change source bytes.
    """
    if filesystem not in FILESYSTEMS:raise ValueError('filesystem')
    options='ro,nodev,nosuid,noexec'
    if filesystem=='ext4':return options+',noload'
    return options+',uid=1000,gid=1000,fmask=0177,dmask=0077'


def discover():
    p=subprocess.run(['/usr/bin/lsblk','--json','--bytes','--paths','--output','NAME,TYPE,TRAN,FSTYPE,MOUNTPOINTS,SIZE,MAJ:MIN'],
                     text=True,capture_output=True,env=ENV,timeout=10,check=True)
    if len(p.stdout)>1024*1024:raise ValueError('device_inventory_size')
    document=loads(p.stdout);found=[]
    def mounted(node,depth=0):
        if depth>8:raise ValueError('device_tree_depth')
        return any(node.get('mountpoints') or []) or any(mounted(n,depth+1) for n in node.get('children',[]))
    for disk in document['blockdevices']:
        # No loops, device mapper, root/boot disks or non-USB transports.
        if disk['type']!='disk' or disk.get('tran')!='usb':continue
        children=disk.get('children',[])
        if mounted(disk):continue
        name=Path(disk['name']).name
        if not re.fullmatch(r'sd[a-z]+',name):continue
        sys=Path('/sys/class/block')/name
        if not re.search(r'/usb[0-9]+/',str(sys.resolve())):continue
        sequence=(sys/'diskseq').read_text().strip()
        if not sequence.isdecimal():continue
        for part in children:
            if part['type']!='part' or part.get('children') or part.get('fstype') not in FILESYSTEMS:continue
            if not re.fullmatch(r'/dev/sd[a-z]+[0-9]+',part['name']):continue
            if not re.fullmatch(r'[0-9]+:[0-9]+',part['maj:min']):continue
            found.append({'device':part['name'],'number':part['maj:min'],'diskseq':sequence,
                          'filesystem':part['fstype'],'size_bytes':part['size']})
    return found[:16]


def open_directory(parent,name):
    if not name or name in ('.','..') or '/' in name or not name.isprintable():raise ValueError('directory')
    try:os.mkdir(name,0o755,dir_fd=parent)
    except FileExistsError:pass
    return os.open(name,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=parent)


def copy_content(source,category,family=None):
    """Runs after dropping all root IDs/groups. No symlink traversal or overwrite."""
    if os.geteuid()!=1000 or category not in CATEGORIES:raise ValueError('copy_identity')
    library.import_destination(category, '', family)
    copied=skipped=total=visited=ignored_metadata=0
    base=os.open(CONTENT,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    source_fd=os.open(source,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    def walk(src,parts,depth=0):
        nonlocal copied,skipped,total,visited,ignored_metadata
        if depth>12:raise ValueError('depth')
        names=os.listdir(src)
        if len(names)>10000:raise ValueError('entries')
        for name in sorted(names):
            visited+=1
            if visited>10000:raise ValueError('entries')
            if host_metadata(name):ignored_metadata+=1;continue
            if not name.isprintable() or len(name.encode())>240:skipped+=1;continue
            status=os.stat(name,dir_fd=src,follow_symlinks=False)
            if stat.S_ISDIR(status.st_mode):
                try:child=os.open(name,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=src)
                except PermissionError:
                    # A normal ext4 drive may contain root-only lost+found.
                    # Never elevate copying privileges to traverse it.
                    skipped+=1;continue
                try:walk(child,[*parts,name],depth+1)
                finally:os.close(child)
                continue
            ext=Path(name).suffix.lower()
            if not stat.S_ISREG(status.st_mode) or ext not in EXTENSIONS:skipped+=1;continue
            if copied+skipped>=10000 or total+status.st_size>MAX_BYTES:raise ValueError('limit')
            fs=os.fstatvfs(base)
            if fs.f_bavail*fs.f_frsize < status.st_size+MARGIN:raise ValueError('space')
            dest=os.dup(base)
            try:
                for component in [*library.import_destination(category,ext,family),*parts]:
                    new=open_directory(dest,component);os.close(dest);dest=new
                try:os.stat(name,dir_fd=dest,follow_symlinks=False)
                except FileNotFoundError:pass
                else:skipped+=1;continue
                temp='.pcbm-import-'+secrets.token_hex(12)
                inp=os.open(name,os.O_RDONLY|os.O_NOFOLLOW,dir_fd=src)
                try:
                    if not stat.S_ISREG(os.fstat(inp).st_mode):raise ValueError('file_changed')
                    out=os.open(temp,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644,dir_fd=dest)
                    try:
                        with os.fdopen(out,'wb') as dst,os.fdopen(os.dup(inp),'rb') as stream:
                            remaining=status.st_size
                            while remaining:
                                data=stream.read(min(remaining,1024*1024))
                                if not data:raise ValueError('short_read')
                                dst.write(data);remaining-=len(data)
                            if stream.read(1):raise ValueError('file_grew')
                            dst.flush();os.fsync(dst.fileno())
                        os.link(temp,name,src_dir_fd=dest,dst_dir_fd=dest,follow_symlinks=False)
                        os.fsync(dest);copied+=1;total+=status.st_size
                    finally:
                        try:os.unlink(temp,dir_fd=dest)
                        except FileNotFoundError:pass
                finally:os.close(inp)
            finally:os.close(dest)
    try:walk(source_fd,[])
    finally:os.close(source_fd);os.close(base)
    result={'copied':copied,'skipped':skipped,'bytes':total}
    if ignored_metadata:result['ignored_metadata']=ignored_metadata
    return result


def stop_worker(pid):
    """Bounded TERM grace, then KILL and reap; never leave a live copy worker."""
    for sig in (signal.SIGTERM,signal.SIGKILL):
        try:os.kill(pid,sig)
        except ProcessLookupError:pass
        deadline=time.monotonic()+2
        while time.monotonic()<deadline:
            if os.waitpid(pid,os.WNOHANG)[0]:return
            time.sleep(0.02)
    # A kernel I/O wait can outlive SIGKILL; refuse a safe-removal assertion.
    raise ImportFailure('copy_failed',False)


def perform(entry,category,family=None,worker=None):
    if entry not in discover():raise ValueError('device_changed')
    target=trusted(WORK/'source')
    if os.path.ismount(target):raise ValueError('mount_busy')
    fd=os.open(entry['device'],os.O_RDONLY|os.O_NOFOLLOW)
    try:
        s=os.fstat(fd);number=f'{os.major(s.st_rdev)}:{os.minor(s.st_rdev)}'
        if not stat.S_ISBLK(s.st_mode) or number!=entry['number'] or entry not in discover():raise ValueError('device_changed')
        # ext4 may replay a journal even for a read-only mount. Source media
        # must remain unchanged; unclean media requiring recovery is refused.
        options=mount_options(entry['filesystem'])
        try:
            subprocess.run(['/usr/bin/mount','-t',entry['filesystem'],'-o',options,
                            '--',f'/proc/self/fd/{fd}',str(target)],pass_fds=(fd,),env=ENV,
                           stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True,timeout=20)
        except (OSError,subprocess.SubprocessError):
            raise ImportFailure('mount_failed',not os.path.ismount(target)) from None
        pid=None;reaped=False;failure=None;answer=None
        try:
            reader,writer=os.pipe()
            pid=os.fork()
            if pid==0:
                try:
                    os.close(reader);os.close(fd)
                    os.setgroups([]);os.setgid(1000);os.setuid(1000)
                    answer=worker(target) if worker else copy_content(target,category,family)
                    os.write(writer,json.dumps(answer).encode());os.close(writer)
                    os._exit(0)
                except Exception as error:
                    try:os.write(writer,json.dumps({'error':copy_failure(error)}).encode())
                    except OSError:pass
                    os._exit(2)
            os.close(writer)
            try:
                import select
                if not select.select([reader],[],[],1800)[0]:raise ImportFailure('copy_failed',False)
                raw=os.read(reader,8192)
            finally:os.close(reader)
            _,status=os.waitpid(pid,0);reaped=True
            if status!=0:
                try:code=loads(raw).get('error')
                except (ValueError,AttributeError):code=None
                if code not in ('access_denied','space','limit','depth','entries'):code='copy_failed'
                failure=ImportFailure(code,False)
                raise failure
            answer=loads(raw)
        finally:
            worker_failure=None
            if pid and not reaped:
                try:stop_worker(pid)
                except ImportFailure as error:worker_failure=error
            try:
                subprocess.run(['/usr/bin/umount','--',str(target)],env=ENV,check=True,
                               stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=20)
            except (OSError,subprocess.SubprocessError):
                raise ImportFailure('unmount_failed',False,answer) from None
            if os.path.ismount(target):raise ImportFailure('unmount_failed',False,answer)
            if worker_failure is not None:raise worker_failure
            if failure is not None:failure.source_unmounted=True
    finally:os.close(fd)
    return {**answer,'source_unmounted':True}


def validate_request(raw):
    if len(raw)>4096:raise ValueError('size')
    d=loads(raw)
    if (isinstance(d,dict) and type(d.get('schema_version')) is int and d['schema_version']==2
            and set(d)=={'schema_version','operation','token'} and d['operation']=='session'
            and isinstance(d['token'],str) and re.fullmatch('[0-9a-f]{32}',d['token'])):return d
    if not isinstance(d,dict) or type(d.get('schema_version')) is not int or d['schema_version']!=1:raise ValueError('request')
    if d=={'schema_version':1,'operation':'list'}:return d
    if (set(d) in ({'schema_version','operation','token','category'}, {'schema_version','operation','token','category','family'}) and d['operation']=='import'
            and isinstance(d['category'],str) and d['category'] in CATEGORIES
            and ('family' not in d or isinstance(d['family'],str) and d['family'] in library.FAMILIES)
            and isinstance(d['token'],str) and re.fullmatch('[0-9a-f]{32}',d['token'])):return d
    raise ValueError('request')


def main():
    import fcntl
    request={}
    try:
        os.umask(0o077)
        def interrupted(signum,frame):raise InterruptedError('import_interrupted')
        for sig in (signal.SIGTERM,signal.SIGINT,signal.SIGHUP):signal.signal(sig,interrupted)
        if os.geteuid()!=0 or len(sys.argv)!=1:raise ValueError('invocation')
        from .config_backend import policy
        if not policy()['system_ready']:raise ValueError('setup_incomplete')
        raw=bytearray()
        import select
        deadline=time.monotonic()+20
        while len(raw)<=4096:
            if not select.select([0],[],[],max(0,deadline-time.monotonic()))[0]:raise ValueError('request_timeout')
            byte=os.read(0,1)
            if not byte or byte==b'\n':break
            raw.extend(byte)
        raw=bytes(raw)
        if len(raw)>4096:raise ValueError('size')
        request=validate_request(raw)
        trusted(WORK)
        with (WORK/'lock').open('a') as lock:
            fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
            if request=={'schema_version':1,'operation':'list'}:
                entries={secrets.token_hex(16):x for x in discover()}
                from .config_backend import Linux
                Linux().write(WORK/'devices.json',json.dumps(entries))
                print(json.dumps({'schema_version':1,'status':'ok','devices':[
                    {'token':k,'label':f'USB partition {i+1}: {v["filesystem"]}, {v["size_bytes"]//1024**2} MiB'}
                    for i,(k,v) in enumerate(entries.items())]}))
            elif request.get('schema_version')==2:
                from .ingest_session import run
                entries=loads(trusted(WORK/'devices.json').read_bytes())
                answer=perform(entries[request['token']],None,worker=run)
                print(json.dumps({'schema_version':2,**answer}),flush=True)
            elif (set(request) in ({'schema_version','operation','token','category'}, {'schema_version','operation','token','category','family'}) and request['schema_version']==1
                  and request['operation']=='import' and request['category'] in CATEGORIES
                  and isinstance(request['token'],str) and re.fullmatch('[0-9a-f]{32}',request['token'])):
                entries=loads(trusted(WORK/'devices.json').read_bytes())
                answer=perform(entries[request['token']],request['category'],request.get('family'))
                print(json.dumps({'schema_version':1,'status':'ok',**answer}))
            else:raise ValueError('request')
        return 0
    except (OSError,ValueError,TypeError,KeyError,subprocess.SubprocessError) as error:
        if request.get('schema_version')==2:
            detail=error.result if isinstance(error,ImportFailure) and isinstance(error.result,dict) else {}
            print(json.dumps({**detail,'schema_version':2,'status':'partial' if detail.get('saved') else 'failed',
                              'error':error.code if isinstance(error,ImportFailure) else 'unavailable',
                              'source_unmounted':error.source_unmounted if isinstance(error,ImportFailure) else None}),flush=True)
            return 2
        print(json.dumps({'schema_version':1,'status':'failed',
                          'error':error.code if isinstance(error,ImportFailure) else 'unavailable',
                          'source_unmounted':error.source_unmounted if isinstance(error,ImportFailure) else None}))
        return 2
