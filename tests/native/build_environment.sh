#!/bin/bash
# Opt-in: run in a NEW disposable copy of the failed attempt's root, never evidence.
set -euo pipefail
: "${PCBM_ENV_STAGE:?explicit disposable staging directory required}"
[[ $EUID == 0 && -f $PCBM_ENV_STAGE/DISPOSABLE && $PCBM_ENV_STAGE == /srv/project-cbm/staging/* ]]
ROOTFS_DIR=$PCBM_ENV_STAGE/root
COMMON=$PCBM_ENV_STAGE/common
[[ -f $ROOTFS_DIR/etc/debian_version && -f $COMMON ]]
mount --make-rprivate /
export ROOTFS_DIR SOURCE_DATE_EPOCH=1789513200
CAPSH_ARG=''
# Reproduce the exact maintainer-script failure, not just a mocked subprocess.
if env TMPDIR=/builder-only/nonexistent chroot "$ROOTFS_DIR" /usr/bin/mktemp; then
 echo 'unexpected legacy mktemp success' >&2; exit 1
fi
if env TMPDIR=/builder-only/nonexistent DEBIAN_FRONTEND=noninteractive chroot "$ROOTFS_DIR" dpkg --configure apparmor; then
 echo 'unexpected legacy AppArmor success' >&2; exit 1
fi
echo 'BEFORE: inherited invalid TMPDIR reproduces mktemp and AppArmor failure'
# Do not poison the harness interpreter or mount commands: set shell exports here.
export TMPDIR=/builder-only/nonexistent TMP=/bad TEMP=/bad HOME=/bad USER=bad LOGNAME=bad
export XDG_CONFIG_HOME=/bad XDG_RUNTIME_DIR=/bad PYTHONPATH=/bad PYTHONHOME=/bad
export GIT_CONFIG_GLOBAL=/bad GIT_DIR=/bad http_proxy=http://bad.invalid HTTPS_PROXY=http://bad.invalid
export CBM_KIT=/bad CBM_RELEASE_LOCK=/bad CBM_UNEXPECTED=/bad BASH_ENV=/bad ENV=/bad
source "$COMMON"
on_chroot <<'EOF'
set -eu
[[ $HOME == /root && $USER == root && $LOGNAME == root ]]
[[ $TMPDIR == /tmp && $TMP == /tmp && $TEMP == /tmp ]]
[[ $LANG == C.UTF-8 && $LC_ALL == C.UTF-8 && $DEBIAN_FRONTEND == noninteractive ]]
[[ $SOURCE_DATE_EPOCH == 1789513200 ]]
for name in XDG_CONFIG_HOME XDG_RUNTIME_DIR PYTHONPATH PYTHONHOME GIT_CONFIG_GLOBAL GIT_DIR http_proxy HTTPS_PROXY CBM_KIT CBM_RELEASE_LOCK CBM_UNEXPECTED BASH_ENV ENV; do
 [[ ! -v $name ]] || exit 1
done
[[ $(stat -c %a /tmp) == 1777 ]]
p=$(mktemp); [[ $p == /tmp/* ]]; rm -- "$p"
df -B1 /tmp
dpkg --configure apparmor
dpkg --audit
[[ $(dpkg-query -W -f='${db:Status-Status}' apparmor) == installed ]]
apt-get check
echo 'AFTER: clean target env, tmp mode/space, mktemp, AppArmor, dpkg and apt PASS'
EOF
