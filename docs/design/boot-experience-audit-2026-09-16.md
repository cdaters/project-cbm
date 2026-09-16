# Boot experience: presentation and performance

**2026-09-16 — read-only POC3 audit and future measurement design.**
No boot settings changed, VM started, image rebuilt or physical timing performed.
The owner observed rainbow screen → Linux/kernel/systemd text → Project CBM Menu.
That is not a POC3 failure: quiet boot and timing were outside its qualification scope.

## Observed exact POC3 path

Boot FAT contents were read directly from the frozen raw image without mounting or
writing it. The active kernel command line is:

```text
console=serial0,115200 console=tty1 root=PARTUUID=2fd93bd6-02 rootfstype=ext4 fsck.repair=yes rootwait
```

Relevant config.txt entries include `dtparam=audio=on`, `display_auto_detect=1`,
`auto_initramfs=1`, `dtoverlay=vc4-kms-v3d`, `max_framebuffers=2`,
`disable_fw_kms_setup=1`, `arm_64bit=1`, `disable_overscan=1`, `arm_boost=1`.
There is no `disable_splash=1`, `quiet`, logo suppression or systemd status policy.
Thus visible firmware/kernel/status output is consistent with the frozen inputs.
The PARTUUID above is this image's identity, not a future device assumption.

The first-boot unit runs after local filesystems/machine-id commit, before getty on
tty1/tty2, with a ten-minute timeout. The getty override starts agetty autologin for
non-root pi. The profile execs the Project CBM console session only on tty1; tty2
remains the diagnostic terminal. The session loops Menu and restores terminal state.
This getty/login/PAM sequence supplies the working emulator session; do not remove
it merely to hide a banner. The older Menu startup/bootmode flow is a separate
implementation and must not silently become a second first-boot coordinator.

The legacy cover helper uses framebuffer tooling and optional conversion/delay.
Its presence in source is not a measured contribution to this image's boot time;
asset availability and the actual executed path must be checked before blaming it.
No captured on-Pi critical-chain trace exists. Enabled-unit lists cannot establish
which services materially delay an interactive Menu.

## A. Presentation / quietness recommendation

The firmware rainbow screen is controlled by Raspberry Pi firmware; upstream
[`disable_splash`](https://www.raspberrypi.com/documentation/computers/config_txt.html#disable_splash)
documents suppressing it. A future quiet candidate can evaluate that setting,
`quiet` and `logo.nologo`, plus a deliberate systemd status policy. Keep the modern
KMS display mode and all emulator geometry/session behavior. These are proposed
candidate inputs, not instructions to edit POC3 on the Pi.

The [kernel parameter reference](https://www.kernel.org/doc/html/latest/admin-guide/kernel-parameters.html)
and [systemd manual](https://manpages.debian.org/trixie/systemd/systemd.1.en.html)
distinguish console verbosity from logging. Prefer status-on-failure behavior where
usable (`systemd.show_status=auto`) over hiding every fault. Retain bounded logs and
the engineering diagnostic path. Do not disable journald or redirect all errors to
/dev/null merely to produce a clean display. Initramfs and firmware messages may
need separate policy; kernel quiet alone is not a complete seamless-boot mechanism.

Start with a brief intentional Project CBM text/banner when the console is ready,
then immediately show Menu. No artificial display delay. Defer a Plymouth/graphical
splash until measured benefit justifies dependencies and another DRM handoff. Hiding
a login banner must not bypass PAM/session setup or delay errors indefinitely.

Provide a documented verbose engineering build profile with the same essential
runtime configuration. Quiet/verbose choice is declared input identity. A tester
should collect diagnostics on failure, not manually alter a frozen qualification
system. Normal product troubleshooting policy is a separate decision from POC3's
private tty2 console. Do not automatically ship engineering access unchanged publicly.

## B. Actual boot performance recommendation

Measure before removing services or adding optimizations. Separate first boot's
expansion/identity/user initialization from subsequent cold boot and reboot. Inspect
[`systemd-analyze time`, `blame`, `critical-chain`, `plot`](https://manpages.debian.org/trixie/systemd/systemd-analyze.1.en.html)
and monotonic journal timestamps. Blame is not the critical path: work overlaps,
some units report started before an application is usable, and firmware timing may
not be available on Raspberry Pi. Do not add all unit durations together.

Do not remove fsck, identity generation, entropy/security initialization, KMS or
getty/PAM to shorten a number. Investigate actual waits, repeated probes, unnecessary
blocking tasks and cover conversions only after traces identify them. Background
work still competes for Pi 3 CPU/storage and must be considered in Menu response.
No measured acceptance budget is claimed by this audit.

## Start-to-finish future measurement procedure

1. Use a newly authorized exact-hash candidate. Record Pi model, RAM, boot medium,
   power supply, display/mode, attached devices, temperature/throttling and input lock.
2. Record an external video/timer reference starting at power application. This covers
   firmware/pre-kernel time that Linux timestamps cannot reliably supply. Define the
   first intentional Project CBM presentation visibly, excluding rainbow/kernel text.
3. Record the first interactive Menu, confirming a key moves selection. Process start
   or a drawn screenshot alone is not proof of interactivity.
4. From Menu, time RUN until C64 is visibly usable and responds to a key. From VICE
   Quit, time until Menu accepts navigation. Capture exact timestamps/action markers.
5. Capture reboot-command → interactive Menu separately from power-on → Menu.
6. Retain systemd time/blame/critical-chain/plot and relevant monotonic journal output,
   with private data omitted. Proposed future application readiness markers should
   correlate with these logs, not replace external observation.
7. Use separate first-boot and steady-state samples; collect at least ten controlled
   steady-state trials when practical. Report all values, median and range; treat a
   percentile from a small sample cautiously. Do not conceal outliers or failed starts.
8. Compare one bounded change at a time using the same hardware/media. Record actual
   CPU/RAM/storage pressure and first-boot-only work before proposing a budget.

Required metrics: power-on → intentional presentation; power-on → interactive Menu;
reboot → interactive Menu; Menu → usable x64sc; VICE Quit → interactive Menu. Retain
measurement method/uncertainty and raw observations externally, summary in qualification
records. No additional physical tests are authorized by this document.
