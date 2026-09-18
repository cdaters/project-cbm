# POC4 corrective attempt #4: owner handoff

**READY TO FLASH: YES. READY FOR OWNER PHYSICAL TEST.**
One private engineering image passed construction and complete offline validation.
Physical Cover visibility, keyboard/VT recovery, actual VICE behavior and Wi-Fi
association remain **UNTESTED**. Neither attempt-3 physical root cause is proven.
[Exact result and source/input mapping](private-poc4-attempt4.json) •
[hash-bound Pi 3B procedure](../qualification/poc4-attempt4-pi3b-regression.md).

## Identity and version rationale

Product **1.1.0-poc.4 / private-engineering-poc4, corrective attempt 4** continues the
same lifecycle/setup milestone. Existing attempts 2/3 and the [recovery contract](../recovery.md)
use a distinct attempt and lock-derived build ID when inputs change; no POC5 scope is
introduced. Menu evolves independently: `v1.1.0_poc4.2`, tag object
`d670e0436fe8b01f9b52416fe661baa97670cd0c`, peeled `171e67b3de181074245fb2bdc70cb60af5688b8e`.
Product integration/runtime source is `f5511e10154e6db93f472716e9ddefd04abadb26` on
`feature/1.1-build-foundation`; Menu is on `feature/1.1-debian-package`.
Final documentation HEADs are recorded by the external recovery manifest, separately
from frozen integration and package-source commits. No push/publication.

Both worktrees began clean. Actual owner-scope commits were Product `59c36d1` and
Menu `aeb4350`; the supplied `deb4350` spelling differs from the actual Menu commit.
Their top scopes agree. Both AGENTS files and commits remain unchanged. Accepted
source checkpoint `archive/poc4-run2-source-correction-2026-09-17-verified` reverified
all 73 files and source bytes, manifest SHA-256
`b79f26c9649e24c4532d1e1545f15e0a142b9ad183c2eab903740187b3744ed3`.

## Components

| Component | Version | Status | Package/input filename | Bytes | SHA-256 |
| --- | --- | --- | --- | ---: | --- |
| menu | 1.1.0~poc4.2-1+pcbm1 | NEW | `project-cbm-menu_1.1.0~poc4.2-1+pcbm1_all.deb` | 1102572 | `15f7d10c37fd67195941d56e1067bb87a45bb5aed1adcc0dbd2dc35e978bf5ac` |
| runtime | 1.1.0~poc4.1-1 | NEW | `project-cbm-runtime_1.1.0~poc4.1-1_all.deb` | 25708 | `0803ff827b7fa9f688858b2ee0ed6758e640ad37942588a58de327a55f55d56c` |
| tcpser | 1.1.6~beta-1+pcbm1 | REUSED | `project-cbm-tcpser_1.1.6~beta-1+pcbm1_arm64.deb` | 26872 | `8b8f8a4f3ec98dddf5bdb347320dad05e1bbe5230e0ee2727248c247a5af584f` |
| vice | 3.10-1+pcbm3 | REUSED | `project-cbm-vice_3.10-1+pcbm3_arm64.deb` | 4650184 | `c9d798a591c22faa9ffc3141b7f5177ece36a05e53d9d2c8aae1ce93c22fcfbe` |
| sid_wizard | 1.97 | REUSED | `objects/46872e5c937f681fa161a2acf88937040f2b90a091b03d8153513035bd62223e` | 184320 | `46872e5c937f681fa161a2acf88937040f2b90a091b03d8153513035bd62223e` |
| striketerm | 2014 Final | REUSED | `objects/72b803c54c7892857c0ddb5674dabc841d59a496285975546bef689308940595` | 174848 | `72b803c54c7892857c0ddb5674dabc841d59a496285975546bef689308940595` |
| qualification_media | 0.1.0 | REUSED | `qualification-media.tar` | 194560 | `61673c45058ba31d2e28c699c631e99173c4e44b8b49c82c83735c2c5614d0af` |

Optional software is integrated from the listed retained payloads, not represented as
invented Debian packages. Content-addressed filenames are relative to the new kit.
Only Runtime and Menu needed new package bytes for accepted source changes. VICE,
TCPser, media and optional source/recipe/artifact mappings remain exactly equal to
attempt 3 and pass native metadata/API/media/rights verification. Source repository,
ref, source hash and reason per component are in the exact result and lock. All seven
Cover assets remain unchanged, totaling 1,180,157 bytes, readable by the unprivileged
renderer. StrikeTerm remains **PRIVATE-ENGINEERING-ADMITTED /
PUBLIC-RELEASE-RIGHTS-GATE-PENDING**. Constituent Cover public rights remain separate.
No reference SID/demo payloads were acquired; PSID/RSID playback remains outside scope.

## Frozen inputs and artifacts

All locators are relative to configured bulk storage, currently
`/Volumes/TheBench/ProjectCBM-Work`.

- Lock: `inputs/frozen-poc4-attempt4/release-lock.json`, **schema 4**.
  SHA-256 `b3430b626d5156c582f4e3e457d47916a16b527c3dcf7586a90cae96c3882b72`.
- Frozen integration: `f5511e10154e6db93f472716e9ddefd04abadb26`.
- Pinned pi-gen: `6fcca44892d5d4b36f826d2b8fb16d716369fada`.
- 2,872 retained content objects verify; native transitive catalog/package/API checks
  pass. Unchanged base/host closures, pi-gen patches, configuration/rights/media inputs
  remain exact. New configuration changes only image date; defaults are unchanged.
- Raw: `artifacts/private-poc4-attempt-4/2026-09-17-project-cbm-1.1.0-poc.4-lite-private-poc.img`, **3087007744 bytes**.
  SHA-256 `f699595fdd31a7f8125bb1882ce8d468ce7dd1b4734d85986b1962e992875b21`.
- XZ: `artifacts/private-poc4-attempt-4/image_2026-09-17-project-cbm-1.1.0-poc.4-lite-private-poc.img.xz`, **597616864 bytes**.
  SHA-256 `076a42911faa24bc4f2d4c225c92d621498261b630e63de35b6c7dc8af0760e2`.
- XZ decompression reproduces raw exactly in the guest and after external transfer;
  raw hash is unchanged by read-only inspection. No historical artifact was overwritten.

One invocation of the established isolated-network Lima/VZ native arm64 Debian 13
factory completed in **182.81 seconds**, exit 0, maximum individual-process RSS
508,908 KiB. AppArmor 4.1.0-1 configured successfully. Security/package gates were not
weakened. Existing nonfatal upstream pseudo-terminal/changelog notices remain distinct
from package errors. The build starts from frozen inputs, never from the test root.

## Validation

| Scope | Result |
| --- | --- |
| Initial Product macOS host suite | 154/155 PASS; known context-dependent `test_mktemp_regression` expectation FAIL |
| Final Product macOS suite, including new integrity-negative test | 155/156 PASS; same single known failure |
| Menu host suite | 70/70 PASS |
| Native Linux Product / Menu source suites | 156/156 and 70/70 PASS |
| Installed focused lifecycle | 9/9 PASS, including real PTY three-cycle restoration, timeout/signals/reaping/failure-open |
| Installed SDL | All seven real Covers decode/present/release under dummy video; three real-renderer/VICE-fixture cycles PASS |
| Native package, account, setup, privilege, services and import | PASS within isolated namespace/hardware limits |
| Actual image | 121 main + 20 supplemental + 65 corrective = **206 PASS** |
| FAT/ext4 / systemd / ELF closure | PASS; no repair; 127 ELF objects, no missing dependencies |
| Installed package identity | All 672 versions/architectures match 709 retained descriptors; component payload verification PASS |

The known macOS failure is preserved, not relabeled as a pass. Native Linux validates
its actual mktemp behavior successfully. No product change was made for that host test.
One new negative test rejects missing/stale/symlinked corrective payloads. Bash syntax,
Python parsing, added JSON, local links, diff/size/secret review are checked at handoff;
ShellCheck is unavailable. Native harness corrections were ordinary fixture preparation:
expect `pending` before Wi-Fi prerequisites, and transfer its test into the active
namespace's private `/tmp`. Initial logs remain retained; no product gate was relaxed.
The isolated init was explicitly asked to exit cleanly after tests, result success.

Actual installed image checks cover lock-generated identity, first-boot incompletion,
owner/admin/privilege boundaries, service defaults/readiness, SSH off, NetworkManager,
Menu/Runtime/VICE/TCPser, storage/import/configuration/status, optional applications and
rights notices, all Covers/mappings/renderer, diagnostic source bytes, POC3 geometry,
ALSA/F10 and original qualification media. Sealing checks find no reusable credentials,
host keys, machine identity or builder residue. Package installation and actual native
AppArmor/dpkg/APT/sudoers checks pass; no generic root execution was introduced.

The actual image contains pre-Cover terminal capture; same-group bounded Cover
supervision/TERM/KILL/reap; independent restoration and readback before VICE and after
exit; persistent structured Cover timings/status; terminal-phase diagnostics; and one
shared unprivileged launcher. Native tests prove only their supported fixture/headless
behavior. No physical tty/KMS/VT or visible-Cover pass is claimed.

It also contains human-readable setup selectors/internal mapping, Advanced, Back/retry/
resume, immediate working feedback, Wi-Fi-before-completion ordering, hidden-password
explanation and protected credential handling. All normal choices match installed Linux
catalogs. Real namespace locale/keyboard/timezone changes, owner authentication, revised
region/network state and completion gates pass. NetworkManager parses a synthetic
punctuation/space credential without exposing it. Actual radio association is UNTESTED.

## Footprint and controlled host

| Before first-boot expansion | Bytes |
| --- | ---: |
| Raw image | 3087007744 |
| Root filesystem capacity | 2430955520 |
| Root used | 1651539968 |
| Root free including reserved blocks | 779415552 |
| Available to ordinary users | 635551744 |

No minimum SD-card size is inferred. Expansion, sustained maintenance margin and
actual user capacity on the owner's card remain physical measurements.

Host inventory/update guards passed before construction, in the factory after pi-gen,
and after validation. Actual before/after inventory bytes agree, SHA-256
`352fb0f9ed6503e7570278573c8a04219856d8bde086c66e173c7d51c6dd0aa6`.
No host package drift occurred. Guest ext4 available bytes were 52,893,679,616 before
construction and 43,381,764,096 afterward. No remaining build mounts, loops or factory
processes; builder is **stopped**. External mount/capacity guards passed throughout.

## Recovery, preservation and next action

Recovery: `archive/poc4-attempt4-2026-09-17`. Its external manifest and restore report
bind final Project/Menu refs, full bundles, exact offline refs/peeled tags/symbolic HEAD,
fsck, input/package inventories, validation and this hash-bound procedure. Manifest
checksum is separate to preserve the acyclic contract. Images are referenced by their
verified retained locators/hashes, not duplicated into recovery. Evidence is
`qualification/poc4-attempt4-2026-09-17`. Disposable staging roots, credential databases
and journals are excluded; only explicit top-level harnesses and sanitized logs are
retained. TheBench remains one failure domain; independent encrypted custody is open.

Earlier POC1–3, POC4 attempts, failed attempts, frozen kits/packages/locks/artifacts,
qualification/photos/card evidence, checkpoints and protected refs verify unchanged.
Original historical manifest also passes all 1,677 entries. Both AGENTS files unchanged.
Physical evidence is not rewritten. Dosbian-derived organization/recovery ideas remain
backlog; no boot optimization, PSID/RSID work, other-model test or public rights decision.

**Next owner action: FLASH THE EXACT NEW IMAGE AND PERFORM THE HASH-BOUND PI 3B
PHYSICAL REGRESSION PROCEDURE.** Priority: pre-RUN Menu/VT, visible Cover, VICE,
F10/Quit, immediate Menu input and VT return, repeated three times. Then first-boot UX,
Wi-Fi, media/audio/input, SID-Wizard, StrikeTerm, mc/mixer, USB, Samba, SSH, TCPser/mDNS
and persistence. On priority failure preserve the live state and collect the new phase
diagnostics before unrelated tests. No automatic physical test or second candidate.
Stop for owner review. Nothing pushed or published; independent reproducibility is open.
