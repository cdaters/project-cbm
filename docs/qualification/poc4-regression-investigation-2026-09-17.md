# POC4 attempt #3 regression investigation — owner review

Recorded 2026-09-17. **STOP: collect existing physical SD-card evidence. No source
correction selected; no new candidate prepared or qualified.**

## A. Executive findings

The exact frozen POC3 and POC4 attempt #3 inputs, lifecycle sources, dependency
sources, build/offline records and available native engineering results were compared.
The owner-reported POC4 results are now an [additive qualification record](poc4-attempt3-pi3b-owner-report-2026-09-17.json).
The dead post-VICE keyboard/VT and missing Cover causes are **not confirmed**; their
relationship is **UNKNOWN**. A Cover timeout followed by capture/restoration of an
already-altered keyboard mode is a strong candidate, not a demonstrated event.

No physical-run logs were found in the inspected retained evidence. The candidate
discards Cover output/status and does not persist keyboard-mode/foreground-group
snapshots. Host SDL dummy and mock tests cannot supply those observations. The owner's
stop condition therefore applies before a responsible lifecycle correction can be
selected. No lifecycle or first-boot runtime source was changed. First-boot defects
have been source-audited, but lower-priority implementation is deferred at this stop.

**Next owner action: collect existing attempt #3 SD-card evidence using the
[read-only collection procedure](poc4-regression-collect-evidence.md).** No reflash,
new launch, automatic hardware test, package build, input freeze or image build.

## B. Physical results and exact identity

| Identity | Binding |
| --- | --- |
| Product / hardware | 1.1.0-poc.4 / private-engineering-poc4, attempt #3; owner-tested Pi 3B |
| Product frozen integration | `b362c70215cef0e2c6c6a845635c47fd39b3ebbf` |
| Menu | `v1.1.0_poc4.1`, peeled `407ced58b711209631cdfb4db6dcd741a555f408` |
| Lock SHA-256 | `435c6e0d7a5a45eaff3f45af6d384fca5b602139fa9fb640950e2f5e7b4f39a9` |
| Raw SHA-256 | `37d2699c7a639e050e531a4d5a132d4b197e5a60270a969814c573f436036cd8` |
| XZ SHA-256 | `4a6bce98e089e3c39246393b7476c687a7818ea5a6b67fa811fb6bee8da5a83e` |

Full locators/sizes are in the [unchanged build record](../build/private-poc4-attempt3.json).
Physical test date and detailed equipment were not supplied; recording date is not
substituted for test date. The master image and used test SD card are distinct evidence.

- **PASS:** first boot fundamentally completed; appliance became usable; Menu appeared;
  RUN launched selected/default VICE; VICE ran; F10 opened its menu; Quit exited;
  Menu visually returned; mc launched; SID-Wizard and StrikeTerm presence; enrollment
  succeeded with a simple alphanumeric test passphrase (no credential retained).
- **FAIL:** Cover not visibly presented; returned Menu keyboard unresponsive;
  Ctrl+Alt+F2 and Ctrl+C unresponsive after return.
- **OBSERVED UX DEFECT:** apparent hangs without feedback; awkward region/locale/country
  flow; prepopulated UTF-related field/Enter surprise; technical code input; unreliable
  Back; invisible password typing; unhelpful error on an unsuccessful password attempt.
- **UNTESTED:** actual application use/save/relaunch; USB; Wi-Fi reconnect/reboot/external
  traffic and explicit no-Ethernet/Stay Offline scenarios; Samba, SSH, TCPser, mDNS;
  Advanced Mixer; broader preferences/direct boot/services persistence; root capacity,
  interruption and first-boot replay; POC4 geometry/audio/joystick/original media and
  repeated controlled cycles. F10 success is not a general keyboard test. mc launch
  is not a copy/exit/return test. See the JSON for the complete per-item matrix.
- **INTENTIONALLY DISABLED / NOT APPLICABLE:** automatic optional-service activation
  and unsupported generic PSID/RSID playback. Deliberate opt-in service operation is
  still UNTESTED, not failed merely because initially disabled.

The [POC3 attestation](poc3-pi3b-owner-report-2026-09-16.json) proves the bounded
Menu → VICE → responsive Menu baseline, both VT directions, geometry, media, SID voices,
joystick and reboot. The current owner further identifies VT switching after return.
**POC3 contained no new SDL Cover**, so its pass does not qualify that presentation path.
Original build/physical records and attempt #3's hash-bound procedure remain unchanged.

## C. POC3 → POC4 differential

Comparison uses Product `0a0e271d86c68a969d8b18189c561ed51a8b0e09` →
`b362c70215cef0e2c6c6a845635c47fd39b3ebbf`, Menu
`897cee7c792b11bfed80168a576f263340f5f57d` →
`407ced58b711209631cdfb4db6dcd741a555f408`, and both full verified frozen kits.
No base binary-package name/version/hash changed. VICE and TCPser package bytes
are identical. Menu changed, and the Product runtime package was added.

Evidence abbreviations: **S** exact Git source diff; **K** rehashed frozen-kit comparison;
**O** retained offline inspection; **N** retained native/headless tests; **P** owner report;
**L** missing physical launch/state evidence. Confidence describes the stated finding,
not confidence that an unobserved event occurred.

| Component / behavior | POC3 | POC4 attempt #3 / relevant change | Missing Cover? | Dead input/VT? | Evidence / confidence / classification | Next test |
| --- | --- | --- | --- | --- | --- | --- |
| Base graphics/input/login stack | Pinned SDL2 2.32.4, Mesa, libdrm, kernel, PAM/systemd, kbd, dialog | Same base package catalog and hashes | No dependency-version change | No dependency-version change | K/O; high; UNRELATED as a package-upgrade explanation, runtime interactions still possible | Inspect actual live backend/session evidence |
| VICE executable, geometry/audio/F10 | VICE 3.10-1+pcbm3, per-chip true aspect/desktop fullscreen, ALSA/F10 | Same package and defaults/diagnostic source | Not a Cover stage | Same VICE can inherit different state | S/K; high; UNRELATED as a VICE binary regression; POSSIBLE CONTRIBUTOR through entry state | Compare captured VICE profile/resources/exit |
| Getty/login/PAM tty1/tty2 | agetty autologin pi, normal login/PAM | Same getty drop-ins and profile entry; both enabled | Guard still expects tty1 | Live seat/session not measured | S/O; high unchanged recipe, UNKNOWN runtime | Existing before/sample sessions and service status |
| Console session | Login → Menu loop | First-run loop, preferences initialization, at most one direct boot added | Could change inherited environment/state | Possible first-boot/session contribution | S/P/L; POSSIBLE CONTRIBUTOR, low causal confidence | Setup markers, chosen boot mode, tty/process records |
| Accounts/groups | pi UID 1000, narrow power policy | Owner UID 1001, pcbm-operators added; pi removed from sudo | No changed video/render/input membership in recipe | No direct input/VT rule change found | S/O; high; UNRELATED as direct graphics grant removal | Check reported UID/session, do not broaden privileges |
| Locale/keyboard | No interactive region pass | localedef/update-locale, setupcon save-only, timedatectl | Inherited locale can differ | Selected keyboard applies next boot; no explicit live keyboard takeover here | S; POSSIBLE CONTRIBUTOR to entered characters, low for total dead VT | Setup state/current saved layout; no credential request |
| Profile/default/content resolution | Hard-coded launch whitelist; legacy default | Validated Product registry/preferences; app-specific content profile | Mapping error possible in principle, fixture/asset mapping passes | No ioctl/session ownership in resolver | S/K/O/N; high mapping evidence; UNKNOWN actual selection | Physical record profile and validated preference value |
| Cover artwork/install | SDL Cover absent; historical hook had no installed usable new art | Seven exact assets; explicit package list | Assets present; package modes readable | Assets themselves do not own input | K/O/package listing; high; UNRELATED as missing packaged artwork | Verify card identity; logs cannot reconstruct visibility |
| Cover invocation | No effective SDL stage | Shared launcher calls timeout → wrapper → Python before engineering wrapper | Yes: guard/error/timeout invisible | Yes if state remains altered | S/P/L; STRONG CANDIDATE jointly with cleanup boundary; physical event unknown | Existing VICE log first; scoped live plan if insufficient |
| Foreground process group / signals | No Cover timeout group | GNU timeout without `--foreground` creates a new group; child TTIN/TTOU dispositions reset | Possible job-control interaction | Possible state/cleanup interaction | Exact coreutils 9.7 source; high group semantics, low causal confidence; POSSIBLE CONTRIBUTOR | Read actual pgid/tpgid and signal/wait state; PTY alone not Linux VT proof |
| SDL display/input initialization | VICE owns SDL stage | Additional SDL video init/window/renderer, evdev keyboard/VT ownership | Init/render failure or early timeout possible | Interrupted ownership release possible | Exact SDL source/S/N; STRONG CANDIDATE, not confirmed | Cover stage/status and owned-mode snapshots |
| Cover duration/termination | Absent | 0.75 s render loop; whole wrapper limited to 2 s + 0.5 s grace | Startup/cleanup time counts against limit | SIGKILL cannot execute finally; reaping does not prove console restoration | S/N/P/L; high mechanics, UNKNOWN physical timeout | Measured phase times and termination reason |
| Engineering terminal snapshot/restore | Save state immediately before VICE; restore afterward | Same code, but save now occurs **after Cover** | Does not observe Cover | Can preserve prior corruption; restores saved keyboard, KD_TEXT, termios | S; high ordering; STRONG CANDIDATE contribution if Cover left bad state | Need saved mode before/after Cover and cleanup result |
| VICE subprocess / stdin / signals | `/dev/tty` stdin, captured stdout, inherited group/session; signal forwarding | Same code | No direct effect | Same code with potentially changed entry state | S; high; UNKNOWN current actual state | PIDs/phase/exit; missing fd/group/mode fields require later live plan |
| Menu return / resets | Same Menu loop; zero-argument cover, reset, clear after RUN; stty cleanup | Return hook retained; no-argument new Cover exits before SDL | Not a second renderer or prelaunch clearing race | Existing reset may interact with damaged state; not new root-cause evidence | S; high; POSSIBLE CONTRIBUTOR, low | Establish which process is running/reading; do not add more resets |
| Network/service activation | Services masked | NM available/offline initially; optional opt-in services; narrow backend | No direct display code | Additional system activity/state, not established cause | S/O; low causal confidence; POSSIBLE CONTRIBUTOR | Existing approved environment/service records |
| Build environment correction | Older builder/chroot environment | Sanitized target environment | No runtime Cover implementation | No new tty ownership code | S/K/O; UNRELATED on available evidence | No build retry needed for diagnosis |

No row is classified CONFIRMED CAUSE for either physical lifecycle failure.

## D. Complete Cover path

RUN uses `pcbm_load_default_machine` → `pcbm_launch_machine` → `pcbm-boot` → shared
`pcbm-run-vice`. Registry resolve yields executable/approved flags; invalid selection
stops before Cover. `pcbm-cover --profile` resolves the same profile's cover identity:
C64-family → c64, x128/80col → c128, xcbm2 → cbm2, xcbm5x0 → cbm5,
xvic → vic20, xplus4 → plus4, xpet → pet. CONTENT uses its actual resolved launch
profile, including the admitted C64 app override, not merely the default machine.
The actual owner's launched profile remains unrecorded outside the requested logs.

Exact command, after environment/home setup and content validation:

```sh
/usr/bin/timeout --signal=TERM --kill-after=0.5s 2s /usr/bin/pcbm-cover --profile "$profile" >/dev/null 2>&1 || true
```

The wrapper requires non-root, `tty` exactly `/dev/tty1`, safe identity and existing
non-symlink JPEG/PNG. It execs `/usr/bin/python3
/usr/libexec/project-cbm-menu/pcbm_cover_view.py ASSET`. All seven packaged files
are root-owned 0644; launcher/wrapper/renderer package entries are root-owned 0755.
Retained offline checks establish exact installed payloads and dependencies. This
session inspected package modes; it did not remount the image to re-measure file modes.

The launcher exports fixed pi XDG/HOME and ALSA settings. Cover otherwise inherits
the login environment; it does not pin an SDL video driver. VICE's subsequent
engineering wrapper reconstructs a smaller allowlisted environment. Thus the two
SDL processes do **not** have identical environment policy. Actual driver selection,
DRM master acquisition, window output and Pi timing are unknown.

Renderer calls SDL video init, current display mode, fullscreen-desktop window,
accelerated renderer with software fallback, IMG texture decode and aspect-fit render.
The loop is 0.75 seconds from its post-initialization deadline; any key/quit can end it.
A held/queued key could shorten visibility; no event trace establishes this occurred.
Finally destroys texture, renderer and window, then IMG_Quit/SDL_Quit. Python handles
TERM/INT; synchronous native calls and forced SIGKILL limit what finally can guarantee.
VICE starts only after the timeout command returns; there is no deliberate background
Cover. No source evidence of VICE launching concurrently with the presentation loop.

Ordinary failure/status and stderr are discarded, so missing asset/guard exit, SDL error,
successful skipped presentation and timeout are indistinguishable in retained launcher
output. The native tests use SDL dummy: 0.768/0.765 s in attempt-3 staging; a synthetic
TERM-ignoring child was killed in 2.505 s. They prove neither visible KMS presentation
nor keyboard cleanup after a real renderer timeout. Failure point remains UNKNOWN.

## E. Post-VICE keyboard/VT findings

`engineering.py` is byte-identical between frozen integration revisions. It opens
`/dev/tty` read/write, saves termios and KDGKBMODE, uses that fd as VICE stdin, captures
stdout/stderr, and inherits the controlling session/process group. It forwards
TERM/HUP/INT to the child, waits, records exit, then attempts saved KDSKBMODE, KD_TEXT,
saved termios and cursor/clear output. Restore errors are swallowed. There is no
post-restore verification. Existing shell `stty sane` changes termios, not proof of
keyboard mode or VT ownership. None of these cleanup actions was added here.

The retained SDL 2.32.4 source explicitly opens `/dev/tty`, saves keyboard mode, uses
VT_PROCESS, and can mute console translation with K_OFF. Normal shutdown restores
keyboard mode and VT_AUTO. It also installs emergency signal/atexit cleanup. Therefore
"the process exited" alone does not prove all state restored, and neither does a
claimed timeout alone prove restoration failed. SIGKILL does not execute that cleanup.

If Cover leaves K_OFF and engineering saves it, restoring that saved value after VICE
would preserve a dead console. This is a conditional mechanism supported by source,
**not a captured K_OFF value or confirmed root cause**. Other live conditions remain
possible: foreground-group mismatch, different controlling terminal, blocked Menu or
dialog input, altered termios, signal disposition, evdev/DRM ownership or session state.

| Required observation | Available finding |
| --- | --- |
| tty1 process owner, controlling terminal, pgid/tpgid | Intended path known; actual failed-state values absent |
| termios, echo/canonical/raw flags, keyboard/KD/VT mode | Read/restoration code known; saved and returned values not persisted |
| SDL input/device/DRM release | Normal source cleanup known; physical release unobserved |
| VICE exit and signal | Owner reports Quit; exact process status needs `record.json` |
| Menu alive and reading expected stdin / dialog fd | Visual return alone cannot establish this; no failed-state capture |
| VT switching | Owner reports Ctrl+Alt+F2 failed after return; prelaunch POC4 directions not supplied |
| Cursor/terminal output | Menu visible; no proof that interactive ownership returned |

## F. Relationship

**UNKNOWN.** Both failures may share an interrupted Cover/keyboard-state sequence, or
Cover may simply fail open while a separate session/input problem occurs. No A/B
hardware run or physical mode/exit capture distinguishes them. No claim that SDL2 itself
regressed: the library bytes match POC3; the additional use of it is new.

## G. Corrections and implementation stop

No runtime source, privilege, process ownership, timeout, reset, Cover asset or package
was changed. No speculative `--foreground`, increased timeout, forced VT switch or
additional terminal reset was applied. Normal docs/evidence commits are the only
repository changes. The first-boot source defects are actionable separately, but this
task explicitly prioritizes explaining the lifecycle and stops when physical evidence
is required. Completing lower-priority UI changes would not resolve that gate.

Possible future corrections must be selected after evidence: preserve the correct
pre-presentation state in its lifecycle owner; guarantee/review cleanup on each failure
path; retain bounded stage/status evidence; address foreground ownership if demonstrated.
These are test requirements, not an accepted implementation or permission for broad
keyboard/framebuffer manipulation. Keep one unprivileged VICE launch and failure-open
presentation throughout.

## H–K. First boot, region, Wi-Fi and long operations

The [stage-by-stage source audit](poc4-first-boot-ux-findings-2026-09-17.md) gives purpose,
inputs, Back/Cancel, work, bounds, failure/retry and persisted state for every stage.
Confirmed defects: linear abort/restart instead of previous-step Back; technical raw
identifiers; no masked/invisible-entry explanation; invisible synchronous backend work;
generic Boolean failure results; setup finishes before its optional Wi-Fi subflow,
whose resume flag exists only in shell memory. No corrected UI contract is implemented.

The UTF field is the `en_US.UTF-8` language input; keyboard defaults to `us`; country
expects uppercase two-letter input. The default locale passes syntactic validation;
the precise Enter failure is unknown. Future named selections must map to installed
catalogs and retain advanced owner administration without silently assuming US.

Wi-Fi permits printable ASCII punctuation/spaces. Existing source tests and retained
native NetworkManager parsing tests support this transport contract; neither identifies
the failed owner credential or proves AP authentication. Raw nmcli results are discarded,
so the backend cannot label that event authentication failure. Credentials travel via
stdin and intended root-only NetworkManager storage; no secret appears in this report.

No Pi duration is measured. Root boot has a 10-minute service limit; backend commands
typically have 60-second bounds, client 75 seconds, scan reader 8 seconds and activation
30 seconds. The aggregate multi-command lifetime is not equivalent to the client limit.
Future immediate named working states and reliable timeout/retry semantics are required;
none was added at this evidence stop.

## L. Checks and limits

Host baseline: **Product 142 passed / 143 run, one existing host-dependent failure**;
**Menu 65/65 passed**, including the shared-launcher checker. Product's failing
`test_build_environment.BuildEnvironment.test_mktemp_regression` expected nonexistent
TMPDIR to fail; macOS `mktemp` returned success in the unsandboxed test context. It is
not a Cover/VICE/first-boot runtime test failure. Do not rewrite it or claim an all-pass
suite. Initial default-interpreter attempts also lacked jsonschema; the full results
use the pinned, offline-retained dependencies in a new external test environment.

Relevant passing baseline coverage: exact Cover assets/mapping, failed/missing renderer
fallback, normal mocked SDL cleanup, launch arguments/content/F10/status, bounded VICE
logs/repeated mock launches, UI cancel/mismatch/resume, settings validation, punctuation
transport/redaction and malformed backend results. The Cover fixtures replace GNU
timeout; headless native staging ran separately in the prior milestone. Existing tests
do not establish real tty keyboard mode/VT behavior, KMS resource cleanup, repeated
physical handoffs or actual first-boot latency. No new behavioral regression tests were
added because no source correction was selected.

Preservation audit: **5,681 files verified**, including both complete accepted frozen
kits, POC3/POC4 raw/XZ images and attempt-3 checkpoint/retained evidence. No mismatch.
Initial audit reader stopped on POC3's older JSON layout after kit verification; its
partial outputs remain separate. The corrected reader completed in `verified/`.
An additional **14,163 files** verified against earlier frozen/checkpoint records,
including the 5,503-entry POC1/POC2 baseline, POC4 failed attempt #1, attempt #2 and
both attempt-3 blocked checkpoints. Counts overlap other verification scopes and
must not be added as a unique-file total. No prior evidence was rewritten.
Final JSON/link/diff/size/privacy, unchanged AGENTS and refs, and recovery checks are
recorded in the external checkpoint; they are not physical qualification.

## M. Package and next-candidate impact

No Product/Menu implementation commits have yet been selected for a corrected image.
The new qualification/docs commits must inform the eventual release decision but are
not themselves a runtime fix. The [unbound procedure](poc4-next-candidate-regression-draft.md)
is NOT READY TO FLASH.

| Input | Conditional next work |
| --- | --- |
| Menu 1.1.0~poc4.1-1+pcbm1 | New independent source version/tag/peeled commit and package hash after accepted Cover/launcher/UI corrections. Never replace current tag/package. No version assigned here. |
| Product runtime 1.1.0~poc4-1 | New version/package if backend/setup/status/catalog/result changes are implemented. Existing package cannot carry later source edits. |
| Integration source | Refresh exact integration archive/ref for diagnostics/session/first-boot/stage changes and compatibility validation. Geometry/default/media bytes should remain as POC3 unless evidence warrants review. |
| VICE 3.10-1+pcbm3 | Reuse exact `c9d798a591c22faa9ffc3141b7f5177ece36a05e53d9d2c8aae1ce93c22fcfbe` unless evidence establishes required VICE change. |
| TCPser 1.1.6~beta-1+pcbm1 | Reuse exact `8b8f8a4f3ec98dddf5bdb347320dad05e1bbe5230e0ee2727248c247a5af584f`; no defect implicated here. |
| Base packages, Cover artwork, original qualification media, admitted optional payloads | Eligible for unchanged reuse under existing hashes/rights gates; verify compatibility, retained closure and builder guard. Do not silently update or reacquire. |

Before freeze: corrected-source tests; real GNU-timeout/PTY/job-control checks; failure
and cleanup injection; repeated launcher/return; narrow privilege and credential
redaction; first-boot state/Back/retry/progress/catalog tests; native package/API and
installed-path verification; unchanged VICE geometry/audio/F10; pinned environment and
host inventory guards. After construction: full read-only payload/closure/filesystem/
identity checks and the physical draft, newly bound to real hashes. None is automatic.

## N. Dosbian design input

No retained Dosbian analysis was found by name/content in the inspected Product/Menu
docs and external qualification/archive records. The owner's supplied principles inform
the analysis: presentation does not own emulator lifecycle; bounded lifetime and
explicit resource ownership; truthful progress, reversible configuration and human
concepts. No Dosbian code was copied or executed; no MEDIA/TOOLS/POWER/recovery redesign
was implemented. The proposed main-menu evolution and selective reset/backup/support
report ideas remain **backlog input for later review**, not accepted 1.1 requirements.

Preserved owner backlog: potential Main Menu `RUN / MACHINES / CONTENT / MEDIA /
CONTROL / FILES / TOOLS / POWER`; MEDIA could hold USB import, selected-content export,
import history/result and safe eject. TOOLS could hold diagnostics, support-report
export, bounded self-tests and Recovery (selective preference reset, saved-configuration
restore and instructions). POWER could hold Reboot/Shut Down. Selective setting reset
to Project CBM defaults, preference/VICE configuration backup and restore, contextual
help and configured/active/pending/unavailable/failed reporting remain proposals.
None of these organizational or recovery features is implemented or approved here.

## O–Q. Git, continuity and recovery

Predecessor owner scopes remain Product `8a93683`, Menu `be73ff1`; neither was amended
or replaced and neither AGENTS.md was edited. New ordinary evidence/continuity commits
are listed with full IDs in the recovery manifest and final owner handoff. Contributor
noreply identity was checked before commits. Branches remain Product
`feature/1.1-build-foundation` and Menu `feature/1.1-debian-package`; nothing pushed.

Evidence: configured bulk root `qualification/poc4-regression-2026-09-17`.
Recovery: `archive/poc4-regression-investigation-2026-09-17`. Its manifest/checksum and
restore report bind final refs, full bundles, new documentation/qualification, check logs,
source-change inventory and earlier evidence identities. Full offline mirror restoration,
all refs/peeled tags, bundle integrity and fsck must pass before declaring the checkpoint
complete. Master images are referenced by path/hash, never duplicated into it. Independent
backup/custody is unchanged and unresolved; another folder on TheBench is not a backup.

## R–S. Remaining physical work and one next action

The [future regression draft](poc4-next-candidate-regression-draft.md) requires both
prelaunch VT directions; visibly correct bounded Cover; VICE geometry/input/joystick;
F10/Quit; **immediately responsive** Menu and both VT directions after return; two
complete cycles and preferably three; default/explicit/content profile selection;
fresh offline/no-Ethernet setup, navigation/failure/retry/progress measurements; original
media/audio/input; then remaining applications, USB, network/services and persistence.
All new physical checks remain UNTESTED.

**COLLECT ADDITIONAL PHYSICAL EVIDENCE:** preserve and collect the existing used attempt
#3 card's allowlisted diagnostic/setup/identity records using the linked read-only
instructions. No boot is needed for offline retrieval. If the Pi is still in the failed
live state, report that before powering it down. Do not perform a new test, candidate
construction or implementation step automatically. Stop for owner review.
