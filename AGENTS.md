# Working on Project CBM

Read CURRENT-STATE.md first, then docs/architecture.md, docs/provenance.md and
docs/testing.md. Repository files are the continuity record; old Codex sessions
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

## Checks and phase boundary

Run git diff --check, validate added JSON, check local links, inspect staged file
sizes and secret patterns, and use per-file Bash syntax checks for shell changes.
Follow docs/testing.md for focused behavioral and physical-device qualification.
Keep logical commits and leave a clear git status. Do not claim hardware passes
from static checks. Verify preservation manifests after preservation changes.

Preservation/reconciliation/continuity is complete. The next milestone is the
Project CBM 1.1 reproducible-build proof-of-concept in docs/build-and-release.md.
Starting that milestone requires a new owner instruction; this preservation
authorization does not authorize pi-gen, runtime changes, an image or publication.
