# Final architecture/reconciliation validation — 2026-09-15

Scope: documentation and ADR only. Owner accepted the earlier repository-only
cold-start comprehension review. That acceptance does not imply full kit restoration,
physical qualification or build recovery.

## Inputs and commit identification

- Product input: `7f9c4a363cf19154a9637ed8b251049bf23723e0`.
- Menu input: `c3746a12e6146f880c49979df8da2a3567200924`.
- Existing recovery/maintenance/tag identities: [provenance](provenance.md).
- Product commit subject: `Accept 1.1 foundation and reconcile project recovery scope`.
- Menu commit: `ed16b3e8ef0d43581a5a8f31b2944f869ee5c12c` —
  `Align Menu continuity with accepted product architecture`.

Resolve exact resulting IDs with `git log --format='%H %s'` in each repository.
The containing commit cannot name its own hash. Any later validation follow-up
records prior commit IDs separately. No push or release is part of this phase.
These new commits are not in the sealed historical/design bundles; a new independent
checkpoint remains future retention work. Do not mistake the older bundles for a
backup of the final architecture decision.

## Validation results

- PASS: current changed Markdown links/anchors and balanced fences; 167 local links
  checked across both repositories, including the final validation record.
- Broader repository link scan: 232 valid local links, one pre-existing missing
  image target in Menu `public-docs/README.md` (`assets/images/project-cbm-header.png`).
  That historical mirror remains unchanged; current product docs take precedence.
  This is an intentionally unresolved mirror-packaging defect, not a new broken link.
- PASS: both repository JSON files parse, reject duplicate keys/non-finite constants
  in the check, and remain documentation. The edited worksheet is explicitly not
  a release lock or executable schema. No production validator was implemented.
- PASS: 22 individual Menu script/packaging Bash syntax checks. Nothing was executed.
- PASS: both `git diff --check` checks after removing one touched whitespace defect.
- PASS: new/changed file size and secret-shape inspection plus manual diff review.
  Changes are Markdown plus one JSON design worksheet; no new binaries, private key
  contents, tokens, password hashes, historical extracts or source/build payloads.
  Existing documented public defaults are identified as historical, not newly tested.
- PASS: exact tag objects/peeled commits match the pre-phase inventories in both repos.
  Product historical audit, release notes and malformed checksum file remain byte-identical.
  All Menu scripts/config/packaging/CI/assets/public-docs bytes remain unchanged.
- PASS: read-only verification of `historical.json` (1,677 entries),
  `retained-audit.json` (296) and `prior-audit-records.json` (82) against original
  preservation manifests; no baselines regenerated and no archive writes performed.
- PASS: all four listed recovery bundles were rehashed; the existing design checkpoint
  checksum and all 11 payloads match. [Exact locators/digests](provenance.md#recovery-bundle-locators-and-digests).
- Upstream source links were accessed during research on 2026-09-15. The ADR explicitly
  identifies the Pi 3 Buildroot moving-source fallback where the tagged file could
  not be fetched; no version/commit was invented as a frozen CBM input.

The architecture decision is accepted; physical qualification remains UNTESTED.
Independent backup/custody, Linux bootstrap, signing custody, SBOM choice, measured
acceptance budgets, original v1.0 input closure and build-chain gaps remain open.
The phase creates no packages, first-boot code, pcbm-info, builder, image or release.
No runtime/service/privilege change, historical mutation or push occurred.
