# Validation and qualification

Run2/source continuation (2026-09-17): [review and limits](qualification/poc4-run2-source-review-2026-09-17.md).
Final retained host run: Product 155 tests, 154 PASS; unchanged unsandboxed macOS
`test_mktemp_regression` expectation FAIL. Menu 70/70 PASS. Nine focused lifecycle
tests cover pre-Cover keyboard baseline, actual host PTY three-cycle termios restoration,
failure-open status, missing renderer, timeout/escalation/reap, per-operation restoration
failure, no forced foreground/foreign VT ownership, and signal cancellation. First-boot
tests cover Back/change, mismatch/invalid retry, Wi-Fi retry/alternate/offline/resume,
working feedback before backend, narrow setup gates and secret/malformed-response bounds.
Host tests do not prove physical KMS/VT/visible Cover or real Wi-Fi/account behavior.
Next native/package/candidate/physical gates remain in the linked report; no build here.

Current 2026-09-17 checkpoint: [POC4 physical-regression investigation](qualification/poc4-regression-investigation-2026-09-17.md).
The exact attempt #3 owner report establishes missing Cover and post-VICE keyboard/VT
FAIL, despite successful VICE/F10/Quit/visual return. No cause or corrected candidate
is qualified. Source baseline: Menu 65/65 PASS; Product 142/143 PASS with one existing
macOS mktemp expectation failure. New [physical procedure](qualification/poc4-next-candidate-regression-draft.md)
is an unbound NOT READY TO FLASH draft. [Existing-card evidence collection](qualification/poc4-regression-collect-evidence.md)
is the next owner action; no automatic retest. Earlier checkpoint claims below are historical.

Current bounded result: [POC4 attempt #3](build/poc4-attempt3-owner-review.md): 143 Product,
65 Menu plus launcher checker PASS; actual native ARM64 package/owner/backend/service/
USB-loop/Cover/utility/environment checks PASS within stated limits. Construction is
automatic-approval blocked, so new-image offline tests NOT RUN and physical UNTESTED.
The attempt #3 procedure remains an unbound draft; no flash instruction yet.


Latest build checkpoint: [POC4 attempt #2](build/private-poc4-attempt2.md): 142 product
and 50 Menu tests plus launcher checker; native environment/package/runtime revalidation;
121 main + 20 supplemental offline checks; FAT/ext4/systemd and 113 ELF objects PASS.
[Environment regression](../tests/native/build_environment.sh) reproduces the old actual
AppArmor failure before verifying the corrected boundary. Native namespaces/fixture
results do not certify Pi first boot, peripherals, networking or optional applications.
Follow only the [exact-hash Pi 3B procedure](qualification/poc4-attempt2-pi3b-smoke-test.md)
after owner review. Preserve original attempt #1 and POC1–3 records unchanged.

Latest source checkpoint: [configuration maturation](runtime/configuration-maturation.md).
Current bundles/manifests and offline restore evidence are under configured bulk
storage at `archive/configuration-maturation-2026-09-16`. The earlier checkpoints
remain unchanged. Source implementation is not a new installed/qualified image.


Current physical checkpoint: [POC3 owner attestation](qualification/poc3-pi3b-owner-report-2026-09-16.json)
records the bounded Pi 3B pass, including corrected geometry and joystick. The
[completed build](build/private-poc3.md) and [planned procedure](qualification/poc3-pi3b-smoke-test.md)
remain unchanged. Photos and owner observations have separate evidence limits.
[Product audit](design/appliance-audit-2026-09-16.md) proposes next work; no new runtime
or additional-model qualification is authorized. Earlier sections retain their dated
checkpoint scope; they do not override CURRENT-STATE.

## Safe checks for continuity/source work

- Run `git diff --check` and inspect staged paths/sizes and diff. Validate added
  JSON and local documentation links. Scan new files for private keys, token shapes,
  password hashes and accidental history/identity material without printing contents.
- Syntax-check each shell file individually. In project-cbm-menu:

  ```bash
  for f in scripts/pcbm-* packaging/*.sh; do bash -n "$f" || exit; done
  ```

  Syntax checks do not execute the scripts. Use ShellCheck when available and
  distinguish existing findings from regressions. It was unavailable in this phase.
- Never use an installer, docs-sync, release-prep or hardware/service command as
  a harmless static check. No installer, packaging build or runtime was run here.
- For runtime work, add focused tests for relevant launcher, service, mount,
  error/cancel, config and packaging/version behavior. The old CI only packages ZIPs.

## Preservation verification

`tools/preservation-inventory.py verify MANIFEST.json` reads the recorded tree
and detects changes/loss/additions in file bytes, paths/types, modes, mtimes and
xattr hashes, without following symlinks. It does not promise ACL/ownership/atime
preservation. Detailed manifests are private external records, not publication inputs.
Anchor hashes are in [preservation-manifests.json](preservation-manifests.json).
Use the recorded script against historical, retained-audit and prior-audit-records
manifests on TheBench; do not regenerate a baseline to hide a mismatch.

Git bundles must pass `git bundle verify`; complete before-local .git archives also
retain reflogs/config/unreachable objects. Check existing tag objects/peeled commits
against [provenance](provenance.md). Recovery blob hashes must match all 17 original
image extracts. Full verification results are recorded in the external phase archive.

## Hardware policy and matrix

Retain the full [audit hardware and comparison matrix](audit-2026-09-15.md#j-hardware-and-qualification-matrix).
It covers Pi 3B, 3A+ (512 MiB), 3B+, 4B, 400, 5, 500 and 500+. All remain
unqualified by this work. Pi 3 is the performance floor; do not silently use x64
instead of x64sc to hide a regression. CM/Zero models are not automatically added.

Compare exact 1.0.0 Trixie against frozen 1.1 candidates with equivalent hardware,
power, cooling, display, storage and licensed content. Record image hashes, board
revision/RAM, EEPROM/kernel/firmware, VICE config, display/audio/controller identity
and throttling. Separate first boot from steady state; use >=10 boot/launch runs,
median and worst case. The audit's tentative thresholds are review triggers, not
measured guarantees. Measure Pi 3 RAM/swap and audio continuity early.

Qualify boot/expansion/offline operation, VICE machines/media, graphics/audio/input,
USB import, storage types, service/credential policy, IP232, power, backup/restore,
two-flash identity and release integrity. Keep per-candidate results in
/Volumes/TheBench/ProjectCBM-Work/qualification and commit small summaries here.
No physical tests were performed during audit or preservation.

## Black-box recovery acceptance

The [recovery test matrix](recovery.md#8-acceptance-tests-and-current-evidence) adds
context-free handoff, offline bundle restore, mounted-image identity, lost-builder/
upstream reconstruction, metadata agreement, privacy negatives, old-schema reading,
qualification binding, hash-cycle rejection, relocation and independent-backup drills.
A build passing syntax checks does not meet these gates. The accepted preservation
bundles passed the actual offline all-ref/17-script restore test in this design pass.
No 1.1 image/schema/runtime test is claimed; those components do not exist yet.
Keep PASS/FAIL/UNTESTED/BLOCKED and exact candidate/test-suite identity in records.

## Architecture and footprint qualification for 1.1

[ADR-0001](adr/0001-base-distribution-and-image-architecture.md) is accepted design,
not measured performance. Compare the same VICE workloads, services, display and
storage settings. Do not compare a reduced-feature alternative with the full appliance.

Record raw/XZ bytes, filesystem capacity/used bytes before and after first boot,
runtime/development package inventory, installed identity size, free user-data bytes,
peak initialization/update space and steady-state log/cache/swap growth. No 8 GB
minimum is mandated. Agree safe free-space margin from measurements and publish the
minimum usable storage bytes, not only a nominal card label. Test full-disk behavior,
import/save/config failures and safe user recovery. No compiler/source/cache/recovery
archive belongs in a public image without an explicit runtime need.

Test the selected single-root expansion on SD, USB and NVMe where targeted; interrupted
and repeated initialization; absence of cloned identity on two flashes; unclean power;
verified backup/reflash/restore; package-update interruption; Samba and Unix credentials
independently in both change directions. Record actual enabled/active/listening states
for SSH/Samba/TCPser/Avahi against the declared candidate policy. All remain unperformed.

The owner accepted the repository-only cold-start comprehension review on 2026-09-15.
This is a project-continuity pass, not independent archive restore, Linux bootstrap,
image-side identity validation or hardware qualification. Full recovery tests operate
on the external kit; only the minimal installed identity is required on the appliance.

## Milestone 1 host-only contract checks

Use Python with requirements-contracts.txt and run
`python -m unittest discover -s tests -v`. The 15 tests cover schema meta-validation,
strict/duplicate JSON rejection, pins/package identity, checksums/locators, minimal
identity/golden fixture, private/output fields, read-only workspace refusal and
published tag regression checks. Companion-tag tests skip explicitly if its checkout
is absent. Current local run had no skips. No builder, image or hardware pass follows
from these tests. [Checkpoint](build/milestone1-checkpoint.md) records the scope.

## First private POC validation (current, 2026-09-15)

[POC result](build/private-poc1.md) supersedes earlier no-image checkpoint statements.
26 tests passed on macOS and native Debian; all 50 read-only image checks passed,
plus ext4/FAT integrity, enabled CBM systemd unit validation and exact XZ/raw hash
agreement. Historical 1,677-entry manifest and immutable tags remain unchanged.
No physical Pi behavior, first-boot interruption safety, performance budget or
independent reproducibility pass is implied. Owner review is the current stop.


## POC1 physical Pi 3B follow-up (latest, 2026-09-15)

The owner reports the exact frozen POC1 booted and reached a correctly rendered,
keyboard-operable tty1 Menu. RUN/x64sc produced a black screen with no console
recovery. [Formal record](qualification/poc1-pi3b-2026-09-15.json) separates these
PASS/FAIL results from UNTESTED later VICE behavior. The previous offline checks
remain valid within their original limited scope.

[Read-only analysis](qualification/poc1-pi3b-analysis.md) ranks hypotheses without
claiming a proven cause. [Setup review](qualification/setup-ux-review.md) separately
records the raspi-config privilege UX gap and required offline-capable 1.1 setup.
Masked services are not failures. [Media plan](qualification/poc2-media-plan.md)
requires licensing, actual checksums and independent known-good validation before
embedding any test payload. No media exists or was obtained in this analysis.

Owner authorization is required before implementing fixes/diagnostics/media or
building POC2. Freeze a new candidate, verify diagnostic access before launch, and
stop on failure without repairing the running qualification artifact.


## POC2 offline completion (latest, 2026-09-15)

[POC2 checkpoint](build/private-poc2.md): 34 host/native tests, shared Menu launcher
checks, 79 offline image checks, read-only filesystems/systemd units and 112 ELF
objects passed. Exact original-media hashes and scoped reference results are in
[the result](build/private-poc2.json). These are not Pi graphics/audio/input passes.
At that build checkpoint, physical testing remained UNTESTED; the linked
[Pi 3B record](qualification/poc2-pi3b.json) now contains the subsequent owner report.
Use [the exact-hash smoke procedure](qualification/poc2-pi3b-smoke-test.md), verify
diagnostic access first, and stop on failure without repairing the candidate.
POC1's evidence remains unchanged. STOP for owner review; no automatic next build.

## POC2 physical follow-up (current, 2026-09-15)

[Formal owner-reported matrix](qualification/poc2-pi3b.json): core boot/Menu/VT,
x64sc rendering/observed stability/keyboard/F10/Quit/return, original PRG/SID-tone/
video-input/D64 tests and normal reboot pass. Aspect-ratio preservation fails;
joystick, broader profiles/models/persistence, first-boot interruption, deferred
services and independent reproducibility remain untested. No single POC1 cause is
confirmed. [Geometry investigation](qualification/poc2-pi3b-aspect-analysis.md)
recommends a narrow POC3 before additional Pi models; owner approval is pending.

For geometry, distinguish emulator canvas screenshots from the final HDMI display.
Record true-aspect resources, PAL/NTSC/model/border, renderer, physical connector
mode and observed margins/cropping. Use external photos with locators/hashes when
available; do not claim physical proof from source defaults or a screenshot alone.
Preserve the frozen candidate; proposed defaults require a new input lock/image.


## Configuration source validation (2026-09-16)

Use the product's pinned developer requirements in an external/disposable environment.
Run from each repository respectively (Python 3.11+; jsonschema for developer tests):

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

Product tests exercise exact allowlists, invalid input, readiness, secret exclusion,
private/atomic writes and fake Linux adapters. Menu tests invoke actual controllers with
fake dialog/commands, checking cancellation, errors, typed requests, return paths and
existing machine/launcher behavior. No host system changes occur. Run the Menu suite
with the sibling product checkout present. The standalone launcher checker is also
included in discovery. Do not count it as a new hardware test.

Reproduce source timings from product:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 tests/benchmark_configuration.py
PYTHONDONTWRITEBYTECODE=1 python3 tests/benchmark_information_machines.py
```

The optional macOS process-memory measurement requires permitted resource accounting.
The [results](runtime/configuration-validation.json) distinguish static/fixture success
from unperformed native Linux installation, real dialog, service/account/network and
physical Pi tests. Before runtime activation, test the exact dependency paths/catalogs,
root trust chain and sudoers policy in a disposable Linux target; first-boot interruptions,
owner authentication, hostname resolution, network secrets/failures and each service's
readiness/listeners require separate verification. POC3 qualification cannot cover new
source settings merely because its Menu, VICE and geometry passed on Pi 3B.

## Optional applications/reference content source addendum

120 product tests and 44 Menu tests plus the launcher checker passed. New tests
cover source/member hashes, deterministic D64 chains/allocation, frozen-lock version
admission, source-to-payload verification, user-state preservation, unsafe path/media
rejection, registry profile selection and actual content-browser success/failure.
See [contract/results](runtime/optional-applications-contract.md). The separate
[physical procedure](qualification/optional-applications-procedure.md) is pending a
new approved candidate; no reference SID, application or demo runtime pass is implied.
Metadata catalog validation does not establish rights or media compatibility.

## Post-attempt-2 cover source checks

60 Menu tests plus launcher checker cover registry selection, exact asset hashes,
default/explicit/content launches, missing/failed renderer fallback and SDL lifetime.
Native Debian arm64 headless SDL decoded two real covers and released video between
runs; GNU timeout stopped a simulated hung renderer. No physical KMS/VT evidence.
See [cover design/results](runtime/covers.md) and the
[future candidate test addendum](qualification/covers-next-candidate.md). These tests
do not change or qualify the already-frozen POC4 attempt #2 image.
