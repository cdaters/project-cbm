# RC2 Pi 4 B physical regression and performance procedure

**READY FOR OWNER PHYSICAL TEST: YES after recovery verification.**
**READY TO FLASH: YES.** Every RC2 physical result begins UNTESTED.
[Build report](../build/private-rc2.md) · [exact results](../build/private-rc2.json).
Recovery: `archive/rc2-2026-09-19`; verify its manifest SHA and restore-report PASS.

| Identity | Exact binding |
| --- | --- |
| Product | 1.1.0-rc.2 / private-engineering-rc2 / attempt11 |
| Integration | `e09a285f199fdcf29c6ad7d5dac92bbfefd262b4` |
| Menu | v1.1.0_rc2 / bcbf61e9e3d263f409b4983b5c2a30d6bf37f18f |
| Lock | `inputs/frozen-poc4-attempt11/release-lock.json` |
| Lock SHA-256 | `9831849a3fd12c12528e09d1b7f265d9b03e48ca2819b99f0dfe4583156e7581` |
| Raw | `artifacts/private-rc2-attempt-11/2026-09-19-project-cbm-1.1.0-rc.2-lite-private-rc1.img`; 3095396352 bytes |
| Raw SHA-256 | `f3b21038c1fc289c58396cb8106348cd3cda514a96548e5c6d0c9277fced1be4` |
| XZ | `artifacts/private-rc2-attempt-11/image_2026-09-19-project-cbm-1.1.0-rc.2-lite-private-rc1.img.xz`; 598069592 bytes |
| XZ SHA-256 | `f4b638100f37d673d9a455015121a8ea753b9bcd2daeca02630cba9e33a24ca9` |

Paths are relative to `/Volumes/TheBench/ProjectCBM-Work`. The legacy private-rc1
filename suffix is preserved from the exporter; installed identity is RC2. Use these
exact hashes, not a guessed filename. Raw/XZ equivalence passes in both locations.

## Prepare and stop conditions

Use a fresh expendable card and preserve RC1 unchanged. Verify the selected raw/XZ
hash above, then flash with imaging-tool OS customization disabled. Record **Pi 4 B**,
RAM, card, supply, cooling, display/HDMI/audio, keyboard and enabled services. Each
function begins UNTESTED; another model is not qualified by this procedure.

Stop and preserve evidence on a core boot, input, Cover, VICE or return regression.
You need not finish optional tests first. Do not repair the qualification card in
place or change emulator settings to obtain a performance pass.

## Boot presentation, timing and setup

1. Time power-on to a Menu that accepts keyboard input. Record setup time separately.
   Confirm suppressed rainbow/routine Linux output and a **visible graphical Project
   CBM primary image before Menu**, not just console text. The retained historical
   graphic says Model 5 / 500; that wordmark is not the hardware support policy.
2. Complete region, keyboard, timezone, masked owner password and first Wi-Fi scan/
   connection. Confirm correct password ranges and truthful working/error feedback.
   The one normal username is **pcbm**, home **/home/pcbm**; Computer Name defaults
   to **projectcbm**. No separate pi password or account switch should be needed.
3. Check concise Main Menu state and detailed Network/System Information, including
   gateway/DNS where supplied. Exercise Wi-Fi/Ethernet/multiple/no connection where
   practical and report these separately; unavailable values must not be invented.
4. Reboot safely. Confirm no setup rerun and intended Wi-Fi/name/service persistence.
   Measure three comparable subsequent boots, with the same peripherals/services.
   Primary graphic must appear each boot and yield cleanly to responsive Menu.
5. From enabled SSH, collect read-only timing and the numeric session trace:

```sh
systemd-analyze time
systemd-analyze critical-chain getty@tty1.service
systemd-analyze blame | head -n 20
python3 - <<'PY'
from pathlib import Path
for p in sorted(Path.home().joinpath('.local/state/project-cbm/boot').glob('boot.*.tsv'), key=lambda p:p.stat().st_mtime)[-3:]:
    print(p.name)
    print(p.read_text())
PY
```

RC1 measured about 30 seconds power-to-Menu, kernel 2.354s plus userspace 15.314s;
getty started 8.261s into userspace. Its journal places getty at 10.615919 and PAM
opening at 15.749980 monotonic seconds. RC2 removes the evidenced Type=idle deferral,
adds an intentional 1.5-second graphic dwell and traces the remaining path. Compare
monotonic origins correctly; never add concurrent unit durations. `dialog_dispatch`
marks invocation, while `first_input` marks completion of an interaction. Neither
alone proves first-frame readiness. Report actual savings or regression; no precise
speedup is preclaimed. Do not disable network waits to improve the result.

## Core lifecycle and unified files

6. From Menu, Ctrl+Alt+F2/F1 must work. RUN C64: correct machine Cover, complete
   geometry, keyboard, BASIC and audio. F10→Quit must return promptly to responsive
   Menu. Repeat at least three times and repeat VT switching after exit. The separate
   accepted VICE-active VT limitation remains; quit VICE before switching.
7. CONTENT and FILES use **/home/pcbm/content**. FILES offers Browse files and Import
   from USB. Browse files must open Midnight Commander with library/home panels;
   navigate/read/write your content without sudo or a second account, then F10 returns.
8. SSH/SFTP as pcbm starts in /home/pcbm. Copy a permitted small C64 file into
   `content/demos/c64`; it must be visible and launchable in CONTENT. Check its
   ownership with `ls -l` if needed. Existing configuration/diagnostics belong to pcbm.
9. On an expendable FAT/exFAT USB drive, place permitted test files. Choose FILES→
   Import from USB (or CONTENT→IMPORT), the partition, C64 and Demos. The working
   screen must stay readable, then report a definite copy/skip result and safe release.
   Find files under `content/demos/c64/Imported`, launch them, and repeat import:
   existing files must be preserved and counted as skipped. Test ext4 if practical.
10. If import fails, leave the result screen visible and report its exact reason.
    A confirmed unmount allows removal; an unconfirmed/failed unmount means retain the
    drive until safe shutdown. Do not repeat rapidly or assume a fleeting shell message
    was success. Do not artificially damage a filesystem to exercise failure labels.
11. Test another supported machine-family file, optional SID-Wizard and private-admitted
    StrikeTerm, joystick/peripherals and BBS/Modem where practical. Report each separately.
    Generic SID playback is not supplied. Use VICE settings for ROM/REU resources.

## Pi 4 real-time performance

12. Keep normal C64 **x64sc**, initial preferences, correct PAL/NTSC expectation and
    warp off. Test BASIC, an ordinary game/disk workload, then owner-supplied
    **kong_arcade_oxyron.prg**, 37,282 bytes, SHA-256
    `a80816ec175ffcbc44b4127f43ea43091df28494e8da9ef9e93bff72c1fdd554`.
    The payload is not bundled or redistributed.
13. After loading/warm-up, observe at least 60 uninterrupted seconds: correct SID
    pitch/tempo, graphics pace, software behavior. Note frame drops separately from
    whole-machine slow motion. Repeat F10/Quit/launch and confirm responsive Menu.
14. During active emulation, collect these read-only health values (authenticated sudo
    is acceptable if vcgencmd needs it; no separate pi password):

```sh
vcgencmd measure_clock arm
vcgencmd measure_temp
vcgencmd get_throttled
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq
top -H -p "$(pgrep -n -x x64sc)"
```

15. Preserve numeric `CBM_PERFORMANCE` lines from the exact launch under
    `~/.local/state/project-cbm/diagnostics/launch-*/vice.log`, directly readable as pcbm.
    Record when the settled workload begins. Engineering selects **12 consecutive
    complete non-warp samples spanning at least 60 seconds**, excluding loading, F10,
    pause/reset and quitting. Do not cherry-pick good intervals. Telemetry ends after
    120 samples (about 10 minutes); collect within that window. A read-only numeric extract:

```sh
python3 - <<'PY'
from pathlib import Path
root=Path.home()/'.local/state/project-cbm/diagnostics'
for p in sorted(root.glob('launch-*/vice.log'))[-2:]:
    print(p.parent.name)
    for line in p.read_text(errors='replace').splitlines():
        if line.startswith('VSync: CBM_PERFORMANCE '):
            print(line)
PY
```

Engineering parses the retained extract with `tools/vice_performance.py`, using the
recorded settled interval (10–21 is an example, not a universally valid selection).
PASS requires weighted 98–102% speed, no complete sample below 95%, expected PAL/NTSC
emulated FPS (roughly 50/60), warp off, correct audio/visual pace/compatibility and
reliable Menu return. Emulated FPS is not physical display refresh. Insufficient
measurement stays UNTESTED. RC1's reference PASS does not qualify this new candidate.

## Services and recovery

16. Enable Remote Access; confirm actual On, correct Computer Name/IP/username/help.
    Connect from another computer using `ssh pcbm@projectcbm.local` or displayed IP
    and first-boot password. Verify reboot persistence; disable and verify a new
    connection is refused.
17. Set the separate File Sharing password, enable sharing and confirm actual state/
    Network Discovery. Connect using the displayed Mac/Windows address, username pcbm,
    share **Project CBM**. Copy into demos/c64; CONTENT/FILES/SSH must see the same
    library with usable permissions. Test discovery separately from direct connection,
    reboot persistence, disable and refusal. Windows tests may remain UNTESTED if absent.
18. Confirm Computer Name changes update connection help/resolution and persist.
    Check Advanced Terminal is pcbm; Owner Administration asks for the first-boot
    password and returns safely when exited. Do not disclose passwords in reports.
19. Confirm safe shutdown, normal tty2 recovery and enabled SSH diagnostics. Preserve
    installed identity, boot traces, primary-presentation.json and relevant launch
    cleanup/performance records if anything fails. Do not collect credential files,
    Samba secrets, private keys or history. Photos/logs remain private outside Git,
    with caption/bytes/hash. Follow verified read-only evidence policy for a removed card.

**Stop for owner physical qualification. No publication or additional hardware claim.**
