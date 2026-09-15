# Project CBM Roadmap

Updated 2026-09-15. [ADR-0001](docs/adr/0001-base-distribution-and-image-architecture.md)
accepts the 1.1 foundation. [CURRENT-STATE](CURRENT-STATE.md) and the
[build handoff](docs/build-and-release.md#new-session-first-task) define the next
milestone. Architecture approval does not authorize implementation or publication.

## Project CBM 1.1 priorities, in order

1. **Reproducible-build foundation:** pinned Raspberry Pi OS Lite/arm64 pi-gen,
   small CBM stage, versioned VICE/Menu/TCPser packages, retained input/host/source
   closure, two clean builds, external release/provenance records and minimal
   installed identity. Full black-box project recovery stays in repositories/kits.
2. **Security and reliability:** image sealing, retry-safe first boot and expansion,
   fresh device identity, bounded privileges, coherent service/credential policy,
   safe imports, a shared validated launcher, non-destructive configuration and
   corrected packaging/version behavior. Implement as separately reviewable work.
3. **Qualification:** Pi 3 performance floor and 3A+ memory first; per-model graphics,
   audio/input, networking, storage, power-loss/retry, backup/restore and credential
   tests through Pi 500+. Measure system footprint and remaining user capacity;
   determine minimum storage empirically. No mandated 8 GB minimum.
4. **Bounded quality of life:** keyboard/controller guidance and reviewed profiles,
   clearer status/version/import feedback, reversible VICE settings, screenshots
   only after a working qualified capture path. These do not block the foundation.

## Existing behavior to retain

Console boot, Bash/dialog front panel, SDL2 VICE/ALSA, default-machine selection,
menu or direct-machine boot and return from emulator. Auto-launch is already present.

## Deferred pending concrete need and separate scope

Separate USERDATA partition, immutable/overlay root, system-preserving or A/B updater,
user scripting API, web administration, themes/catalogs/scrapers, screenshot galleries,
BBS directories and model-specific LED effects. Pi-specific optimization must preserve
the Pi 3 baseline. No new subsystem is implied by this list.

## Product boundaries

No desktop requirement, no general multi-platform emulation distribution, and no
unreviewed bundled content. Future redistribution follows per-asset rights review;
[historical content findings](docs/v1.0-current-notes.md#content-and-distribution-policy)
remain part of the record. 1.0.x receives important/security maintenance only;
no 1.0.1 is created or approved by this roadmap.
