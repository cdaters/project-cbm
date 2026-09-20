#!/usr/bin/python3
"""POC first boot: one root-growth owner, retry checks, no builder identity."""
import fcntl
import json
import os
from pathlib import Path
import re
import subprocess
import stat

STATE = Path('/var/lib/project-cbm/first-boot')


def completed(state=STATE):
    """Only a valid protected completion marker may skip one-time expansion."""
    path = state/'complete.json'
    if not path.exists() and not path.is_symlink():
        return False
    parent, marker = state.lstat(), path.lstat()
    if (not stat.S_ISDIR(parent.st_mode) or parent.st_uid != 0 or parent.st_mode & 0o077
            or not stat.S_ISREG(marker.st_mode) or marker.st_uid != 0
            or marker.st_mode & 0o022 or marker.st_nlink != 1 or marker.st_size > 1024):
        raise ValueError('unsafe first-boot completion marker')
    value = json.loads(path.read_text())
    if (not isinstance(value,dict) or set(value) != {'schema_version','root_growth_verified'}
            or type(value['schema_version']) is not int or value['schema_version'] != 1
            or value['root_growth_verified'] is not True):
        raise ValueError('invalid first-boot completion marker')
    return True


def run(*args):
    return subprocess.check_output(args, text=True).strip()


def geometry(document, root, disk_bytes):
    table = document['partitiontable']
    parts = table['partitions']
    if table['label'] != 'dos' or table.get('unit') != 'sectors' or table.get('sectorsize', 512) != 512:
        raise ValueError('POC supports only the declared DOS/512-byte sector layout')
    if len(parts) != 2 or parts[1]['node'] != root or parts[1]['type'].lower() != '83':
        raise ValueError('root must be the final Linux partition in the declared two-partition image')
    boot, data = parts
    if boot['start'] < 1 or data['start'] < boot['start'] + boot['size']:
        raise ValueError('invalid or overlapping partition geometry')
    end = data['start'] + data['size']
    if data['size'] <= 0 or end * 512 > disk_bytes:
        raise ValueError('root partition exceeds device capacity')
    return {'disk_id':table['id'], 'start':data['start'], 'size':data['size'],
            'free_tail_bytes':disk_bytes-end*512}


def write_state(name, value):
    temp=STATE/(name+'.next')
    with temp.open('w') as stream:
        json.dump(value,stream,sort_keys=True); stream.write('\n'); stream.flush(); os.fsync(stream.fileno())
    temp.replace(STATE/name)
    fd=os.open(STATE,os.O_DIRECTORY)
    try: os.fsync(fd)
    finally: os.close(fd)


def main():
    if os.geteuid()!=0: raise SystemExit('first boot requires root')
    STATE.mkdir(parents=True,exist_ok=True,mode=0o700)
    with (STATE/'lock').open('w') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        if completed(STATE):
            return
        mid=Path('/etc/machine-id').read_text().strip()
        if not re.fullmatch('[0-9a-f]{32}',mid) or mid=='0'*32:
            raise ValueError('systemd must initialize persistent machine-id before CBM')
        root=os.path.realpath(run('findmnt','-nro','SOURCE','/'))
        if run('findmnt','-nro','FSTYPE','/')!='ext4': raise ValueError('expected writable ext4 root')
        parent=run('lsblk','-ndo','PKNAME',root)
        if not re.fullmatch('[a-zA-Z0-9_-]+',parent): raise ValueError('ambiguous root parent device')
        disk='/dev/'+parent
        number=Path('/sys/class/block',Path(root).name,'partition').read_text().strip()
        if number!='2': raise ValueError('unexpected root partition number')
        disk_bytes=int(run('blockdev','--getsize64',disk))
        before=geometry(json.loads(run('sfdisk','--json',disk)),root,disk_bytes)
        journal=STATE/'growth.json'
        if journal.exists():
            previous=json.loads(journal.read_text())
            if any(previous[k]!=before[k] for k in ['disk_id','start']):
                raise ValueError('root geometry changed since initialization; inspect before retry')
        else: write_state('growth.json',before)
        # growpart's documented status 1 means no available growth, not an error.
        result=subprocess.run(['growpart',disk,number],check=False)
        if result.returncode not in (0,1): raise ValueError('partition growth failed; retained journal requires inspection')
        after=geometry(json.loads(run('sfdisk','--json',disk)),root,disk_bytes)
        if after['start']!=before['start'] or after['size']<before['size']:
            raise ValueError('unexpected partition movement/shrink')
        if int(run('blockdev','--getsize64',root)) != after['size']*512:
            raise ValueError('kernel geometry is stale; reboot before retry, do not repeat mutations')
        if after['free_tail_bytes'] > 10*1024*1024:
            raise ValueError('root did not grow to the expected device tail')
        subprocess.run(['resize2fs',root],check=True)
        if run('id','-u','pi')!='1000': raise ValueError('unexpected appliance account identity')
        for path in ['/home/pi/pcbm', '/home/pi/.config','/home/pi/.config/vice',
                     '/home/pi/.local','/home/pi/.local/state','/home/pi/.local/state/vice',
                     '/home/pi/.local/share','/home/pi/.local/share/vice']:
            target=Path(path)
            if target.is_symlink(): raise ValueError('refusing user-state symlink during initialization')
            if not target.exists():
                target.mkdir(mode=0o755)
            os.chown(target,1000,1000)
        # Existing choices remain untouched. Network listeners are disabled in POC.
        write_state('complete.json',{'schema_version':1,'root_growth_verified':True})
        os.sync()


if __name__=='__main__': main()
