# Milestone 1 checkpoint: awaiting build-host approval

Date: 2026-09-15. **This is the first implementation checkpoint, not a completed POC.**
The owner must select/approve the [Linux build-host proposal](linux-build-host-study.md)
before infrastructure installation, VM/disk allocation, package construction, pi-gen
or image building. No runtime/service/privilege/content-management behavior changed.

## What exists

- [Input/identity/workspace contracts](contracts.md): three JSON Schemas, strict offline
  reader/semantic validator, minimal-identity generator, read-only workspace guard,
  synthetic lock/identity fixtures and 15 unittest cases. Initial test-first run failed
  because the implementation was absent; the final suite passes without network.
- [Input-retention policy](input-retention.md): must/should/cache/excluded classes,
  package/source/host closure and independent recovery responsibilities.
- [Package and stage design](package-and-stage-design.md): versioned external Debian
  packages, component/product ownership and the smallest eventual Lite integration.
- [First-boot/footprint design](first-boot-and-footprint.md): sealing/initialization
  split, retry/actual-root requirements and measured capacity gates.
- [Host study](linux-build-host-study.md): viable choices, evidence, recommendation,
  storage/cache implications, estimates and reconstruction plan. No runnable VM or
  provisioning config silently commits the owner to a choice.

## Git inputs and publication

Product branch was created from published main
`29933789ec8d29bd55f2b00cbcf309132058413f`. Menu remains published main
`bb4f24fadae6e852bf29fb0e32ad8ced9db7268c`; no Menu feature branch or implementation.
Product contract commit is `e4d1556`; the following design/checkpoint commit is the
feature tip recorded by the external checkpoint. No feature-branch push or merge.

Both main branches and Menu maintenance/recovery refs are public. Product
maintenance/1.0 remains local/bundled by explicit owner decision after GH007 on
historical email metadata; public product v1.0.0 is the authoritative maintenance
baseline. No retry, historical rewrite, formal-tag mutation or privacy-setting change.
See [privacy reconciliation](../privacy-reconciliation-2026-09-15.md).

## Validation and evidence limits

PASS: 15 unittest cases (with negative mutation subcases), all three schemas checked
against Draft 2020-12, deterministic fixture identity, direct retained-file integrity,
workspace failure cases and exact published product/Menu tag regressions. JSON parsing
rejects duplicate keys, floats/non-finite values and BOMs. Tests use synthetic inputs,
not real candidate packages or a rootfs. The workspace mount tests inject observations;
no actual workspace registration/VM filesystem was created.

Static completion checks passed: 55 current-document local links/anchors, all 8
repository JSON files, both new Python files parsed, diff whitespace and secret/size
checks. Largest existing files are 217,571 product bytes and 361,069 Menu bytes; no
large binary was added. Checks cover
Python syntax, git diff whitespace, added-file sizes and secret shapes, protected
historical/runtime paths and both repositories' tags/status. Dependency wheels, exact
pi-gen research file identities, outputs and source bundles are retained in the external
checkpoint. Small Python-only validation dependencies were installed under /tmp in an
isolated venv; no Mac system package or Linux host infrastructure was installed.

The current tool verifies direct input descriptors, not the contents of transitive
closure catalogs, actual package control metadata, source tag/object agreement or
full external output/qualification graphs. Those are explicit acquisition/packaging/
attestation tasks before assembly. No real release lock, production Menu candidate,
VICE authenticated source choice or full Raspberry Pi package closure is claimed.
No physical Pi qualification or comparative VM benchmark has occurred.

## Recovery checkpoint and exact next step

A new external archive, relative to configured archive root:
`milestone1-contracts-2026-09-15/`. Its README and checkpoint.json identify all accepted
refs/bundles, validation results, dependency/research artifacts and source hashes; the
checkpoint digest is stored separately. Restore into fresh mirrors and compare refs,
fsck and the recovered-script hashes. The separate completed-publication checkpoint
under `privacy-reconciliation-2026-09-15/published/` remains unchanged. Earlier repair,
partial-publication, architecture and original historical records retain their meaning.

The feature checkpoint is local/TheBench only, not independently encrypted/off-site.
No large image artifacts were copied. Full loss-of-builder/upstream reconstruction,
independent custody, signing custody, SBOM selection, measured acceptance budgets and
historical v1.0 input/build-chain gaps remain unresolved.

**Next action: owner choice of build host.** Recommendation is Lima/VZ plain Debian
arm64, 8 vCPUs, 12 GiB RAM and a 160 GiB sparse external disk, with explicit external
cache placement and a 256 GiB free-space preflight. UTM is the strongest alternative.
Once approved, pin/retain bootstrap/tool inputs, register guarded storage, provision
only the approved host, run Linux capability probes, then implement package recipes
and the small stage under separately reviewable changes. Resolve candidate service/
account/first-boot policy before assembly. Do not infer approval from elapsed time.
