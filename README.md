# Project CBM

Project CBM is a keyboard-driven Commodore appliance for Raspberry Pi, built from
Raspberry Pi OS Lite arm64, SDL2 VICE, ALSA and a Bash/dialog Menu. It preserves user
control, a reliable console/emulator lifecycle and an independently recoverable image
factory. Pi 3 is the performance floor; each model requires its own qualification.

**1.1 is in private release-readiness refinement, not a public release.** Start with
[the documentation](docs/README.md). [CURRENT-STATE](CURRENT-STATE.md) identifies the
exact current candidate, qualification, remaining work and recovery checkpoint.

| I want to… | Start here |
| --- | --- |
| Use Project CBM | [User guide](docs/release/user-guide.md) |
| Configure networking and services | [Connection guide](docs/release/networking.md) |
| Add my content | [Content and utilities](docs/release/user-guide.md#content-and-utilities) |
| Build Project CBM | [Build Your Own](docs/release/build-your-own.md) |
| Customize my image | [Customization](docs/release/customization.md) |
| Develop Project CBM | [Developer entry](docs/release/development.md) |
| Troubleshoot or recover | [Recovery help](docs/release/recovery.md) |

The Product repository owns OS/runtime integration, image construction, qualification,
rights and recovery. The independently versioned [Menu repository](https://github.com/cdaters/project-cbm-menu)
owns presentation, scripts, Covers and UI packaging. Project CBM is independently
assembled and is not a fork of Combian64; see [acknowledgements](ACKNOWLEDGEMENTS.md).

Project source licensing is in [LICENSE.md](LICENSE.md). Upstream software and third-party
content keep their own licenses. Private input admission is not public redistribution
permission; see [provenance](docs/provenance.md) and [optional applications](docs/runtime/optional-applications-contract.md).

The historical v1.0.0 release remains documented in [corrected historical notes](docs/v1.0-current-notes.md)
and [release notes](release-notes/v1.0.0.md). Its inherited accounts/content/service
defaults are not 1.1 defaults. Do not use old instructions to initialize a 1.1 image.
