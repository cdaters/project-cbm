# Project CBM 1.1.0

Project CBM turns a Raspberry Pi into a Commodore-focused appliance: switch on,
choose a machine, and start exploring BASIC, games, demos or your own programs.
VICE 3.10 provides the emulation. Project CBM brings it together with a keyboard
Menu, first-boot setup, machine artwork and an organized content library.

## What is new

- Raspberry Pi OS Lite (64-bit), based on Debian 13 “Trixie”.
- Guided first boot for region, keyboard, timezone, administrator password and Wi-Fi.
- Project CBM startup artwork and machine-specific Covers before emulation.
- Eleven profiles spanning C64, SuperCPU 64, C64 DTV, C128 (40/80 columns), VIC-20,
  Plus/4, PET and the CBM-II families, including the faster C64 option.
- One `pcbm` account and an understandable library at `/home/pcbm/content`.
- USB import with read-only source access, duplicate preservation and filtering of
  known host-OS metadata. Supported dot-prefixed content remains discoverable.
- CCGMS 2021 for C64 BBS calls through the included modem bridge; SID-Wizard for
  creating SID music. Bring games, demos and other software you are entitled to use.
- File Sharing, Remote Access (SSH), Network Discovery, and useful IP/gateway/DNS
  information. Network services are opt-in, with clear connection instructions.
- Midnight Commander file management and normal Linux access for advanced owners.
- Expanded user, networking, content, recovery, customization and developer guides.

## Hardware

Raspberry Pi **4 B is physically qualified**. Pi 400, Pi 5 and Pi 500-class machines
are supported targets where compatible but are not all physically qualified. Use a
suitable power supply, cooling, HDMI display, keyboard and microSD card with room for
the uncompressed image and your content.

The final 1.1.0 image passed the owner's Raspberry Pi 4 B smoke test, including
fresh setup, display/input/audio, repeated emulator/Menu return, USB import,
a live CCGMS/TCPser BBS connection, reboot, persistence and shutdown.

Pi 3 and Zero-class systems are outside 1.1.0 support. Representative Pi 3 B+ VICE
workloads could not sustain the intended real-time experience. This is not a claim
that those machines cannot boot, or that every workload on newer models is benchmarked.

## Your first session

Follow [Getting Started](getting-started.md) to verify and flash the image. Connect
keyboard/display/audio, then complete the setup. Choose **RUN** for C64 BASIC.
Press **F10 → Quit** to return to Project CBM. Use **POWER** for safe shutdown.

**CONTENT** browses your library; **IMPORT** brings in USB files. The [User Manual](user-guide.md)
explains every Menu area and the [content guide](content.md) gives examples.

For BBS use, turn on BBS / Modem and launch CCGMS from its C64 Communications folder.
Select **Swift / Turbo DE** to match the shipped SwiftLink/ACIA interface at **$DE00**,
and begin at **2400 baud**. The [networking guide](networking.md)
walks through calling, exchanging text, disconnecting and returning to the Menu.

## File transfer and remote access

The default Computer Name is `projectcbm`; the username is `pcbm`. Enable services
when needed. SSH uses your administrator password. File Sharing uses its own password
and exposes the content library to your Mac or Windows computer. Direct hostname/IP
connection works even when automatic network browsing is unavailable.

## Installation and upgrades

Download `project-cbm-1.1.0.img.xz` and `SHA256SUMS` from the project release page.
On macOS use `shasum -a 256 project-cbm-1.1.0.img.xz`; on Linux use `sha256sum`;
on Windows use `Get-FileHash -Algorithm SHA256`. Compare the published value for that
exact file before flashing. Checksums detect changed/corrupt downloads; this release
is not cryptographically signed.

Flashing erases the selected card. Back up content and important settings first.
The supported upgrade path is a fresh image, first boot, then restoration of compatible
user data—not an in-place operating-system upgrade. See [backup and recovery](recovery.md).
After a reflash, an expected SSH host-key change is explained in [troubleshooting](troubleshooting.md).

## Known limitations

- Quit VICE before switching Linux consoles with Ctrl+Alt+F2/F1.
- Automatic network browsing varies by client/network; use the displayed hostname/IP.
- Hardware qualification is specific to the tested model; see the hardware guidance above.
- Generic PSID/RSID music-file playback is not provided; SID-Wizard is a music editor.

## Credits and notices

Thanks to VICE, TCPser, CCGMS, SID-Wizard, Raspberry Pi OS/Debian and their contributors.
Craig Daters created Project CBM's branding and Covers. Code and artwork have separate
terms. See [software and notices](software-components.md) and the accompanying source/
notice material. CCGMS uses an unchanged program on a Project CBM application disk;
unrelated upstream compilation utilities are not bundled. StrikeTerm is not included.

[All documentation](../README.md) · [Customization](customization.md) · [Development](development.md)
