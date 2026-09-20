# Boot presentation and timing

Quiet presentation and actual boot speed are separate. Project CBM suppresses the
firmware rainbow with `disable_splash=1`, uses `quiet loglevel=4 logo.nologo`, and
keeps `systemd.show_status=auto` so failures can still be reported. Root device,
console, filesystem, KMS and initramfs settings remain intact. These options follow
the [Raspberry Pi firmware documentation](https://www.raspberrypi.com/documentation/computers/config_txt.html#disable_splash)
and [kernel command-line documentation](https://www.kernel.org/doc/html/latest/admin-guide/kernel-parameters.html).

After normal tty1 login/PAM and any unfinished setup, the console session displays
Project CBM's primary artwork, then opens Menu (or the saved direct-boot profile).
This is the existing `pcbmcover1.jpg` from the released v1.0.0 image, rendered through
SDL2 at the existing display mode. Its historical Model 5 / 500 wordmark is retained;
the [hardware policy](../supported-hardware.md) determines supported models. It remains privately
admitted artwork pending the existing constituent graphics/font rights review.

The Product supervisor captures terminal state, bounds/reaps the renderer and restores
and checks the terminal before continuing. Presentation lasts 1.5 seconds after the
first frame is submitted, within the existing six-second total budget. Failure skips
the decoration. The seven machine Covers and their 0.75-second dwell remain distinct.
There is no root framebuffer writer, early graphics service or new VT owner. A clear
boot identity is intentional presentation time, not a claimed speed optimization.
Physical visibility and repeated display handoff still require owner qualification.

## Evidence behind the changes

RC1 on Pi 4 B completed boot and setup, but its primary graphic was physically absent.
The Menu called `pcbm-cover` without a profile; the current wrapper rejected that
obsolete invocation. Brief console text did not satisfy the intended appliance
identity. The released v1.0.0 used the same no-argument call for a numbered general
artwork image. RC2 uses an explicit primary mode with the current terminal supervisor,
rather than restoring the old framebuffer/ImageMagick implementation.

RC1 stopwatch power-to-Menu was approximately 30 seconds. Its second boot reported
2.354 seconds kernel plus 15.314 seconds userspace. These are different measurement
origins: neither systemd startup completion nor getty activation proves Menu is ready.
The retained journal shows getty activation at monotonic 10.615919 seconds and PAM
session opening at 15.749980 seconds, a 5.134061-second gap. The user manager then
started in 466 milliseconds. The exact RC1 image inherits getty `Type=idle`, whose
console-output deferral has a five-second ceiling (installed `systemd.service(5)`).
RC2 sets `Type=simple` in the existing getty drop-in, preserving all first-boot,
user-session, tty, login and PAM ordering. This removes that scheduling deferral;
it does not establish a measured RC2 power-on improvement before physical testing.

NetworkManager-wait-online is retained. Its large `blame` value was not the tty1
ordering bottleneck. No EEPROM, filesystem, swap or networking service is removed
on the basis of its duration alone. RC1's guarded completed-growth fast path remains:
valid protected completion skips repeated growth/sync work, while missing or unsafe
state still follows the existing initialization/failure checks.

## Measuring a boot

Use a stopwatch from power application until the first Menu accepts keyboard input.
Record first setup separately from later boots; record enabled services and storage.
On the Pi, collect:

```sh
systemd-analyze time
systemd-analyze critical-chain getty@tty1.service
systemd-analyze blame | head -n 20
```

RC2 also retains `/home/pcbm/.local/state/project-cbm/boot/boot.*.tsv`. Each line has
kernel-uptime seconds and a fixed phase: console entry, setup, profile initialization,
primary presentation, Menu entry, status collection and dialog dispatch. `first_input`
records completion of the first Menu interaction, **not** the instant the display first
became interactive. `dialog_dispatch` is the invocation boundary; use the stopwatch
and keyboard observation for actual readiness. No passwords, keys, filenames, network
identifiers or typed input appear in this trace. The owner can read it directly.
Primary rendering/restoration evidence is in
`~/.local/state/project-cbm/diagnostics/primary-presentation.json` on private candidates.
Compare monotonic values with journal monotonic values; systemd critical-chain values
are relative to userspace start. Never add concurrent unit durations together.

## Failure and recovery access

Ctrl+Alt+F2 provides the normal local console; Ctrl+Alt+F1 returns to Menu. The accepted
VICE-active VT limitation is unchanged: quit VICE first. SSH can collect diagnostics
when enabled. Kernel errors and service failures remain visible; the quiet settings
do not delete journals or disable failure handling. Keep exact failed-candidate evidence
before changing settings or reflashing. For deeper recovery see [recovery](recovery.md).
On your own customized image, removing `quiet` and restoring a higher `loglevel` in
the single-line `/boot/firmware/cmdline.txt` restores more console output; preserve
root and console parameters. Do not modify a qualification artifact during evidence
collection, and never claim quieter output alone proves faster startup.
