# POC3 presentation defaults and engineering evidence

Owner authorized 2026-09-16. Scope: non-stretched VICE presentation, bounded
engineering measurements and a new private candidate. POC1/POC2, their inputs and
physical records remain immutable. No SSH, settings redesign or public release.

## What is known before implementation

[POC2's Pi 3B report](../qualification/poc2-pi3b.json) has working boot/Menu,
launch/rendering/keyboard/audio/media/return/VT/reboot, with geometry FAIL.
[Four retained photographs](../qualification/poc2-pi3b-aspect-analysis.md#photo-supplement--2026-09-16)
corroborate visible output/stretching. Their manifest SHA-256 is
`00d9028d621441a5f18b990835c7d51008c7108d3a30c3f7867f16ece516b05d`.
They do not identify the active mode/renderer or a confirmed cause.

The unmodified POC2 VICE executable was tested in an isolated software reference:
SDL dummy video, software renderer, requested 1280×720 window, PAL and NTSC.
Frame-60 observation showed true aspect mode's different logical geometries:
PAL 719×544 and NTSC 576×494. SDL supplied horizontal margins rather than using
an uncorrected widescreen canvas. This proves the retained implementation can
preserve geometry in that reference environment, not on the physical KMS chain.

POC2 does not seed fullscreen/aspect settings. Compiled defaults are true aspect 2,
fullscreen off, desktop fullscreen mode 0. Historical v1.0 had explicit window
sizes/filtering, not an explicit aspect flag. The leading unconfirmed hypothesis
is implicit windowed KMS mode selection plus downstream scaling. Do not infer an
upstream VICE rendering defect, monitor fault or missing GL from this result.

## Initial policy and configuration ownership

Use true aspect (`2`), fullscreen (`1`), desktop-resolution fullscreen mode (`0`)
for each relevant video chip. Preserve the full canvas and accept **pillarboxing**
(black bars on the sides) or letterboxing (bars above/below). No universal 4:3,
custom pixel multipliers, legacy HDMI modes, crop-to-fill or new filter policy.
VICE supplies machine/standard pixel geometry, including PAL versus NTSC.

| VICE config section / Menu profile | Chip resources |
| --- | --- |
| C64, C64SC, SCPU64, C64DTV, CBM-II-5x0 | VICII |
| C128 / x128 and x128-80col | VICII and VDC |
| VIC20 / xvic | VIC |
| PLUS4 / xplus4 | TED |
| CBM-II / xcbm2, PET / xpet | Crtc |

[Generator](../../tools/vice_presentation.py) is the single source for the initial
INI settings. During image construction the product installs a root-owned reference
at `/usr/share/project-cbm/vice-defaults.ini` and an initial pi-owned
`/home/pi/.config/vice/sdl-vicerc`. Exclusive creation preserves any existing file
or symlink. This runs only before sealing, never at launch or on each boot.

- **Protected build policy:** a new candidate starts with correct per-chip defaults,
  no resolution hacks, no root emulator and the existing safe launch/return contract.
- **Initial defaults:** true aspect, fullscreen, desktop fullscreen mode. They are
  not immutable runtime restrictions on the user.
- **User preferences:** after initialization VICE owns the user file. Its ordinary
  Save settings operation persists choices. Unsaved choices need not survive exit.
  Resetting VICE to upstream factory defaults or deleting the user config deliberately
  returns upstream behavior; CBM does not silently reseed on the next launch.
- **Precedence:** VICE reads the user config; later command-line options override it.
  No geometry arguments, `-default`, or replacement `-config` are added to Menu.
  Existing `-sounddev sdl` and `-menukey 291` remain the POC launch contract.
  `-dumpconfig` captures values when parsed; reference tests place it last.

The user copy is excluded from the system-owned path inventory. First-boot growth,
identity and directory initialization stay unchanged. No Menu package/source change
is required. This candidate does not migrate existing installations in place.

## Engineering diagnostics

The VICE package revision adds a source patch solely for opt-in numeric/video
telemetry. The product's engineering wrapper sets `CBM_PRESENTATION_DIAGNOSTICS=1`.
At presented frames 60, 300 and 900 (at most three records per process), VICE logs:

- active chip, aspect mode/pixel aspect, video standard, fullscreen/mode;
- SDL video driver, renderer name/capability flags/texture limits;
- window, renderer output and logical canvas sizes;
- viewport and scale, window flags, SDL's current display mode/refresh.

Viewport coordinates are SDL logical coordinates; use the reported scale to
interpret physical output margins. SDL's reported mode is not independent proof
of the actual connector timing. If fewer frames render, fewer/no records may exist;
that absence is not proof of a hang. No full configuration dump is retained in the
appliance: it can include user paths and unrelated state.

The same versioned package contains `/usr/libexec/project-cbm-vice/drm-state`, a
small libdrm reader used by the existing snapshots. It opens only `/dev/dri/card0`
through `card15` read-only and queries connector/encoder/CRTC mode state. A CRTC is
the display controller feeding an output. Records contain local connector numbers,
connection status, active mode dimensions/timing and controller dimensions/offsets.
No EDID, serial, machine identity, privileged modesetting, DRM-master acquisition,
root helper, new groups or sudo grant. Root/arbitrary arguments/non-engineering
invocations are refused. Permission or unavailable-mode limitations are reported,
not bypassed. It does not identify a monitor's internal scaling setting.

The observer's existing four-launch rotation, 128 KiB output tail, three bounded
samples, two-second command timeouts and redaction remain. A fresh `pcbm-diagnostics`
on tty2 captures current state plus retained launch evidence. No SSH is enabled.
The VICE patch is opt-in; geometry correction itself uses upstream-supported
resources, not a renderer patch. Corresponding source/license/patch are retained.

## Tests and reference limitations

Host tests cover deterministic per-chip defaults, no forced PAL/NTSC/pixel ratio,
exclusive creation, preservation of existing user/symlink state, no boot/launch
rewrite, diagnostic opt-in and read-only helper restrictions. Existing launcher,
return, bounded log/redaction, graphics/session, service/sudo, media and lock tests
remain required. Image inspection checks exact template/user ownership, diagnostics,
package closure and all existing sealing/session/media constraints.

[Native reference harness](../../tests/reference/poc3-presentation.py) exercises
all 11 profiles and x64sc PAL/NTSC using the compiled package executable and a new
user-config directory per case. It checks actual dumped resources, frame telemetry,
saved preference preservation and CLI precedence. Cycle-limit exit 1 is expected;
initialization failure is not accepted. The SDL dummy desktop is 1024×768, so its
fullscreen tests do not simulate native 16:9 KMS. The separate unchanged-POC2
1280×720 window test validates aspect fitting in a widescreen software output.
Neither test proves physical video/audio/input, actual HDMI timing or Pi performance.

Initial reference attempts lacked a runtime-data path; a reused package build tree
also failed dpkg's generated-README source check. Those attempts are retained as
failed engineering work, not candidate qualification. Final builds use fresh source.
No issue justifies editing old frozen inputs or silently disabling validation.

## Frozen build and stop

Build VICE only using `build/packages/build.sh RECIPE WORKSPACE poc3-final vice-only`.
Reuse unchanged frozen Menu, TCPser, OS closure and qualification media. Commit the
integration recipe, export `git archive --prefix=project-cbm/ COMMIT` to externally
retained `inputs/project-cbm-integration-poc3-final.tar`, then run
`tools/freeze_poc3_inputs.py WORKSPACE RECIPE COMMIT` in Linux. It verifies POC2's
kit, adds new content-addressed objects and writes a distinct POC3 lock. Existing
object hard links must never be written in place. Construct with the same isolated
network-namespace command in [the factory guide](poc2-design.md#rebuild-from-the-retained-kit-only-after-a-new-build-is-authorized),
substituting the POC3 kit and its frozen integration source. No upstream acquisition
or package upgrade is needed for this bounded change.

After image/offline validation and recovery, stop for owner Pi 3B testing. The
physical procedure must capture mode/renderer/geometry before expanding hardware
coverage, retain POC2 regression checks and stop without manual settings repair if
geometry remains wrong. POC4, other models and broader modernization are not authorized.

Primary interfaces checked 2026-09-16:
[VICE config/CLI order](https://vice-emu.sourceforge.io/vice_2.html),
[VICE SDL/fullscreen](https://vice-emu.sourceforge.io/vice_8.html),
[SDL logical size](https://wiki.libsdl.org/SDL2/SDL_RenderGetLogicalSize).
Exact VICE 3.10 source and the versioned diagnostic patch take precedence over
moving web documentation. Per-machine geometry is specified in the
[POC2 analysis](../qualification/poc2-pi3b-aspect-analysis.md).

## Host drift discovered and corrected before candidate acceptance

The VM's inherited unattended-upgrade timer ran on 2026-09-16 around 08:56–08:57 UTC.
It changed 13 versions and added one kernel package. This is **builder drift**, not
an appliance package upgrade. An initial assembly completed with the old host
inventory in its lock; it is retained as an unaccepted provenance attempt and must
not be flashed/qualified as POC3. Its lock starts `d7f801ef`; it is not overwritten.

Automatic APT/unattended-upgrade units are now masked in the disposable VM during
controlled work. This is not a change to appliance services. Retain the exact
changed binaries, corresponding sources, repository metadata and current inventory
under `inputs/poc3-host-supplement`. The corrected kit is `inputs/frozen-poc3-final`.
The running kernel remained 6.12.95+deb13-cloud-arm64; 6.12.107 was installed but
not booted. No host reboot intervened. Final package build started 09:05:22 UTC,
after logged automatic updates ended; its buildinfo and dependency inventory are
retained. Final image construction uses the corrected closure and a fresh workspace.

The factory now checks package names/versions against the lock and requires the
five automatic-update units masked before and after construction. Negative tests
reject drift, duplicate inventory and enabled update units. Do not weaken this
guard to rebuild. For intentional host maintenance, stop builds, review/unmask the
units or update explicitly, retain the new exact closure, and freeze a new lock.
Do not leave security maintenance forgotten merely because the disposable builder
uses controlled update windows. The repository recipe, not the VM state, is authority.
