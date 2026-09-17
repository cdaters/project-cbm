# Next-candidate physical regression procedure — unbound draft

**NOT READY TO FLASH. No candidate, package version, release lock or image hash is
assigned by this document.** First resolve the [existing-card evidence request](poc4-regression-collect-evidence.md),
then complete and review source corrections. Construction requires separate owner
authorization. Do not apply this procedure to an invented POC4 attempt #4 or POC5.

After an authorized construction passes offline checks, bind a new copy of the procedure
to its Product integration commit, explicit Menu tag/peeled commit, package hashes,
lock/raw/XZ hashes and physical equipment. Preserve this draft and earlier exact-candidate
records. Record PASS, FAIL, UNTESTED, OBSERVED UX DEFECT or NOT APPLICABLE with reasons.

## Lifecycle gate — Pi 3B first

1. Boot to Menu. Record keyboard, storage, power, display/mode/scaling, audio path and
   controller equipment. Confirm Menu controls work.
2. Before VICE: tty1 → tty2 works, diagnostic shell input works, tty2 → tty1 works.
   Capture bounded initial state using the reviewed diagnostics available in that candidate.
3. RUN resolves the displayed saved/default machine. Correct Cover is visibly present,
   preserves artwork proportions and has a bounded measured duration. Record the first
   visible frame and clean transition; no forced display mode or lingering process.
4. VICE starts once, correct C64 geometry/full canvas and expected unused display area
   remain. Keyboard works; joystick works where hardware is available.
5. F10 opens VICE menu; Quit exits. Menu must visibly return **and accept keyboard input
   immediately**. An image of Menu alone is not a pass.
6. Ctrl+Alt+F2 works immediately after return. Capture post-return diagnostic state on
   tty2; return to tty1 and confirm Menu remains interactive.
7. Complete a second full RUN → Cover → VICE → F10/Quit → Menu cycle, repeating input
   and both VT directions. Prefer a third cycle to expose accumulated state.
8. Check before-Cover, after-Cover, VICE-running and after-cleanup evidence for tty,
   foreground group, session, keyboard/display modes and successful resource cleanup
   **if the corrected diagnostics provide those fields**. No stale renderer/VICE process,
   zombies, inherited changed mode, open input ownership or leaked mounts. Missing
   telemetry is an evidence gap, not success inferred from the display.

Stop at the first functional failure, preserve logs before rotation, and do not apply
`reset`, `stty sane`, `chvt`, service restarts, package changes or repeated launches to
make a failure disappear. Current-source evidence collection does not authorize running
this future procedure on hardware.

## Cover/profile routing

Verify default RUN, one explicit MACHINES launch (for example VIC-20), and CONTENT whose
actual validated launch profile differs from the user's default (for example admitted
C64 application content while default is VIC-20). The Cover must match the **actual
launch profile**, with preferences unchanged by the content override. Record each
exercised profile separately; do not infer all eleven profiles passed.

## Fresh first boot

Use separately identified fresh cards/runs for Stay Offline and no-Ethernet Wi-Fi. Do
not erase first-boot state on a used card and call it a fresh candidate test.

Verify initial expansion and measured free capacity, human-readable region/language,
keyboard and timezone, owner initialization/authenticated administration, optional
networking, country/radio, scan, SSID selection, password feedback and connection result.
Record which keyboard layout is active during passwords and when a saved layout applies.

Exercise Forward → Back → change → Forward; Cancel/Escape at every stage; invalid-input
retry; mismatched confirmation; authentication failure → retry password → alternate SSID
→ country/radio → Stay Offline. Use only owner-controlled APs and synthetic test
credentials, including supported punctuation/spaces. Never capture credential bytes in
logs, argv, screenshots or reports. Verify markers do not falsely complete incomplete
work; interrupted setup resumes coherently on separately authorized disposable media.

Measure meaningful operations from dispatch to result: root growth/sync, locale
generation, keyboard compilation, timezone, owner preparation, country/radio, scan,
connection and final save. Record actual elapsed time and whether truthful feedback
appeared immediately. No fake percentages. Explicitly record bounded failure and safe
retry after an operation timeout; eventual success alone is insufficient UX evidence.

Verify completion, reboot, no unexpected setup replay, and actual tested persistence.
For Wi-Fi verify reconnect after reboot separately from initial password acceptance.
Local network availability and Internet connectivity are different claims.

## Core and remaining qualification

Re-run the existing original `pcbm-smoke.prg`, `pcbm-sid-check.prg`,
`pcbm-video-input.prg` and `pcbm-check.d64`: loading, arithmetic, three expected SID
voices, colors/movement, keyboard, joystick where available, correct geometry and
clean interactive return. Preserve POC3 true-aspect/desktop-fullscreen behavior and
saved VICE preferences. No PSID/RSID or fidelity claim follows from SID tones.

After the priority gates pass, qualify separately:

- SID-Wizard launch/use/save/relaunch and StrikeTerm launch/use/return; presence is
  already reported in attempt #3 but functionality remains untested.
- USB import, destination/ownership/no overwrite/unmount; mc file operations/return;
  Advanced Mixer and later VICE audio. No-control digital mixers may be NOT APPLICABLE.
- Wi-Fi reconnect; Samba from another machine; SSH enable/connect/disable; TCPser/BBS
  end-to-end; mDNS where applicable. Services require explicit supported opt-in and
  return to the declared disabled state afterward.
- Broader preferences, direct-machine boot once per login, return to Menu, service
  persistence and configured/active state reporting.

Absent AP/client/BBS/controller means a reasoned UNTESTED/NOT APPLICABLE result,
never a fabricated failure or pass. No additional Pi model, publication, rights change
or independent reproducibility claim follows from this procedure.
