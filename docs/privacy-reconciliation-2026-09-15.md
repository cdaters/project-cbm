# Unpublished commit identity reconciliation

Date: 2026-09-15. Owner-authorized exception for exactly eight unpublished commits.

## Reason and scope

GitHub GH007 blocked the attempted product push because its unpublished commits
exposed the owner's private commit email. The atomic product push changed no remote
refs; the Menu push was not attempted. GitHub privacy protections remain enabled.
Both repositories now use the owner's verified GitHub noreply identity; no Git or
GitHub settings were changed by this repair. No already-published commit was rewritten.

Fresh remote inventories and clean worktrees were verified before preservation and
again before ref replacement. No additional unpublished commits appeared. The exact
eight replacements are below and in the [machine-readable mapping](privacy-reconciliation-2026-09-15.json).

## Commit mapping

| Repository | Old commit | Replacement commit |
| --- | --- | --- |
| project-cbm | `7f9c4a363cf19154a9637ed8b251049bf23723e0` | `93c96b123c26c803fd6d23e74fd7bb830f25ec64` |
| project-cbm | `8020d475e9a09421a2d9afde3226a1022d5cb18b` | `0154a5031e601552b59dcd5d4a170813959b52f5` |
| project-cbm | `9d7ea95a770186dfc5814fb46474a2c84b4fc7e7` | `41973da7b1d146c07f716398bcd197c4b9e57c75` |
| project-cbm | `a44e2a73051c84a3697a4093a30bcde18bb1ecc4` | `31c75570ff588d1fc6d50ea885d9dc1f2359a51c` |
| project-cbm-menu | `1cd5e0d378a4066f239c92a30aafdd97cb415dcf` | `a4148db54001790eaddb4e31104917c16149b181` |
| project-cbm-menu | `c3746a12e6146f880c49979df8da2a3567200924` | `871d2cd1bd0c67a974e5286824868d35765dcd65` |
| project-cbm-menu | `deb19f13c64ed9a604b942509e9366d5d0a740c4` | `96ceb66494762efdab64a510e1302d4d24c580ad` |
| project-cbm-menu | `ed16b3e8ef0d43581a5a8f31b2944f869ee5c12c` | `a53b2ce02dbc0baa94e3fa3ded2b1640617b67e9` |

These are new preservation/continuity/architecture commits, including the Menu
forensic root containing historical bytes; none is an original published historical
commit. Only author/committer identity and necessarily dependent parent IDs changed.
Raw object comparison verified equal trees and message bytes, unchanged author and
committer dates/timezones, preserved parent order and the exact old/new parent mapping.
The recovered root remains parentless. Current documentation corrections are separate
new commits, not content changes disguised as metadata rewrites.

## Ref policy

- Product `maintenance/1.0` remains published historical `46fbf47d66596b2f3d0f6ab53d26bdd90632c73c`.
- Menu `maintenance/1.0` and `recovered/image-v1.0.0-runtime` now resolve to
  `a4148db54001790eaddb4e31104917c16149b181`.
- The previously unpublished annotated forensic tag object changed from
  `d3163efd4baca08fcdaf83a6db8854bee31509ee` to
  `21ae1d2b8d595f0339295351bd34fcea44a78db4`. Its annotation bytes, name and tagger
  timestamp are unchanged; its target and tagger email now match the privacy repair.
- Published product `v1.0.0`, Menu `v1.0.0`, `pre-v1-skeleton` and remote backup history
  are unchanged. This exception does not authorize future retagging or history repair.

## Recovery checkpoints

Locators are relative to a configured archive root, currently
`/Volumes/TheBench/ProjectCBM-Work/archive`. The additive checkpoint is
`privacy-reconciliation-2026-09-15/`; the original historical directory and sealed
preservation/design archives remain untouched. No large images were duplicated.

- `pre-rewrite/`: full original bundles; private historical metadata.
- `rewrite-plan.json`: exact before/remote refs, intended mapping, bundle hashes and ref updates.
- `rewrite-verification.json`: per-commit tree/message/date/parent verification.
- `repair.py`: exact scoped repair procedure; retained for audit, not an instruction to rerun.
- `rewritten/`: standalone replacement bundles, ref inventory and offline restore results.
- Later `ready-to-push/` and `published/` checkpoints are written only when those phases
  complete. Each has `checkpoint.json`, its separate SHA-256, bundles and restored mirrors.
  Use `published/checkpoint.json` only after it exists and verifies; it will identify
  final documentation commits and remote inventories without a circular self-hash.

Verified rewritten checkpoint (before follow-up documentation):

| Relative bundle locator | Bytes | SHA-256 |
| --- | ---: | --- |
| `privacy-reconciliation-2026-09-15/rewritten/project-cbm.bundle` | 785319 | `fc48ec107308d2267d2d1fcaf334fc211f3d2f25ff95a2876a9309f75b17a234` |
| `privacy-reconciliation-2026-09-15/rewritten/project-cbm-menu.bundle` | 1963629 | `7d4f65c0425fe853cd921a20b4096be67f1bd630493bd0c6f3ca0e3016ef75ba` |

Its `checkpoint.json` SHA-256 is
`b2ad95a773447546adb006b1118fc460f4455858d98823cef594d5abd9e80ea1`.
Offline mirror restoration matched all 5 product refs and 8 Menu refs, passed
`git bundle verify` / `git fsck --full`, and compared all 17 recovered scripts byte
for byte. This proves source/ref recovery, not image rebuilding or physical qualification.

Earlier audit and architecture-validation records intentionally retain their old
IDs as checkpoint evidence. Old objects remain in private bundles/reflogs; they are
not current publication refs. Restore old checkpoints in isolation, consult this
mapping and choose the later verified checkpoint when resuming current development.
Do not delete or rewrite old archives to conceal the identity repair.

## Validation and publication state

Metadata-only rewrite and rewritten offline restoration: PASS. Static checks passed:
44 current-document local links/anchors, all 3 repository JSON files (duplicate keys
and non-finite constants rejected), 22 per-file Bash syntax checks, diff whitespace,
reviewed documentation-only changes, and private-key/token/password-hash patterns.
Largest reachable Git blobs are 217,571 product bytes and 361,069 Menu bytes; no
large build artifact was introduced. All newly publishable commit identities match
the effective noreply identity. Historical audit/release/checksum and all runtime
trees are unchanged. Original preservation manifests verified all 1,677 historical,
82 prior-audit-record and 296 retained-audit entries without changed paths.
Publication is pending documentation commits and a fresh remote comparison.
Push main normally in each repository, then only the accepted maintenance/recovery
refs; never force-push. Stop on any rejection. The final external checkpoint records
exact resulting remote refs and accepted documentation tips. No release assets change.

## Remaining gaps and next action

One unencrypted APFS volume is not independent backup. Independent encrypted
custody/restore, Linux bootstrap, signing custody, SBOM choice, measured acceptance
budgets, historical input/build-chain gaps and all physical Pi qualification remain
open. Earlier historical bundle digests still identify their original bytes. The
new checkpoint closes the missing-architecture-commit bundle gap, not these gaps.

After successful publication and final checkpoint verification, stop this repair.
Resume Milestone 1 by creating product `feature/1.1-build-foundation` from verified
main; leave Menu on main. Implement release-lock/installed-identity contracts and
static tests, retention and design records, and research the Linux build host.
The owner must approve the host choice before any infrastructure provisioning,
large disk allocation, package build, pi-gen or image build.
