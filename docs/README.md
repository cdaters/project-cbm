# Project CBM documentation

These entry points describe the current private 1.1 implementation. A guide describes
intended behavior; only a hash-bound qualification record establishes a physical PASS.
See [current state](../CURRENT-STATE.md) for the candidate and exact owner procedure.

| Task | Authoritative guide |
| --- | --- |
| Flash, first boot, use Menu/VICE, content, USB and utilities | [User guide](release/user-guide.md) |
| Computer Name, owner credentials, SSH, sharing and discovery | [Networking and services](release/networking.md) |
| Understand release reproduction, derivatives and the private factory | [Build Your Own](release/build-your-own.md) |
| Understand pi-gen and the actual factory | [Factory guide](release/factory.md) |
| Change branding, defaults, content or packages | [Customization](release/customization.md) |
| Accounts, configuration and installed paths | [System layout](release/accounts-and-layout.md) |
| VICE source, packaging, profiles and performance | [VICE guide](release/vice.md) |
| Return to development after time away | [Developer entry](release/development.md) |
| Diagnose or recover an appliance | [User recovery](release/recovery.md) |
| Restore source/input/build records | [Engineering recovery](recovery.md) |
| Check model qualification | [Hardware status](supported-hardware.md) |

Canonical engineering contracts: [architecture](architecture.md),
[configuration](runtime/configuration-contract.md), [Covers](runtime/covers.md),
[security](security.md), [testing](testing.md), [build/release](build-and-release.md),
[environment boundary](build/environment-boundary.md) and [rights](provenance.md).
Dated build/qualification records are historical evidence and are never current
instructions merely because they once said READY. Current governance is in
[AGENTS](../AGENTS.md).

Historical 1.0 guides: [end-user guide](end-user-guide.md),
[flashing](flashing-the-image.md), [troubleshooting](troubleshooting.md),
[screenshots](screenshots.md), and [audit corrections](v1.0-current-notes.md).
The new guides replace their account/service/default advice for 1.1.

- [Content library and migration](release/content.md)
- [Boot presentation, timing and recovery](release/boot.md)
