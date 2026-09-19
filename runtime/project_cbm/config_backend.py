"""Root-only, fixed-operation backend. Disabled until trusted activation policy exists.

Never install this development source by running it with sudo. The future package
installs a fixed isolated entry point and validates ownership before granting access.
"""
import fcntl
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import time
import re
import pwd
import grp
import xml.etree.ElementTree as ET
from .configuration import decode, validate, result, SERVICES, keyfile, match, WIFI_UUID
from .data import read_json

POLICY=Path('/etc/project-cbm/configuration-policy.json')
ENV={'PATH':'/usr/sbin:/usr/bin:/sbin:/bin','LC_ALL':'C','SYSTEMD_PAGER':'cat','SYSTEMD_COLORS':'0','HOME':'/run/project-cbm'}


def trusted(path):
    # No symlinks in any directory/file in this privileged trust chain.
    for p in (path,*path.parents):
        s=p.lstat()
        if stat.S_ISLNK(s.st_mode) or s.st_uid!=0 or s.st_mode & 0o022:raise ValueError('unsafe_system_path')
    return path


def policy():
    p=read_json(trusted(POLICY))
    if not isinstance(p,dict) or set(p)!={'schema_version','owner_user','appliance_user','system_ready','network_ready','ready_services'}:raise ValueError('policy')
    if type(p['schema_version']) is not int or p['schema_version']!=1:raise ValueError('policy')
    if p['appliance_user']!='pi':raise ValueError('appliance_account')
    if not all(match(p[k],r'[a-z][a-z0-9_-]{0,30}') for k in ('owner_user','appliance_user')) or p['owner_user'] in ('root',p['appliance_user']):raise ValueError('policy_account')
    if any(type(p[k]) is not bool for k in ('system_ready','network_ready')):raise ValueError('policy')
    if not isinstance(p['ready_services'],list) or any(x not in SERVICES for x in p['ready_services']):raise ValueError('policy_services')
    return p


class Linux:
    def __init__(self):
        # One budget across a compound request, below the client's 75s limit.
        self.deadline=time.monotonic()+65

    def run(self,argv,stdin=None):
        # No shell, raw error logging, inherited environment or command return text.
        remaining=self.deadline-time.monotonic()
        if remaining<=0:raise subprocess.TimeoutExpired(argv,65)
        return subprocess.run(argv,input=stdin,text=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,
                              env=ENV,timeout=min(60,remaining),check=False).returncode==0

    def service(self, name, enabled):
        from .service_info import units, listeners, state, PORTS
        # File Sharing opt-in includes local discovery, stated in its UI action.
        if name=='sharing' and enabled and not self.service('discovery',True):return False
        args=['/usr/bin/systemctl','--no-ask-password','enable' if enabled else 'disable','--now',SERVICES[name]]
        if name=='discovery':args.append('avahi-daemon.socket')
        if not self.run(args):return False
        end=min(self.deadline,time.monotonic()+3)
        port=25232
        if name=='modem':port=read_json(trusted(Path('/etc/project-cbm/modem.json')))['port']
        expected=PORTS.get(name,('tcp',port))
        while time.monotonic()<end:
            try:
                def query(argv):
                    remaining=end-time.monotonic()
                    if remaining<=0:raise TimeoutError()
                    p=subprocess.run(argv,capture_output=True,text=True,env=ENV,timeout=min(1,remaining))
                    if p.returncode or len(p.stdout)>65536:raise ValueError('service_query')
                    return p.stdout
                rows=units(query(['/usr/bin/systemctl','--system','--no-pager','show','--property=Id,LoadState,ActiveState,SubState,UnitFileState',SERVICES[name]]))
                listening=expected in listeners(query(['/usr/bin/ss','-H','-ltnu']))
                actual=state(rows.get(name),listening)
                if enabled and actual=='on' or not enabled and actual=='off' and not listening:return True
            except (OSError,ValueError,subprocess.SubprocessError):pass
            time.sleep(min(.1,max(0,end-time.monotonic())))
        return False

    def listed(self,kind,value):
        if kind=='country':
            return value in {line.split()[0] for line in Path('/usr/share/zoneinfo/iso3166.tab').read_text().splitlines() if line and not line.startswith('#')}
        if kind=='locale':
            return value in {line.split()[0] for line in Path('/usr/share/i18n/SUPPORTED').read_text().splitlines() if line.endswith(' UTF-8')}
        if kind=='timezone':
            p=Path('/usr/share/zoneinfo')/value
            return p.is_file() and p.resolve().is_relative_to(Path('/usr/share/zoneinfo'))
        if kind=='keyboard':
            layouts=ET.parse('/usr/share/X11/xkb/rules/base.xml')
            return value in {n.text for n in layouts.findall('./layoutList/layout/configItem/name')}
        return False

    def keyboard(self, layout):
        # Debian console-setup owns this file. Preserve model/variant/options and
        # comments, replace only layout; never source it in this process.
        path=trusted(Path('/etc/default/keyboard'))
        if path.stat().st_size>65536:raise ValueError('keyboard_size')
        old=path.read_text()
        lines=[line for line in old.splitlines() if not re.match(r'^\s*(?:export\s+)?XKBLAYOUT\s*=',line)]
        self.write(path,'\n'.join(lines)+f'\nXKBLAYOUT="{layout}"\n')
        # Compile for next boot; do not seize tty1 or force a live keymap reload.
        return self.run(['/usr/bin/setupcon','--save-only','--keyboard-only'])

    def hostname(self, value):
        path=trusted(Path('/etc/hosts'))
        if path.stat().st_size>65536:raise ValueError('hosts_size')
        lines=path.read_text().splitlines();found=False;updated=[]
        for line in lines:
            fields=line.split('#',1)[0].split()
            if fields and fields[0]=='127.0.1.1':
                # Preserve additional administrator aliases and comments.
                comment=(' #'+line.split('#',1)[1]) if '#' in line else ''
                line='127.0.1.1\t'+' '.join([value,*fields[2:]])+comment
                found=True
            updated.append(line)
        if not found:updated.append('127.0.1.1\t'+value)
        if not self.run(['/usr/bin/hostnamectl','--no-ask-password','hostname',value]):return False
        self.write(path,'\n'.join(updated)+'\n',0o644)
        return True

    def credential_ready(self, user):
        p=subprocess.run(['/usr/bin/pdbedit','-L','-v','-u',user],capture_output=True,text=True,env=ENV,timeout=5)
        flags=re.search(r'^Account Flags:\s*\[([^]]+)\]',p.stdout,re.M)
        return p.returncode==0 and flags is not None and 'D' not in flags[1] and 'N' not in flags[1]

    def country_ready(self):
        p=subprocess.run(['/usr/bin/raspi-config','nonint','get_wifi_country'],capture_output=True,text=True,env=ENV,timeout=5)
        country=p.stdout.strip()
        return p.returncode==0 and match(country,r'[A-Z]{2}') and self.listed('country',country)

    def wifi_rescan(self):
        from .wifi_scan import scan
        original_deadline = self.deadline
        self.deadline = min(self.deadline,time.monotonic()+25)
        def query(argv):
            remaining = self.deadline-time.monotonic()
            if remaining <= 0: return None
            try:
                p = subprocess.run(argv, capture_output=True, text=True, env=ENV,
                                   timeout=min(1,remaining), check=False)
                return p.stdout if p.returncode == 0 and len(p.stdout) <= 65536 else None
            except (OSError,subprocess.SubprocessError): return None
        def request(argv):
            try: return self.run(argv)
            except (OSError,subprocess.SubprocessError): return False
        try: observation = scan(query, request, self.deadline)
        finally: self.deadline = original_deadline
        self.write('/var/lib/project-cbm/setup/wifi-scan.json',
                   json.dumps(observation,sort_keys=True)+'\n',0o644)
        return observation['result']=='complete'

    def write(self,path,content,mode=0o600):
        path=Path(path);trusted(path.parent)
        if path.exists() or path.is_symlink():trusted(path)
        fd,tmp=tempfile.mkstemp(prefix='.pcbm-',dir=path.parent)
        try:
            with os.fdopen(fd,'w') as f:
                os.fchmod(f.fileno(),mode);f.write(content);f.flush();os.fsync(f.fileno())
            os.replace(tmp,path)
            d=os.open(path.parent,os.O_DIRECTORY);os.fsync(d);os.close(d)
        finally:
            if os.path.exists(tmp):os.unlink(tmp)


    def setup_read(self):
        from .setup import STATE, initial
        trusted(STATE.parent)
        if not STATE.exists():return initial()
        return read_json(trusted(STATE))

    def setup_save(self,state):
        from .setup import STATE, STATUS
        self.write(STATE,json.dumps(state,sort_keys=True)+'\n')
        # Safe projection only; status has no credentials or machine identifiers.
        self.write(STATUS,json.dumps(state,sort_keys=True)+'\n',0o644)

    def owner_expected(self,user):
        try:
            account=pwd.getpwnam(user)
            return (user=='pcbm' and account.pw_uid==1001 and account.pw_dir=='/home/pcbm'
                    and account.pw_shell=='/bin/bash' and user in grp.getgrnam('sudo').gr_mem)
        except KeyError:return False

    def owner_ready(self,user):
        if not self.owner_expected(user):return False
        for line in trusted(Path('/etc/shadow')).read_text().splitlines():
            fields=line.split(':')
            if fields[0]==user:
                return len(fields)>1 and fields[1].startswith('$') and len(fields[1])>20
        return False

    def setup_prerequisites(self):
        growth=read_json(trusted(Path('/var/lib/project-cbm/first-boot/complete.json')))
        machine=trusted(Path('/etc/machine-id')).read_text().strip()
        return (growth=={'schema_version':1,'root_growth_verified':True}
                and re.fullmatch('[0-9a-f]{32}',machine) is not None and machine!='0'*32
                and self.run(['/usr/sbin/visudo','-c','-f','/etc/sudoers']))

    def setup_activate(self,p):
        self.write(POLICY,json.dumps({**p,'system_ready':True},sort_keys=True)+'\n',0o644)

    def ssh_keys(self):
        return self.run(['/usr/bin/ssh-keygen','-A'])

    def modem(self,values):
        self.write('/etc/project-cbm/modem.json',json.dumps({'schema_version':1,**values},sort_keys=True)+'\n',0o644)
        # Only restart an already active service. Saving settings never enables it.
        if self.run(['/usr/bin/systemctl','--quiet','is-active','tcpser.service']):
            return self.run(['/usr/bin/systemctl','--no-ask-password','restart','tcpser.service'])
        return True


def apply(request, p, system):
    """Injectable executor; tests supply a fake OS. Caller serializes real mutations."""
    validate(request);op=request['operation'];v=request['values']
    if op.startswith('setup-'):
        from .setup import apply as setup_apply
        return setup_apply(request,p,system,apply)
    if not p['system_ready']:return result('pending')
    if op in ('network','wifi-enroll','wifi-country','wifi-disconnect','wifi-forget','wifi-rescan') and not p['network_ready']:return result('pending')
    if op=='service':
        name=v['service']
        if name not in p['ready_services']:return result('pending')
        if name=='sharing' and v['enabled'] and not system.credential_ready(p['owner_user']):return result('credentials_required')
        if name=='sharing' and v['enabled'] and 'discovery' not in p['ready_services']:return result('pending')
        if name=='ssh' and v['enabled'] and not system.ssh_keys():return result('failed')
        return result('ok' if system.service(name,v['enabled']) else 'failed')
    elif op=='hostname':return result('ok' if system.hostname(v['value']) else 'failed')
    elif op=='timezone':
        if not system.listed('timezone',v['value']):return result('invalid')
        args=['/usr/bin/timedatectl','--no-ask-password','set-timezone',v['value']]
    elif op=='locale':
        if not system.listed('locale',v['value']):return result('invalid')
        if not system.run(['/usr/bin/localedef','-i',v['value'].split('.')[0],'-f','UTF-8',v['value']]):return result('failed')
        args=['/usr/sbin/update-locale','LANG='+v['value']]
    elif op=='keyboard':
        if not system.listed('keyboard',v['value']):return result('unavailable')
        return result('saved_restart' if system.keyboard(v['value']) else 'failed')
    elif op=='wifi-country':
        # The vendor adapter also enables the radio. UI confirmation makes this explicit.
        if not system.listed('country',v['value']):return result('invalid')
        args=['/usr/bin/raspi-config','nonint','do_wifi_country',v['value']]
    elif op=='network':args=['/usr/bin/nmcli','networking','on' if v['enabled'] else 'off']
    elif op=='wifi-enroll':
        # Country must have been configured separately; readiness gate enforces activation.
        path='/etc/NetworkManager/system-connections/pcbm-wifi.nmconnection'
        if not system.country_ready():return result('wifi_country_required')
        if not system.run(['/usr/bin/nmcli','networking','on']):return result('failed')
        if not system.run(['/usr/bin/nmcli','radio','wifi','on']):return result('failed')
        system.write(path,keyfile(v['ssid'],v['password']))
        if not system.run(['/usr/bin/nmcli','connection','load',path]):return result('failed')
        args=['/usr/bin/nmcli','--wait','30','connection','up','uuid',WIFI_UUID]
    elif op=='wifi-rescan':
        return result('ok' if system.wifi_rescan() else 'wifi_scan_unconfirmed')
    elif op in ('wifi-disconnect','wifi-forget'):
        args=['/usr/bin/nmcli','connection','down' if op=='wifi-disconnect' else 'delete','uuid',WIFI_UUID]
    elif op=='sharing-password':
        # Initial credential enrollment precedes adding sharing to ready_services.
        ok=system.run(['/usr/bin/smbpasswd','-s','-a',p['owner_user']],stdin=v['password']+'\n'+v['password']+'\n')
        if ok:ok=system.credential_ready(p['owner_user'])
        if ok:system.write('/var/lib/project-cbm/sharing-status.json',json.dumps({'schema_version':1,'username':p['owner_user'],'password_set':True})+'\n',0o644)
        return result('ok' if ok else 'failed')
    elif op=='modem':
        return result('ok' if system.modem(v) else 'failed')
    elif op=='power':args=['/usr/bin/systemctl','--no-ask-password',v['action']]
    else:return result('invalid')
    try:ok=system.run(args)
    except subprocess.TimeoutExpired:ok=False
    return result('ok' if ok else 'wifi_failed' if op=='wifi-enroll' else 'failed')


def main():
    answer=result('invalid')
    try:
        if len(sys.argv)!=1 or os.geteuid()!=0:raise ValueError('invocation')
        request=decode(sys.stdin.buffer.read(4097))
        try:p=policy()
        except (OSError,ValueError,TypeError):p=None
        if p is None:answer=result('pending')
        else:
            # Parent directory created root:root 0755 by future package, never by user request.
            directory=trusted(Path('/run/project-cbm'))
            fd=os.open(directory/'configuration.lock',os.O_CREAT|os.O_RDWR|os.O_NOFOLLOW|os.O_NONBLOCK,0o600)
            try:
                s=os.fstat(fd)
                if s.st_uid!=0 or not stat.S_ISREG(s.st_mode) or s.st_nlink!=1 or s.st_mode & 0o077:raise ValueError('lock')
                fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
                answer=apply(request,p,Linux())
            finally:os.close(fd)
    except BlockingIOError:answer=result('busy')
    except (ValueError,TypeError,KeyError,ET.ParseError):answer=result('invalid')
    except (OSError,subprocess.SubprocessError):answer=result('failed')
    print(json.dumps(answer,sort_keys=True))
    return 0 if answer['status'] in ('ok','saved_pending','saved_restart') else 2
