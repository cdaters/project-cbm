# First runtime foundation slice — 2026-09-16

**Completed source implementation; STOP for owner review.** The owner accepted the
[appliance audit](../design/appliance-audit-2026-09-16.md) boundaries and retained
Bash + dialog. A renderer migration offered no demonstrated benefit; this slice
improves structured data, ownership and reusable interfaces instead.

## Implemented

| Product source | Responsibility |
|---|---|
| `runtime/bin/pcbm-info` | Standalone read-only text/JSON entry point |
| `runtime/project_cbm/info.py` | Injectable bounded collectors, allowlisted projection and presentation |
| `runtime/project_cbm/data.py` | Strict bounded JSON/text/profile validation |
| `runtime/project_cbm/preferences.py`, `runtime/bin/pcbm-preferences` | User-only read/validated atomic update/explicit malformed recovery |
| `runtime/data/profiles.json` | Eleven current profiles; labels, executable, chip and constrained launch metadata |
| `schemas/info.schema.json`, `preferences.schema.json`, `machine-profiles.schema.json` | Versioned developer validation contracts |
| `tests/test_runtime_foundation.py`, fixtures and benchmark | Fixture/negative/schema/atomicity/relocation tests and measured development-host costs |

Menu commit `cb6bb25db4c13f2cd241bd13ff49af083f0a1fc6` adds only `lib/pcbm-ui.sh`, its declared future install path, ten tests and
[UI/result documentation](../../../project-cbm-menu/docs/UI-CONTRACT.md). Existing
Main Menu/CONTROL hierarchy, launcher, VICE preferences, session and service policy
are unchanged. No full pcbm-config implementation or privileged backend is introduced.

The new preference file is not yet consumed by existing Menu/boot code. It is labeled
separately from current legacy configuration; effective boot mode remains unknown.
Registry consumers in this slice are info/preferences; later Menu/launcher conversion
must preserve exact profile/argument behavior and migrate legacy preference data once.
Read the [information](info-contract.md) and [preference](preferences.md) contracts.

## Validation

- Product: **75 tests PASS**, including 35 new runtime tests and 40 existing foundation/
  POC regression tests. Fixtures cover Pi 3/3A+, 4, 5, 500, 500+ and unknown future
  model strings; they are synthetic data, not hardware validation.
- Menu: **10 UI tests PASS**, existing launcher argument/exit checker PASS; 24 shell
  files pass individual Bash syntax checks. Bash 3.2 was exercised with strict mode.
- Strict schema tests, private-field exclusion, partial-report behavior, read-only
  relocated CLI, timeout/environment boundary, preferences/schema validation, write
  failures, explicit repair and retry, symlinks/permissions/root rejection and lock
  contention are covered. No old installer or release-prep tool was executed.
- JSON Schema uses the existing pinned developer requirements. Runtime dependencies
  are standard-library Python only. ShellCheck is unavailable on this host.
- No real-dialog rendering, native Linux integration run or new physical qualification
  was performed. Linux command behavior is exercised with fixtures and documented
  upstream interfaces. Future package/runtime integration must test it on Linux.

Reproduce from the product checkout using an environment with
[the pinned test dependencies](../../requirements-contracts.txt):

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
PYTHONDONTWRITEBYTECODE=1 python3 tests/benchmark_runtime_foundation.py
```

From the Menu checkout:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
bash -n lib/pcbm-ui.sh
```

The original implementation checks used the existing disposable test venv, Python
3.14.5. A fresh developer can recreate it from the requirements; its temporary pathname
is not part of the contract. Nothing was installed into macOS system Python or Lima.

## Performance measured here

Development host: owner-described M4 Pro Mac, Darwin arm64, Python 3.14.5.
[Exact measurements](performance.json) are sanitized; no raw host report retained.

| Measurement | Samples | Median | Maximum |
|---|---:|---:|---:|
| Complete fixture collection | 100 | 0.189 ms | 0.553 ms |
| CLI startup/report on Mac with unavailable Linux interfaces | 20 | 43.56 ms | 46.26 ms |
| Bash start + source helper + normalized result | 20 | 2.41 ms | 3.18 ms |

Maximum CLI resident memory observed: **22,691,840 bytes (21.64 MiB)**. Collector makes
at most two normal command attempts and one optional existing engineering DRM query.
No daemon/cache/background telemetry. Fixture timings exclude real Linux I/O and
actual tool latency; Bash measurement excludes real dialog rendering. macOS timing
needed read-only access to kernel counters outside the filesystem sandbox. These
figures establish neither a Pi budget nor equal/better Pi 3 performance. Measure Linux
and Pi 3/512 MiB Pi 3A+ at a later explicitly authorized qualification step.

## Continuity and next boundary

Frozen POC1–3 input locks/images/packages/media/qualification and all pre-existing
Git tags remain unchanged. No VM start, package/image build, POC4, optional software,
network/service enablement, physical test or push. Source branches remain product
feature/1.1-build-foundation and Menu feature/1.1-debian-package. No new tag/version
is created. A later image/package must use new source/version/input identities.

Recovery checkpoint: configured external bulk workspace,
`archive/runtime-foundation-2026-09-16`. Its manifest records both source commits,
bundle hashes, tests/performance, preservation checks and offline all-ref restoration.
It supplements previous checkpoints and does not duplicate images. This is still
one storage device; independent backup/custody is unresolved.

**Recommended next owner-authorized slice:** wire a read-only System Information view
to pcbm-info JSON and the new UI contract, then a narrowly reviewed MACHINES preference/
registry consumer migration with explicit legacy import and unchanged launcher behavior.
Decide activation/versioning together; do not imply the new preferences already affect
boot. Broad CONTROL reorganization, first-use setup, privileged settings, network/
services, boot optimization and optional applications remain later work. No image is
automatically authorized by this recommendation.
