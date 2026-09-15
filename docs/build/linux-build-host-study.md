# Linux build host: owner decision checkpoint

Research date: **2026-09-15**. Status: **historical proposal; owner approved Lima/VZ with 10 GiB RAM**.
See [approved implementation](lima-build-host.md) for the current recipe/status.
The observations and proposed 12 GiB below record the pre-approval study.
No VM/container/hypervisor was installed or started, no Linux disk allocated, and no
package or image built. ADR-0001 remains accepted; this selects a build host, not a
new appliance foundation. Small host-only Python contract dependencies were installed
in an isolated temporary test environment; they are not Linux infrastructure.

## Recommendation

**Use a dedicated arm64 Debian 13/Trixie VM managed by Lima, with Apple's VZ backend,
plain mode, and all VM disks/download cache/build data on TheBench.** Start with
8 virtual CPUs, 12 GiB RAM and a 160 GiB sparse virtual disk containing ext4. Use
standard SSH/file transfer and build directly inside the guest; add isolated Debian
package-build environments there after approval. Do not add a Docker layer initially.

This is engineering judgment: native arm64 execution and an independently managed
Debian kernel give pi-gen the Linux mechanisms it needs, while declarative VM setup
and ordinary Debian tooling make unattended reconstruction simpler. Lima is an
open-source frontend; Apple's installed virtualization framework/macOS are proprietary.
The underlying Linux recipe must work without Lima on another suitable arm64 host.
No M4 build-time benchmark or actual guest capability pass is claimed.

**UTM with an arm64 Debian VM is the strongest alternative** if a visible VM console
and manual recovery workflow matter more than declarative lifecycle automation, or
Lima's cache/socket constraints cannot be cleanly accommodated. Both are viable;
therefore the owner checkpoint is mandatory, not a formality.

## Observed local environment (M)

Read-only inspection found Mac mini M4 Pro, 12 CPU cores (8 performance/4 efficiency),
24 GB RAM, macOS 27.0 build 26A428. Internal free space is about 82 GiB; TheBench has
about 1.0 TiB free on its 2 TB APFS volume. These are observations, not reserved space.
Parallels Desktop 26.2.1 and OrbStack 2.2.1 are installed. The `docker` command points
into OrbStack; its presence does not mean Docker Desktop or a suitable builder exists.
Lima/UTM/Podman/QEMU CLI tools were not found. No existing VM was started or inspected
for private contents, and license/subscription ownership was not inferred.

## Required Linux capabilities (R/U)

The observed [pi-gen arm64 source](https://github.com/RPi-Distro/pi-gen/tree/6fcca44892d5d4b36f826d2b8fb16d716369fada)
is commit `6fcca44892d5d4b36f826d2b8fb16d716369fada`; it is research evidence, not a
frozen CBM release input. It requires Debian-based Linux and proper Linux build
storage; native arm64 avoids the unsupported non-native emulation route. Its work
stages can consume tens of GiB. CPU architecture alone does not make macOS a Linux host.

The inspected [build script](https://github.com/RPi-Distro/pi-gen/blob/6fcca44892d5d4b36f826d2b8fb16d716369fada/build.sh)
checks native arm64 execution. Its [container wrapper](https://github.com/RPi-Distro/pi-gen/blob/6fcca44892d5d4b36f826d2b8fb16d716369fada/build-docker.sh)
uses privileged execution and Linux kernel/device facilities. Guest root/sudo,
loop devices/partition scanning, mount/unmount, chroot, /proc,/sys,/dev handling and
ext4 tools must work. Native package construction additionally needs a pinned Debian
build environment and complete compiler/header/build-dependency closure. No nested
hardware virtualization or Pi GPU is needed to construct packages/images.

After approval, a disposable capability probe must verify loop attachment, partition
visibility, mount/chroot cleanup, native arm64 execution, ext4 ownership/modes,
case sensitivity, symlinks/hardlinks/xattrs and adequate free space. Record guest
kernel/page size and exact tool versions. Rootless containers are not an equivalent
host for this unmodified privileged pipeline. A running systemd in a full VM is
ordinary Linux administration; target services must still be suppressed in chroots.

## Options compared (I unless cited)

| Option | pi-gen/packaging fit | Storage, isolation and automation | Ownership/cost/tradeoff |
| --- | --- | --- | --- |
| Lima + VZ arm64 Debian VM | Strong expected fit: native arm64, own Debian kernel, root/loops/chroot; untested | Entire state/disk on configured external root; plain mode limits integration; declarative config + SSH suitable for unattended builds | Free Apache-2.0 frontend; Apple framework dependency; cache relocation/socket constraints require explicit setup |
| UTM arm64 Debian VM | Strong expected fit; own kernel and ext4; untested | Store VM bundle/drive on TheBench; SSH automation after creation; useful console | Free/open source download; more GUI/bootstrap capture work. Automation exists but does not expose every feature |
| Installed Parallels arm64 VM | Technically viable with appropriate guest/resources | External VM bundle, own kernel, SSH automation; disable unnecessary Mac sharing | Proprietary/commercial; installed does not establish suitable license/resource limits. No demonstrated CBM benefit justifies preferring it over free tools |
| Installed OrbStack Linux machine or Docker backend | Plausible, but kernel/loop/mount/storage controls need a capability proof | Shared optimized kernel; isolated mode reduces Mac integration; existing application data must not be moved casually | Proprietary frontend, free personal use under vendor terms; exact kernel ownership and reconstruction add coupling. Existing convenience is not decisive |
| Docker Desktop, Podman machine, Colima-style container host | Potentially works with rootful privileged container and suitable Linux VM kernel | Still needs a Linux VM on macOS; two configuration layers; APFS bind mounts remain unsuitable build roots | Open-source engines do not make every frontend free/open; little first-POC value over a dedicated VM. Rootless mode fails required capability contract |
| Dedicated Raspberry Pi/other native arm64 Linux machine | Strongest ordinary-Linux fit with adequate RAM and SSD | Native ext4/loops; SSH automation; separate failure/power domain; transfer artifacts to TheBench | No Mac frontend dependency, but hardware/power/storage and another maintained host. A Pi 3 is the runtime floor, not a sensible build-host constraint |
| Remote native arm64 Linux VM/server | Viable if provider grants required guest root/kernel/device controls | Remote Linux disk plus verified transfer to retained storage; CI possible | Recurring compute/storage/egress costs, network/custody dependence and provider setup. No existing suitable host is established |
| macOS native or x86 emulation as default | macOS lacks Linux kernel/chroot semantics; x86 adds target-execution emulation | Shared architecture/translated tools do not supply Linux behavior | Reject native macOS. Keep x86/emulation outside first supported factory unless evidence demands it |

Upstream evidence for option-specific facts:

- [Lima VZ](https://lima-vm.io/docs/config/vmtype/vz/),
  [plain mode](https://lima-vm.io/docs/config/plain/) and
  [license](https://github.com/lima-vm/lima/blob/master/LICENSE): VZ provides the Mac
  VM backend; plain mode disables host mounts, automatic containerd, guest-agent
  convenience and SSH agent forwarding while retaining SSH/base provisioning.
- [UTM free/open-source installation](https://docs.getutm.app/installation/macos/),
  [drive settings](https://docs.getutm.app/settings-apple/drive/) and
  [scripting](https://docs.getutm.app/scripting/scripting/): VM disks and CLI/AppleScript
  lifecycle support exist; not every setting is exposed through automation.
- [Parallels Apple Silicon](https://kb.parallels.com/en/125343) documents arm64 guests;
  [product editions](https://www.parallels.com/products/desktop/) establish commercial
  choices. Verify purchased edition and resource limits before selecting it.
- [OrbStack architecture](https://docs.orbstack.dev/architecture) documents its shared
  kernel and Mac integration; [machine documentation](https://docs.orbstack.dev/machines/)
  does not officially support custom kernel modules;
  [isolated machines](https://docs.orbstack.dev/machines/isolated) reduce integration.
  [Pricing](https://orbstack.dev/pricing) distinguishes free personal and paid use.
  Do not infer loop support failure just from custom-module limitations; test it.
- [Podman machine](https://docs.podman.io/en/latest/markdown/podman-machine.1.html)
  documents the Linux VM requirement on macOS; [Docker privileges](https://docs.docker.com/engine/containers/run/)
  document the broad capabilities of privileged containers. They do not eliminate
  VM-kernel dependence or make host-shared APFS into ext4.

No option has measured CBM build performance. Local native arm64 virtualization
should use the M4 efficiently, but I/O, stage copying and compression may dominate.
Compare cold/warm elapsed time, peak memory and disk use after approval. A VM is an
isolation boundary, not permission to run unreviewed historical scripts or expose
builder identity in an image. Keep the package/image process independent of frontend
APIs so it can move to native/remote arm64 Linux later.

## Proposed concrete host/storage envelope

These are requested limits/estimates, **not allocations already made**:

- Host frontend candidate: [Lima v2.2.0](https://github.com/lima-vm/lima/releases/tag/v2.2.0),
  observed through GitHub release metadata. Pin and retain the arm64 release binary,
  checksum/source/license and required guest-agent payloads before installation.
  Prefer its minimal release distribution over installing unrelated container tooling.
- Guest: Debian 13/Trixie arm64, generic Linux kernel, ext4, no desktop. Current
  [Debian release information](https://www.debian.org/releases/trixie/) reports 13.7;
  a dated bootstrap artifact/hash and authenticated host package snapshot are still
  to be selected and retained. Do not use a moving `latest` URL in the final recipe.
- Compute: 8 vCPUs, 12 GiB RAM, initial build concurrency 6; leaves roughly half the
  Mac RAM for macOS/tools. Do not infer performance-core pinning from vCPU count.
- Disk: one **160 GiB sparse virtual disk**, initially estimated 40–100 GiB allocated
  during the POC. The estimate includes stage copies, package environments and images;
  measure it. Sparse virtual capacity is not reserved physical capacity.
- Require at least **256 GiB external free space** before initial provisioning/build
  and recheck actual free space in host and guest at stage boundaries. This is a
  proposed factory safety budget, not the appliance/card minimum. Adjust only from
  measurements and renewed review if the required host allocation materially changes.

Proposed layout under configured bulk root (today TheBench):

```text
build-host/lima/          Lima state and 160 GiB virtual disk; private host identity
cache/lima/               Lima downloads/conversions, external and recreatable
inputs/build-host/        Verified bootstrap and frontend/tool inputs
inputs/, packages/       Retained source/package/closure inputs
artifacts/, qualification/  Candidate output/provenance
archive/                 Standalone checkpoints and restore evidence
```

Inside the VM, use `/srv/project-cbm/{inputs,packages,builds,cache,artifacts,scratch}`
on its ext4 disk. Transfer verified immutable files with SSH/scp/rsync; plain mode
needs no general Mac filesystem sharing. Build copies/checkouts live on ext4, never
under APFS, VirtioFS, SSHFS or an accidental Mac home mount. TheBench stores the disk
file; the guest filesystem supplies Linux semantics. Final artifacts transfer back
and are rehashed before acceptance. Existing original evidence directories are never
mounted into the builder.

**Lima storage caveat:** [LIMA_HOME](https://lima-vm.io/docs/config/environment-variables/)
relocates state, but [Lima internals](https://lima-vm.io/docs/dev/internals/) document
`~/Library/Caches/lima` as the macOS cache location and a 104-character socket-path
limit. Do not assume XDG_CACHE_HOME relocates that Mac cache. Approval of this option
must include explicit cache placement: verify the pinned release's supported override,
or create a reviewed symlink at that cache path into `cache/lima` before its first
download. Inspect/preserve any existing cache; never replace it blindly. This is a
specific host-path change to approve, not something already done. Keep LIMA_HOME and
instance names short; validate socket paths before VM creation. If these constraints
cannot be satisfied cleanly, stop and propose UTM rather than fall back internally.

Raw disk conversion/copying can consume full virtual capacity. Stop the VM before
backup, preserve sparsity with a verified method, and measure allocated bytes; an
APFS clone on TheBench is not independent backup. Guest keys/host state stay private
on this presently unencrypted disk. Independent encrypted backup/custody remains open.
No Mac global temp setting, Docker data root, existing VM or home directory was changed.

## Reconstruction and post-approval sequence

1. Retain owner decision and exact frontend/bootstrap URLs, hashes, signatures/trust,
   source/licenses, guest config and host package/tool closure. Record macOS/VZ version
   as execution context; Linux recipe must not require this exact Mac model/path.
2. Register the expected mounted workspace/marker and free-space floor. Establish
   external VM state, cache/download/temp paths and guard every launcher operation.
3. Install the approved pinned frontend and create the guest from retained bootstrap
   bytes/config. Keep personal host shares, agent forwarding and host credential imports
   off; provision builder-only access privately. No GUI Windows or Microsoft dependency.
4. Run disposable Linux capability probes; record PASS/FAIL with versions. If loops,
   mounts, native execution, filesystem semantics or storage routing fail, stop before
   pi-gen and revise the implementation plan rather than changing the foundation silently.
5. Install exact package-building/pi-gen dependencies from retained metadata; create
   clean component build environments. Complete real source provenance, Menu candidate
   and service/account/first-boot decisions before freezing a real image input lock.
6. Prove standard SSH-driven reconstruction, then lost-builder/offline reconstruction
   from the kit. Store recipes and inputs, not only the VM. A replacement native arm64
   Linux host runs the same package/image process with configured storage roots.

## Owner checkpoint

Approve Lima/VZ/arm64 Debian with the envelope and explicit cache placement above,
or select UTM, an existing commercial frontend, or a native/remote Linux host with
its tradeoffs. **Do not provision until the owner answers.** No VM YAML, provisioning
script or runnable builder has been created to pre-empt that choice. Exact bootstrap
hash/package closure and actual host capability/performance tests remain incomplete.
