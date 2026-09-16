# Project CBM current state

## Runtime activation: build-integrity stop — 2026-09-16

**No POC4 image exists. STOP for owner review; do not flash, retry or build another
candidate automatically.** POC3 remains the last physically demonstrated Pi 3B
foundation. [Attempt/report](docs/build/poc4-blocked.md), [exact inputs](docs/build/poc4-blocked.json),
[native staging evidence](docs/build/runtime-activation.md).

First-boot/owner administration, the fixed backend, NetworkManager/service adapters,
USB broker, boot preferences and matching runtime/Menu packages are source-implemented.
138 product tests, 50 Menu tests plus the launcher checker pass. Native Debian tests
verified package installation, account/PAM/sudo, helper restrictions, offline setup,
services, private Wi-Fi keyfiles, terminal return and synthetic-media import. This is
not physical qualification or proof that all candidate/runtime gates are complete.

Integration: `cf3a289f99bd7599c8e6f1aa3da4753aa733f981`.
Menu: `v1.1.0_poc4`, peeled `bb8a66ea9da994b30f978ad87d61c9aedb03dad6`.
New schema-4 lock: `inputs/frozen-poc4/release-lock.json`, SHA-256
`99f3985b8eac77398fbc71d66160f91beff50d04f6ae246757a4f081436bfacc`.
The lock and packages remain frozen evidence of this failed attempt.

Image construction failed during upstream stage1 AppArmor package configuration:
the operator invocation exported a builder-only TMPDIR into the target chroot;
`mktemp` could not use that absent path. No AppArmor/security bypass, frozen-input
mutation, image repair or retry was attempted. Host inventory remained pinned; no
build mounts/loops or proxy remain. The VM is stopped. See the report for the exact controlled failure.

SID-Wizard 1.97 core is frozen under its accepted license. Author-endorsed StrikeTerm
2014 Final bytes match the recorded Combian hash and are **PRIVATE-ENGINEERING-ADMITTED;
PUBLIC-RELEASE-RIGHTS-GATE-PENDING**. Neither was delivered in a new image. Requested
reference SID/demo payloads remain owner-supplied. Generic `.sid` autostart is blocked;
a dedicated PSID/RSID player remains a later gate.

Branches: product `feature/1.1-build-foundation`; Menu `feature/1.1-debian-package`.
Recovery checkpoint: configured bulk storage `archive/runtime-activation-blocked-2026-09-16`;
exact final refs, bundles and restoration verification are in its manifest. Build
logs: `qualification/poc4-build-blocked-2026-09-16`; final packages: `packages/poc4-final`.
POC1–3 and historical refs remain immutable. No push/publication or physical test.
Independent backup/custody and independent clean rebuild remain unresolved.

**Next owner action:** review the stopped attempt and authorize a bounded build-host
versus chroot environment fix, regression test and new attempt location/input identity
as needed. `/tmp` inside the external-backed Linux guest is not the Mac's internal
`/private/tmp`. Do not remove AppArmor or weaken security to get an image. Complete
remaining staging/offline/qualification-procedure gates before any physical test.
Boot presentation/performance stays deferred until a new candidate physically passes.

Earlier sections below are completed historical checkpoints and do not supersede
this stop or the private StrikeTerm decision.

## Optional applications and reference-content addendum — 2026-09-16 / STOP

Configuration maturation below remains complete. The owner additionally authorized
SID-Wizard/StrikeTerm source integration and rights/provenance research for selected
SID/demo references. [User guide](docs/runtime/optional-applications.md),
[exact input/rights/factory contract](docs/runtime/optional-applications-contract.md),
[reference findings](docs/design/reference-content-2026-09-16.md).

SID-Wizard **1.97 native one-SID core** is admitted under its author's explicit
permissive notice. Source hash/member selection and deterministic D64/tar are retained;
no example music, host application or full manual is installed. Schema 3 declares
optional source/recipe/rights/payload inputs; schemas 1/2 and frozen locks remain intact.
The stage installs a template/notice and fresh user working disk only when declared.
No new full candidate lock, package, image, upstream binary rebuild or physical pass.

StrikeTerm 2014 remains **OWNER-SUPPLIED**: source/version/author references resolved,
complete-disk redistribution permission and upstream-byte comparison unresolved.
CONTENT now asks the profile authority to route the two application folders to
validated x64sc without changing the user's normal default. Shared launcher, F10,
geometry, session, diagnostics, audio and privilege policy are unchanged.

All **17 requested SID/demo references remain OWNER-SUPPLIED**. HVSC #85 metadata
establishes 14 exact SID paths; Last Party's HVSC version is D500, not D420. No requested
reference media was acquired. Wonderland XIV is a four-side D64 production; no clear
redistribution grant or current VICE compatibility was established. SID discovery
still does not establish PSID/RSID playback: a validated SID-player route remains
future product work. Safe USB import remains pending the constrained broker.

120 product tests and 44 Menu tests plus the launcher checker pass. Actual admitted
source/subset hashes, deterministic preparation and small-directory staging verified.
Mac routing median: 0.058 ms warm / 25.2 ms new process plus registry; not a Pi budget.
[Validation](docs/runtime/optional-software-validation.json),
[performance](docs/runtime/optional-software-performance.json),
[future application physical procedure](docs/qualification/optional-applications-procedure.md).

Product branch: feature/1.1-build-foundation. Menu: feature/1.1-debian-package.
Menu source commit: `9f74202986ed16fde9f9b1f9da8cace70e784b72`.
Exact output refs/bundles are recorded in the verified external checkpoint
`archive/optional-content-2026-09-16` under the configured bulk workspace.
Retained inputs: `inputs/optional-software-2026-09-16` (input fragment, not a full lock);
original source review: `inputs/optional-software-review-2026-09-16`.
Prior checkpoints and POC1–3 remain immutable. Independent backup/custody unresolved.

**Next owner action:** review this addendum, then authorize first-boot/owner-account
and runtime activation integration in Linux staging, including matching versioned
packages and these optional-content contracts. SID/PSID/RSID dispatch, safe import
and service/modem gates require implementation/qualification; no new architecture
study. Do not automatically build POC4, test hardware, enable services or publish.

## Configuration maturation complete — 2026-09-16 / STOP

The final concentrated Menu/configuration architecture pass is source-complete.
[User guide](docs/runtime/pcbm-config.md), [implementation and activation contract](docs/runtime/configuration-contract.md),
[checkpoint/results](docs/runtime/configuration-maturation.md).

CONTROL opens the coherent Bash/dialog pcbm-config. Nine shallow task areas separate
normal settings, System Information, About and Advanced. pcbm-info JSON remains the
information authority. Registry/default preferences and POC3 launcher/geometry are
preserved. Terminal is a returning child shell; dead QUIT and competing legacy startup,
status/version, generic USB mount and broad service paths are retired. Audio settings
are parsed as data and saved atomically, not sourced as shell.

Product now implements schemas, unprivileged JSON client, fixed validated root adapters
and separate authenticated owner/raspi-config dispatch. Normal UI never asks for broad
sudo; owner administration uses a separate initialized account and ordinary authenticated
sudo. No root helper/policy/sudoers/account or service was installed in this source pass.

**Pending runtime activation:** matching versioned packages, first-boot owner credentials,
trusted helper/policy setup, NetworkManager and each service's explicit readiness.
Boot intent still needs its session consumer; typed TCPser settings need a fixed launch
adapter; safe USB import needs the constrained broker defined in the contract. These
are pending implementation/integration gates, not claims of working runtime features.
Services remain off/masked in POC3. No new image/package, VM start, Pi test or publication.

108 product tests, 43 Menu tests plus the launcher checker pass. Schema/syntax/link/
privacy/size/tag checks and sudoers syntax pass. Mac fixture timings are retained;
real dialog, Linux installation/account/service behavior and Pi performance are untested.
POC1–3 artifacts and historical evidence remain unchanged; all existing tags are intact.

Branches: product feature/1.1-build-foundation; Menu feature/1.1-debian-package.
Menu source commit: `87a16af19e7329b7cf8dbc16ee9420613f35245f`.
Recovery: configured bulk workspace archive/configuration-maturation-2026-09-16,
with exact source commits/ref inventories, both bundles and verified offline restoration.
Preservation report: qualification/configuration-maturation-2026-09-16/preservation.json.
Prior checkpoints remain immutable; independent backup/custody is still unresolved.

**Next owner action:** approve first-boot/owner-account and runtime activation integration
in a disposable Linux staging target. Complete exact package/dependency/authentication/
network/service gates and the required storage/modem/boot consumers before a later
explicitly approved candidate. No more Menu framework/architecture study is recommended.
Do not automatically build POC4, change POC1–3, enable services, optimize boot, include
optional software, test another Pi or push. Earlier sections below are historical
completed checkpoints and do not replace this current state.

## System Information and machine consumers complete — 2026-09-16 / STOP

Menu source commit: `4feda57c2ff1f5d0807a6873c0b88b5d84435bd8` on
`feature/1.1-debian-package`; product stays on `feature/1.1-build-foundation`.

Read the [source checkpoint](docs/runtime/information-machines-slice.md),
[user workflow](docs/runtime/information-and-machines.md) and
[consumer contract](docs/runtime/information-machines-contract.md).

CONTROL now has a read-only System Information view consuming pcbm-info JSON. MACHINES,
RUN, cover selection and the shared content default use the product registry/preferences.
Missing user state imports a validated legacy default once; valid new state wins.
Malformed state is preserved with explicit backed-up recovery. No sudo to choose a
default. Boot preference remains inactive; dormant pcbm-start migration is deferred.

86 product tests and 26 Menu tests plus the launcher checker pass. Syntax/schema/link/
privacy/size/ref checks pass; source/fixture Mac timings are recorded, not Pi budgets.
No real dialog/Linux installation or new physical qualification. POC1–3 and all existing
tags remain unchanged. No VM start, package/image build, POC4, service change or push.

Recovery: configured bulk workspace `archive/information-machines-2026-09-16`, with
exact commits/ref inventories, both bundles and verified offline restoration. Earlier
checkpoints remain intact; independent backup/custody is still unresolved.

**Next owner action:** review this slice, then authorize the bounded About/current-status
cleanup described in the checkpoint. Broader CONTROL/settings work and any future
package/image/hardware work require their own scope. The preceding foundation and POC
sections below are historical completed checkpoints, not the present consumer state.

## First runtime foundation slice complete — 2026-09-16 / STOP

Owner-approved boundaries now have their first bounded source implementation:
[checkpoint](docs/runtime/foundation-slice.md), [user guide](docs/runtime/pcbm-info.md),
[JSON information contract](docs/runtime/info-contract.md), and
[user preference/profile contract](docs/runtime/preferences.md).

- `runtime/bin/pcbm-info` is read-only, standalone and independent of dialog: human
  output or schema-1 JSON separates built identity, running hardware and current state.
  Missing data is explicit; no network probes, secrets, daemon or Python runtime extras.
  Optional active display mode uses the already-present engineering DRM helper only.
- User-owned typed preferences use XDG config, private permissions, validation, locking,
  atomic replacement and explicit malformed-data recovery. Reads never create state.
  **Not yet wired into the existing Menu/boot consumers**; no automatic legacy import.
- Eleven-profile registry now supplies info/preference validation. Existing Menu/
  launcher mappings remain unchanged until a targeted compatibility migration.
- Menu's opt-in Bash/dialog library defines selection/Cancel/Back/error/result contracts;
  no broad menu reorganization or privileged backend was implemented.

75 product tests (35 new), 10 Menu UI tests, the existing launcher checker and 24
per-file Bash syntax checks pass. Python 3.14.5/Bash 3.2 on macOS; no native Linux
integration or hardware pass claimed. CLI median 43.56 ms, observed peak 21.64 MiB;
these are Mac measurements, not Pi 3/3A+ budgets. ShellCheck unavailable.

Product remains feature/1.1-build-foundation; Menu remains feature/1.1-debian-package
at `fa2e5d8ef46f20c18a7e9735beee1cd1ac5961e3`.
No package/image was built, VM started, POC4 created, services enabled or code pushed.
POC1–3 and existing tags are unchanged. Recovery checkpoint:
`archive/runtime-foundation-2026-09-16` under configured external bulk storage, including
both bundles, exact source identities, test/performance/preservation evidence and
offline restoration report. Prior checkpoints remain intact. Independent backup remains
unresolved; this checkpoint alone is not a second custody location.

**Next owner action:** review this source slice, then authorize the targeted information
view and machine-preference/registry consumer migration described in the checkpoint.
No broad configuration redesign, first boot, network/service implementation, optional
software, new image or additional hardware testing is authorized automatically.
The POC3 physical/audit results below remain the preceding completed checkpoint.

## POC3 physical pass and product audit — 2026-09-16 / STOP

**Exact POC3 passed the owner's bounded Pi 3B appliance/geometry smoke test.**
The [additive physical attestation](docs/qualification/poc3-pi3b-owner-report-2026-09-16.json)
supplements the unchanged planned/build records below. Boot/Menu, both VT directions,
x64sc/C64 rendering and corrected geometry/pillarboxing, keyboard, smoke/SID/video-input
PRGs, all three expected SID tones, joystick, D64, F10/Quit/return and reboot passed.
No new failure was reported. Other machines/models/PAL–NTSC comparisons, measured mode,
network/services/setup, broader persistence and clean-rebuild reproducibility remain
unestablished. POC1's precise cause and POC2's exact scaling component remain unconfirmed.

Seven owner photographs were inspected read-only and copied with verified hashes to
`qualification/poc3/pi3b-owner-report-2026-09-16/photos/` beneath configured bulk storage.
The adjacent `evidence.json` SHA-256 is
`f9aef329cf04fb37ef4b11cf7ced0198050625cd5e8368f2502f8985655de422`.
Originals at `/Volumes/TheBench/temp/0?-poc3*.jpg` remain unchanged. No images in Git;
still photos do not prove audio/movement/input transitions. POC3 raw/lock/package
identities remain exactly those in the completed build checkpoint below.

[Product audit and recommended work order](docs/design/appliance-audit-2026-09-16.md)
is the current design checkpoint, with linked Menu/framework, Combian/optional-software
and boot studies. Recommendation: retain familiar Bash/dialog, streamline CONTROL,
separate read-only pcbm-info from configuration UI and narrow product backends, consolidate
preference ownership, and measure boot before optimization. Concrete before/after
workflows cover fewer levels, duplicate actions, unsupported commands and safe saves.
StrikeTerm redistribution remains unverified; SID-Wizard inclusion is conditional on
exact release/license/source review. No optional software acquired or embedded.

POC3 is a suitable basic factory + bounded Pi 3B appliance foundation, **not a release,
beta/RC, all-model qualification or reproducibility proof**. No runtime changes, VM
start, POC4, other-model test, service/SSH enablement or publication occurred. Menu stays
unchanged at `5cf863312a62ac458d5f6c362a9e81b9d14ec20c` on feature/1.1-debian-package.
Product stays on feature/1.1-build-foundation. Documentation/JSON/link/content checks
and external preservation verification are recorded with the additive audit checkpoint:
`archive/poc3-pi3b-product-audit-2026-09-16` (manifest and offline Git restore report).
Earlier checkpoints are retained unchanged; no duplicated image archive is needed.

**Next owner action:** review the proposed boundaries/navigation and authorize one
bounded next implementation slice. Suggested first slice: read-only pcbm-info plus
shared UI/result and preference contracts, then separately approved offline setup and
narrow privileged operations. Do not infer POC4/build or broad modernization approval.
Independent custody/backup, signing/SBOM choices, measured budgets, historical input
closure/build-chain gaps and independent clean rebuild remain unresolved.

The sections below are completed historical checkpoints, not current status or authorization.

## Completed POC3 build checkpoint (before physical test)

**Private POC3 built and offline-validated; physical POC3 remains UNTESTED.**
[Completed build record](docs/build/private-poc3.md), [exact results](docs/build/private-poc3.json),
[presentation policy/findings](docs/build/poc3-design.md) and
[hash-bound Pi 3B procedure](docs/qualification/poc3-pi3b-smoke-test.md) are the current
checkpoint. The [planned physical matrix](docs/qualification/poc3-pi3b.json) has no passes yet.

POC2's Pi 3B core launch/audio/media/return/VT/reboot passes and geometry failure
remain unchanged. POC3 seeds per-chip true aspect + desktop fullscreen once, preserves
saved user preferences and adds bounded presentation/DRM diagnostics. Menu/TCPser,
first boot, tty/getty/PAM, F10/menu/Quit, privileges, service masks and media remain
unchanged. No SSH. Root cause is still unconfirmed: software reference geometry works;
actual Pi/SDL/KMS/display scaling needs the new physical evidence.

- Integration: `0a0e271d86c68a969d8b18189c561ed51a8b0e09`.
- Lock: `inputs/frozen-poc3-final/release-lock.json`, SHA-256
  `3f3180f50e5c990ad63fc3d564a56bbd86b80f9b38c6a4aff7b42ed9438b9f5e`.
- Raw: `artifacts/private-poc3/2026-09-16-project-cbm-1.1.0-poc.3-lite-private-poc.img`,
  3,095,396,352 bytes; SHA-256 `9a8b1e0465c93981dfa6b09772e9e3fbf5c487a915bba0046b5de034f9331f33`.
- XZ: `artifacts/private-poc3/image_2026-09-16-project-cbm-1.1.0-poc.3-lite-private-poc.img.xz`,
  596,947,568 bytes; SHA-256 `e7d9657bfbb1124b38c2f1f3479698e24a34be7234db80d766f189da946ace3c`.
- VICE: `3.10-1+pcbm3`, SHA-256 `c9d798a591c22faa9ffc3141b7f5177ece36a05e53d9d2c8aae1ce93c22fcfbe`.
  Menu `v1.1.0_poc2` / peeled `897cee7c792b11bfed80168a576f263340f5f57d`, TCPser
  and original MIT media are reused exactly; all identities are in the build record.

40 macOS/native Linux tests and Menu launcher tests passed. 12 software-reference
cases cover 11 profiles plus PAL/NTSC; saved preferences/CLI precedence passed.
85 read-only image checks, filesystems/systemd units and 113 ELF dependencies passed.
2,789 frozen objects and raw/XZ agreement verified. 5,503 POC1/POC2 baseline files
and the original 1,677-entry historical manifest remain unchanged. POC2 photographic
evidence references/hashes remain in its formal record, not embedded in Git.

An initial assembly was rejected for builder inventory drift from inherited automatic
APT updates. Its old lock/artifact/log remain separate, **not accepted for flashing**.
The corrected lock retains the exact host supplement; before/after inventory guards
and masked builder update units now prevent accepting that drift. These are builder-only
controls, not changed appliance service policy. See the build record for limitations.

Bulk locators above are relative to configured ProjectCBM-Work. Recovery:
`archive/milestone1-private-poc3-2026-09-16`; detailed evidence: `qualification/poc3`.
Builder is stopped. Product remains `feature/1.1-build-foundation`; Menu remains
`feature/1.1-debian-package` without changes. Nothing published. Independent backup,
clean rebuild, acceptance budgets and full settings UX remain unresolved.

**Next:** owner review, then exact-hash Pi 3B geometry + bounded regression test.
If geometry fails, collect diagnostics and stop without manual repair. No physical
test by this task, POC4, other model, SSH or broader modernization. The completed
POC2 sections below are prior checkpoints, not current authorization/status.

## Completed POC2 review

Updated 2026-09-16 — **POC2 physical Pi 3B smoke test completed; geometry defect remains.**
[Formal physical results](docs/qualification/poc2-pi3b.json) and
[aspect-ratio investigation / narrow POC3 proposal](docs/qualification/poc2-pi3b-aspect-analysis.md)
are the current qualification authority. Boot/Menu/input, diagnostic VT in both
directions, RUN/x64sc, C64 rendering and observed stability, keyboard, F10 menu,
Quit/return, PRG, original SID tones, video/input program, D64 and basic reboot
passed. **Correct aspect-ratio preservation FAILED:** horizontal widescreen stretch.
Joystick was unavailable. Other profiles/models, PSID/RSID, broader configuration
persistence, first-boot interruption, services/setup and clean-rebuild reproducibility
remain UNTESTED. No full model/release qualification follows from this bounded test.

The [completed build checkpoint](docs/build/private-poc2.md) and
[exact artifact results](docs/build/private-poc2.json) remain unchanged historical
build evidence. No POC2 image, lock, package, media or POC1 record changed. VM remains
stopped. No runtime fix, POC3, additional-model test, networking, release or push.

POC1 remains immutable: Pi 3B boot/Menu/input PASS, x64sc display/console recovery
FAIL, later VICE qualification UNTESTED. All 2,731 baseline files, including the
[physical record](docs/qualification/poc1-pi3b-2026-09-15.json), rehash unchanged.
Its physical cause remains unconfirmed. POC2 adds explicit GL runtime, standard
getty/login/PAM tty1, unprivileged shared RUN/content/F10-menu-quit behavior, bounded
persistent diagnostics, non-root tty2 and original declared media. Full settings/
privilege UX remains deferred; masked services are not failures. No broad sudo.

- Integration: `2b894ad187f0b603d2e0c9965aba242073e2cb90`.
- Lock: `inputs/frozen-poc2/release-lock.json`, SHA-256
  `bc1c6e16c32d6285973933b8d50371899bc18e5407dd654c9a14d1187eb194ac`.
- Raw image: `artifacts/private-poc2/2026-09-16-project-cbm-1.1.0-poc.2-lite-private-poc.img`, 3095396352 bytes,
  SHA-256 `ef221dc09ea65d3976f88e65cde8f153a9c32989be09c6b35d545b111ccb7467`.
- XZ image: `artifacts/private-poc2/image_2026-09-16-project-cbm-1.1.0-poc.2-lite-private-poc.img.xz`, 596406680 bytes,
  SHA-256 `757aca812835c676d75eaad651b6739fc79461c25c8aa7426524f6692a6b3d9f`.
- Menu input: `v1.1.0_poc2`, peeled `897cee7c792b11bfed80168a576f263340f5f57d`,
  package SHA-256 `e29bc3598f3be0869f79184250f88a03f4c59f1304a20a428223bac58c97bd11`.
- Original MIT media: source `14e4ade77ec83e0429d194a6b5ecfa5ef7655e75`,
  bundle SHA-256 `61673c45058ba31d2e28c699c631e99173c4e44b8b49c82c83735c2c5614d0af`.

Paths are relative to configured bulk storage, currently TheBench/ProjectCBM-Work.
34 macOS/native Linux tests, shared Bash launcher tests, 79 image checks, read-only
filesystem/unit checks and 112 ELF-object closure checks passed. All 2,738 retained
objects rehashed, XZ/raw agree, historical 1,677-entry manifest and existing tags
are unchanged. Reference software-rendered VICE checks demonstrate original-media
loading/execution and generated SID samples, not physical audio/input/graphics.
Supported no-color stdout logging avoids a reproduced VICE 3.10 logger crash; this
does not retrospectively diagnose POC1's physical failure. Exact limitations and
package/source/build identities are in the checkpoint above.

Current branches remain product feature/1.1-build-foundation and Menu
feature/1.1-debian-package. Later validation/continuity commits do not alter frozen
input identities. Final Git bundles/ref inventories and offline restore evidence:
`archive/milestone1-private-poc2-2026-09-15`; detailed evidence: `qualification/poc2`.
Independent encrypted backup remains unresolved. Existing historical/preservation/
POC1 checkpoints are untouched.

**Investigation:** the frozen image has no VICE geometry configuration/arguments;
upstream 3.10 nevertheless defaults to per-chip true aspect mode (2). Historical
v1.0 has explicit window sizes/filtering, but no explicit aspect/fullscreen setting.
Leading hypothesis: implicit windowed KMS mode selection plus downstream scaling;
actual renderer/mode/resource capture is missing. Do not claim adding mode 2 alone
fixes it. Prefer true per-chip aspect + explicit desktop-resolution fullscreen,
with bars where needed, without hard-coded 4:3 or HDMI-resolution hacks.

**Next:** owner authorization for a narrow POC3 geometry/defaults/measurement change,
new frozen candidate and offline validation, followed by owner Pi 3B geometry and
regression testing before other models. STOP pending that decision. Full settings/
privilege redesign remains deferred. Four owner-supplied photos are now retained
and visually reviewed under `qualification/poc2-pi3b-photos-2026-09-16`, with
per-file hashes/captions in the formal physical record. They corroborate visible
C64/media output and stretching; no diagnostic reports or confirmed cause. All
result classifications and frozen candidate identities remain unchanged.

This review's small evidence is under `qualification/poc2-pi3b-owner-report-2026-09-15`;
additive Git recovery/ref/offline-restore checkpoint:
`archive/poc2-pi3b-review-2026-09-15`. Earlier checkpoints retain their original
meaning. Photo-supplement source recovery: `archive/poc2-pi3b-photos-2026-09-16`.
This top section supersedes older physical-pending statements below.

## What shipped

| Item | Verified baseline |
| --- | --- |
| Product | Project CBM v1.0.0, original Trixie console appliance |
| OS/base | Raspberry Pi OS Lite 64-bit, Debian 13.4 Trixie; 2026-04-21 reference, pi-gen `4ad56cc850fa60adcc7f07dc15879bc95cc1d281`, stage2 |
| Kernels | arm64 vendor 6.12.75 v8 and 2712; no device EEPROM qualification implied |
| VICE | Source-built 3.10 SDL2 under /usr/local, direct ALSA; retained build output matches installed x64sc |
| TCPser | 1.1.6_beta, retained checkout `fe7feff4862406b277e009d14c219f5d16cf1222`; full integration unqualified |
| Menu shipped | Exact 17 scripts recovered at `a4148db54001790eaddb4e31104917c16149b181`, annotated `recovered/image-v1.0.0-runtime` in companion repo |
| Formal Menu | Existing v1.0.0 peels to `399c6158caa8ed2762744d512c1841b94ad64403`; 12 script matches, five differences, extra experimental screenshot helper |
| Source lineage | Historical v6.1/v6.3/v6.4 -> v6.5/GoldMaster/for65. v6.5 source equivalence is not byte identity or a full installed configuration snapshot |

[Provenance and hashes](docs/provenance.md) distinguish fact, inference and unknown.
No known Bookworm generation exists. No pre-existing Menu commit matches all
shipped bytes; the new root recovery commit records recovery, not invented ancestry.

## Development and maintenance

- Canonical main fast-forwarded 26 commits each: product `46fbf47` -> `493229c`;
  Menu `f185d91` -> `b7e4d85`, followed by local continuity commits. Full IDs and
  preservation records: [provenance](docs/provenance.md).
- The eight unpublished preservation/continuity commits received an owner-authorized
  metadata-only privacy repair. Current refs and verified replacement bundles are in
  [privacy reconciliation](docs/privacy-reconciliation-2026-09-15.md). Both main branches and Menu recovery/maintenance refs are published. Product
  maintenance/1.0 remains intentionally local/bundled; public product v1.0.0 is the
  authoritative maintenance baseline. GH007 rejected new branch creation because
  of historical commit email metadata; do not retry, rewrite v1.0.0 or weaken privacy.
  GitHub release assets are unchanged.
- Product maintenance/1.0 starts at immutable product v1.0.0 `46fbf47d66596b2f3d0f6ab53d26bdd90632c73c`.
  Menu maintenance/1.0 starts at the exact recovery commit above, not formal Menu
  v1.0.0. It contains scripts and provenance only, not an installable image recipe.
- 1.0.x = original Trixie generation, important/security fixes only. 1.1.x = current
  Trixie reproducible-build/modernization generation. No 1.0.1 exists or is approved.
- Work from short feature branches off main when 1.1 is authorized. Repository
  separation, immutable releases, explicit input pins and Pi 3 floor are protected.

## Qualification and known problems

Goal: Pi 3B/3A+/3B+, 4B/400, 5/500/500+ where technically supportable. Pi 3 is
the performance floor; 3A+ needs a separate 512 MiB memory qualification. The
historical audit did not qualify hardware. Exact POC1 failed x64sc/console recovery;
exact POC2 now passes bounded Pi 3B emulation/return/audio/media checks with an
aspect-ratio failure. This is not full model qualification; other models and
performance budgets remain unqualified. See [testing](docs/testing.md) and the new physical record.

Verified static/integrity checks cover image hashes, runtime extraction/lineage,
Git preservation and individual Bash syntax. They do not qualify boot, graphics,
audio, controllers, IP232, USB/NVMe or cloned identity behavior.

Known issues are cataloged in [security](docs/security.md): baked identity/SSH keys,
cloud-init and builder residue; broad sudo; TCPser default mismatch; inconsistent
Samba service policy; USB import safety; non-idempotent installer; writing docs-sync
dry run/deletion risk; version-display and CI/version mismatch; source/release
divergence; PiShrink/manual build limitations; content/license provenance gaps.
Current guidance is corrected in [v1.0 notes](docs/v1.0-current-notes.md); no runtime
fixes were applied. Historical audit/release notes/assets/checksum bytes are preserved.

## POC1 direction and next task (historical; superseded above)

Keep the console Bash/dialog -> SDL2 VICE -> ALSA appliance, with product-owned
integration and an independently versioned Menu. ADR-0001 selects writable ext4
with logical system/user-data separation, existing
content paths, external component .deb builds and backup/reflash/validated restore.
No mandated 8 GB minimum: measure footprint, initialization/maintenance margin and
free user capacity. Separate USERDATA and immutable roots are deferred.

Milestone 1 reached its first controlled-build checkpoint on
`feature/1.1-build-foundation`. The image uses integration commit
`024db4985202ef0675b12e12b8982af91c6d6ad3`; later validation/docs commits do not
change its frozen identity. Menu packaging is on `feature/1.1-debian-package` at
`77a708019c9d8a11e657d7e5d2dde7b7ecb340ba`, local annotated `v1.1.0_poc1`.
Both published main branches and existing release/recovery tags are unchanged.

Real lock: `inputs/frozen-poc1/release-lock.json` under the configured bulk root;
SHA-256 `703aa6e1b0d278262a2dc83c31740b3c589788e3953e3ac822e948133529d566`.
Private raw/XZ and records: `artifacts/private-poc1`. Raw SHA-256
`ae8d2032736e1d3ae2e49d4370aa62d00fc06f9fc567e70e400491900d45bf9f`;
XZ SHA-256 `b9adaaa55a7543441607fc90f7651cc35588f9c024e8a160110d857919ef2a06`.
26 macOS/Linux tests and 50 offline image checks passed at construction. Physical
Pi 3B boot/Menu now passed; x64sc display and console recovery failed. First-boot
expansion/identity measurements and later VICE qualification remain UNTESTED.
This is a controlled build, not reproducibility proven.

Read-only analysis found missing desktop GL runtime (v1 used the OpenGL renderer),
a direct tty service without the previous PAM/login session, and differing kernel/
Mesa stacks. SDL has a GLES fallback, so no root cause is confirmed without runtime
logs. POC1 raspi-config calls also lack an authorization path; this is a separate
setup UX gap, not a failure of intentionally masked services. The required 1.1
setup UX is offline-capable with narrowly authorized operations, not broad sudo.

Next: owner review of the bounded POC2 proposal and authorization before fixes,
engineering diagnostics, media creation or rebuilding. Do not modify frozen POC1,
restart the builder, modernize broadly or publish anything. Product remains on
feature/1.1-build-foundation; Menu working branch is feature/1.1-debian-package at
99063f8299192877f7d17d0ccd9635f135b89fdc (the frozen POC1 input stays the earlier
77a7080 commit above). This analysis changes product documentation/records only.
Both retained raw-image hashes were reverified; inspected package/launcher payloads
match the frozen image. Documentation JSON/local links/diff and immutable-tag
checks are recorded in the analysis checkpoint; no physical rerun was performed.
Private detailed comparison and additive source checkpoint are retained under
qualification/poc1-pi3b-2026-09-15 within the configured external workspace.
Earlier build/recovery checkpoints remain unchanged; no image is duplicated.

### Black-box recovery requirement

Read [recovery](docs/recovery.md) for scenarios A–H, historical confidence levels,
portable storage, independent backup/restore and acceptance tests. A future developer
must recover the product from CBM repositories/retained artifacts alone, without old
sessions, the original Mac or reference projects.

Full project recovery belongs in repositories and retained build/release infrastructure.
1.1 carries only minimal `/usr/share/project-cbm/identity.json`, generated from the
same frozen lock: product/Menu/VICE/base/TCPser mapping, integration/build ID and config
schema identity, with external provenance lookup. The generator is implemented; its 1,443-byte output is installed and verified
offline in the private POC. No full lock, recipes, schema corpus,
archives or package closure merely for recovery in the appliance. Proposed pcbm-info
reads E; it is not implemented. Final image hashes/qualification stay external to
avoid cycles. A final manifest hashing the image cannot have its digest embedded in
that image; use a predecessor digest/build-ID lookup. JSON worksheet is design-only.

The accepted preservation bundles were restored into fresh mirrors without GitHub:
all 5 product refs, 8 Menu refs and 17 recovered script hashes matched; fsck passed.
Owner accepted repository-only cold-start comprehension on 2026-09-15. Offline 1.1 identity now passes on the private image. An independent clean Linux
rebuild and independent-medium restore remain unperformed. Host-only schema/privacy negatives pass using synthetic fixtures. Read-only lessons from Spitfire/FireComm/CircuitNET are summarized in recovery.md; CBM does not depend
on them. Spitfire's migrated reference copy has missing tools.

Current local paths are deployment choices, not architecture. Independent encrypted
backup/custody, Linux bootstrap environment, signing custody and standard SBOM format
remain open. At that earlier checkpoint no infrastructure was provisioned. The earlier design checkpoint remains
separate from the sealed preservation archive. The additive privacy-reconciliation
checkpoint now retains all eight replacement commits, including the architecture
work, with full offline restore checks. See its record for subsequent checkpoint phases.

## Evidence and storage

- Original history (read-only by policy): `/Volumes/TheBench/Projects/Project CBM`.
- New bulk work: `/Volumes/TheBench/ProjectCBM-Work/{inputs,packages,builds,cache,artifacts,qualification,scratch}`.
- Durable inventory/Git snapshots/recovery: `ProjectCBM-Work/archive/preservation-2026-09-15`.
- Additive design checkpoint/bundles: `ProjectCBM-Work/archive/black-box-design-2026-09-15`.
- Original assets/extraction: `ProjectCBM-Work/archive/audit-2026-09-14/workspace`.
- [Reconciled audit](docs/audit-2026-09-15.md); original report retained externally.

TheBench is ~2 TB APFS with ~1.13 TB available at preservation time. Check actual
space/mount before work. The approved guest supplies ext4 in its external sparse disk. One device is not an
independent backup; owner review of a second encrypted backup destination remains.
Unknowns: original base-XZ identity/full input lock, complete raw-to-shrunk command
chain, VICE upstream tar provenance/patch state, content licenses and all physical
qualification. Public availability/credential remediation and any new release need
separate owner review. These do not prevent starting an explicitly authorized POC.

## Final architecture phase checkpoint (historical, pre-rewrite IDs)

Inputs: product main `7f9c4a363cf19154a9637ed8b251049bf23723e0`; Menu main
`c3746a12e6146f880c49979df8da2a3567200924`. Both began clean. Exact historical release,
Menu recovery refs and rehashed bundle locators are in [provenance](docs/provenance.md#recovery-bundle-locators-and-digests).
Research dated 2026-09-15 is cited in ADR-0001; it is not a future release input lock.
Current policy now distinguishes project recovery, minimal installed identity,
reproducible builds and disaster recovery. Roadmap and user-facing content/service/
credential/hardware guidance are reconciled; historical evidence is not rewritten.

Validation and exact commit lookup are recorded in [phase validation](docs/architecture-phase-validation.md).
No builder, Linux provisioning, packaging, runtime/first-boot change, image, push or
release. Stop after documentation commits. Independent backup/custody, Linux bootstrap,
signing custody, SBOM format, measured acceptance budgets and historical 1.0 input/
build-chain gaps remain open. Implementation is the next separately authorized task.

## Milestone 1 pre-approval checkpoint (historical)

Contract implementation commit: `e4d1556` (resolve full ID in Git); later design/handoff
commit follows on the same local feature branch. Feature work is not pushed or merged.
The 15 host-only tests passed, including published tag identities, strict JSON/schema
validation, malformed/missing pins, safe locators, minimal-identity projection and
workspace refusal cases. No physical Pi, Linux capability or real input-closure pass
is claimed. The old worksheet remains visibly historical and fails lock validation.

Current source recovery is additive under archive/milestone1-contracts-2026-09-15;
its checkpoint.json and separate SHA-256 identify the final branch tip, bundles,
validation/research/test-dependency artifacts and exact next step. Read its README
after verifying the catalog. Published synchronization bundles remain under
archive/privacy-reconciliation-2026-09-15/published, checkpoint SHA-256
`6ff18bafcc57a7e054a22fff66efedd3618ea6bd1a6f9dedf2c6d1bacdbc255c`.

Recommendation awaiting approval: Lima/VZ plain arm64 Debian VM, 8 vCPUs, 12 GiB RAM,
160 GiB sparse ext4 disk on TheBench, explicit external download/cache placement.
UTM is the main alternative. Approval must precede host installation/provisioning;
exact bootstrap/input pins and actual Linux capability tests remain future work.

## Milestone 1 approved host checkpoint (historical, before package work)

Lima 2.2.0, source `de0816ea4bdc5267b428ab21025889b8dd785526`; pinned dated
Debian cloud bootstrap and checksums in build/host/inputs.json. Instance `cbm` is
running on VZ, plain mode, no host mounts/container platform. Disk and state:
`ProjectCBM-Work/build-host/lima/cbm/disk`; cache: `ProjectCBM-Work/cache/lima`.
Actual root is ext4; Debian 13 kernel `6.12.95+deb13-cloud-arm64`. The guest is
infrastructure, not Raspberry Pi qualification or a release base image.

20 host tests passed. Full loop/partition/ext4/mount/chroot/device/xattr tests,
APT HTTPS/authenticated metadata/install/remove/source, Git acquisition and 1 MiB
bidirectional SSH/rsync hash test passed. Two probe defects (admin PATH and xattr
read permissions) were corrected; original failed logs retained. APT export excludes
transient lock/partial files after initial permission errors; important inputs were
catalogued. No host capability workaround was needed. All details and limitations:
[capability record](docs/build/lima-capability-2026-09-15.md).

Retained bootstrap inputs: `ProjectCBM-Work/inputs/build-host/`; 82-file inventory
and raw private infrastructure logs: `ProjectCBM-Work/build-host/records/`.
Next: retain and select exact pi-gen arm64/VICE/Menu/TCPser inputs and package-build
closure, then implement the smallest locked POC factory. Do not claim a frozen real
release lock, complete source/package closure, image, reproducibility or hardware pass.

## Private component packages and retention work (historical, before input freeze)

Successful private Debian candidates retained under `ProjectCBM-Work/packages/poc1/`:

- VICE `3.10-1+pcbm1`, arm64; SHA-256
  `674c40040965b689d08cdc225f8954c0fb2433ef68459f51aa7f6360b1710d20`.
- Menu `1.1.0~poc1-1+pcbm1`, all; SHA-256
  `3f7557cdbdd44922954a6e640a1bcb3a96f446f6dbe6631afe667aa5e5d5f0fd`.
  Companion feature/1.1-debian-package at `77a708019c9d8a11e657d7e5d2dde7b7ecb340ba`;
  local-only annotated v1.1.0_poc1 object `e265f3cbb995ad0a9a7748987b2d9c88019aa787`.
  Formal and forensic tags/main are unchanged. Menu packaging relocates required
  command paths to /usr/bin and excludes release-prep, screenshot and unreviewed art.
- TCPser `1.1.6~beta-1+pcbm1`, arm64; SHA-256
  `8b8f8a4f3ec98dddf5bdb347320dad05e1bbe5230e0ee2727248c247a5af584f`.

Exact source selection is in build/inputs-poc.json (NOT a frozen release lock).
pi-gen arm64 `6fcca44892d5d4b36f826d2b8fb16d716369fada` and TCPser
`fe7feff4862406b277e009d14c219f5d16cf1222` sources/bundles are externally retained.
VICE needs dos2unix, xa65, SDL2-image and evdev development dependencies; those
configure findings are now in the recipe. Out-of-tree compilation avoids source
contamination; native CPU optimization is explicitly disabled. Build logs and .dsc,
source archives, .buildinfo, .changes and debug .debs are retained outside Git.

Pinned pi-gen stages 0/1/2 completed in an input-resolution-only run with all image
exports disabled. No final appliance has been constructed. Resolved base is Trixie
13.7 with raspberrypi-sys-mods 1:20260914 and vendor kernel metapackages
1:6.18.50-1+rpt1. Actual vendor early resize hooks require the `resize` kernel argument;
first-boot draft removes that argument and coordinates one explicit growth owner.
Full source/host package retention and a frozen replay-capable input kit remain in
progress. Seventeen old bootstrap .deb versions were absent from today's indexes;
exact-version Debian snapshot recovery is underway, without upgrades/substitution.
Inspect newer dirty scripts/state and build-host/records before resuming. Next:
complete/verify retention, freeze real lock, review/test integration and first boot,
then one private image and offline validation. No publication or physical Pi test.

## Frozen factory implementation checkpoint (historical, before first image)

26 contract/retention/geometry tests pass on macOS and native Debian, with no skips.
The initial Linux test copy omitted a worksheet and Git refs; the complete copy now
passes. This was a test setup error, not a required Linux capability failure.
Exact old host binaries (17) and sources (10) were recovered via Debian snapshots.
All remaining runtime source acquisition completed, with explicit libftdi1 source-name
reconciliation. Unneeded rpi-connect-lite is excluded before construction because its
source entry was unavailable; original failed discovery records remain unchanged.

The minimal factory is in tools/{freeze_poc_inputs,retained_inputs,construct_poc,
install_poc_stage}.py and [integration notes](build/pigen/README.md). A frozen kit
contains content-addressed direct inputs and nested source/package/metadata catalogs.
Source .dsc SHA-256 payload lists and actual .deb identities are checked. Final assembly
runs with loopback-only networking and frozen APT transport; absent inputs fail closed.
Two explicit pi-gen patches exclude Connect and prevent export-time user rename/
package upgrades. They do not rewrite upstream history or bypass APT authentication.

Private POC policy: local pi console Menu, locked passwords, no broad sudo, no baked
credentials; SSH/Samba/TCPser/Avahi/NetworkManager disabled. Binaries are installed,
but network configuration and privileged Menu controls remain incomplete. No cover
art/private historical content is imported. First boot owns root growth and seeds
user state; pure geometry tests pass, actual first boot remains physically untested.
Next: commit this input recipe, archive that commit, freeze/verify/export the real kit,
construct one private image, validate offline, retain results and STOP for owner review.

## Final POC1 recovery checkpoint (historical)

`ProjectCBM-Work/archive/milestone1-private-poc1-2026-09-15` is the additive current
checkpoint: README, checkpoint.json plus SHA-256, both full Git bundles/ref lists,
offline mirror restoration/fsck results and validation/remote-ref records. Its exact
final branch tips are recorded externally to avoid a self-referential commit hash.
The frozen kit has 2,697 rehashed objects; images and component artifacts remain in
their existing external locations, without duplicating historical images.

Original historical manifest verifies all 1,677 entries unchanged. Both formal v1.0.0
tags, Menu recovery refs and published main refs are unchanged. Product maintenance/1.0
remains local/bundled. Independent encrypted custody remains unresolved; a second
folder on TheBench is not an independent backup. Current VM is stopped, not deleted.
