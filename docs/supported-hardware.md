# Supported Hardware

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
- Quality 16GB or larger microSD card
- HDMI display
- USB keyboard
- Official or high-quality power supply
- Ethernet for easiest first network setup

## Why Raspberry Pi 5 and Pi 500 Matter

One of the reasons Project CBM exists is to provide a ready-to-image Commodore emulation environment for newer Raspberry Pi hardware.

Earlier Commodore-focused Raspberry Pi distributions helped establish the appeal of a fast, appliance-style setup, but Project CBM specifically aims to include Raspberry Pi 5 and Raspberry Pi 500-class systems in its supported hardware target.

For best performance, Project CBM recommends Raspberry Pi 5 or Raspberry Pi 500, while still targeting Raspberry Pi 3 and Raspberry Pi 4 where practical.

## Optional Hardware

- USB gamepad/controller
- USB flash drive for importing games, demos, music, programs, or ROM files
- Ethernet cable

## Notes

- Controller behavior may vary by model.
- Pi 5 and Pi 500 are recommended for the smoothest experience.
- Pi 3 is the performance floor. Model-specific performance and compatibility require qualification; heavier profiles may have documented limits.
