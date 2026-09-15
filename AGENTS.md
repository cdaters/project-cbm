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
  Linux builder needs suitable Linux filesystem semantics; no builder is set up.
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
