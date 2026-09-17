# Working on Project CBM

## Current owner scope: POC4 attempt #3 physical-regression investigation

POC4 attempt #3 construction and offline validation are complete. The frozen
candidate, release lock, packages, images, checkpoints and exact-hash physical
procedure are immutable qualification evidence.

The owner has physically tested the exact POC4 attempt #3 image on Raspberry
Pi 3B and observed new qualification results that supersede the previous
"physically untested" state.

Current owner-reported observations include:

- first boot fundamentally completed;
- first-boot pacing/feedback was poor enough that some transitions appeared
  hung;
- region/locale/Wi-Fi-country interaction was awkward and exposed technical
  input expectations;
- Back navigation did not reliably return to the previous first-boot step;
- Wi-Fi password entry gave no visible masked-input feedback;
- one attempted Wi-Fi password was rejected with an unhelpful error while a
  simple alphanumeric password succeeded;
- Midnight Commander launched successfully;
- SID-Wizard and StrikeTerm are present but are not yet functionally qualified;
- RUN launched the selected/default VICE machine;
- the expected Project CBM machine Cover was not visibly presented before VICE;
- VICE itself ran;
- F10 opened the VICE menu;
- Quit exited VICE and visually returned to the Project CBM Menu;
- after return, Project CBM keyboard input was non-responsive;
- Ctrl+Alt+F2 did not switch to diagnostic VT2;
- Ctrl+C did not respond;
- POC3 previously physically passed the complete Menu -> VICE -> Menu lifecycle,
  including responsive keyboard input and VT switching after return.

The missing Cover and post-VICE input/VT failure are priority regressions
against the intended lifecycle. The SDL2 Cover renderer is new in POC4 and is
a legitimate investigation target, but it must not be assumed to be the cause
without evidence.

The owner authorizes a bounded forensic investigation and correction of these
POC4 physical regressions.

Authorized work:

- record the new owner-reported physical qualification evidence;
- compare exact POC4 attempt #3 behavior/configuration/source with the
  physically known-good POC3 lifecycle;
- inspect retained POC4 engineering diagnostics and launch/session evidence;
- determine why the Cover was not visibly presented;
- determine why keyboard/VT ownership or terminal state was not restored after
  VICE exit;
- investigate whether the Cover renderer, launcher, SDL/KMS/DRM behavior,
  session/getty/PAM state, terminal cleanup, signal handling or another POC4
  change caused or contributed to the regression;
- reproduce relevant lifecycle behavior in safe host/native tests where useful;
- implement the smallest evidence-based source correction necessary;
- add focused regression tests for Cover presentation/cleanup and repeated
  Menu -> Cover -> VICE -> Menu lifecycle behavior;
- analyze the first-boot UX findings and implement bounded corrections for
  progress feedback, human-readable region/Wi-Fi-country choices, Back/Cancel/
  retry behavior, password-entry feedback and useful validation errors where
  evidence supports the change;
- update qualification, continuity and recovery documentation;
- prepare the next versioned package/input/candidate work required to
  physically verify the corrections.

Do not modify the frozen POC4 attempt #3 image, lock, packages or evidence.

Do not hide a lifecycle failure with retries, forced resets, broad privilege,
arbitrary VT manipulation or timing sleeps unless evidence establishes a
bounded timing requirement.

Presentation must not own emulator lifecycle. Cover failure must not prevent
VICE startup, and Cover cleanup must release all interactive/display resources.

One authoritative unprivileged VICE launch path must remain.

The corrected lifecycle must preserve POC3's known-good geometry, audio,
F10/Quit behavior and Menu return contract.

First-boot UX corrections must remain offline-capable, retry-safe and
appliance-oriented. Users should choose human concepts such as country,
keyboard and network rather than entering Linux implementation strings where
a safe selection can be provided.

Long-running first-boot/configuration operations must provide immediate,
truthful working-state feedback and bounded failure behavior so normal work
does not appear to be a hang.

Wi-Fi password handling must not expose credentials in logs, process
arguments, diagnostics or output. Do not weaken accepted NetworkManager or
credential-security boundaries merely to accept more passwords.

The recent Dosbian 4.0 analysis is design/reference input only. Do not copy
Dosbian code or reorganize Project CBM around Dosbian during this regression
milestone.

Do not implement the proposed MEDIA/TOOLS/POWER/recovery information-
architecture refinements yet. Preserve them as later Project CBM 1.1 design
input.

This scope does NOT authorize:

- mutation of any frozen POC1-POC4 candidate;
- broad Menu redesign;
- implementation of unrelated Dosbian-derived features;
- boot-presentation optimization;
- PSID/RSID playback implementation;
- testing another Raspberry Pi model;
- push;
- publication.

If the investigation establishes a correction requiring a new image, stop
after the corrected source, tests, package/input/candidate plan and recovery
checkpoint are ready for owner review.

Do not automatically build the next image unless a later current owner scope
explicitly authorizes that build.

Preserve all historical evidence, rights gates and recovery records.

Read CURRENT-STATE.md first, then docs/recovery.md, docs/architecture.md,
docs/provenance.md and docs/testing.md. Repository files are the continuity record; old Codex sessions
are not required. Update CURRENT-STATE.md after meaningful work, including exact
input/recovery refs, checks, unresolved issues and the next task.

## Ownership and protected decisions

- This repository owns the product/distribution: Raspberry Pi OS integration,
  image builder, release input mapping, VICE/TCPser/Menu integration, qualification,
  hardware policy, artifacts, release notes and public product documentation.
- Companion: ../project-cbm-menu (https://github.com/cdaters/project-cbm-menu).
  It owns independently versioned scripts, assets, interfaces, packaging and tests.
  Never consume arbitrary Menu main for a release: require version/tag, peeled
  commit and artifact SHA-256. See docs/build-and-release.md.
- Released 1.0.0 is already arm64 Trixie, not Bookworm. 1.0.x receives important
  and security fixes only; 1.1.x is the active reproducible-build generation.
- Pi 3 is the performance floor. Target Pi 3 through Pi 500+ where technically
  supportable; qualification is per model, not inferred from Raspberry Pi OS.
  Retain Bash/dialog, console boot, SDL2 VICE and ALSA unless evidence warrants review.
- Existing tags/history and release assets are immutable by policy. Never reset,
  force-push, retag or silently replace artifacts. Recovery refs are evidence,
  not release replacements. No 1.0.1 has been created.

- Full black-box PROJECT recovery is a repository/build/release-infrastructure
  responsibility. The image carries minimal installed identity only. The same frozen
  lock drives construction, minimal identity and external attestations; keep the
  acyclic checksum design in docs/recovery.md. No full lock/recipes/archives/closure
  in the appliance merely for recovery. Offline identity needs no boot/Menu/network.
- ADR-0001 accepts Raspberry Pi OS Lite + pinned arm64 pi-gen with selected appliance
  practices, writable ext4 and logical user-data separation for 1.1. Read
  docs/adr/0001-base-distribution-and-image-architecture.md before foundation work.
  Reopen only for its evidence-based triggers. No mandated 8 GB card minimum;
  measure footprint, first-boot/maintenance margin and free user capacity.
- Preserve rationale and evidence limits. CURRENT-STATE is the last completed
  checkpoint; inspect newer dirty work before changing it. Never erase unknown work
  to match a document. Reference projects are read-only learning material, not CBM
  recovery/build dependencies or sources of automatic authorization.

## Storage and security

- Canonical Git source/docs stay in ~/Code. Large images, inputs, packages,
  build trees, caches and qualification results belong under
  /Volumes/TheBench/ProjectCBM-Work. Check the mounted volume and space first;
  never silently fall back to the internal SSD. Use build-specific temp/cache paths.
- /Volumes/TheBench/Projects/Project CBM is original historical evidence.
  Do not modify, rename, normalize, deduplicate, clean or execute it in place.
  Manifests and Git bundles: ProjectCBM-Work/archive/preservation-2026-09-15.
- TheBench is APFS, unencrypted, case-insensitive, ownership disabled. A future
  Linux builder needs suitable Linux filesystem semantics. The approved Lima/VZ
  guest now uses an ext4 filesystem in an external sparse disk; see
  docs/build/lima-build-host.md and CURRENT-STATE.md for capability status.
- Historical images/logs may contain identity, private keys, credentials, history,
  build residue and unlicensed media. Record presence/type, never private contents.
  Do not commit/publish image extracts beyond reviewed original source. Historical
  preservation and public release artifacts are separate trust domains.
- Do not casually broaden sudo, networking, listeners, service defaults, boot,
  first-boot or installer behavior. Read docs/security.md before related work.
- Do not execute legacy installers, docs-sync (even --dry-run), release-prep,
  privileged image tooling or historical scripts as a documentation/static check.

Current source/storage paths above describe this operator's deployment. Future
build/recovery tooling must accept configured roots and relative artifact locators;
a replacement machine must not require /Users/cdaters or /Volumes/TheBench.
Independent recovery copies and restore drills are required; GitHub and caches are
not assumed permanent storage. See docs/recovery.md for current gaps.

## Checks and phase boundary

Run git diff --check, validate added JSON, check local links, inspect staged file
sizes and secret patterns, and use per-file Bash syntax checks for shell changes.
Follow docs/testing.md for focused behavioral and physical-device qualification.
Keep logical commits and leave a clear git status. Do not claim hardware passes
from static checks. Verify preservation manifests after preservation changes.

### Completed architecture phase (historical boundary)

Preservation and the owner-accepted cold-start review are complete. Final architecture
and documentation reconciliation are complete under ADR-0001. Metadata schemas/generator,
pcbm-info, first boot and independent backup remain unimplemented. The next milestone
is the Project CBM 1.1 POC in docs/build-and-release.md, requiring a NEW implementation
instruction. This architecture phase authorizes documentation/ADR commits only:
stop before pi-gen, Linux provisioning, packaging, runtime changes, image build or
publication. No push is authorized.

## Commit identity and current owner authorization

Use the contributor's GitHub-provided noreply identity when email privacy is enabled.
Before commits, check effective author/committer identity and repository-local
overrides; keep privacy protection enabled. Do not hard-code an operator email in
project tooling. Never repair published history. The 2026-09-15 owner exception
applied only to eight explicitly scoped unpublished commits and the dependent
unpublished Menu forensic tag; see the product privacy reconciliation record.

The owner has authorized Milestone 1 contracts/tests and build-host research, with
a hard approval checkpoint before Linux host provisioning, disk allocation, package
builds, pi-gen or images. The current identity-repair task authorizes its scoped
rewrite, additive documentation/checkpoints and normal publication only; stop after
verified pushes and offline recovery. Earlier phase-specific no-push/no-implementation
statements above describe those completed phases, not a substitute for current scope.

## Publication resolution and active milestone

Both main branches and Menu maintenance/recovery refs are published. Product
maintenance/1.0 stays local/bundled by owner decision: public v1.0.0 is the
authoritative public maintenance baseline. GH007 on the historical commit does
not authorize rewriting it, changing privacy settings or retrying that branch push.
The owner now authorizes resuming Milestone 1 on product
feature/1.1-build-foundation after synchronization/checkpoint verification. Complete
contracts/tests and retention/package/integration/first-boot design plus Linux host
research; STOP for the build-host options/recommendation checkpoint before installing
software, provisioning a VM/container/host, allocating large disks, building packages,
running pi-gen or building an image. No Menu feature branch without actual Menu work.

## Milestone 1 owner checkpoint (completed approval boundary)

Host-only input/identity/workspace schemas, validators, generator and tests are now
implemented on feature/1.1-build-foundation. See docs/build/contracts.md and
docs/build/milestone1-checkpoint.md for exact checks/remaining limits. Package,
integration-stage, first-boot and retention designs are documents only.
STOP pending the owner's choice in docs/build/linux-build-host-study.md. Do not
install/provision a Linux host, allocate disks, build packages, run pi-gen or build
an image until that approval arrives. Do not treat synthetic fixtures as real pins.
Do not retry product maintenance/1.0 publication; public v1.0.0 remains its baseline.

## Approved Linux host implementation (latest owner authority)

Owner approved Lima/VZ native arm64 Debian 13 plain mode, initially 8 vCPU, 10 GiB
RAM, 160 GiB sparse disk. Repository recipe is authoritative; VM is disposable.
All large state/disks/cache/temp/inputs must stay on the guarded configured external
workspace. See docs/build/lima-build-host.md. No container stack, host shares or
architectural workaround may be introduced to repair a failed capability gate.

On feature/1.1-build-foundation, prove the Linux capability gate before complete
build-stack installation or pi-gen. STOP on any required unavailable/unreliable
capability and report evidence for owner review. Only after all gates pass, continue
pinned input retention, external component packaging, real release lock, minimal
integration/first-boot and ONE private engineering POC image with offline validation.
Then STOP. No physical Pi qualification, broad modernization or release publication
is authorized in this phase. Do not treat one controlled build as reproducibility
proven, or synthetic fixtures as real inputs. Earlier phase boundaries above are
historical. No Menu feature branch until actual Menu source/packaging changes.

## First private POC completed (latest checkpoint)

The approved host gate passed and one frozen-input private image now exists, with
50 offline checks passing. See docs/build/private-poc1.md and CURRENT-STATE.md.
STOP for owner review. No automatic physical Pi testing, second image, package rebuild,
broad modernization or publication. Frozen integration/lock/image bytes are immutable
checkpoint inputs/outputs; later validators/docs must not silently alter them.
Current VM is stopped, not deleted. Preserve external inputs and both feature branches.

## POC1 physical failure analysis (latest owner boundary)

The owner tested exact POC1 on Pi 3B: boot/Menu/keyboard passed; x64sc display and
console recovery failed. See docs/qualification/poc1-pi3b-analysis.md and the
separate setup-ux-review.md. Read-only comparison and documentation/qualification
records are authorized; runtime, packaging, stage, privilege/network changes,
media acquisition/creation and POC2 are NOT yet authorized. STOP for owner review.
Intentionally masked POC1 services are not failures. Do not change frozen POC1 or
infer process state from the activity LED. Preserve UNTESTED later qualification.

## Authorized POC2 implementation (current owner boundary)

Owner authorized bounded graphics runtime/session/return corrections, private
persistent diagnostics and non-root diagnostic VT, original tiny qualification
media, a new frozen POC2 build and offline validation. No SSH, physical testing,
POC3, broad settings/privilege redesign, public release or push. Preserve all POC1
artifacts/lock/packages/qualification record unchanged. Stop after POC2 validation,
physical smoke-test instructions and continuity/recovery checkpoint.

## Documentation style

Use established software/Linux/Debian/Raspberry Pi/release terminology when it
improves precision; historical labels such as "Phase" are not protected in current
docs. Explain specialized terms on first use, prefer plain English, and maintain
concise start-to-finish how-to guides alongside architecture/reference material.
A capable Raspberry Pi/retro-computing user should not need release-engineering
expertise. Preserve historical documents as evidence; never modernize their words
to imply that later architecture existed at the time.

## POC2 completed (latest checkpoint / STOP)

POC2 built and passed offline/static checks; see docs/build/private-poc2.md and
CURRENT-STATE. VM stopped. Preserve both frozen candidates, locks/packages/media,
physical records and checkpoints. STOP for owner review and the hash-bound Pi 3B
procedure; no automatic physical testing, POC3, SSH, broad redesign or publication.

## POC2 physical review (current owner boundary)

Owner-reported Pi 3B results are in docs/qualification/poc2-pi3b.json; read the
companion aspect analysis before proposing geometry changes. Core launch/rendering/
return/audio/media/diagnostic VT/reboot passed; aspect preservation failed. POC1
precise cause remains unconfirmed. Only read-only investigation and qualification/
documentation updates are authorized now. STOP before implementing the proposed
POC3, building, additional-model testing, networking or publication. Frozen candidates
and historical records remain immutable; this new external qualification does not
change installed identity or the input lock. Preserve UNTESTED items explicitly.

## Authorized POC3 geometry work (current owner boundary)

Owner authorizes only native VICE per-chip geometry/fullscreen defaults, preserved
user preferences, bounded engineering evidence and one new frozen private POC3.
Read docs/build/poc3-design.md. Preserve POC1/POC2 and photo/qualification records.
STOP after POC3 offline validation, hash-bound Pi 3B procedure and recovery records;
no physical test, POC4, other models, SSH, broad modernization or publication.

## POC3 completed (latest checkpoint / STOP)

Read docs/build/private-poc3.md and CURRENT-STATE. Accepted POC3 is built and
offline-validated; physical results are UNTESTED. Preserve all three candidates and
the separate rejected host-drift attempt. Builder is stopped. No new build, physical
test, other Pi model, SSH, broad modernization or publication under this task.
Next owner action is review, then the exact-hash Pi 3B geometry/regression procedure.
Controlled future builds must pass the before/after host inventory/update-unit guard;
intentional builder updates require retained inputs and a new lock.

## POC3 physical qualification and product audit (latest boundary / STOP)

The owner reported a bounded Pi 3B POC3 pass including geometry, joystick and SID
voices. Read the additive physical attestation and docs/design/appliance-audit-2026-09-16.md.
Earlier physical-UNTESTED/build authorizations above describe completed checkpoints.
This task authorizes only read-only research, additive evidence retention and current
qualification/continuity/design documentation. Preserve POC1–3 and original Combian
reference material; do not acquire/embed optional software, build POC4, implement the
redesign, test other models, enable services/SSH or publish. STOP for owner review.

Menu changes should preserve Project CBM's personality while streamlining organization,
common task steps, state ownership and shared implementation. Historical menu structure
is not protected when it demonstrably obstructs use. Require concrete before/after
benefit, predictable Back/Cancel, tested narrow privilege and equal/better measured
Pi 3 response; separately qualify the Pi 3A+ 512 MiB constraint. No renderer migration
merely for novelty. Recommendations in the audit are not implementation authorization.

## First runtime foundation slice (latest completed boundary / STOP)

Owner approved pcbm-info, shared UI/results and user-owned preferences only. Read
CURRENT-STATE and docs/runtime/foundation-slice.md. Source implementation/tests are
complete; no image/package build, broader Menu/CONTROL reorganization, first boot,
network/services, optional software, other-model test or push. Preserve POC1–3.
The new registry/preferences are not yet activated in existing Menu/boot consumers;
never present desired preferences as effective state. pcbm-info JSON is the detection
authority for future configuration UI; no pretty-output scraping or duplicate probes.
STOP after the verified recovery checkpoint for owner review and the next bounded slice.

## Information and machine consumers (latest completed boundary / STOP)

The owner-authorized source slice is complete; read CURRENT-STATE and
`docs/runtime/information-machines-slice.md`. System Information consumes pcbm-info JSON;
MACHINES/RUN/shared content selection consume product registry/user preferences. Valid
new preferences win, missing state may import legacy once, malformed state requires
explicit recovery. Never restore sudo-based default writes or duplicate machine tables.
Boot preferences remain inactive; retire/migrate dormant pcbm-start before activating
that path. Preserve POC1–3, tags and earlier checkpoints. No POC4, image/package build,
broad CONTROL/settings changes, services/SSH, new hardware test or push in this slice.
STOP for owner review after tests and verified source recovery checkpoint.


## Configuration maturation (latest completed boundary / STOP)

The owner-approved final concentrated configuration pass is source-complete. Read
CURRENT-STATE and the product docs/runtime/configuration-contract.md. Retain the
pcbm-menu / pcbm-config / read-only pcbm-info / narrow backend boundaries. Ordinary
preferences remain user-owned; root operations are fixed, validated and readiness-gated.
Authenticated owner administration remains available after first-boot account setup;
never replace it with universal credentials or unrestricted passwordless root.

Do not mistake source adapters or saved boot/modem intent for activated runtime behavior.
Matching packages, account/service integration and constrained storage/modem/boot consumers
are product gates. Preserve POC1–3, tags and earlier checkpoints. No POC4, package/image
build, service activation, new hardware test, boot optimization, optional software or
push is authorized by this completed pass. Next owner review is first-boot/owner-account
and runtime activation integration, not another Menu framework/architecture study.

## Optional applications and reference content (latest source boundary / STOP)

Owner added SID-Wizard/StrikeTerm integration and SID/demo rights research after the
configuration pass. Read docs/runtime/optional-applications-contract.md and
CURRENT-STATE. Only the reviewed native SID-Wizard 1.97 core is admitted for future
frozen inputs. StrikeTerm and the requested HVSC/demo references remain owner-supplied;
free downloads, freeware labels, archive inclusion and Combian possession do not
establish redistribution rights. No automatic content downloader/scraper is authorized.

Preserve original basic qualification media separately from third-party references.
New application inputs require schema 3 and exact source/recipe/rights/payload hashes;
never edit POC1–3 locks/images/packages or add bytes to a finished image. Source routing
uses validated registry profiles and preserves default/VICE preferences. No POC4,
physical testing, service activation or publication in this addendum. Next product
milestone remains first-boot/owner-account/runtime integration, not Menu architecture.


## Runtime activation attempt stopped (latest checkpoint)

Read CURRENT-STATE and docs/build/poc4-blocked.md. First-boot/runtime source and
matching packages were implemented/tested; the new frozen lock is failed-attempt
evidence. No POC4 image exists. A builder-only TMPDIR leaked into pi-gen's target
chroot and AppArmor package configuration failed. STOP for owner review; do not
bypass security, retry, overwrite the lock/attempt or claim image/hardware passes.
Preserve POC1–3, all existing tags and optional-input rights classifications.
StrikeTerm is privately admitted only; public rights remain pending. No push.
Future approved construction must validate builder versus chroot environment;
Linux guest /tmp is external-backed and distinct from macOS /private/tmp.

## POC4 attempt #2 authorization

The owner authorizes only the documented builder/chroot environment correction,
regression/native revalidation and ONE new POC4 build attempt. Attempt #1 lock,
packages, failed tree and evidence remain unchanged. Use a distinct frozen kit and
attempt output path. Preserve AppArmor and package verification. Stop on recurring
or new build-integrity failure; otherwise finish offline validation, exact hashes,
Pi 3B procedure and recovery checkpoint. No physical test, POC5, push or publication.
Read docs/build/environment-boundary.md and CURRENT-STATE for current progress.

## POC4 attempt #2 completed / STOP

Read CURRENT-STATE, docs/build/private-poc4-attempt2.md and the exact-hash Pi 3B procedure.
The bounded environment correction, native revalidation and ONE fresh build succeeded.
Attempt #1 remains immutable failed evidence; attempt #2 is a distinct frozen input set
and offline-validated private image, not physically qualified or reproducibility-proven.
Preserve both attempts, POC1–3, all tags and rights gates. Builder stopped. STOP for owner
review; no physical test, next build, other Pi model, boot optimization, push or publication.

## Post-attempt-2 cover follow-up

Read CURRENT-STATE and docs/runtime/covers.md. Machine COVERS are source-implemented
after the frozen attempt #2 image; do not claim that image contains them. Preserve
all completed artifacts/locks/checkpoints. New Menu packaging/input freeze/build needs
owner review; no automatic third attempt. Boot presentation remains deferred.
