# Getting Started

[Documentation index](../README.md) · [Complete User Manual](user-guide.md)

This is the short route from an image download to Commodore 64 BASIC. Project CBM
1.1.0 is released and starts with a short setup on the Pi.
[Download the current release](https://github.com/cdaters/project-cbm/releases/tag/v1.1.0).

## Hardware

Use a Raspberry Pi 4 B, a suitable power supply, an HDMI display and cable, a USB
keyboard, and a microSD card with room for the expanded image and your collection.
Check the download's **uncompressed** size, not just its smaller `.xz` size. Leave
space for setup, updates and content. A card reader is needed on your Mac or PC.
HDMI audio is the normal starting choice; turn up the display's volume. Ethernet is
optional and is often the easiest network connection. Wi-Fi can be set up on the Pi.
A controller is optional; the Menu works with a keyboard.

Project CBM 1.1 targets Pi 4 B/400, Pi 5 and Pi 500-class systems. Pi 4 B is physically
qualified; the other models are targets that still need their own physical qualification.
Pi 3/Zero-class systems are unsupported for 1.1: representative Pi 3 B+ VICE testing
could not sustain the intended real-time experience. This does not mean those machines
cannot boot the software. No blanket promise is made for every workload or peripheral.

## Download and check the image

Download [project-cbm-1.1.0.img.xz](https://github.com/cdaters/project-cbm/releases/download/v1.1.0/project-cbm-1.1.0.img.xz)
and [SHA256SUMS](https://github.com/cdaters/project-cbm/releases/download/v1.1.0/SHA256SUMS)
from the [1.1.0 release](https://github.com/cdaters/project-cbm/releases/tag/v1.1.0).
The raw `.img` is not uploaded separately. The source ZIP is not a bootable image.

A SHA-256 checksum is a fingerprint of a file. Compare the result below with the value
published **for that exact file**. A match detects corruption or unexpected changes;
it does not independently establish that the publisher or software is trustworthy.
For `project-cbm-1.1.0.img.xz` (599,290,700 bytes), the expected SHA-256 is:

```text
8b3738a204da16e148f5674a95f1ffb55a67b8ad1ce1d997b1858594a899c13d
```

The uncompressed image is 3,095,396,352 bytes. The published SHA256SUMS also lists
the accompanying source/documentation assets; you need not download those to flash
the image. The commands below check the image alone.

macOS Terminal:

```sh
shasum -a 256 project-cbm-1.1.0.img.xz
```

Linux terminal:

```sh
sha256sum project-cbm-1.1.0.img.xz
```

Windows PowerShell:

```powershell
Get-FileHash -Algorithm SHA256 .\project-cbm-1.1.0.img.xz
```

Do not flash a file whose checksum differs. Download it again and check the version.

## Flash the card

**Flashing erases the selected card.** Back up anything on it and double-check the
selected device. Disconnect unrelated removable disks if that helps avoid mistakes.

Raspberry Pi Imager can write a downloaded custom image; another image-writing tool
is also suitable. Choose your Pi, choose **Use Custom** (or the equivalent local-image
option), select the Project CBM image, select the SD card, and write it. Let verification
finish, then safely eject the card. Imager screens vary by version; see the
[official Imager instructions](https://www.raspberrypi.com/documentation/computers/getting-started.html).

**Skip Imager OS customisation.** Project CBM has its own account, Wi-Fi and first-boot
setup. Do not inject an alternate username, password, hostname, SSH configuration or
cloud-init setup. If your writer does not accept XZ, extract it first and write the
resulting `.img`, keeping the original download for checksum comparison.

## Connect and power on

With power disconnected, insert the card and connect keyboard, HDMI and optional
Ethernet. Switch the display to the correct input, then power the Pi. Some initial
black-screen time while video starts is normal. Project CBM artwork should appear
while the appliance prepares, followed by initial setup. This is not an instant-on
system; storage and connected hardware affect startup. The owner verified boot and
first setup on the final Pi 4 B image; no fixed startup-time promise is made.

## First boot

Project CBM prepares storage and system identity automatically. The setup screens ask
for language/locale, keyboard, timezone, an administrator password, and whether to use
Ethernet, Wi-Fi or remain offline. Wi-Fi also asks for the country where the Pi is used,
then scans for networks. Read working messages and wait for each operation to finish.

Your username is **pcbm**. Choose a password of **12–128 printable characters, excluding
colon**. Passwords are masked. Keyboard changes take effect after reboot, so the first
password is entered using the currently active layout; setup tells you this. Remember
that distinction when using punctuation. Wi-Fi uses an **8–63 printable ASCII character**
personal-network password. Optional remote services remain off until you enable them.

The default Computer Name is **projectcbm**. Setup does not add a separate name-selection
step; change it later under CONTROL → Network → Computer Name if needed. Applied setup
choices survive a restart. Back revisits screens; Escape pauses setup so it can resume.
After successful completion, the wizard does not repeat on later boots.

## Your first C64 session

1. At Main Menu, use Up/Down to highlight **RUN**, then press Enter.
2. A Commodore 64 Cover briefly appears, then VICE starts the C64. The BASIC screen
   is the emulated computer; Project CBM has not become a Linux desktop.
3. Try typing `PRINT "HELLO"` and press Enter.
4. Press **F10**, select **Quit** in VICE's menu, and confirm if asked.
5. You return to Project CBM. Choose **POWER**, confirm shutdown, and wait for the Pi
   to finish shutting down and storage activity to stop before removing power/card.

If your keyboard uses function keys for media controls, use its Fn key with F10.
Do not pull power while the Pi is writing. **REBOOT** safely restarts it instead.

Next: [learn the Menu](user-guide.md), [import your first disk](content.md#usb-import)
or [copy files from a Mac/PC](networking.md#file-sharing).
