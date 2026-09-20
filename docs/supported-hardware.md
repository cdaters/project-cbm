# Project CBM 1.1 hardware policy

The owner has selected **Pi 4-class hardware and newer** for Project CBM 1.1.
Targets are Raspberry Pi 4 B, 400, 5, 500 and 500+ where technically supportable;
each model requires separate qualification. Pi 3/Zero-class hardware is outside the
1.1 release target. Existing images and historical results are retained unchanged.

Attempt #8 has an [owner-reported Pi 4 B C64 performance PASS](qualification/poc4-attempt8-pi4-owner-report-2026-09-19.json)
for the private Donkey Kong reference with x64sc. The retained active non-warp interval
covers 145.219 seconds at weighted 100.002% speed. This is one workload, not blanket
qualification for every profile or newer Pi. The next physical target is Pi 4 B.
Pi 3 B+ performance failures remain valid historical evidence; no further Pi 3 tuning
or default-core downgrade is planned. OS support alone does not qualify Project CBM.

Use a suitable power supply, HDMI display and keyboard. Storage must hold the exact
raw image plus first-boot, maintenance and content headroom; no unsupported nominal
8 GB minimum is asserted. See [testing](testing.md) and [current status](../CURRENT-STATE.md).

## Historical policy and records (superseded for 1.1)

## Current performance release gate

Attempt #7 has an [owner-reported Pi 3 B+ real-time C64 failure](qualification/poc4-attempt7-pi3b-plus-performance-2026-09-18.json). Pi 3 remains the performance floor. The [correction and measurable qualification contract](runtime/c64-performance-2026-09-18.md) adds sustained emulation speed, audio/visual correctness and representative workloads to functional testing. No newer candidate has a physical performance PASS yet.

# Hardware Targets and Qualification

Project CBM v1.0.0 targets Raspberry Pi 3 through Raspberry Pi 5 and Pi 500-class systems.

## Target Raspberry Pi Models

- Raspberry Pi 3
- Raspberry Pi 4
- Raspberry Pi 400
- Raspberry Pi 5
- Raspberry Pi 500 (and 500+)

## Qualification status (2026-09-15)

The list above is a product target, not a completed hardware qualification claim.
Pi 3B/3A+/3B+, 4B/400, 5/500/500+ remain in scope where technically supportable.
Pi 3 is the performance floor; 512 MiB Pi 3A+ needs separate memory testing.
No physical Pi was tested by this audit/preservation work. Raspberry Pi OS support
alone cannot qualify Project CBM. See [testing and the audit matrix](testing.md).
Compute Modules and Zero 2 are not automatically included.

## Recommended Setup

- Raspberry Pi 5 or Pi 500 for best performance
- Quality storage sized for the image, first boot, maintenance margin and user content. The old 16 GB suggestion is not a qualified 1.1 minimum.
- HDMI display
- USB keyboard
- Official or high-quality power supply
- Ethernet for easiest first network setup

## Why Raspberry Pi 5 and Pi 500 Matter

One of the reasons Project CBM exists is to provide a ready-to-image Commodore emulation environment for newer Raspberry Pi hardware.

Earlier Commodore-focused Raspberry Pi distributions helped establish the appeal of a fast, appliance-style setup, but Project CBM specifically aims to include Raspberry Pi 5 and Raspberry Pi 500-class systems in its hardware target.

For best performance, Project CBM recommends Raspberry Pi 5 or Raspberry Pi 500, while still targeting Raspberry Pi 3 and Raspberry Pi 4 where practical.

## Optional Hardware

- USB gamepad/controller
- USB flash drive for importing games, demos, music, programs, or ROM files
- Ethernet cable

## Notes

- Controller behavior may vary by model.
- Pi 5 and Pi 500 are recommended for the smoothest experience.
- Pi 3 is the performance floor. Model-specific performance and compatibility require qualification; heavier profiles may have documented limits.

## Storage qualification

There is no mandated 8 GB card minimum. Determine minimum supported capacity from
measured final image size, first-boot needs and safe free-space margin, using actual
usable device bytes rather than nominal card labels. Publish compressed/raw image
sizes, installed system footprint and free user-data capacity after first boot.
See [ADR-0001](adr/0001-base-distribution-and-image-architecture.md).
