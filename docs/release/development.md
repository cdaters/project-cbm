# Return to Project CBM development

[Canonical content paths and hierarchy](content.md) cover the library, machine routing,
USB import, optional applications and safe preservation of older content.


Read Product and Menu AGENTS/CURRENT-STATE from disk, inspect branches/HEAD/dirty work,
then follow the exact next action. Preserve unfamiliar changes and immutable evidence.
Product owns runtime/integration/build/qualification; Menu owns its independent UI
package. Start with [architecture](../architecture.md), [configuration](../runtime/configuration-contract.md),
[Covers](../runtime/covers.md), [security](../security.md), [tests](../testing.md),
[build workflow](build-your-own.md) and [recovery](../recovery.md).

The release guides are the current user path. Dated build/qualification files preserve
history; they are not competing instructions. CURRENT-STATE points to the current
candidate, its exact lock/artifacts and the physical procedure. Keep changing checkpoint
facts there rather than in governance. Test reports distinguish host fixtures, native
Linux, actual-image validation and owner physical observations. Never infer a physical
PASS from installed packages or simulated hardware.

Use the Python dependencies in `requirements-contracts.txt`. From Product run
`python3 -m unittest discover -s tests`; from Menu run the same command with Product
checked out beside it. Run per-file Bash syntax, JSON/schema, local link/path, whitespace,
size and secret-pattern checks. Native tests under `tests/native` require their guarded
disposable Linux namespace; never invoke them on a live appliance or builder root.
The native candidate harness is retained with the qualification evidence. Historical
runtime/install/release-prep scripts are not static validators.

Before freezing, commit logical local changes after checking author/committer privacy,
version changed packages and pin Menu's annotated tag plus peeled full commit and hash.
Use a new attempt directory. Build source and output are recoverable without the VM;
GitHub and caches are not the sole authority. Failed attempts remain evidence. A passing
candidate ends at the owner's exact-hash physical procedure, not automatic publication.

Current accepted limitation: keyboard VT switching while VICE's SDL/KMS console backend
is active. F10 → Quit then switch works; retain it until a supported upstream solution
can preserve input/display ownership. [Boot presentation and timing](boot.md) describe
the current quiet console settings, guarded initialization fast path, unchanged baseline
and required physical checks. Quieter output is not evidence of a faster boot.

## Follow a change through the system

For a UI wording change, begin in Menu `scripts/pcbm-menu`, `scripts/pcbm-config` or
`scripts/pcbm-first-run`; presentation helpers are in `lib`. For information/status,
start in Product `runtime/project_cbm/info.py` and its JSON schemas. Menu consumes
those records, so a new status field belongs in the Product contract and focused
tests before it is formatted. Configuration requests pass through the Runtime's
validated client/backend rather than arbitrary sudo shell commands.

Machine selection starts in `runtime/data/profiles.json` and validated preferences.
Launching enters Menu's shared `pcbm-run-vice`, with Product integration under
`build/pigen/stage-cbm/files`. Cover, emulator and terminal restoration are one owned
transition. A package can build correctly and still mishandle real tty/DRM input;
repeat physical launch/quit testing after any change to this path.

Account creation and image-wide defaults belong to `tools/install_poc_stage.py`.
The Unix account is `pcbm`; `owner` remains the conceptual role and setup step/API name.
Do not rename role fields while editing usernames. First-boot secrets travel through
protected input, never command arguments or logs. Native tests exercise actual su,
sudo, SSH and Samba behavior in a disposable target, in addition to fixture tests.

Package recipes under `build/packages` and Menu's `debian` determine install layout and
versions. The frozen integration archive determines what pi-gen actually executes.
Editing your working tree after freezing does not change that candidate. Make another
version/lock for changed bytes; do not patch a completed image to make a check pass.

## Performance changes

`tools/benchmark_vice.py` creates an original reproducible CPU/screen/SID workload and
measures a fixed emulated-cycle interval with real WAV samples. Use a new output
directory for each run. Dummy audio that synthesizes no samples, warp that skips sound,
and VM CPU percentages do not establish Pi performance. `tools/vice_performance.py`
parses bounded installed numeric telemetry for a chosen uninterrupted physical interval.
The exact procedure must identify image, hardware, workload, settings, clocks/throttling,
audio/visual result and lifecycle. Owner reference media stays outside source packages.
See [the performance decision](../runtime/c64-performance-2026-09-18.md) for the retained
comparison and limitations; current defaults are explained in [VICE](vice.md).

## Returning after an absence

Use CURRENT-STATE to locate the newest build report, lock, artifacts, recovery manifest
and pending physical procedure. Verify the actual Git refs and dirty work; the state
file can lag a interrupted operation. Read the relevant canonical contract, run focused
checks, and preserve unfamiliar files before cleanup. A recovered VM is useful but not
the source of truth: the recipe, retained inputs and verified recovery bundles must
be enough to reconstruct the engineering state on replacement infrastructure.
