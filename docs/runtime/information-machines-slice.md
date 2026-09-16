# System Information and machine consumers — 2026-09-16

**Completed source slice; STOP for owner review.** This implements only the owner-approved
System Information, registry/MACHINES/default preference migration and RUN validation.
No image/package build, POC4, frozen candidate change, new hardware test or publication.

Menu implementation commit: `4feda57c2ff1f5d0807a6873c0b88b5d84435bd8`.
The external checkpoint records the corresponding final product commit without a
self-referential in-repository checksum.

## What changed

- CONTROL gains **INFO — System Information**, with four concise groups, scrolling,
  complete wrapped values and graceful missing/partial information. One pcbm-info JSON
  collection supplies the view; no UI hardware/version probes. Existing SYSTEM/SHOW
  remains the future About cleanup location; no large About subsystem is added.
- MACHINES retains direct launch and DEFAULT selection. Lists/current marker come from
  the product registry. Saving a default returns directly to Main Menu with its label;
  the redundant success dialog and extra Back step are removed. No root/sudo.
- Valid user preferences win; only missing state imports a validated legacy ID under
  the writer lock. Legacy data stays intact. Malformed preferences use a stated safe
  fallback and require confirmation for backed-up recovery. Concurrent completed
  selections cannot be overwritten by a stale initialization attempt.
- RUN, no-argument pcbm-boot and shared content selection use the resolved default.
  The launcher and cover selection use validated registry metadata. Ten approved VICE
  entry points cover eleven profiles; the C128 80-column flag remains explicit.
  Audio, F10, geometry, session, diagnostic and content paths remain configured as before.
- Boot preferences are still inactive. No broad configuration or privileged backend
  changes occurred. Future packaging must install matching product commands and encode
  their versioned dependency before attempting a candidate; old tags remain immutable.

Read the [user guide](information-and-machines.md), [consumer interface](information-machines-contract.md),
[preferences](preferences.md), and [information schema](../../schemas/info.schema.json).

## Checks and evidence limits

[Validation summary](information-machines-validation.json) and [synthetic screen example](information-example.txt).

- **86 product tests PASS**: existing builder/recovery/POC regression checks plus fixture
  info/schema/prefs tests and eleven new selection/migration/registry interface tests.
- **26 Menu tests PASS**, plus the existing shared-launcher executable checker. They
  cover structured projection, missing/partial/future-model data, unknown/null values,
  malformed JSON, secret/control exclusions, wrapped long values, 40/80/larger layouts,
  navigation results, registry listing/current marking, save/cancel/recovery/failure,
  actual Main Menu RUN/return dispatch, C128 80-column argv and executable injection.
- Existing preference tests retain atomic replacement, lock contention, failed-write,
  ownership/mode/symlink/root refusal coverage. Static success does not establish
  power-loss durability on Pi media.
- Per-file Bash syntax, Python/JSON syntax, schemas, changed-document local links,
  whitespace, staged sizes/private-pattern review and immutable tag comparison pass.
  ShellCheck remains unavailable; no full shell-lint pass is claimed.
- Mac arm64, Python 3.14.5, Bash 3.2. **No actual dialog rendering, native Linux package
  integration, physical Pi performance or new hardware qualification**. Fixtures and
  fake commands never launch VICE or run sudo. All prior physical POC3 results still
  refer only to its frozen source/package/image, not this new source slice.

[Exact performance samples](information-machines-performance.json) include collection,
JSON preparation, profile validation, preference reads/atomic writes, CLI startup and
full entry scripts with fake dialog. The integrated information timing uses fixture
input; add real collection cost when planning the actual UI. Python process startup is
larger than in-process parsing; Main Menu now fetches ID+label once rather than twice.
No daemon/cache or background probe loop. Re-measure on Linux/Pi 3 and 512 MiB Pi 3A+
when separately authorized; these numbers do not prove equal/better Pi response.

From sibling source checkouts, with the product's pinned developer requirements:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
PYTHONDONTWRITEBYTECODE=1 python3 tests/benchmark_information_machines.py
```

Run unittest discovery separately in Menu as well. Its cross-repository consumer tests
need the product checkout and the same test environment. Runtime needs Python standard
library only; jsonschema and fixture modules are developer dependencies, not image data.

## Preservation and recovery

Source branches: product `feature/1.1-build-foundation`, Menu
`feature/1.1-debian-package`. No new package versions/tags or pushes. POC1/2 preservation
baseline **5,503 entries** matches; POC3 lock/raw/XZ and **2,789 frozen input objects**
match their retained hashes. Formal/pre-existing tags and peeled targets are unchanged.
No historical evidence or qualification record was edited. No photos/images/binaries
were added to source control.

New external checkpoint: `archive/information-machines-2026-09-16` under configured bulk
storage. The manifest records exact commits, bundles/checksums, all refs/peeled tags,
validation and performance evidence; offline mirrors verify all-ref restoration and
Git fsck. Preservation report: `qualification/information-machines-2026-09-16/preservation.json`.
Previous checkpoints remain intact. The checkpoint is on TheBench, **not an independent
backup**; independent custody/restore remains unresolved. No image duplication.

## Exact next recommended slice

Owner review, then a bounded **About and current-status cleanup**: use this structured
information authority for existing version/status displays, separate concise credits/
licenses/links from System Information, and retire stale duplicate probes/claims. Keep
larger CONTROL/navigation/privileged settings changes separate. Before any future image,
assign new source/package versions and a product-runtime dependency, validate staged
installation on Linux and record new immutable inputs. POC4 is not authorized here.

The later boot-preference activation must migrate or retire dormant `pcbm-start`
first. Network/services/first boot, broad privilege redesign, boot optimization,
optional software and other hardware qualification remain later owner-approved work.
