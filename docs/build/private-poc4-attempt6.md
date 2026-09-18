# Private POC4 attempt #6 — 2026-09-18

**READY TO FLASH: YES. Stop for owner Pi 3B testing.**
[Exact result](private-poc4-attempt6.json) and
[hash-bound physical procedure](../qualification/poc4-attempt6-pi3b-regression.md).
No physical test, push or publication by Codex. This candidate is physically UNTESTED.

[Attempt #5 findings](../runtime/physical-ux-correction-2026-09-18.md) retain the exact
owner report, verified read-only card identity/35 files and 27 hashed/captioned original
photos outside Git. Specified lifecycle, setup completion and information IP functions
PASS; Cover and first scan FAIL. Other unreported functions remain UNTESTED.

Cover is now admitted with exact artwork. Two slots hit the old two-second budget
before renderer completion and were killed; one submitted a frame, without proven
visibility. All terminal restorations/VICE exits pass. New six-second total budget
plus existing half-second grace, first-present-relative 0.75-second dwell and phase
timings address the supported defects while preserving same-group terminal ownership.
The exact stalled initialization call and remaining physical visibility require testing.

Wi-Fi formerly read cached APs immediately after scan acceptance. It now waits for
ready devices and advanced LastScan, with at most two requests and a 25-second bound.
The precise historical radio/regulatory cause is unrecorded. No-radio timeout and
fixed private diagnostics are truthful. Dialog asterisks work through the protected
pipe. ASCII ranges fix the reproduced C-locale Unicode-dash corruption; the first
card launch has no LANG/LC_ALL, later launches have en_US.UTF-8. Main Menu formats
Product's bounded network-only JSON; detailed information stays in existing views.
Quiet/rainbow/startup suppression, boot presentation and measured fast boot stay deferred.

## Frozen identities and outputs

Product integration `5992e2a7b1a84cbad016a293624d48aaa7cdd1cf`; Menu `v1.1.0_poc4.4`,
peeled `6522111691ce494b00637549365d6a5f2a7773ff`, annotated tag object
`f1d4560c678288d7d7d6b2bfcfd26e58a6fa9f45`.
Only Runtime `1.1.0~poc4.3-1` and Menu `1.1.0~poc4.4-1+pcbm1` were rebuilt.
Runtime package SHA-256 `161eb30ad22ae00b6930056ac8c2a34c67576744ea0fe3a247be2032eea8857b`.
Menu package SHA-256 `f1d5c59561c2a8b09ce823d0e2380d7f90ed143ced7b9e8d49f0bb057a8cf82c`.
VICE/TCPser, seven Covers, closures, pinned pi-gen and rights admissions reuse exact bytes.

Schema-4 lock `inputs/frozen-poc4-attempt6/release-lock.json`, 2,923 verified objects,
SHA-256 `8a5f7c929e73ac38ab42945b2bf22d577eb2b8a9e0500dd69c27f005f75c6de2`.
Bulk paths are relative to `/Volumes/TheBench/ProjectCBM-Work`:

| Output | Bytes | SHA-256 |
| --- | ---: | --- |
| `artifacts/private-poc4-attempt-6/2026-09-18-project-cbm-1.1.0-poc.4-lite-private-poc.img` | 3087007744 | `bf81b1f95ab65d19753f85fdafbb5a93f45eae68b0bea4208bef62c9d6a2c328` |
| `artifacts/private-poc4-attempt-6/image_2026-09-18-project-cbm-1.1.0-poc.4-lite-private-poc.img.xz` | 598195324 | `028d9b8b0fbc92bcfe75741b9d842885efda9e194cfbc6d1e8cfe26b8967354f` |

## Validation and limits

Product host/native 173/173; Menu host/native 85/85; installed lifecycle 10/10,
seven actual SDL dummy Covers and three renderer/VICE-fixture cycles PASS. Native
AppArmor/privileges/accounts/setup/services/import/utilities, synthetic IP/MAC and
kernel tty alias checks PASS. Real dialog C/C.UTF-8 masking/ranges PASS. Installed
no-radio scan returns in 10.022 s; five native-VM Main Menu summary runs 38.30–65.93 ms.
These are not physical radio/KMS or Pi latency evidence. Initial test harness failures
and their corrected reruns are retained in the exact result/evidence.

Pinned native arm64 Lima/VZ pi-gen build: 187.92 s, process peak RSS 504792 KiB, exit 0.
Actual image: 121 main + 20 supplemental + 89 corrective checks PASS; 127 ELF objects,
672 installed package identities, FAT/ext4 read-only checks and systemd units PASS.
Raw/XZ equivalence verified in guest and again after external transfer. No image edits.

Root capacity 2430955520, used 1651564544, ordinary-user available 635527168 bytes
before expansion; boot used 78420992 bytes. Native setup/regression overlay allocated
16408576 bytes. New compressed packages 1133392 plus unpacked payload 1469440 bytes;
reserving those measured amounts leaves 616515760 bytes of the image's user allowance.
This conservative arithmetic is not a full-OS-upgrade guarantee or a measured physical
first-boot peak. Expanded capacity depends on the card/test; no nominal 8 GB minimum.

Host inventory/update masks, capabilities before/after and final cleanup PASS. Builder
stopped, no remaining factory processes/mounts/loops. Nondestructive 160→192 GiB growth
was preceded by a fully hashed stopped disk/configuration clone; no host package updates.
Historical checkpoints, frozen objects, protected refs and both AGENTS files verify.

## Recovery and next action

`archive/poc4-attempt6-2026-09-18` contains final refs/bundles, verified offline restore,
peeled tags/symbolic refs/fsck, reviewed evidence and hashes/relative locators for inputs,
packages, raw/XZ and private physical evidence. Its manifest digest stays external to
avoid a checksum cycle. No credential-bearing native roots are exported. Private stopped
builder preservation is separately indexed. TheBench copies are not independent custody;
independent encrypted backup and clean-build reproducibility remain open.

Owner: verify the exact image hash, use a fresh test card without Imager customization,
then follow the linked procedure. Prioritize initial scan/masking/ASCII feedback and
visible correct Cover with immediate Menu input and both VT directions across three
cycles. Preserve phase diagnostics before another launch on failure. Test Main Menu IP
states against Network Information. Stop on failure; do not repair qualification media.
