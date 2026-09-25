# How pi-gen builds Project CBM

[Documentation index](../README.md) · [Build Your Own](build-your-own.md)

Raspberry Pi OS is created with a build system called **pi-gen**. Project CBM uses it
to start with Raspberry Pi OS Lite, add its software/configuration, and produce a bootable
SD-card image. Instead of installing a desktop and launching a program inside it, the
Pi logs into the Project CBM console Menu. VICE uses the graphics/audio stack directly.

A **stage** is a group of build steps applied to the future Pi filesystem. That filesystem
is a directory on the Linux builder until export turns it into partitions in an image.
Commands on the builder and commands inside that target are different: confusing them
can change the build computer instead of the image.

## Base and stages

Project CBM 1.1 uses Raspberry Pi OS Lite 64-bit, Debian 13 Trixie, with the pinned arm64
pi-gen commit `6fcca44892d5d4b36f826d2b8fb16d716369fada`. A pin means later upstream
changes are not silently substituted. The current recipe is described by
`build/pigen/config.json`; older names in source-selection tools do not define the current
product version. [Software composition](software-components.md) lists the package choices.

| Stage | What it contributes in the pinned source |
| --- | --- |
| stage0 | Bootstraps Debian with debootstrap, sets up package repositories/keyring and locale, installs initramfs/raspi-firmware and Pi v8/2712 kernel packages |
| stage1 | Basic system/network adjustments, raspi-config, netbase and systemd time synchronization |
| stage2 | Raspberry Pi OS Lite console/userland, keyboard setup, SSH tools, NetworkManager/Wi-Fi firmware, Avahi, USB/storage and Pi utilities; no desktop stage is selected |
| stage-cbm | Project CBM's own packages, content, account/session, first boot, service policies, artwork integration and installed build information |
| export-image | Creates partitions/filesystems, generates final initramfs images, copies the target and exports/compresses the SD image |

Project CBM marks stage0/1/2 to skip their image exports and exports only stage-cbm.
Cloud-init setup is disabled; Project CBM owns first boot. The recipe excludes
rpi-connect-lite and removes selected development payload before final export. Upstream
stage package lists therefore are not the final installed package manifest.

## The Project CBM recipe

These are real repository paths. Most personal changes affect a few files, not the whole tree.

```text
project-cbm/
  build/
    host/
      lima.yaml                 # Mac's Linux VM allocation; build host only
      inputs.json               # Pinned bootstrap downloads
      build-packages.list       # Linux image-build tools
      capability-gate.sh        # Checks the build environment
    packages/
      runtime/debian/            # Runtime package metadata/install recipe
      vice/debian/               # VICE build flags, patches and dependency declarations
      tcpser/debian/             # TCPser package recipe
      build_candidate.sh        # Current changed-package factory helper
    pigen/
      config.json               # Image name/date, base, stages, initial locale/timezone
      defaults.json             # Declared appliance defaults and hardware policy
      frozen-export.patch       # pi-gen export changes for preserved inputs
      target-environment.patch  # Keeps builder environment out of target operations
      exclude-connect.patch     # Excludes the unneeded remote-connect package
      stage-cbm/
        prerun.sh               # Copies the preceding target filesystem
        00-cbm/00-run.sh         # Calls Product's target installer
        EXPORT_IMAGE            # Export filename suffix
        files/                  # First boot, getty/profile, launch/splash and modem integration
  runtime/
    data/profiles.json          # Machines exposed to Menu
    project_cbm/                # Information, preferences, configuration, import and setup
    config/                    # Policy, sudo and File Sharing templates
    bin/                       # Public command entry points
    libexec/                   # Fixed privileged entry points
  tools/
    install_poc_stage.py        # Applies stage-cbm to ROOTFS_DIR
    construct_poc.py            # Verifies inputs, prepares pi-gen and invokes build.sh
    freeze_private_candidate.py # Records a new private input set from a predecessor
    retained_inputs.py         # Checks retained files and metadata
    vice_presentation.py       # Generates initial VICE resources
    validate_poc_image.py       # Checks actual image contents
    package_manifest.py        # Exports exact installed package inventory
project-cbm-menu/
  scripts/                     # Menu, CONTENT, IMPORT, CONTROL and shared launch entry
  lib/                         # Dialog/status/setup and artwork presentation helpers
  covers/                      # Primary artwork and seven machine Covers
  debian/                      # Independently versioned Menu package
```

`stage-cbm/00-cbm/00-run.sh` calls `tools/install_poc_stage.py` with the release lock,
input directory and pi-gen's `ROOTFS_DIR`. The installer copies the four component `.deb`
files into target-local `/tmp`, installs them and deliberate system dependencies, checks
installed versions, then applies appliance configuration. **There is no stage-cbm
00-packages list in this recipe**: explicit extra installation is in the Python installer,
while component dependencies live in their Debian `control` files.

The constructor renders pi-gen variables for `stage0 stage1 stage2 stage-cbm`, Trixie,
arm64, `FIRST_USER_NAME=pcbm`, no cloud-init/SSH/passwordless general sudo, and XZ level 3
compression. It copies stage-cbm into the pinned pi-gen tree and calls that tree's
`./build.sh`. Do not invoke stage-cbm by itself against an arbitrary root directory;
it requires the matching Product packages, policy and input record.

## What stage-cbm configures

The normal account is pcbm, UID 1000, `/home/pcbm`; the library is `/home/pcbm/content`.
Root stays root. The installer sets Computer Name `projectcbm`, prepares user directories
and absent-only VICE settings, and installs restricted helpers and normal authenticated
administration. No universal password or developer SSH key is copied into the image.

The Linux getty/login/PAM session enters `pcbm-console-session`. The unprivileged boot
supervisor displays primary artwork while the next screen prepares. First boot handles
region, administrator password and networking. `pcbm-first-boot.service` owns filesystem expansion
and first-boot system preparation, avoiding competing expansion/setup mechanisms.
The [layout reference](accounts-and-layout.md) identifies installed paths and units.

NetworkManager owns connections. SSH, Samba, Avahi and TCPser are installed with explicit
setup/enable policy. File Sharing exports only the library. Runtime reports actual state;
Menu formats it. Optional applications are installed from explicit verified sources and
working-copy locations, not downloaded opportunistically during first boot.

## Why Linux storage and clean inputs matter

Build work uses ext4: Linux permissions, symlinks, device nodes and mounts must behave as
they do on the Pi. macOS APFS holds archives/images well but does not serve as the target
root filesystem. The qualified VM has no shared host filesystem and no container stack.
Builder temporary files and target `/tmp` are kept separate; the target environment is
sanitized so a Mac/VM temporary-directory variable cannot break programs inside it.

Before official construction, the project saves actual source archives, packages and
repository authentication metadata, not just download URLs. A release lock records their
versions and hashes. The builder serves those saved packages through a local APT transport
inside a network-isolated build, preventing changes in Internet mirrors from altering the
result. Acquiring inputs is a separate earlier step. Builder package inventory/update guards
catch unexpected toolchain changes; they are build-host controls, not appliance settings.

These extra records support debugging and later rebuilds. They do not make a private input
kit publicly available. [Public-bootstrap status](../documentation/public-bootstrap.md)
explains what must be supplied before a new public user can assemble a complete image.

## Outputs and verification

The current constructor derives a directory from the candidate's private identity and
optional attempt argument, then creates a new `builds/<directory>`; it refuses to overwrite
existing work. It places extracted `pi-gen` and `project-cbm` recipes there, with pi-gen
work under `work/` and raw output under `work/export-image/`. `DEPLOY_DIR` points to
`artifacts/<directory>` for compressed image/export information. The generated pi-gen
`config` gives the exact paths. The filenames derive from `image_name`, `image_date`
and stage-cbm's `EXPORT_IMAGE` suffix, not a guessed version string.

The ordered commands are in [the official walkthrough](../build/official-factory-walkthrough.md).
Actual-image validation reads the finished partitions, package list, ELF dependencies,
accounts/services, first boot, lifecycle files and minimal installed identity. The raw
hash is compared with the decompressed XZ hash. The full release lock/source collection
stays outside the appliance; `/usr/share/project-cbm/identity.json` is the small installed
record linking it to the build. Image hashes are recorded afterward so they do not create
a circular checksum dependency.

A successful offline build still needs physical tests for display, keyboard, audio,
networking and performance. Rebuilding independently from the same inputs and comparing
results is needed to demonstrate reproducibility; the project does not infer that proof
from one successful build. [Developer recovery](development.md#release-and-recovery)
explains preservation without making it a prerequisite for ordinary appliance use.
