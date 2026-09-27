# Project CBM roadmap

## Implemented for 1.2

- Search Assembly64, filter results, read details and save selected files locally.
- Import selected USB files after scanning and reviewing the destination.
- Browse USB safely in Midnight Commander, then explicitly unmount.
- Take screenshots over SSH, including supported VICE/gameplay and Covers.
- Start at Menu or directly in the current RUN machine; return with F10/Quit.
- Clearer sizes, friendly labels and predictable Back/Parent navigation.

The final 1.2 image still requires its focused physical regression before publication.
See [release notes](../release/release-notes-1.2.0.md) and [current state](../../CURRENT-STATE.md).

## Later work

Save & Run in one step; Recent Additions UI; explicit ROM management; selectable
compatible public servers; additional Pi models/peripherals; public first-build
bootstrap; release signing and standardized software inventories. These are not
promised 1.2 features. FTP remains reference-only, never an automatic fallback.

## Historical acceptance records

The dated text below records planning for 1.1/1.2; its future-tense implementation
and admission status has been superseded by the completed features above.

# Post-1.1.0 work (historical)

## 1.2.0 implementation — 2026-09-24

The owner has now authorized incremental implementation. Phases 1–4 implement result reporting, shared ingestion, bounded USB discovery/
selection, the CONTENT interface and separate read-only FILES USB browsing; see the [development contract](../runtime/ingestion-contract.md)
and [current checkpoint](../../CURRENT-STATE.md). Physical qualification remains pending. Assembly64 remains access-gated. No 1.2.0 release or qualification is
claimed. The acceptance-era backlog below is retained as historical scope.


These owner-deferred items do not block Project CBM 1.1.0 and are not included features:

Owner-accepted design (2026-09-24): [Content ingestion and Online Library](content-ingestion-online-library.md).
It develops the existing online/USB items below; all future behavior remains
unimplemented and the published 1.1.0 release is unchanged. The provisional feature
target is **1.2.0**, with reporting/contracts → shared primitives and USB selection
→ CONTENT UX → read-only FILES browsing → legitimate-access-gated Online Library
→ Save & Run. No separate 1.1.1 is planned solely for the reporting defect. CONTENT
will own the sole normal USB Import entry; Online Library names Assembly64 inside
the feature. No implementation, new tag or release is authorized by this record.

- **Project CBM Online Library / Assembly64**: investigate search, results/details,
  optional downloads into `/home/pcbm/content`, and Download & Run through existing
  profile routing. Future design must address service terms, content rights and safety.
- Complete public source-to-image bootstrap/tooling.
- Cryptographic release signing and standardized SPDX/CycloneDX SBOM generation.
- Additional physical model/peripheral qualification and documentation screenshots.
- Optional later CCGMS Future evaluation, without changing the accepted 2021 release.

New contrary evidence about correctness, privacy or distribution may require review;
missing optional work alone does not reopen the 1.1.0 release scope.

## USB import and content ingestion — owner deferred, 2026-09-24

The owner accepts whole-selected-partition recursive import and automatic safe
unmount for 1.1.0. The reporting defect below is a known nonblocking limitation;
it does not justify another immutable candidate. See the
[owner disposition](../qualification/final-1.1.0-usb-import-disposition.md).

1. **Fix `import_client.py` result/reporting loss.** Preserve validated
   `ignored_metadata` counts and structured failure/unmount information across
   the broker/client/Menu boundary. Currently success drops the metadata count;
   failure becomes a generic result and loses `error`/`source_unmounted`, causing
   conservative drive-release feedback. Retain bounded validation and sanitized
   errors. Verify the complete boundary for success, partial failure, successful
   cleanup and failed unmount; do not infer successful release from missing data.
2. **Redesign USB selection UX.** Discover and preview eligible content, then let
   the user select files/folders before copying. Make scan scope, classification,
   destination and collision behavior explicit. This is future design work only.
3. **Consider shared content ingestion for USB and future Assembly64.** Evaluate
   discovery → classification → selection → destination → collision handling →
   import/results. Preserve source-specific access, privilege and rights rules;
   this consideration neither implements Assembly64 nor authorizes downloads.
4. **Consider explicit USB browsing for FILES / Midnight Commander.** Design a
   deliberate mount/browse/safe-eject workflow separate from IMPORT's temporary
   read-only mount and automatic unmount. Define ownership and cleanup before
   changing either workflow.
