[![Project CBM 1.2.0](https://img.shields.io/badge/release-1.2.0-blue)](https://github.com/cdaters/project-cbm/releases/tag/v1.2.0) [![Platform: Raspberry Pi arm64](https://img.shields.io/badge/platform-Raspberry%20Pi%20arm64-C51A4A)](docs/release/getting-started.md#hardware) [![Code license: MIT](https://img.shields.io/badge/code%20license-MIT-orange)](LICENSE.md)

<p align="center">
  <img src="assets/images/project-cbm-header.png" alt="Project CBM" width="100%">
</p>

# Project CBM

Project CBM turns a Raspberry Pi into a keyboard-operated Commodore computer
collection. Switch it on, choose a machine, and arrive at BASIC or launch your
games, demos and programs. Machine artwork, called **Covers**, identifies the
computer as it starts. **F10 → Quit** brings you back to Project CBM.

Built on Raspberry Pi OS Lite (64-bit), based on Debian 13 “Trixie”, with SDL2 VICE
and a Bash/dialog Menu. No desktop or cloud account is required. You retain normal
Linux terminal and administrator access.

## Current Release

**Project CBM 1.2.0 is released.** [Release page and notes](https://github.com/cdaters/project-cbm/releases/tag/v1.2.0).
The exact released image passed all five focused Raspberry Pi 4 B checks: USB
browsing, Guided Import, RUN, direct boot and Assembly64. Earlier qualification
records retain the broader lifecycle and screenshot testing.

## What's new in 1.2

**Assembly64 Online Library** brings search and downloads to **CONTENT → Online
Library**. Find software, narrow results with filters, read details, choose files
and save them to your local library. Saved software stays available offline.
[How to use Assembly64](docs/release/online-library.md).

- **Import files from USB:** choose a folder, scan, select supported files, review
  the destination and import. Unsupported files are explained.
- **Browse a USB drive safely:** FILES → USB Drive opens Midnight Commander with
  a read-only source. Copy what you need, press F10, then Safe Unmount.
- **Take screenshots from SSH:** `pcbm-screenshot` saves Menu, MC, Cover and supported
  VICE/gameplay pictures in `/home/pcbm/content/screenshots/`.
- **Choose your startup:** open Menu or start the current RUN machine directly,
  with normal Cover presentation and F10/Quit return.
- Clearer file sizes, Back/Parent navigation, duplicate handling and friendly labels.

[Read the 1.2 release notes](docs/release/release-notes-1.2.0.md) or start with the
[download and setup guide](docs/release/getting-started.md).

**Powered by Assembly64** — [official website](https://assembly64.hackerswithstyle.se).
Assembly64 is an independent external service, not owned by Project CBM. Optional
[PayPal](https://www.paypal.com/donate/?hosted_button_id=8D6YK9LXULYPE) and
[Ko-fi](https://ko-fi.com/assembly64) links support its team. Project CBM bundles no
Assembly64 collection. Bring or download only software you are entitled to use.

## What Is Included

- VICE 3.10 and eleven profiles covering C64, SuperCPU 64, C64 DTV, C128
  (40/80 columns), VIC-20, Plus/4, PET and the CBM-II families.
- Guided first boot, keyboard Menu and machine Covers.
- Organized local library, guided USB import and separate read-only USB browsing.
- CCGMS 2021 for BBS calls through TCPser and SID-Wizard for creating music.
- Midnight Commander, optional file sharing, SSH and network discovery.

## Hardware Support

**Raspberry Pi 4 B is physically qualified for this release.** Pi 400, Pi 5 and
Pi 500-class systems are targets requiring separate model qualification. Pi 3 and
Zero-class hardware are outside the 1.2 target. See [hardware and setup requirements](docs/release/getting-started.md#hardware).
A supported machine profile is not a claim that every workload or peripheral has
been tested.

## Screenshots

These retained **1.0.0** images illustrate the project's appearance; they are not
screenshots of 1.2.0. Menu labels and behavior have changed. No replacement screens
have been fabricated.

<img src="screenshots/v1.0.0/02-main-menu.png" alt="Historical Project CBM 1.0.0 Main Menu" width="480">
<img src="screenshots/v1.0.0/09-vice-c64-startup.png" alt="Historical C64 Cover artwork, not an emulator screenshot" width="320">

[Historical gallery](docs/screenshots.md) · [Current screenshot capture checklist](docs/release/screenshot-checklist.md)

## Download

- [Project CBM 1.2.0 compressed image — project-cbm-1.2.0.img.xz](https://github.com/cdaters/project-cbm/releases/download/v1.2.0/project-cbm-1.2.0.img.xz)
- [SHA256SUMS](https://github.com/cdaters/project-cbm/releases/download/v1.2.0/SHA256SUMS)
- [All release assets, source archives, notices and inventory](https://github.com/cdaters/project-cbm/releases/tag/v1.2.0)

Verify the compressed image before flashing. Its SHA-256 is:

```text
b2b7836f752d4b5b3a9a7cd5116776dff8f19eceaf4ad155b9541cc2efb69b5d
```

The download is 599,119,848 bytes and expands to a 3,095,396,352-byte image.
Allow additional space for setup, updates and your library. The raw image is not a
public asset; extract the XZ only if your imaging tool needs it. GitHub's source
ZIP/TAR files are not bootable images.

## Getting Started / Documentation

| Task | Read this |
| --- | --- |
| Verify, flash and reach C64 BASIC | [Getting Started](docs/release/getting-started.md) |
| Learn everyday Menu tasks | [User Manual](docs/release/user-guide.md) |
| Add content or import USB files | [Content and USB](docs/release/content.md) |
| Share files, enable SSH or call a BBS | [Networking and services](docs/release/networking.md) |
| Fix a problem or protect your files | [Troubleshooting](docs/release/troubleshooting.md) and [backup/recovery](docs/release/recovery.md) |

[Documentation index](docs/README.md) · [Support](SUPPORT.md)

## Development / Repository Layout

Product owns OS/runtime integration, image construction and authoritative user
documentation. [Project CBM Menu](https://github.com/cdaters/project-cbm-menu) owns
Menu presentation, scripts, artwork and its independently versioned package.
The 1.2 development branch is `feature/1.2-content-ingestion`;
`main` is retained as historical repository history.

- `runtime/`: appliance integration and validated operations.
- `build/`, `tools/`, `tests/`: factory recipes, engineering tools and checks.
- `docs/release/`: current user and developer guides.
- `docs/design/`: design decisions and future work.

Start with [Development](docs/release/development.md), [Contributing](CONTRIBUTING.md)
or [Build Your Own](docs/release/build-your-own.md). The public first-build bootstrap
is not yet complete; a published image is not a claim of independent reproducibility.

## Roadmap

Assembly64, guided USB import, read-only USB browsing, SSH screenshots and startup
improvements are implemented for 1.2. Future work includes more hardware testing,
one-step Save & Run, and improved public build tooling. [Roadmap](docs/design/post-1.1-roadmap.md).

## License / Upstream Software

Project-owned code and documentation use [MIT](LICENSE.md). Upstream software,
artwork and supplied content have their own terms; the MIT badge is not a blanket
license for the image. See [software and rights](docs/release/software-components.md),
[release policy](docs/release/release-policy.md) and [acknowledgements](ACKNOWLEDGEMENTS.md).

## Project History / Maintainer Records

[Current engineering checkpoint](CURRENT-STATE.md) · [Architecture](docs/architecture.md)
· [Provenance](docs/provenance.md) · [Security history](docs/security.md)
· [Engineering recovery](docs/recovery.md) · [Historical 1.0 notes](docs/v1.0-current-notes.md).
These preserve earlier audits and qualification evidence without replacing current
user instructions.

The immutable Product `v1.2.0` tag identifies the frozen binary-source snapshot.
Later repository documentation records clarifications and engineering work;
[publication identities](docs/build/published-1.2.0.json) and the release manifest
record the exact release source/documentation snapshots.
