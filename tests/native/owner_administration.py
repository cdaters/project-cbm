import os,sys,subprocess,secrets,pty,select,time,signal,json
# Deliberate extra interlock: never change accounts on an ordinary Linux host.
from pathlib import Path
assert Path('/var/lib/project-cbm/native-staging-only').read_text()=='DISPOSABLE PCBM NAMESPACE\n'
assert Path('/run/systemd/container').read_text().strip()=='pcbm-staging'
os.chdir('/')
secret=secrets.token_urlsafe(24)
def run(args,stdin=None):return subprocess.run(args,input=stdin,text=True,capture_output=True,timeout=15)
def terminal(password,success):
 pid,fd=pty.fork()
 if pid==0:
  os.environ['TERM']='xterm'
  os.execvp('runuser',['runuser','-u','pi','--','/usr/bin/pcbm-admin','terminal'])
 seen=b'';sent=False;command=False;deadline=time.monotonic()+20
 try:
  while time.monotonic()<deadline:
   if select.select([fd],[],[],.1)[0]:
    try:data=os.read(fd,8192)
    except OSError:break
    if not data:break
    seen=(seen+data)[-32768:]
    if not sent and b'Password:' in seen:
     os.write(fd,password.encode()+b'\n');sent=True
    if success and sent and not command and b'owner@cbm-staging' in seen:
     os.write(fd,b"printf '\\nCBMUID=%s\\n' \"$(id -u)\"; exit\n");command=True
   p,status=os.waitpid(pid,os.WNOHANG)
   if p:break
  else:
   print(json.dumps({'harness_timeout':True,'sent':sent,'command_sent':command}),flush=True)
   raise RuntimeError('terminal timeout')
  assert (b'CBMUID=1001' in seen)==success
  assert secret.encode() not in seen
  print(json.dumps({'advanced_terminal_authentication':success,'expected_result':True,'secret_not_echoed':True}),flush=True)
 finally:
  os.close(fd)
  try:os.kill(pid,signal.SIGKILL);os.waitpid(pid,0)
  except (ProcessLookupError,ChildProcessError):pass
try:
 assert run(['chpasswd'],'owner:'+secret+'\n').returncode==0
 terminal('deliberately-invalid-password',False)
 terminal(secret,True)
 # Actual authenticated vendor invocation: no hardware country is presumed.
 p=run(['runuser','-u','owner','--','sudo','-k','-S','-p','','--','/usr/bin/raspi-config','nonint','get_hostname'],secret+'\n')
 assert p.returncode==0 and p.stdout.strip()=='cbm-staging'
 print('Authenticated raspi-config noninteractive invocation: PASS',flush=True)
finally:
 run(['usermod','--password','!','owner']);secret=None
