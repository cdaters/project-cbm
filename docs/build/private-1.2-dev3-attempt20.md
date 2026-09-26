# Private 1.2.0-dev.3 / attempt20

**PRIVATE NON-RELEASE. Built and validated; STOP for owner Pi4 physical testing.**
This candidate combines the independently committed Menu friendly-label fix with
on-demand screenshots. It does not change attempt18/19 or published1.1.0.
[Machine-readable identities](private-1.2-dev3-attempt20.json).

## Source and packages

Menu presentation fix `f9c4607d884a5573a943a9e1c1dd01832ca6dece`; private package
version commit `53e5409999bebe97746220d75af51cbbf28eb095`, annotated `v1.2.0_dev2`
(object `532a221e32efaeb4ed448bb2d34d0c27462d8449`). Screenshot implementation
`033bfd16776b360663f25bbbed8e14f682e4a55a`; frozen Product integration
`f87a2c521cc3a034ecd69a5db59ad19be99cebfe`. Product/Menu versions remain independent.

- runtime: `1.2.0~dev3-1`, 89,996 bytes, SHA-256 `894e3fe224140b361dd2587056e1062354f0c807b2ab7d1bfaf8edf63929672e`.
- menu: `1.2.0~dev2-1+pcbm1`, 1,299,480 bytes, SHA-256 `5348969f2353443f4b28f91dd14676d481d81003d61256b74a39e58b349df8f0`.
- kms-capture: `1.0.0~dev1-1`, 17,472 bytes, SHA-256 `b9185f6b0602d886d88ad5986ab96bde3cc119a89918423cb7efeb4c752bc963`.

Frozen lock: `dc28290451f7b8ce78eca9625bd3d0ab052ab7df2c61f5776a666c48bd83d514`. Retained kit:
`inputs/frozen-poc4-attempt20`. VICE/TCPser, content allowlist, read-only USB protections
and Assembly64 network-disabled status are unchanged.

## Image identity

All paths below are relative to registered bulk storage
`/Volumes/TheBench/ProjectCBM-Work`:

- Raw: `artifacts/private-1.2-dev3-attempt-20/2026-09-26-project-cbm-1.2.0-dev.3-lite-private-1.2-dev3.img`
  — 3,095,396,352 bytes; SHA-256 `014e9598453e9361984559ac060583dbfb76947ba51206d704c6773e2175d330`.
- XZ: `artifacts/private-1.2-dev3-attempt-20/image_2026-09-26-project-cbm-1.2.0-dev.3-lite-private-1.2-dev3.img.xz`
  — 599,067,756 bytes; SHA-256 `8a7e07bd58f126be105f31b63f782d313d1c08f1634174b5090fb1ab8bcfe356`.

Native and exported raw/XZ equivalence PASS. This is one successful build, not a
reproducibility claim. Root filesystem capacity2,439,266,304 bytes, used1,655,668,736;
available to the ordinary user before expansion639,315,968 bytes. Maintenance margin
and expanded physical-card capacity remain unmeasured; no nominal8GB minimum is asserted.

## Capture boundary and provenance

[Command/security contract](../runtime/screenshot.md). Ordinary `pcbm-screenshot`
uses a fixed, no-argument sudo helper. Only that binary has a scoped `!use_pty`
exception for binary stdout; general sudo and USB terminal policy are unchanged.
The helper checks trusted readiness and the fixed runtime account, discovers the
single active vc4 scanout, exports read-only pixels and closes DRM/GEM/PRIME resources.
It permanently drops groups, all real/effective/saved UID/GID privileges and capability
sets before PNG encoding. No master acquisition request, modesetting, VT switch,
framebuffer write, arbitrary command/device/output path or file capability is provided.

The separate GPL-2.0-only `project-cbm-kms-capture` component uses the reviewed
pcercuei/kmsgrab commit `d4c6061a59f4b7ecb6b39f96c7d39a5d5f48b702` as its technical
starting point. Exact upstream reference, notices, complete license and corresponding
source are retained. MIT Runtime code is separate. Existing libdrm/libpng/zlib/libcap
are reused; no FFmpeg binary is installed. The native helper is67,744 bytes.
One linear fullscreen RGB565/XRGB8888/opaqueARGB8888 plane is supported. Unsupported
composition, transforms, modifiers and ambiguous displays fail clearly; no fbdev fallback.

## Validation and limits

Native Product324/324, Menu109/109, GPL component scenario tests, eleven real USB
installed-path cases and twelve screenshot installed-path cases PASS. These cover
filename/traversal/symlink/overwrite/concurrency/interruption/partial-output handling,
private modes/ownership, time/output bounds, no/ambiguous display, unsupported format,
pitch/offset/modifier/composition, page-flip retry, permission/sync failure, GEM cleanup,
readiness/account/argument denial, real permanent privilege drop and binary sudo output.
The screenshot installed test substitutes only pixel acquisition in a separately
compiled test executable; actual production helper verifies headless failure. This
is not proof of visible Pi scanout. Initial missing-Git-context test errors are retained;
final tests use exact repository bundles and all pass without skips.

354 actual-image checks,7 privacy checks and11 additional capture security/ELF checks
PASS. All673 installed package identities match retained artifacts; the existing127-object
ELF graph and separate8-object helper graph resolve (graphs overlap; do not add them).
FAT/ext4/systemd, exact installed payloads, PIE/RELRO/NOW/non-executable stack/no file
capabilities, dependency/source closure and corresponding-source offline restore/compile
PASS. Native builder inventory/update guards and capability checks pass before/after;
no host package update occurred. Network-isolated assembly consumed retained inputs.

[Hash-bound owner procedure](../qualification/attempt20-pi4-screenshot-usb.md).
All new physical screenshot cases, moving gameplay/latency/audio impact, Cover/transition
behavior and corrected-ID HDMI appearance remain UNTESTED. Earlier probe captures and
attempt19 owner results remain separate evidence. Deliberate busy-unmount fault injection
is still distinct from the owner's normal safe-unmount PASS.

## Preservation and recovery

Evidence: `qualification/screenshot-dev3-implementation`. Existing stable1.1.0,
attempt18 and attempt19 raw/XZ rehash unchanged; protected Product/Menu tags unchanged.
Earlier guest attempts, failed trials and logs remain retained. No live Pi changes.
Recovery checkpoint: `archive/private-1.2-dev3-attempt20-2026-09-26` (completion/seal
reported in CURRENT-STATE). It binds full Git bundles, exact refs/tags, source and
package closure, build/validation evidence and image bytes. TheBench is unencrypted;
same-volume recovery is not independent custody. Independent encrypted custody and
independent restore drills remain outstanding. No publication, release, Online Library
network client, BIN/ROM policy change or next feature is authorized by this result.
