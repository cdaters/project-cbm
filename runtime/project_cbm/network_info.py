"""Bounded, read-only live interface data. Never inspect saved connections or secrets."""
import ipaddress
import re
from .data import loads

IP = ['/usr/sbin/ip', '-j', 'address', 'show']
DEVICES = ['/usr/bin/nmcli', '--terse', '--escape', 'yes', '--fields',
           'GENERAL.DEVICE,GENERAL.TYPE,GENERAL.STATE', 'device', 'show']
WIFI = ['/usr/bin/nmcli', '--terse', '--escape', 'yes', '--fields',
        'DEVICE,ACTIVE,SSID', 'device', 'wifi', 'list', '--rescan', 'no']
STATES = {10:'unmanaged', 20:'unavailable', 30:'disconnected', 40:'connecting',
          50:'connecting', 60:'authentication-required', 70:'connecting',
          80:'connecting', 90:'connecting', 100:'connected', 110:'disconnecting', 120:'failed'}


def interface(value):
    if not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9_.:-]{1,15}', value):
        raise ValueError('interface')
    return value


def fields(line):
    """Decode nmcli terse separators without confusing escaped SSID colons/backslashes."""
    result=[]; cell=''; escaped=False
    for char in line:
        if escaped:
            if char not in ':\\': raise ValueError('nm_escape')
            cell+=char; escaped=False
        elif char=='\\': escaped=True
        elif char==':': result.append(cell); cell=''
        else: cell+=char
    if escaped: raise ValueError('nm_escape')
    return result+[cell]


def addresses(raw):
    data=loads(raw)
    if not isinstance(data,list) or len(data)>32: raise ValueError('interfaces')
    result=[]; seen=set()
    for d in data:
        if not isinstance(d,dict):raise ValueError('interface_record')
        name=interface(d['ifname'])
        if name in seen: raise ValueError('duplicate_interface')
        seen.add(name)
        if name=='lo': continue
        state=d.get('operstate','UNKNOWN')
        if not isinstance(state,str):raise ValueError('operstate')
        state=state.lower()
        if state not in ('up','down','unknown','dormant','lowerlayerdown','notpresent','testing'): raise ValueError('operstate')
        mac=d.get('address');mac=mac.lower() if isinstance(mac,str) and re.fullmatch(r'(?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}',mac) else None
        row={'interface':name,'type':'unknown','operstate':state,'state':'unknown',
             'ipv4':[],'ipv6':[],'mac':mac,'ssid':None}
        entries=d.get('addr_info',[])
        if not isinstance(entries,list) or len(entries)>16: raise ValueError('addresses')
        for entry in entries:
            if not isinstance(entry,dict):raise ValueError('address_record')
            flags=entry.get('flags',[])
            if not isinstance(flags,list) or not all(isinstance(v,str) for v in flags):raise ValueError('address_flags')
            family=entry.get('family')
            if family not in ('inet','inet6'): continue
            if entry.get('tentative') or entry.get('dadfailed') or set(entry.get('flags',[])) & {'tentative','dadfailed'}: continue
            if not isinstance(entry.get('local'),str):raise ValueError('address')
            address=ipaddress.ip_address(entry['local']);prefix=entry['prefixlen']
            if type(prefix) is not int or not 0<=prefix<=address.max_prefixlen or address.version!=(4 if family=='inet' else 6): raise ValueError('address')
            if address.is_unspecified or address.is_multicast or address.is_loopback: continue
            key='ipv4' if address.version==4 else 'ipv6'
            value=str(address)+'/'+str(prefix)
            if value not in row[key]:row[key].append(value)
            if len(row[key])>8:raise ValueError('address_count')
        result.append(row)
    return sorted(result,key=lambda row:row['interface'])


def devices(raw):
    result={}; current=None
    for line in raw.splitlines():
        if not line: continue
        parts=fields(line)
        if len(parts)!=2:raise ValueError('nm_fields')
        key,value=parts
        if key=='GENERAL.DEVICE':
            current=interface(value)
            if current in result or len(result)>=32:raise ValueError('nm_devices')
            result[current]={}
        elif key in ('GENERAL.TYPE','GENERAL.STATE') and current is not None:
            dest='type' if key=='GENERAL.TYPE' else 'state'
            if dest in result[current]:raise ValueError('nm_duplicate')
            if dest=='type': value={'ethernet':'ethernet','wifi':'wifi','bridge':'bridge','bond':'bond','tun':'tunnel','wireguard':'tunnel','loopback':'other'}.get(value,'other')
            else:
                match=re.fullmatch(r'(\d{1,3}) \([^\r\n]*\)',value)
                if not match:raise ValueError('nm_state')
                value=STATES.get(int(match[1]),'unknown')
            result[current][dest]=value
        else:raise ValueError('nm_key')
    if any(set(row)!={'type','state'} for row in result.values()):raise ValueError('nm_incomplete')
    return result


def active_ssids(raw):
    result={}
    for line in raw.splitlines():
        parts=fields(line)
        if len(parts)!=3:raise ValueError('wifi_fields')
        name,active,ssid=parts;interface(name)
        if active not in ('yes','no'):raise ValueError('wifi_active')
        if active=='no':continue
        if name in result:raise ValueError('wifi_duplicate')
        if not ssid or len(ssid.encode('utf-8'))>32 or not ssid.isprintable():raise ValueError('ssid')
        result[name]=ssid
    return result


def collect(source, attempt, include_ssids=True):
    def query(args, parser):
        code,raw=source.command(args)
        if code:raise ValueError('query_failed')
        return parser(raw)
    rows=attempt('network_addresses',lambda:query(IP,addresses))
    if rows is None:return None
    status=attempt('network_manager_devices',lambda:query(DEVICES,devices),{})
    for row in rows:row.update(status.get(row['interface'],{}))
    # A cached AP list only, never a scan; never confuse a connection name with SSID.
    if include_ssids and any(row['type']=='wifi' and row['state']=='connected' for row in rows):
        ssids=attempt('network_active_ssid',lambda:query(WIFI,active_ssids),{})
        for row in rows:
            if row['type']=='wifi' and row['state']=='connected':row['ssid']=ssids.get(row['interface'])
    return rows
