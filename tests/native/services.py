"""Opt-in native service revalidation inside the guarded disposable namespace."""
import json,os,secrets,subprocess,sys,time
from pathlib import Path
assert Path('/var/lib/project-cbm/native-staging-only').read_text()=='DISPOSABLE PCBM NAMESPACE\n'
assert Path('/run/systemd/container').read_text().strip()=='pcbm-staging'
os.chdir('/');sys.path.insert(0,'/usr/share/project-cbm/runtime')
from project_cbm.config_backend import Linux
from project_cbm.configuration import keyfile,WIFI_UUID

def run(args,data=None):return subprocess.run(args,input=data,text=True,capture_output=True,timeout=65)
def request(op,**values):
 p=run(['runuser','-u','pcbm','--','sudo','-n','--','/usr/libexec/pcbm-config-root'],json.dumps({'schema_version':1,'operation':op,'values':values}))
 answer=json.loads(p.stdout);print(json.dumps({'operation':op,'status':answer['status']}),flush=True)
 assert answer['status']=='ok';return answer
secret=secrets.token_urlsafe(24)+';\\ test'
path=Path('/etc/NetworkManager/system-connections/pcbm-wifi.nmconnection')
try:
 request('sharing-password',password=secret)
 request('modem',port=25232,baud=2400)
 for friendly,unit in [('ssh','ssh'),('sharing','smbd'),('modem','tcpser'),('discovery','avahi-daemon')]:
  request('service',service=friendly,enabled=True)
  assert run(['systemctl','is-active',unit]).returncode==0
  if friendly=='modem':
   for i in range(30):
    listeners=run(['ss','-ltnp']).stdout
    if ':25232' in listeners:break
    time.sleep(.1)
   assert '127.0.0.1:25232' in listeners
  request('service',service=friendly,enabled=False)
  assert run(['systemctl','is-active',unit]).returncode!=0
 print('SSH/Samba/TCPser/mDNS start/stop and loopback modem listener: PASS',flush=True)
 request('network',enabled=True)
 Linux().write(path,keyfile('CBM synthetic staging',secret))
 assert path.stat().st_mode&0o777==0o600
 assert run(['nmcli','connection','load',str(path)]).returncode==0
 observed=run(['nmcli','--escape','no','--show-secrets','-g','802-11-wireless-security.psk','connection','show','uuid',WIFI_UUID])
 assert observed.returncode==0 and observed.stdout.rstrip('\n')==secret
 # No radio exists: fail cleanly, without printing credentials.
 assert run(['nmcli','--wait','2','connection','up','uuid',WIFI_UUID]).returncode!=0
 request('wifi-forget');request('network',enabled=False)
 report=run(['runuser','-u','pcbm','--','pcbm-info','--json'])
 assert report.returncode==0 and json.loads(report.stdout)['schema_version']==1
 assert secret not in report.stdout
 for binary in ('pcbm-config','pcbm-first-run','pcbm-start-profile','pcbm-admin'):
  assert Path('/usr/bin',binary).is_file()
 print('NetworkManager keyfile parsing/redaction, offline path, installed info/config/boot interfaces: PASS',flush=True)
finally:
 run(['nmcli','connection','delete','uuid',WIFI_UUID]);path.unlink(missing_ok=True)
 run(['smbpasswd','-x','pcbm'])
 for p in Path('/etc/ssh').glob('ssh_host_*'):p.unlink()
 secret=None
