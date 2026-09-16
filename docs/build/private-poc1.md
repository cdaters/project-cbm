# First private Project CBM 1.1 POC — owner review checkpoint

Completed 2026-09-15. **STOP: first controlled image and offline validation complete.**
No physical Raspberry Pi test, second clean build, public release or push was performed.
This is `1.1.0-poc.1`, candidate `private-engineering-poc1`, not Project CBM 1.1.0 final.
[Machine-readable results](private-poc1.json) contain exact bytes, hashes and checks.

## Build host and storage

[Lima recipe/reconstruction](lima-build-host.md) and [capability evidence](lima-capability-2026-09-15.md)
record Lima **2.2.0**, official source `de0816ea4bdc5267b428ab21025889b8dd785526`.
Official Darwin arm64 archive SHA-256:
`bbdef91774885a0d05f7b048c4eb89ae2bcf3a0c252ae7ca7934e63df76d93c3`.
Upstream SHA256SUMS/API digest agree; local codesign check passed. Detached signature
is retained but not independently GPG-verified. Exact dated Debian cloud bootstrap,
SHA-512 and origin are in [host inputs](../../build/host/inputs.json).

Apple VZ, native arm64 Debian 13/Trixie, plain mode, no desktop/container platform/
Rosetta/host directory shares. Initial allocation: 8 vCPU, 10 GiB RAM, 160 GiB sparse
disk. Guest kernel: `6.12.95+deb13-cloud-arm64`; `/dev/vda1` ext4. The VM is now
**stopped**, not deleted. Ordinary SSH/rsync moves inputs and outputs. Guest work:
`/srv/project-cbm`; repository recipes remain authoritative, not the VM's live state.

Current configurable bulk root is `/Volumes/TheBench/ProjectCBM-Work` on external APFS.
Relative locations:

| Material | Location |
| --- | --- |
| Lima installation | `build-host/tools/lima-2.2.0` |
| LIMA_HOME / VM | `build-host/lima` / `build-host/lima/cbm` |
| Sparse virtual disk | `build-host/lima/cbm/disk` |
| Cache / temporary files | `cache/lima` / `build-host/tmp` |
| Operator config / rendered VM recipe | `build-host/workspace.json` / `build-host/records/cbm.yaml` |
| Host diagnostics/acquisition/build logs | `build-host/records` |
| Frozen portable input kit | `inputs/frozen-poc1` |
| Private component packages/source/build records | `packages/poc1` |
| Raw/XZ image and validation | `artifacts/private-poc1` |
| Final source/recovery checkpoint | `archive/milestone1-private-poc1-2026-09-15` |

Lima's pinned macOS downloader has no operator cache-location override. The previously
absent `~/Library/Caches/lima` is a reversible symlink to external `cache/lima`; actual
bytes remain external. `~/.lima` was not created. No unrelated cache was replaced.
The mount/marker/path/free-space guard refuses unavailable or misconfigured storage.

| Measurement | Before | After stopped VM / exported image |
| --- | ---: | ---: |
| Internal SSD free bytes | 88,085,303,296 | 85,821,947,904 |
| TheBench free bytes | 1,133,635,264,512 | 1,093,710,807,040 |
| VM disk virtual bytes | — | 171,798,691,840 |
| VM disk physically allocated bytes | — | 32,436,912,128 |

Measurements are snapshots, not reserved capacity. macOS swap reached 2 GiB allocated
(about 1.53 GiB used at final measurement), explaining part of the internal decrease;
the entire delta cannot be attributed precisely. No large VM/download/build path fell
back to internal storage. The guest had 130,281,299,968 bytes available during export.
GNU time recorded build wall 149.41 seconds, CPU 224%, max process RSS 504,168 KiB;
these are not aggregate peak VM memory measurements. Future clean builds need continuous
VM CPU/RAM/disk telemetry before changing the initial allocation.

## Capability gate and exact inputs

PASS: native platform; ext4 ownership/uid/gid/mode/executable bits, symlink/hardlink,
case and xattr semantics; root/sudo, loop devices, partitioning, mkfs/mount/unmount,
bind mounts, device nodes, chroot/proc/sys/dev; authenticated HTTPS APT/dpkg install/
remove/source; DNS/HTTPS/Git; bidirectional SSH/rsync hash match. Loopback-only network
namespace operation also passed. No required capability failed or workaround was added.

The first full probe had PATH and xattr-read test defects; corrected probes passed,
with original failures retained. Full-stack QEMU user-binfmt is an upstream pi-gen
dependency, not a different VM backend or emulation workaround; arm64 ran natively.

| Input | Exact identity |
| --- | --- |
| Integration | `024db4985202ef0675b12e12b8982af91c6d6ad3` |
| pi-gen arm64 | `6fcca44892d5d4b36f826d2b8fb16d716369fada` |
| Resolved base | Trixie 13.7; raspberrypi-sys-mods `1:20260914`; kernel metapackages `1:6.18.50-1+rpt1` |
| VICE | 3.10 official tar; SHA-256 `8e5bac18cbcb9f192380ad3ef881f8790f5b75c41d7b3da65d831985d864d6d1` |
| Menu | local annotated `v1.1.0_poc1`, tag object `e265f3cbb995ad0a9a7748987b2d9c88019aa787`, peel `77a708019c9d8a11e657d7e5d2dde7b7ecb340ba` |
| TCPser | `fe7feff4862406b277e009d14c219f5d16cf1222`, 1.1.6_beta |
| Frozen release lock SHA-256 | `703aa6e1b0d278262a2dc83c31740b3c589788e3953e3ac822e948133529d566` |

No arbitrary main is consumed during construction. The externally retained pi-gen and
TCPser Git bundles and Menu tag/source bind exact code. [Source selection](../../build/inputs-poc.json)
is a discovery record; the full frozen lock is authoritative for construction.
Its 2,697 content-addressed objects were rehashed after transfer outside the VM.
Direct descriptors, nested closure hashes, .dsc payload SHA-256 lists, component build
records and actual Debian package control identities passed verification.

17 old bootstrap binary versions and 10 corresponding sources absent from current
indexes were recovered exactly through Debian's official snapshot API. SHA-1 snapshot
identities and local SHA-256 were verified; this is not an independently verified
historical Release-signature claim. Current APT authentication was never disabled.
libftdi1 required explicit `--only-source` lookup. Unneeded rpi-connect-lite lacked a
matching Sources entry and was explicitly excluded with a hashed patch; discovery
failures remain recorded, not presented as successful source recovery.

## Packages, integration and first boot

All three private Debian packages built with standard Debian tooling outside the
appliance. Sources, .dsc/orig/debian archives, .buildinfo/.changes and logs are retained.

| Package | SHA-256 |
| --- | --- |
| `project-cbm-vice_3.10-1+pcbm1_arm64.deb` | `674c40040965b689d08cdc225f8954c0fb2433ef68459f51aa7f6360b1710d20` |
| `project-cbm-menu_1.1.0~poc1-1+pcbm1_all.deb` | `3f7557cdbdd44922954a6e640a1bcb3a96f446f6dbe6631afe667aa5e5d5f0fd` |
| `project-cbm-tcpser_1.1.6~beta-1+pcbm1_arm64.deb` | `8b8f8a4f3ec98dddf5bdb347320dad05e1bbe5230e0ee2727248c247a5af584f` |

VICE uses SDL2/ALSA, generic ARMv8-A flags and `--disable-arch`; no build-machine-native
CPU optimization. Package dependency findings and unsuccessful configure attempts are
retained. Builds used fresh source trees in the dedicated guest; sbuild isolation and
independent package rebuilds remain future work. Menu's small packaging branch relocates
installed command paths, excludes developer/experimental helpers and unreviewed cover art.
No unrelated Menu main changes, formal tag movement or historical image content import.

[Stage/first-boot implementation](../../build/pigen/README.md) installs packages,
directories, configuration, units and minimal identity. Two hashed patches exclude
Connect and prevent export-time user rename/package upgrades. Final assembly ran in
a loopback-only network namespace against frozen APT transport. Missing inputs could
not silently fall back to upstream. Nonfatal apt-listchanges warnings for unavailable
GCC changelogs are retained; installed package payload checks passed.

The private console uses pi with locked passwords and no broad sudo. SSH, Samba,
TCPser, Avahi and NetworkManager are disabled/masked. Their future network/privilege
behavior remains incomplete; this POC does not reproduce every v1.0 control. No reusable
builder credentials are copied. VICE ROM/data came from its upstream source; public
distribution rights still need separate review.

One CBM coordinator owns growth: actual root-device discovery, checked DOS two-partition
geometry, journaled growpart/resize2fs, retry checks and user-state seeding. Vendor resize
argument/competing units are disabled; cloud-init is purged. Systemd receives an
`uninitialized` machine-id marker. No SSH keys are generated because SSH is disabled.
Pure geometry tests pass. Actual first boot, interrupted growth, fresh identity on two
flashes and persistence remain **UNTESTED**. `pcbm-info` is not implemented.

Minimal identity is 1,443 bytes at `/usr/share/project-cbm/identity.json`, generated from
the exact frozen lock. No full lock, source/closure/recovery archive or schemas are
included merely for recovery. Image hashes and qualification remain external outputs.

## Artifact and offline validation

Under `artifacts/private-poc1`:

- Raw: `2026-09-15-project-cbm-1.1.0-poc.1-lite-private-poc.img`, **3,087,007,744 bytes**;
  SHA-256 `ae8d2032736e1d3ae2e49d4370aa62d00fc06f9fc567e70e400491900d45bf9f`.
- XZ: `image_2026-09-15-project-cbm-1.1.0-poc.1-lite-private-poc.img.xz`, **596,520,504 bytes**;
  SHA-256 `b9adaaa55a7543441607fc90f7651cc35588f9c024e8a160110d857919ef2a06`.
- XZ decompression equals the retained raw bytes; `artifact-hashes.json` records this.
- `offline-checks/offline-validation.json` and `packages.tsv` retain all 50 checks and
  the 666-package installed inventory. [Validator](../../tools/validate_poc_image.py)
  uses read-only loop mounts and never executes target programs.

PASS: partition/filesystem layout, expected package versions and installed payload
checksums, Menu/VICE/TCPser files, declared service masks/enables, minimal identity
agreement, uninitialized machine-id, no host SSH keys/authorized keys/cloud state,
no obvious builder paths/history, source trees, cached .debs, compilers/development
headers or temporary build policy/proxy. Both vendor initramfs files exist. ext4
`e2fsck -fn` and FAT `fsck.fat -n` passed. Enabled CBM units passed systemd-analyze;
its first combined invocation correctly reported TCPser's intentional mask.

| Footprint (before first boot) | Bytes |
| --- | ---: |
| Boot partition | 536,870,912 |
| Root partition | 2,541,748,224 |
| Root filesystem capacity | 2,430,955,520 |
| Root used / free | 1,650,515,968 / 780,439,552 |
| Root available to ordinary user | 636,575,744 |
| Boot used | 78,420,992 |
| Installed package size sum (dpkg metadata) | 1,595,138,048 |
| VICE / Menu / TCPser installed size | 41,765,888 / 105,472 / 79,872 |

Package metadata sizes are not additive filesystem allocation measurements. Product
integration files have a small installed path inventory; no separate measured total
of every CBM-owned filesystem block is claimed. Expanded user capacity, update margin,
peak initialization space and minimum supported media size remain empirical work.

## Recovery, recreation and remaining limits

Use the host recipe to render/start a recreated VM, then re-run its capability gate.
Restore verified kit objects to a configured guest workspace using SSH/rsync. The
frozen kit includes bootstrap, exact host binary/source closure, toolchain inventory,
repository metadata, recipes and component source/packages. Replay host package
versions against retained inputs before claiming the same environment; the convenience
bootstrap package-list installation alone is not an exact lost-builder replay.
An independent offline host reconstruction and expired-metadata trust procedure are
still unperformed. Do not silently disable authentication/expiry checking years later.

To reproduce this construction after separate authorization, extract the verified
integration archive named by the lock into a recipe directory and use its schemas/tools:

```sh
python3 RECIPE/tools/retained_inputs.py KIT/release-lock.json KIT
sudo unshare --net python3 RECIPE/tools/construct_poc.py KIT/release-lock.json KIT WORKSPACE
```

Here KIT/RECIPE/WORKSPACE are operator-selected paths on suitable Linux ext4; provide
absolute paths. Construction deliberately refuses an existing `builds/private-poc1`.
Use a fresh workspace, never erase unfamiliar work. Required future host packages and
exact installed tool versions are in the retained host closure/inventory. The later
validator is retained by the final product bundle, separate from the image's frozen
integration commit. Output hashes never enter that predecessor lock.

Recovery checkpoint contains both full Git bundles, exact refs, validation records,
this input/artifact identity and a hashed catalog. Fresh offline mirrors must reproduce
every accepted local ref and pass fsck; published tags/remote refs remain unchanged.
Original historical preservation manifest still verifies all 1,677 entries unchanged.
No image asset, release or branch was pushed during this implementation.

**One controlled build is not reproducibility proven.** Filesystem/PARTUUID randomness,
timestamps, maintainer scripts, initramfs, cache/changelog state and tool/compression
behavior need an independent clean comparison. SOURCE_DATE_EPOCH helps but does not
settle this. Standard SBOM choice, independent encrypted backup/custody, signing
custody, public content/license review, measured budgets and historical v1.0 input/
build-chain gaps remain open. aria2 is deferred: curl plus explicit hashes suffices
for this POC; transport is never the trust authority.

## Exact next step — requires owner review

Authorize a physical **Pi 3B** smoke test using the retained XZ and a spare card with
adequate measured capacity, known-good power, HDMI, keyboard and audio. Verify the XZ
hash, record board/storage identity, then test first boot/growth, unique machine-id,
Menu arrival, x64sc launch and return, video/audio/input and saved configuration.
Capture logs and timings without treating a single run as qualification. Test Pi 3A+
separately for 512 MiB RAM. Later steps: interrupted/repeated first boot, two-flash
identity, larger media/USB/NVMe where targeted, remaining model matrix, and independent
clean package/image rebuild comparison. No physical test is authorized by this record.
