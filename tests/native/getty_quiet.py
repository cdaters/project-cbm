"""Installed agetty/login/PAM through a PTY in disposable native staging only."""
import os,pty,select,signal,time,json,re
from pathlib import Path
assert os.geteuid()==0
assert Path('/var/lib/project-cbm/native-staging-only').read_text()=='DISPOSABLE PCBM NAMESPACE\n'
pid,fd=pty.fork()
if pid==0:
 os.environ['TERM']='xterm';os.environ['HISTFILE']='/dev/null'
 os.execv('/sbin/agetty',['agetty','--autologin','pcbm','--skip-login','--noissue','--nohostname','--noclear','-','xterm'])
data=b'';sent=False;status=None
try:
 deadline=time.monotonic()+15
 while time.monotonic()<deadline:
  if select.select([fd],[],[],.1)[0]:
   try:part=os.read(fd,4096)
   except OSError:part=b''
   data+=part
   if not sent and re.search(rb'\$\x1b\[00m ',data):
    os.write(fd,b"printf 'QUALIFIED_UID:%s\\n' \"$(id -u)\"; exit\n");sent=True
  got,status=os.waitpid(pid,os.WNOHANG)
  if got:break
 else:
  os.kill(pid,signal.SIGKILL);os.waitpid(pid,0);raise AssertionError(('getty/login timeout',repr(data[-600:])))
 assert sent and b'QUALIFIED_UID:1000' in data,(status,len(data))
 assert b'automatic login' not in data and b'My IP address' not in data
 print(json.dumps({'result':'PASS','agetty_login_PAM_uid':1000,'automatic_login_announcement_suppressed':True,'issue_suppressed':True,'physical_tty1':'UNTESTED'}))
finally:os.close(fd)
