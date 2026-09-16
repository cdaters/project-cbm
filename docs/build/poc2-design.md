# POC2 implementation and build guide

Owner authorized the bounded follow-up to the immutable POC1 Pi 3B launch failure.
The [analysis](../qualification/poc1-pi3b-analysis.md) remains historical evidence.
No single correction establishes the physical root cause.

## What changes

- VICE package revision declares SDL's dynamically loaded GL/GLX/EGL/GLES/GBM and
  Mesa DRI runtime dependencies. No desktop or development package is needed.
- Standard getty → login/PAM → pi's Bash owns tty1 and the engineering tty2. PAM
  establishes the login/session environment; one system-owned profile dispatches
  only tty1 to a small Menu loop. No desktop manager or direct competing tty unit.
  pi has a valid shell but its password stays locked. Autologin is local only.
- Shared unprivileged Menu launcher covers RUN and content. VICE `-menukey 291`
  selects F10: open emulator menu, choose Quit, confirm, return to Menu. It does
  not mean F10 immediately terminates emulation. No historical window geometry.
- Product engineering observer bounds stdout/stderr, records identity/PIDs/timing/
  exit/signal and samples still-running processes. A running sample is not a hang
  diagnosis. It saves/restores the owned terminal's keyboard/text/termios state.
- `pcbm-diagnostics` creates a local report without root, network or a daemon. Four
  launch directories, 128 KiB output tail each, three bounded snapshots each and
  one report bound ordinary use; logs are local private troubleshooting material.
  Allowlisted environment only, no process argv, credentials or serial/EDID dump.
  Kernel-journal permission denial is retained as a limitation, not bypassed.
- tty2 autologin is engineering-only and non-root. SSH and other POC1 masked network
  services remain disabled. Exact no-argument reboot/poweroff are the only added
  sudo operations, for safe qualification shutdown; no arbitrary service control.
- Original tiny [media](../../qualification/media/README.md) is declared in lock
  schema 2, injected before image freeze into ordinary content paths. Schema 1
  remains readable for POC1. Known-good independent runtime validation is pending.
- Unsupported network/BBS/raspi-config actions explain the engineering restriction.
  Full offline-first setup and narrow privileged configuration remain later 1.1 work.

Primary references checked 2026-09-15:
[agetty](https://manpages.debian.org/trixie/util-linux/agetty.8.en.html) delegates to
login, including autologin; [pam_systemd](https://manpages.debian.org/trixie/libpam-systemd/pam_systemd.8.en.html)
registers sessions. VICE 3.10 retained src/arch/sdl/ui.c declares -menukey and MenuKey.
These mechanisms do not substitute for a Pi 3B KMS/session test.

## Controlled workflow

1. Guard external storage with tools/build_host.py preflight; start the existing
   approved Lima guest. Use SSH/rsync; all guest builds stay on ext4, virtual disk
   and retained outputs on the configured bulk volume.
2. Verify POC1 preservation baseline. Commit/review sources, create a distinct
   local Menu candidate tag and retain the exact archive/peeled commit/hash.
3. Build updated VICE/Menu packages externally. Retain TCPser unchanged when its
   source/package is unchanged. Preserve package build records and corresponding source.
4. Build the original media from its committed source. Record the real archive/
   per-file hashes and pending independent runtime qualification.
5. Derive a NEW frozen POC2 input kit from POC1 plus explicitly verified new inputs.
   Do not rewrite POC1 lock/objects/packages. Retain newly required APT binaries,
   authenticated metadata and corresponding sources; keep kernel/Mesa pins.
6. Run host/Linux tests before assembly. Construct through the frozen factory in
   an isolated network namespace. Missing retained input must fail closed.
7. Perform read-only image validation, export raw/XZ hashes and footprint, verify
   POC1 remained unchanged, update continuity and additive recovery bundles.
8. STOP: owner performs the separate physical test. No POC3, SSH or publication.

This guide records the recipe; the final POC2 checkpoint will bind exact commits,
commands, hashes, outcomes and physical test instructions. One controlled build
is not proof of independent reproducibility or a working Pi GPU.

## Reference-test findings before image construction

The isolated builder reference uses newly built VICE, SDL dummy video with the
software renderer, and source-tree system resources; it is independent of the
candidate's Pi KMS/ALSA/tty path. Smoke PRG and D64 produced the expected PASS screen;
the SID program completed and video/input rendered colors and a star. These checks
do not establish physical audio, keyboard/joystick input or Pi graphics.

The first reference attempt crashed before logging: VICE 3.10 src/log.c:746–767
leaves color-stripped pointers null when file logging is off and color is on,
then uses those pointers when stdout is redirected. GDB identified the banner's
log_archdep call. Supported `+logcolorize -logfile -` avoids that crash and routes
output through CBM's bounded observer. No VICE source patch or guessed upstream
fix is applied. This reference failure does not retrospectively identify POC1's
physical cause (POC1 used default file logging).

A dummy-audio WAV recorder initially produced zero channels, and warp-mode file
output produced no samples; these are retained test limitations, not media PASS
claims. The final reference record distinguishes program execution, audio samples,
and still-unperformed human/physical checks. A cycle-limit exit is deliberately
nonzero in VICE; inspect expected screenshots/logs, not exit code alone.

GDB installation affected 12 host binary packages (including Python dependency
updates despite apt's --no-upgrade option). Supplemental exact binaries, sources,
metadata and inventory are retained for image-assembly provenance. Component
packages were built before that diagnostic installation. None of these debugging
dependencies are added to the appliance.
