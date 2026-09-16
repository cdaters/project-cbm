# POC3 Pi 3B: geometry and regression smoke test

**Not performed. Owner review is required before physical testing.** Use only the
exact candidate/hash in the completed [POC3 build record](../build/private-poc3.md).
Do not repair its OS, VICE defaults or display configuration during qualification.

## 1. Identify and flash

Candidate: **1.1.0-poc.3 / private-engineering-poc3**. Exact filenames, sizes and
SHA-256 values are in the linked build record and [planned result](poc3-pi3b.json).
Raw SHA-256: `9a8b1e0465c93981dfa6b09772e9e3fbf5c487a915bba0046b5de034f9331f33`.
XZ SHA-256: `e7d9657bfbb1124b38c2f1f3479698e24a34be7234db80d766f189da946ace3c`.
Verify SHA-256 before flashing. Do not customize the image in Imager or enroll
networking. Use the same Pi 3B/display setup as POC2 where possible. No joystick
is required. Record monitor make/model, nominal resolution/aspect, cable, audio
path and current monitor scaling setting **without changing them to fix a failure**.

## 2. Boot, Menu and diagnostic access

1. Confirm boot, automatic tty1 Main Menu, rendering and keyboard.
2. Ctrl+Alt+F2: confirm the non-root diagnostic shell and keyboard work. Run
   `pcbm-diagnostics`; record its report location. Ctrl+Alt+F1 returns to Menu.
3. If either basic path fails, stop and report it; do not repair sudo or services.

## 3. Primary geometry gate: default x64sc

1. Choose RUN. Confirm C64 startup/READY, keyboard and a stable display.
2. Allow about 35 seconds so the existing periodic snapshots capture active state.
3. Photograph the **whole physical display**, including border/bezel and any unused
   area. Record whether horizontal stretching is absent, the full C64 canvas is
   visible and uncropped, and black sidebars (pillarboxing) or top/bottom bars
   (letterboxing) appear. A raw VICE screenshot alone does not show HDMI geometry.
   Do not demand exactly 4:3 or identical PAL/NTSC border widths.
4. While VICE is running, switch to tty2 and run `pcbm-diagnostics`. Capture the
   report; then return to tty1. The retained timed samples may better describe the
   VICE-active mode, since switching VTs can change display ownership/state.
5. In the report's latest launch log, retain `CBM_PRESENTATION` lines: driver,
   renderer/capabilities, chip/standard/aspect/fullscreen, window/output/logical
   dimensions, viewport/scale and SDL display mode. Preserve `active_drm` from
   timed samples: connector numbers/type and actual mode dimensions/refresh.
   Unavailable readings are limitations, not permission to add root access.
6. Type a short BASIC command. F10 opens VICE's menu; select Quit. Confirm clean
   return and responsive Project CBM Menu.

**If geometry is wrong or launch fails: collect diagnostics and STOP.** Do not try
aspect settings, renderer overrides, HDMI modes, package installs or monitor
scaling changes to make this candidate pass. No POC4 or other model test follows.

### Diagnostic files

`/home/pi/.local/state/project-cbm/diagnostics/` contains `report.json`, snapshots
and up to four launch directories. Copy/report them using the established offline
qualification process; SSH stays disabled. For extraction, mount the card's root
read-only with `ro,noload` in Linux or use a read-only ext4 reader. Do not repair
fsck or mount writable. The four-launch rotation will replace old launches: capture
primary geometry evidence before continuing through many media tests. Read-only
viewing/reporting on tty2 is allowed; changing diagnostic limits is not.

## 4. Bounded POC2 regression subset (only if geometry passes)

Through the ordinary CONTENT browser, load each existing qualification artifact:

| Content | Expected result |
| --- | --- |
| Programs / Qualification/pcbm-smoke.prg | PASS program screen, FOUR = 4 |
| Music / Qualification/pcbm-sid-check.prg | Triangle, saw and pulse original tones audible; DONE; mono SID, no PSID/RSID/stereo claim |
| Demos / Qualification/pcbm-video-input.prg | 16 color cells, moving star, keyboard code changes, preserved geometry |
| Programs / Qualification/pcbm-check.d64 | Disk attachment/loading executes smoke PASS |

For each, confirm F10/menu/Quit and responsive return. Mark joystick UNTESTED
unless hardware is available; it is not required for this gate. Repeat tty switching
while practical and record separately if it fails only during VICE. Perform normal
CBM reboot and confirm automatic Menu return. Do not infer broader persistence.

## 5. Optional PAL/NTSC preference check (after default geometry passes)

If familiar with VICE's ordinary machine/model settings, deliberately select an
NTSC C64 model, save settings through VICE, Quit and launch again. Record the exact
selected model and whether it persisted. Capture a whole-screen photo and diagnostic
record with standard/aspect values. Compare with the default PAL observation;
shape/margins may legitimately differ. This is an explicit user-preference test,
not permission to repair a failed default. Do not edit config files or pass custom
launch commands. If the setting is unclear, mark this check UNTESTED rather than
improvise. Stop on incorrect geometry; retain the chosen model in the report.

Other VICE profiles remain physically UNTESTED by this x64sc gate. Their generated
settings/reference tests do not qualify hardware behavior. Do not test another Pi
model automatically.

## 6. Return results and stop

Use [the planned matrix](poc3-pi3b.json): PASS / FAIL / UNTESTED separately. Supply
exact image hash, display setup, photos and diagnostic paths. Retain originals
externally, not large files in Git. The frozen image/lock cannot be changed to
record outcomes. Stop for owner review after this bounded test.
