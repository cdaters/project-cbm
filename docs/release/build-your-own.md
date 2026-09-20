# Build Your Own Project CBM

Project CBM turns a Raspberry Pi into a keyboard-operated Commodore appliance. The
image combines Raspberry Pi OS Lite arm64, a separately packaged VICE emulator suite,
a Bash/dialog front panel, and Product-owned setup, configuration and lifecycle code.
Project CBM 1.1 uses **Debian 13 (Trixie)** through Raspberry Pi OS. A desktop is not
required: SDL2 presents the emulator directly through the Linux graphics stack, and
ALSA supplies audio. The writable ext4 filesystem keeps normal Linux administration
available while organizing appliance content and preferences separately.

Start with [the image recipe](factory.md), [accounts and installed layout](accounts-and-layout.md)
and [VICE](vice.md). This page then tells you which build route is possible and gives
the actual private factory commands. You do not need a previous session or the original
developer's disk to understand the recipe.

## Three different build objectives

| Objective | Inputs you need | What the result establishes |
| --- | --- | --- |
| Reproduce a released version | Published exact source refs, release lock, retained binary/source closure, recipes/patches, host/bootstrap identity and rights-cleared assets | A build of the declared release inputs; bit-for-bit reproducibility still needs independent comparison |
| Make your own derivative | Your selected source/recipe, legally usable assets, newly authenticated package closure and your own lock/identity | Your own image, requiring your own validation and hardware qualification |
| Continue private frozen engineering | The complete verified predecessor kit plus changed committed sources/packages | A distinct private candidate; predecessor objects are reused without substituting current mirror packages |

**Public bootstrap status:** the current implementation can build and validate private
frozen candidates, but Project CBM 1.1 does not yet provide a published complete public
input kit or a general first-lock bootstrap command. A private predecessor kit is not
publicly available merely because this guide mentions it. The public completion work is
specific: publish the chosen Product/Menu refs and component/corresponding-source
artifacts; supply authenticated exact Debian/Raspberry Pi binary and source closure and
metadata or a documented acquisition catalog; distribute the approved host/bootstrap
inputs and manifest; resolve or replace private-only artwork/optional inputs; and provide
an initial-lock assembler that does not assume `frozen-poc4-attemptN`. The current
`freeze_private_candidate.py` deliberately operates on verified predecessors and private
version families. It is not the public bootstrap implementation.

Those gaps do not hide how the image is made. The complete integration recipe, package
recipes, schemas and validators are in this repository. The following sections explain
how to edit and construct components today, and where the existing frozen image workflow
begins. Do not describe a fresh build against today's mirrors as a reproduction of an
older exact image. A derivative may deliberately choose new dependencies, but must record
that selection and validate a new identity.

## Get oriented in the source

Keep the repositories as siblings. Product owns OS integration, Runtime, profiles,
package recipes, image locks, build/validation tools and this documentation. Menu owns
its scripts, dialog presentation, Covers, helper modules and Debian packaging. Their
versions are independent; the image lock pins the exact Menu tag object, commit and
package hash. Updating Product never means automatically consuming Menu's latest branch.

```sh
git clone https://github.com/cdaters/project-cbm.git
git clone https://github.com/cdaters/project-cbm-menu.git
```

For a released build, use the exact refs supplied with that release. A generic branch
checkout is useful for reading/development, but is not a release identity. There is no
published 1.1 release tag implied by these examples. Read `build/pigen/config.json`,
`tools/install_poc_stage.py`, `runtime/data/profiles.json` and the component recipes under
`build/packages` before editing. [Customization](customization.md) gives concrete changes
and tells you which package or integration source must be rebuilt.

## Build component packages from source

Package builds run on native arm64 Debian 13. Install the development prerequisites
listed by the relevant `debian/control` on a disposable acquisition/build host, then
record exact installed versions. `dpkg-checkbuilddeps` reports missing dependencies;
`dpkg-buildpackage` constructs both source and binary artifacts. Runtime/Menu are
architecture-independent packages, but VICE and TCPser are arm64 binaries. Keep generated
source trees and artifacts on the external Linux filesystem, outside your source checkout.

For VICE, `build/inputs-poc.json` records the upstream source URL and SHA-256. See
[VICE package construction](vice.md) for exact source identity and build flags. Once you
have obtained and verified that source tarball, the actual Debian recipe works as follows
inside a new build directory:

```sh
tar -xf "$CBM_INPUTS/vice-3.10.tar.gz"
cp -a "$CBM_PRODUCT/build/packages/vice/debian" vice-3.10/debian
cp "$CBM_INPUTS/vice-3.10.tar.gz" project-cbm-vice_3.10.orig.tar.gz
cd vice-3.10
dpkg-checkbuilddeps
dpkg-buildpackage -us -uc -sa
```

`CBM_INPUTS` is your verified input directory and `CBM_PRODUCT` your Product checkout.
The `.orig.tar.gz`, `.dsc`, Debian source archive, `.deb`, `.buildinfo` and `.changes`
are retained together. VICE patches are applied by Debian's quilt source workflow;
do not also apply them manually and then package a doubly patched source tree.

Runtime uses Product source plus `build/packages/runtime/debian`; Menu carries its own
`debian` directory. The factory helper below exports these clean sources and creates
their deterministic original tarballs before invoking the same Debian tooling. TCPser's
recipe is `build/packages/tcpser/debian` and its exact source selection is in the input
record. Reuse an unchanged verified package rather than rebuilding it under the same
version. If you change code, patches, build flags or package metadata, increment the
package version and retain a new build record.

Building packages alone does not create an appliance image. The base closure, pi-gen
recipe, first boot, account/service setup, identity and export steps below supply the
rest. A public first-lock bootstrap must join those inputs explicitly; copying a private
image's filesystem is not the source build process.

## Private frozen-factory walkthrough: prepare the host and repositories

Use native arm64 Debian 13 with Linux ext4 workspace and the exact retained toolchain.
The qualified macOS route uses pinned Lima/VZ plain mode: follow the actionable
[host recipe](../build/lima-build-host.md), including external workspace registration,
pinned bootstrap, render/start and capability probes. Current measured allocation is
8 CPUs, 10 GiB RAM and a 192 GiB sparse disk (grown from 160 GiB with a stopped backup).
The gate requires more than 40 GiB free inside ext4 before construction; the external
provisioning guard requires 256 GiB free. These are factory headroom gates, not card
minimums. Preserve disk headroom for prior attempts, source packages and overlays.

Clone Product and Menu beside each other in your source root, select reviewed exact
refs and read both AGENTS/CURRENT-STATE files. Use Python with
`requirements-contracts.txt`; required Python libraries are retained in the builder.
Do not install/update build packages during frozen assembly. The host recipe's workspace
configuration supplies the bulk root and `build-host/lima/cbm/ssh.config`; source and
bulk paths are operator choices, not usernames embedded in a recipe.

On macOS, these existing wrapper commands manage the registered host:

```sh
python3 tools/build_host.py --workspace-config "$CBM_WORKSPACE_CONFIG" preflight
python3 tools/build_host.py --workspace-config "$CBM_WORKSPACE_CONFIG" lima start cbm
ssh -F "$CBM_SSH_CONFIG" lima-cbm
```

Inside the guest, run the Product recipe's `build/host/capability-gate.sh full`. Verify
host package inventory/update guards against the predecessor lock using
`build_host_guard.verify(lock, kit)` before package work. The complete invocation is:

```sh
PYTHONPATH="$CBM_RECIPE/tools" python3 - "$CBM_PRIOR_KIT" <<'PY'
import sys
from pathlib import Path
from retained_inputs import verify_kit
from build_host_guard import verify
kit=Path(sys.argv[1]); verify(verify_kit((kit/'release-lock.json').read_bytes(),kit),kit)
PY
```

Here `CBM_RECIPE` is the checked-out/exported Product recipe and `CBM_PRIOR_KIT` is a
verified predecessor kit in guest storage. No credentials belong in these variables.

## Export clean inputs and build changed packages

Make your bounded changes, run Product/Menu tests per [testing](../testing.md), update
the changed package changelogs, commit clean source and create an annotated new Menu
tag at its HEAD. Do not reuse an existing version/tag. The refinement helper currently
supports private `1.1.0_poc4.N` and `1.1.0_rcN` Menu versions; RC product identity
is explicitly supplied when freezing. A replay of an unchanged kit needs no new package.

From Product on the source host, choose unused attempt/version values:

```sh
python3 tools/export_candidate.py "$CBM_BULK" ../project-cbm-menu \
  --attempt "$CBM_ATTEMPT" --menu-tag "$CBM_MENU_TAG"
```

It refuses dirty repositories or an unannotated Menu tag. A changed Menu must be at
its tagged HEAD; `--reuse-menu` permits an exact unchanged predecessor tag. It creates source
archives plus `inputs/candidate-export-attemptN.json` with exact commits/tag/hash/bytes.
Verify the external mount first as described in the host recipe. Transfer those new
files into the guest's `inputs` using SSH/rsync, verify hashes there, and extract the
Product archive into a new `recipes/poc4-attemptN` directory. Never unpack over an old
recipe or use an unverified transfer. In the guest (set variables to those exact paths):

```sh
bash "$CBM_RECIPE/build/packages/build_candidate.sh" "$CBM_RECIPE" \
  /srv/project-cbm "$CBM_ATTEMPT" "$CBM_MENU_SOURCE_VERSION" runtime-menu
```

`CBM_MENU_SOURCE_VERSION` is the tag without its leading v. The script creates a new
`packages/poc4-attemptN`, builds Runtime and Menu with dpkg-buildpackage and retains
`.deb`, `.dsc`, source tarballs, `.buildinfo`, `.changes` and logs. The final argument
selects `runtime-menu`, `runtime-vice` (reuse Menu), or `runtime-menu-vice`. RC2 changes Runtime and Menu and reuses verified VICE. When VICE changes, use `--vice-version` during freezing;
when Menu is reused, use `--reuse-menu` during both export and freezing. Reused Menu
version/tag/source must equal the predecessor exactly. Reuse TCPser/closures/assets
and any unchanged component with its original verified identity. Their original recipes are under `build/packages`; adding a dependency
requires authenticated acquisition/retention and a new closure before freezing.

These examples build changed Runtime/Menu together. Add `--vice-version` only
when VICE changes and select the matching package set; a version string is not evidence
that a package was rebuilt. The freeze checks actual package fields and hashes.

Run native tests against the actual new packages in a disposable isolated staging root;
see [native tests](../../tests/native/README.md). Preserve lower-image identity, make it
read-only and put mutations in a separate overlay. Never use the qualification SD card.

## Freeze and construct

Use exact full commits and annotated tag object from the export record:

```sh
python3 "$CBM_RECIPE/tools/freeze_private_candidate.py" /srv/project-cbm \
  "$CBM_RECIPE" "$CBM_PRODUCT_COMMIT" "$CBM_MENU_COMMIT" "$CBM_MENU_TAG_OBJECT" \
  --attempt "$CBM_ATTEMPT" --previous-attempt "$CBM_PREVIOUS_ATTEMPT" \
  --runtime-version "$CBM_RUNTIME_DEB_VERSION" --menu-version "$CBM_MENU_DEB_VERSION" \
  --product-version 1.1.0-rc.2 --candidate private-engineering-rc2
python3 "$CBM_RECIPE/tools/retained_inputs.py" "$CBM_KIT/release-lock.json" "$CBM_KIT"
sudo unshare --net python3 "$CBM_RECIPE/tools/construct_poc.py" \
  "$CBM_KIT/release-lock.json" "$CBM_KIT" /srv/project-cbm --attempt "$CBM_ATTEMPT"
```

`CBM_KIT` is the newly created `inputs/frozen-poc4-attemptN`. The freeze helper supports
verified POC4 predecessors starting at attempt 6, strictly increasing new attempts, and
refuses existing output directories. Freeze verifies corresponding source, package
identity, Cover manifest and all retained descriptors. Historical predecessor inputs
are verified with their exact retained integration recipes before the new recipes verify
the new kit; a changed content-path recipe must not redefine historical evidence. Preserve stdout/stderr externally
as the attempt's build log; a failure is evidence, not a directory to overwrite.

## Validate and retain

Set `CBM_RAW` to the exported raw image, `CBM_XZ` to the compressed artifact, and
`CBM_EVIDENCE` to a new directory on guest ext4. Run as root where loop/mount is required:

```sh
sudo python3 "$CBM_RECIPE/tools/validate_poc_image.py" "$CBM_RAW" "$CBM_KIT/release-lock.json" "$CBM_EVIDENCE/offline"
sudo python3 "$CBM_RECIPE/tools/validate_poc2_closure.py" "$CBM_RAW" "$CBM_EVIDENCE/closure.json"
sudo python3 "$CBM_RECIPE/tools/validate_poc4_supplement.py" "$CBM_RAW" "$CBM_EVIDENCE/supplement.json"
sudo python3 "$CBM_RECIPE/tools/validate_rc2.py" "$CBM_RAW" "$CBM_KIT/release-lock.json" "$CBM_KIT" "$CBM_EVIDENCE/refinement.json"
sha256sum "$CBM_RAW" "$CBM_XZ"
xz -dc "$CBM_XZ" | sha256sum
```

Use pipefail when checking a decompression pipeline. The last digest must equal the raw
digest. Also compare every installed package/version/architecture in `offline/packages.tsv`
against the retained `.deb` closure, and preserve filesystem/ELF outputs. The concrete
candidate validation driver is retained alongside its results; do not omit gates merely
because the commands above returned success. Re-run host guards/capabilities, compare
before/after inventory, and verify no remaining build processes, mounts or loop devices.
Export packages, kit, raw/XZ and logs to the external workspace; repeat hash/equivalence
checks after transfer. Measure used/free space and first-boot/maintenance allowance.

Create an additive checkpoint following [engineering recovery](../recovery.md): exact
refs, full bundles, offline clone/ref/tag/fsck validation, retained-input/output manifests
and independent custody status. Prepare an exact-hash Pi 4 B procedure before flashing.
A build is not physical qualification, nor proof of independent-build reproducibility.
Stop for owner testing; no command here authorizes publication or clears third-party rights.
