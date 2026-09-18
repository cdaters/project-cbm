> Current 1.1 release-readiness checkpoint: [attempt #7](build/private-poc4-attempt7.md)
> and [CURRENT-STATE](../CURRENT-STATE.md). Start with the [release documentation](README.md),
> [actual build walkthrough](release/build-your-own.md) and [factory explanation](release/factory.md).
> Dated checkpoints below retain historical evidence; they do not override current governance.

# Build and release contract

Current checkpoint: [POC4 attempt #2](build/private-poc4-attempt2.md) is built and
offline-validated; [Pi 3B qualification](qualification/poc4-attempt2-pi3b-smoke-test.md)
is pending owner review/testing. Attempt #1 remains immutable failed construction.
Use the [explicit builder/target environment contract](build/environment-boundary.md),
new frozen attempt kit and `--attempt 2` workspace. Host drift guard remains mandatory.
No physical behavior or independent reproducibility is claimed. STOP before another
build, hardware test or publication; older phase boundaries below are historical.

Status: [ADR-0001](adr/0001-base-distribution-and-image-architecture.md) remains
accepted. Exact private POC3 has a [bounded physical Pi 3B pass](qualification/poc3-pi3b-owner-report-2026-09-16.json),
including corrected geometry, alongside its unchanged [build checkpoint](build/private-poc3.md).
The [product audit](design/appliance-audit-2026-09-16.md) proposes the next work order.
STOP for owner design review; no POC4, additional models or publication. Independent
clean-rebuild reproducibility and public release readiness remain unproven.

Full [black-box project recovery](recovery.md) is mandatory for the repositories and
build/release infrastructure from 1.1. The image carries only minimal installed identity;
locks, recipes, schema/test corpora and inventories stay external. The contract defines
the JSON lock/identity/external qualification relationship, offline identity, retained
inputs/environment bootstrap and recovery tests. The design worksheet is not a
usable lock; formal input/identity schemas/generator are now in the POC branch. A successful or repeatable
build alone is insufficient for release readiness.

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
Builder tooling and build-specific temp/cache paths belong on TheBench in this
current deployment. Future tooling must accept configured roots and portable relative
locators, without literal Mac paths. Retain bootstrap/toolchain and corresponding
source closure, not only runtime package inputs.

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

**STOP for owner review:** POC2 is built and offline validation complete. Read
[the current checkpoint](build/private-poc2.md), CURRENT-STATE and the
[hash-bound Pi 3B procedure](qualification/poc2-pi3b-smoke-test.md).
Do not automatically construct another image, perform a physical test or publish.

### Completed first-POC construction sequence (historical)

Milestone 1 and the Lima/VZ build host are owner-approved. The
[host capability gate](build/lima-capability-2026-09-15.md) passed; use the
[repository-controlled recipe](build/lima-build-host.md) and inspect CURRENT-STATE
for newer work. The sequence below records the first POC workflow:

1. Read AGENTS.md, CURRENT-STATE.md, this contract, recovery.md, provenance and testing.
   Inspect Git and preserve unfamiliar dirty work; verify Menu recovery versus the
   formal release before choosing an input.
2. Continue existing feature/1.1-build-foundation. Inspect TheBench mount/space
   and identify the available native arm64 Linux host or suitable Linux VM and
   Linux filesystem backed by TheBench. APFS folders are not a Linux rootfs.
   The approved host is Lima/VZ plain Debian arm64; do not silently choose the Mac
   internal disk, change global temp settings or provision a costly remote host.
3. Verify official current pi-gen arm64 Lite guidance and candidate Trixie inputs.
   Record full builder/input identities; follow accepted ADR-0001 rather than reopening
   the foundation comparison without a revisit trigger. First formalize the recovery
   contract's
   lock/minimal-identity/external/qualification schemas and offline validation fixtures,
   including checksum-cycle rejection and retained environment/input closure.
   Audit-era upstream versions are not a current lock.
4. Establish the smallest pinned arm64 Lite stages plus one Project CBM integration
   stage. Package/pin VICE 3.10 SDL2, a reviewed Menu candidate/package with explicit
   tag/commit/hash, and TCPser. Do not substitute formal Menu v1.0.0 for the exact
   shipped runtime without recording the five changes and extra helper.
5. Build one PRIVATE POC on Linux using TheBench-backed bulk storage, preserving
   inputs/logs/output hashes plus minimal installed identity from that same lock.
   Retain full recipes/recovery material externally and measure image footprint/free
   user capacity; no arbitrary nominal SD-card size is an acceptance requirement.
   Generate external image/qualification records after image freeze; never alter a
   qualified image to insert its results. Validate recovery/image composition and
   record blockers, then STOP for owner review. A later clean repeat/comparison and
   physical Pi 3B/3A+ qualification require the subsequent phase.

The first deliverable should establish the host/filesystem and pinned inputs,
then a minimal reviewable recipe and private image evidence. Do not start optional
screenshots/themes/controller additions before the reproducible-build foundation.
Runtime defect fixes belong in separately reviewable changes within the new scope.

Current milestone boundary: stop on a required Linux capability failure, or after
one private POC image and offline/static validation. No public release or automatic
physical Raspberry Pi testing. Read the latest CURRENT-STATE rather
than treating historical phase boundaries as the current implementation status.

## 2026-09-18 private attempt #6

Attempt #6 is a distinct private lock/image using Runtime 1.1.0~poc4.3-1 and Menu 1.1.0~poc4.4-1+pcbm1; construction/offline gates pass. No reproducibility or physical success claim. See [build record](build/private-poc4-attempt6.md).
