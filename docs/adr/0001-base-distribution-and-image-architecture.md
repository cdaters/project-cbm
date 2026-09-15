# ADR-0001: Project CBM 1.1 Base Distribution and Image Architecture

- **Status: Accepted architectural decision**, 2026-09-15, under the owner's final
  architecture/reconciliation authorization. Implementation and qualification are
  not complete or authorized by this ADR. No image or Linux host was built.
- **Decision: Option C**, Raspberry Pi OS Lite 64-bit/Trixie, pinned arm64 pi-gen
  and a small CBM integration stage, with the bounded appliance practices below.
- Supersedes the provisional foundation recommendation in the historical audit and
  the earlier requirement to embed full recovery recipes/metadata in the appliance.
- Research date: **2026-09-15**. Upstream pages/branches describe research evidence,
  not a frozen CBM input lock. Pin and retain exact revisions during implementation.

## Context and evidence rules

Project CBM is a dedicated Commodore appliance: fast console boot, Bash/dialog
front panel, SDL2 VICE, ALSA, simple content management, optional TCPser/BBS, network
file transfer, and reliable emulator-to-menu return. Pi 3 is the performance floor;
Pi 3A+ needs separate 512 MiB qualification. Low maintenance burden and long-term
project recoverability matter more than theoretical minimalism.

**Requirement (R):** owner/product constraint. **Upstream (U):** documented mechanism,
not CBM qualification. **Measured/observed (M):** direct retained evidence, with scope.
**Inference (I):** engineering judgment. **Untested (T):** assumption needing a build
or physical test. Tables of tradeoffs below are I unless explicitly marked U/R/M/T.

M: the audited 1.0 XZ is 804,405,364 bytes, its expanded image 6,839,124,480 bytes,
and its package inventory includes 1,002 packages and development residue. These
are historical artifact measurements, not a lean-system budget or RAM benchmark.
No comparative boot/RAM/build-time results exist. [Provenance](../provenance.md),
[audit composition](../audit-2026-09-15.md#actual-image-composition), [testing](../testing.md).

## Options and decisive comparison

| Option | What it means | Main benefit | Main cost | Disposition |
| --- | --- | --- | --- | --- |
| A: Raspberry Pi OS Lite + pi-gen | Pinned vendor Lite stages plus CBM stage, conventional distro administration | Shortest path to familiar vendor integration and Debian packages | Builder alone does not define sealing, data ownership, upgrade or recovery policy | Sound foundation, incorporated into C; insufficient as the complete appliance decision |
| B: Buildroot | CBM-maintained external board/package tree and selected Linux rootfs | Fine-grained dependency/footprint control and integrated cross-build | More responsibility for full-system integration, update delivery and per-model enablement | Not selected for 1.1 |
| C: Lite + pi-gen + selected appliance practices | A with explicit runtime cleanup, data/config boundaries, lifecycle, identity and release policy | Keeps vendor/package ecosystem while addressing actual v1.0 failures | Retains a larger general-purpose baseline and requires disciplined qualification | Selected; no Batocera code, runtime or dependency |
| D: rpi-image-gen | Raspberry Pi's declarative Debian image tooling | Layer/image-layout and audit facilities may reduce future custom work | New tool/config integration without a demonstrated requirement that pi-gen cannot meet | Serious fallback, not materially better for this bounded first POC |

### Upstream facts used in the comparison

U: [pi-gen's arm64 README](https://github.com/RPi-Distro/pi-gen/tree/arm64) describes
staged Raspberry Pi OS construction, stage2 Lite, configurable work/output locations
and XZ export. It expects Linux filesystem semantics; non-native QEMU building is
not its supported route. Its Lite documentation warns that development tools can
be included. A pinned branch name alone does not freeze APT inputs.

U: [Buildroot's manual](https://buildroot.org/downloads/manual/manual.html) describes
Linux-hosted cross-compilation, external project trees, download/compiler caches,
and whole-rootfs construction rather than target binary-package management.
Its legal-info output has omissions requiring review, including some external
toolchain material. Buildroot does not force read-only storage. Its
[init configuration](https://raw.githubusercontent.com/buildroot/buildroot/2026.08/system/Config.in)
offers systemd as well as smaller alternatives. The
[reproducibility option](https://raw.githubusercontent.com/buildroot/buildroot/2026.08/Config.in)
is marked experimental and warns about output-path/package limitations.

U: Buildroot is maintained, not an abandoned or unsupported option. Its
[LTS policy](https://buildroot.org/lts.html) provides three-year LTS beginning with
2025.02 and vulnerability tracking/backports. The [release listing](https://buildroot.org/download.html)
showed 2026.08 stable and 2025.02 LTS through March 2028 when reviewed. This support
does not deliver a tested CBM image or maintain CBM's custom packages automatically.

U: [rpi-image-gen](https://github.com/raspberrypi/rpi-image-gen) combines declarative
layers, mmdebstrap/bdebstrap and genimage, and advertises SBOM/CVE reporting. Its
native supported hosts are Debian Bookworm/Trixie arm64; namespace/mount capabilities
still matter even when invoking it as a regular user. Its convenience tooling is
not proof of a retained-input, offline CBM rebuild.

### Maintenance and component upgrades

| Criterion | A / C: Raspberry Pi OS | B: Buildroot |
| --- | --- | --- |
| Security/CVE response | Use Debian and Raspberry Pi package channels; CBM tracks custom software and tests integrated candidates | Adopt upstream fixes/LTS, triage selected and custom packages, rebuild and distribute a complete CBM system |
| Kernel/firmware | Preserve vendor packaging/update path; qualify selected versions and device EEPROM separately | Own board configs, kernel/firmware selection and deployment, including new-board integration |
| Dependency maintenance | Package relationships and configuration handling available; prune with runtime tests | Explicit selection can reduce dependencies, but recipe/toolchain changes require dependency rebuild discipline |
| VICE update | Build a new versioned .deb externally; qualify SDL/audio/ROM/license behavior | Change/review recipe, cross-build and requalify complete system |
| Menu update | Independently versioned package with product-pinned interfaces/config schema | Retain independent source/version; stage via a CBM Buildroot recipe |
| TCPser update | Own a small source/package recipe, pin version plus commit and test IP232 | Own equivalent recipe and dependencies, release with rebuilt system |
| OS generation upgrade | Qualified fresh image and validated content/config restore; no blind suite change | Rebase Buildroot/toolchain/board tree and regenerate full system |
| Upstream/new Pi models | Vendor enablement reduces integration work; CBM qualification still required | Upstream board recipes help, but CBM assembles missing userspace/drivers/utilities and model coverage |
| Long-term workload | Closest to existing operator skills and appliance behavior | Viable with sustained embedded-distribution ownership; no evidence that footprint savings offset this workload for CBM |

U: Raspberry Pi documents stable kernel updates through its
[normal OS update path](https://www.raspberrypi.com/documentation/computers/linux_kernel.html).
[Debian security](https://www.debian.org/security/) provides security advisories and
package updates. CBM cannot assume those channels cover locally built VICE, Menu,
TCPser, every vendor package, or a modified appliance's integration.

**Explicit answer (I): Buildroot does not presently offer enough demonstrated CBM
benefit to justify the additional ownership.** It could materially reduce footprint,
but the full SDL2/Mesa/ALSA/networking appliance would need measurement. Selecting
BusyBox instead of Bash or dropping required services to win a size comparison would
not compare equivalent products. This decision does not claim Buildroot is slow,
insecure, incompatible with Pi, or unable to recover reproducible builds.

### Build and long-term reconstruction

| Criterion | A / C | B | Required for either |
| --- | --- | --- | --- |
| Input pins | pi-gen/integration revisions plus authenticated Debian/RPi binary and source closure | Buildroot/toolchain/board revisions, source archives, hashes, patches/config | Retain bytes, not just URLs/versions; no moving inputs |
| Host | Initially native arm64 Linux or a suitable arm64 Linux VM; mount/loop capabilities, proper Linux storage | Linux cross-build host can target arm64 without running target binaries as the main build model | Record bootstrap/tool dependencies, architecture, privileges and filesystem semantics |
| Time/cache | Reuse distro binaries; custom application compile still costs time; stage copies consume disk | Toolchain/Mesa/dependency compilation may dominate cold builds; compiler cache helps | Measure cold/warm duration, peak space/RAM; caches cannot be the only retained input copy |
| Reproducibility | pi-gen is not an automatic complete lock or bitwise guarantee | Reproducibility controls are useful, not proof for every package | Two clean builds; compare packages/application/config and explain whole-image differences |
| Years-later recovery | Need complete authenticated package/source and host closure | Need complete source/toolchain and host closure, not only defconfig | Offline fresh-host reconstruction, portable kit and independently held copies |
| Provenance | Component .debs and full image inventory map to external records | Built package recipes and full image inventory map to external records | Same frozen lock generates minimal E; Q/R bind exact frozen image externally |

T: no host is provisioned, and no candidate pi-gen/Buildroot build times or resource
budgets were measured. Do not use the Pi 3 runtime floor as a build-host constraint.
TheBench-backed Linux storage is the current deployment plan; a replacement system
uses configured roots. [Build/release](../build-and-release.md), [recovery](../recovery.md).

## Hardware assessment

U: Raspberry Pi's [configuration reference](https://www.raspberrypi.com/documentation/computers/configuration.html)
distinguishes BCM2711 and BCM2712 overlay families, including 400 and 500/500+.
Buildroot's [Pi 3 arm64 configuration](https://github.com/buildroot/buildroot/blob/master/configs/raspberrypi3_64_defconfig)
lists 3B/3B+ but no named 3A+ DTB, a coverage gap to investigate rather than a
claim of incompatibility. It provides a starting point; the tagged 2026.08 file could not be retrieved in this
review, so this Pi 3 reference is explicitly a moving research source. The inspected
[2026.08 Pi 4 recipe](https://raw.githubusercontent.com/buildroot/buildroot/2026.08/configs/raspberrypi4_64_defconfig)
lists 4B/400 DTBs; its [Pi 5 recipe](https://raw.githubusercontent.com/buildroot/buildroot/2026.08/configs/raspberrypi5_defconfig)
lists 5/500 DTBs, but not a named 500+ DTB. Those recipes are per-family examples,
not a universal CBM image or evidence that 500+ cannot work.

| Target (all unqualified for CBM) | A / C integration expectation (I) | B integration work/risk (I) | Physical gate (T) |
| --- | --- | --- | --- |
| Pi 3B | Vendor arm64 baseline; protect RAM/CPU headroom | Start from Pi 3 recipe; include required drivers/userspace; avoid newer-CPU-only binaries | x64sc normal-speed workload, boot/menu latency, audio, power/thermal |
| Pi 3A+ | Same family does not prove 512 MiB fit | Minimized rootfs may help, but graphics/services still consume RAM | Memory/swap under content scans and sharing; Wi-Fi-only setup, USB hub |
| Pi 3B+ | Preserve model firmware/network support | Verify DTBs, firmware and networking independently | Ethernet/Wi-Fi, USB controllers, boot |
| Pi 4B | Vendor BCM2711 path | Recipe exists; integrate KMS/audio/network/runtime stack | Both HDMI outputs, SD/USB boot, lower-RAM board |
| Pi 400 | Vendor keyboard-computer path | Listed in Pi 4 recipe; keyboard behavior still product work | Fn/F10, keymaps, 40/80-column use, audio |
| Pi 5 | Vendor BCM2712 path | Separate kernel/config path; selected Pi 5 recipe targets Cortex-A76 | DRM selection, audio, RP1/USB, power button, SD/USB |
| Pi 500 | Vendor BCM2712 keyboard-computer path | DTB in inspected Pi 5 recipe; no inferred input pass | Integrated keyboard, Fn keys, power and network |
| Pi 500+ | Vendor enablement is preferred starting point | Explicitly verify required kernel/firmware/DTB and boot integration; coverage not established by inspected recipe | NVMe expansion/boot, EEPROM, keyboard/power/display/audio |

A Pi 5-optimized userspace must not become the sole Pi 3–500+ artifact. A common
arm64 baseline with the vendor's model kernel/firmware coverage is the target; prove
it per model. Device EEPROM is not determined by installed image packages.
CM/Zero models are outside automatic inclusion. Vendor new-model support is a
maintenance advantage, never permission to mark a CBM test cell passed.

### Graphics, audio, input and network across the options

U: SDL2 has a [KMSDRM backend](https://raw.githubusercontent.com/libsdl-org/SDL/SDL2/src/video/kmsdrm/SDL_kmsdrmvideo.c)
and its [Linux notes](https://raw.githubusercontent.com/libsdl-org/SDL/SDL2/docs/README-linux.md)
identify runtime library and udev/input dependencies. Raspberry Pi's
[OS utilities documentation](https://www.raspberrypi.com/documentation/computers/os.html)
notes different DRM-card layout on Pi 5+ and dynamic card numbering.

I: A/C inherit more of the vendor kernel/Mesa/firmware/ALSA/udev integration; B can
assemble the same mechanisms but CBM must select and validate them. Neither builder
settles SDL device access, display mode, framebuffer splash coexistence, HDMI/USB
sound routing, controller enumeration or reliable console return. Keep direct ALSA;
prefer stable discovered device identities over numeric assumptions during later
runtime work. Test Wi-Fi firmware/regulatory settings, Ethernet, DHCP, hotplug and
offline boot on each relevant model. Raspberry Pi utilities such as raspi-config,
vcgencmd and kmsprint are useful diagnostics; in B equivalent utilities must be
selected/ported rather than assumed present. No desktop is required by any option.

## Runtime assessment across foundations

| Runtime criterion | A / C assessment (I) | B assessment (I) |
| --- | --- | --- |
| Footprint | Larger distro starting point; remove non-runtime payloads with dependency checks | More selection control; compare only after including equivalent VICE/SDL2/audio/network features |
| RAM | Services, emulator and display stack dominate the question; measure PSS/RSS and swap | Smaller userspace may help; filesystem size alone says little about emulator RAM or audio continuity |
| Boot | Keep console and remove unnecessary waits/services after measurement | Minimal init/service selection may boot faster; no CBM measurements establish an advantage |
| SSH/admin/debugging | Familiar package-managed tools and systemd logs, within explicit exposure policy | Possible, but CBM must select tools/logging; a tiny shell image is not equivalent support capability |
| Samba/Avahi | Retain packaged capability, qualify credentials/discovery and declare defaults | Available mechanisms need selection, integration and CVE/update ownership; no required always-on discovery |
| Write state | Conventional persistent config/logs/saves; bound growth | Neither Buildroot nor immutable storage eliminates persistent identity/config/Samba/VICE state |
| Power-loss recovery | Writable-root failure cases need tests | Read-only models can reduce base writes but still need userdata/boot/update recovery tests |
| Init/first boot | Keep systemd and coordinate existing vendor mechanisms | Can choose systemd or alternatives, but changing init would expand Menu/service compatibility work |

T: no option has a measured CBM boot-time, RAM or power-loss advantage. The selected
foundation reduces integration uncertainty; qualification must test that inference.

## Selected appliance patterns and storage design

U: Batocera documents separate [system/userdata organization](https://wiki.batocera.org/batocera.linux_architecture),
[boot-partition editing](https://wiki.batocera.org/edit_boot_partition),
[lifecycle scripts](https://wiki.batocera.org/launch_a_script), and an
[overlay persistence workflow](https://wiki.batocera.org/modify_the_system_while_it_s_running).
These illustrate useful concepts. CBM adopts no Batocera code, configuration, hooks,
root scripts, filesystem image or dependency. Filesystem claims are evaluated using
Linux documentation below, rather than copying the wiki's filesystem rankings.

| Pattern | 1.1 decision (R/I) | Reason |
| --- | --- | --- |
| Explicit system versus user-data ownership | Adopt now as architecture | Make backup, migration and future mounts possible without rewriting launch semantics |
| Keep build/development/recovery material external | Adopt now | Preserves user capacity and reduces accidental release state |
| Minimal release identity and reproducible external provenance | Adopt now | Support can identify a base without shipping developer infrastructure |
| Retry-safe first boot; defined startup/launch/exit lifecycle | Adopt now | Direct response to observed identity/launch/expansion weaknesses |
| Separate internal USERDATA partition | Defer | Partition boundaries do not automatically preserve data during whole-disk flashing |
| Read-only/SquashFS/OverlayFS system | Defer | Update/config/log/write-state design and Pi 3 cost need evidence |
| A/B or firmware-style transactional system updater | Defer | Requires boot selection, rollback, power-fail and migration design |
| User-defined lifecycle scripting API | Defer | No concrete use case justifies a public extension/security contract yet |
| Root execution of scripts from imported content or boot media | Reject | Content transfer must not become an implicit privileged execution interface |
| Batocera frontend/multi-emulator/plugin framework | Reject for CBM | Does not serve the dedicated Commodore scope |
| Full project recovery kit in runtime image | Reject | Owner clarification: development/release infrastructure responsibility |

### System and user data

**Decision: keep FAT boot plus a single writable ext4 root for 1.1**, with logical
ownership boundaries. Keep `/home/pi/pcbm` as the default content location to avoid
an unnecessary path migration. User preferences remain separate from package-owned
defaults and machine credentials; legacy preference paths must be explicitly mapped
by a future backup/config schema. Define one product-configured content root; do not
scatter hard-coded assumptions through launch/import/share helpers.

SYSTEM: OS, VICE, Menu, TCPser when included, runtime libraries and static assets.
USERDATA: games, demos, music, programs, ROMs, screenshots, saves and validated user
configuration. Machine IDs, SSH keys, credentials, service policy and boot settings
are not ordinary user-preference restore payloads.

| Layout | Assessment |
| --- | --- |
| Existing root + conventional /home | Selected: simplest capacity sharing and expansion; content can fill root, so free-space reporting, bounded logs/cache and failure handling are qualification requirements |
| Separate internal ext4 USERDATA partition/filesystem | Better allocation/isolation, potential future system-only update; adds partition sizing, grow ordering, mount failure and migration work; root can outgrow its allocation |
| Separate /home filesystem | Familiar layout but mixes content/preferences with identity and dotfile state unless backup selection is explicit |
| Bind mount from external/separate filesystem | Useful future compatibility bridge retaining `/home/pi/pcbm`; require mount-before-launch/sharing and fail closed when missing, so data is not written under an absent mount |
| Symlink/alternate configured content root | May support advanced storage later; must handle permissions, availability and backup paths deliberately |

A separate partition on the same device is not a backup and a full-disk flash can
destroy it. Initial release upgrades use verified backup, fresh flash and validated
restore, with explicit overwrite warnings. Later system-only upgrades may preserve
USERDATA only after a tested partition/update contract. Larger cards should provide
more usable content capacity. SD, USB and NVMe layouts must not assume `mmcblk0`.

### Writable versus immutable system

| Model | Gain | Cost/limit for CBM | Decision |
| --- | --- | --- | --- |
| Writable ext4 | Familiar administration, package updates, persistent config/logs | More writable state; interrupted updates/writes need recovery | Select for 1.1 |
| Read-only ext4 + explicit writable locations | Protects base from normal writes | Must enumerate /etc, /var, identity, Samba/VICE state; maintenance remount/update workflow | Defer |
| SquashFS + persistent data | Compressed read-only base, whole-system replacement | New image/update/boot path; decompression/cache costs and writable state still exist | Defer |
| Read-only lower + tmpfs OverlayFS | Disposable runtime changes | RAM use and copy-up; persistence surprises; especially risky to assume fit on 3A+ | Defer |
| Read-only lower + persistent OverlayFS | Base isolation with persistent changes | Upper-layer drift/copy-up storage and compatibility across base replacement | Defer |
| Verified immutable base/A-B | Potential authentication/rollback benefits | Signing, boot integration, duplicate system space and interrupted-update machinery | Defer until an explicit deployment need |

U: [ext4 journaling](https://docs.kernel.org/filesystems/ext4/journal.html) protects
metadata consistency; default journaling does not guarantee all file contents after
a crash. [SquashFS](https://docs.kernel.org/filesystems/squashfs.html) is compressed
and read-only. [OverlayFS](https://docs.kernel.org/filesystems/overlayfs.html) combines
layers and can copy lower files into the writable upper layer on writes.

I: read-only does not protect writable saves, boot media or a failing storage device.
A partition boundary alone cannot solve abrupt power loss. For writable 1.1 use
bounded logs/cache, atomic validated preference updates and orderly shutdown; measure
unclean-power recovery and interrupted first boot/update. Do not disable useful
journaling or use a RAM overlay just to report a smaller image or fewer writes.
SSH troubleshooting and ordinary Linux administration remain possible; public service
exposure is governed separately below. No corruption-resistance claim is measured yet.

### Footprint and user capacity

R: **no mandated 8 GB SD-card minimum**. The earlier 16 GB suggestion is historical
user guidance, not the measured minimum for 1.1. Select the architecture on product
needs, then measure raw/XZ bytes, filesystem-used bytes, runtime package footprint,
first-boot growth, steady-state logs/cache/swap needs and free user-data bytes on
actual media. Reserve safe maintenance/first-boot margin before publishing a minimum.

Remove compilers, source trees, headers, build caches, development packages and full
recovery archives unless a documented runtime requirement exists. Retain necessary
runtime interpreters/tools and license notices. Preprocess static assets where it
preserves display behavior. Do not strip essential firmware/debugging capability
blindly. Free capacity should remain available for Commodore content and user state.

## First boot and construction boundary

**Construction:** install runtime packages/defaults/static assets; establish paths
and permissions; set explicit service policy; generate minimal E from frozen L;
seal away reusable machine IDs, SSH keys, credentials, random seed/provisioning state,
builder homes/logs and caches. Retain sources and full records externally. Do not
initialize every clone with the build host's identity.

**First boot:** use one coordinated, retry-safe policy to expand the actual root
filesystem on its actual device, obtain fresh device identity and SSH host keys,
initialize validated user config without overwriting existing choices, and complete
local/offline account setup. Persist completion only after the relevant step succeeds.
Do not regenerate established keys merely because a later step is retried.
No USERDATA partition creation is required by the selected layout.

U: [systemd image guidance](https://systemd.io/BUILDING_IMAGES/) describes removal or
reset of cloned identity/seed state and automatic machine-ID initialization.
I: delegate to the selected upstream mechanisms where appropriate; “one owner” means
one product policy and ordering, not replacing systemd's identity implementation.
Choose the exact pi-gen/cloud-init/growth integration after reviewing the pinned
inputs. Never stack PiShrink, cloud-init resize and another competing grow service.
Test missing/empty/uninitialized machine-id semantics for the selected systemd version.

Network recommendation: TCPser opt-in; SSH/Samba access only after usable unique
identity and explicit credentials. Avahi/mDNS is optional discovery tied to the chosen
network-sharing policy, not a new always-on requirement. Preserve required network
access capability. Exact installed/enabled/active defaults and bindings for each
service must be recorded and security-reviewed before candidate assembly; do not
inherit v1.0 or upstream defaults accidentally. The choice of builder does not set
them. This ADR changes no running service.

## Lifecycle and hooks

**Decision:** use ordinary systemd units for system services/startup/shutdown and a
small shared Bash launcher contract for before-VICE/after-exit responsibilities
without a separate hook engine. Startup first checks initialization;
launch validates machine/media and prepares display/audio; exit and failure paths
restore the console/menu. Service start/stop uses the service manager.

U: [systemd.service](https://manpages.debian.org/trixie/systemd/systemd.service.5.en.html)
provides explicit start, stop, post-stop and timeout behavior. I: specify ordering,
arguments, environment, user/privilege, timeout and error/cleanup behavior in focused
interfaces when implemented. Shell traps cannot promise cleanup on power loss or
SIGKILL; startup recovery must cope. Shutdown hooks cannot guarantee a final write
when power is removed. No automatic execution of user-media scripts, root hooks or
elaborate plugin framework. A public opt-in unprivileged hook API can be reconsidered
only for a concrete use case with bounded behavior.

## Updates and packaging

**Update model:** retain package-based administration for controlled same-suite
maintenance; publish new tested CBM images for product/base-generation upgrades,
using backup/reflash/validated restore. Do not add a self-updater, A/B slots or an
in-place distribution conversion to 1.1. Do not pull arbitrary Git branches on an
appliance. New package state is live drift from the original E, not a newly qualified
base release; E remains unchanged. Security fixes must not be frozen forever merely
to preserve reproducibility: retain old inputs while qualifying updated candidates.

U: Raspberry Pi documents [APT updates and free-space checks](https://www.raspberrypi.com/documentation/computers/os.html).
I: before release, document which tested update combinations CBM supports and how to
recover interrupted updates. APT capability is not a promise that every future
upstream package combination is qualified. Firmware-style replacement is a better
fit for B, but CBM would still need to design data preservation and recovery.

**Packaging decision:** build VICE, Menu and TCPser outside the final appliance as
separately versioned Debian packages. Prefer standard `/usr` package paths, with a
reviewed launcher-path transition from v1.0 `/usr/local`. Menu owns its package and
interfaces; product owns integration/service/defaults, VICE/TCPser recipes and the
complete release mapping. Keep Menu tag/peeled commit/artifact hash independent of
product version. Record source, patches, flags, licenses and corresponding source.
Start with VICE 3.10 SDL2/ALSA; review TCPser's shipped lineage explicitly.

A retained local package repository/directory is sufficient initially; no public
package server is required. Split build dependencies/debug/source packages from the
runtime payload. Staged tarballs are useful intermediate evidence, but package file
ownership/dependencies/config handling better fit this foundation. For B the matching
choice would be Buildroot recipes in a CBM external tree and staged rootfs artifacts,
not pretending Debian packages can simply be installed into an arbitrary rootfs.
No component packaging is implemented in this phase.

## Boot partition and recovery access

Keep the vendor FAT boot model and document read-only offline access for troubleshooting.
Minimal nonsecret support identity may be mirrored there later if a demonstrated
support need justifies it; generate any copy from E and verify agreement. It is not
a second authority or a recovery kit. No credentials, private keys or sensitive
network configuration should be exposed for convenience. Boot edits can prevent
booting and FAT does not provide Unix permission isolation; avoid general root
script ingestion. An offline support note can point to retained project docs without
requiring them to be bundled on the appliance. Full recovery remains external.

## Consequences and rejected alternatives

We gain continuity with the existing console appliance, vendor enablement and ordinary
Debian administration while fixing the build/release boundary. We accept a potentially
larger baseline, package-closure retention work, writable-root failure modes and real
per-model qualification cost. We must actively audit Lite's dependency selection;
“Lite” is not proof of a clean production payload.

A is retained as the base but C explicitly settles the surrounding appliance policy.
B is rejected for 1.1 on maintenance/value grounds, not theoretical capability.
D is deferred because no blocking pi-gen limitation has been demonstrated; its
layering/audit strengths are worth revisiting if they remove measured complexity.
Custom debootstrap/framework construction is rejected: CBM should not own another
boot/image framework when maintained upstream tooling can serve the initial target.
No numeric scoring or invented performance result is used to select a winner.

## Revisit triggers

Reopen only with recorded evidence of one of these, and compare equivalent workloads:

1. Pruned Lite fails agreed Pi 3/3A+ RAM, normal-speed audio, boot or capacity budgets,
   and a measured alternative remedies it with a credible maintenance plan.
2. pi-gen cannot satisfy retained-input/offline reconstruction or required layouts
   without substantial custom machinery; demonstrate how rpi-image-gen or B resolves it.
3. Vendor package/support availability blocks a required model or sustainable security
   response; quantify the delta and ownership of the proposed replacement.
4. Repeated field power-loss failures justify immutable-system complexity, or a real
   unattended deployment requires transactional rollback/system-only updates.
5. Measured reflash/restore burden or storage-fill failures justify separate USERDATA.
6. A maintained Buildroot implementation demonstrates material runtime benefit with
   a named owner and sustainable update/hardware qualification resources.

A newer tool release, an arbitrary card label, or Batocera's success alone is not a
revisit trigger. Physical questions remain boot/latency/RAM/audio/input/KMS/network,
Pi 500+ NVMe/EEPROM, footprint/free space, unclean power, first-boot retry/two-flash
identity and migration/update recovery. [Testing](../testing.md) tracks these gates.
The next task is the separately authorized [1.1 POC](../build-and-release.md#new-session-first-task),
not further open-ended foundation debate. Stop this phase after documentation commits.
