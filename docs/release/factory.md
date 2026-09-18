# pi-gen and the Project CBM factory

[Build Your Own](build-your-own.md) gives the commands. This page explains their inputs
and effects. The accepted base is Raspberry Pi OS Lite **arm64/Trixie** on writable
ext4, with logical separation of user content. Lite supplies supported Pi kernel,
firmware and Debian/Raspberry Pi packages without adding a desktop. This is not a
Bookworm lineage or a read-only kiosk. See [ADR-0001](../adr/0001-base-distribution-and-image-architecture.md).

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
