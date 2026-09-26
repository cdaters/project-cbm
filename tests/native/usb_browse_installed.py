"""Real installed FILES/FIFO/sudo/broker/MC regression in a disposable chroot.

Run ONLY in the isolated package-test root with a synthetic block device and a
root-owned discovery fixture. The launcher, Menu, sudoers, broker and MC are real.
No production discovery/test switch is added. Never run on an appliance.
"""
import ctypes
import curses
import fcntl
import json
import os
from pathlib import Path
import pty
import select
import signal
import struct
import subprocess
import sys
import termios
import time

assert os.geteuid()==0 and Path('/run/cbm-disposable-usb-test').is_file()
assert ctypes.CDLL(None).prctl(36,1,0,0,0)==0  # init-like adoption/reaping for crash tests
SOURCE=Path('/run/project-cbm/import/browse')
curses.setupterm('linux')
KEYS={name:curses.tigetstr(name) for name in ['kf3','kf10','kcuu1','kcud1','kend','khome']}
results=[]

def processes(comm):
    out=[]
    for p in Path('/proc').glob('[0-9]*'):
        try:
            if p.joinpath('comm').read_text().strip()==comm:
                if proc(int(p.name))['state']=='Z':
                    try:os.waitpid(int(p.name),os.WNOHANG)
                    except ChildProcessError:pass
                else:out.append(int(p.name))
        except OSError:pass
    return out

def wait_for(test, timeout=12):
    until=time.monotonic()+timeout
    while time.monotonic()<until:
        value=test()
        if value:return value
        time.sleep(.05)
    raise AssertionError('condition timeout')

def proc(pid):
    fields=Path(f'/proc/{pid}/stat').read_text().split(') ',1)[1].split()
    return dict(zip(['state','ppid','pgid','sid','tty','tpgid'],fields[:6]))

class Console:
    def __init__(self):
        self.pid,self.fd=pty.fork()
        if self.pid==0:
            os.fchown(0,1000,5)
            fcntl.ioctl(0,termios.TIOCSWINSZ,struct.pack('HHHH',30,100,0,0))
            os.initgroups('pcbm',1000);os.setgid(1000);os.setuid(1000)
            os.execve('/usr/bin/pcbm-files',['pcbm-files'],{
                'PATH':'/usr/bin:/bin','HOME':'/home/pcbm','USER':'pcbm',
                'LOGNAME':'pcbm','TERM':'linux','LC_ALL':'C.UTF-8'})
        self.transcript=bytearray();self.buffer=bytearray();self.closed=False
    def drain(self, seconds=.15):
        until=time.monotonic()+seconds
        while time.monotonic()<until:
            if select.select([self.fd],[],[],.03)[0]:
                try:data=os.read(self.fd,65536)
                except OSError:break
                if not data:break
                self.buffer.extend(data);self.transcript.extend(data)
    def expect(self, text, timeout=12):
        until=time.monotonic()+timeout
        while time.monotonic()<until:
            self.drain()
            if text in self.buffer:
                found=bytes(self.buffer);self.buffer.clear();return found
        raise AssertionError('screen missing '+repr(text)+' tail='+repr(bytes(self.buffer[-1500:])))
    def send(self, value):
        self.drain();self.buffer.clear();os.write(self.fd,value)
    def open(self, usb=True):
        self.expect(b'Files')
        self.send((KEYS['kcud1'] if usb else b'')+b'\r')
        if usb:
            self.expect(b'Choose a partition');self.send(b'\r')
            self.expect(b'Mount Read-Only');self.send(b'\r')
        mc=wait_for(lambda:processes('mc'))[0];self.drain(.6)
        return mc
    def quit_mc(self):
        self.send(KEYS['kf10']);self.drain(.4)
        if b'quit' in self.buffer.lower():self.send(b'\r')
        wait_for(lambda:not processes('mc'));self.drain(.3)
    def finish(self):
        if not self.closed:
            try:os.kill(self.pid,signal.SIGHUP)
            except ProcessLookupError:pass
            os.close(self.fd);self.closed=True
        try:os.waitpid(self.pid,0)
        except ChildProcessError:pass

for case in ['navigation','repeat','sigint','hup','disconnect','bridge-crash','worker-crash','busy','ordinary']:
    c=Console();holder=None
    try:
        mc=c.open(case!='ordinary');state=proc(mc)
        assert state['sid']==str(c.pid) and state['pgid']==state['tpgid']==str(c.pid),state
        fds=[os.readlink(f'/proc/{mc}/fd/{i}') for i in range(3)]
        assert len(set(fds))==1 and (fds[0]=='/dev/tty' or fds[0].startswith('/dev/pts/')),fds
        assert int(state['tty'])!=0
        attrs=termios.tcgetattr(c.fd)
        assert not attrs[3] & (termios.ICANON|termios.ECHO)
        bridge=int(state['ppid'])
        if case!='ordinary':
            assert b'pcbm-ingest-session' in Path(f'/proc/{bridge}/cmdline').read_bytes()
            line=next(l for l in Path('/proc/mounts').read_text().splitlines() if l.split()[1]==str(SOURCE))
            options=set(line.split()[3].split(','))
            assert {'ro','nodev','nosuid','noexec'} <= options and options & {'noload','norecovery'},line
        if case=='navigation':
            # View selected fixture contents to prove actual selection/panel changes,
            # not merely that key bytes were delivered or MC rendered a frame.
            for key,marker in [(KEYS['kend']+KEYS['kcuu1'],b'CBM_NATIVE_ALPHA'),(KEYS['kcud1'],b'CBM_NATIVE_BETA'),(KEYS['kcuu1'],b'CBM_NATIVE_ALPHA')]:
                c.send(key);c.drain(.15);c.send(KEYS['kf3']);c.expect(marker)
                c.send(KEYS['kf10']);c.drain(.2)
            c.send(b'\t'+KEYS['kend']);c.drain(.15);c.send(KEYS['kf3']);c.expect(b'CBM_NATIVE_LIBRARY')
            c.send(KEYS['kf10']);c.drain(.2)
            # Literal Ctrl+C remains MC's native cancellation key, not a shell echo.
            c.send(b'\x03');c.drain(.15);assert processes('mc')
        if case in ['sigint','hup']:
            os.killpg(c.pid,signal.SIGINT if case=='sigint' else signal.SIGHUP)
            wait_for(lambda:not processes('mc'));wait_for(lambda:not os.path.ismount(SOURCE))
        elif case=='disconnect':
            os.close(c.fd);c.closed=True
            wait_for(lambda:not processes('mc'));wait_for(lambda:not os.path.ismount(SOURCE))
        elif case in ['bridge-crash','worker-crash']:
            victim=bridge
            if case=='worker-crash':
                candidates=[]
                for p in Path('/proc').glob('[0-9]*'):
                    try:
                        if p.stat().st_uid==1000 and b'/usr/libexec/pcbm-import-root' in p.joinpath('cmdline').read_bytes():candidates.append(int(p.name))
                    except OSError:pass
                assert len(candidates)==1,candidates;victim=candidates[0]
            os.kill(victim,signal.SIGKILL)
            wait_for(lambda:not processes('mc'));wait_for(lambda:not os.path.ismount(SOURCE))
        else:
            if case=='busy':
                holder=subprocess.Popen(['/usr/bin/sleep','60'],cwd=SOURCE)
            c.quit_mc()
            if case=='ordinary':
                c.expect(b'Files')
            else:
                c.expect(b'Safe Unmount')
                if case=='repeat':
                    c.send(KEYS['kcud1']+b'\r');wait_for(lambda:processes('mc'));c.drain(.5);c.quit_mc();c.expect(b'Safe Unmount')
                c.send(b'\r')
                if case=='busy':
                    response=c.expect(b'release was not confirmed')
                    assert b'safe to remove' not in response
                    assert os.path.ismount(SOURCE)
                    holder.terminate();holder.wait();holder=None
                    subprocess.run(['/usr/bin/umount',str(SOURCE)],check=True)
                else:
                    c.expect(b'safe to remove');assert not os.path.ismount(SOURCE)
        results.append({'case':case,'PASS':True,'mc_process':state,'fds':fds})
        print(json.dumps(results[-1]),flush=True)
    finally:
        if holder:holder.terminate();holder.wait()
        c.finish()
        # Diagnostic traces contain only generated fixture names and isolated UI.
        Path('/tmp/usb-installed-'+case+'.terminal').write_bytes(c.transcript)
        wait_for(lambda:not processes('mc'))
# The bridge also carries ordinary ingestion: preserve scan/select/plan/import
# and explicit cancellation, with only broker-confirmed final release.
for import_files in (False,True):
    listed=subprocess.run(['runuser','-u','pcbm','--','/usr/bin/pcbm-import-operation'],
        input='{"schema_version":1,"operation":"list"}\n',text=True,capture_output=True,check=True)
    token=json.loads(listed.stdout)['devices'][0]['token']
    bridge=subprocess.Popen(['runuser','-u','pcbm','--','/usr/bin/pcbm-ingest-session'],
        stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    def exchange(value):
        bridge.stdin.write(json.dumps(value)+'\n');bridge.stdin.flush()
        assert select.select([bridge.stdout],[],[],15)[0], 'ingestion reply timeout'
        return json.loads(bridge.stdout.readline())
    try:
        assert exchange({'schema_version':2,'operation':'session','token':token})['status']=='ready'
        if import_files:
            assert exchange({'operation':'scan','folder':'root'})['status']=='ok'
            assert exchange({'operation':'select','mode':'all','selected':True})['status']=='ok'
            assert exchange({'operation':'plan','category':'programs','family':'shared'})['status']=='ok'
            answer=exchange({'operation':'import'})
            assert answer['saved']==1,answer
            saved=list(Path('/home/pcbm/content').rglob('0fixture.prg'))
            assert len(saved)==1 and saved[0].read_bytes()==b'\x01\x08CBM native original fixture'
        else:answer=exchange({'operation':'cancel'})
        assert answer['source_unmounted'] is True,answer
        bridge.stdin.close();assert bridge.wait(timeout=5)==0
        results.append({'case':'ingest-save' if import_files else 'ingest-cancel','PASS':True})
        print(json.dumps(results[-1]),flush=True)
    finally:
        if bridge.poll() is None:
            bridge.stdin.close();bridge.wait(timeout=35)
assert not os.path.ismount(SOURCE)
print(json.dumps({'result':'PASS','installed_path':True,'TERM':'linux','cases':results,'physical_Pi':'UNTESTED'}),flush=True)
