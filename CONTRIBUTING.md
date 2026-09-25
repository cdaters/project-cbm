# Contributing to Project CBM

Thanks for your interest in Project CBM.

Useful contributions include:

- Bug reports
- Tested hardware notes
- Controller mapping notes
- Documentation fixes
- Menu/script improvements
- VICE configuration improvements
- Compatibility reports for Pi 4-class and newer target models; qualify each model
  separately. Pi 3/Zero-class hardware is outside the 1.1 target.

## Bug Reports

Please include:

- Raspberry Pi model
- SD card size and brand if relevant
- Display connection type
- Keyboard/controller model
- Exact error text or screenshot
- Steps to reproduce

## Pull Requests

For scripts:

- Keep shell scripts POSIX/Bash-friendly where practical.
- Avoid hard-coding user-specific paths unless documented.
- Use clear comments.
- Prefer safe defaults.

## Image Releases

Large `.img`, `.img.gz`, and `.img.xz` files should not be committed to git.

Use GitHub Releases for image artifacts.

## Maintainer workflow

Read [AGENTS.md](AGENTS.md) and [CURRENT-STATE.md](CURRENT-STATE.md). Follow
[checks and qualification](docs/testing.md), update current state after meaningful
work, and use the [ownership/release contract](docs/build-and-release.md).
