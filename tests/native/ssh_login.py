import json,os,pty,secrets,select,signal,subprocess,time
from pathlib import Path
assert Path('/var/lib/project-cbm/native-staging-only').is_file()
assert Path('/run/systemd/container').read_text().strip()=='pcbm-staging'
os.chdir('/')
def run(args,data=None):return subprocess.run(args,input=data,text=True,capture_output=True,timeout=65)
def request(enabled):
 p=run(['runuser','-u','pcbm','--','sudo','-n','--','/usr/libexec/pcbm-config-root'],json.dumps({'schema_version':1,'operation':'service','values':{'service':'ssh','enabled':enabled}}))
 assert json.loads(p.stdout)['status']=='ok'
secret=secrets.token_urlsafe(24);pid=None
try:
 assert run(['chpasswd'],'pcbm:'+secret+'\n').returncode==0
 request(True)
 pid,fd=pty.fork()
 if pid==0:os.execvp('runuser',['runuser','-u','pcbm','--','ssh','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','NumberOfPasswordPrompts=1','pcbm@127.0.0.1','id','-u'])
 raw=b'';sent=False;end=time.monotonic()+10
 while time.monotonic()<end:
  if select.select([fd],[],[],.1)[0]:
   try:data=os.read(fd,8192)
   except OSError:break
   if not data:break
   raw=(raw+data)[-32768:]
   if b'password:' in raw.lower() and not sent:os.write(fd,secret.encode()+b'\n');sent=True
 assert sent and b'1000\r\n' in raw and secret.encode() not in raw
 os.close(fd);os.waitpid(pid,0);pid=None
 request(False)
 assert run(['ssh','-o','BatchMode=yes','-o','ConnectTimeout=2','pcbm@127.0.0.1','true']).returncode!=0
 print(json.dumps({'local_ssh_owner_password_login_uid1000':'PASS','secret_not_echoed':'PASS','new_connection_after_disable':'REFUSED','physical_other_computer':'UNTESTED'}))
finally:
 if pid:
  try:os.kill(pid,signal.SIGKILL);os.waitpid(pid,0)
  except (ProcessLookupError,ChildProcessError):pass
 try:request(False)
 except Exception:pass
 run(['usermod','--password','!','pcbm']);secret=None
