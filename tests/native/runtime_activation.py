import json, os, secrets, subprocess, sys
from pathlib import Path
# Deliberate extra interlock: never change accounts on an ordinary Linux host.
from pathlib import Path
assert Path('/var/lib/project-cbm/native-staging-only').read_text()=='DISPOSABLE PCBM NAMESPACE\n'
assert Path('/run/systemd/container').read_text().strip()=='pcbm-staging'
os.chdir('/')
def run(args, data=None, timeout=70):
 return subprocess.run(args,input=data,text=True,capture_output=True,timeout=timeout)
def request(op,**values):
 p=run(['runuser','-u','pi','--','sudo','-n','--','/usr/libexec/pcbm-config-root'],json.dumps({'schema_version':1,'operation':op,'values':values}))
 try:answer=json.loads(p.stdout)
 except Exception:raise RuntimeError('invalid helper result') from None
 print(json.dumps({'operation':op,'exit':p.returncode,'status':answer['status']}),flush=True)
 return answer
assert run(['visudo','-cf','/etc/sudoers']).returncode==0
# No arbitrary root command or helper argv permitted.
assert run(['runuser','-u','pi','--','sudo','-n','--','/usr/bin/id']).returncode!=0
assert run(['runuser','-u','pi','--','sudo','-n','--','/usr/libexec/pcbm-config-root','evil']).returncode!=0
assert request('command',value='id')['status']=='invalid'
assert request('setup-finish')['status']=='invalid'
assert request('setup-region',locale='en_US.UTF-8',keyboard='us',timezone='America/Phoenix')['status']=='ok'
password=secrets.token_urlsafe(24)
try:
 assert request('setup-owner',password=password)['status']=='ok'
 p=run(['runuser','-u','pcbm','--','sudo','-k','-S','-p','','--','/usr/bin/id','-u'],password+'\n')
 assert p.returncode==0 and p.stdout.strip()=='0'
 print('Authenticated owner sudo: PASS',flush=True)
 assert run(['systemctl','unmask','NetworkManager.service']).returncode==0
 assert run(['systemctl','start','NetworkManager.service']).returncode==0
 assert request('setup-network',enabled=False)['status']=='ok'
 # Root growth passed separately on a disposable image; this harness injects
 # its completion projection because namespace root is deliberately not a disk.
 marker=Path('/var/lib/project-cbm/first-boot/complete.json')
 marker.parent.mkdir(exist_ok=True,parents=True)
 marker.write_text('{"schema_version":1,"root_growth_verified":true}\n')
 marker.chmod(0o600)
 assert request('setup-finish')['status']=='ok'
 assert request('setup-owner',password=secrets.token_urlsafe(24))['status']=='invalid'
 print('First-boot completion and locked-out reset: PASS',flush=True)
 assert request('sharing-password',password=password)['status']=='ok'
 sys.path.insert(0,'/usr/share/project-cbm/runtime')
 from project_cbm.config_backend import Linux
 print(json.dumps({'samba_credential_ready':Linux().credential_ready('pcbm')}),flush=True)
 assert Linux().credential_ready('pcbm')
 assert run(['sshd','-t']).returncode!=0 # no sealed host keys
 assert Linux().ssh_keys()
 assert run(['sshd','-t']).returncode==0
 print('Fresh SSH key generation/configuration: PASS',flush=True)
finally:
 run(['usermod','--password','!','pcbm'])
 run(['smbpasswd','-x','pcbm'])
 password=None
