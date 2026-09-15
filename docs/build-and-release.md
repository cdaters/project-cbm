# Build and release contract

Status: contract and handoff only, 2026-09-15. No builder, lock implementation,
package changes, 1.1 image or new release is present. The original process was
interactive source-Pi installation, card capture, PiShrink and XZ compression.
Historical Menu build notes/workflow remain evidence, not the future image recipe.

## Required mapping for every future product candidate

| Field | Required identity/evidence |
| --- | --- |
| Project CBM | Semantic version, candidate identity, architecture and edition/base description |
| OS/base input | Raspberry Pi OS release/date and source; official base image URL/size/SHA-256 if used, OR exact pi-gen Lite recipe/package state; never conflate these |
| Builder | pi-gen/builder repository and full commit, configuration digest, host/OS/architecture, toolchain versions |
| Package closure | Exact Debian/Raspberry Pi package versions, architectures, .deb hashes and retained authenticated index metadata; include transitive dependencies |
| VICE | 3.10 initially; source URL/hash/license, patches, configure/compiler flags, package version/hash, corresponding source and build log |
| TCPser | Version and full source commit, patches/build flags, package version/hash and source/license; evaluate the shipped 1.1.6_beta lineage deliberately |
| Menu | Independent version, explicit tag, tag object where annotated, peeled full commit, artifact SHA-256, packaging identity, compatible configuration schema |
| Integration | Full project-cbm commit, clean-tree status, integration/config/assets hashes |
| Configuration | Explicit schema version, system/user ownership, supported migration/restore behavior |
| Content | Allowed file inventory, license/provenance per asset and exclusion decisions |
| Qualification | Exact candidate hashes, supported model/revision/RAM matrix, results and known limitations |
| Outputs | Raw/compressed image sizes and hashes, package inventory/SBOM, manifest, logs, source/license artifacts, public docs and release notes |

Never use arbitrary current main as a dependency. A tag alone is insufficient;
resolve and verify its peeled commit and downloaded artifact digest. Fail on dirty
source, missing inputs, checksum/version/schema mismatch or unknown provenance.
Do not fill unknown historical inputs with guessed values. Historical identities
are in [provenance](provenance.md), not a claim that a complete lock has been recovered.

Retain the entire package closure, not just a caching proxy or version list.
Debian snapshots do not automatically preserve Raspberry Pi packages. Separate
networked acquisition from clean repeatable assembly using retained verified inputs.
Builder tooling and build-specific temp/cache paths belong on TheBench.

## Reproducibility and release gates

Initially demonstrate two clean builds with identical declared inputs, package
sets, application files and configuration. Compare image outputs and explain every
remaining difference before claiming byte reproducibility. Record timestamps,
locale/timezone, ordering, paths, identifiers and toolchain behavior. Per-device
keys and machine identity must be generated after imaging, not baked into output.

Physical qualification is mandatory, especially Pi 3, before compatibility claims.
The POC is local and private pending identity, credentials, privilege, service,
installer and content gates in [security](security.md). No release publication is
implicitly authorized by building a POC. Preserve existing tags/assets unchanged.

## New-session first task

With a NEW owner instruction authorizing the 1.1 POC, begin in ~/Code/project-cbm:

1. Read AGENTS.md, CURRENT-STATE.md, this contract, provenance and testing. Inspect
   clean Git state and verify the Menu recovery/formal release distinction.
2. Create a short POC feature branch off current main. Inspect TheBench mount/space
   and identify the available native arm64 Linux host or suitable Linux VM and
   Linux filesystem backed by TheBench. APFS folders are not a Linux rootfs.
   The build environment decision is still open; do not silently choose the Mac
   internal disk, change global temp settings or provision a costly remote host.
3. Verify official current pi-gen arm64 Lite guidance and candidate Trixie inputs.
   Record full builder/input identities and a small proposed input-lock schema
   implementing the mapping above. Audit-era upstream versions are not a current lock.
4. Establish the smallest pinned arm64 Lite stages plus one Project CBM integration
   stage. Package/pin VICE 3.10 SDL2, a reviewed Menu candidate/package with explicit
   tag/commit/hash, and TCPser. Do not substitute formal Menu v1.0.0 for the exact
   shipped runtime without recording the five changes and extra helper.
5. Build one PRIVATE POC on Linux using TheBench-backed bulk storage, preserving
   inputs/logs/output hashes. Validate image composition and record blockers; then
   repeat cleanly and compare. Plan Pi 3B/3A+ checks early using the audit matrix.

The first deliverable should establish the host/filesystem and pinned inputs,
then a minimal reviewable recipe and private image evidence. Do not start optional
screenshots/themes/controller additions before the reproducible-build foundation.
Runtime defect fixes belong in separately reviewable changes within the new scope.

This preservation phase stops before step 2; it does not itself authorize this work.
