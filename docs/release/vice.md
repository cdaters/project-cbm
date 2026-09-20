# VICE in Project CBM

VICE emulates the Commodore machines; Project CBM supplies the appliance around it.
The emulator owns CPU/chip behavior, media handling, joystick/key mappings and saved
emulator preferences. Menu chooses a validated machine profile and launches through
one shared transition path. Product owns the machine registry, initial resource seed,
package/build identity and qualification policy.

## Source and package construction

The selected upstream version is **VICE 3.10**. Its source archive is `vice-3.10.tar.gz`
from `https://downloads.sourceforge.net/project/vice-emu/releases/vice-3.10.tar.gz`.
The retained source SHA-256 is
`8e5bac18cbcb9f192380ad3ef881f8790f5b75c41d7b3da65d831985d864d6d1`.
`build/inputs-poc.json` records the selection; each release lock retains the actual source,
Debian recipe, patches, corresponding source package, build record and binary hash.
The current package recipe is `build/packages/vice/debian`. A version label alone does
not identify a Project CBM build: check the Debian revision and installed image identity.

Build dependencies are declared in that recipe's `control`: debhelper, SDL2/SDL2_image,
DRM/evdev, ALSA, PNG/zlib, curl, readline/editline development libraries, flex, bison,
texinfo, pkg-config, dos2unix and xa65, plus the native compiler/toolchain. The final
image contains runtime libraries, not this whole development environment.

`debian/rules` uses an out-of-source `debian/build` directory and these configure options:

```text
--enable-sdl2ui --with-alsa --with-sdlsound --without-pulse
--disable-arch --enable-x64 --disable-html-docs
```

The package targets portable ARMv8-A with generic CPU tuning. `--disable-arch` prevents
upstream host-native architecture selection from making a package specific to the
builder's CPU. The performance correction selects `-O3` for both C and C++ while retaining
Debian hardening, stack protection, PIE/link protections and the portable instruction
baseline. It does not enable fast-math, use the Mac CPU as an instruction target, or
assume a Pi 5. The nested reSID build must receive the same intended optimization flags;
checking only the top-level Makefile is insufficient.

Patches are listed in `debian/patches/series`. The presentation patch emits a few
opt-in numeric geometry/backend records; the performance patch emits bounded speed/FPS
records independent of VICE's synchronization-reset smoothing. These diagnostics do not
change emulated timing or graphics. They contain no passwords, content paths or device
identities. The package also builds the unprivileged read-only `drm-state` helper.
No renderer, framebuffer-mode or keyboard-ownership workaround is introduced by telemetry.

`dpkg-buildpackage -us -uc -sa` builds the binary and corresponding source records after
the original tarball and Debian recipe are staged. The factory retains `.dsc`, source
archives, `.deb`, `.buildinfo`, `.changes` and logs. Use the exact source/patch/recipe
hashes from the frozen lock when reproducing a version. See [Build Your Own](build-your-own.md)
for the full distinction between source packages, a derivative image and frozen replay.

## Executables and profiles

| VICE executable | Registered use |
| --- | --- |
| `x64sc` | Cycle-accurate C64 profile |
| `x64` | Alternate fast C64 core, separately available for comparison/use |
| `xscpu64` | C64 with SuperCPU |
| `x64dtv` | C64 DTV |
| `x128` | C128; the 80-column profile adds the validated `-80col` option |
| `xcbm2`, `xcbm5x0` | The corresponding CBM-II families |
| `xvic` | VIC-20 |
| `xplus4` | Plus/4 |
| `xpet` | PET |
| `vsid` | Upstream SID-oriented executable; its presence does not establish a supported appliance PSID/RSID workflow |
| `c1541`, `cartconv`, `petcat` | Upstream media/conversion tools, not replacement appliance launchers |

The authoritative registry is Product `runtime/data/profiles.json`, installed under
`/usr/share/project-cbm/runtime/data/profiles.json`. Its schema and runtime validator
constrain executable names/options and map each profile to its Cover. A Menu label is
not an arbitrary shell command. Adding a profile requires changing the registry and
its validation contract together where the new identifier/options are not already
admitted. The C128's two video chips are deliberately distinct; do not apply a single
C64 geometry override to every machine.

## Display and sound path

VICE is built with SDL2 UI. On the Pi console SDL2 selects KMSDRM and supplies the
OpenGL renderer. DRM/GBM and Mesa libraries complete that graphics path even when they
are loaded dynamically rather than appearing as direct ELF dependencies. A native
headless test using SDL's dummy/software backend is useful for logic/relative CPU tests,
but it cannot reproduce the Pi GPU, display mode, keyboard ownership or scanout behavior.

The initial seed in `tools/vice_presentation.py` sets true aspect mode, fullscreen and
fullscreen mode 0 separately for each chip. VICE calculates PAL/NTSC pixel geometry and
retains the complete canvas; unused side areas are intentional. The shared launcher does
not impose per-launch pixel dimensions, stretch the output or write saved resources.
The Pi display mode and VICE's internal render size are different settings. Their CPU/
GPU costs need measurement; changing one to conceal cropping is not a performance fix.

The launcher selects VICE's SDL sound device and `SDL_AUDIODRIVER=alsa`. VICE's sound
engine synthesizes the emulated SID, SDL delivers samples, and ALSA accesses the device.
The corrected C64/C64SC seed selects reSID interpolation (`SidResidSampling=1`),
retaining the SID engine, filters and sample-rate behavior. This replaces the more
expensive resampling seed inherited from compiled defaults. The actual owner reference
used 36.9% less native CPU with the combined portable -O3/interpolation correction;
physical Pi performance still requires qualification. High-frequency sampling and
SID readback-sensitive behavior can differ; users may save resampling on faster hardware.
Other profiles keep their existing resources. The exact sound model/resources remain
emulator preferences. Audio thread CPU alone does not measure
SID emulation cost, which is principally on the main emulator thread.

## Cover, emulator and return

Menu invokes `pcbm-run-vice`. Product's engineering supervisor captures terminal state
before the Cover, admits the foreground tty safely, bounds/supervises/reaps the renderer,
restores/verifies the terminal, and runs the requested VICE executable unprivileged.
The normal invocation includes `-sounddev sdl -menukey 291`; the engineering path adds
fixed non-colour logging. F10 opens VICE's menu; Quit returns through the supervisor to
a responsive Menu. A missing/failed Cover allows VICE to continue after safe cleanup.
Do not add a second launcher for a performance profile.

Linux getty/login/PAM owns the original console session. The current SDL/KMS active-VICE
VT shortcut limitation is documented; leaving VICE restores working Menu VT switching.
Changing the emulator core does not automatically change SDL's console behavior. The
performance milestone preserves this lifecycle and does not implement quiet/fast boot.

## Preferences and performance qualification

The initial template is `/usr/share/project-cbm/vice-defaults.ini`. The user configuration
is `/home/pi/.config/vice/sdl-vicerc`; the installer creates it only if absent. Save
preferences through VICE when you want them retained. User resources, compiled defaults,
Product seeds and launch flags are separate sources of effective settings; support
reports should distinguish them. Restoring old saved resources can also restore old
performance choices, so compare them explicitly during a fresh-image regression.

Pi 4-class hardware is the Project CBM 1.1 performance floor. Functionally launching a profile is
not enough: representative games, demos, disk software, BASIC and music must sustain
real-time emulation on the minimum qualified model. The owner-supplied demanding
reference is private test material, not a bundled game. Compiler/core/resource decisions
must follow bounded evidence and retain the highest fidelity that satisfies real time.
Attempt #8 has an owner Pi 4 B PASS for the demanding reference under x64sc, supported
by 145.219 seconds at weighted 100.002% speed. The final low sample was quitting,
confirmed by the owner. The saved configuration is retained with that result. No
host/native result independently qualifies a Pi, and every new image still needs its
own regression. The normal C64 core remains x64sc; no Pi 3 tuning or core tier is selected.

Engineering `CBM_PERFORMANCE` records contain measured wall-window speed percentage,
emulated FPS and warp state. They are capped at 120 records, about five seconds apart,
and enabled only with the existing private diagnostics switch. Unlike status smoothing,
the measurement does not reset to 100% merely because synchronization falls behind.
Exclude setup/loading, menus, pauses and warp intervals from qualification. FPS describes
emulated frames, not necessarily every physical display refresh; PAL and NTSC targets
differ. The physical procedure couples these numbers with correct audio pitch/tempo,
visual speed, clocks/throttling and repeated launch/quit behavior.

The generated benchmark in `tools/benchmark_vice.py` uses original three-voice/audio
and CPU/screen activity, a fixed cycle budget and validated WAV output. Its native
software renderer is explicitly different from KMSDRM. VICE's dummy sound backend can
skip meaningful channel/sample generation, so a zero-length or silent output invalidates
an audio comparison. Invalid harness attempts are retained as failures, not timed passes.
For complete results and the final selected release settings, follow the current build
report and its exact-hash physical procedure from [current state](../../CURRENT-STATE.md).
