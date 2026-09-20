"""Only inside an isolated disposable appliance: one user, authenticated root."""
import os,subprocess,secrets,pty,select,time,signal,json
from pathlib import Path
assert Path('/var/lib/project-cbm/native-staging-only').read_text()=='DISPOSABLE PCBM NAMESPACE\n'
assert Path('/run/systemd/container').read_text().strip()=='pcbm-staging'
os.chdir('/')
def run(args,stdin=None):return subprocess.run(args,input=stdin,text=True,capture_output=True,timeout=20)
secret=secrets.token_urlsafe(24)
def shell(action,expected_uid):
 pid,fd=pty.fork()
 if pid==0:
  os.environ['TERM']='xterm'
  os.execvp('runuser',['runuser','-u','pcbm','--','/usr/bin/pcbm-admin',action])
 seen=b'';sent=False;command=False;deadline=time.monotonic()+20
 try:
  while time.monotonic()<deadline:
   if select.select([fd],[],[],.1)[0]:
    try:data=os.read(fd,8192)
    except OSError:break
    if not data:break
    seen=(seen+data)[-32768:]
    if action=='owner' and not sent and b'password for pcbm:' in seen.lower():
     os.write(fd,secret.encode()+b'\n');sent=True
    if not command and (action=='terminal' or sent) and (b'$ ' in seen or b'# ' in seen):
     os.write(fd,b"printf '\\nCBMUID=%s\\n' \"$(id -u)\"; exit\n");command=True
   if os.waitpid(pid,os.WNOHANG)[0]:break
  assert command and f'CBMUID={expected_uid}\r\n'.encode() in seen,'shell identity/readiness'
  assert sent==(action=='owner') and secret.encode() not in seen
  print(json.dumps({'action':action,'uid':expected_uid,'password_required':sent,'secret_not_echoed':True}),flush=True)
 finally:
  os.close(fd)
  try:os.kill(pid,signal.SIGKILL);os.waitpid(pid,0)
  except (ProcessLookupError,ChildProcessError):pass
try:
 assert run(['chpasswd'],'pcbm:'+secret+'\n').returncode==0
 shell('terminal',1000)
 wrong=run(['runuser','-u','pcbm','--','sudo','-k','-S','-p','','--','/usr/bin/id','-u'],'invalid-fixture\n'*3)
 assert wrong.returncode!=0 and wrong.stdout.strip()!='0'
 shell('owner',0)
 # A cached authentication must not admit an unrelated fresh no-password admin call.
 denied=run(['runuser','-u','pcbm','--','sudo','-k','-n','--','/usr/bin/id','-u'])
 assert denied.returncode!=0
 computer=Path('/etc/hostname').read_text().strip()
 p=run(['runuser','-u','pcbm','--','sudo','-k','-S','-p','','--','/usr/bin/raspi-config','nonint','get_hostname'],secret+'\n')
 assert p.returncode==0 and p.stdout.strip()==computer
 print('Single-user terminal, authenticated root/vendor administration and rejection: PASS',flush=True)
finally:
 run(['runuser','-u','pcbm','--','sudo','-K'])
 run(['usermod','--password','!','pcbm']);secret=None
