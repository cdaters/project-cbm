# Changelog

All notable Project CBM changes should be documented here.

## [1.1.0-rc.4] - Private release-polish candidate

- Replace bundled StrikeTerm with a CCGMS-only disk containing the unchanged verified
  CCGMS 2021 program, source, BSD notice and attribution; unrelated compilation utilities
  are excluded. Add application-scoped VICE SwiftLink/IP232 options for existing TCPser.
- Discover G71 content and use compatible C64/C128 1571 routing; retain legitimate
  dot-prefixed supported content while excluding known host metadata.
- State the File Sharing password's colon restriction in its prompt.
- Distinguish Craig Daters' release-authorized branding/Covers from MIT code, record
  owner release policy and update user connection instructions and validation.
- Physical qualification is pending. No final release publication is implied.

## [1.0.0] - Initial Public Release

### Added

- Raspberry Pi OS Lite-based Project CBM image.
- Console-first boot experience.
- Project CBM menu system.
- Machine launch options for supported VICE Commodore emulators.
- Splash/cover screen support.
- Samba/network helper menu support.
- Content/import organization structure.
- PiShrink-compatible release process.
- First-boot filesystem expansion support.

### Notes

- First release image target: Raspberry Pi 3 through Raspberry Pi 5 / Pi 500.
- Project CBM was inspired in spirit by Carmelo Maiolino's Combian64 project, while being independently assembled as a Raspberry Pi OS Lite-based image using VICE, SDL2, and a custom Project CBM menu system.
- One of the goals of this release is to provide a current, ready-to-image Commodore emulation environment for newer Raspberry Pi systems, especially Raspberry Pi 5 and Raspberry Pi 500-class hardware.
- Distributed as compressed `.img.xz` through GitHub Releases.
