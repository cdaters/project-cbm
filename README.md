# Project CBM

Project CBM turns a Raspberry Pi into a keyboard-operated Commodore computer
collection. Switch it on, choose a machine, and arrive at BASIC or launch something
from your games, demos and programs. Machine artwork, called **Covers**, identifies
the computer as it starts. F10 → Quit brings you back to Project CBM.

Project CBM 1.1 is based on Raspberry Pi OS Lite (64-bit), using Debian 13 “Trixie”.
VICE supplies Commodore emulation; Project CBM adds the Menu, initial setup, content
library, USB import, network services and the integration that makes them work together.
Linux is still underneath, and you retain normal terminal and administrator access.
No cloud account is required.

**Project CBM 1.1 is a release candidate, not yet a published final release.**
[GitHub Releases](https://github.com/cdaters/project-cbm/releases) is the download
location. Check the version there: an older release has its own instructions.

## Hardware and machines

The 1.1 hardware target starts with Raspberry Pi 4 B and Pi 400, and includes Pi 5
and Pi 500-class systems where qualified. Pi 4 B has physical test evidence; that
does not establish equivalent qualification for every newer model. Pi 3 and Zero
families are outside 1.1 support. See [hardware guidance](docs/release/getting-started.md#hardware).

Choose C64, SuperCPU 64, C64 DTV, C128 in 40 or 80 columns, VIC-20, Plus/4, PET,
CBM-II or CBM-II 5x0. The [machine table](docs/release/user-guide.md#machines) explains
the choices. Bring software you have permission to use; a supported file format is
not permission to distribute its contents.

## Choose your starting point

| I want to… | Read this |
| --- | --- |
| Get from download to C64 BASIC | [Getting Started](docs/release/getting-started.md) |
| Learn the Menu and everyday tasks | [User Manual](docs/release/user-guide.md) |
| Add games or import a USB drive | [Content and USB](docs/release/content.md) |
| Copy from a Mac/PC or enable SSH | [Networking and services](docs/release/networking.md) |
| Build an image from source | [Build Your Own](docs/release/build-your-own.md) — includes current public-build gaps |
| Change Covers, defaults or software | [Customization](docs/release/customization.md) |
| Contribute code | [Development](docs/release/development.md) |
| Fix a problem or recover my files | [Troubleshooting](docs/release/troubleshooting.md) and [backup/recovery](docs/release/recovery.md) |

[All documentation](docs/README.md) includes the technical references. Product code
and Menu code live in [separate repositories](https://github.com/cdaters/project-cbm-menu).
See [LICENSE.md](LICENSE.md), [software and rights](docs/release/software-components.md)
and [acknowledgements](ACKNOWLEDGEMENTS.md) for attribution and third-party conditions.
Release engineering status belongs in [CURRENT-STATE.md](CURRENT-STATE.md).
