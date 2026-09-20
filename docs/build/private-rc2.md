# Project CBM 1.1.0 RC2 — private attempt #11

**READY TO FLASH: YES after the recovery manifest/restore verification below.**
[Exact results](private-rc2.json) · [Pi 4 B procedure](../qualification/rc2-pi4b-regression.md).
All 294 actual-image checks, 672 installed package identities, 127 ELF objects,
raw/XZ equivalence and host integrity pass. One image exported; RC2 physical behavior
is UNTESTED. Nothing pushed or published.

## Physical baseline and corrections

The [RC1 owner report](../qualification/rc1-attempt9-pi4-owner-report.json) records the
Pi 4 B Cover/VICE/F10/Menu, setup, persistence and demanding C64 reference PASS, and
primary boot graphic/account-content/USB/practical FILES failures. MC launch alone
passed. Unreported functions remain UNTESTED. Samples 10–21 of two retained numeric
logs span 60.089/60.092s: weighted 99.998829/99.998327%, minimum 99.981/99.959%,
emulated FPS 50.124081/50.123830. Both metric windows pass; warp 23–31 is excluded.
Owner audiovisual observations supply the separate physical context.

RC2 uses one pcbm UID 1000/home for Menu, VICE, SSH/SFTP, FILES, diagnostics and Samba;
canonical library is `/home/pcbm/content`. Root stays locked and general administration
requires the first-boot password. Narrow helpers and separate Samba password remain.
No account migration or permission relaxation was performed on the tested RC1 card.

RC1's root FAT/exFAT mount inherited 0077, blocking its intentionally unprivileged copy
worker. Native kernel tests reproduce this and pass fixed UID/GID/mask options with
read-only/noexec/nosuid/nodev mounting, no overwrite, safe error feedback and unmount.
FILES exposes library/home browsing and the existing safe import workflow. Actual RC2
USB success is a physical gate, not inferred from loops.

The exact v1.0 image's numbered primary art and boot chain were inspected read-only.
RC1's obsolete no-argument Cover call was rejected. RC2 explicitly presents unchanged
private-admitted `pcbmcover1.jpg` through supervised SDL, 1.5s after first submission,
with terminal capture/restore and bounded child cleanup. Its historical Model 5/500
wordmark is retained; it does not change Pi 4 policy. Seven machine Covers and VICE
bytes/settings are unchanged. No old framebuffer/ImageMagick boot mechanism was copied.

RC1's 5.134061s getty→PAM gap matches inherited Type=idle's five-second deferral.
Type=simple preserves getty/login/PAM/first-boot ordering. Numeric private phase traces
separate setup/profile/presentation/status/dialog boundaries. The observed 30-second
power-to-Menu path is not fully explained, and RC2 speed/visibility are not preclaimed.
NetworkManager-wait-online and unrelated maintenance services remain intact.
See [correction contract](../runtime/rc2-corrections.md) and [boot guide](../release/boot.md).

## Validation and retained failure

Product 222/222 and Menu 99/99 pass on host/native; installed lifecycle 12/12, all seven
machine Covers plus primary image, three repeated cycles, authenticated admin, local
SSH/service persistence/discovery, dialog, MC and ext4/FAT/exFAT import pass within
native fixture limits. Initial fixture failures are retained in the exact report.
Source Bash/Python/JSON/link/privacy/whitespace checks pass; documentation has 81 local
links checked across 11 release guides. Public bootstrap gaps remain explicit.

Attempt 10 stopped before export because the strict installer JSON reader rejected
fractional 1.5 seconds. Its frozen kit/tree/logs remain. A distinct recipe-only attempt11
uses 1500milliseconds and pre-freeze reader checks; all four exact package descriptors
are reused. Host integrity passes before/after failure and success. Final build took
173.69s, peak 505412KiB. No finished image or protected input was replaced.

The inherited export suffix is **private-rc1**, while the version and installed identity
are **RC2**. Original filenames are preserved below and bound by hashes. This cosmetic
filename issue does not relabel the installed identity or justify another image build.

## Exact inputs and artifacts

Integration `e09a285f199fdcf29c6ad7d5dac92bbfefd262b4`. Menu tag v1.1.0_rc2 object
`ab2560a00d3535b5fa4357511bc166f572cab22b`, peeled
`bcbf61e9e3d263f409b4983b5c2a30d6bf37f18f`.
Runtime package source remains `54e5351c871a119a2d49077407f712a7eb57d0d5`;
recipe-only retry source is the integration above.

| Package | Status | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| project-cbm-menu_1.1.0~rc2-1+pcbm1_all.deb | NEW for RC2; exact reuse from halted attempt10 in attempt11 | 1294180 | `a6ceb57e4e7565cc9932d2a624027751349c49885a576bce5226d13847475ec6` |
| project-cbm-runtime_1.1.0~rc2-1_all.deb | NEW for RC2; exact reuse from halted attempt10 in attempt11 | 67580 | `26b74b9f4896d1d5abae0cf41d5c75078c49df43eb83a602c85671b850a4bd0f` |
| project-cbm-tcpser_1.1.6~beta-1+pcbm1_arm64.deb | REUSED from RC1 | 26872 | `8b8f8a4f3ec98dddf5bdb347320dad05e1bbe5230e0ee2727248c247a5af584f` |
| project-cbm-vice_3.10-1+pcbm4_arm64.deb | REUSED from RC1 | 5069684 | `a7b77c3b006eb190c64c10cadbfd91ce4152a73523c440496209293da2901dc1` |

Lock `inputs/frozen-poc4-attempt11/release-lock.json`, SHA-256 `9831849a3fd12c12528e09d1b7f265d9b03e48ca2819b99f0dfe4583156e7581`.
Paths below are relative to configured external bulk workspace, currently
`/Volumes/TheBench/ProjectCBM-Work`.

Raw `artifacts/private-rc2-attempt-11/2026-09-19-project-cbm-1.1.0-rc.2-lite-private-rc1.img`; **3095396352 bytes**;
SHA-256 `f3b21038c1fc289c58396cb8106348cd3cda514a96548e5c6d0c9277fced1be4`.

XZ `artifacts/private-rc2-attempt-11/image_2026-09-19-project-cbm-1.1.0-rc.2-lite-private-rc1.img.xz`; **598069592 bytes**;
SHA-256 `f4b638100f37d673d9a455015121a8ea753b9bcd2daeca02630cba9e33a24ca9`.

Raw/XZ expanded equivalence passes independently in guest and on external copies.
The exact package manifest is `qualification/rc2-2026-09-19/packages.json`.
Footprint/margin measurements and their limits are in the JSON report; no unsupported
nominal minimum card size is invented.

## Recovery and next action

Checkpoint `archive/rc2-2026-09-19` retains both full Git bundles, exact refs/peeled tags,
source/input/artifact locators, allowlisted evidence, verified offline restores/fsck
and manifest hashes. The final external `manifest.json` and `restore-report.json`
are the checksum authority; verify PASS before flashing. Earlier candidates, failed
attempt10 and v1.0 preservation evidence remain unchanged. The builder is stopped
with its external-backed disk retained. Independent encrypted custody and independent
clean-build reproducibility remain open; another folder on TheBench is not a backup.

Release blockers are exact RC2 physical acceptance and the existing public rights/
bootstrap gates. Physical qualification, outcome documentation and optional future
work are separated in the JSON report. **Flash this exact image and perform the Pi 4 B
RC2 procedure; stop and report any core regression first.** No push/public release.
