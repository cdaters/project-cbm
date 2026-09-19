# POC4 attempt #8 — Pi 3 B+ performance qualification

**READY FOR OWNER PHYSICAL TEST: YES. READY TO FLASH: YES with verified recovery.**
All new physical results start UNTESTED. Verify the recovery manifest/restore report PASS.

| Identity | Exact binding |
| --- | --- |
| Product | 1.1.0-poc.4 / private-engineering-poc4, attempt 8 |
| Integration | `9aef29a7e87f7a88bd47d9f01c430aa3eb0c0b21` |
| Menu | v1.1.0_poc4.6 / `2ec5f8dcb04b5d86f64a2ce6a96625c3528eac73` |
| Lock | `inputs/frozen-poc4-attempt8/release-lock.json` |
| Lock SHA-256 | `53d2d25f997613434e16fdecc0057eeea88da74783f9487b2501cbec4d1cce57` |
| Raw | `artifacts/private-poc4-attempt-8/2026-09-18-project-cbm-1.1.0-poc.4-lite-private-poc.img`; 3095396352 bytes |
| Raw SHA-256 | `e4bb7f03ed26583097f92e8b8d1c2e9e4e3616d4d39940c78f70618ca3a81c40` |
| XZ | `artifacts/private-poc4-attempt-8/image_2026-09-18-project-cbm-1.1.0-poc.4-lite-private-poc.img.xz`; 599057044 bytes |
| XZ SHA-256 | `892082b4ef8468dab3273b4746350863f9bc75c17e6c2e18a0ef3b4eb62129e4` |

Paths are relative to `/Volumes/TheBench/ProjectCBM-Work`. Raw/XZ equivalence passes.
[Build report](../build/private-poc4-attempt8.md) / [exact results](../build/private-poc4-attempt8.json).
Recovery: `archive/poc4-attempt8-2026-09-18`; its manifest is the external authority.

## Before flashing

Use a fresh expendable card; preserve attempt #7 and its evidence. Verify the complete
raw or XZ SHA-256 above. Leave imaging-tool OS customization off. Record Raspberry Pi
**3 B+**, power supply, card, HDMI mode/display, audio path, keyboard and controller.
No other Pi model is qualified by this procedure. Record PASS / FAIL / UNTESTED for each
item. Do not wait to finish optional checks before reporting a core regression.

The default login is **pcbm**, Computer Name **projectcbm**. SSH uses the first-boot
owner password; File Sharing uses its separate password. Console/content remain pi.
Quiet/fast boot is unchanged; rainbow and Linux startup output are expected here.

## Core and account regression

1. Boot and complete first boot. Confirm masked password entry and readable ranges.
2. Confirm first Wi-Fi scan, connect or deliberately continue offline, reach Menu.
3. Check keyboard, default machine and current Main Menu/network/service status.
4. From Menu, Ctrl+Alt+F2 and Ctrl+Alt+F1 must work before emulation.
5. RUN C64: correct visible Cover, complete aspect-preserving canvas, keyboard and
   BASIC. Enter a short BASIC loop or your usual BASIC sanity commands.
6. F10 → Quit: responsive Menu; repeat both VT directions. Active-VICE VT remains the
   accepted separate limitation. Do not change console modes to force it.
7. Verify Advanced administration authenticates as pcbm. If using SSH for live metrics,
   explicitly enable Remote Access, confirm actual On and the displayed connection
   example, then connect from the other computer: `ssh pcbm@projectcbm.local` (or its
   displayed IP). Use the first-boot password; never put it in a command.
8. Confirm File Sharing's username/help is pcbm with a separate password if exercised.
   Verify enabling, actual state, direct connection, disabling and new-connection refusal.
9. Reboot safely: setup stays complete, Wi-Fi/name/preferences and intended services
   persist. Existing public/client-discovery limitations remain separately recorded.

## Performance workloads

Test a fresh default C64 configuration first. Do not restore attempt #7's VICE settings
before this comparison. The new initial C64 setting is reSID interpolation; x64sc, SID
filters, true-drive/VIC-II accuracy, CRT/display geometry and the shared launcher remain.
A saved VICE resource file can override this seed; record any intentional customization.

10. Launch an ordinary representative game/demo/disk workload you own. Allow loading
    and warm-up to finish, disable warp, and observe at least 60 uninterrupted seconds.
11. Repeat with the owner's **kong_arcade.prg**, 37,282 bytes, SHA-256
    `a80816ec175ffcbc44b4127f43ea43091df28494e8da9ef9e93bff72c1fdd554`.
    Supply it privately through USB/import or File Sharing; it is not bundled in the
    image. The earlier Mac copy was in `Downloads/c64/demos` on TheBench. Load it through
    normal CONTENT or VICE controls. Do not redistribute it with a report.
12. Record whether audio pitch/tempo and graphics run at the expected normal pace.
    Occasional display frame skipping is distinct from sustained emulation slowdown.
13. Collect objective speed records for each workload as described below. Repeat a
    second launch if an interval contains a menu, pause, reset, load or warp transition.
14. During the demanding workload, collect CPU clock/governor, temperature, throttling
    and emulator process/thread consumption. Useful read-only commands on the Pi are:

```sh
vcgencmd measure_clock arm
vcgencmd measure_temp
vcgencmd get_throttled
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq
top -H -p "$(pgrep -n -x x64sc)"
```

Run these through the authenticated remote shell while VICE stays on tty1, or capture
with the owner's usual monitoring method. Do not claim load-time or post-exit values
were taken during the slow segment. A full-speed CPU with no throttling is useful
context, not by itself a performance PASS. Do not install extra profiling packages or
change governor/display/accuracy settings on the qualification candidate.

15. F10 → Quit and verify immediate responsive Menu. Repeat the launch/Cover/quit path
    three times; verify both VT directions after quitting.
16. Launch other previously used machine profiles, check Covers/input/audio and their
    ordinary representative workload speed where practical. Report each independently.
    BASIC, ordinary disk software, SID/music and common peripheral/controller behavior
    should remain correct; software installation alone is not a qualification.

## Objective speed measurement

Private launch diagnostics keep `vice.log` under
`/home/pi/.local/state/project-cbm/diagnostics/launch-*`. Each process emits at most
120 `CBM_PERFORMANCE` records, normally one per five wall seconds. The sample number is
local to that launch. The telemetry reports raw emulation speed and emulated FPS;
VSync display refresh and rendered frames are different measurements.

After the workload is loaded and stable, note the next sample number from the active
launch. Select **12 consecutive complete samples** with no loading, pause, menu, reset or
warp, spanning at least 60 seconds. Do not choose only the fastest samples. Start the
measurement promptly after a new launch; telemetry ends after about ten minutes.
These directories are private to pi. From an authenticated administrator shell, use
`sudo grep CBM_PERFORMANCE` with the exact selected launch log path; keep the output
private. Never broaden directory permissions to make collection easier.
After a safe shutdown, preserve the log through the read-only evidence workflow; the
engineering collector already bounds/redacts logs, but complete logs remain private.

On the engineering host, run the read-only parser from this Product source:

```sh
python3 tools/vice_performance.py "$CBM_VICE_LOG" --first-sample 10 --last-sample 21
```

Replace 10/21 with the actual observed steady interval; these are not prescribed sample
numbers. The parser outputs only numeric fields and refuses malformed/incomplete
intervals. It does not copy surrounding paths or private network information.

**Performance PASS requires all of:**

- weighted emulation speed **98–102%** over that steady interval;
- no complete five-second sample below **95%**;
- warp off throughout, at least 12 consecutive samples and at least 60 seconds;
- emulated FPS consistent with the selected PAL/NTSC standard (roughly 50/60);
- correct normal audio pitch/tempo and visual pace, with no sustained slowdown;
- correct software behavior and successful repeated quit/Menu return.

An insufficient/malformed interval is UNTESTED, not PASS. A numeric PASS alone cannot
prove fidelity or real display/audio behavior. If a steady workload fails the speed gate,
the Pi 3 performance release blocker remains. Report the exact workload/settings and
interval; preserve diagnostics before experimenting. Do not silently switch to x64 or
disable accuracy features to turn this candidate's result into a pass.

## Evidence and stop

On regression, stop unrelated tests and preserve the relevant launch directory,
installed identity, selected numeric interval, workload hash, hardware-health readings
and owner observations. Do not collect shadow files, NetworkManager keys, Samba password
databases, shell history or unrelated home files. Retain original screenshots privately
outside Git with captions, byte counts and SHA-256. Safely shut down and follow the
read-only card policy; do not repair the tested candidate in place.

Report core/function/performance results separately. No performance PASS is inferred
for another Pi model or untested machine profile. Stop after owner testing; this procedure
does not authorize publication, quiet/fast boot changes or dropping the Pi 3 floor.
