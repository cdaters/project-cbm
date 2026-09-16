# Approved Lima build host

Owner approval and implementation research: **2026-09-15**. This supersedes the
unapproved resource envelope in the [host study](linux-build-host-study.md).
Lima/VZ is the current implementation of an ordinary native arm64 Linux build-host
contract; the disposable VM is not the recovery authority. No runtime dependency
on Lima is introduced. Capability results, not successful creation alone, gate builds.

## Pinned implementation

- [Lima 2.2.0 release](https://github.com/lima-vm/lima/releases/tag/v2.2.0), source
  `de0816ea4bdc5267b428ab21025889b8dd785526`, Apache-2.0. Install the minimal
  Darwin arm64 archive into a versioned external prefix; no Homebrew/global package
  changes or container stack. Exact archive hash: [inputs](../../build/host/inputs.json).
- Apple Virtualization.framework (VZ), native aarch64, Debian 13/Trixie
  `genericcloud-arm64-20260712-2537.qcow2`. Dated URL and SHA-512 are pinned; no
  moving latest fallback. The digest is independently present in Debian's
  [SHA512SUMS](https://cloud.debian.org/images/cloud/trixie/20260712-2537/SHA512SUMS)
  and Lima's pinned template. This is build infrastructure, not the Raspberry Pi OS
  appliance base. Retain bytes because Debian rotates old cloud images.
- Owner-approved initial allocation: **8 vCPU, 10 GiB RAM, 160 GiB sparse raw disk**.
  These are engineering allocations, not permanent minimum requirements. Measure
  CPU, peak RAM, guest/external disk use and wall time during later builds.
- macOS arm64 VZ host; [upstream requirements](https://lima-vm.io/docs/config/vmtype/vz/)
  are satisfied by the inspected M4 Pro/macOS 27.0. This does not prove guest capability.
- [Plain mode](https://lima-vm.io/docs/config/plain/), no mounts, no containerd,
  Rosetta, nested virtualization, desktop, forwarded SSH agent or imported personal
  public keys. Dedicated disposable builder user and Lima SSH identity. Default
  outbound user networking; no bridged interface or exposed appliance listeners.

The input trust record starts with HTTPS acquisition, pinned digests from upstream
release metadata/checksum lists, and retained signature files. A retained signature
is not a verified signature: report any independent signer validation separately.
The repository pin is the reconstruction authority once reviewed; downloader output
never updates it automatically. No claim of fully retained Linux package closure
is made until the capability gate passes and that closure is explicitly captured.

## Storage registration and routing

Canonical source remains in configured Git repositories. Register the real mounted
bulk workspace with a `.project-cbm-workspace.json` marker containing only
`workspace_id`. An operator workspace JSON follows the
[workspace schema](../../schemas/workspace-config.schema.json). Registration must
verify the mount identity, filesystem, free space and intended existing directory;
the launcher never creates a missing mount/workspace as a fallback. The current
operator file is `ProjectCBM-Work/build-host/workspace.json`, outside Git.

| Relative to configured bulk root | Purpose |
| --- | --- |
| `build-host/lima/` | LIMA_HOME; private disposable SSH/state |
| `build-host/lima/cbm/disk` | Verified 160 GiB sparse raw guest disk (Lima 2.2.0 layout) |
| `build-host/tools/lima-2.2.0/` | Versioned frontend installation |
| `build-host/tmp/` | Explicit TMPDIR for Lima/download/conversion processes |
| `cache/lima/` | Re-creatable Lima cache |
| `inputs/build-host/` | MUST RETAIN bootstrap/archive/hash/signature/source metadata |
| `build-host/records/` | Rendered config, storage/capability observations and private infrastructure diagnostics |

The current root is `/Volumes/TheBench/ProjectCBM-Work`; it is operator configuration,
not a requirement on replacement machines. Provisioning guard floor is 256 GiB
external free space. Guest builds use `/srv/project-cbm` on ext4, never APFS shares.
Sparse virtual capacity is not reserved physical space. Measure `stat.st_size` versus
`stat.st_blocks * 512`, `du -k`, guest `df -B1` and external/internal free bytes before
and after each substantial operation. Leave room for conversions and stage copies.

In [pinned Lima download code](https://github.com/lima-vm/lima/blob/v2.2.0/pkg/downloader/downloader.go),
`WithCache` uses Go's `os.UserCacheDir()` plus `lima`; the
[VM image call path](https://github.com/lima-vm/lima/blob/v2.2.0/pkg/fileutils/download.go)
does not expose `WithCacheDir` as operator configuration. macOS resolves this to
`~/Library/Caches/lima`; XDG_CACHE_HOME is not the Mac override. The approved reversible
arrangement is a symlink from that otherwise absent path to bulk `cache/lima`.
The launcher refuses an existing unrelated directory or differently targeted symlink.
Preserve/review an existing cache manually before any replacement. To reverse this
setup, stop all associated instances and remove only that verified symlink; retained
external bytes remain. Do not remove the entire macOS Caches directory.

## Reconstruction commands

Use Python with [pinned contract dependencies](../../requirements-contracts.txt).
The implementation is [build_host.py](../../tools/build_host.py); it checks mount,
workspace marker, containment, free space and external cache before each operation.
Set `CBM_WORKSPACE_CONFIG` to the registered operator JSON and `CBM_PYTHON` to that
Python. Run from the product repository:

```sh
"$CBM_PYTHON" tools/build_host.py --workspace-config "$CBM_WORKSPACE_CONFIG" preflight
"$CBM_PYTHON" tools/build_host.py --workspace-config "$CBM_WORKSPACE_CONFIG" prepare
"$CBM_PYTHON" tools/build_host.py --workspace-config "$CBM_WORKSPACE_CONFIG" acquire
"$CBM_PYTHON" tools/build_host.py --workspace-config "$CBM_WORKSPACE_CONFIG" install
"$CBM_PYTHON" tools/build_host.py --workspace-config "$CBM_WORKSPACE_CONFIG" render
```

`prepare` creates the approved cache link/directories. `acquire` uses curl with HTTPS,
resume, retry and mandatory post-download digest verification, retaining partial files
externally. Existing complete files are reverified. `install` refuses to overwrite an
existing prefix. Restore verified retained inputs into the same relative layout to
avoid network acquisition. Rendered paths are operational output, not portable pins.

Use `lima validate <rendered cbm.yaml>`, then `lima start --name=cbm --tty=false
<rendered cbm.yaml>` through the same wrapper. Check `lima list` and run the core
[capability probe](../../build/host/capability-gate.sh) by SSH/stdin before installing
build dependencies. Lima's generated `ssh.config` is private connection configuration;
use `ssh -F <instance>/ssh.config lima-cbm` and `rsync -e 'ssh -F ...'` for ordinary
bidirectional transfers, recording hashes before/after. No shared host folders needed.

Core must pass before full diagnostics. The full probe requires guest packages
`fdisk e2fsprogs util-linux kmod attr busybox-static git curl ca-certificates rsync`;
source acquisition additionally needs `dpkg-dev` and authenticated `deb-src` metadata.
These are diagnostic/bootstrap dependencies, not the complete pi-gen/package stack.
Record exact installed versions and authenticated package metadata, test installation
and removal of a disposable package and acquisition of a source package. Run full probe,
record SSH transfer hashes, storage statistics and confirm all gate categories before
marking PASS. The script prints partial success explicitly; it cannot certify the
entire gate by itself. A required failure stops work without architectural workarounds.

## Lifecycle and identity boundary

Stop using wrapper `lima stop cbm`. After separately verifying all required sources,
packages, locks, artifacts and records were exported and hashed, `lima delete cbm`
destroys disposable state/disk. This is an explicit destructive operator command,
never an automatic failure handler. Retain bootstrap inputs, recipes and evidence;
then render/create/test again. Do not copy a running raw disk as a recovery backup.
Use ordinary Linux/SSH/rsync/package management for build recipes so another suitable
arm64 Linux host can replace Lima. Full offline reconstruction also needs retained
Linux package closure; do not equate a bootable bootstrap image with that closure.

VM keys, machine-id, cloud-init state, builder home/history, Lima state, host paths
and credentials must never be copied into appliance assembly. Build an independent
rootfs from declared inputs; emit only generated minimal release identity. External
build-host private diagnostics and keys are not public Git source or release inputs.

## Download engine

[aria2](https://github.com/aria2/aria2) supports resume, multiple sources and Metalink.
**Defer it for the first POC:** curl already supplies resumable HTTPS, bounded retries
and explicit destinations; CBM verifies against the lock after acquisition. Multiple
mirror orchestration is not yet required. Neither downloader is a trust authority.
aria2 is not an appliance dependency. Revisit only on measured acquisition reliability
problems that simpler transport cannot handle.

## Controlled package-update windows

Before package/image work, stop and mask the guest's `apt-daily.timer`,
`apt-daily-upgrade.timer`, `apt-daily.service`, `apt-daily-upgrade.service` and
`unattended-upgrades.service` after confirming no update is in progress. These are
builder-only settings. POC3 exposed inherited unattended-upgrade drift; see
[the reconciliation](poc3-design.md#host-drift-discovered-and-corrected-before-candidate-acceptance).
Construction checks masked state and exact locked host package versions before
and after building. Retain changed inputs and freeze a new lock for intentional
maintenance; review updates between build windows. Never silently run a stale lock
against a newly updated host or apply these builder settings to the appliance.
