# Post-1.1.0 work

These owner-deferred items do not block Project CBM 1.1.0 and are not included features:

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
