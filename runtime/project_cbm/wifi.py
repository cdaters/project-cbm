"""Read NetworkManager's scan cache; no credentials, addresses or direct radio IO."""
import json
import subprocess
from .config_backend import ENV


def split(line):
    fields=[''];escaped=False
    for c in line:
        if escaped:fields[-1]+=c;escaped=False
        elif c=='\\':escaped=True
        elif c==':':fields.append('')
        else:fields[-1]+=c
    if escaped:raise ValueError('trailing_escape')
    return fields


def parse(raw):
    if len(raw)>65536:raise ValueError('size')
    rows={}
    for line in raw.splitlines():
        fields=split(line)
        if len(fields)!=3:continue
        name,strength,security=fields
        if not name or not name.isprintable() or len(name.encode())>32:continue
        if not strength.isdecimal() or not 0<=int(strength)<=100:continue
        if not security.isprintable() or len(security)>64:continue
        # This UI enrols WPA-personal only, not open or enterprise networks.
        if 'WPA' not in security or '802.1X' in security:continue
        row={'ssid':name,'signal_percent':int(strength),'security':security}
        if name not in rows or int(strength)>rows[name]['signal_percent']:rows[name]=row
    return sorted(rows.values(),key=lambda r:(-r['signal_percent'],r['ssid']))[:32]


def main():
    try:
        p=subprocess.run(['/usr/bin/nmcli','--terse','--escape','yes','--fields','SSID,SIGNAL,SECURITY',
                          'device','wifi','list','--rescan','no'],capture_output=True,text=True,
                         timeout=8,check=True,env=ENV)
        answer={'schema_version':1,'status':'ok','networks':parse(p.stdout)}
    except (OSError,ValueError,subprocess.SubprocessError):
        answer={'schema_version':1,'status':'unavailable','networks':[]}
    print(json.dumps(answer,sort_keys=True));return 0
