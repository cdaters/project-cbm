# Post-release documentation and accepted design — 2026-09-24

## Scope

Owner accepted the [content and Online Library design](../design/content-ingestion-online-library.md)
in separate Product commit `2e5bb6d`. The existing [roadmap](../design/post-1.1-roadmap.md)
records the six phases and provisional 1.2.0 direction. No implementation is included.

The documentation cleanup follows in separate Product and Menu commits. It corrects
current-user entry points while preserving release snapshots and historical records.

## Public presentation

Owner authorized the existing published branches as GitHub defaults:

- Product: `feature/1.1-build-foundation`.
- Menu: `feature/1.1-debian-package`.

`main` is preserved as historical history, without merging or rewriting it. The
Product README leads with 1.1.0 and exact download/checksum links. The docs index
separates Start Here, Using Project CBM, Development and History. Menu's README
identifies source 1.1.0/package 1.1.0-1+pcbm1 and sends image users to Product.

Both READMEs use one badge-only line, a blank line, then the title. Noisy activity
badges and the misleading separate Menu-release badge were removed. Code-license
badges do not claim that artwork or the complete image is MIT-licensed.

Current manuals no longer describe publication or final physical qualification as
pending. Public source publication is distinguished from the still-incomplete initial
build bootstrap. Historical checksum instructions, packaging/interface/version notes
and dated audits are preserved with additive context. Existing images are unchanged;
C64/C128 artwork is correctly captioned as historical Covers, not emulator output.
Historical Pi 3 priorities remain in the old roadmap under an explicit historical
heading; current contributor guidance uses the Pi 4-class target.

## Validation and limits

- Repository documentation/link and shell-example syntax checker; focused parser
  regression tests for badge layout and document-relative links.
- Local Markdown links/anchors and image paths, fences, file sizes, sensitive-pattern
  scan, manual diffs and working-tree scope inspection in both repositories.
- GitHub Markdown rendering of both READMEs and the Product docs index, including
  a single badge paragraph before the title; badge SVGs and public checksum/download
  links checked. The public image was not unnecessarily downloaded or rebuilt.
- Final public default-branch/README/ref checks and unchanged release asset metadata,
  both annotated tag identities and historical main refs retained externally.
- Runtime, Menu scripts/libraries, package metadata/recipes and image construction
  files are unchanged. The only Python edits are documentation validation/tests.

Detailed counts/results, rendered HTML, exact commit/ref identities and public checks
are retained in `archive/post-1.1-design-docs-2026-09-24` under configured bulk storage.
That additive checkpoint includes Git bundles and offline restore/fsck verification.
This documentation record does not create new hardware, runtime or API qualification.
No historical recovery manifest is rewritten; independent custody remains incomplete.

## Next action

A subsequent implementation task may begin Phase 1: importer result/reporting
correctness and contracts for provisional 1.2.0. No separate 1.1.1 is created solely
for this issue. Later online qualification first requires legitimate Assembly64
access and service expectations; no other client identity or credentials may be used.
