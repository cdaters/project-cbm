# Final 1.2.0 candidate / attempt26

**PRIVATE, UNPUBLISHED. Physical Pi4 regression remains UNTESTED.** Final version
metadata is already in the image so publication can use the exact tested bytes.
This is a new build, not a relabelled or modified attempt25.
[Full identities/results](final-1.2.0-attempt26.json) ·
[Required physical procedure](../qualification/attempt26-pi4-final.md).

## Fix and sources

FILES → USB Drive omitted the shared UI's hide-tags setting. Menu fix `0b08624`
sets it, matching Guided Import; dialog still returns the original stable device
key. Duplicate/shortened-identical labels retain correct mapping. No mount,
privilege, terminal or transfer implementation changed.

Frozen Product `adb61cfef7942a73fd10feed91db7c76d34114d8`; Menu `7792fed364c93b0dc6f741a4e985ed00c9d39411`.
Local annotated `v1.2.0` tag objects: Product `d69adb9e8d8730886f0eb9a9b2988055dc1535f8`;
Menu `524db35daa649ce2c43860d59cc4fbd11acb8cc4`. Nothing pushed or published.
Runtime `1.2.0-1`, Menu `1.2.0-1+pcbm1`, separate GPL KMS `1.0.0-1` are newly
packaged; VICE/TCPser retain their exact prior packages. Runtime/helper behavior
is unchanged; updated user guides, notices and final package identities are new.
Owner explicitly extended unchanged artwork and VICE policy to1.2.0.
Lock `ccbd487c39dea2e000f3ae28d2dd81aabadea40cdd4b8de2a5718968382d1819`; kit `inputs/frozen-poc4-attempt26`.

## Checks

Native Product354/Menu123, zero skips; installed USB11/screenshot12/Online8 PASS.
Installed tests exercise real dialog/FIFO/sudo/broker/MC under TERM=linux, including
foreground terminal/fds, keys, exit, disconnect/crashes and busy-release wording.
376 image checks plus4 boot/Online byte checks,7 privacy and11 KMS security
checks PASS; 673 package identities and ELF
closure checked. Frozen external kit 3360 files
verified; raw/XZ equivalence and GPL packaged-source offline compile PASS.
Documentation605 checks PASS. Host inventory/update/capability guards unchanged.

Two initial installed-test runs falsely failed because raw terminal bytes split
friendly labels/action text at coloured shortcut letters. Retained transcripts
establish this. Test-only commits `a997e09`/`ee86a48` normalize terminal formatting;
the passing external verification recipe differs only in that test. Frozen source,
packages and final image inputs were not patched. Neither failed run is hidden.
Mac-only mktemp expectation remains contextual; the native full suite passed.

## Exact files

Paths relative to registered ProjectCBM-Work:

- Raw: `artifacts/release-1.2.0-attempt-26/2026-09-27-project-cbm-1.2.0.img`
  3095396352 bytes; SHA-256 `2a5d192477eac37c819b267ca05b63d466186504c0b92230819208ad94c4f35a`.
- XZ: `artifacts/release-1.2.0-attempt-26/image_2026-09-27-project-cbm-1.2.0.img.xz`
  599119848 bytes; SHA-256 `b2b7836f752d4b5b3a9a7cd5116776dff8f19eceaf4ad155b9541cc2efb69b5d`.

Root capacity 2439266304 bytes; used
1655762944; available to user before expansion
639221760. Do not infer a nominal SD minimum.

## Publication and recovery

Await the five owner physical checks in the linked procedure. Publish only these
exact passing bytes after the source/privacy/assets audit; do not rebuild afterward.
Public asset name will be `project-cbm-1.2.0.img.xz`; renaming/copying must preserve
this XZ hash. No GitHub release or uploaded assets exist from this work.

Recovery checkpoint: `archive/final-1.2.0-attempt26-2026-09-27`. Bundles, exact
refs/peeled tags, offline restore/fsck, manifests, inputs, corresponding source,
packages, image and tests are retained. Same-volume unencrypted TheBench storage
is not independent custody; independent encrypted backup/restore remains outstanding.
Historical images/tags/evidence remain unchanged. No live Pi patch or flashing.
