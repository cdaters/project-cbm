"""Direct MC primitive and lease tests on synthetic read-only ext4.

This is not installed-path coverage; use usb_browse_installed.py for that gate.

Use a private mount namespace, a NEW root-owned base under /srv/project-cbm,
and the copied runtime path. No appliance or physical device is touched.
"""
import json
import os
from pathlib import Path
import pty
import select
import signal
import subprocess
import sys
import time

base, runtime = map(Path, sys.argv[1:])
assert os.geteuid()==0 and not base.exists()
base.mkdir(mode=0o755)
sys.path.insert(0,str(runtime))
from project_cbm import usb_browse, library
subprocess.run(['/usr/bin/mount','--make-rprivate','/'],check=True)
source=base/'source';source.mkdir()
dest=base/'content';dest.mkdir();os.chown(dest,1000,1000)
home=base/'home';home.mkdir();os.chown(home,1000,1000)
image=base/'synthetic.img'
with image.open('xb') as stream:stream.truncate(16*1024**2)
subprocess.run(['/usr/sbin/mkfs.ext4',str(image)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
loop=subprocess.check_output(['/usr/sbin/losetup','--read-only','--find','--show',str(image)],text=True).strip()
results=[]
try:
    subprocess.run(['/usr/bin/mount','-t','ext4','-o','ro,nodev,nosuid,noexec,noload',loop,str(source)],check=True)
    for cancel in [False,True]:
        pid,master=pty.fork()
        if pid==0:
            try:
                os.setgroups([]);os.setgid(1000);os.setuid(1000)
                os.environ['TERM']='xterm'
                usb_browse.MC_ENV['HOME']=str(home)
                library.ROOT=dest
                start=time.monotonic()
                usb_browse.browse(source,lambda:cancel and time.monotonic()-start>1)
                os._exit(0)
            except usb_browse.IngestError as error:
                os._exit(0 if cancel and str(error)=='cancelled' else 2)
            except Exception:os._exit(3)
        ended=False;captured=0;start=time.monotonic();sent=False
        try:
            while time.monotonic()-start<12:
                if not cancel and not sent and time.monotonic()-start>2:
                    os.write(master,b'\x1b[21~\r');sent=True
                if select.select([master],[],[],0.1)[0]:
                    try:captured+=len(os.read(master,65536))
                    except OSError:pass
                found,status=os.waitpid(pid,os.WNOHANG)
                if found:
                    ended=True
                    assert os.waitstatus_to_exitcode(status)==0,(cancel,status)
                    break
            assert ended,'MC did not return'
            assert captured>100,'MC did not render to the PTY'
            results.append({'cancel':cancel,'rendered':True,'returned':True})
        finally:
            if not ended:
                os.kill(pid,signal.SIGTERM);os.waitpid(pid,0)
            os.close(master)
    subprocess.run(['/usr/bin/umount',str(source)],check=True)
    assert not os.path.ismount(source)
    # Broker lease worker has no interactive-terminal responsibility.
    from project_cbm import importer
    device=os.stat(loop)
    entry={'device':loop,'number':f'{os.major(device.st_rdev)}:{os.minor(device.st_rdev)}',
           'filesystem':'ext4','diskseq':'synthetic-only','size_bytes':image.stat().st_size}
    for disconnect in [False,True]:
        req_read,req_write=os.pipe();res_read,res_write=os.pipe()
        pid,master=pty.fork()
        if pid==0:
            os.close(req_write);os.close(res_read)
            os.dup2(req_read,0);os.dup2(res_write,1)
            os.close(req_read);os.close(res_write)
            importer.WORK=base;importer.discover=lambda:[entry]
            usb_browse.MC_ENV['HOME']=str(home);library.ROOT=dest
            os.environ['TERM']='xterm'
            try:
                result=importer.perform(entry,None,worker=usb_browse.run,purpose='browse')
                print(json.dumps({'schema_version':2,**result}),flush=True)
                os._exit(0)
            except Exception:os._exit(3)
        os.close(req_read);os.close(res_write)
        def read_reply():
            raw=bytearray();deadline=time.monotonic()+12
            while time.monotonic()<deadline:
                ready=select.select([res_read,master],[],[],0.1)[0]
                if master in ready:
                    try:os.read(master,65536)
                    except OSError:pass
                if res_read in ready:
                    char=os.read(res_read,1)
                    assert char,'broker pipe closed'
                    if char==b'\n':return json.loads(raw)
                    raw.extend(char)
                    assert len(raw)<=8192
            raise AssertionError('broker reply timeout')
        ended=False
        try:
            assert read_reply()['status']=='ready'
            if disconnect:
                os.close(req_write);req_write=None
            else:
                os.write(req_write,b'{"operation":"release"}\n')
            assert read_reply()['status']=='releasing'
            final=read_reply()
            assert final['source_unmounted'] is True,final
            _,status=os.waitpid(pid,0);ended=True
            assert os.waitstatus_to_exitcode(status)==0
            assert not os.path.ismount(base/'browse')
            results.append({'broker_protocol':True,'client_disconnect':disconnect,'released':True})
        finally:
            if req_write is not None:os.close(req_write)
            os.close(res_read);os.close(master)
            if not ended:os.kill(pid,signal.SIGTERM);os.waitpid(pid,0)
finally:
    if os.path.ismount(source):subprocess.run(['/usr/bin/umount',str(source)],check=True)
    subprocess.run(['/usr/sbin/losetup','-d',loop],check=True)
print(json.dumps({'result':'PASS','mc_pty':results,'read_only_mount_released':True,'physical_Pi':'UNTESTED'},indent=2))
