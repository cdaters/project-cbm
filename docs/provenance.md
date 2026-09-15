# Historical provenance and preservation

Reconciled 2026-09-15. The [full audit](audit-2026-09-15.md) retains the original
assessment, corrections and qualification matrix. Facts below come from inspected
bytes/refs; inferences and unknowns are labeled.

## Image and source identities

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| Published pcbm-v1.0.0-rpi3-5.img.xz | 804405364 | `0bb17d7c72d2de7f8e70f77f001683547ae3cf2db6f832f3d2727d971cd47ec9` |
| Decompressed published image | 6839124480 | `168a3026eca2bc328e03e47dfbb0cbe17740180504ad7858496df84982e89849` |
| Historical raw pcbm-v1.0.0-rpi3-5.img | 15931539456 | `845d99d1ea20aca85c0739e5fa1bf8a9d2046bcb5f9d302576ef74bb39cdc9fe` |
| Product published docs ZIP | 179709 | `c4fceb9ea1d76217ec8febb18005c0e4c39168d0405a88434083f18a46174944` |
| Product published SHA256SUMS | 179 | `bbd4fc904724c1a0249c340e39966c136906dc7d0f5c1f10a885c6eda3ac29f2` |
| Formal Menu bundle | 1785229 | `86239c674b6541a10628ac5b43995e200739240073d23c85206d4a7a21e6314e` |
| Menu published docs ZIP | 179619 | `7295cc34da7513e9bc7db87857ae687390edb2bfd1f2bfe3449e90e7f4c76e4f` |

TheBench's two historical XZ copies and retained downloaded XZ match the published
hash. Do not confuse the 15.93 GB raw capture with the 6.84 GB decompressed release.
Both images have byte-identical 17-script runtime and os-release. The raw capture
has a larger root partition and lacks the published PiShrink rc.local. This strongly
supports its pre-PiShrink origin; a complete byte-level transformation/command chain
has not been recovered or replayed. The two whole images are not byte-identical.

Internal v6.1/v6.3/v6.4 bundles, v6.2 notes, v6.4 hotfix/patched/obsolete/backup
variants and v6.5 loose/archive material are preserved in place. GoldMaster and
scriptsForChat/for65 are additional late-development evidence, not public releases.
Compared with the shipped 17 scripts, v6.1/v6.3/v6.4 loose sets contain 13/15/17;
the simple comparison finds 6/7/10 normalized matches. These counts describe observed
files, not a proven linear commit history or behavioral equivalence for early versions.
All 17 v6.5, GoldMaster and for65 loose/archive scripts match after the documented
comment/whitespace comparison, but none is byte-identical to its shipped counterpart.
Accepted prior review established v6.5 executable-source equivalence; normalization
alone is not a shell semantic proof. The surrounding configs are not a system snapshot.

The 5.2 MB project-cbm-v6.4-build.log records VICE configure flags, make parallelism,
installation and compiler output; dated build notes provide further context. This
improves the earlier diary-only evidence. It does not prove every logged action is
the final build invocation or recover a complete source/package lock. Full transcripts
remain private; only command-token line references and hashes were exported.

## Git reconciliation

| Repository | Before local main | Verified GitHub main / fast-forward result |
| --- | --- | --- |
| project-cbm | `46fbf47d66596b2f3d0f6ab53d26bdd90632c73c` | `493229c8bd4135a9c9132b770087b72313e64e99` |
| project-cbm-menu | `f185d916959a7bd6ed4d561e0c66e7f42f1efb28` | `b7e4d858ce54e6623b6264b930e841e03fad1a19` |

Each clean main fast-forwarded 26 commits, then received local continuity commits.
Before fetch, full local .git archives and --all bundles were made, and live GitHub
refs/mirror/bundles/release metadata captured. No reset, force update, retag, asset
mutation or push was used. Existing remote backup/pre-v1-cleanup and annotated
pre-v1-skeleton are retained. Final bundles include new refs and continuity commits.

Product lightweight v1.0.0 remains `46fbf47d66596b2f3d0f6ab53d26bdd90632c73c`.
Formal Menu annotated v1.0.0 remains object `0756331cf872dfeaec17bdb75939f84e47e04f9f`,
peeled commit `399c6158caa8ed2762744d512c1841b94ad64403`. Main at b7e4d85 has the same
runtime/config/packaging as that formal release; subsequent changes were documentation.
The formal source has 12 exact shipped matches, five changed scripts (control,
system, network, start, release-prep) and an extra experimental screenshot helper.
Its source release is related to the product image, not a byte-identical dependency.

New annotated Menu tag `recovered/image-v1.0.0-runtime` points to root commit
`1cd5e0d378a4066f239c92a30aafdd97cb415dcf` (tag object
`d3163efd4baca08fcdaf83a6db8854bee31509ee`). No historical Git parent is asserted.
The commit contains exactly extracted scripts plus recovery/license/hash documentation;
no normalization, reconstruction, configuration or private image state was imported.
Original executable mode is represented in Git; uid/gid/modes are in the manifest.
It is forensic source evidence, not an installable package or normal release.

## Maintenance policy

- Product maintenance/1.0 starts at product v1.0.0; this is the correct product
  documentation/release branch point, not a claim that Git contained an image recipe.
- Menu maintenance/1.0 starts at the recovered root commit. Bring future important
  or security fixes, packaging and necessary configuration forward deliberately,
  with a reconciliation changelog and new qualification. Do not merge the entire
  formal release and silently claim equivalence. The immutable recovery tag stays fixed.
- 1.0.x is the original Trixie appliance generation; 1.1.x is active current-Trixie
  reproducible-build work. There is no Bookworm maintenance branch. No 1.0.1 was
  created or published. Branches and the recovery tag are local and externally bundled.

## Preservation inventory and trust domains

Original root: `/Volumes/TheBench/Projects/Project CBM`, unchanged in place.
New archive: `/Volumes/TheBench/ProjectCBM-Work/archive/preservation-2026-09-15`.
Retained assets/extraction/clones: `ProjectCBM-Work/archive/audit-2026-09-14/workspace`.

| Material | Treatment / classification |
| --- | --- |
| Historical raw/published images; identity/config evidence; build logs/diaries; Git administrative archives and draft metadata | PRIVATE-HISTORICAL; preserve existing bytes, manifest in place; publication is not sanitation |
| Reviewed original MIT scripts/docs, public checksum/release metadata | PUBLIC/REDISTRIBUTABLE subject to original license; detailed inventories use conservative provisional labels |
| Media, ROMs, scans, cover artwork/source assets, fonts, mixed bundles | PROVENANCE-UNKNOWN until per-file rights review; preserve license/readme clues with assets |
| Disposable inspector environment, caches, future build trees; published-image decompression derivable from verified XZ | RECREATABLE operationally; sensitive derived images still retain PRIVATE-HISTORICAL handling; no deletion in this phase |

All loose/archive versions, scriptsForChat/for65, hotfixes/patches, backups/obsolete
variants, logs, config, docs, artwork/fonts and source assets under the original root
are covered, including hidden files and xattr hashes. No multi-GB copies were made.
Existing historical duplicates were not deduplicated. Original audit/relocation
records are separately inventoried and preserved unchanged.

External `git/` has before-local .git archives/bundles, remote mirrors/bundles,
ref inventories and release metadata including the abandoned draft. `reconciliation/`
has image/lineage comparisons, exact scripts and manifests. `manifests/` has tree
inventories; [anchor hashes](preservation-manifests.json) enable integrity checks.
External README and validation records explain verification and final-state bundles.

Manifests record paths, type, size/hash, mode/mtime and xattr hashes; they never dump
file contents or private keys. Labels are conservative handling guidance, not new
license grants. Detailed manifests stay private. ACL/ownership/atime recovery is not
claimed. One APFS device is not an independent backup; choose a second encrypted
destination and periodic full verification separately. Do not alter historical modes
or set immutable flags in place just to enforce a policy label.

## Remaining historical questions

Original official-base XZ/checksum and complete input closure; final capture/shrink
invocation; independent VICE tarball authentication and any source patches; whether
all art/media/fonts may be redistributed; actual two-flash identity behavior and
per-model hardware performance remain unresolved. Preserved files improve evidence,
but a build transcript, branch name or OS compatibility list cannot close these gaps.
