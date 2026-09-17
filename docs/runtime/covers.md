# Machine-launch covers

Source continuation, 2026-09-17: [run2 evidence and defensive corrections](../qualification/poc4-run2-source-review-2026-09-17.md).
Physical causes remain unconfirmed. New source delegates Cover plus VICE to Product's
`engineering.py run-with-cover` owner: pre-Cover baseline, same-group bounded child,
structured telemetry, restoration/readback before VICE and after return. No frozen
candidate changed. Renderer keeps 0.75s intended presentation and desktop aspect fit;
held keys no longer skip decoration. Native/physical validation remains pending.
The following earlier account is historical, not the current source contract.

Physical follow-up, 2026-09-17: Covers are installed in frozen POC4 attempt #3, but
the owner did **not** see the Cover and reported dead keyboard/VT after VICE Quit.
[Investigation](../qualification/poc4-regression-investigation-2026-09-17.md) records
the exact evidence and UNKNOWN cause/relationship. No runtime correction selected;
existing-card evidence is needed. The source/build-era account below is preserved and
does not establish a physical Cover or cleanup pass.

Project CBM's **cover** is its existing machine-specific launch artwork. It is
separate from the deferred power-on boot splash/presentation work.

## Status and scope

Source implementation completed after the POC4 attempt #2 image was frozen.
**Attempt #2 does not contain this implementation or the cover assets.** Its lock,
packages, image and checkpoint remain unchanged. A future authorized build needs a
new Menu version/tag/package, integration identity, frozen lock and output hashes.
Do not reuse `v1.1.0_poc4` or modify a finished image to add covers.

The owner identified the existing `project-cbm-menu/covers/pcbmcover-*.jpg` images as
“my cover/splash images” and authorized preserving that experience. The seven exact
machine JPEGs are unchanged. [Asset manifest](../../../project-cbm-menu/docs/cover-artwork.json)
records source revision, sizes, hashes and evidence limits. This permits the requested
private engineering preparation; it does not establish independent clearance of every
embedded third-party photograph, logo or font for public redistribution. Review that
evidence before a public release. Generic numbered covers and historical source-art
archives are not installed. No historical evidence was changed or copied into Git.

## One mapping, one transition

The existing validated [profile registry](../../runtime/data/profiles.json) is the
only profile-to-cover mapping:

| Profiles | Existing cover identity |
| --- | --- |
| x64, x64sc, xscpu64, x64dtv | c64 |
| x128, x128-80col | c128 |
| xcbm2 | cbm2 |
| xcbm5x0 | cbm5 |
| xvic | vic20 |
| xplus4 | plus4 |
| xpet | pet |

`pcbm-run-vice` validates the selected profile/media, calls `pcbm-cover --profile`,
waits for it to exit, then launches VICE. RUN, explicit machine launches and CONTENT
therefore use the profile actually being launched. A content-forced C64 profile uses
the C64 cover even if the user's default is VIC-20. The old dialog-library prelaunch
call was removed to avoid showing a cover twice. Existing direct `pcbm-cover c64`
identity syntax remains compatible; no duplicate mapping or random wrong-machine
fallback is introduced. MACHINES' existing selection/navigation semantics stay intact.

## Display mechanism

The historical helper used fbset, ImageMagick conversion and fbi with a temporary
framebuffer image. The new small Python-standard-library helper binds the SDL2 and
SDL2_image libraries already present for VICE. It initializes video only, creates a
fullscreen-desktop window at the current display mode and fits the existing artwork
on black at approximately half the screen height without stretching it.

[SDL fullscreen-desktop](https://wiki.libsdl.org/SDL2/SDL_SetWindowFullscreen)
uses the desktop mode instead of requesting a legacy physical resolution. SDL owns
its window/renderer/texture, all destroyed before [SDL shutdown](https://wiki.libsdl.org/SDL2/SDL_Quit).
This fits the current Raspberry Pi OS KMS display path, described in the
[Raspberry Pi display configuration](https://www.raspberrypi.com/documentation/computers/config_txt.html).
Actual driver handoff still requires a physical test; the APIs alone do not prove it.

The cover lasts 0.75 seconds; any key can skip it. The launcher limits the entire
process to two seconds plus a 0.5-second termination grace period and waits/reaps it
before VICE. Missing asset/library/display, decoder/renderer failure or timeout proceeds
to VICE. It runs only unprivileged on tty1. It uses no sudo, framebuffer writes, temporary
image, VT switch, external resolution command or background renderer. SDL cleanup runs
on ordinary failure and handled termination; a forced kill relies on process/driver
resource reclamation and must be qualified on the Pi. Existing launcher terminal cleanup
remains. VICE geometry, fullscreen resources, audio, preferences and F10 are unchanged.

Debian packaging lists the seven filenames explicitly and declares SDL2/SDL2_image.
The seven JPEGs total 1,180,157 bytes. Those libraries already exist in the frozen attempt #2 closure; no desktop, ImageMagick,
fbi, new Python framework or image-generation tool is added. No new package was built.

## Validation and limits

142 product tests, 60 Menu tests and the existing launcher checker pass. Cover fixtures cover mapping,
exact artwork hashes/package paths, default/explicit/content-selected profile, missing
artwork, failed renderer, rejection before rendering, return status/F10, unchanged user
preference, single transition ownership, geometry fit and SDL resource cleanup.

Native Debian arm64 staging ran the real SDL2/SDL2_image libraries as UID 1000 with the
SDL dummy video driver. Two sequential real JPEG presentations passed: C64 0.792 s,
VIC-20 0.779 s. SDL video was uninitialized afterward. An actual GNU timeout terminated
a TERM-ignoring child in 2.512 s. These are VM/headless observations, not Pi performance
or evidence of visible artwork, DRM handoff, keyboard/VT behavior or VICE startup.
The initial measurement wrapper was unavailable (`/usr/bin/time`); the test was rerun
without installing anything, using monotonic elapsed time. Peak memory was not measured.

Evidence: configured workspace `qualification/covers-source-2026-09-16`.
Source recovery: `archive/covers-source-2026-09-16`, exact refs and offline bundle restore.
The earlier attempt #2 checkpoint is independently preserved and referenced, not edited.

## Next gate

Review the source correction and authorize a new frozen package/input/build attempt
if covers are required in the next physical candidate. Then run the
[cover qualification addendum](../qualification/covers-next-candidate.md) alongside the
full POC4 Pi 3B procedure, bound to that new candidate's hashes. No new image, physical
test, additional Pi model, boot optimization or publication is part of this source follow-up.
