# POC2 Pi 3B results and display-geometry review

Recorded/researched 2026-09-15. **Owner review; no runtime change or POC3 build.**
The [formal physical record](poc2-pi3b.json) contains the complete PASS/FAIL/UNTESTED
matrix. The [hash-bound procedure](poc2-pi3b-smoke-test.md) identifies the tested
candidate. This follow-up supersedes physical-pending statements in the completed
[POC2 build checkpoint](../build/private-poc2.md), without changing that checkpoint.

## Result and evidence limits

The owner reports successful Pi 3B boot, automatic Menu/rendering/keyboard, both
VT switches and diagnostic-shell keyboard, RUN/x64sc launch, C64 rendering and
observed display stability, VICE keyboard, F10 menu, Quit and clean responsive
return to CBM. Smoke PRG, original SID tones, video/input program and D64 smoke
loading passed. A normal reboot returned automatically to Menu.

**Correct aspect-ratio preservation failed:** C64 output stretched horizontally
across the widescreen display, also visible in the video/input program. This is
not a rendering or stability failure. Joystick is UNTESTED because none was
available. Basic reboot/startup persistence does not establish saved-configuration
persistence. SID tones do not establish PSID/RSID, stereo or emulation fidelity.

POC2 resolves POC1's observed launch/display and console-recovery failure. POC2
changed graphics dependencies, getty/login/PAM sessions and launcher/diagnostics;
therefore **POC1's precise cause remains unconfirmed**. Its record is unchanged.

Evidence is the owner's report, not an assistant-observed test or an instrumented
measurement. Test date/time, board revision, monitor/model/mode/scaling, card,
power supply and detailed timings were not supplied. No physical photographs or
card diagnostic files were available in the retained qualification folders at
review. Existing `qualification/poc2/media-reference` pictures are reference
software-renderer checks, not photographs from this physical test. When operator
photos/reports arrive, retain original bytes externally, record SHA-256/relative
locator/caption and add an evidence supplement. Do not rewrite image/lock/build
records or infer unreported passes from the procedure's requested steps.

## Exact inspected inputs

Locators below are relative to configured bulk storage, currently
`/Volumes/TheBench/ProjectCBM-Work`; no historical artifact was mounted writable.

| Input | Identity |
| --- | --- |
| Raw POC2 | `artifacts/private-poc2/2026-09-16-project-cbm-1.1.0-poc.2-lite-private-poc.img`; SHA-256 `ef221dc09ea65d3976f88e65cde8f153a9c32989be09c6b35d545b111ccb7467` |
| Frozen input lock | `inputs/frozen-poc2/release-lock.json`; SHA-256 `bc1c6e16c32d6285973933b8d50371899bc18e5407dd654c9a14d1187eb194ac` |
| VICE package | `project-cbm-vice 3.10-1+pcbm2 arm64`; SHA-256 `ea941c6d7e2e7c61366bd8b6b45bbf9a1dc538c013e336f6c96ae94265535ab0` |
| VICE source | `inputs/vice/vice-3.10.tar.gz`; SHA-256 `8e5bac18cbcb9f192380ad3ef881f8790f5b75c41d7b3da65d831985d864d6d1`; no lock-declared patches |
| Menu source/package | `v1.1.0_poc2`, peeled `897cee7c792b11bfed80168a576f263340f5f57d`; package SHA-256 `e29bc3598f3be0869f79184250f88a03f4c59f1304a20a428223bac58c97bd11` |
| Product integration | `2b894ad187f0b603d2e0c9965aba242073e2cb90` |
| Historical v1.0 released raw image | `archive/audit-2026-09-14/workspace/assets/pcbm-v1.0.0-rpi3-5.img`; SHA-256 `168a3026eca2bc328e03e47dfbb0cbe17740180504ad7858496df84982e89849` |

Read-only ext4 inspection rehashed POC2 and read its installed identity, launcher,
engineering observer, empty VICE configuration directory and package database.
No VICE process was executed, guest started, package built or image altered.
The package/source/lock and image binary checks are retained with this review's
external evidence. Historical configuration was compared with the preserved
read-only POC1/v1 comparison, then re-read from the released v1 image.

## Frozen settings versus unknown live settings

The image has no `/home/pi/.config/vice/sdl-vicerc`, `/etc/vice/sdl-vicerc` or
`/usr/share/vice/sdl-vicerc`. Its VICE user-config directory is empty. The packaged
shared launcher sets HOME/XDG paths, `SDL_AUDIODRIVER=alsa`, `-sounddev sdl` and
`-menukey 291`; it supplies no geometry or fullscreen arguments. The engineering
wrapper passes an allowlisted environment, adds logging options, and supplies no
renderer/aspect override. `/etc/environment` is empty.

Exact VICE 3.10 source establishes these **factory defaults**, not a captured
resource dump from the tested card:

| Resource | Factory value / meaning |
| --- | --- |
| `<chip>AspectMode` | `2`, true machine pixel-aspect correction |
| `<chip>AspectRatio` | `1.0`, custom pixel multiplier; unused in true mode |
| `<chip>Fullscreen` | `0`, windowed request |
| `<chip>FullscreenMode` | `0`, desktop resolution when fullscreen is enabled |
| `Window0Width/Height` | `0`, let VICE derive initial dimensions |
| `SDL2Backend` | empty, automatic renderer selection |
| C64 `MachineVideoStandard` | PAL factory default; actual live selection uncollected |

The frozen image uses SDL2 `2.32.4+dfsg-1`, Mesa GLX
`26.2.2-1~bpo13+0~rpt1`, full KMS and no desktop. VICE build flags are SDL2/ALSA,
SDLSound, no PulseAudio, generic architecture and x64 enabled, as pinned in the
lock. The actual physical video driver, renderer, connector mode and live resource
values require runtime evidence; KMSDRM/OpenGL are expected, not newly measured.

## Historical comparison

The released v1.0 `/home/pi/.config/vice/sdl-vicerc` has SHA-256
`7c5c3fe2dbb0fdd7c660925c180ad8b613b014567718b231f9b469e9f70c48a1`.
It explicitly sets window sizes/positions and bilinear filtering:

- C64/C64SC/SCPU64/C64DTV/CBM-II/CBM-II-5x0/PET: 720×576, position −40/−48.
- C128/VIC20/PLUS4: 800×600, position −80/−60.
- Per-chip `GLFilter=1`; F10 key 291 and SDL sound.

It has **no explicit aspect-mode, fullscreen or renderer override**. POC2 omitted
those window/filter settings, not a historical explicit aspect flag. Window
positions and chosen sizes are not a portable native-aspect policy. Do not copy
720×576, negative positions or an arbitrary 4:3 multiplier as the fix. The old
OpenGL selection is a retained log fact, not a controlled same-display Pi 3B
geometry measurement. Historical notes are context; installed bytes take precedence.

## Leading explanations, ranked

1. **Implicit window-to-physical-mode selection plus display scaling — leading
   engineering hypothesis.** POC2 makes a windowed request without a deliberate
   desktop-resolution fullscreen policy. SDL 2.32.4 KMSDRM's
   `KMSDRM_GetModeToSet` selects a closest connector mode from window dimensions
   for a non-fullscreen window. A lower/non-native physical mode stretched by a
   widescreen display could defeat correct geometry inside the framebuffer.
   Omitted historical window sizes can affect this selection. Actual mode/scaler
   state is missing, so this is not a confirmed cause or proof of a Pi kernel bug.
2. **Runtime resource/viewport or renderer mismatch.** True aspect is the compiled
   default, but there is no tested-card resource dump, renderer log or viewport
   measurement. A live override, initialization/resize interaction or renderer
   problem could produce different results. Do not blame operator changes; none
   were reported. Merely adding `AspectMode=2` restates the default and cannot be
   claimed to fix the defect.
3. **Display-side scaling independent of VICE's requested mode.** Monitor settings
   and input timing were not supplied. Document them before changing kernels,
   firmware, HDMI boot configuration or renderer packages.

The confirmed product defect is absence of demonstrated, consistently preserved
geometry. Offline inspection narrows the likely layer but cannot settle the
physical output chain. Missing GL is no longer a leading explanation for this
specific defect: POC2 successfully renders and exits.

## Supported strategy and ownership

Use VICE's per-video-chip **true aspect mode (`2`)**, together with explicit
**fullscreen at the desktop/current display resolution (mode `0`)**. Retain the
normal KMS/HDMI-selected modern display mode; fit the emulated canvas inside it.
Allow black sidebars or top/bottom bars, preserve the full intended visible canvas,
and avoid stretch-to-fill or overscan cropping. Do not promise that every canvas
is exactly 4:3. Do not force integer scaling/filter changes as part of this fix.

VICE's SDL2 implementation multiplies canvas width by the machine's pixel-aspect
value and calls `SDL_RenderSetLogicalSize`. SDL fits/centers a differing logical
aspect inside its rendering output by default. VICE fullscreen mode 0 requests
`SDL_WINDOW_FULLSCREEN_DESKTOP`; custom fullscreen mode 1 switches modes.
These are supported mechanisms, but their effect on this Pi/display still needs
measurement. Ensure desktop resolution means the expected connector mode after
startup, not a stale mode already selected by a window.

**Recommended ownership:** product-owned, generated initial per-machine VICE
configuration, initialized without overwriting existing user preferences. The
shared Menu launcher remains the common execution path. Verify VICE config search
and precedence; do not use `-config` to replace user settings on every launch or
repeat policy separately in RUN and CONTENT. Explicit per-chip launch arguments
are useful for controlled comparisons, but permanent unconditional arguments would
override saved user choices. Keep the package's upstream defaults unpatched unless
an actual upstream defect is demonstrated. If first-use configuration is chosen,
make its creation retry-safe and keep profile sections isolated.

## Machines and PAL/NTSC

The policy is shared; resource names and machine geometry differ:

| Menu profile | VICE resource prefix / proposed defaults |
| --- | --- |
| x64, x64sc, xscpu64, x64dtv, xcbm5x0 | `VICIIAspectMode=2`, `VICIIFullscreen=1`, `VICIIFullscreenMode=0` |
| x128, x128-80col | Both `VICII` and `VDC` resources; verify selected/alternate canvas and transitions |
| xvic | `VICAspectMode=2`, `VICFullscreen=1`, `VICFullscreenMode=0` |
| xplus4 | `TEDAspectMode=2`, `TEDFullscreen=1`, `TEDFullscreenMode=0` |
| xcbm2, xpet | `CrtcAspectMode=2`, `CrtcFullscreen=1`, `CrtcFullscreenMode=0` |

This table is a proposed configuration contract, **not implemented behavior or
qualification**. Only x64sc was physically exercised. All listed profiles share
the SDL2 presentation risk; other profiles are not marked failed. VSID/PSID/RSID
are outside this smoke result and need separate treatment if exposed later.

PAL and NTSC change VICE's machine-provided pixel-aspect values. For example,
x64sc's source uses approximately 0.936508 for PAL and 0.75 for NTSC; these are
horizontal pixel multipliers, not display ratios. VIC, TED and VDC have their own
values. CRTC assumes square pixels with render-mode correction. Border choice,
canvas dimensions and doubling also matter. Let VICE calculate these values;
do not hard-code them in CBM or pass `1.3333` as a universal pixel aspect.

## Recommended next candidate: narrow POC3 before other models

Choose **A: correct and validate geometry on Pi 3B before expanding hardware
qualification**. The baseline now exercises core emulation successfully, so
repeating the known geometry defect on 3A+/3B+ would add little useful evidence.
POC2 remains useful immutable evidence; it is not full Pi 3B release qualification.

Proposed bounded scope, requiring new owner authorization:

1. Establish effective resources, SDL renderer/video driver, logical/output sizes
   and active connector mode using a disposable reference runtime or approved
   read-only collection from the tested card. Keep geometry diagnostics bounded;
   omit EDID serials/identity. Do not modify frozen POC2 to try fixes.
2. Implement only the explicit native-aspect/desktop-fullscreen defaults and the
   minimum initialization/launcher integration needed. Retain graphics closure,
   session, F10, engineering VT/logs, service policy and existing media. No forced
   HDMI resolution, OS upgrade, broad setup work or SSH.
3. Pre-build checks: verify registered resources for every profile (including both
   C128 canvases); PAL/NTSC expectations; generated-config precedence, existing-user
   preservation and repeat-safe initialization; RUN/content consistency; rendering
   into a known widescreen reference output with expected unused margins and no
   cropping. A raw emulated screenshot alone cannot prove final-screen geometry.
   Include launch/failure/return and sudo/service regression checks.
4. If supported defaults do not produce correct reference geometry, stop to gather
   renderer/viewport evidence before patching VICE/SDL/KMS. Do not call an explicit
   restatement of true aspect a demonstrated correction.
5. Freeze a new candidate/lock and hashes through the factory, reuse unchanged
   verified components/media where possible, and perform offline validation. Do
   not mutate either old image or inject undeclared media. Stop with a hash-bound
   Pi 3B procedure; physical testing remains an owner action.
6. On Pi 3B, compare the same widescreen display: record physical mode/scaling and
   photographed geometry, PAL/NTSC x64sc, RUN and normal media paths, F10/return,
   VT and reboot. Review other chip/profile geometry on this same board as a bounded
   presentation check, not full machine compatibility qualification. Joystick only
   if available; otherwise UNTESTED. Expand to 3A+/3B+ after the geometry gate passes.

The existing suite lacks a calibrated physical-aspect target. Start with measured
canvas/margins versus VICE geometry and retained full-screen photos. If a tiny
original geometric pattern is needed, propose/version/hash it as a new declared
input; do not silently revise qualification-media 0.1.0.

## Source references and reproducible inspection

Research date: 2026-09-15. Online documentation describes supported interfaces;
the retained exact source/package is the authority for POC2's implementation.

- [VICE machine resources](https://vice-emu.sourceforge.io/vice_7.html): per-chip
  aspect modes and machine video settings.
- [VICE SDL options](https://vice-emu.sourceforge.io/vice_8.html): fullscreen mode,
  renderer, window dimensions and command-line equivalents.
- Exact `vice-3.10.tar.gz`: `src/video/video-resources.c:277–307,489–508,1099–1145`;
  `src/arch/sdl/video_sdl2.c:377–404,621–668,1006–1025,1056–1145`;
  `src/arch/sdl/menu_video.c:522–544`; `src/viciisc/vicii.c:138–153`;
  `src/vic20/vic.c:88–100`, `src/plus4/ted.c:249–261`,
  `src/vdc/vdc.c:78–92`, `src/crtc/crtc.c:324–338`.
- [SDL2 logical sizing](https://wiki.libsdl.org/SDL2/SDL_RenderSetLogicalSize) and
  [logical scaling policy](https://wiki.libsdl.org/SDL2/SDL_HINT_RENDER_LOGICAL_SIZE_MODE).
- [SDL2 fullscreen API](https://wiki.libsdl.org/SDL2/SDL_SetWindowFullscreen).
- [SDL release-2.32.4 KMSDRM source](https://raw.githubusercontent.com/libsdl-org/SDL/release-2.32.4/src/video/kmsdrm/SDL_kmsdrmvideo.c):
  `KMSDRM_GetClosestDisplayMode`, `KMSDRM_GetModeToSet`, `KMSDRM_CreateSurfaces`.
  This is upstream version-matched source; no claim that every Debian patch was
  audited or that this identifies the actual physical mode.

External follow-up: `qualification/poc2-pi3b-owner-report-2026-09-15` contains the
small read-only inspector/results and verification record. Source bundle/refs and
offline restoration are in `archive/poc2-pi3b-review-2026-09-15`. These are additive;
sealed POC1/POC2 build checkpoints remain unchanged. Same-device retention still
is not an independent encrypted backup. No image rebuild, VM start or push occurred.

## Review validation

Documentation diff/size/privacy checks, strict JSON (including duplicate-key
rejection), 66 local links and unchanged-tag checks in both repositories passed.
The formal matrix records 26 scoped PASS entries, one FAIL and 22 UNTESTED entries;
these counts are record granularity, not 49 independent hardware trials. Frozen
POC1 physical and POC2 build records remain byte-identical. POC2 raw/XZ, lock,
VICE source/package and Menu package checks pass; installed x64sc matches its
package. The 1,677-entry original historical manifest verifies unchanged. No
runtime test or new physical observation was performed in this review.
