# Using Project CBM 1.1

Project CBM turns a Raspberry Pi into a keyboard-driven Commodore appliance using
Raspberry Pi OS Lite, VICE and the Project CBM Menu. This guide describes the current
private 1.1 implementation, not a published release. See the repository's
[qualification record](../qualification/poc4-attempt6-pi3b-owner-report-2026-09-18.json)
for exactly what the owner tested on Pi 3B. A new image needs its own physical test;
installation and offline tests do not prove hardware or network discovery behavior.

## Flash and start

Use the exact image and SHA-256 in the candidate's physical procedure. On macOS,
`shasum -a 256 IMAGE.img.xz` prints its digest; Linux uses `sha256sum IMAGE.img.xz`.
Compare the entire value. Write the image with an imaging application, select the
correct expendable card and leave Imager OS customization off. Writing erases that
card. Safely eject it, connect HDMI and a keyboard to the Pi, insert it and power on.
Card capacity must exceed the actual raw image; leave space for your content.
Expansion happens through the appliance's first-boot owner.

Choose language, keyboard, timezone and Wi-Fi country during first boot. The owner
account is **owner**. Choose its password (12-128 printable characters, excluding colon); asterisks
confirm typing. This password protects Remote Access and Advanced administration.
There is no factory password. The ordinary console account **pi** runs Menu and VICE;
it is not the remote login account. The wizard can resume unfinished work and does
not rerun after successful completion.

Wi-Fi scans show bounded working feedback. Choose a network and enter its password,
or continue offline. Personal Wi-Fi accepts 8-63 printable ASCII characters. Enterprise
Wi-Fi is not part of the ordinary setup workflow. Ethernet uses normal network
configuration; device names need not be eth0 or wlan0. No connection means no IP is
shown. An address does not establish Internet access.

## Menu and machines

The Main Menu shows the default machine, current connected addresses and relevant
active or pending services. MACHINES can launch another machine/profile or save the
RUN default. RUN uses that default. A matching **Cover** appears during transition,
then VICE starts. A failed Cover never prevents emulator startup.

Press **F10** for VICE's menu and choose **Quit** to return to Project CBM. Preserve
VICE's complete aspect-correct canvas; save emulator preferences in VICE. From Menu,
Ctrl+Alt+F2 reaches tty2 and Ctrl+Alt+F1 returns. In the current SDL/KMS build, that
keyboard VT shortcut does not work while VICE is active: quit VICE first. Repeated
launch/quit remains the supported workflow; do not change keyboard/console modes to
force a switch. Advanced provides authenticated Linux administration. Owners retain
control of their Pi and can customize Linux, with corresponding recovery consequences.

## Content and utilities

CONTENT launches recognized files through the shared machine launcher. Your library
lives under `/home/pi/pcbm`, organized into games, demos, music, programs and ROMs.
Use content for which you have rights. IMPORT copies selected supported content from
USB into the selected category's `Imported` folder; music remains in
`/home/pi/pcbm/music/Imported`. Read the destination/count shown when import finishes.
Wait for the tool's unmount confirmation before unplugging USB. It does not turn every
USB filesystem into a permanently writable network share. FILES starts Midnight
Commander; quit it with F10 to return.

SID-Wizard is an optional Commodore music editor, launched through its registered
application entry and the existing VICE path. StrikeTerm is a terminal application
available only in admitted private engineering images; its public redistribution
remains gated. Presence is not qualification: test each application and USB import
using the candidate procedure. TCPser supplies the optional BBS / Modem connection;
configure the emulator's local modem endpoint shown under Services. Network BBS
access needs an endpoint you are entitled to use; no Internet-facing server is enabled.

## Configure and shut down

CONTROL groups machine preferences, picture/sound/controllers, region, Network,
Services, storage, information and Advanced. Network contains **Computer Name**
(default `projectcbm`), Wi-Fi and current network details. Services contains state-aware
On/Off actions and **How to connect**. See [networking and services](networking.md).
System Information retains detailed IP, MAC, interface, package and runtime information.
Saved preferences and actual running state are distinguished.

Choose POWER to shut down before removing power or storage. REBOOT restarts safely.
If a core function regresses during qualification, stop and preserve the candidate's
allowlisted diagnostics before launching again; never repair a test artifact in place.
See [troubleshooting and recovery](recovery.md). Rainbow and startup text remain visible.
Quiet presentation and measured faster boot are separate future work.
