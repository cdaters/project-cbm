"""Actual installed Menu/FIFO/unprivileged adapter/writer; only HTTP is synthetic.

Run exclusively in usb_browse_stage's networkless disposable overlay, never a Pi.
"""
import curses
import fcntl
import json
import os
from pathlib import Path
import pty
import re
import select
import signal
import struct
import time

assert os.geteuid()==0 and Path('/run/cbm-disposable-usb-test').is_file()
entry=Path('/usr/share/project-cbm/runtime/bin/pcbm-online-session');original=entry.read_bytes()
curses.setupterm('linux');DOWN=curses.tigetstr('kcud1')
results=[]
fixture='''
from project_cbm.online_backend import Transport
import json
def synthetic_get(self,path,limit,cancelled=lambda:False):
    assert self.profile.client_id == 'cbm'
    if cancelled():
        from project_cbm.online_backend import OnlineError
        raise OnlineError('cancelled')
    release={'id':'original-native','category':1,'name':'Native Original Set','year':2026,'group':'Original test fixture'}
    if path.startswith('search/aql/'):value=[release]
    elif path.startswith('search/meta/'):value=release
    elif path.startswith('search/entries/'):value={'contentEntry':[{'id':0,'path':'disk1/original.prg','size':4},{'id':1,'path':'disk2/original.prg','size':4}]}
    elif path.startswith('search/bin/'):return 'application/octet-stream',b'\\x01\\x08AB'
    else:raise AssertionError('unexpected synthetic operation')
    return 'application/json',json.dumps(value).encode()
Transport.get=synthetic_get
'''

def workers():
    found=[]
    for p in Path('/proc').glob('[0-9]*'):
        try:
            if p.stat().st_uid==1000 and b'/usr/bin/pcbm-online-session' in p.joinpath('cmdline').read_bytes():found.append(int(p.name))
        except OSError:pass
    return found

class Console:
    def __init__(self):
        self.pid,self.fd=pty.fork();self.buffer=bytearray();self.trace=bytearray()
        if self.pid==0:
            os.fchown(0,1000,5);fcntl.ioctl(0,termios.TIOCSWINSZ,struct.pack('HHHH',30,100,0,0))
            os.initgroups('pcbm',1000);os.setgid(1000);os.setuid(1000)
            os.execve('/usr/bin/pcbm-content',['pcbm-content'],{'PATH':'/usr/bin:/bin','HOME':'/home/pcbm','TERM':'linux','LC_ALL':'C.UTF-8'})
    def drain(self,seconds=.1):
        until=time.monotonic()+seconds
        while time.monotonic()<until:
            if select.select([self.fd],[],[],.02)[0]:
                try:data=os.read(self.fd,65536)
                except OSError:return
                self.buffer.extend(data);self.trace.extend(data)
    def expect(self,value):
        until=time.monotonic()+12
        while time.monotonic()<until:
            self.drain()
            if value in re.sub(rb'\x1b\[[0-?]*[ -/]*[@-~]', b'', self.buffer).replace(b'\x0f', b''):self.buffer.clear();return
        raise AssertionError('missing '+repr(value)+' '+repr(self.buffer[-1500:]))
    def send(self,value):
        self.drain();self.buffer.clear();os.write(self.fd,value)
    def select(self,n=0):self.send(DOWN*n+b'\r')
    def prepare(self):
        self.expect(b'Browse Library');self.select(2)
        self.expect(b'Powered by Assembly64');self.select()
        self.expect(b'Search by Title');self.send(b'Fixture\r')
        self.expect(b'Native Original Set');self.select()
        self.expect(b'Release Details');self.select()
        self.expect(b'Select all supported files');self.select(2)
        self.expect(b'Review destination');self.select(4)
        self.expect(b'Destination - Category');self.select()
        self.expect(b'Destination - Machine');self.select()
        self.expect(b'Download selected files for review');self.select()
        self.expect(b'Review Save')
    def close(self):
        try:os.killpg(self.pid,signal.SIGHUP)
        except ProcessLookupError:pass
        os.close(self.fd)
        try:os.waitpid(self.pid,0)
        except ChildProcessError:pass

import termios
try:
    entry.write_text(original.decode().replace('from project_cbm.online_session import main',fixture+'\nfrom project_cbm.online_session import main'))
    c=Console()
    try:
        c.prepare()
        assert workers()
        assert all(Path(f'/proc/{pid}').stat().st_uid==1000 for pid in workers())
        assert not list(Path('/home/pcbm/content').rglob('original.prg'))
        results.append('installed Content/Online/Menu/FIFO/adapter explicit preparation without library writes')
        c.select();c.expect(b'Saved: 2')
        paths=list(Path('/home/pcbm/content').rglob('original.prg'))
        assert len(paths)==2 and all(p.read_bytes()==b'\x01\x08AB' and p.stat().st_uid==1000 for p in paths)
        assert {p.parent.name for p in paths}=={'disk1','disk2'}
        results.append('real shared atomic writer preserves both selected disk paths and ownership')
        c.select();c.expect(b'Search Results')
        c.send(b'\x1b');c.expect(b'Search by title')
        c.send(b'\x1b');c.expect(b'Browse Library')
        results.append('return to responsive Content Menu')
    finally:
        Path('/tmp/online-installed-save.terminal').write_bytes(c.trace);c.close()
    c=Console()
    try:
        c.prepare()
        assert b'Already Present' in c.trace
    finally:
        Path('/tmp/online-installed-hup.terminal').write_bytes(c.trace);c.close()
    until=time.monotonic()+12
    while workers() and time.monotonic()<until:time.sleep(.1)
    assert not workers()
    state=Path('/home/pcbm/.local/state/project-cbm/ingestion')
    assert all(p.name in ('lock','online.lock') or p.suffix=='.jsonl' for p in state.iterdir())
    for name in ('lock','online.lock'):
        with (state/name).open('r') as stream:fcntl.flock(stream,fcntl.LOCK_EX|fcntl.LOCK_NB)
    results.append('HUP closes worker anonymous staging and both locks without losing saved files')
    print(json.dumps({'result':'PASS','cases':results}))
finally:
    entry.write_bytes(original)
