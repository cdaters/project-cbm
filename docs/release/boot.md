# Boot presentation and timing

Quiet presentation and actual speed are separate. The RC1 source disables the
firmware rainbow (`disable_splash=1`), uses `quiet loglevel=4 logo.nologo` for the
kernel and `systemd.show_status=auto` for service startup. Kernel errors and service
failure reporting remain available. Root device, console, filesystem, KMS and
initramfs settings remain intact. These options follow the
[Raspberry Pi firmware documentation](https://www.raspberrypi.com/documentation/computers/config_txt.html#disable_splash)
and [kernel command-line documentation](https://www.kernel.org/doc/html/latest/admin-guide/kernel-parameters.html).

Project CBM's text presentation uses `/etc/issue` and the existing tty1 login session.
It adds no delay, renderer, framebuffer writer, video-mode switch or competing VT
owner. `/home/pi/.hushlogin` suppresses routine login prose for the appliance account;
getty/login/PAM still establish the session. The normal first-boot wizard, Menu and
Cover/VICE transition retain their owners. This is a simple console presentation,
not an animated early-firmware graphic; its appearance requires physical checking.

## Baseline and the bounded speed change

The owner measured unchanged attempt #8 on Pi 4 B: kernel 2.390 s, userspace 16.960 s,
19.351 s total, with graphical.target at 16.959 s userspace. Samba and its network
readiness wait were the reported target critical path. NetworkManager-wait-online
spent 5.966 s; this is not automatically a delay to interactive Menu. No stopwatch
power-on-to-Menu measurement was collected. Unit times can overlap and must not be
summed as if serial. Enabled owner services also affect comparisons.

The Project CBM first-boot initializer took 1.885 s and source inspection showed that
it reran partition growth, filesystem expansion and global sync despite already
having a completion marker. RC1 returns early only for the exact valid marker in
its root-protected state directory. Missing completion still executes all original
geometry/growth checks. Malformed or unsafe completion fails for inspection rather
than silently claiming success. The Menu setup wizard has its own existing state.
This removes unnecessary repeated work; actual Pi boot-time improvement remains to
be measured on the new image. No timing saving is claimed from quieter output.

Networking, wait-online, Samba, EEPROM checks, filesystem checks and swap services
are retained. Disabling a useful service merely because it appears in `blame` is not
an accepted optimization. A clone of a fully initialized card is not a fresh image:
it retains completion and does not automatically expand again. Use a fresh image
and selective content restoration, or deliberate Linux storage administration.

## Compare and recover

On each candidate collect `systemd-analyze time`, `systemd-analyze critical-chain`,
`systemd-analyze critical-chain getty@tty1.service`, and `systemd-analyze blame`.
Also time power-on to the interactive Menu with the same Pi, storage, network,
services and peripherals. Separate first boot from subsequent boots. Record repeated
runs and any failure; a headless VM does not qualify visible boot behavior or Pi speed.

If normal boot needs inspection, use tty2/Advanced or SSH when enabled. The current
boot's kernel/service logs remain available; do not assume persistence after shutdown.
For verbose next-boot diagnostics, an owner can edit the FAT boot partition's
`cmdline.txt`, removing `quiet`, `loglevel=4` and `systemd.show_status=auto`. Keep the
file on one line and preserve root/console options. Removing `disable_splash=1` from
`config.txt` restores the firmware rainbow. Preserve the original files first and
bind modified test state separately from the immutable candidate.

The implementation is `tools/boot_presentation.py`, `tools/install_poc_stage.py`,
`build/pigen/stage-cbm/files/pcbm-console-session` and `first_boot.py`. Changes require
a distinct image, actual-image validation and a physical lifecycle/boot regression.
