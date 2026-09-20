> Current 1.1 release-readiness checkpoint: [CURRENT-STATE](../CURRENT-STATE.md)
> and [CURRENT-STATE](../CURRENT-STATE.md). Start with the [release documentation](README.md),
> [actual build walkthrough](release/build-your-own.md) and [factory explanation](release/factory.md).
> Dated checkpoints below retain historical evidence; they do not override current governance.

# Architecture and ownership

## Decision and precedence

[ADR-0001](adr/0001-base-distribution-and-image-architecture.md), accepted 2026-09-15,
selects Raspberry Pi OS Lite + pinned arm64 pi-gen and bounded appliance practices.
For 1.1 retain writable ext4 and logical system/user-data separation, minimal installed
identity, separately built Debian packages and backup/reflash/validated restore.
No 8 GB minimum: measure footprint and usable user-data capacity. Full black-box
recovery stays in repositories and retained development/release infrastructure.
This decision does not authorize implementation. [Current v1.0 corrections](v1.0-current-notes.md)
explain precedence over historical release/audit statements.

## Current appliance

RC2 source follows firmware → kernel/initramfs → systemd → tty1 getty/login/PAM →
pcbm's profile → Product console session → primary presentation → Bash/dialog Menu
→ shared Cover/VICE launch → Menu. One normal user, `pcbm` UID 1000, owns the local
and SSH/file-management experience. Root remains separate and general administration
requires authenticated sudo. Fixed appliance operations retain narrow helpers.

The canonical library is `/home/pcbm/content`; preferences are
`/home/pcbm/.config/project-cbm/preferences.json`, and VICE preferences remain in
`/home/pcbm/.config/vice`. Account, installed-path and migration details are in the
[account/layout contract](release/accounts-and-layout.md). Runtime and Menu use the
Product registry and pcbm-info authorities; there is one setup/expansion owner and
one supervised terminal lifecycle. No old pcbm-start path competes for startup.

Pi 4-class hardware is the 1.1 floor. RC1 Pi 4 B Cover/VICE/F10/return and the owner
reference performance passed physically; RC2 changes require a new hash-bound test.
Other models/workloads are not qualified by that result. Historical Pi 3 failures
remain evidence. See [hardware](supported-hardware.md) and the
[RC1 owner report](qualification/rc1-attempt9-pi4-owner-report.json).

## Repository contract

| Authority | Owns |
| --- | --- |
| project-cbm | OS integration, image build system, product lock/manifest, VICE/TCPser/Menu mapping, qualification, artifacts, product docs, release notes, supported hardware policy |
| project-cbm-menu | Independently versioned menu scripts/assets, menu interfaces/contracts, packaging and focused tests |

Product docs here are authoritative. Menu public-docs/ is a historical packaging
mirror, not a competing authority. Do not run its unsafe sync helper; migrate
packaging to an explicit pinned docs input during later authorized work.

The product must consume an explicit Menu version/tag, peeled commit and artifact
SHA-256. Product and Menu version numbers need not match. A Menu source release
alone is neither a product release nor proof of hardware qualification.

## Interfaces to preserve and clarify in 1.1

- Menu presents choices and dispatches launch/control helpers; VICE remains the
  emulator and owns emulator interaction. Retain F10 and a reliable console return.
- Product defines installed paths, account/home/content locations, service policy,
  privileged operation boundary and configuration schema. Menu declares required
  binaries, accepted settings, launch arguments, exit/error behavior and dependencies.
- Converge RUN, MACHINES, CONTENT and direct boot on a validated launcher contract.
  This is a planned change, not implemented during preservation.
- Separate immutable defaults from validated user overrides, with atomic writes
  and non-destructive upgrades. Never restore machine identity as user preferences.
- One tested owner for expansion and first boot; do not layer competing PiShrink,
  cloud-init and custom resize flows. Avoid broad root file commands and new network
  services merely for UI convenience.
- Pi 3 performance is a gate. No desktop, web admin, heavyweight catalog, runtime
  containers, SDL3 migration or Pi 5-only optimization is part of the initial POC.

See [build/release contract](build-and-release.md), [testing](testing.md) and
[security](security.md). This document defines boundaries, not new runtime behavior.

## Recovery is a product requirement

The [black-box recovery contract](recovery.md) explains how a stranger recovers
source, inputs, rationale, build environment, release identity and qualification
without original context/infrastructure. Full records, recipes, input closure and
recovery documents stay external. Minimal offline-readable installed identity and
portable retained-input locators are mandatory from 1.1. One lock generates identity;
final image/qualification hashes remain external to avoid circular dependencies. Runtime
identity reporting consumes generated metadata, not another version file. TheBench
is the current bulk deployment, not a required product pathname or platform.

## POC3 initial presentation policy

[POC3 design](build/poc3-design.md) supplies initial VICE per-chip true aspect and
desktop-resolution fullscreen. Fit the complete emulated canvas; accept black
sidebars (pillarboxing) or top/bottom bars rather than stretch-to-fill. VICE owns
PAL/NTSC pixel geometry; CBM does not enforce a universal 4:3 multiplier or legacy
HDMI resolution. Root-owned reference defaults and a pi-owned initial config are
created at image construction only. Normal launches/first boots preserve subsequent
user settings. The existing shared Menu launcher and session/privilege contract stay
unchanged. Generated profiles and software-reference tests are not physical passes.
POC2's recorded Pi 3B success and geometry failure remain immutable evidence.

## Approved component boundaries and first source slice

The owner accepted the appliance audit's pcbm-menu / pcbm-config / pcbm-info /
narrow-privileged-backend separation and retaining Bash + dialog. The
[first implemented slice](runtime/foundation-slice.md) adds read-only info, opt-in UI
contracts and user preference/profile foundations. Broader configuration UI/backends
are not implemented. Existing POC consumers still use their old configuration; later
migration must switch them coherently rather than create competing effective values.
