# Project CBM 1.1.0 — exact publication review plan

Status: **READY FOR PUBLICATION AUTHORIZATION**. This document is a proposal;
no push, upload or release creation is authorized or performed.

## Qualified identities

The [final result](final-1.1.0.json) records attempt15's raw/XZ, package and lock
hashes. [Owner final Pi 4 B attestation](../qualification/final-1.1.0-pi4-owner-pass.json)
records **PASS**, including live CCGMS/TCPser BBS operation, reboot/persistence and
shutdown. [RC4 owner acceptance](../qualification/rc4-owner-release-acceptance.json)
remains PASS. No test is repeated and the Pi is shut down.

Product branch: `feature/1.1-build-foundation`. Its final documentation commit is
recorded as `product.head` in the external `publication-plan.json` listed below,
avoiding a commit hashing itself. Product annotated `v1.1.0` remains object
`627937867f59b76ea5c3c96fdbb14ebd47ed507f`, peeled commit
`787c275005aaf2c03b2ed769edc815a34ccafc9f`.

Menu branch: `feature/1.1-debian-package`, HEAD
`7df45cf40eae1ca64cd5740e4b93347e3717bdb4`; annotated `v1.1.0` remains object
`9f471a2ddd7492d041d9563809e301da9c79ed57`, peeled to that same commit.
Runtime `1.1.0-1` and Menu `1.1.0-1+pcbm1` packages remain frozen and unchanged.
Later Product commits contain documentation/governance/qualification, not new
image inputs. The clarified manuals do not replace documentation inside the image.

## Exact public assets

All paths in the table are relative to configured bulk storage:
`releases/1.1.0-publication-review-2026-09-24/`.
On this host the complete prefix is
`/Volumes/TheBench/ProjectCBM-Work/releases/1.1.0-publication-review-2026-09-24/`.
**Attach each of these 20 files to the Product GitHub Release.** No directory
wildcard, private recovery bundle, lock/kit, development directory or other file
is part of the upload plan. `SHA256SUMS` binds the other 19 assets; the manifest
binds the 18 payload files, keeping the checksum graph acyclic.

| Exact relative file | Intended public disposition |
| --- | --- |
| `project-cbm-1.1.0.img.xz` | Primary downloadable flash image; unchanged qualified bytes |
| `SHA256SUMS` | SHA-256 download checksums; not a signature |
| `RELEASE-MANIFEST.json` | Asset identities, raw image reference, source tags and qualification |
| `RELEASE-NOTES.md` | Attach and use its exact text as the GitHub Release body |
| `README.txt` | Release-set use, verification and source overview |
| `LICENSE.md` | Project license; separate artwork terms retained |
| `NOTICES.txt` | Component notices and rights/provenance pointers |
| `COMPONENT-INVENTORY.json` | Exact Runtime/Menu/VICE/TCPser and optional-component identities |
| `installed-packages.json` | Exact final-image 672-package inventory, machine-readable |
| `installed-packages.tsv` | Same final installed package inventory, tabular |
| `SOURCE-INVENTORY.json` | Retained corresponding-source provenance/hashes |
| `SOURCE-README.txt` | How to use accompanying source archives and source refs |
| `project-cbm-1.1.0-component-sources.tar.gz` | Exact retained VICE/TCPser recipes, patches, sources; CCGMS/SID-Wizard source/notices |
| `project-cbm-1.1.0-os-sources-01.tar` | Exact retained OS source artifacts, part 1; upload all three parts |
| `project-cbm-1.1.0-os-sources-02.tar` | OS corresponding source, part 2 |
| `project-cbm-1.1.0-os-sources-03.tar` | OS corresponding source, part 3 |
| `project-cbm-runtime-1.1.0-sources.tar` | Exact frozen Runtime corresponding Debian source package |
| `project-cbm-menu-1.1.0-sources.tar` | Exact frozen Menu corresponding Debian source package |
| `project-cbm-1.1.0-docs.tar.gz` | Complete release manual set below, including CCGMS clarification |
| `QUALIFICATION.json` | Sanitized exact-image owner PASS attestation; no remote BBS identity |

The raw image **should not be uploaded publicly**. Retain it for recovery and
local flashing at `releases/1.1.0/project-cbm-1.1.0.img` (3,095,396,352 bytes,
SHA-256 `6c9b7599461a41f6ab30b666dd718329c34f863f11a46dfd20d61fe9830d2468`).
The public XZ is 599,290,700 bytes, SHA-256
`8b3738a204da16e148f5674a95f1ffb55a67b8ad1ce1d997b1858594a899c13d`.
Decompressing it supplies that raw image; no second image download is needed.

### Exact manual archive members

`project-cbm-1.1.0-docs.tar.gz` contains these ordinary files, with no Finder
metadata, Git state, host paths or private records:

- `docs/README.md`
- `docs/release/accounts-and-layout.md`
- `docs/release/boot.md`
- `docs/release/build-your-own.md`
- `docs/release/content.md`
- `docs/release/customization.md`
- `docs/release/development.md`
- `docs/release/factory.md`
- `docs/release/getting-started.md`
- `docs/release/installed-packages.json`
- `docs/release/networking.md`
- `docs/release/recovery.md`
- `docs/release/release-notes-1.1.0.md`
- `docs/release/release-policy.md`
- `docs/release/screenshot-checklist.md`
- `docs/release/software-components.md`
- `docs/release/troubleshooting.md`
- `docs/release/user-guide.md`
- `docs/release/vice.md`

Most manual bytes are reused from verified staging, including its final-image
package inventory and portable technical links. The networking guide, user guide
and release notes receive the small documentation update; the archive index is
made publication-neutral. Existing frozen source archives are copied byte-for-byte.
GitHub's automatically generated tag source archives are supplementary; they do
not replace any corresponding-source assets in this list.

## Proposed Git/GitHub operations — only after authorization

1. Recheck the reviewed local hashes and exact remote refs. If an existing remote
   branch/tag/release conflicts, stop for review; do not force or replace it.
2. Push only Product's reviewed documentation HEAD to
   `cdaters/project-cbm:refs/heads/feature/1.1-build-foundation` and its existing
   annotated `refs/tags/v1.1.0` object. Do not move the tag to the documentation HEAD.
3. Push only Menu commit `7df45cf40eae1ca64cd5740e4b93347e3717bdb4` to
   `cdaters/project-cbm-menu:refs/heads/feature/1.1-debian-package` and its existing
   annotated `refs/tags/v1.1.0` object. No private candidate tags or other branches
   are included, and neither repository's `main` is changed by this plan.
4. Create one public, non-prerelease GitHub Release in **cdaters/project-cbm**,
   tag **v1.1.0**, title **Project CBM 1.1.0**. Attach exactly the 20 files above.
   No separate Menu GitHub Release is proposed.
5. Use the exact prepared `RELEASE-NOTES.md` bytes as the body, with no generated
   changelog or added claims. Its source is this commit's
   `docs/release/release-notes-1.1.0.md`; relative documentation links are converted
   to immutable URLs at the reviewed Product documentation commit. The exact
   text and hash are available in the review set before authorization.
6. Verify public asset hashes and published tag objects after upload; record the
   actual publication result separately. This is a future action, not a claimed pass.

## Verification and retained records

External evidence: `qualification/final-1.1.0/publication-review-2026-09-24/`.
Its `publication-plan.json` records exact reviewed branch HEADs, tag objects,
release name/body source and every asset path/hash/size. Validation includes the
original staging manifest and checksums, frozen lock and package hashes, new
asset checksums, documentation links/JSON/privacy and unchanged binary identities.
The prior actual-image/raw-XZ/equivalence gates remain PASS; no construction,
package test or physical check is repeated for documentation-only changes.

Additive recovery: `archive/final-1.1.0-publication-review-2026-09-24/` with bundles,
exact refs, offline restoration/fsck and a manifest/checksum. Earlier sealed
release staging/recovery is preserved. Optional/deferred work remains as previously
accepted. No genuine release blocker remains; **only owner publication authorization**.

Commits pushed: **NO**. Tags pushed: **NO**. GitHub Release created: **NO**.
Public image uploaded: **NO**. Anything published: **NO**.
