#!/bin/bash
set -euo pipefail
r=${PCBM_STAGING_ROOT:?explicit disposable staging area required}/root
[[ $EUID == 0 && -f $r/etc/debian_version ]]
mount --make-rprivate /
mount --bind "$r" "$r"
mount -t proc proc "$r/proc"
mount --bind "$r/proc/sys" "$r/proc/sys"
mount -o remount,bind,ro "$r/proc/sys"
mount -t tmpfs -o mode=755 tmpfs "$r/sys"
mkdir -p "$r/sys/fs/cgroup"
mount -t cgroup2 cgroup2 "$r/sys/fs/cgroup"
mount -o remount,ro "$r/sys"
mount -t tmpfs -o mode=755,nosuid tmpfs "$r/dev"
for spec in 'null 1 3' 'zero 1 5' 'full 1 7' 'random 1 8' 'urandom 1 9' 'tty 5 0'; do
 read -r name major minor <<< "$spec"
 mknod -m 666 "$r/dev/$name" c "$major" "$minor"
done
mkdir "$r/dev/pts" "$r/dev/shm"
mount -t devpts -o newinstance,ptmxmode=0666,mode=0620,gid=5 devpts "$r/dev/pts"
ln -s pts/ptmx "$r/dev/ptmx"
mount -t tmpfs -o mode=1777,nosuid,nodev tmpfs "$r/dev/shm"
mount -t tmpfs -o mode=755,nosuid,nodev tmpfs "$r/run"
mount --make-rshared "$r"
exec setpriv --bounding-set=-sys_module,-sys_time,-sys_rawio,-sys_boot chroot "$r" /usr/bin/env container=pcbm-staging /sbin/init
