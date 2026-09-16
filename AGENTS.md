# Working on Project CBM

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
