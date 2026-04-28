<p align="center">
  <img src="assets/images/project-cbm-header.png" alt="Project CBM" width="100%">
</p>

# Project CBM

**Project CBM** is a ready-to-boot Raspberry Pi image that turns a Raspberry Pi into a clean, keyboard-friendly Commodore emulation environment.

It is built around Raspberry Pi OS Lite, the console/SDL2 version of VICE, and a custom Project CBM menu system. The goal is simple:

> Power on. Boot fast. No desktop required. Just Commodore.

## Project Background

Project CBM v1.0.0 was created as a modern Raspberry Pi OS Lite-based Commodore emulation image inspired in part by the appliance-style experience of Carmelo Maiolino's Combian64.

Project CBM is independently assembled and is not a fork of Combian64. The v1.0.0 release focuses on providing a ready-to-image Project CBM environment for Raspberry Pi 3, Raspberry Pi 4, Raspberry Pi 5, and Raspberry Pi 500-class systems.

## Current Release

**Version:** v1.0.0  
**Image artifact:** `pcbm-v1.0.0-rpi3-5.img.xz`

The release image is distributed through **GitHub Releases**. Large image files are not stored directly in this repository.

## Supported Hardware

Target systems:

- Raspberry Pi 3
- Raspberry Pi 4
- Raspberry Pi 5
- Raspberry Pi 500

Recommended:

- Raspberry Pi 5 or Pi 500 for best performance
- Quality 16GB or larger microSD card
- HDMI display/audio
- USB keyboard
- Optional USB gamepad/controller
- Optional Ethernet connection for easiest first network setup

## What Is Included

Project CBM includes:

- Raspberry Pi OS Lite base
- VICE 3.10 console/SDL2 build
- Project CBM menu system
- Commodore machine launchers
- Splash/cover screen support
- USB import helpers
- Samba/network sharing helpers
- BBS/modem support hooks using TCPser
- Appliance-style runtime configuration

## Screenshots

<p align="center">
  <img src="screenshots/v1.0.0/02-main-menu.png" alt="Project CBM Main Menu" width="45%">
  <img src="screenshots/v1.0.0/03-machines-menu.png" alt="Project CBM Machines Menu" width="45%">
</p>

<p align="center">
  <img src="screenshots/v1.0.0/04-content-menu.png" alt="Project CBM Content Menu" width="45%">
  <img src="screenshots/v1.0.0/09-vice-c64-startup.png" alt="VICE C64 startup through Project CBM" width="45%">
</p>

See the full [Screenshot Gallery](docs/screenshots.md).

## Download

Go to this repository's **Releases** section, open the latest release, and download the files listed under **Assets**:

```text
pcbm-v1.0.0-rpi3-5.img.xz
pcbm-v1.0.0-docs.zip
SHA256SUMS
```

Then verify the image before flashing:

```bash
sha256sum -c SHA256SUMS
```

On macOS, you can also use:

```bash
shasum -a 256 -c SHA256SUMS
```

If the files are valid, you should see output similar to:

```text
pcbm-v1.0.0-rpi3-5.img.xz: OK
pcbm-v1.0.0-docs.zip: OK
```

If verification fails, delete the downloaded file and download it again from the official Project CBM GitHub Release.

## Flashing the Image

Use Raspberry Pi Imager, BalenaEtcher, or another imaging tool that supports `.img.xz` files.

Do **not** copy the `.img.xz` file to the SD card like a normal document. The image must be written to the card.

See the full guide:

- [End-User Guide](docs/end-user-guide.md)
- [Flashing the Image](docs/flashing-the-image.md)
- [Supported Hardware](docs/supported-hardware.md)
- [Checksums and Verification](docs/checksums-and-verification.md)
- [Troubleshooting](docs/troubleshooting.md)

## First Boot Defaults

| Item | Default |
|---|---|
| Linux user | `pi` |
| Default password | `cbm-ready` |
| Hostname | `pcbm` |
| Default Project CBM machine | Commodore 64 accurate/recommended emulator |
| Default emulator profile | `x64sc` |
| Project CBM content folder | `/home/pi/pcbm` |
| VICE emulator menu key | `F10` |
| SSH | Enabled by default |
| Samba file sharing | Enabled by default |
| WiFi | Intentionally left unconfigured |

After first boot, change the default password.

## Repository Layout

```text
README.md                 Project overview and quick start
LICENSE.md                License for Project CBM scripts and documentation
CHANGELOG.md              Project changelog
CONTRIBUTING.md           Contribution guidelines
SUPPORT.md                Support and issue-reporting guidance
docs/                     End-user documentation
release-notes/            Release-specific notes
checksums/                Archived checksum files by release version
screenshots/              Project screenshots and UI examples
```

## Releases

- [v1.0.0 Release Notes](release-notes/v1.0.0.md)
- [Changelog](CHANGELOG.md)

## License and Upstream Software

Project CBM scripts and documentation are provided under the license included in this repository.

The downloadable image contains upstream software with its own licenses, including Raspberry Pi OS, Debian packages, VICE, SDL2, and other tools. See [LICENSE.md](LICENSE.md) for details.

## Status

Project CBM v1.0.0 is the first public image release. It is usable, but still young enough to occasionally knock over a candle in the wizard tower.
