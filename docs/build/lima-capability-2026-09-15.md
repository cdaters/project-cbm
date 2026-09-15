# Lima/VZ capability gate — 2026-09-15

**PASS**, including actual privileged image operations. This is build-host evidence;
no Project CBM image, reproducibility or physical Raspberry Pi pass follows from it.
Owner-approved [recipe](lima-build-host.md): Lima 2.2.0 VZ/plain, 8 vCPU, 10 GiB RAM,
160 GiB sparse raw disk on configured external storage. The guest remains running.

## Evidence

Private raw logs and catalogs live under configured bulk `build-host/records/`.
They are infrastructure evidence, not appliance files or public Git payloads.

| Category | Observed result |
| --- | --- |
| Platform | Debian 13/Trixie, arm64/aarch64, Linux `6.12.95+deb13-cloud-arm64`, eight CPUs, MemTotal 10,179,140 KiB |
| Root | `/dev/vda1`, ext4, writable; capacity 168,881,938,432 bytes; after diagnostics used 1,363,144,704 and available 160,604,790,784 bytes |
| Filesystem | Actual loop-backed ext4: uid/gid 1234/2345, mode 0751, executable bit, hard/symbolic links, case-distinct names, user xattr round-trip |
| Privileges | sudo/root, loop module/device, partitioned 128 MiB image, losetup partscan, mkfs.ext4, mount/unmount, bind mount, proc/sysfs/tmpfs, device-node creation, static-busybox chroot accessing proc/sys/dev |
| Cleanup | Successful probe detached loop and unmounted its filesystems. Failed test image retained as diagnostic evidence |
| Packages | APT authenticated metadata over HTTPS; hello 2.10-5 installed, executed, purged; corresponding source acquired; dpkg and source-package tools available |
| Network | DNS/HTTPS Debian access, Git ls-remote of pi-gen arm64, ordinary SSH host-to-guest |
| Transfer | rsync over SSH both directions, 1,048,576 bytes, identical SHA-256 `ca2187b17b439e2b4b905badcd880a74f34308841b3dcaaa3623bd2edfff65ca` |
| Isolation | Plain-mode startup verified; no host filesystem shares, containerd or Rosetta enabled; dedicated disposable builder SSH identity |
| Storage | VM disk 171,798,691,840 apparent bytes; 1,687,449,600 allocated bytes at gate; all state/input/cache/temp routing external |

Before installation: internal free **88,085,303,296** bytes; external free
**1,133,635,264,512** bytes. At gate: internal **88,064,573,440**; external
**1,131,271,086,080**. These are filesystem observations affected by concurrent
host activity, not exact attribution. Internal delta about 20 MiB gives no evidence
of an accidental multi-GB internal VM/cache. The sparse raw disk itself is external.
The cache symlink resolves to the verified external directory; local pinned bootstrap
input avoided a redundant Lima network cache copy.

## Probe corrections and evidence limits

The first full attempt failed its tool lookup because ordinary SSH PATH omitted
/usr/sbin. Installed sfdisk worked by absolute path; the probe now sets its admin
PATH. The next attempt correctly denied an unprivileged xattr read after deliberately
setting the test file owner/mode to 1234:2345/0751. Reading as root passed. Neither
was a missing Linux capability; both original failed logs remain alongside the final
passing `capability-full-root-read.log`. No hypervisor/kernel/container workaround.

Initial bootstrap export encountered permission errors for transient APT `lock` and
`partial` entries. Export was repeated successfully with these non-input paths and
`auxfiles` excluded. `retained-inputs.json` hashes 82 retained bootstrap files. This
is not yet the complete pi-gen/toolchain/runtime/corresponding-source closure.
Initial diagnostic dependencies resolved from current authenticated Debian metadata,
which was captured with exact package versions and available .debs. Full lost-builder
reconstruction still needs the remaining declared build closure and a replay drill.

Lima archive SHA-256 matches both API metadata and upstream SHA256SUMS. macOS
codesign validation passed and virtualization entitlement is present; this is not
an independent publisher-key signature assertion. Lima detached signature was retained,
not independently GPG-verified. The attempted Debian `SHA512SUMS.sign` URL returned
404; no signature verification is claimed. Debian guest SHA-512 matches the official
checksum list and pinned Lima source. Linux APT authenticated repository metadata
normally; bootstrap-image trust and APT authentication are separate observations.

Core/full probe and bootstrap scripts are under build/host. Their host static checks
and the combined 20 contract/storage tests passed. No full-stack build, no image,
no boot/video/audio/controller/network qualification on a Raspberry Pi, no clean
independent rebuild. **Next: pinned retained POC inputs and component package builds.**
