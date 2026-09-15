# Component packages and minimal integration stage

Design only, 2026-09-15. No Debian package recipe, pi-gen stage or runtime change is
implemented. [Contracts](contracts.md) implement declared metadata validation only.
ADR-0001's foundation is closed; this specifies the first private POC boundary.

## Debian package ownership

Use standard debhelper/dpkg-buildpackage, with fresh arm64 Debian Trixie package-build
environments, preferably sbuild after host approval. [sbuild](https://manpages.debian.org/trixie/sbuild/sbuild.1.en.html)
supports isolated package building; [Debian build guidance](https://www.debian.org/doc/manuals/maint-guide/build.en.html)
identifies source and build outputs. Keep .dsc, source tarballs, .buildinfo, .changes,
logs, toolchain and dependency closure. No component is compiled in the final rootfs.
Menu's packaging recipe belongs in its own repository when that work starts.

| Package | Architecture/version direction | Runtime payload and ownership |
| --- | --- | --- |
| project-cbm-vice | arm64, initially `3.10-1+pcbm1` | VICE executables under /usr/bin; runtime data under /usr/share/vice; no compilers, headers, build trees or caches |
| project-cbm-menu | all, `<Menu version>-<packaging revision>` | Reviewed scripts under /usr/bin/pcbm-* and static assets under /usr/share/project-cbm-menu; default templates there; no invocation of historical installer/docs-sync/release-prep during build |
| project-cbm-tcpser | arm64, upstream label `1.1.6_beta` can map to Debian `1.1.6~beta-1+pcbm1` if selected | /usr/bin/tcpser, notices; reusable service unit only if agreed with product integration; no automatic enable/start during construction |

These are names/version rules, not built or released packages. A Menu candidate
must be reviewed, independently versioned/tagged and hashed; neither formal 1.0.0
nor the forensic recovery root is silently selected as the 1.1 dependency. New packaging
may require a Menu branch later. Do not create one just to mirror the product branch.

Derive shared-library dependencies with dpkg-shlibdeps; explicit script dependencies
include Bash/dialog and the actual binaries used by retained helpers. VICE build
dependencies include the C/C++ toolchain and chosen SDL2/ALSA development libraries;
freeze the complete set from a successful clean configure/build, not a guessed list.
Verify actual ELF dependencies, architecture and installed-file ownership. SDL2 KMSDRM,
Mesa/DRM/GBM/input support, ALSA utilities, network tools and vendor firmware are
integration runtime dependencies that must survive pruning. Use Debian arm64 baseline
flags suitable for Pi 3, never M4/Pi 5 `-march=native` or a newer-CPU-only package.

If VICE/TCPser files conflict with distro packages, declare reviewed Conflicts/Replaces
relationships rather than overwriting files; see [Debian relationships](https://www.debian.org/doc/debian-policy/ch-relationships.html).
Do not invent a Provides version until compatibility is tested. A future product
integration package may own product defaults/services, but an extra package is not
required for the first stage: retain a stage-installed ownership manifest instead.

## Configuration and service boundary

Product integration owns /etc/pcbm, service policy, account/content paths, permissions,
minimal identity and first-boot coordination. Menu owns UI/interfaces, not product
version or credentials. Keep immutable templates in /usr/share and seed user preferences
only when absent into /home/pi/.config/pcbm; VICE owns /home/pi/.config/vice. User data
stays /home/pi/pcbm. Packages must not own individual user saves/configuration files.

Administrator-edited files installed by packages under /etc use conffile handling;
generated user files are not conffiles. Maintainer scripts must be retry-safe and must
not reset choices or start services in the build chroot. Use the standard Debian
service helpers and controlled policy-rc.d during image assembly, with product policy
setting final enabled/masked state. [Debian maintainer-script policy](https://www.debian.org/doc/debian-policy/ch-maintainerscripts.html)
explains idempotence and installation sequencing. Exact units/defaults remain a reviewed
implementation decision; no historical Samba/TCPser/sudo behavior is changed here.

GPL corresponding-source requirements for VICE/TCPser and every dependency, Menu MIT
notices, and separate ROM/media/font/art rights must be reviewed before redistribution.
Do not import private image content into packages as a shortcut. Strip debug data to
separate retained debug artifacts when useful, without removing required runtime assets.

## Smallest future stage

Observed upstream arm64 tip for research:
`6fcca44892d5d4b36f826d2b8fb16d716369fada` (2026-09-15). This is not an accepted release
pin. Its [build.sh](https://github.com/RPi-Distro/pi-gen/blob/6fcca44892d5d4b36f826d2b8fb16d716369fada/build.sh)
selects arm64/Trixie and checks native executable support. The factory must retain
and freeze the actual chosen revision plus all APT inputs before a real build.

Ordered stage contract: `stage0 -> stage1 -> stage2 -> stage-cbm`. No desktop stages.
Only the final CBM stage exports the candidate; suppress upstream intermediate-image
exports. pi-gen's stage convention supports package lists/chroot scripts, but the
CBM launcher must verify frozen inputs before executing any sourced shell config.
JSON locks are data and must never be eval'ed or sourced as shell.

The future integration stage must:

1. Verify lock/schema, retained artifact bytes, clean integration source, chosen
   Menu tag/peeled commit, package control metadata and full transitive closure.
2. Install exact versioned CBM .debs from retained local inputs, with service startup
   suppressed during assembly. Resolve dependencies from the frozen repository state.
3. Install product-owned defaults/static assets/required directories and record every
   owned path. Preserve the recognizable console/menu -> VICE -> menu flow first.
4. Install generated minimal identity and first-boot policy. Preserve /home/pi/pcbm;
   no USERDATA partition, immutable root, plugin framework or sophisticated updater.
5. Audit actual installed packages/files and remove unnecessary development residue.
   Use a reviewed runtime allowlist/dependency check, not an indiscriminate autoremove.
6. Seal machine/credential/build residue, validate the offline image, export once,
   then hash raw/compressed outputs and write external provenance.

No runnable stage is supplied yet. Before assembly, explicitly settle SSH/Samba/TCPser/
Avahi installed/enabled/active defaults, credentials and privilege policy. ADR recommends
TCPser opt-in and gates network access on initialized identity/credentials. SSH default
is not approved merely because upstream has a default. Essential v1.0 behavior means
console/menu/emulation/return and content paths; it does not authorize cloning baked
keys, private residue or silently shipping broad legacy sudo rules.

## Later POC gates

Offline: partition/fstab/root identity, installed package/hash/version agreement,
absence of build tools/private identity, required runtime files, service enablement
inventory, content rights, first-boot ownership and footprint. Compare two clean
builds from identical inputs; initially distinguish semantic from bitwise equivalence.
Then physical Pi boot/menu/VICE-return/audio/KMS/controller/network/expansion tests,
starting with Pi 3 and separately Pi 3A+. A Mac VM can build ARM64 binaries; it cannot
qualify Raspberry Pi hardware or prove full-speed emulation on the performance floor.
