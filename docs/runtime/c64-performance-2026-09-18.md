# C64 performance correction and account refinement — 2026-09-18

Attempt #7's [owner report](../qualification/poc4-attempt7-pi3b-plus-performance-2026-09-18.json)
is a Pi 3 B+ **release-blocking real-time failure**, not just missing frames. Music and
graphics both slow while x64sc's main thread occupies approximately one core. Captured
1.4 GHz, 45.1 C, throttled=0x0, available memory and unused swap do not suggest thermal,
undervoltage or memory pressure at observation time. They are snapshots, not proof of
all conditions throughout the run. Unreported functions remain UNTESTED.

## Exact evidence and installed state

The removable external USB card root was verified read-only before interpretation.
Its installed identity equals `make_identity()` for attempt7 lock
`1c25d7f7850c63c41e2730bdaef2deef9cd6d0ccf1321c9b23fd4d9228926b3d`.
The already-mounted Paragon collection is engineering evidence, not a claim of pristine
forensic acquisition or no prior journal replay. No card writes/remounts occurred.
Six screenshots plus relevant identity/configuration and bounded persistent diagnostics
were copied/hashed/captioned outside Git under the registered workspace's
`qualification/poc4-attempt7-performance-2026-09-18`. Its initial 21-file manifest SHA-256
is `1cd2a6527570bf287aaa9f2cae081a9076081046dffe02b6decdd59ab4a164bc`.
Private LAN addresses in originals remain outside public documentation.

Installed VICE is `project-cbm-vice 3.10-1+pcbm3 arm64`, package SHA-256
`c9d798a591c22faa9ffc3141b7f5177ece36a05e53d9d2c8aae1ce93c22fcfbe`.
Card x64sc SHA-256 `96e529227caadb338ba34790ef79f09ec557f4e2e7c0fe98b5f076b5a4db1f0a`
and x64 SHA-256 `a094899b2be748fb6c5371392087a938076794028d26503f2e41ebacca27a480`
match the retained native package executables. Both engines really are installed.

The exact logged invocation is `/usr/bin/x64sc -sounddev sdl -menukey 291 +logcolorize -logfile -`.
The saved `sdl-vicerc` contains only the Product geometry/fullscreen seed. The final
resource log reports no changed SID, drive, speed or accuracy resource. Runtime reports
KMSDRM/OpenGL, true aspect, complete fullscreen 1920x1080@60 presentation, VSync enabled,
SDL-to-ALSA audio, reSID MOS8580 with filters, 48 kHz resampling, and repeated delays
exceeding one second. Compiled defaults include 100% speed and CRT rendering; no observed
user-saved performance override explains the failure. VICE's emulation thread includes
CPU/chip and SID synthesis work; low SDL audio-thread CPU does not make synthesis cheap.

The owner identified `kong_arcade.prg`; card and separately supplied copy are identical,
37,282 bytes, SHA-256 `a80816ec175ffcbc44b4127f43ea43091df28494e8da9ef9e93bff72c1fdd554`.
Only private external qualification copies are retained. It is excluded from source,
packages, image content and public redistribution.

## Bounded comparisons and decision

The preserved 1.0 runtime also selected x64sc and SDL/ALSA. Its source example contains
presentation offsets/filtering rather than a recovered Pi 3 speed preset. VICE is 3.10
in both generations. The historical build transcript predominantly contains `-O3`,
including upstream host-native checks; current Debian packaging supplied `-O2`.
We restore portable `-O3`, not the historical host-native instruction selection. The
historical image is not rebuilt or treated as a reproducible equivalent configuration.

The native Apple ARM64 Debian builder is useful for relative CPU costs, not Pi capacity.
Original synthetic workloads compared sampling modes, CRT/internal-size choices and the
installed x64 core. Software/dummy rendering differs from Pi KMSDRM; those comparisons
did not justify changing the physically working presentation. Early harness runs had
missing logger flags, dummy-device channel/sample suppression and an incompatible
recording-device combination. They are retained and excluded from valid audio evidence.
The accepted harness uses direct WAV output, fixed cycles, isolated preferences and
checks actual non-silent sample duration. Warp is disabled. No runtime/network private
state or owner credentials are part of the benchmark.

For the owner's exact program, each comparison emulated 60 million cycles and generated
60.896 seconds of audio. Console mode excludes host renderer cost; elapsed wall times
were 61.22–61.25 seconds. These are one bounded reference run per configuration, not a
statistical Pi benchmark or complete interactive gameplay qualification:

| Configuration | Native process CPU seconds | Change from installed baseline |
| --- | ---: | ---: |
| Installed -O2 x64sc, reSID resampling | 28.396857 | baseline |
| Portable -O3 x64sc, reSID resampling | 22.442322 | 21.0% less CPU |
| Portable -O3 x64sc, reSID interpolation | 17.907009 | 36.9% less CPU |
| Portable -O3 x64, reSID resampling | 12.292922 | 56.7% less CPU |

The first two generated identical audio hashes. Interpolation and x64 produced different
hashes; no bit-identical sound/compatibility claim is made for them. The evidence points
to the available single-thread emulation budget, with meaningful compiler/core/SID costs.
It does not establish an exact percentage attribution on the physical Pi or exclude all
GPU/display overhead there.

**Chosen candidate:** retain x64sc and the existing rendering/input/lifecycle path;
build VICE with portable -O3 plus existing Debian hardening; seed `SidResidSampling=1`
for C64/C64SC only. Preserve reSID, SID filters, 48 kHz/default rate behavior, true-drive
and VIC-II accuracy resources, PAL/NTSC geometry, VSync and user preference ownership.
This gives substantial measured headroom without substituting the less cycle-accurate
core. Interpolation trades the more expensive resampling/anti-aliasing method for lower
cost; high-frequency spectral differences and SID readback-sensitive software need
qualification. It does not disable the analog SID filter or select FastSID.

The default applies to the C64 profiles uniformly; no scattered Pi-model detection is
introduced. A faster machine's user may select/save resampling in VICE. Other profiles
retain their previous defaults and require their own functional/performance checks.
The Pi 3 hardware policy is unchanged. **Reliable Pi real time is still UNTESTED for the
new candidate until the owner runs the exact-hash procedure.**

## Objective qualification

A separate bounded VICE telemetry patch reports raw wall-window emulation speed and
emulated FPS about every five seconds, at most 120 times per process, through the
existing private diagnostics switch. It stays independent of VICE's sync-reset metric
initialization, which can otherwise repeatedly initialize a slow run to 100%.
No paths, secrets or device identity are included in those records. Warp transitions
and cycle-counter reset restart the measurement window; pause/menu intervals must be
excluded explicitly by the observer. Existing terminal supervision is unchanged.

For a steady representative interval: collect at least 12 consecutive non-warp samples
covering at least 60 seconds after loading/warm-up. Require weighted speed 98–102%, no
five-second sample below 95%, correct audible pitch/tempo, appropriate visual pace and
no sustained slowdown. PAL/NTSC emulated FPS should agree with its video standard;
physical display-refresh FPS is a different measure. Repeat ordinary software and the
demanding external reference, then F10/Quit and repeated launch/input regressions.
`tools/vice_performance.py` validates selected samples and exports only numeric fields.
A metric PASS alone is not physical qualification or proof of correct software behavior.

## Owner identity

Literal `owner` entered fresh-image account creation in commit `1876b9c` during runtime
activation. It was not a historical account/recovery dependency. The fixed UID 1001,
separate home, authenticated sudo and policy contract remain, with username `pcbm` and
home `/home/pcbm`. SSH, Samba, first-boot guidance, readiness checks, status/tests and
manuals follow that identity. Role names, setup step `owner`, `setup-owner` request and
Advanced owner-administration actions keep their descriptive/API meaning. Existing
images/recovery evidence are not renamed or migrated. Console/content remain `pi`.
