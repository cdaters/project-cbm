# POC4 corrective attempt #5 — exact-hash Pi 3B regression

**READY FOR OWNER PHYSICAL TEST. READY TO FLASH: YES.**
All required offline gates passed. This candidate's physical results are **UNTESTED**.
Codex performed no physical test. [Build report](../build/private-poc4-attempt5.md) and
[exact result](../build/private-poc4-attempt5.json) record the validation and limits.

| Identity | Exact binding |
| --- | --- |
| Product | 1.1.0-poc.4 / private-engineering-poc4, corrective attempt 5 |
| Integration | `9b0220beaf49dca44862a6e9fe874f5e4fa96e8d` |
| Menu | `v1.1.0_poc4.3`, peeled `664b0a76b798a64d697e0d2d3baa0d45a5406ebd` |
| Lock | `inputs/frozen-poc4-attempt5/release-lock.json`, schema 4 |
| Lock SHA-256 | `4568aa184063aa7e3a0ae5217a98320f68735665f5e08340d48368530c88968e` |
| Raw | `artifacts/private-poc4-attempt-5/2026-09-18-project-cbm-1.1.0-poc.4-lite-private-poc.img`, 3087007744 bytes |
| Raw SHA-256 | `5385acc822d7f280dd2eb5654368ef282ed941d4dc946368871510d98c752e66` |
| XZ | `artifacts/private-poc4-attempt-5/image_2026-09-18-project-cbm-1.1.0-poc.4-lite-private-poc.img.xz`, 597605380 bytes |
| XZ SHA-256 | `3923c319e485bbccad642b8a8b8039fc8acd0694a308ec631aeeffa64ed3e567` |
| Raw/XZ equivalence | PASS in guest and external retained copies |

Bulk locators are relative to configured storage, currently
`/Volumes/TheBench/ProjectCBM-Work`. Recovery: `archive/poc4-attempt5-2026-09-18`.
The manifest/restore report binds final source refs, exact inputs and artifacts.

Attempt #4's [owner report and diagnostics](poc4-attempt4-card-review-2026-09-17.md)
remain unchanged: lifecycle PHYSICALLY PASSING on the tested Pi 3B; Cover FAIL.
This candidate corrects the confirmed tty admission contract defect while retaining
the same supervisor/terminal restoration bytes. The earlier failure's precise physical
branch was inferred, and attempt #3's root cause remains unproven. New physical Cover
rendering and continued lifecycle behavior must be established here.

Verify the image hash before flashing. Use the exact raw or XZ above, with no Imager
OS customization: Project CBM owns initialization. Preserve the master images, lock,
packages, previous test card/evidence and recovery records. Record Pi **3B**, card,
power supply, keyboard, display/cable/mode/scaling, audio and available controller.
Use a fresh disposable test card. Initial setup must finish to reach Menu; Stay Offline
is sufficient to begin the priority lifecycle gate. Later optional/network tests are
not prerequisites for that gate. Do not improvise power-loss tests or test another model.

Record each item as PASS, FAIL, UNTESTED, OBSERVED UX DEFECT, or NOT APPLICABLE, with
reason and observations. A returned Menu picture is insufficient: input must work.
Photographs show appearance; timing, audio, input and connectivity require observations.
Store photographs/logs privately under a new external qualification directory, with
original names, captions, byte counts and SHA-256. Never photograph or report credentials.

## Priority lifecycle: stop immediately on failure

1. Boot to Project CBM Menu.
2. Verify Menu keyboard controls before RUN.
3. Switch tty1 → tty2 with Ctrl+Alt+F2; verify shell input. Run `pcbm-diagnostics` to
   capture a pre-run snapshot. Return using Ctrl+Alt+F1.
4. Verify tty2 → tty1 and Menu input again.
5. Choose RUN; note the displayed default machine.
6. Verify that machine's correct Cover is visibly displayed. Record visible duration;
   intended presentation is approximately 0.75 seconds, not a frame seen in telemetry.
7. Verify sane artwork proportions and presentation without cropping or stretching.
8. Verify VICE launches once.
9. Verify POC3 true-aspect geometry, complete canvas and expected unused screen area.
10. Verify VICE keyboard input.
11. Verify F10 opens the VICE menu.
12. Choose Quit.
13. Verify Menu visually returns.
14. Verify Menu keyboard input **IMMEDIATELY**.
15. Verify Ctrl+Alt+F2 after return; collect diagnostics below before another launch.
16. Return tty2 → tty1 and verify Menu remains responsive.
17. Repeat the complete RUN → Cover → VICE → F10/Quit → Menu cycle, including immediate
    Menu input and both VT directions.
18. Repeat a **third** complete cycle. Preserve all three launch slots before routing
    tests; only four launch directories are retained and further launches rotate them.

Do not repair a failure with `reset`, `stty sane`, `chvt`, service restarts, configuration
file edits, package changes or repeated launches. Stop unrelated testing and preserve
state first. Keyboard/VT behavior on the physical Pi cannot be inferred from native PTY
or dummy-SDL tests.

## Cover routing after the priority gate

19. Verify default RUN Cover agrees with the saved profile.
20. Verify an explicit MACHINES profile launch, for example VIC-20, shows its Cover.
21. With a different default, use CONTENT to launch admitted C64 application content
    whose resolved profile is x64sc. Cover must match actual content profile, with the
    saved default unchanged. Record only exercised profiles as qualified.

## First-boot UX and persistence

Document these on initial setup and, where needed, a separately identified fresh card
flashed with the same exact image. Do not erase setup markers on a used card and call
it first boot. Detailed Wi-Fi testing can follow the priority lifecycle gate.

22. Human-readable region/language choices map internally to supported settings.
23. Human-readable keyboard selection; note that the new layout applies after reboot.
24. Named timezone selection; test Advanced for another supported identifier if useful.
25. Owner setup, password confirmation/retry, authenticated administration and clean
    return. No preset/default password or arbitrary passwordless root is expected.
26. Named Wi-Fi regulatory country appropriate to the actual location.
27. Stay Offline path on its fresh run; optional remote services remain off.
28. Wi-Fi scan with no Ethernet cable and an owner-controlled WPA-personal AP.
29. SSID selection; no unsupported/open/enterprise network claim.
30. Explicit hidden-password explanation; characters intentionally do not appear.
31. Successful association using owner-held credentials; do not retain those bytes.
32. Back/change/Forward at region, keyboard, timezone, country, SSID and password;
    Escape pauses. Resume must preserve completed owner enrollment without resetting it.
33. Safely test invalid input and connection failure/retry, alternate SSID/country and
    Stay Offline fallback. Confirm malformed/failed responses are understandable. Do not
    deliberately damage the filesystem or interrupt password writes/root expansion.
34. Truthful immediate working messages during region/account/scan/connect/save work;
    measure actual durations. Setup must not complete before the chosen network path
    finishes. A timeout is an unconfirmed result requiring retry, not rollback.
35. Reboot normally.
36. First boot does not unexpectedly rerun; capture actual capacity after expansion.

## Core media/audio/input

37. Run original `programs/Qualification/pcbm-smoke.prg`.
38. Run `music/Qualification/pcbm-sid-check.prg`.
39. Verify audible SID output, including all three expected voices. This is not
    PSID/RSID playback, dual-SID or fidelity qualification.
40. Run `demos/Qualification/pcbm-video-input.prg`.
41. Verify colors/movement and keyboard/input response.
42. Verify joystick when hardware is available; otherwise record UNTESTED with reason.
43. Load `programs/Qualification/pcbm-check.d64`.
44. After these launches, F10 → Quit → immediately responsive Menu and VT switching.

## Applications and utilities

45. CONTENT → Music → Creation → SID-Wizard: launch/use/save a small owner-created
    work to its working disk/return/relaunch. Root template remains unchanged.
46. CONTENT → Programs → Communications → StrikeTerm: launch/input/clean return.
    Private engineering admission remains; physical success grants no public rights.
47. FILES → Midnight Commander: browse/copy an owner-created content file; F10 returns.
48. Advanced Mixer: available controls/card selection, Escape return and later VICE
    audio. Devices without mixer controls may be NOT APPLICABLE. No sudo global store.
49. USB import with real removable owner-controlled test media: correct selection,
    destination/category/ownership, no overwrite, clean unmount and content discovery.

## Networking/services after lifecycle acceptance

Use only supported UI controls and authorized local clients/endpoints. Enable one
feature deliberately, record initial/final states, and disable it afterward. Lack of
AP/client/BBS equipment means UNTESTED or NOT APPLICABLE, not an invented failure/pass.

50. Wi-Fi reconnect and persistence after reboot.
51. System Information and CONTROL → Network → Network information must agree:
    interface name, Ethernet/Wi-Fi type, connection state, assigned IPv4/IPv6 CIDRs,
    effective current MAC and active SSID when available. Compare with the intended
    interface/AP without recording credentials; measure time to show the view on Pi 3B.
    Distinguish disconnected/unavailable
    from connected, and link/IP state from Internet access. Link-local IPv6 needs an
    interface zone. Saved connection names must not be presented as SSIDs. Verify
    clean presentation at the console width and safe handling of unavailable fields.
52. Samba/File Sharing: separate Samba credential, enable/configure/client connection
    to intended content share only, then disable.
53. SSH: explicitly enable, owner login/authenticated administration from trusted client,
    then disable. No root login or authentication workaround.
54. mDNS discovery when applicable, then disable.
55. TCPser/BBS when deliberately enabled, using an authorized endpoint; verify typed
    port/baud and return to disabled state. Do not expose a public inbound listener.
56. State reporting distinguishes configured, active, pending, unavailable and failed
    where the current implementation supports those states.

## Final persistence

57. Default-machine preference persists and RUN uses it.
58. Relevant VICE preferences persist without overwriting POC3 geometry defaults on launch.
59. First-boot selections persist.
60. Network configuration persists appropriately, including the selected offline state.
61. Normal reboot returns to the intended Project CBM startup path. If direct-machine
    startup is deliberately tested, launch once, Quit → Menu and verify recovery.

## Failure collection: no network requirement

**IF THE PRIORITY FAILURE REAPPEARS:
DO NOT REBOOT OR POWER OFF UNTIL THE NEW DIAGNOSTIC COLLECTION PATH HAS BEEN
ATTEMPTED, unless continued operation is unsafe.**

This applies to missing/failed/timed-out Cover, VICE launch failure or abnormal exit,
dead Menu input, broken VT switching and second/third-cycle failure. Stop launching:
rotation keeps only four slots. Do not enable SSH as a workaround. First try the
preverified tty2 route once; an already-working, deliberately enabled administration
channel is optional, not the only collection path.

Persistent directory: `/home/pi/.local/state/project-cbm/diagnostics/`.
Each `launch-*` slot contains the following when that phase was reached:

| File | Evidence |
| --- | --- |
| `pre-cover.json` | Original terminal modes/termios, tty, PID, session, process group and foreground group before Cover |
| `cover.json` | Cover PID, monotonic start/end, exit/signal, timeout/KILL flags, structured admission/skip, asset-ready and renderer initialization/backend/presented/released events |
| `post-cover.json` | Terminal readback immediately after Cover returns |
| `cover-cleanup.json` | Restoration attempt/errors/mismatch and verified readback before VICE |
| `before.json` | After Cover cleanup, before VICE: session/process/audio/DRM observations |
| `record.json` | Resolved profile/executable, VICE PID, phase, timing, status/signal |
| `sample-0.json` … `sample-2.json` | Bounded observations during sufficiently long VICE runs |
| `vice.log` | Bounded, redacted VICE output/geometry/ALSA observations |
| `post-vice.json` | Terminal readback after VICE, before final restoration |
| `cleanup.json` | Final restoration attempt/errors/mismatch and verified state before Menu |

Interpret new `cover.json` stages before assuming a renderer failure:

- `admitted`: stdin and controlling terminal identify tty1, VT1 was active and the
  existing group was foreground when checked. This is admission, not visibility.
- `skip_root`, `skip_non_linux`, `skip_nonterminal`, `skip_wrong_tty`,
  `skip_inactive_vt`, `skip_background`, `skip_tty_unavailable`: renderer was skipped
  for the stated guard reason; VICE must still proceed safely.
- `skip_arguments`, `skip_profile`, `skip_asset`: wrapper input/profile/file admission
  failed. `asset_ready` means the selected managed asset passed its wrapper checks.
- `initializing`, `video`, `renderer`, `presented`, `released`: successive SDL stages.
  `presented` means submission occurred; a photograph/owner observation is still
  required to establish visible Cover output. Preserve missing-stage evidence.

Cover stays in its parent's process group by construction; the parent/foreground
groups and Cover PID are retained, but there is no separate stored child-PGID field
or explicit reap boolean. A completed `cover.json` is written only after its wait/reap
path returns. Submitted presentation telemetry does not prove physical visibility.
Missing phase files are evidence gaps, never assumed success. Mode/ioctl availability
and permissions can limit collection; do not broaden privileges to hide that limit.

On tty2 as `pi`, preserve automatic records first, then request a fresh snapshot:

```bash
umask 077
state=/home/pi/.local/state/project-cbm/diagnostics
out=$(mktemp -d /home/pi/pcbm/programs/Qualification/poc4-attempt5-evidence.XXXXXXXX) || exit 1
mkdir "$out/automatic"
for slot in "$state"/launch-*; do
  [ -d "$slot" ] && [ ! -L "$slot" ] || continue
  target="$out/automatic/${slot##*/}"
  mkdir "$target"
  for name in record.json pre-cover.json cover.json post-cover.json cover-cleanup.json before.json sample-0.json sample-1.json sample-2.json vice.log post-vice.json cleanup.json; do
    [ -f "$slot/$name" ] && [ ! -L "$slot/$name" ] || continue
    cp -p -- "$slot/$name" "$target/$name"
  done
 done
cp /usr/share/project-cbm/identity.json "$out/identity.json"
pcbm-diagnostics
for name in snapshot.json report.json; do
  [ ! -f "$state/$name" ] || cp -p -- "$state/$name" "$out/$name"
done
find "$out" -type f ! -name SHA256SUMS -exec sha256sum {} + > "$out/SHA256SUMS"
printf 'Private evidence saved at %s\n' "$out"
```

These commands only copy the allowlisted evidence and request the bounded diagnostic
snapshot; they do not reset the terminal, relaunch VICE or repair the candidate.
Retain the output privately and review it before sharing: redaction is not a guarantee
against private filenames in free-form VICE output. Never copy the whole home, `/etc`,
NetworkManager profiles, passwords, keys or unrelated journals. Record failure time,
last successful step and whether each command/VT was accessible; a photo can preserve
visible state without claiming input responsiveness.

If both VTs are dead and no existing channel works, record that collection was attempted,
photograph the display and stop for review. Automatic phase files survive on the card;
no new launch is needed. After live-state preservation/review, offline collection may
use a Linux reader mounting the correct root partition **read-only with `ro,noload`**.
Identify the card by size/device/partition table; do not guess a disk number, run fsck
repair, or mount it writable. Copy only the diagnostic directory and minimal identity
to a new private external output directory, hash them, and unmount.

The owner also accepts a verified read-only Paragon mount as used-card engineering
runtime evidence when its historical journal-replay semantics are unknown. Verify
read-only flags before reading identity or allowlisted files; never call that pristine
forensic evidence. Do not remount, repair or write to the card. If read-only access
cannot be verified, stop collection for review. Networking is unnecessary.
Missing telemetry or a failed collection is reported honestly; neither proves a root cause.
