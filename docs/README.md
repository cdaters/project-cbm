# Project CBM Documentation

Welcome to the Project CBM documentation folder.

These guides are written for users who want to download, verify, flash, boot, and use Project CBM without needing to build a Raspberry Pi system from scratch.

Project CBM is intended to behave like a small Commodore-focused appliance:

> Power on. Boot fast. No desktop required. Just Commodore.

## Start Here

If you are new to Project CBM, read these in order:

1. [Supported Hardware](supported-hardware.md)  
   Make sure your Raspberry Pi model and basic hardware setup are supported.

2. [Checksums and Verification](checksums-and-verification.md)  
   Verify that your downloaded release files are complete and unmodified before flashing.

3. [Flashing the Image](flashing-the-image.md)  
   Write the Project CBM `.img.xz` release image to a microSD card.

4. [End-User Guide](end-user-guide.md)  
   Learn how to boot Project CBM, use the menu system, launch Commodore machines, import files, use Samba sharing, and adjust basic settings.

5. [Troubleshooting](troubleshooting.md)  
   Use this if something does not work as expected.

## Documentation Index

| Guide | Purpose |
|---|---|
| [End-User Guide](end-user-guide.md) | The main user manual for Project CBM. Covers first boot, menu usage, machines, content folders, import tools, networking, Samba, SSH, boot modes, and legal notes. |
| [Flashing the Image](flashing-the-image.md) | Explains how to write the Project CBM release image to a microSD card using Raspberry Pi Imager, BalenaEtcher, or Linux command-line tools. |
| [Checksums and Verification](checksums-and-verification.md) | Explains how to verify downloaded Project CBM release files using `SHA256SUMS`. |
| [Supported Hardware](supported-hardware.md) | Lists supported Raspberry Pi models and recommended hardware. |
| [Screenshot Gallery](screenshots.md) | Shows Project CBM v1.0.0 menus, splash screen, control panel, network screen, system screen, and VICE emulator examples. |
| [Troubleshooting](troubleshooting.md) | Common fixes for menu, emulator, network, Samba, WiFi, USB import, and command-line issues. |

## Quick Download Checklist

From the Project CBM GitHub Release, download:

```text
pcbm-v1.0.0-rpi3-5.img.xz
pcbm-v1.0.0-docs.zip
SHA256SUMS
```

Then verify the downloaded files before flashing.

Linux / Raspberry Pi OS:

```bash
sha256sum -c SHA256SUMS
```

macOS:

```bash
shasum -a 256 -c SHA256SUMS
```

If verification succeeds, you should see output similar to:

```text
pcbm-v1.0.0-rpi3-5.img.xz: OK
pcbm-v1.0.0-docs.zip: OK
```

## Quick Flashing Reminder

The Project CBM release image is a complete Raspberry Pi system image.

Do not copy the `.img.xz` file to the SD card like a normal document.

Use an imaging tool such as:

- Raspberry Pi Imager
- BalenaEtcher
- `dd` on Linux, for advanced users

See [Flashing the Image](flashing-the-image.md) for details.

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

## Legal Note

Project CBM does not include or distribute copyrighted ROMs, commercial software, disk images, or game collections.

Users are responsible for making sure they have the legal right to use any ROMs, games, demos, music, programs, or disk images they add.

Freeware, public domain software, homebrew projects, and user-owned backups are the safest places to begin.

## For Developers and Contributors

This documentation describes the public Project CBM v1.0.0 release.

For project history and future plans, see:

- [Release Notes](../release-notes/v1.0.0.md)
- [Changelog](../CHANGELOG.md)
- [Roadmap](../ROADMAP.md)
- [Contributing](../CONTRIBUTING.md)
- [Support](../SUPPORT.md)
