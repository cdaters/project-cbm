# Private 1.2 development image preparation

**NON-RELEASE. Physical Pi qualification is pending.** This is a separate engineering
candidate for Phase 1–4 USB/content work. Project CBM 1.1.0 remains the published stable
release. Nothing in this procedure authorizes publication or physical flashing.

## Identity rules

The factory explicitly admits product `1.2.0-dev.N` only with candidate
`private-engineering-1.2-devN`, where N is a positive integer without leading zeros.
Runtime and Menu require their respective `1.2.0~devN-1` and
`1.2.0~devN-1+pcbm1` package identities; component development numbers can differ.
Menu must have an exact annotated `v1.2.0_devN` source tag. This is a private
component checkpoint, never a `v1.2.0` release tag. Full commits, tag object,
package/source hashes and the existing API dependency still apply.

The initial image identity is **1.2.0-dev.1 / private-engineering-1.2-dev1**;
Runtime `1.2.0~dev1-1`, Menu `1.2.0_dev1` / `1.2.0~dev1-1+pcbm1`.
The new attempt is **16**, based on verified attempt15 retained inputs.
The frozen lock hash is the build ID, independently recorded in the eventual result.

Development configuration and export suffix have separate source files:
`build/pigen/config-development.json` and `stage-cbm/EXPORT_IMAGE_DEVELOPMENT`.
The factory selects them only for the matching explicit development identity.
The image name is `project-cbm-1.2.0-dev.1`, suffix `-lite-private-1.2-dev1`.
Installed identity and the existing engineering marker carry the private candidate.
Mixed development/release identities, bare 1.2.0, missing identity pairs and mismatched
image names/suffixes are rejected. No path silently falls back to a release.

The default 1.1 `config.json` and `EXPORT_IMAGE` stay byte-identical to `v1.1.0`.
The original exact final-release version/package/tag rules remain in force. No
published ref, frozen input, package or image is rewritten. The new image has a
new lock and output directory. Historical attempt directory names are retained as
factory locators; product identity comes from the lock, not that directory spelling.

## Deployment choice

Use a **fresh private engineering image on a separate microSD card**, following the
[supported factory](official-factory-walkthrough.md). Keep the stable card intact.
The [supported upgrade model](../release/recovery.md#upgrade-or-reflash) uses a fresh
image. No supported hot-deploy command exists for this changed Runtime/Menu pair.
Copying scripts or installing packages over the qualified 1.1 card would leave a
modified system outside its frozen identity and would not establish qualification.

Required preparation: native arm64 Debian Lima/VZ and pinned pi-gen; verified external
storage/capacity; unchanged host inventory/update guards; clean committed source
exports; new Runtime/Menu binaries and corresponding source; exact reuse checks for
VICE/TCPser/OS/assets; disposable installed-package tests; freeze; isolated offline
construction; actual-image validation and raw/XZ comparison; additive source/input/
image recovery. No network client or hosted Assembly64 titles enter the image.

Image construction uses new paths `inputs/frozen-poc4-attempt16`,
`packages/poc4-attempt16`, `builds/private-1.2-dev1-attempt-16` and
`artifacts/private-1.2-dev1-attempt-16` beneath configured bulk storage.
These paths must be absent before their respective steps. Failed attempts remain
retained; a changed input set requires a new attempt and, when applicable, package
identity. Never repair a frozen image in place.

The [physical procedure](../qualification/content-1.2-pi4-usb.md) becomes ready only
after a completed image/result record supplies exact hashes and verified recovery.
Until then its status is **BLOCKED: image preparation**, not READY TO FLASH.

## Contextual macOS test failure

Exact test: `test_build_environment.BuildEnvironment.test_mktemp_regression`,
`tests/test_build_environment.py:34`. The retained final unsandboxed host run executes
284 tests: **283 PASS, one FAIL**. Its assertion is:

```text
self.assertNotEqual(old.returncode,0)
AssertionError: 0 == 0
```

The negative control deliberately supplies `TMPDIR=/builder-only/nonexistent-cbm-env-test`
and runs `/bin/sh -c 'p=$(mktemp) || exit; rm -- "$p"'`. On this macOS run it returns
zero, contrary to the test's expected Linux failure. This assertion fails before the
test's subsequent sanitized-environment command is reached. The earlier sandboxed
host pass does not establish macOS portability; sandbox effects can change the control.

This is known from the pre-ingestion September 17/18 checkpoints in
[testing](../testing.md); the test was introduced by `93d264a` for the factory
environment fix. The identical native ARM64 Linux suite passed **284/284**. The
separate retained native environment regression reproduced the actual old
mktemp/AppArmor failure and then passed with the sanitized boundary. The factory
sets TMPDIR/TMP/TEMP to `/tmp`; it does not inherit the builder's temporary paths.

The failure exposes a platform-dependent assumption in the host negative control.
It does not demonstrate a Linux/Pi runtime or ingestion defect. USB atomic writes
use the ingestion writer's exclusive temporary files and directory descriptors;
this test exercises the factory shell environment. No code/test is changed merely
to make macOS green. Retained evidence is
`qualification/content-1.2-development-2026-09-24/host-product-final.log` and
`guest-final/native-product-phase4a.log` in configured bulk storage.
