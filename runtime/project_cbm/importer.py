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
from .config_backend import ENV, trusted
from .data import loads

WORK = Path('/run/project-cbm/import')
CONTENT = Path('/home/pi/pcbm')
FILESYSTEMS = {'vfat','exfat','ext4'}
CATEGORIES = {'games','demos','programs','music'}
EXTENSIONS = {'.prg','.p00','.t64','.tap','.d64','.d71','.d81','.g64','.g71','.x64','.sid','.crt'}
MAX_BYTES = 2 * 1024**3
MARGIN = 256 * 1024**2


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


def copy_content(source,category):
    """Runs after dropping all root IDs/groups. No symlink traversal or overwrite."""
    if os.geteuid()!=1000 or category not in CATEGORIES:raise ValueError('copy_identity')
    copied=skipped=total=visited=0
    base=os.open(CONTENT,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    source_fd=os.open(source,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    def walk(src,parts,depth=0):
        nonlocal copied,skipped,total,visited
        if depth>12:raise ValueError('depth')
        names=os.listdir(src)
        if len(names)>10000:raise ValueError('entries')
        for name in sorted(names):
            visited+=1
            if visited>10000:raise ValueError('entries')
            if not name.isprintable() or len(name.encode())>240:skipped+=1;continue
            status=os.stat(name,dir_fd=src,follow_symlinks=False)
            if stat.S_ISDIR(status.st_mode):
                child=os.open(name,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=src)
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
                for component in [('music' if ext=='.sid' else category),'Imported',*parts]:
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
    return {'copied':copied,'skipped':skipped,'bytes':total}


def perform(entry,category):
    if entry not in discover():raise ValueError('device_changed')
    target=trusted(WORK/'source')
    if os.path.ismount(target):raise ValueError('mount_busy')
    fd=os.open(entry['device'],os.O_RDONLY|os.O_NOFOLLOW)
    try:
        s=os.fstat(fd);number=f'{os.major(s.st_rdev)}:{os.minor(s.st_rdev)}'
        if not stat.S_ISBLK(s.st_mode) or number!=entry['number'] or entry not in discover():raise ValueError('device_changed')
        subprocess.run(['/usr/bin/mount','-t',entry['filesystem'],'-o','ro,nodev,nosuid,noexec',
                        '--',f'/proc/self/fd/{fd}',str(target)],pass_fds=(fd,),env=ENV,
                       stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True,timeout=20)
        pid=None;reaped=False
        try:
            reader,writer=os.pipe()
            pid=os.fork()
            if pid==0:
                try:
                    os.close(reader);os.close(fd)
                    os.setgroups([]);os.setgid(1000);os.setuid(1000)
                    answer=copy_content(target,category)
                    os.write(writer,json.dumps(answer).encode());os.close(writer)
                    os._exit(0)
                except Exception:os._exit(2)
            os.close(writer)
            try:raw=os.read(reader,1024)
            finally:os.close(reader)
            _,status=os.waitpid(pid,0);reaped=True
            if status!=0:raise ValueError('copy_failed')
        finally:
            if pid and not reaped:
                try:os.kill(pid,signal.SIGTERM)
                except ProcessLookupError:pass
                os.waitpid(pid,0)
            subprocess.run(['/usr/bin/umount','--',str(target)],env=ENV,check=True,
                           stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=20)
    finally:os.close(fd)
    return loads(raw)


def validate_request(raw):
    if len(raw)>4096:raise ValueError('size')
    d=loads(raw)
    if not isinstance(d,dict) or type(d.get('schema_version')) is not int or d['schema_version']!=1:raise ValueError('request')
    if d=={'schema_version':1,'operation':'list'}:return d
    if (set(d)=={'schema_version','operation','token','category'} and d['operation']=='import'
            and isinstance(d['category'],str) and d['category'] in CATEGORIES
            and isinstance(d['token'],str) and re.fullmatch('[0-9a-f]{32}',d['token'])):return d
    raise ValueError('request')


def main():
    import fcntl
    try:
        os.umask(0o077)
        def interrupted(signum,frame):raise InterruptedError('import_interrupted')
        for sig in (signal.SIGTERM,signal.SIGINT,signal.SIGHUP):signal.signal(sig,interrupted)
        if os.geteuid()!=0 or len(sys.argv)!=1:raise ValueError('invocation')
        from .config_backend import policy
        if not policy()['system_ready']:raise ValueError('setup_incomplete')
        raw=sys.stdin.buffer.read(4097)
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
            elif (set(request)=={'schema_version','operation','token','category'} and request['schema_version']==1
                  and request['operation']=='import' and request['category'] in CATEGORIES
                  and isinstance(request['token'],str) and re.fullmatch('[0-9a-f]{32}',request['token'])):
                entries=loads(trusted(WORK/'devices.json').read_bytes())
                answer=perform(entries[request['token']],request['category'])
                print(json.dumps({'schema_version':1,'status':'ok',**answer}))
            else:raise ValueError('request')
        return 0
    except (OSError,ValueError,TypeError,KeyError,subprocess.SubprocessError):
        print(json.dumps({'schema_version':1,'status':'failed','message':'Import could not complete. Previously copied files remain; inspect device/space and retry. A busy mount requires diagnostics.'}))
        return 2
