# Attempt #8: bounded live C64 engine A/B

**Attempt #8 physical performance: FAIL. No attempt #9 build is authorized yet.**
[Owner result](poc4-attempt8-pi3b-plus-performance-fail-2026-09-18.json).
The 36.9% native CPU reduction did not deliver sufficient Pi 3 B+ performance. It
remains evidence only for that native comparison. No hardware-tier default is selected.

## Identity and settings gate — existing owner SSH shell

These commands only read identity, package metadata and hashes. The owner enters any
sudo password locally, never in a command or report. No package installation, candidate
configuration edit, new SSH access or release-identity change is needed.

```sh
cat /usr/share/project-cbm/identity.json
dpkg-query -W project-cbm-vice
sha256sum /usr/bin/x64sc /usr/bin/x64
sudo -u pi sha256sum \
  /home/pi/.config/vice/sdl-vicerc \
  /usr/share/project-cbm/vice-defaults.ini \
  /home/pi/pcbm/demos/kong_arcade.prg \
  /home/pi/.config/pcbm/preferences.json
```

Expected attempt #8 identity:

- build_id/release_lock_sha256:
  `53d2d25f997613434e16fdecc0057eeea88da74783f9487b2501cbec4d1cce57`;
- integration: `9aef29a7e87f7a88bd47d9f01c430aa3eb0c0b21`;
- VICE: `3.10-1+pcbm4`, package SHA-256
  `a7b77c3b006eb190c64c10cadbfd91ce4152a73523c440496209293da2901dc1`;
- x64sc: `bc046286c8071a2e9ebeeabb923afb977528bf64b409e8fd8a7845cbda2ad69b`;
- x64: `df642b3c2d690a74f39273fe1d0fdc86cecd7e7180487dfde2b8398851d638c5`;
- both initial VICE configuration files:
  `48dbc0a4132ea8dcdd44e43a0052f3e9ee9689918161943e0555ad158b8440e9`;
- owner reference, 37,282 bytes:
  `a80816ec175ffcbc44b4127f43ea43091df28494e8da9ef9e93bff72c1fdd554`.

The exact frozen package/image validation establishes that both binaries were shipped.
Current live hashes must confirm that state. The preferences hash is a before/after
fingerprint, not a prescribed value. If a file is missing, the identity differs, or the
saved VICE configuration differs from the initial seed, retain the output and inspect
only relevant resources before proceeding; do not reset or overwrite it. If the owner
put the reference elsewhere, use its actual path and verify the same hash.

Both seed sections (C64 and C64SC) select reSID interpolation and identical per-chip
aspect/fullscreen settings. Both engines use the shared C64 PAL defaults, reSID/filter
and normal speed. The installed common launcher supplies SDL sound, ALSA and F10.
VICE's SDL default SaveResourcesOnExit is 0 and the seed does not override it. Do not
save settings or turn on saving-on-exit during this experiment. Check the active
settings in F10 if anything was changed in memory during the current session; start
fresh A/B sessions so previous in-memory changes cannot contaminate the comparison.

## Two launches on the physical Menu

Use the Pi keyboard for launching; SSH is for observation. This preserves tty1's
existing getty/PAM/session, Cover supervisor, SDL/KMS ownership and Menu return.
Do not start another graphical VICE process from SSH or launch it as root.

1. Before quitting the currently slow session, retain its existing numeric telemetry
   with the read-only command below. Label it the original failed run, not the fresh A.
2. F10 → Quit. Confirm responsive Menu.
3. **A:** MACHINES → **Commodore 64** (`x64sc`). Select the machine directly; do not
   choose DEFAULT. Load `kong_arcade.prg` inside that running VICE using the same method
   used for the original observation. Let loading/warp finish and reach the chosen
   active demo/game segment. Note the segment, audio/graphics speed and sample boundary.
4. Observe at least 60 uninterrupted seconds and collect the measurements below.
5. F10 → Quit. Confirm responsive Menu.
6. **B:** MACHINES → **Commodore 64 (fast)** (`x64`). Again select it directly, without
   entering DEFAULT. Load the identical payload inside VICE, use the same segment and
   observe/measure the same duration. Keep display/audio/peripherals unchanged.
7. F10 → Quit. Confirm responsive Menu, the original RUN default and ordinary Menu
   VT switching. Re-run the hash command above: VICE configuration, Product preferences,
   payload, binaries and identity must remain unchanged. Retain any discrepancy.

MACHINES' ordinary launch branch does not save the RUN default. Its initialization is
idempotent for valid existing preferences. Both profiles use the same Cover and shared
launch path. Loading within VICE avoids CONTENT's deliberate C64-core selection.
Only the existing appliance's ordinary bounded runtime diagnostics are produced; this
experiment installs no helper or persistent configuration. Leave those diagnostics in
place for preservation. Stop on any new lifecycle regression.

This existing profile route is smaller and safer than introducing a temporary graphical
SSH launcher. No extra command-line launch mechanism or new tty/device permission is
needed. No third configuration is selected: first establish the A/B result.

## Measurements — SSH while each workload is active

Use the same commands for both runs. Exactly one engine should be active:

```sh
pgrep -u pi -x 'x64(sc)?'
CBM_AB_PID=$(pgrep -u pi -x 'x64(sc)?')
case "$CBM_AB_PID" in ''|*[!0-9]*) echo 'Stop: expected one emulator PID' ;;
  *) top -b -H -d 2 -n 2 -p "$CBM_AB_PID" ;;
esac
sudo vcgencmd measure_clock arm
sudo vcgencmd measure_temp
sudo vcgencmd get_throttled
```

Use the second top refresh for the current two-second interval; the first can represent
an average since startup. Record the main emulation thread, SDL audio and system idle,
with the clock/temperature/throttling readings. Do not call post-exit readings active
workload measurements. The SSH shell variable disappears with that shell; it is not a
Project CBM preference. Do not change governor, affinity, voltage or display mode.

Read the latest launch's bounded speed records:

```sh
sudo -u pi sh -c '
  d=$(ls -dt /home/pi/.local/state/project-cbm/diagnostics/launch-* | head -n 1)
  test -n "$d" && test -f "$d/vice.log" || exit 1
  printf "%s\n" "$d"
  grep CBM_PERFORMANCE "$d/vice.log" | tail -n 16
'
```

Telemetry is capped at 120 records per launch, about ten minutes of wall time. In an old
session, the last recorded sample is not necessarily current. Fresh A/B launches reset
the counter. Observe the last sample just after reaching the target segment, then select
12 consecutive *subsequent* complete non-warp samples covering at least 60 seconds.
Exclude loading, pauses, menus and resets; do not cherry-pick fast samples. Check that
sample numbers advanced during the observed interval. If recording has ended or the
log rotated, that interval is insufficient evidence, not a performance PASS.

The engineering host can apply `tools/vice_performance.py` to the preserved log using
those explicit first/last sample numbers. It emits only numeric values. The established
metric gate is weighted speed 98–102%, no full window below 95%, at least 12 consecutive
samples/60 seconds, warp off. PAL should be roughly 50 emulated FPS (NTSC roughly 60);
these are emulated frames, not display scanout or rendered-frame counts.

For each run report: engine/hash, unchanged config/payload hashes, observed segment,
normal/slow SID tempo and pitch, normal/slow graphics, selected numeric samples,
main/audio-thread CPU, system idle, ARM clock/temperature/throttling, F10/Quit and Menu
return. A numeric PASS also needs correct visible/audible behavior. One successful demo
is a credible correction lead, not broad compatibility or another-model qualification.

## Decision after physical evidence

If x64 sustains real time and behaves correctly, retain that result and assess ordinary
C64 games, demos, disk software, music and peripherals before choosing a hardware-tier
policy. The retained VICE 3.10 manual's C64 features section distinguishes x64 from
x64sc's finer cycle-based/pixel-accurate VIC-II behavior and higher host demand; it does
not justify calling x64 wholly non-cycle-accurate. Timing-sensitive effects may differ.
Use exact observed compatibility evidence, not merely the engine's name or VM results.

If both are slow, compare the measured speed deficit and shared display/audio settings
before proposing at most one justified third case. Do not build a candidate speculatively.
No new image, package/default change, quiet/fast boot work or Pi 3 support withdrawal
is authorized by this test. Existing candidate artifacts/recovery remain immutable.

Current access limitation: automated SSH has no usable authentication and computer-use
access to the owner's open SSH terminal is unavailable. Owner-run read-only output and
physical observation are required; do not share passwords or add access merely for this test.
