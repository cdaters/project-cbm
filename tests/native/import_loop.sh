#!/bin/bash
set -euo pipefail
base=${PCBM_STAGING_ROOT:?explicit disposable staging area required}
mkdir "$base/usb-fixture"
printf '\001\010synthetic copy test\n' > "$base/usb-fixture/probe.prg"
printf 'synthetic SID classification only\n' > "$base/usb-fixture/probe.sid"
ln -s /etc/shadow "$base/usb-fixture/ignored.prg"
truncate -s 32M "$base/usb-fixture.img"
mkfs.ext4 -q -F -d "$base/usb-fixture" "$base/usb-fixture.img"
loop=$(losetup --read-only --find --show "$base/usb-fixture.img")
trap 'losetup -d "$loop"' EXIT
sha256sum "$base/usb-fixture.img" > "$base/usb-before.sha256"
parent=$(systemctl show pcbm-native-staging -p MainPID --value)
pid=$(pgrep -P "$parent" -x systemd)
read -r major minor < <(stat -c '%t %T' "$loop")
major=$((16#$major));minor=$((16#$minor))
systemctl set-property --runtime pcbm-native-staging "DeviceAllow=$loop r"
nsenter -t "$pid" -m -p -n -u -i -C --root /usr/bin/python3 - "$loop" "$major" "$minor" <<'PY'
import os,sys,stat,json,subprocess
from pathlib import Path
os.umask(0o077)
os.chdir('/');sys.path.insert(0,'/usr/share/project-cbm/runtime')
from project_cbm import importer
# Explicit test-only discovery adapter: production discovery must reject loops.
device,major,minor=sys.argv[1],int(sys.argv[2]),int(sys.argv[3])
try:
 importer.discover()
except subprocess.CalledProcessError:
 pass # This isolated service namespace deliberately hides block-device sysfs.
if os.path.exists(device):os.unlink(device)
os.mknod(device,stat.S_IFBLK|0o600,os.makedev(major,minor))
entry={'device':device,'number':f'{major}:{minor}','diskseq':'synthetic-test-only','filesystem':'ext4','size_bytes':32*1024**2}
importer.discover=lambda:[entry]
answer=importer.perform(entry,'programs')
assert answer['copied']==2 and answer['skipped']>=1,answer
for category,filename in [('programs','probe.prg'),('music','probe.sid')]:
 p=Path('/home/pcbm/content')/category/'Imported'/filename
 assert p.is_file() and p.stat().st_uid==1000
assert not os.path.ismount(importer.WORK/'source')
again=importer.perform(entry,'programs');assert again['copied']==0 and again['skipped']>=3
family=importer.perform(entry,'demos','c64')
assert family['copied']==2 and family['skipped']>=1,family
for category,filename in [('demos','probe.prg'),('music','probe.sid')]:
 p=Path('/home/pcbm/content')/category/'c64/Imported'/filename
 assert p.is_file() and p.stat().st_uid==1000
repeat=importer.perform(entry,'demos','c64');assert repeat['copied']==0 and repeat['skipped']>=3
assert not os.path.ismount(importer.WORK/'source')
print(json.dumps({'native_loop_import':answer,'retry':again,'family_import':family,'family_retry':repeat,'source_unmounted':True,'discovery':'test adapter; real USB needs Pi validation'}))
os.unlink(device)
PY
sha256sum -c "$base/usb-before.sha256"
