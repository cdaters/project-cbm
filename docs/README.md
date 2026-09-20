# Project CBM documentation

Project CBM gives your Raspberry Pi a Commodore-focused front panel. Start at the
level you need; you do not need the build guides to use an image.

## Use Project CBM

- [Getting Started](release/getting-started.md): hardware, download, flash, first boot and C64 BASIC.
- [User Manual](release/user-guide.md): every Main Menu and CONTROL area, machines, VICE and common tasks.
- [Content and USB](release/content.md): where files belong, what launches and how import works.
- [Networking and services](release/networking.md): Wi-Fi, Computer Name, Mac/Windows sharing, SSH and BBS/modem.
- [Troubleshooting](release/troubleshooting.md): useful first steps when something goes wrong.
- [Backup, upgrades and recovery](release/recovery.md): protect your files and move to a new image.
- [Startup and recovery display](release/boot.md): expected artwork and advanced verbose boot.

## Build your own

- [Build Your Own](release/build-your-own.md): source, prerequisites, package commands and the current public-build limit.
- [pi-gen factory](release/factory.md): image recipe, standard stages, Linux host and official construction workflow.
- [Software composition](release/software-components.md): important components, exact package inventory and rights.
- [VICE integration](release/vice.md): Project CBM's emulator build, defaults, profiles and performance policy.

## Customize and develop

- [Customization](release/customization.md): worked changes to names, Covers, defaults, applications and packages.
- [Development](release/development.md): repository boundaries, interfaces, tests and release engineering.
- [Accounts and installed layout](release/accounts-and-layout.md): paths, permissions and what is safe to edit.
- [Screenshot checklist](release/screenshot-checklist.md): real screens still needed for the manual.

## Engineering references

The release guides describe current behavior. [CURRENT-STATE](../CURRENT-STATE.md)
tracks physical qualification and the current engineering checkpoint. [Documentation
readiness](documentation/release-readiness.md) records the public-build audit and
remaining release work.

Detailed contracts: [architecture](architecture.md), [configuration](runtime/configuration-contract.md),
[Covers](runtime/covers.md), [security](security.md), [testing](testing.md),
[build/release](build-and-release.md), [engineering recovery](recovery.md) and
[provenance](provenance.md). Dated build/qualification records preserve earlier results;
they are not instructions for operating the current release.

For Project CBM 1.0 use its [historical guide and corrections](v1.0-current-notes.md).
