# Disposable native activation probes

These are privileged, opt-in engineering harnesses, **not ordinary unit tests**.
Never run them on an appliance, the builder root, or preserved media. They modify
only a separately copied staging root and generated synthetic media. Read
[the staging record](../../docs/build/runtime-activation.md) first.

`namespaces.sh` runs under a delegated transient systemd unit and `unshare` with
private mount/PID/network/UTS/IPC/cgroup namespaces. Set `PCBM_STAGING_ROOT` to the
explicit disposable staging directory containing `root`. It uses existing Linux
utilities, not an installed container platform. The staging root needs masked
hardware/getty/root-expansion units and a private preset policy. `/sys` is hidden;
physical devices/graphics/Wi-Fi are intentionally unavailable. Do not expose the
builder's service bus, network or credential stores.

`runtime_activation.py` and `owner_administration.py` run **inside that root** after
installing staging packages, the exact helper authorization, owner account and
inactive policy. They use generated temporary credentials in memory, never argv or
output, and invalidate them in `finally`. Do not archive the resulting root,
credential databases, journals or shadow backups as evidence. Retain test code and
sanitized result records only. The account and first-boot state intentionally remain
inconsistent after credential invalidation: discard the root after testing.

The root-growth completion marker injected by the activation test stands for the
**separate real loop-image growth test**; it is not proof of growth or Pi boot.
The terminal probe expects the controlled `cbm-staging` hostname and Debian's
standard colored prompt. A terminal prompt mismatch is a harness failure.

`import_loop.sh` creates a tiny synthetic ext4 image. It explicitly substitutes
only test discovery because the isolated namespace has no block-device sysfs.
Production has no loop-device admission or test-discovery switch. It tests real
read-only mount/copy/unmount, UID ownership, symlink exclusion, no overwrite and
source SHA agreement. Run only in a new disposable staging directory; retain the
small result, not an unnecessary image. Actual USB discovery/hot unplug needs Pi
testing. An earlier harness without the hidden-sysfs accommodation stopped before
mounting; the importer itself was not relaxed to admit loop devices.
