# Historical provenance and preservation

Latest source checkpoint: [runtime foundation](runtime/foundation-slice.md).
Current bundles/manifests and offline restore evidence are under configured bulk
storage at `archive/runtime-foundation-2026-09-16`. The earlier POC3/audit checkpoints
below remain unchanged. Source implementation is not a new installed/qualified image.


Latest additive evidence: [POC3 Pi 3B physical report](qualification/poc3-pi3b-owner-report-2026-09-16.json)
and [product audit](design/appliance-audit-2026-09-16.md). Current Git bundles and their
SHA-256 manifest/offline restore report are under configured bulk storage at
`archive/poc3-pi3b-product-audit-2026-09-16`. This supplements, rather than replaces,
the completed POC3 build checkpoint and all historical preservation records.

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

Following the authorized unpublished identity repair (see
[old/new mapping](privacy-reconciliation-2026-09-15.md)), the annotated Menu tag `recovered/image-v1.0.0-runtime` points to root commit
`a4148db54001790eaddb4e31104917c16149b181` (tag object
`21ae1d2b8d595f0339295351bd34fcea44a78db4`). No historical Git parent is asserted.
The commit contains exactly extracted scripts plus recovery/license/hash documentation;
no normalization, reconstruction, configuration or private image state was imported.
Original executable mode is represented in Git; uid/gid/modes are in the manifest.
It is forensic source evidence, not an installable package or normal release.

## Maintenance policy

- Public product v1.0.0 is the authoritative public maintenance baseline. The local/
  bundled maintenance/1.0 ref has no unique commits; its publication is intentionally
  deferred by the owner after GH007 rejected historical email metadata during new
  branch creation. Do not retry publication, rewrite v1.0.0 or weaken privacy.
  Product maintenance/1.0 starts at product v1.0.0; this is the correct product
  documentation/release branch point, not a claim that Git contained an image recipe.
- Menu maintenance/1.0 starts at the recovered root commit. Bring future important
  or security fixes, packaging and necessary configuration forward deliberately,
  with a reconciliation changelog and new qualification. Do not merge the entire
  formal release and silently claim equivalence. The immutable recovery tag stays fixed.
- 1.0.x is the original Trixie appliance generation; 1.1.x is active current-Trixie
  reproducible-build work. There is no Bookworm maintenance branch. No 1.0.1 was
  created or published. Current publication/checkpoint status is recorded in
  [privacy reconciliation](privacy-reconciliation-2026-09-15.md).

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

## Black-box recovery assessment

[Recovery section 7](recovery.md#7-historical-10-assessment) distinguishes KNOWN,
RECOVERED, STRONGLY INFERRED, UNKNOWN and conditionally UNRECOVERABLE. 1.0 preserves
exact artifacts and substantial evidence; it does not retroactively meet the new
1.1 lock/self-description/proven-rebuild requirements. No missing pin is manufactured.

The accepted final bundles were restored offline into fresh mirrors during the
2026-09-15 recovery-design pass: all five product refs and eight Menu refs matched
their retained inventories; fsck and all 17 recovery-script hashes passed. This
proves source/ref recovery from that checkpoint, not independent backup or full
build recovery. New design commits are retained separately under the current
ProjectCBM-Work/archive/black-box-design-2026-09-15 deployment. The sealed preservation
archive is unchanged. Portable locators/configured roots must support later relocation;
historical absolute roots remain evidence of the capture environment.

## Recovery bundle locators and digests

Read-only SHA-256/size verification on 2026-09-15 confirmed these existing bundles.
Locators below are relative to the configured archive root (currently
`/Volumes/TheBench/ProjectCBM-Work/archive`), not hard-coded restoration requirements.

| Checkpoint / relative bundle locator | Bytes | SHA-256 |
| --- | ---: | --- |
| `preservation-2026-09-15/git/project-cbm/after-local.bundle` | 734387 | `17b5fa40e3c78ee1fb0fb2fa9f0cd1e79bc613de46ef3119ad2c933b0b3d715e` |
| `preservation-2026-09-15/git/project-cbm-menu/after-local.bundle` | 1959846 | `bd193a3a77e2390aaf68b3ae7e9e15f963566868d26bbb8dcb7db0980635a75e` |
| `black-box-design-2026-09-15/project-cbm.bundle` | 754630 | `17271844e968dc44ea71492169c91c2e2ee4c96ec46f1783dda09cd53a24972e` |
| `black-box-design-2026-09-15/project-cbm-menu.bundle` | 1961346 | `3e80a8e92cd63709b6c45aeabbf8dadcae7600f87a988ca17acd5ac05712ce7d` |

Preservation ref inventories are beside the bundles as `after-local.json`.
The later design archive's `checkpoint.json` lists both repositories, all refs and
payload hashes; `checkpoint.json.sha256` is its separate checksum. The checkpoint
JSON SHA-256 is `dd450d31a487dedf3e5c1ae99a0f513dea4d873ebe7dda13c49f69dfabbcc631`
(rechecked against its checksum record). Its product main
is `7f9c4a363cf19154a9637ed8b251049bf23723e0`, Menu main
`c3746a12e6146f880c49979df8da2a3567200924`. Use the latest verified checkpoint that
actually contains the desired commits. These bundles predate the final architecture
reconciliation and identity repair. They retain their original checkpoint meaning
and old commit IDs. Use the additive
[privacy-reconciliation checkpoint](privacy-reconciliation-2026-09-15.md#recovery-checkpoints)
for current refs and replacement IDs; never overwrite sealed archives.

Full restore instructions are in [recovery](recovery.md#restore-git-without-github).
Retain an independently trusted catalog: a colocated hash is not authentication.
This phase rehashed the bundles and verified all three preservation tree manifests;
it did not repeat the earlier clone/restore drill or create an independent backup.
