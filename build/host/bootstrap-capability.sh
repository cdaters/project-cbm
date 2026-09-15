#!/bin/bash
# Minimal disposable-guest diagnostics only, after core precheck passes.
# Online metadata is captured; this is not yet a frozen complete build closure.
set -Eeuo pipefail
[[ $(uname -s) == Linux && $(uname -m) == aarch64 ]]
sudo install -d -m 0755 -o builder -g builder /srv/project-cbm/inputs/bootstrap /srv/project-cbm/scratch /srv/project-cbm/artifacts
cp --no-clobber /etc/apt/sources.list.d/debian.sources /srv/project-cbm/inputs/bootstrap/debian.sources.original
dpkg-query -W -f='${binary:Package}\t${Version}\t${Architecture}\n' > /srv/project-cbm/inputs/bootstrap/packages-before.tsv
sudo python3 - <<'PY'
from pathlib import Path
p=Path('/etc/apt/sources.list.d/debian.sources')
s=p.read_text().replace('http://','https://').replace('Types: deb\n','Types: deb deb-src\n')
p.write_text(s)
Path('/etc/apt/apt.conf.d/99cbm-retain').write_text('Binary::apt::APT::Keep-Downloaded-Packages "true";\nAPT::Keep-Downloaded-Packages "true";\n')
PY
sudo apt-get update
sudo apt-get install -y --no-install-recommends fdisk e2fsprogs util-linux kmod attr busybox-static git curl ca-certificates rsync dpkg-dev
sudo apt-get install -y --no-install-recommends hello
hello
sudo apt-get purge -y hello
cd /srv/project-cbm/inputs/bootstrap
apt-get source --download-only hello
sudo cp -a /var/lib/apt/lists ./apt-lists
sudo cp -a /var/cache/apt/archives ./apt-archives
cp /etc/apt/sources.list.d/debian.sources ./debian.sources
dpkg-query -W -f='${binary:Package}\t${Version}\t${Architecture}\n' > packages-after.tsv
printf 'APT HTTPS INSTALL REMOVE SOURCE ACQUISITION PASS\n'
