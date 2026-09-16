# POC2 Raspberry Pi 3B smoke test

**Owner completed the bounded test; see [results](poc2-pi3b.json) and
[geometry follow-up](poc2-pi3b-aspect-analysis.md).** This remains the procedure
used for POC2; its requested steps are not proof that each was performed. This private image is not a public
release or qualified appliance. Do not repair it during qualification.

## 1. Verify and flash the exact candidate

Candidate: **1.1.0-poc.2 / private-engineering-poc2**.
Files are under the configured bulk root, currently
`/Volumes/TheBench/ProjectCBM-Work`.

- XZ: `artifacts/private-poc2/image_2026-09-16-project-cbm-1.1.0-poc.2-lite-private-poc.img.xz`
- XZ bytes: `596406680`
- XZ SHA-256: `757aca812835c676d75eaad651b6739fc79461c25c8aa7426524f6692a6b3d9f`
- Raw: `artifacts/private-poc2/2026-09-16-project-cbm-1.1.0-poc.2-lite-private-poc.img`
- Raw bytes: `3095396352`
- Raw SHA-256: `ef221dc09ea65d3976f88e65cde8f153a9c32989be09c6b35d545b111ccb7467`
- Release-lock SHA-256: `bc1c6e16c32d6285973933b8d50371899bc18e5407dd654c9a14d1187eb194ac`

Verify the selected file with `shasum -a 256 FILE` (macOS) or `sha256sum FILE`
(Linux). Flash it using the normal image-writing workflow, checking the destination
card carefully. Record Pi model/revision, card/capacity, power supply, HDMI/display,
audio connection and attached keyboard/controller. Do not enroll networking or
use Imager customizations for this candidate. SSH remains disabled.

## 2. Establish boot and diagnostics before RUN

1. Boot the Pi 3B. Record time to a usable tty1 Main Menu, rendering and keyboard
   navigation. First boot may take longer while the filesystem expands.
2. Confirm the default is Commodore 64 / x64sc.
3. Press **Ctrl+Alt+F2**. Expect a non-root `pi` shell and engineering instructions.
   Run `id -u` (expect 1000), `uname -r`, `df -B1 /`, then `pcbm-diagnostics`.
   This creates a report without requiring a password, root shell or networking.
4. Return with **Ctrl+Alt+F1**. If this initial diagnostic path fails, stop and
   report it before launching VICE; do not improvise a login/sudo repair.

## 3. Test the default launch and return

1. Select **RUN** once. Record whether the C64 screen appears and elapsed time.
2. If it appears, type a short BASIC command, for example `PRINT 2+2`. Expect 4.
3. Press **F10** to open VICE's menu; select **Quit emulator** (confirm if asked).
   F10 opens the menu; it is not an immediate exit key.
4. Confirm that the CBM Main Menu is visible and keyboard navigation works again.
   Repeat once to catch terminal/session cleanup problems.

### If RUN black-screens or stops responding

- Wait about 60 seconds to allow the bounded diagnostic samples to complete.
- Try Ctrl+Alt+F2 once. If reachable, run `pcbm-diagnostics`; record whether x64sc
  appears as running and its state in the report. Do not kill/restart VICE as a fix.
- Reports/logs live at `/home/pi/.local/state/project-cbm/diagnostics/`:
  `report.json`, `snapshot.json`, and up to four `launch-*` directories containing
  `record.json`, `vice.log`, `before.json` and up to three samples.
- From an accessible tty2, `pcbm-system` provides the normal shutdown UI. If no VT
  is reachable, record that fact and the elapsed time, then stop the test. After
  power removal, preserve the card for read-only extraction; the newest buffered
  records are not guaranteed to survive an abrupt cut.
- After a failure/reboot, `pcbm-diagnostics` includes the previous launch record
  plus current state. If tty access never returns, extract that directory using
  a Linux reader, mounting the identified root partition read-only with `ro,noload`.
  Do not run a repair fsck or mount it writable. The same Linux builder can assist
  with a separately authorized read-only card/image extraction; no SSH is needed.
- Share the report and exact image hash. Review local diagnostic data before public
  posting. Record PASS/FAIL/UNTESTED; stop later tests, do not mark them failures.

**No package installs, OS/config repairs, service enablement, sudoers edits, new
kernel parameters, renderer overrides or replacement media on this frozen test.**

## 4. Test declared content through the normal browser

Keep default machine C64/x64sc. In **CONTENT**, choose the indicated category and
the listed `Qualification/filename`. Quit through F10 and verify CBM return after
each program.

| Category/file | Expected observation |
| --- | --- |
| Programs / pcbm-smoke.prg | `PASS: PROGRAM LOADED AND RAN`, arithmetic 4, READY prompt |
| Music / pcbm-sid-check.prg | Three separate original tones: triangle, saw, pulse; screen reaches DONE. Mono SID; no left/right or PSID/RSID claim |
| Demos / pcbm-video-input.prg | 16 color cells (including black), moving star, key-code changes when typing |
| Same input program, joystick | Port 2: neutral 31; up 30, down 29, left 27, right 23, fire 15; combinations differ. If no available/configured controller, mark UNTESTED and explain |
| Programs / pcbm-check.d64 | Disk autostarts the same smoke PASS screen. At READY, optionally `LOAD"$",8` then `LIST`: expect CBM SMOKE; `LOAD"CBM SMOKE",8` then `RUN` repeats the check |

Source/license/per-file hashes: [POC2 result](../build/private-poc2.json).
These original programs passed reference loading/execution checks; physical audio,
interactive input, timing and Pi-specific rendering remain to be established here.
A failed media test must be distinguished from absent audio/controller equipment.

## 5. Reboot and user-state checks (only after earlier steps pass)

Run `pcbm-diagnostics` again. Record root capacity/free space after expansion.
If testing persistence, use an ordinary documented VICE user preference and its
Save settings operation; record exactly what changed. This planned user-state test
is not permission to repair the OS, launcher or image. Reboot through CBM System,
confirm Menu arrival, diagnostics retention and the saved preference. Network/setup
screens should explain their engineering limitation; masked services are not failures.

Record results against [the qualification record](poc2-pi3b.json), with failures and
untested items separate. Stop after this smoke test for owner review. No POC3 or
broader qualification follows automatically.
