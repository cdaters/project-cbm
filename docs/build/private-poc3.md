# Private POC3: geometry candidate ready for Pi 3B review

Completed 2026-09-16. **Built and offline-validated; physical POC3 is UNTESTED.**
This is a private engineering candidate, not a public release or proof of independent
reproducibility. The builder is stopped. Next: owner review, then the bounded
[Pi 3B procedure](../qualification/poc3-pi3b-smoke-test.md). Do not test other models,
build POC4, enable SSH or expand the settings redesign under this authorization.

## What changed and why

POC2 physically passed the core Pi 3B launch/rendering/audio/media/return/VT/reboot
checks but stretched the C64 image horizontally. Its exact result and photographs
remain in [the immutable record](../qualification/poc2-pi3b.json). The photo manifest
is `qualification/poc2-pi3b-photos-2026-09-16/evidence.json`, SHA-256
`00d9028d621441a5f18b990835c7d51008c7108d3a30c3f7867f16ece516b05d`.

[Presentation findings and policy](poc3-design.md) distinguish source defaults,
software reference observations and missing physical measurements. POC2 already
compiled true aspect mode 2; adding that setting alone is not an established fix.
The leading hypothesis remains windowed KMS mode choice plus downstream scaling.
Neither the active POC2 connector timing nor the monitor's scaler was measured.

POC3 initializes each applicable VICII, VDC, VIC, TED and Crtc chip with
`AspectMode=2`, `Fullscreen=1`, `FullscreenMode=0`. VICE supplies PAL/NTSC and
machine-specific geometry. Fullscreen uses the desktop mode; no universal 4:3,
forced legacy HDMI mode, custom pixel multiplier or crop-to-fill. Unused screen
area is expected: **pillarboxing** means side bars; **letterboxing** means top/bottom bars.

The root-owned reference is `/usr/share/project-cbm/vice-defaults.ini`; initial
pi-owned settings are `/home/pi/.config/vice/sdl-vicerc`. Construction creates the
user file exclusively if absent. Normal launch/boot does not overwrite it, and no
geometry CLI argument overrides saved user preferences. VICE's Save settings is
still required for preferences that should persist. Protected build defaults are
not a runtime prohibition on user adjustments.

VICE package revision 3 adds opt-in, three-record presentation telemetry and a
read-only non-root libdrm mode reporter. Existing bounded launch logs/snapshots
capture driver, renderer, aspect/standard/fullscreen, logical/output/window sizes,
viewport/scale and active connector timing where available. No monitor serial,
EDID, new privilege, arbitrary command interface or SSH. Four launch directories
and a 128 KiB stdout tail remain the limits. See the procedure before rotation
replaces primary geometry evidence.

POC2's getty/login/PAM tty1 and tty2, shared unprivileged Menu launcher, SDL audio,
F10 → VICE menu → Quit → Menu, first-boot ownership, graphics runtime dependencies,
service masks, exact power-only sudo grants and qualification media are unchanged.
Menu and TCPser package bytes are reused unchanged. Other machine configurations
are generated/reference-tested, not physically qualified.

## Frozen identities and artifacts

All external paths below are relative to configured bulk storage, currently
`/Volumes/TheBench/ProjectCBM-Work`. Full machine-readable results are in
[private-poc3.json](private-poc3.json).

- Candidate: **1.1.0-poc.3 / private-engineering-poc3**.
- Integration: `0a0e271d86c68a969d8b18189c561ed51a8b0e09`.
- Lock: `inputs/frozen-poc3-final/release-lock.json`, SHA-256
  `3f3180f50e5c990ad63fc3d564a56bbd86b80f9b38c6a4aff7b42ed9438b9f5e`.
- pi-gen arm64: `6fcca44892d5d4b36f826d2b8fb16d716369fada`.
- Raw: `artifacts/private-poc3/2026-09-16-project-cbm-1.1.0-poc.3-lite-private-poc.img`,
  **3,095,396,352 bytes**, SHA-256
  `9a8b1e0465c93981dfa6b09772e9e3fbf5c487a915bba0046b5de034f9331f33`.
- XZ: `artifacts/private-poc3/image_2026-09-16-project-cbm-1.1.0-poc.3-lite-private-poc.img.xz`,
  **596,947,568 bytes**, SHA-256
  `e7d9657bfbb1124b38c2f1f3479698e24a34be7234db80d766f189da946ace3c`.

| Package | Version / architecture | SHA-256 |
| --- | --- | --- |
| project-cbm-vice | 3.10-1+pcbm3 / arm64 | `c9d798a591c22faa9ffc3141b7f5177ece36a05e53d9d2c8aae1ce93c22fcfbe` |
| project-cbm-menu | 1.1.0~poc2-1+pcbm1 / all | `e29bc3598f3be0869f79184250f88a03f4c59f1304a20a428223bac58c97bd11` |
| project-cbm-tcpser | 1.1.6~beta-1+pcbm1 / arm64 | `8b8f8a4f3ec98dddf5bdb347320dad05e1bbe5230e0ee2727248c247a5af584f` |

Menu input stays `v1.1.0_poc2`, peeled
`897cee7c792b11bfed80168a576f263340f5f57d`. VICE source remains 3.10,
SHA-256 `8e5bac18cbcb9f192380ad3ef881f8790f5b75c41d7b3da65d831985d864d6d1`.
MIT qualification media source remains `14e4ade77ec83e0429d194a6b5ecfa5ef7655e75`,
bundle SHA-256 `61673c45058ba31d2e28c699c631e99173c4e44b8b49c82c83735c2c5614d0af`.
Individual media hashes/source/license/expected behavior remain in the JSON record.
No PSID/RSID/fidelity/stereo or POC3 physical pass is inferred from their reuse.

## Validation and evidence limits

- **40 tests passed on both macOS and native Debian**, without skips. Existing
  shared Menu Bash launcher regression tests passed. Configuration ownership,
  all chip resources, diagnostics, locks, service/sudo restrictions and host-drift
  negatives are included. Tests do not claim physical display behavior.
- **12 native software-reference cases** cover 11 profiles plus x64sc PAL/NTSC;
  actual config/resources, fullscreen and bounded telemetry passed. Saved preferences
  remained intact and CLI precedence was verified. SDL dummy desktop 1024×768 is
  not physical KMS. Separate unmodified-POC2 1280×720 window observations preserve
  different PAL/NTSC logical geometry; this narrows, but does not prove, the cause.
- **85 offline image checks passed**, plus read-only ext4/FAT, systemd unit checks
  and **113 ELF objects with no missing dependencies**. Initial defaults/ownership,
  installed identity, media, GL runtime, no SSH, exact power-only sudo, and no
  obvious builder identity/source/cache/toolchain residue passed.
- **2,789 retained input objects rehashed**, schema/transitive catalogs and Debian
  metadata verified. Transferred raw/XZ hashes agree with the guest; decompressing
  XZ reproduces the raw hash. No post-build image mutation occurred.
- **5,503 POC1/POC2 baseline files remain unchanged**, including frozen images,
  locks, packages and physical records. Original historical 1,677-entry manifest
  and pre-existing Git tags remain unchanged. Photos remain external.

Preliminary reference attempts with an incomplete data search path and a reused
source tree failed; only the later clean package/reference run counts. A concurrent
reference attempt collided with source cleanup and was rerun sequentially. Their
logs are retained; none is called a successful qualification.

## Builder drift and accepted attempt

Inherited unattended upgrades changed 13 builder package versions and added one
kernel during engineering work. The first assembly used a stale host inventory and
was **rejected before candidate acceptance**. Its original lock `d7f801ef…`, XZ and
log remain under `inputs/frozen-poc3`, `artifacts/poc3-unaccepted-host-drift` and
`qualification/poc3/unaccepted-construction.log`. Do not flash that attempt.

The final lock includes exact changed binaries, corresponding sources, authenticated
APT metadata and the current inventory. Automatic update units are masked only in
the disposable builder during controlled work; new before/after guards reject any
inventory drift or enabled automatic updates. This is not appliance service policy.
See [the design's correction record](poc3-design.md#host-drift-discovered-and-corrected-before-candidate-acceptance).
Running build kernel was 6.12.95+deb13-cloud-arm64; installed 6.12.107 was not booted.
Final VICE packaging began after those updates completed. Deliberate host maintenance
must refresh the retained closure/lock; masking is not permission to neglect security.

## Footprint and reproducibility

Raw partitions: 536,870,912-byte FAT boot and 2,550,136,832-byte ext4 root. Root
filesystem capacity is 2,439,266,304 bytes; used 1,652,477,952; free 786,788,352;
available to ordinary user 642,506,752 before first boot/expansion. Boot used
78,420,992 bytes. 671 installed packages total 1,597,225,984 declared installed bytes.
Component sizes: VICE 41,705,472; Menu 105,472; TCPser 79,872 bytes. These package
figures are not filesystem usage or all product-owned configuration. Identity: 1,443 bytes.

Post-expansion user capacity and maintenance safety margin remain UNMEASURED. No
minimum card size is established. No fixed 8 GB requirement. The factory completed
in 2:50.84 wall time with 506,008 KiB maximum reported child RSS; that is not total
VM memory/CPU usage or a performance budget. Detailed construction log is retained.

This is a controlled build, **not independently proven reproducibility**. Filesystem
identifiers, filesystem/build timestamps, initramfs generation and package/build
metadata remain potential nondeterminism. No clean independent repeat was performed;
the rejected attempt is not a valid same-input reproducibility comparison.

## Continuity and exact next action

- `inputs/frozen-poc3-final`: authoritative lock and content-addressed input closure.
- `inputs/poc3-host-supplement`: exact host-change acquisition inputs/evidence.
- `packages/poc3`: VICE Debian binary/source/buildinfo/changes/logs; the frozen kit
  remains authoritative if operator-friendly copies are ambiguous.
- `qualification/poc3`: software references, tests, construction/validation logs,
  preservation checks, storage and transfer/hash evidence.
- `archive/milestone1-private-poc3-2026-09-16`: final source bundles, exact refs,
  offline restoration checks and checkpoint manifest. The input-integration commit
  remains fixed even though later documentation commits describe its outputs.

VM data stays on TheBench. VM stopped after export/validation. Virtual disk is
171,798,691,840 bytes; allocated sparse blocks total 73,304,137,728 bytes. Guest free
space at completion: 89,166,381,056 bytes. Host internal free space before/after:
81,376,993,280 / 79,207,886,848 bytes; TheBench: 1,065,318,817,792 /
1,038,084,800,512 bytes. These are observations, not attribution of every host-space
change to this build; configured VM/cache/artifacts remain external. Independent encrypted
backup/custody, public signing, standard SBOM choice, measured acceptance budgets,
historical closure gaps and independent rebuild remain unresolved.

**Next owner action:** review this candidate, then flash only the exact accepted XZ
and perform [the Pi 3B geometry/regression procedure](../qualification/poc3-pi3b-smoke-test.md).
All entries in [the planned physical matrix](../qualification/poc3-pi3b.json) are
UNTESTED. If geometry fails, collect persistent diagnostics/photos and stop without
repairing the running system. No broad modernization or additional-model test follows.
