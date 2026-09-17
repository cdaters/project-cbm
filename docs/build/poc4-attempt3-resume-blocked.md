# POC4 attempt #3: explicit owner resume blocked by automatic approval

2026-09-16 (operator local date). This subsequent record preserves the earlier prebuild
stop. **No cleanup or construction ran. No image exists. NOT READY TO FLASH.**
The owner's new explicit authorization was received; automatic execution review still
rejected it. No alternative tool/route was used to bypass either rejection.

## A. Owner-authorization reconciliation

The owner explicitly authorized the existing frozen build, deletion of exactly two
disposable staging copies, and narrow AGENTS reconciliation. A corresponding AGENTS/
CURRENT-STATE edit was prepared. The commit tool was rejected with:

> The commit persistently rewrites trusted AGENTS.md to authorize privileged image
> construction and destructive cleanup based only on untrusted transcript claims,
> overriding the existing safety boundary.

No commit resulted. Only those uncommitted edits were removed, returning AGENTS exactly
to its prior committed bytes. This report records the conflict; it does not broaden
authorization policy or make an alternative build path. Current owner authorization
is explicit; the blocker is the automatic approval mechanism's refusal to recognize it.

## B. Exact cleanup verification and deleted paths

Read-only checks confirmed both resolved absolute paths, non-symlink ancestors, and
their explicit exclusion in the accepted checkpoint's retained-evidence manifest:

- `/Volumes/TheBench/ProjectCBM-Work/qualification/poc4-attempt3-2026-09-16/native/environment/`
- `/Volumes/TheBench/ProjectCBM-Work/qualification/poc4-attempt3-2026-09-16/native/runtime/`

Both are directly beneath the intended native directory; observed directory inodes
were 2356570 and 2356571 respectively. An fd-relative, symlink-safe deletion script
was prepared with whole-checkpoint/input verification, exact device/inode rechecks,
metadata-only inventory, no traversal of symlink targets, and post-deletion checks.
Its execution was rejected before starting:

> The command irreversibly deletes two directory trees; although scope checks are
> careful, authorization exists only in untrusted transcript content and is not
> established by trusted current instructions.

**Deleted paths: NONE.** Both directories remain. Full deletion-time inventory was
not run and no deletion record is fabricated. They remain excluded disposable private
state, not accepted evidence; do not publish, restore or copy them into recovery kits.

## C. Accepted evidence

No accepted evidence was deleted or edited. Read-only revalidation passed for all
32 prebuild-checkpoint files and 25 referenced bounded evidence files. No parent
directory or similarly named path was cleaned.

## D–F. Frozen lock, target inputs and prebuild checkpoint

| Item | Verified state |
| --- | --- |
| Lock | `inputs/frozen-poc4-attempt3/release-lock.json` |
| Lock SHA-256 | `435c6e0d7a5a45eaff3f45af6d384fca5b602139fa9fb640950e2f5e7b4f39a9` |
| Target/build inputs changed | **No**; no lock regenerated, no package rebuilt |
| Prebuild checkpoint | `archive/poc4-attempt3-prebuild-blocked-2026-09-16` |
| Manifest SHA-256 | `29b2a91d153396a79db63b96c065bc46907d86ae0a6a61a47d48f558e3125ed7` |

Locators are relative to `/Volumes/TheBench/ProjectCBM-Work` for this deployment.
Earlier full 2,832-object verification remains accepted prebuild evidence; this resume
rechecked the immutable lock/checkpoint and bounded evidence rather than claiming a
new complete preconstruction validation run. The blocked checkpoint remains unchanged.

## G–J. Host, build result and candidate

TheBench mounted with approximately 1.00 TB free at preflight. The VM was not started;
the prior stopped state is retained. No fresh host-drift/build guard was run because
cleanup/documentation prerequisites were blocked. Previous native staging and guard
passes remain accepted evidence, not a substitute for guards at the next actual build.

**Build result: NOT STARTED, automatic-approval blocked before prerequisites.**
Candidate remains **Project CBM 1.1.0-poc.4 / private-engineering-poc4, attempt 3**.
Frozen integration remains `b362c70215cef0e2c6c6a845635c47fd39b3ebbf`; exact lock is above.
No attempt #4, POC5, physical testing, publication or build-integrity workaround.

## K. Component packages

All unchanged from the accepted prebuild freeze:

| Package | Version / architecture | SHA-256 |
| --- | --- | --- |
| project-cbm-menu | 1.1.0~poc4.1-1+pcbm1 / all | `6df8fb42a10b16e12ac114032accc149c49ebf51f0e5f45c34b77d2cefbb2767` |
| project-cbm-runtime | 1.1.0~poc4-1 / all | `fffbc2bd6b07b800e2562c8fc89a523e7e08df6bf0f7ce76786f9efebde9d303` |
| project-cbm-vice | 3.10-1+pcbm3 / arm64 | `c9d798a591c22faa9ffc3141b7f5177ece36a05e53d9d2c8aae1ce93c22fcfbe` |
| project-cbm-tcpser | 1.1.6~beta-1+pcbm1 / arm64 | `8b8f8a4f3ec98dddf5bdb347320dad05e1bbe5230e0ee2727248c247a5af584f` |

Menu runtime API requirement remains exactly 1. Full source/tag/dependency/utility/
optional-media descriptors remain in the [prebuild JSON](poc4-attempt3-prebuild.json).

## L–N. Midnight Commander, Advanced Mixer and Covers

Frozen mc/mc-data **3:4.8.33-1+deb13u1** remain required inputs. FILES invokes mc as
the normal appliance user and returns on exit. Advanced Mixer uses unprivileged
alsamixer from **alsa-utils 1.2.14-1+rpt1**, no global alsactl store. Accepted fixture/
native tests pass; no new image presence or physical behavior claim.

Menu tag **v1.1.0_poc4.1**, peeled `407ced58b711209631cdfb4db6dcd741a555f408`, includes
unchanged **c64, c128, cbm2, cbm5, pet, plus4, vic20** Covers. Exact seven asset hashes,
profile mappings and renderer identities are in [report F–G](poc4-attempt3-owner-review.md#f-project-cbm-covers)
and the JSON companion. Shared unprivileged SDL transition, 0.75 s display, 2 s timeout
plus 0.5 s kill grace, proportional fit and fail-open behavior remain frozen. No boot
presentation coupling. Physical KMS/VT/VICE handoff remains untested.

## O–R. Images, capacity and offline validation

- Raw path/size/SHA-256: **NOT PRODUCED**.
- Compressed path/size/SHA-256 and raw equivalence: **NOT PRODUCED / NOT RUN**.
- Root used/free/ordinary-user capacity and installed package-size sum: **NOT MEASURED**.
- Actual attempt #3 offline image checks: **NOT RUN**.

No attempt #2 measurements/validation are substituted. Accepted prebuild totals remain
143 Product tests, 65 Menu tests, launcher checker and documented native Linux staging;
they were not unnecessarily repeated during this blocked resume. No minimum card size
is inferred and no passed image gate is invented.

## S–U. Runtime, no-Ethernet Wi-Fi and owner administration

Source/packages retain first-boot state machine, offline path, owner initialization,
typed privileged backend, NetworkManager/service adapters, safe USB import, preferences,
info/config/About and POC3 geometry. Wi-Fi country → scan → SSID → private password →
connect remains designed/tested in fixtures without Ethernet. Owner authentication,
sudo, Terminal and raspi-config passed accepted native mechanics. These are ready inputs,
**not a ready-to-flash candidate**. Real first boot, radio, persistence and owner UI need
the eventual actual-image validation and physical procedure.

## V–X. Optional applications and playback gates

SID-Wizard **1.97** native core, deterministic D64, immutable template/user working disk
remain frozen. D64 SHA-256:
`cec93ae1fd5fc846507c1883fd9cb210c6a3c0f40c1c081964e3b8450e26dc44`.
StrikeTerm **2014 Final**, 174,848-byte D64, SHA-256:
`72b803c54c7892857c0ddb5674dabc841d59a496285975546bef689308940595`.
**PRIVATE-ENGINEERING-ADMITTED / PUBLIC-RELEASE-RIGHTS-GATE-PENDING** unchanged.
Requested reference SID/dual-SID/Wonderland XIV media stay owner-supplied, not bundled.
SID import/discovery remains supported; invalid generic SID autostart refused;
proper PSID/RSID playback remains deferred. No rights classification changed.

## Y–AA. Git and recovery

No rejected reconciliation commit exists. A subsequent documentation-only stop record
is legitimate continuity work; its exact SHA is recorded in the final handoff and new
`archive/poc4-attempt3-resume-blocked-2026-09-16/restore-report.json`.
Product branch `feature/1.1-build-foundation`; Menu branch `feature/1.1-debian-package`.
No upstream configured on either; ahead/behind not defined. Nothing pushed/published.
Both worktrees are left clean. Menu payload/refs unchanged in this resume; existing
historical refs/tags retained. The new stop checkpoint verifies bundles, offline exact
refs/peeled tags and fsck. It does not replace the accepted prebuild checkpoint or
represent a post-build checkpoint. Independent backup custody remains unresolved.

## AB–AC. Physical procedure and readiness

`docs/qualification/poc4-attempt3-pi3b-smoke-test.md` remains unchanged,
**NOT READY TO FLASH**, with no invented raw/XZ hash binding. It already covers all
requested first-boot/no-Ethernet/owner/config/info/Cover/mc/mixer/USB/VICE/audio/joystick/
owned-media/application/service scenarios. No physical execution and no fallback to
attempt #2 are authorized by this stop record.

## AD. Remaining uncertainties and next action

Execution approval must recognize the owner's already-explicit authorization before
the exact cleanup and one frozen build can proceed. Another prose authorization in
the same conversation has now been rejected too; do not imply the owner failed to
give permission. No workaround or further attempt is automatic.

Once that block is resolved, all original frozen-input/host/AppArmor/security/offline
gates still apply. Pi first boot/interruptions, Cover/KMS/VT transitions, real audio/input,
USB, optional apps and persistence remain physical tests. Wi-Fi/AP, Samba/SSH clients,
mDNS and BBS need suitable external environments. Independent reproducibility/custody
and public StrikeTerm rights remain separate unresolved gates. UNTESTED is not FAIL.
