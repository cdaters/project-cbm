"""Actual installed local service/account contracts in the isolated test namespace."""
import json,os,secrets,subprocess,sys,time
from pathlib import Path
assert Path('/var/lib/project-cbm/native-staging-only').read_text()=='DISPOSABLE PCBM NAMESPACE\n'
assert Path('/run/systemd/container').read_text().strip()=='pcbm-staging'
os.chdir('/');sys.path.insert(0,'/usr/share/project-cbm/runtime')
from project_cbm import info

def run(args,data=None):return subprocess.run(args,input=data,text=True,capture_output=True,timeout=65)
def request(op,**values):
 p=run(['runuser','-u','pi','--','sudo','-n','--','/usr/libexec/pcbm-config-root'],json.dumps({'schema_version':1,'operation':op,'values':values}))
 assert json.loads(p.stdout)['status']=='ok',op

def snapshot():
 p=run(['runuser','-u','pi','--','pcbm-info','--json','--appliance']);assert p.returncode==0;return json.loads(p.stdout)
secret=secrets.token_urlsafe(24)
checks={}
try:
 request('hostname',value='projectcbm-test');d=snapshot();assert d['computer_name']=='projectcbm-test'
 assert 'projectcbm-test' in run(['getent','hosts','projectcbm-test']).stdout
 request('hostname',value='projectcbm');checks['computer_name_change_local_resolution']=True
 request('sharing-password',password=secret)
 marker=Path('/var/lib/project-cbm/sharing-status.json');assert marker.stat().st_mode&0o777==0o644
 assert secret not in marker.read_text();assert snapshot()['sharing_password_set']
 checks['safe_enrollment_projection']=True
 for name,unit in [('ssh','ssh'),('sharing','smbd'),('modem','tcpser'),('discovery','avahi-daemon')]:
  request('service',service=name,enabled=True);d=snapshot();assert d['services'][name]['state']=='on',(name,d['services'][name])
  assert run(['systemctl','is-enabled',unit]).stdout.strip()=='enabled'
  assert run(['systemctl','restart',unit]).returncode==0
  end=time.monotonic()+5
  while time.monotonic()<end:
   if snapshot()['services'][name]['state']=='on':break
   time.sleep(.1)
  else:raise AssertionError('restart readiness')
  if name=='sharing':
   assert snapshot()['services']['discovery']['state']=='on'
   cfg=run(['testparm','-s','--parameter-name=valid users','--section-name=Project CBM']);assert cfg.stdout.strip()=='owner'
   assert run(['testparm','-s','--parameter-name=force user','--section-name=Project CBM']).stdout.strip()=='pi'
   assert run(['testparm','-s','--parameter-name=path','--section-name=Project CBM']).stdout.strip()=='/home/pi/pcbm'
   assert 'WITH_AVAHI_SUPPORT' in run(['smbd','-b']).stdout
   checks['samba_avahi_build_and_owner_share_config']=True
  request('service',service=name,enabled=False);assert snapshot()['services'][name]['state']=='off'
  assert run(['systemctl','is-enabled',unit]).stdout.strip()=='disabled'
  checks[name+'_actual_on_restart_enabled_off_disabled']=True
 d=snapshot();assert d['owner_username']==d['sharing_username']=='owner'
 for args in (['pcbm-info','--json'],['pcbm-info','--json','--appliance']):
  assert secret not in run(['runuser','-u','pi','--',*args]).stdout
 checks['owner_contract_and_redaction']=True
 print(json.dumps({'result':'PASS','checks':checks,'physical_clients_and_reboot':'UNTESTED; restart and enablement are native persistence evidence only'},indent=2))
finally:
 for name in ('ssh','sharing','modem','discovery'):
  try:request('service',service=name,enabled=False)
  except Exception:pass
 run(['smbpasswd','-x','owner']);marker=Path('/var/lib/project-cbm/sharing-status.json');marker.unlink(missing_ok=True)
 secret=None
