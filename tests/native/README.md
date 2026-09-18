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
The terminal probe reads the controlled root's current Computer Name and Debian's
standard colored prompt. A terminal prompt mismatch is a harness failure.

`import_loop.sh` creates a tiny synthetic ext4 image. It explicitly substitutes
only test discovery because the isolated namespace has no block-device sysfs.
Production has no loop-device admission or test-discovery switch. It tests real
read-only mount/copy/unmount, UID ownership, symlink exclusion, no overwrite and
source SHA agreement. Run only in a new disposable staging directory; retain the
small result, not an unnecessary image. Actual USB discovery/hot unplug needs Pi
testing. An earlier harness without the hidden-sysfs accommodation stopped before
mounting; the importer itself was not relaxed to admit loop devices.

## Environment correction revalidation

`build_environment.sh` is the before/after AppArmor regression; see the
[boundary contract](../../docs/build/environment-boundary.md). `services.py` repeats
actual native service operations and in-memory NetworkManager credential parsing.
It emits only result flags and cleans test credentials. nmcli output escaping is
explicitly disabled for the exact in-memory comparison.

The disposable copied runtime root is not a full newly assembled image. Its fresh
namespace `/run` must receive the three directories declared by the frozen stage's
`/usr/lib/tmpfiles.d/project-cbm.conf` before helper tests. Create them with root 0755,
or install/apply that exact tmpfiles declaration. A missing directory is a harness
preparation failure, not permission to relax the helper's trusted-path checks.

## Release refinement probes

`release_services.py` verifies Computer Name changes/local resolution, safe enrollment
metadata, actual On/Off listeners, restart and persisted enablement, owner-only content
share configuration, Samba Avahi build support and redaction. `discovery_local.py`
creates/removes only its synthetic namespace interface and verifies an SMB mDNS answer.
`ssh_login.py` tests real loopback owner/password SSH and refusal after disable; its
secret exists only in memory/stdin. `dialog_status.py` exercises real dialog service
prompts at 40x12, 80x24 and 100x36. These require already completed isolated setup,
not a fresh uninitialized root. The account/credentials are invalidated afterward.
They do not prove physical reboot, remote client reachability or Finder/Explorer browsing.
