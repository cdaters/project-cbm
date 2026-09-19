# Private POC4 attempt #8 — Pi 3 B+ performance candidate

**READY TO FLASH: YES, with the verified recovery checkpoint below. Stop for owner physical testing.**
[Exact results](private-poc4-attempt8.json) · [Pi 3 B+ procedure](../qualification/poc4-attempt8-pi3b-plus-performance.md).
All **260 actual-image checks** and guest/external raw/XZ equivalence pass.
The external recovery manifest/restore report is the final checkpoint authority; it must
show PASS before flashing. This image's physical behavior is **UNTESTED**. Nothing pushed
or published; no SD-card writes, boot-polish work or active-VICE VT workaround.

## Physical evidence and diagnosis

[Attempt #7 owner report](../qualification/poc4-attempt7-pi3b-plus-performance-2026-09-18.json)
records sustained slow audio and graphics with the demanding Oxyron reference on Pi 3 B+.
This is a performance RELEASE BLOCKER; unreported functions remain UNTESTED. Earlier
functional results retain their original image/model binding.

The removable external USB SD root partition was verified read-only before inspection;
installed identity exactly matches attempt #7 lock
`1c25d7f7850c63c41e2730bdaef2deef9cd6d0ccf1321c9b23fd4d9228926b3d`.
Detailed device UUID/mount records remain private external evidence. Already-mounted
Paragon evidence is not presented as pristine forensic acquisition. Six original
screenshots, captions/hashes and allowlisted persistent diagnostics are preserved under
`qualification/poc4-attempt7-performance-2026-09-18`; initial manifest SHA-256
`1cd2a6527570bf287aaa9f2cae081a9076081046dffe02b6decdd59ab4a164bc`.
No large photograph, credential store or owner reference payload entered Git or the image.

The card and supplied `kong_arcade.prg` copies match: 37,282 bytes, SHA-256
`a80816ec175ffcbc44b4127f43ea43091df28494e8da9ef9e93bff72c1fdd554`.
VICE was 3.10-1+pcbm3, x64sc; exact invocation, executable hashes, saved/compiled/runtime
resources and bounded v1.0 comparison are in [the decision record](../runtime/c64-performance-2026-09-18.md).
KMSDRM/OpenGL/VSync, SDL/ALSA, reSID MOS8580/filter/48 kHz resampling and repeated sync
lag were observed; saved resources contained only the initial geometry/fullscreen seed.

Owner readings of 1.4 GHz, 45.1 C, throttled=0x0, available RAM/unused swap and no material
competing workload do not explain the slowdown. x64sc's main thread occupied roughly
one core (99–109% snapshots); its four-thread/all-four-CPU allowance does not parallelize
the emulation core. This supports a single-thread emulation budget bottleneck, not a
claim that GPU cost is zero or that every run was free of throttling.

## Correction and tradeoff

The v1.0 runtime also used x64sc/SDL/ALSA; no recovered Pi 3 preset justified switching
cores. Its historical build predominantly used -O3, versus current packaged -O2.
Native comparisons on the exact reference used the same 60-million-cycle workload and
60.896 seconds of real audio: -O2 x64sc/resampling **28.396857 CPU seconds**;
-O3 x64sc/resampling **22.442322**; -O3 x64sc/interpolation **17.907009**;
-O3 x64/resampling **12.292922**. O3/resampling audio matched baseline exactly.
Interpolation/x64 hashes differed. These are bounded native comparisons, not Pi capacity
or full interactive compatibility measurements. Dummy rendering cannot model Pi scanout.
Invalid early no-sample/recording harnesses remain retained and excluded from conclusions.

**Chosen default:** portable ARMv8-A/generic **-O3**, retaining Debian hardening, and
**x64sc + reSID interpolation** (`SidResidSampling=1`) for initial C64/C64SC preferences.
The combined native reference cost was **36.9% lower**. SID filters, cycle-accurate core,
true-drive and VIC-II accuracy, CRT/geometry/VSync, SDL/ALSA, F10 and transition ownership
remain. No workload hack, model-specific shell branch, FastSID or silent Pi 3 withdrawal.
User-saved settings remain authoritative. Other profiles retain their resources.

Interpolation changes sampling/anti-aliasing cost and can change high-frequency sound
or SID readback-sensitive behavior. It is not bit-identical fidelity. The physical
procedure must establish real time and correct behavior for ordinary C64 software and
the demanding reference. Faster-machine users can save resampling if desired.

Bounded opt-in numeric telemetry measures raw wall-window speed independently of VICE's
reset-to-100% UI smoothing: at most 120 records, roughly five seconds apart. The new
qualification gate requires 12 consecutive steady non-warp samples over at least 60 s,
weighted speed 98–102%, no sample below 95%, appropriate PAL/NTSC FPS and correct normal
audio/visual behavior. Loading/menu/pause/reset/warp intervals are excluded by observation.
The parser emits numeric data only; metric PASS alone is not physical qualification.

## Account and release documentation

Literal `owner` originated in runtime-activation commit `1876b9c`; no recovery constraint
required that name. The role remains Owner/Administrator, default username **pcbm**,
UID 1001/home `/home/pcbm`, authenticated sudo and first-boot owner password. Computer
Name remains **projectcbm**, editable. SSH: `ssh pcbm@projectcbm.local`. File Sharing:
username pcbm, separate password, content share `Project CBM` at `/home/pi/pcbm`, writes
owned by pi. The local console/emulator remains pi. Existing images are not migrated.
First boot, account checks, policy, SSH/Samba, Menu guidance/status/tests and manuals agree.
Credential transport/storage, redaction and opt-in exposure remain intact.

Nine substantial release guides ship in Runtime. Start at [documentation](../README.md):
[user manual](../release/user-guide.md), [network/services](../release/networking.md),
[Build Your Own](../release/build-your-own.md), [pi-gen factory](../release/factory.md),
[VICE](../release/vice.md), [accounts/layout](../release/accounts-and-layout.md),
[customization](../release/customization.md), [developer](../release/development.md),
[user recovery](../release/recovery.md) and [engineering recovery](../recovery.md).
The manuals explain actual stage0/1/2/stage-cbm, package composition, source/build flags,
filesystem/services, practical edits and rebuild/validation consequences. All 66 local
links and 33 concrete source paths in the release audit pass; actual documented private
package/export/freeze/build/validation commands were exercised.

Public release replay, derivatives and private predecessor-kit engineering are distinct.
The public-from-source bootstrap is still incomplete: publication of exact refs/component
and corresponding-source inputs, authenticated OS closure/catalog, host/bootstrap inputs,
rights-cleared assets and a predecessor-independent first-lock assembler remains necessary.
The private kit is not claimed publicly available. Bounded tooling now supports changed
VICE packages and exports an image-bound installed package JSON manifest. Public bootstrap
completion is a release task, not falsely marked done by this private candidate.

## Packages, lock and image

Frozen Product integration `9aef29a7e87f7a88bd47d9f01c430aa3eb0c0b21`. Menu
`v1.1.0_poc4.6`, peeled `2ec5f8dcb04b5d86f64a2ce6a96625c3528eac73`, annotated object
`085ab4bd820709bf0407cdbba35d25060e2541fd`. Runtime/Menu/VICE are newly built; TCPser,
pi-gen/base/host closures, seven Covers, original media and existing optional/private
admissions reuse verified bytes. VICE debug symbols and corresponding-source/build records
are retained externally; debug symbols are not installed in the image.

| Package filename (version included) | Input | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| project-cbm-menu_1.1.0~poc4.6-1+pcbm1_all.deb | NEW | 1106624 | `4df04ab44ebd44313f94e77c1130e3d792f7c0ea9911ca51760b3b765a0b7827` |
| project-cbm-runtime_1.1.0~poc4.5-1_all.deb | NEW | 60460 | `b1c412835fd8c9b55d275c66bfecdbe656d48c43bd5a83cecb445ce1cfbc9479` |
| project-cbm-tcpser_1.1.6~beta-1+pcbm1_arm64.deb | REUSED | 26872 | `8b8f8a4f3ec98dddf5bdb347320dad05e1bbe5230e0ee2727248c247a5af584f` |
| project-cbm-vice_3.10-1+pcbm4_arm64.deb | NEW | 5069684 | `a7b77c3b006eb190c64c10cadbfd91ce4152a73523c440496209293da2901dc1` |

Lock `inputs/frozen-poc4-attempt8/release-lock.json`, 2986 objects;
SHA-256 `53d2d25f997613434e16fdecc0057eeea88da74783f9487b2501cbec4d1cce57`.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `artifacts/private-poc4-attempt-8/2026-09-18-project-cbm-1.1.0-poc.4-lite-private-poc.img` | 3095396352 | `e4bb7f03ed26583097f92e8b8d1c2e9e4e3616d4d39940c78f70618ca3a81c40` |
| `artifacts/private-poc4-attempt-8/image_2026-09-18-project-cbm-1.1.0-poc.4-lite-private-poc.img.xz` | 599057044 | `892082b4ef8468dab3273b4746350863f9bc75c17e6c2e18a0ef3b4eb62129e4` |

Paths are relative to configured bulk storage, currently `/Volumes/TheBench/ProjectCBM-Work`.
The basename resembles earlier attempts; **use the attempt-8 directory and complete hash**.
Raw/XZ equivalence passes before/after transfer. No finished image was modified.
The approved native arm64 Lima/VZ + pinned pi-gen factory took 194.63 seconds, peak RSS
514696 KiB. Independent-build bit-identical reproducibility is not established.

## Validation, capacity and recovery

Product host/native **195/195**, Menu host/native **96/96**, installed lifecycle **10/10**.
Eleven performance/account/manifest focused tests are included in Product's total.
All ten VICE cores pass native cycle-budget smoke and arm64 PIE/RELRO/NOW/non-executable
stack checks. Generated top-level and nested reSID Makefiles confirm portable -O3 and
hardening. Final numeric telemetry passes 12 consecutive samples with **71.048 seconds
of non-silent synthetic audio**. No Pi speed/audio/display qualification is inferred.

Native setup/account/su/sudo, service start/stop/restart/enablement, SSH password login and
refused new connection after disable, SMB mDNS on an isolated dummy interface, real dialog
at three sizes, USB import, MC and network/tty fixtures pass. Seven installed Covers
pass SDL dummy decode/present/release; three supervised cycles restore terminals/reap
children. Physical client discovery, hardware input/audio and reboot persistence remain
procedure items. Corrected harness assumptions and invalid exploratory measurements are
retained in `qualification/poc4-attempt8-2026-09-18/contextual-failures.json`.

Actual image: **121 main + 20 supplemental + 119 refinement = 260 PASS**; **672 package
identities**, **127 ELF objects**, FAT/ext4 integrity, systemd, identity, account/service/
discovery/security/privilege, lifecycle, documentation and no-secret sealing checks PASS.
The package manifest is `qualification/poc4-attempt8-2026-09-18/packages.json`, SHA-256
`6afd2a46095f26268565090af82d3ab1b96c7399f9b04cc2fdaac1f641b24080`. Host inventory/update/capability gates
pass before/after; AppArmor is retained, mounts/loops/emulators are closed and the builder
is stopped with its disk preserved. Remaining builder free space is 36183490560
bytes; another construction needs capacity planning before the 40-GiB start gate.

Root capacity 2439266304, used 1655222272, user available
639762432 bytes before expansion; boot used 78420992.
Measured native overlay writes 174383104 (includes test/debug
package work), changed packages compressed 6236768 and
installed 46824448. Reserving all three leaves
412318112 bytes. This is conservative measured
headroom, not a physical first-boot peak/full OS upgrade guarantee or a nominal card minimum.

Recovery: `archive/poc4-attempt8-2026-09-18`. Verify its external manifest SHA-256 and
`restore-report.json`: complete bundles, exact refs/peeled/symbolic tags, offline source
restore and fsck must pass. The manifest is external to avoid a checksum cycle. Original
historical/audit byte/metadata/xattr manifests and earlier candidate/input/recovery records
verify unchanged. Independent encrypted custody remains open; another directory on the
same TheBench is not an independent backup. No push/publication or protected-ref rewrite.

## Release readiness and next action

- **RELEASE BLOCKER:** Pi 3 B+ real-time qualification; public redistribution gates and
  complete public input/bootstrap route before public release.
- **PHYSICAL QUALIFICATION REQUIRED:** the exact-hash Pi 3 B+ core/performance/account/
  service procedure; other profiles/models independently. This candidate is a possible
  RC basis only after qualification and planned final polish, not a public RC declaration.
- **DOCUMENTATION FOLLOW-UP:** record owner outcomes and publish the exact public release
  manifest/input catalog only when authorized.
- **OPTIONAL POST-1.1 IMPROVEMENT:** supported active-VICE VT and justified Windows browsing
  enhancement. Independent clean rebuild and encrypted recovery custody remain open.

**Next owner action: flash the exact new image and perform the Pi 3 B+ performance
qualification procedure.** Stop on a core failure and preserve evidence. Quiet boot and
measured fast boot remain the next separate owner-directed milestone after a pass.
