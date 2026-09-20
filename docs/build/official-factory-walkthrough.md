# Official factory: construction and preservation walkthrough

This advanced procedure requires a complete previously verified input kit. It is not
the public first-build bootstrap. Start with [Build Your Own](../release/build-your-own.md)
for the public status and package-building introduction. Commands are source-checked;
this documentation pass did not run package builds or construct an image.

## Private frozen-factory walkthrough: prepare the host and repositories

Use native arm64 Debian 13 with Linux ext4 workspace and the exact retained toolchain.
The qualified macOS route uses pinned Lima/VZ plain mode: follow the actionable
[host recipe](lima-build-host.md), including external workspace registration,
pinned bootstrap, render/start and capability probes. Current measured allocation is
8 CPUs, 10 GiB RAM and a 256 GiB sparse disk.
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
selects `runtime-menu`, `runtime-vice` (reuse Menu), or `runtime-menu-vice`. The final release-polish candidate changes Runtime and Menu and reuses verified VICE. When VICE changes, use `--vice-version` during freezing;
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

## Approved CCGMS inputs

The final release composition uses the CCGMS-only disk recipe, not the upstream
compilation. Before freezing, retain the three exact reviewed inputs named in
`build/optional/ccgms.json` beneath the workspace's `inputs/ccgms-2021/`: upstream
D64, published source and BSD license notice. The freeze checks their hashes, extracts
only the verified PRG and constructs the deterministic application disk. See
[CCGMS integration](../runtime/ccgms-integration.md) for provenance and exact identities.
This is a required acquired input set; the factory does not download or scrape it.
The new lock omits StrikeTerm while historical kits keep their original evidence.

## Freeze and construct

Use exact full commits and annotated tag object from the export record. Set
`CBM_PRODUCT_VERSION` and `CBM_CANDIDATE` to the distinct version and private identity
being assembled (for example `1.1.0-rc.3` and `private-engineering-rc3`). The pi-gen
configuration image name and stage-cbm export suffix must match that same identity:

```sh
python3 "$CBM_RECIPE/tools/freeze_private_candidate.py" /srv/project-cbm \
  "$CBM_RECIPE" "$CBM_PRODUCT_COMMIT" "$CBM_MENU_COMMIT" "$CBM_MENU_TAG_OBJECT" \
  --attempt "$CBM_ATTEMPT" --previous-attempt "$CBM_PREVIOUS_ATTEMPT" \
  --runtime-version "$CBM_RUNTIME_DEB_VERSION" --menu-version "$CBM_MENU_DEB_VERSION" \
  --product-version "$CBM_PRODUCT_VERSION" --candidate "$CBM_CANDIDATE"
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
sudo python3 "$CBM_RECIPE/tools/validate_rc3.py" "$CBM_RAW" "$CBM_KIT/release-lock.json" "$CBM_KIT" "$CBM_EVIDENCE/refinement.json"
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
