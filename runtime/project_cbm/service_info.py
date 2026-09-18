"""Small appliance projection owned by pcbm-info; no saved secrets or private stores."""
import json
import re

UNITS = {'ssh':'ssh.service','sharing':'smbd.service','modem':'tcpser.service','discovery':'avahi-daemon.service'}
PORTS = {'ssh':('tcp',22),'sharing':('tcp',445),'discovery':('udp',5353)}


def units(raw):
    rows={}
    for block in raw.strip().split('\n\n'):
        fields=dict(line.split('=',1) for line in block.splitlines() if '=' in line)
        for name,unit in UNITS.items():
            if fields.get('Id')==unit:
                rows[name]={key:fields.get(key) for key in ('LoadState','ActiveState','SubState','UnitFileState')}
    return rows


def listeners(raw):
    ports=set()
    for line in raw.splitlines():
        fields=line.split()
        if len(fields)<6 or fields[0] not in ('tcp','udp'):continue
        match=re.search(r':([0-9]+)$',fields[4])
        if match:ports.add((fields[0],int(match[1])))
    return ports


def state(row, listening):
    if not row or row.get('LoadState') in ('not-found','masked','error') or row.get('UnitFileState')=='masked':return 'unavailable'
    active=row.get('ActiveState')
    if active=='failed':return 'failed'
    if active in ('activating','deactivating','reloading'):return 'pending'
    if active=='active':return 'on' if listening is True else 'pending' if listening is False else 'unavailable'
    if active=='inactive':return 'pending' if row.get('UnitFileState') in ('enabled','enabled-runtime') else 'off'
    return 'unavailable'


def collect(source, attempt, interfaces=None, runtime=None):
    def query(argv,parser):
        code,raw=source.command(argv)
        if code:raise ValueError('command')
        return parser(raw)
    if runtime is None:
        runtime=attempt('appliance_services',lambda:query(['/usr/bin/systemctl','--system','--no-pager','show','--property=Id,LoadState,ActiveState,SubState,UnitFileState',*UNITS.values()],units),{})
    ports=attempt('appliance_listeners',lambda:query(['/usr/bin/ss','-H','-ltnu'],listeners))
    def read_json(path):
        value=json.loads(source.read(path))
        if not isinstance(value,dict):raise ValueError('object')
        return value
    def account():
        p=read_json('/etc/project-cbm/configuration-policy.json')
        owner=p['owner_user']
        if not isinstance(owner,str) or not re.fullmatch('[a-z][a-z0-9_-]{0,30}',owner):raise ValueError('owner')
        return owner
    owner=attempt('appliance_owner',account)
    def hostname():
        value=source.uname()['hostname']
        if not isinstance(value,str) or not re.fullmatch(r'[a-z][a-z0-9-]{0,61}[a-z0-9]|[a-z]',value):raise ValueError('hostname')
        return value
    computer=attempt('appliance_computer',hostname)
    def sharing():
        p=read_json('/var/lib/project-cbm/sharing-status.json')
        if p!={'schema_version':1,'username':owner,'password_set':True}:raise ValueError('sharing_status')
        return True
    password_set=attempt('sharing_enrollment',sharing,False) if source.exists('/var/lib/project-cbm/sharing-status.json') else False
    modem_port=25232
    def modem():
        p=read_json('/etc/project-cbm/modem.json');port=p['port']
        if type(port) is not int or not 1024<=port<=65535:raise ValueError('modem_port')
        return port
    modem_port=attempt('modem_port',modem,25232)
    services={}
    for name in UNITS:
        row=runtime.get(name) if runtime else None
        expected=PORTS.get(name,('tcp',modem_port))
        listening=None if ports is None else expected in ports
        enabled=None if not row else row.get('UnitFileState') in ('enabled','enabled-runtime')
        services[name]={'state':state(row,listening),'enabled':enabled,'listening':listening}
    return {'format':'project-cbm.appliance-info','schema_version':1,'computer_name':computer,
            'owner_username':owner,'sharing_username':owner,'sharing_password_set':password_set,
            'share_name':'Project CBM','interfaces':interfaces,'services':services,'modem_port':modem_port}
