# POC1 Pi 3B failure analysis — owner review

Recorded/researched 2026-09-15. **Diagnosis is evidence-ranked, not confirmed.**
No runtime code, package, integration stage or candidate was changed. No VM was
started, candidate booted, media obtained or POC2 built for this analysis.

## Result and evidence boundary

[Physical record](poc1-pi3b-2026-09-15.json) records the owner's test, not a test
observed by the analyst. Firmware/OS boot, tty1 Menu arrival/rendering and keyboard
navigation PASS. RUN/x64sc display and subsequent console recovery FAIL. VICE
video qualification, audio, input, exit/return, configuration persistence and
later qualification are UNTESTED because testing stopped. Intermittent activity
LED is an observation, not proof that VICE or the whole kernel remained healthy.
No failed-run log, PID, exit status, kernel trace or display identity is available.

The owner separately encountered raspi-config privilege errors. See the
[setup/privilege review](setup-ux-review.md). Disabled/masked SSH, Samba, TCPser,
Avahi and NetworkManager are declared POC1 policy, not qualification failures.

## Exact inspected inputs

Paths below are relative to the configurable external ProjectCBM-Work root.
Canonical frozen identities remain in the [build checkpoint](../build/private-poc1.md).
Both raw images were opened read-only through a userspace ext4/FAT reader, without
mounting, executing or changing them. Whole-image SHA-256 was rechecked.

| Evidence | Identity |
| --- | --- |
| POC1 raw image, `artifacts/private-poc1/2026-09-15-project-cbm-1.1.0-poc.1-lite-private-poc.img` | `ae8d2032736e1d3ae2e49d4370aa62d00fc06f9fc567e70e400491900d45bf9f` |
| Preserved released v1 image, `archive/audit-2026-09-14/workspace/assets/pcbm-v1.0.0-rpi3-5.img` | `168a3026eca2bc328e03e47dfbb0cbe17740180504ad7858496df84982e89849` |
| `inputs/frozen-poc1/release-lock.json` | `703aa6e1b0d278262a2dc83c31740b3c589788e3953e3ac822e948133529d566` |
| POC1 integration commit | `024db4985202ef0675b12e12b8982af91c6d6ad3` |
| Menu input `v1.1.0_poc1`, peeled | `77a708019c9d8a11e657d7e5d2dde7b7ecb340ba` |
| Historical Menu forensic ref, peeled | `a4148db54001790eaddb4e31104917c16149b181` |
| VICE .deb in `packages/poc1`, 3.10-1+pcbm1 arm64 | `674c40040965b689d08cdc225f8954c0fb2433ef68459f51aa7f6360b1710d20` |
| Menu .deb in `packages/poc1`, 1.1.0~poc1-1+pcbm1 all | `3f7557cdbdd44922954a6e640a1bcb3a96f446f6dbe6631afe667aa5e5d5f0fd` |
| VICE 3.10 source tar (same retained upstream tar as historical build) | `8e5bac18cbcb9f192380ad3ef881f8790f5b75c41d7b3da65d831985d864d6d1` |

POC1 installed x64sc SHA-256 is
`b7e935003bcec341023d1f46651c7995a6446d43e3b43990ab6bade5b8e7b7d0`;
it matches the exact .deb payload. Historical x64sc is
`fbde635eea9dd5d610a1e60d8d4ce1077399d5fcffcddb10b5f42140d741f3b2`.
Selected Menu launcher files also match their package payloads. No wrong-package
substitution was found. Selected original v6.4/v6.5 build notes were read in place;
no historical scripts were executed and no historical evidence was edited.

## Ranked causes and counterevidence

### 1. Graphics runtime closure differs from the working baseline

**Observed:** v1 contains libGL.so.1/GLX and EGL/GLES. Its preserved
`/home/pi/.local/state/vice/vice.log` identifies the selected SDL renderer as
`opengl`. That log does not establish which physical model produced it.
POC1 lacks libgl1/libglx0/libglx-mesa0 and libGL.so.1. It has libEGL, libGLESv2,
libgbm and Mesa DRI including vc4_dri.so. The v1 notes explicitly installed
`libgl1-mesa-dri`, `libegl1`, `libgles2` alongside development dependencies.

**Inference:** slimming/package dependency discovery omitted a dynamically loaded
runtime path used by the previous appliance. This is the strongest concrete
renderer delta and a leading fix candidate. ELF DT_NEEDED checks alone cannot
establish SDL's dlopen dependencies.

**Important limit:** missing desktop GL does **not** prove the black screen.
The exact retained SDL 2.32.4 source retries an ES2 context when desktop EGL/GL
loading fails; VICE also tries a fallback renderer. Both images contain the
**same SDL2 binary**, SHA-256
`6e4be9d6b75dc75e7ed44b61d681649e4fc0389182f50350f980ee8105bf62fa`.
A working GLES fallback is plausible but untested on this Pi. Declare the intended
OpenGL runtime closure explicitly and test the fallback/selected driver; do not
add development packages or assert that installing libGL alone is a proven cure.

### 2. Console session and recovery contract regressed

**Observed:** v1 uses tty1 agetty autologin, login/PAM (including pam_systemd),
pi's `/bin/bash`, and a tty1-only dispatch to CBM. POC1 masks getty@tty1 and runs
`pcbm-console.service` directly as pi, with StandardInput=tty, TTYPath=/dev/tty1,
explicit HOME/TERM, but no PAMName. pi's account shell is `/usr/sbin/nologin`;
factory policy supplies no login password. A directly invoked Bash starts Menu
regardless of the account shell, so Menu success does not validate login recovery.

**Inference:** the new arrangement lacks the normal PAM/logind session and
XDG_RUNTIME_DIR setup. It needs deliberate active-seat/DRM/VT ownership validation.
Ordinary tty2 login is also not a usable recovery path with this account policy.
This is a definite observability/recovery design gap, a plausible graphics
contributor, and not proof of DRM permission denial.

**Counterevidence:** both images give pi audio/video/input/render membership;
Group=pi does not discard supplementary groups. StandardInput=tty can provide a
controlling terminal without PAM. Neither absent PAM nor the nologin account
alone proves VICE cannot render. Do not fix this by running VICE as root.

### 3. Pi 3 KMS/Mesa/kernel interaction, including event-loop blockage

POC1 has kernel 6.18.50+rpt, Mesa 26.2.2 and libdrm 2.4.134; v1 has kernel
6.12.75+rpt, Mesa 25.0.7 and libdrm 2.4.131. These are substantial graphics-stack
differences with no physical regression comparison yet. Both boot configurations
use full KMS (`vc4-kms-v3d`), max_framebuffers=2, disable_fw_kms_setup=1 and audio=on.
The Pi 3 vc4 DRI driver is present. The additional POC1 Pi 5 stanza is not evidence
of a Pi 3 fault. No evidence currently justifies a kernel rollback or SDL upgrade.

SDL's Linux keyboard implementation sets K_OFF while reading evdev and installs
VT_PROCESS callbacks. A blocked event loop or failed cleanup can prevent ordinary
Ctrl+C/VT behavior even while other Linux activity continues. Thus the owner's
console symptom is compatible with SDL/DRM initialization or runtime blockage;
it does not establish a kernel-wide hang. Record actual card/connector/mode,
DRM master/session state, kernel errors and process state on the next candidate.

### Lower-ranked alternatives / findings

- **Audio:** both paths use SDL_AUDIODRIVER=alsa and `-sounddev sdl`. The same
  pcbm-audio helper runs before exec. It could stall; no timing markers distinguish
  audio setup from VICE entry. ALSA differs by a Debian maintenance revision.
- **Resource lookup:** POC1 installs under /usr rather than /usr/local; x64sc's
  compiled DATADIR is /usr/share/vice. C64 BASIC/kernal/chargen and default SDL
  keymap exist and match v1 byte-for-byte. Recursive ELF dependency resolution
  found 84 required library names with none missing (including Pulse's private
  library path). This does not validate GPU drivers loaded later at runtime.
- **Configuration:** POC1 has no historical sdl-vicerc. v1 explicitly seeds F10
  (MenuKey=291), 720x576 window geometry and VICIIGLFilter=1. Absence is a real
  defaults/exit-contract gap; old off-screen coordinates must not be copied
  blindly. No forced SDL2Backend was found in that v1 configuration.
- **Splash/framebuffer:** POC1's cover directory is absent. pcbm-cover therefore
  exits before fbi/fbset/display manipulation; splash interference is unlikely
  for this exact image. tty reset/clear/chvt behavior remains in the launch path.
- **Launcher:** pcbm-boot/menu/dialog-lib/audio normalize to the historical scripts
  after the intentional /usr/local/bin to /usr/bin relocation. HOME and XDG
  config/state/data paths are set, but not XDG_RUNTIME_DIR. VICE stdout/stderr goes
  to /tmp/pcbm-vice.log, overwriting the audio prelude. Recovery runs after process
  exit; it cannot rescue a blocked process. Existing EXIT cleanup is not a full
  VT/DRM recovery mechanism.

## Build comparison

| Area | Historical v1 | POC1 |
| --- | --- | --- |
| VICE UI/version | 3.10 SDL2 | 3.10 SDL2 |
| Configure | --enable-sdl2ui --disable-gtk3ui --disable-pdf-docs --enable-x64 --without-pulse | --enable-sdl2ui --with-alsa --with-sdlsound --without-pulse --disable-arch --enable-x64 --disable-html-docs |
| Installation | source-built /usr/local; runtime and development environment mixed | external Debian package /usr, generic ARMv8 flags/hardening |
| Confirmed POC configure summary | historical notes are not full build-chain closure | SDL2, hardware scaling, ALSA/SDL sound; Pulse disabled |
| Raspberry Pi OS | Trixie 13.4 | Trixie 13.7 |
| SDL2 | 2.32.4+dfsg-1 | same package and binary |
| Console | getty/login/PAM | direct system service, no PAMName |
| Default VICE configuration | historical user file | fresh upstream defaults |

The old image's success is behavioral evidence, not authorization to import its
identity, unsafe privileges, development dependencies or unreviewed configuration.

## Can offline inspection determine whether x64sc stayed running?

**No.** It verifies executable/resource presence and identifies viable failure
paths. It cannot determine whether this run reached x64sc, exited unsuccessfully,
blocked in audio/DRM setup, or ran with unusable output. No candidate binary was
executed during analysis. Ctrl+C, VT keys and activity LED cannot settle this.

## Proposed factory/source fix and observability (authorization required)

1. Declare the desktop GL runtime and its resolved closure as package/runtime
   inputs. Check SDL's dynamically loaded paths explicitly. Initially retain the
   other POC1 graphics-stack pins to limit variables; no VICE rebuild-option or
   architecture change without further evidence.
2. Use one supported tty1 login/PAM/logind session and a small CBM dispatch, with
   an intentional interactive-account policy. Prefer standard getty/login/PAM
   integration over hand-emulating a session. Keep Menu/VICE unprivileged. Restore
   a tested F10/return contract without copying all historical window settings.
3. Private engineering profile: bounded persistent launch logs/journal, per-launch
   ID, monotonic timestamps, selected SDL backend/renderer, allowlisted environment,
   audio-before/after, spawn/PID and exit status. Preserve stderr rather than
   truncate earlier stages. Do not log credentials, full environment or history.
4. Add an independent, bounded diagnostic sampler (process state/wchan, session,
   DRM/kernel messages) that does not depend on VICE's event loop. Retain logs for
   offline SD extraction after failure. Persistent logging cannot guarantee the
   last records survive abrupt power loss; cap storage and flush key markers.
5. Provide engineering-only tty2 non-root diagnostic access with a valid shell.
   A second VT alone is insufficient if VT switching stalls. Offline persistent
   records are the baseline. SSH is optional only with separately declared profile
   policy and operator-supplied authorized key, isolated test networking and no
   reusable private key/password; it is not a public default or required network.
6. Do not grant generic sudo, disable DRM master checks, chmod devices broadly,
   force card0, keep the console keyboard active behind VICE, or treat a watchdog
   reboot as proof of a working emulator. Unsupported setup actions should state
   the engineering limitation rather than tell users to repair sudoers.

## Prebuild and physical validation plan

Before rebuilding: test package metadata and dlopen closure on the staged root;
verify installed/source/package identity; validate units/PAM/one tty owner and
account policy; test launch success/nonzero-exit/signal/hang paths with controlled
stubs, log preservation/rotation and redaction; test no blanket sudo; verify
engineering-profile-only diagnostics and two-flash identity sealing. Check seeded
F10 settings and writable HOME/XDG paths. VM tests can test sessions and logging,
not Pi 3 KMS/audio. Add missing checks to the validator rather than retroactively
changing POC1's 50 historical PASS results.

Proposed **POC2 only**: the closure/session/default-return repairs above, bounded
engineering observability, truthful setup-action gating, and the separately
[declared tiny media bundle](poc2-media-plan.md). No broad network/privilege UI,
new updater, foundation change or unrelated features. All changed packages,
integration, media and lock receive new identities; POC1 stays immutable.

After owner authorization and new-image offline checks, flash POC2 to Pi 3B.
First confirm persistent records and diagnostic access, then run default x64sc,
collect backend/renderer/session information and qualify video/audio/input/F10
return using the declared media. Stop on failure and extract logs without repair.
Only subsequent separately planned frozen candidates should vary renderer or
kernel if the evidence still requires isolation. Do not claim physical passes
from the prebuild checks.

## Source basis (research date 2026-09-15)

Primary evidence is the exact retained inputs above, the VICE build log
`packages/poc1/vice-build-sdlimage.log`, and retained SDL source object
`inputs/frozen-poc1/objects/d364cded8bf41f3f503014d3fb6473f1a7077ff468da1638dae4a6bec6ef2277`.
VICE's `src/arch/sdl/video_sdl2.c` contains automatic renderer selection/fallback.
SDL's KMS video implementation retries GLES; its keyboard implementation sets
K_OFF and handles VT callbacks. Upstream cross-checks:

- [SDL 2.32.4 KMS source](https://raw.githubusercontent.com/libsdl-org/SDL/release-2.32.4/src/video/kmsdrm/SDL_kmsdrmvideo.c)
- [SDL 2.32.4 console keyboard source](https://raw.githubusercontent.com/libsdl-org/SDL/release-2.32.4/src/core/linux/SDL_evdev_kbd.c)
- [SDL DRM master requirement](https://wiki.libsdl.org/SDL2/SDL_HINT_KMSDRM_REQUIRE_DRM_MASTER)
- [systemd execution/session semantics](https://manpages.debian.org/trixie/systemd/systemd.exec.5.en.html)
- [pam_systemd session setup](https://manpages.debian.org/trixie/libpam-systemd/pam_systemd.8.en.html)
- [journal persistence/bounds](https://manpages.debian.org/trixie/systemd/journald.conf.5.en.html)

Measured/inspected facts, upstream behavior, engineering inferences and proposed
changes are distinguished above. No hypothesis is a confirmed physical diagnosis.


## Analysis checkpoint verification

- 26 existing host-only tests PASS, including immutable product/Menu release and
  Menu recovery tag assertions; no new runtime test result is implied.
- New qualification JSON parses with duplicate-key/non-finite-number rejection;
  35 local links in the seven changed/new documents resolve, including anchors.
- git diff --check PASS; changed documents reviewed for private keys, tokens,
  password hashes and accidental binaries. No historical image extracts in Git.
- Original historical preservation manifest: all 1,677 entries unchanged.
- Both raw images rehashed; POC1 executable/launcher package payload agreement
  checked. No image, stage, packaging or runtime source changed.
- Private inspection results/tool and an additive documentation Git checkpoint
  belong at `qualification/poc1-pi3b-2026-09-15` under the configured bulk root.
  Its checkpoint manifest records exact commit/bundle identities and offline
  restore verification. Earlier sealed checkpoints are not replaced.

The accompanying Menu repository is unchanged at
`99063f8299192877f7d17d0ccd9635f135b89fdc`. No push is part of this checkpoint.
