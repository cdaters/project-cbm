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
import re
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
    def run(self,argv,stdin=None):
        # No shell, raw error logging, inherited environment or command return text.
        return subprocess.run(argv,input=stdin,text=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,
                              env=ENV,timeout=60,check=False).returncode==0

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

    def credential_ready(self, user):
        p=subprocess.run(['/usr/bin/pdbedit','-L','-u',user],capture_output=True,text=True,env=ENV,timeout=5)
        return p.returncode==0 and any(line.startswith(user+':') for line in p.stdout.splitlines())

    def country_ready(self):
        p=subprocess.run(['/usr/bin/raspi-config','nonint','get_wifi_country'],capture_output=True,text=True,env=ENV,timeout=5)
        country=p.stdout.strip()
        return p.returncode==0 and match(country,r'[A-Z]{2}') and self.listed('country',country)

    def write(self,path,content):
        path=Path(path);trusted(path.parent)
        if path.exists() or path.is_symlink():trusted(path)
        fd,tmp=tempfile.mkstemp(prefix='.pcbm-',dir=path.parent)
        try:
            with os.fdopen(fd,'w') as f:f.write(content);f.flush();os.fsync(f.fileno())
            os.replace(tmp,path)
            d=os.open(path.parent,os.O_DIRECTORY);os.fsync(d);os.close(d)
        finally:
            if os.path.exists(tmp):os.unlink(tmp)


def apply(request, p, system):
    """Injectable executor; tests supply a fake OS. Caller serializes real mutations."""
    validate(request);op=request['operation'];v=request['values']
    if not p['system_ready']:return result('pending')
    if op in ('network','wifi-enroll','wifi-country') and not p['network_ready']:return result('pending')
    if op=='service':
        name=v['service']
        if name not in p['ready_services']:return result('pending')
        if name=='sharing' and v['enabled'] and not system.credential_ready(p['appliance_user']):return result('credentials_required')
        # No unmask here. Masks are an intentional policy boundary, not an error to bypass.
        args=['/usr/bin/systemctl','--no-ask-password','enable' if v['enabled'] else 'disable','--now',SERVICES[name]]
    elif op=='hostname':args=['/usr/bin/hostnamectl','--no-ask-password','hostname',v['value']]
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
        if not system.country_ready():return result('invalid')
        if not system.run(['/usr/bin/nmcli','networking','on']):return result('failed')
        if not system.run(['/usr/bin/nmcli','radio','wifi','on']):return result('failed')
        system.write(path,keyfile(v['ssid'],v['password']))
        if not system.run(['/usr/bin/nmcli','connection','load',path]):return result('failed')
        args=['/usr/bin/nmcli','--wait','30','connection','up','uuid',WIFI_UUID]
    elif op=='sharing-password':
        # Initial credential enrollment precedes adding sharing to ready_services.
        ok=system.run(['/usr/bin/smbpasswd','-s','-a',p['appliance_user']],stdin=v['password']+'\n'+v['password']+'\n')
        return result('ok' if ok else 'failed')
    elif op=='modem':
        system.write('/etc/project-cbm/modem.json',json.dumps({'schema_version':1,**v},sort_keys=True)+'\n')
        return result('saved_pending')  # Typed intent only; safe TCPser adapter/listener qualification is a later gate.
    elif op=='power':args=['/usr/bin/systemctl','--no-ask-password',v['action']]
    else:return result('invalid')
    return result('ok' if system.run(args) else 'failed')


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
