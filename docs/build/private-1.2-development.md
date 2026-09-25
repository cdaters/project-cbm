# Private 1.2 development image preparation

**NON-RELEASE. Physical Pi qualification is pending.** This is a separate engineering
candidate for Phase 1–4 USB/content work. Project CBM 1.1.0 remains the published stable
release. Nothing in this procedure authorizes publication or physical flashing.

## Attempt18 construction and validation correction — 2026-09-25

The preserved builder resumed without package drift. Native Product300/Menu107
logs belong to clean exact source checkouts; staged attempt18 archives match the
canonical commits byte-for-byte. Full capability, Runtime reuse, retained predecessor
and authenticated refresh gates passed. No prior attempt18 kit/image existed.
Freeze18 produced lock/build ID
`4d8bfbea304b5505b51f4fc4fab8cbf66541bea70fdc8a54f1f1287675863a79`.
The isolated frozen construction completed successfully, without rebuilding packages.

The first read-only validation stopped on four false legacy-account expectations in
`validate_activation.py`: activation policy, owner UID, helper group and SID working
path. The parent validator already selected the development single-account layout;
this nested validator did not. Separate read-only evidence confirms `pcbm` UID1000,
no `pi`, `system_ready: false`, the required operator membership and a byte-identical
SID disk owned by UID1000. The correction uses existing strict development identity
admission and retains every check, including rejection of wrong UID/readiness/group.
Stable and historical account models have focused regression coverage.

The failed report stays at `qualification/content-1.2-dev1-attempt18`. Corrected
validation is a later external attestation from separately committed source, with a
new evidence directory. It does not alter attempt18's frozen lock, recipes, packages
or image. No second image construction is warranted by this validator-only fix.
The source checkpoint is still **BLOCKED: final image validation and recovery**.

The corrected main validation then passed, as did filesystem/ELF and supplemental
checks. The inherited content validator exposed a second inspection-only defect:
its AST lookup expected `HOST_METADATA` inside the old importer, but 1.2 imports
the unchanged policy from `usb_discovery.py`. It stopped before a result. The
correction verifies the exact relative import and reads the installed shared policy
without executing it. Tests reject missing/broadened metadata policies and cover
both the stable inline and development shared definitions. Those successful checks
remain retained; only unfinished checks need continuing. A transfer-permission
harness failure created an empty validation2 directory before image inspection;
it and its log are retained separately from validation3 results.

## Retained failed attempts and authenticated retry

Attempt16 froze Product `aefc08e`, Menu `7c12a40` / annotated private
`v1.2.0_dev1` (`b9f94546e166df32849ec7d2143477dc8b1fa8e5`). Lock:
`ff3a1a156003c73e343457a3b5092abdac98c28574549607837bb185d8edc844`.
Construction stopped at stage0 APT update: the retained updates/security InRelease
files expired on September 22. No image was produced. The failed kit, tree and log
remain intact. Builder inventory/update guards passed after the failure. Signature
and expiry checking were not disabled, and the clock was not changed.

The legitimate retry was **attempt17**, with a new lock and output directory, retaining
the same private development product identity and exact unchanged Runtime/Menu packages.
Current signed updates metadata has identical index hashes. Current signed security
metadata advertises one newer package among the 672 installed packages:
`mkvtoolnix 92.0-1` → `92.0-1+deb13u1`. A disposable read-only-image overlay ran normal
APT update and a resolver simulation requiring exactly that one update, then downloaded
its binary and complete corresponding source. No builder or stable-image package was
installed or upgraded. This is a documented new 1.2 input set, not a claim that it
reconstructs 1.1 from identical inputs.

The bounded acquisition recipe is `tools/acquire_development_apt.py`. Its new
`inputs/apt-refresh-dev1-20260925` directory records transport bytes, normal APT
authentication, resolver output and binary/source downloads. The freeze verifier
independently checks current Sequoia signatures using the pinned host keyring, Date/
Valid-Until, signed index hashes and every admitted binary/source hash. Inherited
non-security repository inputs stay identical. The refresh flag is rejected for
the 1.1 release path. No unsigned package, expired-metadata exception, permissive
APT option or ambient crypto-policy override is used.

The newly acquired updates/security metadata is valid until October 2, 2026, at
02:07:43 / 03:12:56 UTC respectively. Later construction still enforces expiry;
the procedure is not a perpetual waiver. The source helper admits only the reviewed
mkvtoolnix version; another delta requires a separately reviewed input set.

Native prebuild Product289 and Menu107 passed; installed development packages passed
integrity/dependency/sudo checks, twelve lifecycle tests, seven Cover decodes, three
terminal-return cycles, FAT/ext4 ingestion and MC PTY/broker release. Initial native
staging missed the sibling Menu checkout. Separate harness retries corrected host-guard
observation inside a PID namespace and a busy `/usr` bind during teardown. Failed logs
are retained; corrected cleanup released every test mount/loop, and the stable raw
image remained `6c9b7599461a41f6ab30b666dd718329c34f863f11a46dfd20d61fe9830d2468`.
These are native results, not physical Pi qualification.

Attempt17 stopped during freeze, before writing a lock or constructing an image:
the Runtime-reuse check compared Git tar permissions (0664/0775) with safe-extracted
recipe permissions (0644/0755). All 65 compared file payloads were identical. The
partial kit remains preserved. The development-only reuse path now compares the
permissions produced by the same `tarfile.data_filter` used for extraction; changed
bytes and executable bits still fail. The historical 1.1 default comparison is
unchanged. The new retry is **attempt18**, using the last complete kit, attempt16,
and the independently authenticated refresh. Attempt17 is not a usable predecessor.
Host Product297 ran with only the known mktemp control failure; native Product297
passed before this small comparison correction. Three additional reuse tests cover
the correction and rejection behavior.

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
Initial attempt **16** used verified attempt15 inputs; the authenticated retry is **18**.
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

The retry uses new paths `inputs/frozen-poc4-attempt18`,
`builds/private-1.2-dev1-attempt-18` and `artifacts/private-1.2-dev1-attempt-18`
beneath configured bulk storage. Exact unchanged development packages remain in
`packages/poc4-attempt16`; no duplicate package with the same version is rebuilt.
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
An independent host observation confirmed `/usr/bin/mktemp` created a file in the
macOS per-user temporary directory and returned zero for both the invalid-control
and sanitized environments. Each probe removed only the temporary file it created.

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
