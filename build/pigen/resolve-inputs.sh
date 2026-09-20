#!/bin/bash
# Input resolution only: no image export and no claim of a frozen release build.
# The retained transport captures exact authenticated APT bytes before lock freeze.
set -Eeuo pipefail
export PATH=/usr/sbin:/usr/bin:/sbin:/bin
workspace=$(realpath "${1:?guest workspace required}")
[[ $(uname -m) == aarch64 && $(findmnt -T "$workspace" -no FSTYPE) == ext4 ]]
[[ $(df --output=avail -B1 "$workspace" | tail -1) -gt $((60*1024*1024*1024)) ]]
curl --fail --retry 5 --retry-connrefused --retry-delay 1 http://127.0.0.1:3142/ >/dev/null
work="$workspace/builds/resolve-inputs"
mkdir "$work"
tar -xf "$workspace/inputs/pi-gen-6fcca448.tar" -C "$work"
cd "$work/pi-gen"
patch --batch -p1 < "$(dirname "$(realpath "$0")")/exclude-connect.patch"
for stage in stage0 stage1 stage2; do touch "$stage/SKIP_IMAGES"; done
cat > config <<CONFIG
IMG_NAME='cbm-input-resolution'
IMG_DATE='2026-09-15'
GIT_HASH='6fcca44892d5d4b36f826d2b8fb16d716369fada'
RELEASE='trixie'
WORK_DIR='$work/work'
DEPLOY_DIR='$work/no-image-export'
STAGE_LIST='stage0 stage1 stage2'
APT_PROXY='http://127.0.0.1:3142'
ENABLE_CLOUD_INIT=0
ENABLE_SSH=0
PASSWORDLESS_SUDO=0
FIRST_USER_NAME='pcbm'
TIMEZONE_DEFAULT='UTC'
LOCALE_DEFAULT='en_US.UTF-8'
KEYBOARD_KEYMAP='us'
KEYBOARD_LAYOUT='English (US)'
CONFIG
sudo /usr/bin/time -v ./build.sh
if [[ -d "$work/no-image-export" ]] && find "$work/no-image-export" -type f | grep -q .; then
    echo 'Unexpected export in input-resolution run' >&2; exit 1
fi
printf 'Input resolution stages complete; no image constructed or release lock frozen\n'
