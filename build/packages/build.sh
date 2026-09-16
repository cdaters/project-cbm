#!/bin/bash
# Native guest package construction; invoke with repository path and guest bulk root.
set -Eeuo pipefail
export PATH=/usr/sbin:/usr/bin:/sbin:/bin
recipe=$(realpath "${1:?repository recipe directory required}")
workspace=$(realpath "${2:?Linux guest workspace required}")
[[ $(uname -m) == aarch64 && $(findmnt -T "$workspace" -no FSTYPE) == ext4 ]]
[[ $(df --output=avail -B1 "$workspace" | tail -1) -gt $((60*1024*1024*1024)) ]]
export SOURCE_DATE_EPOCH=1789513200
export DEB_BUILD_OPTIONS=parallel=6
export TZ=UTC LC_ALL=C.UTF-8
python3 - "$recipe/build/inputs-poc.json" "$workspace/inputs" <<'PY'
import hashlib,json,sys
from pathlib import Path
pins=json.loads(Path(sys.argv[1]).read_text())
for name in ['vice','menu','tcpser','pi_gen']:
 pin=pins[name]; path=Path(sys.argv[2])/pin['filename']
 with path.open('rb') as f: actual=hashlib.file_digest(f,'sha256').hexdigest()
 if actual != pin['sha256']: raise SystemExit('Input rejected: '+name)
print('Selected source input hashes verified')
PY
attempt=${3:-poc1}
[[ $attempt =~ ^[a-zA-Z0-9][a-zA-Z0-9._-]*$ ]]
selection=${4:-all}
[[ $selection == all || $selection == vice-only ]]
out="$workspace/packages/$attempt"
mkdir "$out"  # Refuse reuse; failed build inspection/resume is explicit.
cd "$out"
cp "$workspace/inputs/vice-3.10.tar.gz" project-cbm-vice_3.10.orig.tar.gz
tar -xf project-cbm-vice_3.10.orig.tar.gz
cp -a "$recipe/build/packages/vice/debian" vice-3.10/debian
(
 cd vice-3.10
 dpkg-buildpackage -us -uc -sa
) > vice-build.log 2>&1
if [[ $selection == all ]]; then
tar -xf "$workspace/inputs/tcpser-fe7feff.tar"
tar --sort=name --mtime="@$SOURCE_DATE_EPOCH" --owner=0 --group=0 --numeric-owner -cf - tcpser | gzip -n > project-cbm-tcpser_1.1.6~beta.orig.tar.gz
cp -a "$recipe/build/packages/tcpser/debian" tcpser/debian
(
 cd tcpser
 dpkg-buildpackage -us -uc -sa
) > tcpser-build.log 2>&1
tar -xf "$workspace/inputs/project-cbm-menu-1.1.0_poc2.tar"
tar --sort=name --mtime="@$SOURCE_DATE_EPOCH" --owner=0 --group=0 --numeric-owner --exclude='*/debian' -cf - project-cbm-menu-1.1.0_poc2 | gzip -n > project-cbm-menu_1.1.0~poc2.orig.tar.gz
(
 cd project-cbm-menu-1.1.0_poc2
 dpkg-buildpackage -us -uc -sa
) > menu-build.log 2>&1
fi
sha256sum ./*.deb > package-sha256sums.txt
dpkg-query -W -f='${binary:Package}\t${Version}\t${Architecture}\n' > host-packages.tsv
printf 'Private package build completed; offline metadata/license/runtime audit still required\n'
