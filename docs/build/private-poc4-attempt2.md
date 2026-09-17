# POC4 attempt #2: controlled build and offline validation

Project CBM **1.1.0-poc.4**, private engineering candidate, build attempt **2**, is
built and offline-validated. **Physical behavior remains UNTESTED.** POC3 remains the
physically demonstrated Pi 3B foundation. No Pi test, push, publication, POC5 or boot
optimization occurred. The builder is stopped.

Read the [exact machine-readable report](private-poc4-attempt2.json),
[environment boundary](environment-boundary.md),
[first-boot/runtime design and earlier staging evidence](runtime-activation.md), and
[exact-hash Pi 3B procedure](../qualification/poc4-attempt2-pi3b-smoke-test.md).

## Failure confirmed and bounded correction

Attempt #1 remains [immutable failed evidence](poc4-blocked.md), not a superseded
image. Its exported TMPDIR pointed into the build host; pi-gen's `capsh --chroot`
inherited it. AppArmor 4.1.0-1's postinst called `mktemp` while generating a home-directory
tunable and failed because that path did not exist inside the target.

A NEW disposable copy reproduced both mktemp and actual `dpkg --configure apparmor`
failure. The patched chroot then passed, without AppArmor changes: fixed environment,
1777 `/tmp`, 5,211,652,096 bytes initially free in its staging tmpfs, mktemp, AppArmor,
dpkg audit and APT dependency checks. This confirms the environmental cause, not a
reason to weaken AppArmor or ignore package errors.

Factory entry, frozen transport and pi-gen now start with known values. Retained
pi-gen patch sanitizes debootstrap and on_chroot; CBM's direct chroot has the same
explicit target environment. Host stage/config variables remain available where
needed. Temporary directories, identity/PATH, XDG, locales, proxies, Python/Git,
CBM paths and shell/loader injection variables are covered by the documented policy.
Ambient secrets/environment dumps are not retained.

## Native and static revalidation

- **142 product tests**, **50 Menu tests**, shared launcher checker: PASS.
- Exact unchanged runtime/Menu packages reinstalled; dependency/API checks, dpkg
  configuration/audit/verification, APT check, AppArmor reconfiguration, sudoers: PASS.
- First-boot sequence/offline completion and completed-setup reset refusal; real
  owner PAM/password + authenticated sudo; Terminal wrong/right authentication,
  returning shell and authenticated vendor raspi-config invocation: PASS in Linux.
- Narrow helper rejects arbitrary command/arguments; actual Samba credential store,
  fresh SSH keys, SSH/Samba/TCPser/mDNS start/stop; loopback modem listener: PASS.
- NetworkManager parses private keyfile and round-trips synthetic credentials in
  memory; absent-radio connection fails; forget/offline and credential exclusion from
  installed pcbm-info: PASS. No real Wi-Fi/Ethernet or external service client tested.
- Synthetic read-only USB media: 2 files / 56 bytes copied as pi, symlink/root-only
  directory skipped, retry copied zero, clean unmount, source hash unchanged. Production
  USB discovery was not replaced; the isolated test substituted discovery explicitly.
- Native SID-Wizard deterministic preparation/install, template/working ownership and
  refusal to overwrite existing user state; exact private StrikeTerm admission: PASS.
- First-boot/menu/config/boot payload checks and fixture tests remain distinct from
  physical console, root-growth interruption, service connectivity or C64 application
  execution. Prior loop-growth evidence remains unchanged; no new Pi pass is implied.

Harness corrections: fresh namespace `/run` omitted directories supplied by the real
image's tmpfiles rule; they were initialized with the exact declared modes before
rerun. nmcli's escaped output was disabled for an in-memory comparison. Supplemental
About validation initially assumed an executable/path that does not exist: About is
in pcbm-config plus its installed libexec bridge. Final check uses that implementation.
These were test preparation/assertion corrections; no runtime package/image repair.
Initial result records remain retained alongside the passing records.

## Inputs and isolation

Integration source: `93d264adf3bac6a397112ecd7349ab8105257852`.
Pinned pi-gen: `6fcca44892d5d4b36f826d2b8fb16d716369fada`.
Lock: `inputs/frozen-poc4-attempt2/release-lock.json`, SHA-256:
`27f0e8ca522f745e240d088fc8fe8feab8f98c15eb165d72fad1a9ef18ee3fdf`.

All component package/source identities, base/host closures, defaults, first-boot
payload, qualification media and optional inputs match attempt #1. Changed lock fields:
integration commit/source; sealing-recipe descriptor; appended pi-gen environment patch.
Consequently complete inputs and embedded integration/lock identity are **not identical**.
No component rebuild or Menu retag was needed. Menu stays `v1.1.0_poc4`, peeled
`bb8a66ea9da994b30f978ad87d61c9aedb03dad6`.

| Package | Version / architecture | SHA-256 |
| --- | --- | --- |
| project-cbm-menu | 1.1.0~poc4-1+pcbm1 / all | `b1c95d128eb0f9b3d9ba59528ed7be39d7f94cf158933bd74c83f0eecb83999d` |
| project-cbm-runtime | 1.1.0~poc4-1 / all | `fffbc2bd6b07b800e2562c8fc89a523e7e08df6bf0f7ce76786f9efebde9d303` |
| project-cbm-tcpser | 1.1.6~beta-1+pcbm1 / arm64 | `8b8f8a4f3ec98dddf5bdb347320dad05e1bbe5230e0ee2727248c247a5af584f` |
| project-cbm-vice | 3.10-1+pcbm3 / arm64 | `c9d798a591c22faa9ffc3141b7f5177ece36a05e53d9d2c8aae1ce93c22fcfbe` |

Construction ran once in an isolated network namespace using only frozen transport.
Existing build/output directories are not reused. Before/after exact builder package
inventory and masked automatic-update guard: PASS, unchanged. Kernel
`6.12.107+deb13-cloud-arm64`, aarch64. No builder packages were installed/updated.
Build wall time 166.47 seconds, maximum individual-process RSS 489,572 KiB, no swap;
this is not aggregate VM peak memory. Original 8-vCPU/10-GiB/160-GiB allocation remains.

Nonfatal upstream notices: APT could not open a pseudo-terminal for its terminal log
in CBM's direct chroot; package commands completed successfully. apt-listchanges could
not obtain three GCC changelogs from the frozen transport. No package verification,
maintainer-script failure or AppArmor check was bypassed. The complete logs are retained.

## Output and read-only validation

| Artifact | Bytes | SHA-256 |
| --- | --- | --- |
| Raw | 3087007744 | `e7c0b971ff3c12c09483477f760a09718a038143384774a7d43eca4a790aa217` |
| XZ | 597702372 | `0ced0321d84777a0e65ac4ebbf4bbae7c42f5680ceba37dc16a5820e5ec50bdf` |

External paths: `artifacts/private-poc4-attempt-2/2026-09-16-project-cbm-1.1.0-poc.4-lite-private-poc.img` and `artifacts/private-poc4-attempt-2/image_2026-09-16-project-cbm-1.1.0-poc.4-lite-private-poc.img.xz` under configured bulk
storage. The raw retained image and XZ-decompressed stream have identical hashes;
external copies rehash correctly. Raw hash remains unchanged after all inspections.

**121 main + 20 supplemental offline checks PASS**, FAT/ext4 read-only integrity PASS,
systemd units PASS, **113 ELF objects**, no missing graphics/VICE dependencies. These
cover identity/lock agreement, uninitialized machine-id, no SSH keys/credentials/build
residue, first-boot incomplete state, locked owner account/authenticated sudo, exact
narrow helpers, info/config/About, registry/preferences, session/geometry/F10/diagnostics,
NetworkManager offline initial state, optional-service policy, content ownership/import,
application hashes/working copies and unchanged original qualification media.

| Before root expansion | Bytes |
| --- | ---: |
| Root filesystem capacity | 2430955520 |
| Root used | 1650298880 |
| Root free including reserved blocks | 780656640 |
| Root available to ordinary user | 636792832 |
| Installed package-size sum (672 packages) | 1597359104 |
| SID-Wizard system template/notice/manifest | 179423 |
| StrikeTerm system template/admission record | 175967 |
| Both fresh user working disks | 349696 |

FAT partition: 536,870,912 bytes; ext4 partition: 2,541,748,224 bytes. No arbitrary
minimum card size follows. Post-expansion user capacity and maintenance/initialization
margin require actual media and first-boot qualification. Runtime remains lean; source,
package closure, logs and recovery kits stay outside the appliance.

## Optional content and remaining gates

SID-Wizard **1.97** uses only the reviewed original native SID-Wizard/SID-Maker subset.
Source archive SHA-256 `aeb265f4a778b2acb5aad13e8e98af882888292f749f29f4d18cbf49850e57bc`;
deterministic D64 `cec93ae1fd5fc846507c1883fd9cb210c6a3c0f40c1c081964e3b8450e26dc44`.
Template in `/usr/share/project-cbm/applications/sid-wizard/`; user working disk in
`/home/pi/pcbm/music/Creation/SID-Wizard/`. Accepted license notice retained; no excluded
music/assets/host apps/manual added. C64 execution/save behavior still needs Pi testing.

StrikeTerm **2014 Final**, Alwyz, author-endorsed CSDb artifact
`https://csdb.dk/getinternalfile.php/129890/st2014final.d64`, 174,848 bytes, SHA-256
`72b803c54c7892857c0ddb5674dabc841d59a496285975546bef689308940595`, matches the recorded
Combian copy. Working disk: `/home/pi/pcbm/programs/Communications/StrikeTerm/`.
**PRIVATE-ENGINEERING-ADMITTED / PUBLIC-RELEASE-RIGHTS-GATE-PENDING** remains explicit;
public-purpose rights checking fails closed. This build/any future physical pass does
not establish public redistribution permission.

Requested third-party SID/demo references remain **OWNER-SUPPLIED, NOT BUNDLED**.
Generic `.sid` autostart is refused; PSID/RSID playback remains a separate product gate.
Original Project CBM qualification media are unchanged.

One successful controlled build does not prove reproducibility. Independent clean
rebuild, filesystem/partition identifiers, package-generated caches, timestamps and
compression/tool behavior still need comparison. Pi first boot/interruptions, owner UI,
real display/audio/input, USB hardware discovery, networking/external services and
optional applications remain **UNTESTED** for this candidate. Boot optimization remains
out of scope until successful physical validation (unless a more important blocker).

## Preservation and handoff

POC1/2 baseline: 5,503 entries verified; POC3 exact lock/raw/XZ and 2,789 retained objects
verified. Attempt #1 checkpoint's 23 files and 2,834 retained files reverified unchanged;
old frozen kit has 2,809 objects. New kit's 2,812 objects rehash correctly. No historical
qualification record/tag changed. Failed tree/checkpoint retained, not repaired.

New evidence: `qualification/poc4-attempt2-2026-09-16`; new recovery checkpoint:
`archive/poc4-attempt2-2026-09-16`. The checkpoint manifest records final source refs,
both bundles, hashes and exact offline restoration results; no disposable credential
stores or extra image copies are placed in that checkpoint. Independent backup/custody
remains unresolved outside the Mac/TheBench failure domain.

**Next owner action:** review this result, then use only the
[exact attempt #2 Pi 3B procedure](../qualification/poc4-attempt2-pi3b-smoke-test.md).
Stop at the first failure, retain diagnostics, and report PASS/FAIL/UNTESTED honestly.
No further candidate/build/hardware test or publication is automatic.
