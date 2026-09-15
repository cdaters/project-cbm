#!/bin/bash
# Run through SSH as the disposable builder, never in the appliance or on macOS.
# Phase core precedes optional diagnostic package installation. Any failure stops.
set -Eeuo pipefail
export PATH=/usr/sbin:/usr/bin:/sbin:/bin
trap 'rc=$?; echo "CAPABILITY GATE FAIL line=$LINENO status=$rc" >&2; exit "$rc"' ERR
phase=${1:-core}
[[ $(uname -s) == Linux && $(uname -m) == aarch64 ]]
. /etc/os-release
[[ $ID == debian && $VERSION_ID == 13 && $VERSION_CODENAME == trixie ]]
echo "PLATFORM $PRETTY_NAME $(uname -r) $(dpkg --print-architecture)"
printf 'CPU '; nproc
awk '/MemTotal/ {print}' /proc/meminfo
findmnt -no SOURCE,FSTYPE,OPTIONS /
df -B1 /
[[ $(findmnt -n -o FSTYPE /) == ext4 ]]
sudo -n true
sudo chroot / /bin/true
sudo modprobe loop
sudo losetup --find
if [[ $phase == core ]]; then
    echo 'CORE PRECHECK PASS (full gate still pending)'
    exit 0
fi
[[ $phase == full ]]
for tool in sfdisk mkfs.ext4 losetup mount umount chroot setfattr getfattr busybox git curl rsync; do
    command -v "$tool"
done
sudo install -d -m 0755 -o "$(id -u)" -g "$(id -g)" /srv/project-cbm/scratch
probe=$(mktemp -d /srv/project-cbm/scratch/capability.XXXXXX)
loop=''
cleanup() {
    local result=$?
    trap - EXIT
    set +e
    for dir in dev sys proc bound ''; do
        if mountpoint -q "$probe/root/${dir}"; then sudo umount "$probe/root/${dir}" || result=1; fi
    done
    if [[ -n $loop ]]; then sudo losetup -d "$loop" || result=1; fi
    if [[ $result == 0 ]]; then sudo rm -rf -- "$probe"; else echo "Retained failed probe at $probe" >&2; fi
    exit "$result"
}
trap cleanup EXIT
truncate -s 128M "$probe/disk.raw"
printf 'label: dos\nstart=2048, type=83\n' | sfdisk "$probe/disk.raw"
loop=$(sudo losetup --find --show --partscan "$probe/disk.raw")
sudo udevadm settle
[[ -b ${loop}p1 ]]
sudo mkfs.ext4 -q "${loop}p1"
mkdir "$probe/root"
sudo mount "${loop}p1" "$probe/root"
sudo mkdir -p "$probe/root/"{bin,dev,proc,sys,bound}
sudo cp /usr/bin/busybox "$probe/root/bin/busybox"
sudo touch "$probe/root/owned"
sudo chown 1234:2345 "$probe/root/owned"
sudo chmod 0751 "$probe/root/owned"
[[ $(stat -c '%u:%g:%a' "$probe/root/owned") == 1234:2345:751 ]]
sudo ln "$probe/root/owned" "$probe/root/hard"
[[ $(stat -c %i "$probe/root/owned") == $(stat -c %i "$probe/root/hard") ]]
sudo ln -s owned "$probe/root/sym"
[[ $(readlink "$probe/root/sym") == owned ]]
sudo touch "$probe/root/Case" "$probe/root/case"
[[ $(stat -c %i "$probe/root/Case") != $(stat -c %i "$probe/root/case") ]]
sudo setfattr -n user.cbm -v gate "$probe/root/owned"
[[ $(sudo getfattr --only-values -n user.cbm "$probe/root/owned" 2>/dev/null) == gate ]]
sudo mount --bind "$probe/root/bin" "$probe/root/bound"
sudo mount -t proc proc "$probe/root/proc"
sudo mount -t sysfs sysfs "$probe/root/sys"
sudo mount -t tmpfs tmpfs "$probe/root/dev"
sudo mknod -m 666 "$probe/root/dev/null" c 1 3
sudo chroot "$probe/root" /bin/busybox sh -c 'echo chroot > /dev/null; test -r /proc/self/status; test -d /sys/devices; /bin/busybox test -x /bound/busybox'
curl --fail --location --proto '=https' -o /dev/null https://deb.debian.org/debian/README
git ls-remote https://github.com/RPi-Distro/pi-gen.git refs/heads/arm64
apt-cache policy
printf 'FULL LINUX CAPABILITY PROBE PASS; apt source/install/remove and bidirectional transfer require separate evidence\n'
