# VICE in Project CBM

[Documentation index](../README.md) · [User basics](user-guide.md#run-and-vice-basics) · [Build Your Own](build-your-own.md)

VICE emulates the Commodore machines; Project CBM supplies the appliance around it.
The emulator owns CPU/chip behavior, media handling, joystick/key mappings and saved
emulator preferences. Menu chooses a validated machine profile and launches through
one shared transition path. Product owns the machine registry, initial resource seed,
package/build identity and qualification policy.

## Source and package construction

The selected upstream version is **VICE 3.10**, packaged as **3.10-1+pcbm4**. Its source archive is `vice-3.10.tar.gz`
from `https://downloads.sourceforge.net/project/vice-emu/releases/vice-3.10.tar.gz`.
The retained source SHA-256 is
`8e5bac18cbcb9f192380ad3ef881f8790f5b75c41d7b3da65d831985d864d6d1`.
`build/inputs-poc.json` records the selection; each release lock retains the actual source,
Debian recipe, patches, corresponding source package, build record and binary hash.
The current package recipe is `build/packages/vice/debian`; the [package walkthrough](build-your-own.md#vice) gives its build commands. A version label alone does
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

## Profiles and media

| Display name | Profile ID | VICE backend | Notes |
| --- | --- | --- | --- |
| Commodore 64 (fast) | `x64` | `x64` | Fast C64 emulation |
| Commodore 64 | `x64sc` | `x64sc` | Cycle-accurate C64; recommended for games and demos |
| SuperCPU 64 | `xscpu64` | `xscpu64` | C64 with CMD SuperCPU |
| Commodore 64 DTV | `x64dtv` | `x64dtv` | C64 Direct-to-TV hardware |
| Commodore 128 (40 column) | `x128` | `x128` | 40-column VIC-II display |
| Commodore 128 (80 column) | `x128-80col` | `x128` | Adds -80col for VDC |
| Commodore CBM-II | `xcbm2` | `xcbm2` | CBM-II business computer |
| Commodore CBM-II 5x0 | `xcbm5x0` | `xcbm5x0` | CBM-II 5x0 with VIC-II video |
| Commodore VIC-20 | `xvic` | `xvic` | VIC-20 home computer |
| Commodore Plus/4 | `xplus4` | `xplus4` | Plus/4 family with TED video |
| Commodore PET | `xpet` | `xpet` | PET business computer |

All these profiles use the same shared launcher, which passes an ordinary selected file
as `-autostart`. It does not guarantee every format works on every computer. Typical
C64-family content is PRG/P00, disk/tape/cartridge software; C128 needs suitable C128
software and drive/display settings; VIC-20 often requires the right RAM expansion;
Plus/4, PET and CBM-II require their own machine-compatible programs/media. The
[content format table](content.md#launching-files) is the exact browse/import reference.
ROM/BIN/REU resources are not automatic programs; SID autostart is explicitly refused.
MUS recognition is not a supported standalone music-player workflow.

The package also installs `vsid`, `c1541`, `cartconv` and `petcat`. These upstream tools
are not additional Project CBM Menu profiles. No PAL/NTSC selector exists in MACHINES;
VICE's saved machine/model resources control the standard. The initial resource template
does not force one global PAL/NTSC model across all computers.

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
expensive resampling seed inherited from compiled defaults. The optimization/interpolation combination reduced CPU cost in a native comparison,
but still did not bring the demanding physical reference to real time on Pi 3 B+.
It is not evidence of sufficient Pi 3 performance. High-frequency sampling and
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
Changing the emulator core does not automatically change SDL's console behavior. Primary boot presentation is separate from the machine Cover transition; see [startup](boot.md).

## Preferences and performance qualification

The initial template is `/usr/share/project-cbm/vice-defaults.ini`. The user configuration
is `/home/pcbm/.config/vice/sdl-vicerc`; the installer creates it only if absent. Save
preferences through VICE when you want them retained. User resources, compiled defaults,
Product seeds and launch flags are separate sources of effective settings; support
reports should distinguish them. Restoring old saved resources can also restore old
performance choices, so compare them explicitly during a fresh-image regression.

Pi 4-class hardware is the Project CBM 1.1 performance floor. Functionally launching a profile is
not enough: representative games, demos, disk software, BASIC and music must sustain
real-time emulation on the minimum qualified model. The owner-supplied demanding
reference is private test material, not a bundled game. Compiler/core/resource decisions
must follow bounded evidence and retain the highest fidelity that satisfies real time.
Physical Pi 3 B+ testing of a demanding owner-supplied C64 demo showed slow graphics
and music while the main emulation thread saturated about one core, without reported
throttling or memory pressure. The same reference ran normally on Pi 4 B with numeric
speed evidence near real time. This supports Pi 4-class as the 1.1 minimum; it does not
prove every workload or every newer Pi is qualified. Pi 3/Zero-class machines remain
experimental, unsupported targets even if they boot. The normal C64 core is x64sc;
there is no hardware-tier switch that silently substitutes x64.

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
For engineering results and current physical status, follow [current state](../../CURRENT-STATE.md).
The measurable window uses 12 consecutive complete non-warp samples spanning at least
60 seconds, weighted speed 98–102% and no complete sample below 95%. Physical sound/pace
and launch/quit behavior are also required; emulated FPS is not a display-refresh count.

## Application-specific serial and disk options

CCGMS launched from its documented library folder selects the normal `x64sc` profile
and adds a temporary SwiftLink interface: ACIA enabled, mode 1, base `$DE00`, NMI,
VICE RS232 device 0, IP232 to the configured local TCPser port (initially 25232).
The installed VICE 3.10 option for that device selector is `-myaciadev 0`.
Project CBM reads the same typed `/etc/project-cbm/modem.json` used by `pcbm-modem`;
it does not start a network service merely by launching content. CCGMS users select
Swift / Turbo DE and 2400 baud initially. See the [connection walkthrough](networking.md#bbs--modem).
These arguments do not rewrite the owner's VICE resources. Do not save temporary
application-specific emulator settings as global defaults unless that is intentional.

G71 content uses a 1571 drive (`-drive8type 1571`) for that invocation and is restricted
to C64/C128 profiles. Other media retain their existing launch behavior. Filename and
directory dots do not by themselves hide supported content; known host metadata is
still excluded. No VICE package rebuild is needed for these Product/Menu launch changes.
