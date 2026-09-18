# Return to Project CBM development

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
can preserve input/display ownership. Quiet boot, splash presentation and measured faster
boot are the next separate polish milestone. Do not combine them with service refinement.
