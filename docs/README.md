# Project CBM 1.1.0 Documentation

Project CBM 1.1.0 is publicly released. Start with the user guides below; you do not
need factory or recovery-engineering knowledge to use the image.

## Start Here

- [Hardware and qualification](release/getting-started.md#hardware): Pi 4 B is physically qualified; other target models need separate qualification.
- [Download Project CBM 1.1.0](https://github.com/cdaters/project-cbm/releases/tag/v1.1.0).
- [Download and verify checksums](release/getting-started.md#download-and-check-the-image).
- [Flash the image](release/getting-started.md#flash-the-card), then follow [first boot](release/getting-started.md#first-boot).
- [End-User Manual](release/user-guide.md): keyboard navigation and everyday operation.

## Using Project CBM

- [Main Menu](release/user-guide.md#main-menu).
- [RUN / VICE basics](release/user-guide.md#run-and-vice-basics) and [Machines](release/user-guide.md#machines).
- [CONTENT and library layout](release/content.md) / [USB Import](release/content.md#usb-import).
- [CCGMS / TCPser BBS calls](release/networking.md#call-a-bbs-with-ccgms-2021): use **Swift / Turbo DE** with the shipped configuration.
- [FILES / Midnight Commander](release/user-guide.md#files-and-midnight-commander).
- [File Sharing](release/networking.md#file-sharing) / [SSH and SFTP](release/networking.md#remote-access).
- [Networking](release/networking.md) and [service controls](release/networking.md#services).
- [Troubleshooting](release/troubleshooting.md).
- [Safe shutdown](release/getting-started.md#your-first-c64-session) / [backup and user recovery](release/recovery.md).
- [Startup display](release/boot.md) and [customization](release/customization.md).

These guides describe **shipped 1.1.0 behavior**. USB preview/selection, explicit
USB browsing and Online Library belong to the accepted future design, not this image.

## Development / Reference

- [Developer guide](release/development.md) / [Contributing](../CONTRIBUTING.md).
- [Architecture](architecture.md), [configuration contract](runtime/configuration-contract.md) and [Covers](runtime/covers.md).
- [Build Your Own](release/build-your-own.md): the public initial bootstrap remains incomplete.
- [pi-gen factory](release/factory.md) / [build and release contract](build-and-release.md).
- [Software composition and licenses](release/software-components.md) / [VICE integration](release/vice.md).
- [Accounts and installed paths](release/accounts-and-layout.md).
- [Post-1.1 roadmap](design/post-1.1-roadmap.md) / [accepted content and Online Library design](design/content-ingestion-online-library.md).
- [Engineering recovery](recovery.md) / [testing](testing.md).

## Release Records / History

- [1.1.0 release notes](release/release-notes-1.1.0.md) / [verified publication record](build/published-1.1.0.json).
- [Final Pi 4 B owner qualification](qualification/final-1.1.0-pi4-owner-pass.json).
- [Current engineering checkpoint](../CURRENT-STATE.md): later work and links to retained qualification/recovery records.
- [Provenance](provenance.md) / [security history](security.md).
- [Historical screenshots](screenshots.md) / [current capture checklist](release/screenshot-checklist.md).
- [Historical documentation audit](documentation/release-readiness.md) and [bootstrap audit](documentation/public-bootstrap.md).
- [Historical 1.0 guide and corrections](v1.0-current-notes.md).

Dated audits, build attempts and qualification records preserve what was known at
that time. They are not the starting instructions for operating the current image.
