# Attempt24 owner review: download success and direct-boot display failure

Read-only Pi inspection on 2026-09-27 UTC. PRIVATE NON-RELEASE
Project CBM 1.2.0-dev.5, Raspberry Pi 4 Model B Rev 1.4.
[Candidate and procedure](attempt24-pi4-ux-online.md).

Installed identity matches lock
`ee0308da672c783cf3142e7a581b80344e42cc3605f227b7d8f18cb50dd62819`,
frozen Product `83c137008adf1d9135f19b1243437b30492ddb7b` and the recorded
Runtime/Menu/KMS package versions. Candidate raw SHA-256 is
`754b34e4ab1abd0af65d97956546f295036a4a418b15c20d7f3dd0f14fd1ba7c`;
XZ SHA-256 is `efb7f642b91160b2143abd7f958509f2ffc2f8d618667ba697a4c1f01955f051`.
These are the retained factory artifact hashes, not a rehash of the running,
expanded, user-configured card.

## Bounded physical results

| Case | Status | Evidence and limit |
| --- | --- | --- |
| Assembly64 content download | PASS, owner reported | Owner reports working Assembly64 and successful content downloads. This does not qualify every search filter, duplicate handling, cancellation, offline launch or download format. |
| Mixed PRG/BIN guided preview | PASS for exclusion/presentation | First supplied capture offers one PRG, with three unsupported entries and four ignored metadata entries/folders. Friendly name appears without an opaque tag. No import/save operation is established by this screenshot. |
| Unsupported-only guided preview | PASS for empty-list explanation | Second capture shows zero supported files, four unsupported entries and the FILES > USB Drive alternative. No Select All is offered. |
| Boot directly to current default machine | FAIL | Saved preference is emulator, default x64sc. Owner reports initial artwork followed by blank HDMI; retained capture is black with a small console cursor. VICE runs using SDL offscreen. |
| Return after external VICE TERM | FAIL for physical keyboard responsiveness, owner reported | Visible Main Menu returned, but physical keyboard interaction did not. Foreground ownership appeared correct. See the subsequent chronology below. |
| Owner recovery by forcing Unicode keyboard mode | PASS for recovery only, owner reported | Physical keyboard became responsive immediately. An intervening diagnostic command had changed keyboard mode; the original pre-command mode is unknown. This does not qualify automatic cleanup. |
| Normal F10/return from direct boot, new-image moving gameplay capture, remaining procedure cases | UNTESTED by this report | External TERM and manual recovery do not establish a normal F10 lifecycle PASS. |

## Subsequent owner-reported keyboard failure and recovery

This chronology was supplied after the read-only collection described below. It is
owner-reported physical evidence, not a new agent inspection or a change to the
retained pre-termination diagnostic snapshots. It remains bound to the same
attempt24 image identity and hardware.

1. Direct boot showed blank HDMI while x64sc continued running invisibly.
2. From SSH, the owner ran `pkill -TERM -x x64sc`, terminating only VICE. The
   visible Project CBM Main Menu returned, but the physical keyboard remained
   non-responsive. Thus visible redraw alone did not restore a usable console.
3. Read-only process inspection showed tty1 active, the boot/session/Menu/dialog
   chain present, dialog in tty1's foreground process group, and VICE/SDL processes
   gone. Foreground ownership appeared correct; this does not establish keyboard
   mode or complete console-state correctness.
4. During subsequent diagnosis, ChatGPT mistakenly instructed the owner to run
   `sudo kbd_mode -s < /dev/tty1`. This **sets raw/scancode mode**; it is not a
   read-only query. The keyboard was already unresponsive before this command,
   but its exact kernel keyboard mode had not been measured at that point.
5. A later query showed raw/scancode mode. The owner then ran
   `sudo kbd_mode -u -f < /dev/tty1`. Immediately after forcing Unicode keyboard
   mode, the physical keyboard worked and the visible Main Menu was navigable.

These commands are retained as historical actions, not instructions to repeat on
the qualification Pi. The diagnostic `-s` command altered the evidence: the later
raw/scancode observation **cannot prove direct boot originally left tty1 in that
mode**. The pre-command keyboard failure is established; its exact keyboard-mode
cause remains unknown. Unicode recovery establishes restored usability after the
intervening mode change, not that this mode change was the original defect.

The display-release/launch-order defect remains independently supported by the
earlier logs. Automatic post-TERM physical keyboard restoration failed according
to the owner; normal direct-boot F10/exit remains unqualified. The Pi is now
recovered and responsive. No source/package patch was applied by this update.

## Direct-boot root cause

The normal Menu/dialog path calls `pcbm_boot_handoff` before displaying its UI.
The successful first-run path in `pcbm-console-session` instead proceeds directly
to `pcbm-run-vice` when a boot profile is selected. There is no handoff before that
launch, and the shared launcher does not perform one. The boot supervisor therefore
still owns the primary artwork while the machine Cover and VICE initialize.

Retained monotonic times establish the overlap:

- Primary boot artwork starts at 11.982 seconds, selects KMSDRM and presents HDMI
  at 1920x1080. Its report has no readiness event.
- Startup choice completes at 13.25 seconds. Direct launch starts at 13.567.
- Machine Cover runs at 13.692–16.113 seconds and selects **offscreen**, 1024x768.
- VICE is spawned after audio completes at 16.351 seconds. Its presentation log
  explicitly reports **driver=offscreen**, 1024x768 at 0 Hz.
- Boot artwork reaches its own release deadline and the primary supervisor finishes
  terminal restoration at 40.890 seconds; `primary_done` is 40.92. Clearing the
  restored console leaves the visible black screen while VICE remains offscreen.

Earlier ordinary launches on the same installation record KMSDRM, 1920x1080 at
60 Hz. The failed launch has TERM=linux, the expected unprivileged session and
foreground group on tty1, and stdin attached to `/dev/tty`. Stdout/stderr are the
intentional diagnostic log pipe. This is not the attempt18 USB MC inner-PTY defect.
All four installed Product boot/engineering files match repository source hashes.

The confirmed lifecycle defect is the missing release/acknowledgment before direct
launch. The logs directly establish the resulting offscreen selection; they do not
include a low-level SDL DRM-master error explaining each internal driver probe.
No changes to DRM permissions, VT ownership or VICE configuration are indicated.

## Small correction and regression requirements

In `build/pigen/stage-cbm/files/pcbm-console-session`, perform the existing bounded
`pcbm_boot_handoff` before the selected direct `pcbm-run-vice` invocation. Require
successful acknowledgment before starting the machine Cover or VICE. Preserve the
single-launch-per-login contract and return to Menu after exit. Do not substitute
a delay, forced modeset, root launch or terminal repair. A separate hardening check
should prevent an offscreen backend from being treated as visible appliance output;
forcing a driver alone would not correct this ordering defect.

Existing `tests/test_boot_handoff.py` tests the handshake primitive. The native
`tests/native/boot_handoff.py` replaces the console worker with a fixture that
explicitly calls the handshake, using SDL dummy. Neither exercises the actual
completed-setup/direct-emulator branch, so both can pass with this omission.

Required regression: run the actual console-session branch with readiness pipes
and a controlling PTY; instrument the renderer and launch boundary to assert primary
release, reap and terminal verification precede machine Cover/VICE. Cover immediate
and delayed readiness, missing/failed renderer, timeout, EOF/repeated handoff,
ordinary Menu startup and completed first-run startup. Verify one direct launch,
then normal Menu return on exit/failure. Native tests cannot establish HDMI output;
a fresh immutable candidate needs Pi 4 direct-boot KMS/visible BASIC or gameplay,
F10/return and ordinary Menu-start regression qualification.

The additional keyboard evidence extends this requirement to the complete sequence:
boot artwork release/reap -> machine Cover -> visible VICE -> normal F10/Quit/exit
-> tty1 restoration -> correct kernel keyboard and console modes -> physically
responsive Main Menu. Assert foreground ownership, termios, kernel keyboard mode,
console display mode and VT mode against the valid captured console baseline;
foreground ownership or a successful Menu redraw alone is insufficient. Measure
modes with read-only queries before any recovery action, and keep state-changing
recovery separate from diagnostic evidence.

Exercise external TERM of VICE, abnormal child exit, failed/offscreen initialization,
Cover/renderer failure and bounded timeout paths as well as normal exit. Verify
cleanup ordering, reaping, no late boot-artwork restoration racing the next screen,
and usable display/keyboard after each failure. Mocked mode assertions and native
PTY tests cannot prove physical kernel keyboard/VT behavior: qualify the complete
lifecycle on Pi 4 in a fresh candidate. Do not repair attempt24 in place or use
blanket keyboard-mode forcing as a substitute for correcting lifecycle ownership.

This investigation changes documentation only. No source correction, package,
new candidate or repaired-boot PASS is claimed. During the original agent read-only
inspection, the live Pi was not patched, reconfigured, rebooted, signaled or
remounted; no sudo was needed. The subsequent owner termination and keyboard-mode
changes are recorded separately above and must not be described as read-only.

## BIN and ROM distinction

BIN can represent legitimate machine/drive ROM data. That does not make it generic
runnable media, and the supplied captures show it being excluded by this importer.
`runtime/project_cbm/ingestion.py:EXTENSIONS` deliberately excludes `.bin`;
`library.py:import_destination` accepts games/demos/programs/music, not ROM management.
The presence of `content/roms` directories does not implement a ROM import workflow.
`library.py:content_profile` rejects ROM resources for generic autostart.

Keep the existing exclusion. A future ROM workflow requires explicit ROM role,
target machine/device, validation and VICE configuration/restore semantics. This
report does not add BIN or claim VICE cannot use correctly configured ROM files.

## Retained evidence

Private external directory, relative to configured ProjectCBM-Work:
`qualification/attempt24-owner-review-2026-09-27/`. It contains the three supplied
PNGs, retained boot traces, existing launch/primary diagnostics and an allowlisted
read-only inspection. Source and copied screenshot hashes agree. Diagnostics were
copied while the failed VICE process remained running; these are bounded snapshots,
not an exit/cleanup record. Private filenames remain outside Git.

| Capture | Bytes | SHA-256 |
| --- | ---: | --- |
| pcbm-20260926T235133Z.png | 40219 | `634b8722f37edbf5bfc14016cdbca85278d76d86c4ed1d07957bbb74a3333669` |
| pcbm-20260926T235302Z.png | 39394 | `daf727f8cbdb2fbefe8cb15cd39fecaad72148f4df621268dea7412aac7b4618` |
| pcbm-20260927T000246Z.png | 27282 | `de1ea455412517c5aac1f3cfbd719d35d7c1ea80e7caa18fd5e73e6cd2c6986d` |

Additive recovery belongs under `archive/attempt24-owner-review-2026-09-27`;
the sealed factory checkpoint and all earlier attempts stay untouched. TheBench
remains same-volume custody, not independent encrypted backup.

The later owner chronology is retained separately under
`qualification/attempt24-keyboard-addendum-2026-09-27`, with additive recovery under
`archive/attempt24-keyboard-addendum-2026-09-27`. It does not modify the sealed
original collection or its manifest. No new raw process output or pre-command
keyboard-mode measurement accompanied this owner report.
