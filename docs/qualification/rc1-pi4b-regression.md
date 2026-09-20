# RC1 Pi 4 B physical regression and performance procedure

**READY FOR OWNER PHYSICAL TEST: YES, after recovery verification.**
**READY TO FLASH: YES.** All new physical functions start UNTESTED.
[Build report](../build/private-rc1.md) · [exact machine-readable results](../build/private-rc1.json).
Recovery `archive/rc1-2026-09-19`: verify manifest SHA and restore-report PASS first.

| Identity | Exact binding |
| --- | --- |
| Product | 1.1.0-rc.1 / private-engineering-rc1 / attempt9 |
| Integration | `8401248a94132b386f9d6804823e0c4e3cd247dc` |
| Menu | v1.1.0_rc1 /4346a350d481f4da3a6abc6524373333637dbb82 |
| Lock | `inputs/frozen-poc4-attempt9/release-lock.json` |
| Lock SHA-256 | `e586ae09b6ff486239dc93f814171f0ce0dd0f0fe8bf8b62f3c06f96a345fd9f` |
| Raw | `artifacts/private-rc1-attempt-9/2026-09-19-project-cbm-1.1.0-rc.1-lite-private-rc1.img`; 3095396352 bytes |
| Raw SHA-256 | `7edc2452529dea92623b07a42036ce74ac7c7b84968d449336cdb4f250578115` |
| XZ | `artifacts/private-rc1-attempt-9/image_2026-09-19-project-cbm-1.1.0-rc.1-lite-private-rc1.img.xz`; 599213904 bytes |
| XZ SHA-256 | `84057184795bc05a805e9aa4e8caf971e47f8fbc084396365a671611377798e0` |

Paths are relative to the configured external bulk workspace, currently
`/Volumes/TheBench/ProjectCBM-Work`. Raw/XZ equivalence passes on guest and external copies.

## Prepare

Use a fresh expendable card and retain attempt #8 unchanged. Verify the selected raw
or XZ hash above before flashing; turn imaging-tool OS customization off. Record Pi
**4 B**, RAM, card, power supply, display/HDMI mode, audio, keyboard/controller and
network/service choices. This procedure does not qualify another model.
Record PASS/FAIL/UNTESTED for each function. Stop for evidence on a core regression;
optional tests need not be completed first. No physical result is inferred from offline gates.

## Boot, setup and return

1. Time power-on to an **interactive** Menu. First boot includes expansion/setup and
   must be reported separately from subsequent boots. Confirm rainbow suppression,
   readable Project CBM presentation and reduced routine Linux output. Photograph any
   malformed text or unwanted output. Text appears through the existing console session;
   an animated early-firmware graphic is not promised.
2. Complete region/keyboard/timezone, masked owner password and first Wi-Fi scan/connect
   (or deliberately choose offline). Confirm readable password ranges, working feedback,
   setup completion, keyboard and status. Username is **pcbm**, Computer Name **projectcbm**.
3. Check Main Menu's concise machine/network/service state; verify detailed Network
   and System Information show current gateway/DNS when supplied by the network. Test
   no connection, Wi-Fi, Ethernet and both together where available. Do not assume
   interface names. Unavailable fields must not show invented values.
4. From Menu switch Ctrl+Alt+F2/F1. RUN C64: visible correct Cover, complete geometry,
   keyboard, BASIC, audio; F10 → Quit must return promptly to responsive Menu. Repeat
   three times and repeat VT switching after exit. VICE-active VT remains the accepted
   separate limitation; do not force a kernel/console-mode workaround.
5. Reboot safely. Confirm setup does not rerun, Wi-Fi/name/preferences/services persist
   as configured, and the Menu still responds. Measure three subsequent power-on-to-Menu
   runs with comparable peripherals/services. Capture these read-only commands:

```sh
systemd-analyze time
systemd-analyze critical-chain
systemd-analyze critical-chain getty@tty1.service
systemd-analyze blame | head -n 20
```

The unchanged attempt8 baseline was kernel2.390s + userspace16.960s =19.351s;
tty1 getty began at9.956s userspace. NetworkManager-wait-online5.966s delayed the
Samba/graphical target path, not that tty1 chain. First-boot initialization1.885s was
reported on the completed system. Power-to-interactive-Menu was **not measured**.
Compare the new initialization duration and full timings without adding parallel
unit durations or treating getty activation as interactive Menu. No required speedup
in seconds is invented: pass requires reliable startup without a repeatable regression;
report measured savings separately. Do not disable services just to improve the score.

## Canonical library and applications

6. The library is **/home/pi/pcbm**, independent of the administrator home **/home/pcbm**.
   FILES should open the library. CONTENT should browse games/demos/programs/music/roms
   and machine folders. Test a C64 file in demos/c64 and another machine's supported
   file in its family folder; CONTENT should select a compatible profile without
   changing RUN's saved default. Shared/older unclassified files use the default.
7. USB IMPORT: select partition, machine, category. Confirm category/machine/Imported,
   regular file ownership/use, duplicate preservation and safe completion/unmount.
   SID imports belong in music/c64/Imported; generic SID playback remains unavailable.
   Do not use ROM/REU resources as autostart programs; use VICE settings.
8. Supply the private reference through File Sharing or controlled import, placing it
   in demos/c64. SFTP starts in /home/pcbm; uploading there does not add to CONTENT.
   Do not copy old whole home/config/credential trees onto the fresh candidate.
9. Exercise Midnight Commander, SID-Wizard, StrikeTerm (private admission only), other
   machine profiles, joystick/peripherals and BBS/Modem where practical. Report each
   independently; installed software alone is not PASS. Use your own permitted media.

## Pi 4 real-time performance

10. Start with fresh seeded VICE preferences: normal C64 **x64sc**, PAL/NTSC appropriate
    to the workload, warp off during measurement. Test BASIC, an ordinary game/disk
    workload, then owner-supplied **kong_arcade_oxyron.prg** (also previously named
    kong_arcade.prg),37,282 bytes, SHA-256
    `a80816ec175ffcbc44b4127f43ea43091df28494e8da9ef9e93bff72c1fdd554`.
    It is not bundled or redistributed. Do not tune the candidate solely for this demo.
11. After loading/warm-up, observe at least 60 uninterrupted seconds. Record correct
    SID pitch/tempo, graphics pace, software behavior and any dropped frames separately
    from whole-machine slowdown. Repeat launch/quit and verify responsive Menu return.
12. While the workload runs, use enabled/authenticated SSH for read-only health readings:

```sh
vcgencmd measure_clock arm
vcgencmd measure_temp
vcgencmd get_throttled
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq
top -H -p "$(pgrep -n -x x64sc)"
```

If vcgencmd requires permission, use authenticated sudo for that fixed command.
Collect readings during active emulation, not loading or after quitting. Do not install
profilers or change the governor/audio/geometry/accuracy to obtain a pass.
13. Preserve `CBM_PERFORMANCE` records from the exact launch's `vice.log` under
    `/home/pi/.local/state/project-cbm/diagnostics/launch-*`. Use authenticated sudo to
    read pi-owned logs; do not broaden their permissions. Record the next sample after
    the workload settles and take **12 consecutive complete non-warp samples spanning
    at least 60 seconds**, excluding loading, F10, pause, reset and quitting. Do not
    select only favorable intervals. Logs stop telemetry after 120 samples (~10 minutes).
    On the engineering host, parse the actual observed interval:

```sh
python3 tools/vice_performance.py "$CBM_VICE_LOG" --first-sample 10 --last-sample 21
```

Replace 10/21 with your recorded interval. **Performance PASS requires** weighted
98–102% emulation speed, no complete sample below 95%, expected emulated PAL/NTSC FPS
(roughly 50/60), warp off, correct visual/audio pace and compatibility, and successful
repeated Menu return. Numeric FPS describes emulated frames, not physical refresh.
Insufficient telemetry is UNTESTED. A new steady slowdown is a release blocker on the
Pi4 floor. Attempt8's Pi4 PASS does not qualify this fresh image or every workload.

## Services and recovery access

14. Remote Access: enable; confirm actual On and displayed computer/IP/username/help;
    connect using `ssh pcbm@projectcbm.local` or the displayed IP with the first-boot
    password. Reboot/persistence as intended, disable, verify a new connection is refused.
15. File Sharing: set its separate password, enable, confirm actual On and Network
    Discovery state. Connect on Mac using the displayed SMB address and on Windows
    where available; username pcbm, actual share **Project CBM**. Confirm files appear
    under the canonical library and remain usable in CONTENT. Check permissions,
    discovery, reboot/persistence, disable and refusal of new connections. Report
    direct connection and browsing/discovery separately.
16. Change Computer Name through CONTROL, verify updated address/help and resolution;
    restore your chosen name, confirm persistence. Check relevant service state On,
    Off, Pending/Failed/Unavailable feedback where naturally observed. Do not create
    artificial network damage merely to exercise a label.
17. Confirm tty2/Advanced and enabled SSH remain usable recovery routes. Follow
    [boot recovery](../release/boot.md) if verbose output is needed; first preserve the
    unchanged failing candidate and diagnostics, and record any later modified state
    separately. Shutdown must complete safely before removing power or the card.

## Evidence and stop

Preserve installed identity, relevant allowlisted launch logs/cleanup records, timing,
health readings, selected numeric interval, workload hash and owner observations.
Keep screenshots/logs private outside Git with captions/bytes/SHA-256. Do not collect
shadow files, Wi-Fi keys, Samba password databases, private keys or shell history.
Use the verified read-only card policy after safe shutdown; do not repair the tested
qualification card in place. Report critical failures immediately and keep untested
items explicit. **Stop for owner review; no publication or automatic support claim.**
