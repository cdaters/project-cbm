# pi-gen and the Project CBM factory

[Build Your Own](build-your-own.md) gives the commands. This page explains their inputs
and effects. The accepted base is Raspberry Pi OS Lite **arm64/Trixie** on writable
ext4, with logical separation of user content. Lite supplies supported Pi kernel,
firmware and Debian/Raspberry Pi packages without adding a desktop. See [ADR-0001](../adr/0001-base-distribution-and-image-architecture.md).

pi-gen constructs a target Linux filesystem from staged package/configuration steps,
then exports partitions into an image. Project CBM retains the exact arm64 pi-gen
commit, source archive and patches in its release lock. `construct_poc.py` extracts
those bytes and the Product integration source into a new build directory; it does
not consume an arbitrary current checkout. It runs stage0, stage1, stage2 and the
Product-owned `build/pigen/stage-cbm`. Earlier stages skip image export; the custom
stage supplies the appliance integration and final image.

The custom stage uses `tools/install_poc_stage.py`, installs exact Runtime/Menu/VICE/
TCPser packages and admitted optional inputs, configures accounts, restricted helpers,
services, content directories and first boot, then writes minimal installed identity.
Menu owns presentation; Product owns the shared lifecycle supervisor, privilege boundary,
registry, `pcbm-info`, configuration, first-boot readiness and image identity. Accounts
are initialized locally: no builder identity, factory password or host SSH key is copied.

## Two filesystems, two environments

On the qualified macOS route, Lima/VZ runs native arm64 Debian in plain mode. Its disk
is backed by external storage; `/srv/project-cbm` in the guest is ext4. Git sources
remain in normal source roots; large archives/images/evidence stay in the registered
external workspace. APFS is useful for retaining artifacts, not for building a Linux
rootfs: ownership, case, links, devices, xattrs and mount semantics matter. No host
shares, container stack or architecture translation substitutes for the capability gate.
A native arm64 Linux replacement must satisfy the same gates and exact host inventory;
it is an interface possibility, not a separately qualified host claim.

Builder temporary files and target temporary files are different. The target receives
a sanitized environment with local `/tmp`, never a builder TMPDIR path. `build_environment.py`
replaces inherited variables. AppArmor and package authentication remain enabled.
Changing host packages requires a new retained inventory/lock and revalidation.
Automatic update units are held under the builder-only guard; those settings are not
copied into the appliance. A drift failure stops the affected build, preserves it and
requires a distinct corrected attempt.

## What is frozen

One schema-4 release lock binds clean Product integration, independently tagged Menu,
component binary/corresponding source/recipe/build records, exact base binary and source
closure, authenticated repository metadata, pi-gen, patches, bootstrap/toolchain and
rights/admission records. `retained_inputs.py` verifies descriptors and actual retained
objects. URLs and caches are not input retention. Unchanged packages may be reused only
with their exact records and compatibility; changed source requires a new package version.

Construction runs root only inside an isolated Linux network namespace. A local frozen
APT transport serves authenticated retained bytes; no external routes or package
acquisition are permitted. Source acquisition and trust review happen before freezing.
The installed image carries a small offline-readable identity, not the complete lock,
source archives or builder cache. Image hashes and later evidence stay outside it,
preventing a checksum cycle.

## Outputs and proof

For POC4 attempt N, work lives in `builds/private-poc4-attempt-N`, and compressed output
in `artifacts/private-poc4-attempt-N`. pi-gen exports the raw image in
`work/export-image`; current configuration exports XZ at level 3. Exact names come from
`build/pigen/config.json`. Never replace an existing attempt directory, package, lock
or tag. Raw size, compressed size and SHA-256 are separate records. Hashing decompressed
XZ must equal the raw hash before and after transfer.

Actual-image checks use read-only loop devices and `ro,noload` ext4 inspection. They
check filesystems, packages and ELF dependencies, identity, privilege/service/account
configuration, installed source/assets/docs and lifecycle contracts. Native tests cover
actual Linux boundaries in a disposable isolated overlay. Neither proves visible Covers,
Pi input, Wi-Fi radio or another computer's discovery. Physical qualification binds
reported behavior to the exact image hash and model.

A successful controlled build is **not proof of bit-for-bit reproducibility**. That
claim needs independent clean builds from identical declared inputs, comparison and
explanation of differences. Recovery retains bundles, refs/tags, input objects, packages,
image records and evidence; offline restore/ref/fsck checks establish retrievability.
Independent backup custody remains separate from another folder on the same drive.

## Read the actual stage recipe

The pinned pi-gen revision is
`6fcca44892d5d4b36f826d2b8fb16d716369fada` from its `arm64` branch. The retained source
archive SHA-256 is `74f622d712847674f28763cbdcfae4b00909589305b30ad5df01846d8e003d33`.
The lock pins the commit and archive; the branch name alone is not a pin. pi-gen executes
numbered scripts/package lists in each selected stage. A later stage starts from the
previous stage's filesystem, applies its changes and can request an image export.

| Stage | Contribution in this pinned recipe |
| --- | --- |
| `stage0` | Bootstrap the arm64 Debian filesystem and APT configuration; install Raspberry Pi archive trust material, locales, initramfs/firmware and Pi kernel packages |
| `stage1` | Basic system/network adjustments, `raspi-config`, `netbase` and time synchronization |
| `stage2` | Raspberry Pi OS Lite userland: console/keyboard setup, SSH tooling, networking/Wi-Fi firmware, NetworkManager, Avahi, storage/USB utilities and Pi-specific system utilities |
| `stage-cbm` | Install Project CBM packages and admitted applications; configure accounts, restricted operations, first boot, session lifecycle, content and identity; seal and export the appliance |

Upstream Lite also brings some tools not wanted in the appliance. The CBM installer
purges compiler/development payload, cloud-init and excluded remote-connect software,
then verifies that runtime packages remain installed. “Based on Lite” therefore does
not mean every upstream Lite package is retained unchanged. `linux-image-rpi-v8` and
`linux-image-rpi-2712` support the base's different Pi generations; their presence is
not a performance qualification for each model.

| Recipe file | What to change there |
| --- | --- |
| `build/pigen/config.json` | Image name/date, architecture/suite, selected stages, locale/keyboard/timezone bootstrap defaults and compression |
| `build/pigen/defaults.json` | Declared appliance defaults/contract; changes must agree with the actual installer and frozen configuration |
| `build/pigen/stage-cbm/prerun.sh` | Copy the previous stage root when creating the custom stage |
| `build/pigen/stage-cbm/00-cbm/00-run.sh` | Invoke the Product installer with the exact lock, input kit and target root |
| `build/pigen/stage-cbm/EXPORT_IMAGE` | Request the final custom-stage image export |
| `build/pigen/stage-cbm/files` | First-boot coordinator, getty/profile/session integration, launch diagnostics and service units |
| `tools/install_poc_stage.py` | Target package installation, account creation, configuration, optional input installation and sealing |
| `tools/construct_poc.py` | Verify frozen inputs/host, prepare a fresh pi-gen tree, apply retained patches, configure frozen transport and run construction |
| `build/pigen/target-environment.patch` | Enforce the builder/target environment boundary |
| `build/pigen/frozen-export.patch` | Keep export package acquisition inside the retained-input process |
| `build/pigen/exclude-connect.patch` | Remove the unselected remote-connect component from upstream package selection |

`construct_poc.py` marks stage0/1/2 with `SKIP_IMAGES`, copies the custom stage into
pi-gen, and selects `stage0 stage1 stage2 stage-cbm`. `ROOTFS_DIR` is the target being
constructed, not the builder's `/`. The custom script passes it to the guarded installer,
which refuses `/` and requires a prepared Debian target. Package maintainer scripts run
inside that target with a sanitized environment; services are prevented from starting
as if the builder were the appliance. Final sealing removes temporary package inputs,
sets identity/account/service initial state and leaves user choices for first boot.

## Deliberate package composition

| Group | Examples and purpose |
| --- | --- |
| Debian/Raspberry Pi OS base | systemd, PAM, Bash/coreutils, locales, keyboard/console setup, filesystem and device tools |
| Raspberry Pi integration | Pi kernels, `raspi-firmware`, `raspberrypi-sys-mods`, `raspi-config`, `raspi-utils`, Wi-Fi/Bluetooth firmware |
| Front panel | `dialog`, Python 3, ALSA utilities, Midnight Commander (`mc`), SDL2 and SDL2_image for Covers |
| Emulator graphics/audio | SDL2, ALSA, DRM/GBM, EGL/OpenGL/GLES and Mesa; dynamically loaded graphics libraries are included in closure checks |
| Network services | NetworkManager/iproute2, OpenSSH server, Samba, Avahi, rsync; installation does not mean the optional listener is enabled |
| Project-built packages | `project-cbm-runtime`, `project-cbm-menu`, `project-cbm-vice`, `project-cbm-tcpser` |
| Optional payloads | Admitted SID-Wizard; private StrikeTerm admission remains separate from public redistribution rights |
| Original qualification media | Small Project CBM-generated smoke/input/SID checks; owner reference games/demos/music are not automatically included |

`build/packages/*/debian/control` and Menu's `debian/control` declare direct package
dependencies. The installer adds its explicitly selected utilities; pi-gen's package
lists supply the base. The lock's `base.binary_package_closure` and
`base.source_package_closure` retain exact dependency bytes, not merely package names.
Host build dependencies are a separate closure and are not copied into the image.
Unchanged Project-built packages can be reused with exact hashes and compatibility
checks. Reuse is a provenance choice, not a different class of installed software.

The authoritative **installed** package manifest is `offline/packages.tsv` produced
by `tools/validate_poc_image.py` for each actual image. It records package, version and
architecture and is checked against retained `.deb` artifacts. The candidate's build
report locates that manifest and closure result. It is separate from the acquisition
closure, which may also include build-time or later-purged packages. On your own running
appliance, generate the corresponding machine-readable inventory with:

```sh
dpkg-query -W -f='${binary:Package}\t${Version}\t${Architecture}\n' > packages.tsv
```

Keep that file with your image hash and build record. Public release distribution needs
to include the exact manifest and public input catalog alongside the release; the
private engineering kit is not presumed available to someone reading GitHub.

For a portable JSON inventory tied to the exact raw image, export the validator TSV:

```sh
python3 tools/package_manifest.py "$CBM_EVIDENCE/offline/packages.tsv" \
  --image-sha256 "$CBM_RAW_SHA256" "$CBM_EVIDENCE/packages.json"
```

This read-only conversion rejects malformed/duplicate installed entries, records the
inventory hash, and refuses to overwrite an existing output. The validator TSV has five
columns: package, version, architecture, installed size in KiB and dpkg status. Its JSON
projection includes installed entries only. Neither file contains account or network
credentials. Publish it with a release when publication is authorized; it is useful
without access to private engineering storage.
