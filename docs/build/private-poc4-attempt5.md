# POC4 corrective attempt #5: owner handoff

**READY TO FLASH: YES. READY FOR OWNER PHYSICAL TEST.**
One new private engineering image passed construction and complete actual-image offline
validation. New physical Cover/KMS/VT/input and Wi-Fi behavior remain **UNTESTED**.
[Exact source/component/result record](private-poc4-attempt5.json) ·
[hash-bound Pi 3B procedure](../qualification/poc4-attempt5-pi3b-regression.md) ·
[source correction contract](../runtime/cover-network-correction-2026-09-18.md).

## Identity and correction

**Project CBM 1.1.0-poc.4 / private-engineering-poc4, corrective attempt 5.**
This continues POC4 qualification using its established distinct-attempt/lock identity;
Menu and Runtime versions advance independently only because their source changed.
It is not a public release or POC5. Product integration/runtime source:
`9b0220beaf49dca44862a6e9fe874f5e4fa96e8d` on `feature/1.1-build-foundation`.
Menu `v1.1.0_poc4.3`, tag object `38ede9d60c435fefd2ec51e169ee8939ec9cbf0d`, peeled
`664b0a76b798a64d697e0d2d3baa0d45a5406ebd` on `feature/1.1-debian-package`.
Final documentation HEADs are bound by the recovery manifest, separately from frozen
package sources. Owner governance commits `e098244` / `668ff0a` and both AGENTS are
preserved. Worktrees began clean; no unknown work was discarded.

Attempt #4 remains owner-reported Pi 3B lifecycle **PHYSICALLY PASSING**, Cover **FAIL**.
The `/dev/tty` versus literal `/dev/tty1` guard mismatch is a confirmed source defect
and high-confidence explanation of its retained failures. There was no explicit guard
reason to prove the precise physical branch. Attempt #3's precise root cause is not
retrospectively proven. Earlier physical evidence and UNTESTED items remain unchanged.

The actual new image admits Cover by kernel controlling-tty identity, active VT1 and
foreground group; it retains fixed admission/skip/asset-ready diagnostic events.
Product's shared unprivileged launcher, pre-Cover terminal capture, bounded same-group
supervision/termination/reaping, and restoration/readback before and after VICE are
unchanged. Geometry, ALSA and F10/Quit remain intact. The correction cannot yet be
claimed to make Cover physically visible.

`pcbm-info` now owns bounded per-interface type/state, IPv4/IPv6 CIDRs, effective MAC
and safely available active SSID. System Information and the existing Network view
consume that JSON. No Menu probes, active scans, credential queries, service activation
or new top-level item. Existing human-readable first-boot selections, Advanced,
Back/retry/resume, immediate working feedback, Wi-Fi-before-completion, hidden-password
explanation and protected credential handling remain in the image. Actual association
and detailed setup behavior still require owner testing. Quiet/fast boot remain backlog.

## Components and immutable inputs

| Component | Version | Status | Package/input filename | Bytes | SHA-256 |
| --- | --- | --- | --- | ---: | --- |
| menu | 1.1.0~poc4.3-1+pcbm1 | NEW | `project-cbm-menu_1.1.0~poc4.3-1+pcbm1_all.deb` | 1103688 | `849974423c31c42298970650b5ae2eaf4578f87e80da35933785c5c66e233e7a` |
| runtime | 1.1.0~poc4.2-1 | NEW | `project-cbm-runtime_1.1.0~poc4.2-1_all.deb` | 27508 | `10f07910786faeb09a944ab440bbb6ea8243981c9a84174e2d54590fe552377a` |
| tcpser | 1.1.6~beta-1+pcbm1 | REUSED | `project-cbm-tcpser_1.1.6~beta-1+pcbm1_arm64.deb` | 26872 | `8b8f8a4f3ec98dddf5bdb347320dad05e1bbe5230e0ee2727248c247a5af584f` |
| vice | 3.10-1+pcbm3 | REUSED | `project-cbm-vice_3.10-1+pcbm3_arm64.deb` | 4650184 | `c9d798a591c22faa9ffc3141b7f5177ece36a05e53d9d2c8aae1ce93c22fcfbe` |
| sid_wizard | 1.97 | REUSED | `objects/46872e5c937f681fa161a2acf88937040f2b90a091b03d8153513035bd62223e` | 184320 | `46872e5c937f681fa161a2acf88937040f2b90a091b03d8153513035bd62223e` |
| striketerm | 2014 Final | REUSED | `objects/72b803c54c7892857c0ddb5674dabc841d59a496285975546bef689308940595` | 174848 | `72b803c54c7892857c0ddb5674dabc841d59a496285975546bef689308940595` |
| qualification_media | 0.1.0 | REUSED | `qualification-media.tar` | 194560 | `61673c45058ba31d2e28c699c631e99173c4e44b8b49c82c83735c2c5614d0af` |

The exact record includes source repository/ref/artifact and disposition reasons for
every component. Optional software rows are integrated retained payloads, not invented
Debian packages; their content-addressed filenames are relative to the new frozen kit.
Only Runtime and Menu were rebuilt. VICE/TCPser, base/host closures, pinned pi-gen and
patches, qualification media and optional payloads remain exact. All seven artwork
files preserve their hashes (1,180,157 bytes total) and registry mapping/readability.
StrikeTerm remains **PRIVATE-ENGINEERING-ADMITTED / PUBLIC-RELEASE-RIGHTS-GATE-PENDING**;
SID-Wizard retains its reviewed 1.97 core contract. No new third-party payloads or rights
decisions. Cover constituent rights remain separate from private testing.

Lock: `inputs/frozen-poc4-attempt5/release-lock.json`, **schema 4**,
SHA-256 `4568aa184063aa7e3a0ae5217a98320f68735665f5e08340d48368530c88968e`. All **2,894 objects** verify.
Pinned pi-gen: `6fcca44892d5d4b36f826d2b8fb16d716369fada`.
Configured bulk storage: `/Volumes/TheBench/ProjectCBM-Work`.

- Raw: `artifacts/private-poc4-attempt-5/2026-09-18-project-cbm-1.1.0-poc.4-lite-private-poc.img`; **3087007744 bytes**;
  SHA-256 `5385acc822d7f280dd2eb5654368ef282ed941d4dc946368871510d98c752e66`.
- XZ: `artifacts/private-poc4-attempt-5/image_2026-09-18-project-cbm-1.1.0-poc.4-lite-private-poc.img.xz`; **597605380 bytes**;
  SHA-256 `3923c319e485bbccad642b8a8b8039fc8acd0694a308ec631aeeffa64ed3e567`.
- Decompression reproduces raw exactly in the guest and retained external copy.
  Read-only inspection leaves the raw hash unchanged.

## Tests and actual-image checks

| Validation | Result |
| --- | --- |
| Product host | **162/163 PASS**, known contextual macOS mktemp expectation FAIL |
| Menu host | **76/76 PASS** |
| Native Linux Product / Menu | **163/163 / 76/76 PASS** |
| Focused network collector | **7/7 PASS** |
| Installed lifecycle | **9/9 PASS**, including timeout/failure-open/termination/reaping and PTY restoration |
| Native installed Covers | All seven decode/present/release with SDL dummy backend; three renderer/VICE-fixture cycles PASS |
| Real Linux tty alias | Direct descriptor and `/dev/tty` resolve to same kernel tty; PTY rejected; active VT positive case is a mocked fixture |
| Native networking | Installed ip/nmcli syntax/parsers and synthetic-interface IPv4/IPv6/MAC PASS; no physical Wi-Fi claim |
| Actual-image contracts | **220/220 PASS**: 121 main + 20 supplemental + 79 correction |
| FAT/ext4 integrity, systemd units | PASS, read-only, no repair |
| ELF dependency closure | **127 objects**, no missing dependency |
| Installed identities | **672 packages** matched to 709 frozen descriptors |
| Host inventory/update masks | Before/after PASS, **no drift** |

The known macOS failure is not relabeled a pass; native Linux validates the actual
appliance behavior. The prior 154/155 source-correction and 155/156 attempt-4 results
remain accurately preserved. New fixtures cover alias/foreign tty/active VT/foreground
admission, fixed skip diagnostics, malformed/partial data, address/MAC/SSID handling and
legacy UI compatibility. No physical behavior is inferred from fixture/headless tests.

Native package install, dpkg/APT closure, AppArmor reconfiguration, narrow sudo policy,
first-boot locale/keyboard/timezone choices, owner authentication, Back/retry/resume backend
state, service controls, NetworkManager credential redaction, USB-import loop fixture,
Midnight Commander PTY launch/F10 return and mixer availability passed. Hardware USB,
ALSA controls, radio and actual applications remain owner qualification items.

Staging used a separate guest-ext4 OverlayFS upper over the exact read-only attempt-4
image, avoiding another full copy or deletion of older state. This is only the test
root; pi-gen constructed a fresh image from frozen inputs. An initial harness copied
source into `/tmp` before namespace init mounted its private `/tmp`; placing it inside
the live namespace fixed that test preparation. Shutdown completed before the wrapper
stopped an already-removed transient unit; remaining mounts were explicitly detached
and the old image rehashed. Initial/final logs remain retained. No product/security gate
was weakened. Disposable roots, generated credential stores and journals are not exported.

Actual-image checks cover boot/root filesystems, lock-derived identity, exact component
payloads, dependencies, units/service readiness, first boot/owner administration, SSH
defaults, NetworkManager, privilege policy, Menu/Runtime/VICE/TCPser, Cover mapping and
renderer, persistent admission/lifecycle/terminal diagnostics, POC3 geometry, ALSA/F10,
qualification media, storage/import/configuration/status, optional software/rights
metadata and absence of unexpected secrets, machine identity or builder residue.

## Footprint and build host

| Before first-boot expansion | Bytes |
| --- | ---: |
| Raw image | 3087007744 |
| Root filesystem capacity | 2430955520 |
| Root used | 1651560448 |
| Root free including reserve | 779395072 |
| Available to ordinary users | 635531264 |

No minimum card size is inferred. Actual expanded capacity and maintenance margin need
owner measurement. One controlled build finished in **174.81 seconds**, exit 0; maximum
individual-process RSS 491,680 KiB. The existing Lima/VZ native arm64 Debian 13 factory,
security verification, frozen transport and builder/chroot separation were preserved.
Host package inventory SHA-256 `352fb0f9ed6503e7570278573c8a04219856d8bde086c66e173c7d51c6dd0aa6`
agrees byte-for-byte before and after. Guest available bytes: 43312812032
before, 33800679424 after. No build processes/mounts/loops
remain; builder stopped. Future builds must recheck headroom; this result is not an
ongoing capacity guarantee. External capacity remained sufficient throughout.

## Recovery and owner action

Checkpoint: `archive/poc4-attempt5-2026-09-18`. Its manifest/restore report binds final
Project/Menu refs, full bundles, exact offline refs/peeled tags/symbolic HEAD and fsck,
frozen lock, package/input inventories, validation, artifact hashes and this procedure.
The manifest checksum is separate under the acyclic recovery contract. Images are
referenced, not duplicated into recovery. Evidence: `qualification/poc4-attempt5-2026-09-18`.
Earlier candidates, failed attempts, locks/packages/images, physical reports/photos,
card evidence and checkpoints verify unchanged; original historical preservation also
passes all 1,677 entries. Both AGENTS remain byte-identical to the owner commits.
TheBench is not independent encrypted custody; that and reproducibility remain open.

**ONE next owner action: FLASH THE EXACT NEW IMAGE AND PERFORM THE HASH-BOUND PI 3B
PHYSICAL REGRESSION PROCEDURE.** First verify Menu/VT, visible Cover, VICE/F10/Quit,
immediate Menu input and VT return for three cycles. Preserve diagnostics before reboot
or unrelated tests if a priority failure appears. Then test setup/Wi-Fi/network information,
media/audio/input, SID-Wizard, StrikeTerm, mc/mixer, USB, Samba, SSH, TCPser/mDNS and
persistence. No physical testing, push or publication was performed. Stop for owner review.
