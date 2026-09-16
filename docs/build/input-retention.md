# Input retention and recovery plan

Milestone 1 policy, updated 2026-09-15. The first real frozen kit now exists; see
[private POC results](private-poc1.md). Full recovery is
external infrastructure responsibility. See [contracts](contracts.md) and
[project recovery](../recovery.md). Classifications apply to future CBM inputs;
they do not authorize deletion, normalization or replacement of historical evidence.

| Class | Material | Retention treatment |
| --- | --- | --- |
| MUST RETAIN | Both CBM Git histories/accepted refs, pi-gen exact Git source/bundle, submodule/LFS payloads if introduced | Standalone bundles plus exact ref inventories; source hashes and licenses; verify offline restore |
| MUST RETAIN | All Debian and Raspberry Pi binary packages used by rootfs, package builds and host bootstrap | Exact .deb files, versions, architectures, digests and transitive closure catalogs; source repository origin; no dependence on an APT cache or future mirror |
| MUST RETAIN | Authenticated repository state | InRelease/Release/Release.gpg, Packages/Sources indexes, relevant public keyring and fingerprint/trust/time evidence. Keep original authentication evidence; never silently disable checks for expired snapshots |
| MUST RETAIN | Corresponding Debian/RPi source and CBM components | .dsc/orig/debian tar inputs where applicable, VICE 3.10 source, Menu tagged Git/source artifact, TCPser source; reviewed patches, recipes, build options and all produced component .debs |
| MUST RETAIN | Toolchain and reproducibility inputs | Exact compiler/binutils/libc/development dependencies, build tools, bootstrap image/ISO, environment contract, host package closure, locale/timezone/source-date epoch and flags. A VM snapshot is not their only copy |
| MUST RETAIN | Product configuration/assets | Integration source, defaults/schema, sealing/first-boot recipes, assets and per-file rights inventory; required runtime ROM provenance separately reviewed |
| MUST RETAIN | Accepted candidate/release outputs | Raw and compressed image, frozen lock, minimal identity, build record, manifests, inventories/SBOM, hashes/signatures, sanitized logs and qualification records tied to exact candidate bytes |
| SHOULD RETAIN | Diagnostic support | Failed-build sanitized logs, rejected candidate summaries, download verification transcripts and known-good stopped VM snapshots to shorten recovery |
| RECREATABLE CACHE | Performance aids | APT/compiler/download caches, derived stage trees, throwaway package-build environments, temporary decompression of a verified retained image. Cache eviction cannot remove the only input copy |
| DO NOT RETAIN in public kits | Private operator/device data | Passwords, private keys/tokens, agent sockets, builder homes/history, private URLs, live device IDs and user content. Signing/unlock custody, if needed, is a separate protected system |

“DO NOT RETAIN” is a public-kit policy, not an instruction to destroy private
historical evidence. Detailed private build diagnostics have explicit custody and
retention limits; public build records must be purpose-built summaries. Corresponding
source/license obligations need per-component review before distribution; a retained
file is not automatically licensed for public redistribution.

## Portable layout and catalog

A configured bulk root has `inputs/`, `packages/`, `builds/`, `cache/`, `artifacts/`,
`qualification/`, `scratch/`, `archive/`, plus approved `build-host/` storage.
Current deployment: `/Volumes/TheBench/ProjectCBM-Work`. Source Git stays in ~/Code.
Current external catalogs record relative path, hash/size, source and role.
Handling classes and license/trust decisions are in the associated policy and records;
per-file structured license coverage still needs refinement before public distribution. Never
bind a lock to this Mac's absolute pathname. Predecessor lock references are immutable;
a new acquisition does not overwrite old bytes under an existing accepted identity.

Binary/source closure catalogs must enumerate **every file**, not just top-level
package names or URLs. Distinguish target runtime, component build and host bootstrap
closures, including versioned toolchain dependencies. Retain archive metadata before
expiry; any later offline trust decision needs an explicit record. The implemented retained-input validator checks direct and nested closure files,
component build-record references and Debian metadata. Exact bootstrap is pinned.
A standard SBOM format and independent closure replay remain future work.

## Acquisition and freeze gates

Network acquisition verifies origin and expected digests before indexing bytes.
Separate source builds from image assembly. The full image lock is frozen only when
packages and their predecessor build records exist. Retain the exact configuration
used to resolve dependencies and run a later assembly with upstream access unavailable.
An identical lock does not prove identical images: compare clean builds and document
all differences before claiming bitwise reproducibility.

Synthetic fixtures remain negative/contract test data. The real POC lock separately
pins selected Menu, VICE, TCPser, pi-gen, package/metadata/source closures and bootstrap.
Source acquisition/trust limitations are explicit in the POC record. Existing released/
recovered refs remain historical evidence, not automatic acceptance of a 1.1 input.

## Acceptance, custody and capacity

For an accepted release, retain both distributed compressed bytes and raw qualification
identity. Disposable raw staging copies may be recreated from a verified XZ only when
exact decompression equivalence is recorded; never discard unique accepted evidence.
Do not duplicate historical multi-GB images to refresh Git-only checkpoints.

Verify bundle/catalog digests, clone to fresh mirrors, compare all refs and recovered
scripts, run fsck, then test a relocated clean Linux reconstruction. Keep at least one
independent encrypted recovery copy with separately recoverable custody, in addition
to TheBench and GitHub. That destination, signing custody and a standard SBOM choice
remain owner/engineering gaps. No second backup exists merely because local restore
passes. Archive the Linux environment recipe as well as binaries; ordinary arm64
Debian Linux must remain a documented fallback if a Mac VM frontend disappears.
