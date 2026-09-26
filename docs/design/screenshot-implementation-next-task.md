# Next bounded 1.2 task: pcbm-screenshot

Prepared separately from the USB terminal correction. **No screenshot implementation,
package or image change is included in that candidate.** Wait for the owner to resume
this task after USB qualification; do not start a background build or mutate attempt19.

Basis: [accepted feasibility study](screenshot-feasibility-2026-09-25.md). Read-only
Menu and VICE/BASIC captures on attempt18 were demonstrated; the owner confirmed MC
and VICE HDMI correspondence and VICE F10 return. Covers, moving-game cost, headless
behavior and an installed command are not qualified by those experiments.

## Outcome and boundary

Implement `pcbm-screenshot [basename.png]` as one ordinary-user SSH command, saving
PNG privately under `/home/pcbm/screenshots/`, printing the saved absolute path,
never overwriting a capture and failing concisely when unavailable. Discover the
active CBM KMS display; no user card/plane IDs, desktop or DISPLAY environment.
No Menu action, generic alias, daemon, recording, upload or automatic capture.

Use a small dedicated KMS component. Review pinned pcercuei/kmsgrab commit
`d4c6061a59f4b7ecb6b39f96c7d39a5d5f48b702` as a separately packaged GPL-2.0-only
upstream component with corresponding source, patches, license text and notices.
Do not vendor its code into MIT-labelled runtime modules. Runtime libdrm/libpng/zlib
already exist; retain exact build/source closure before package freeze. Do not add
FFmpeg solely for screenshots or use fbdev as a silent SDL fallback.

## Required engineering decisions and tests

- Review/fix card/connector selection, GetFB2 metadata, pitch/offset/modifier/color
  handling, resource cleanup, bounds and checked privilege dropping. Handle or
  explicitly reject unsupported multi-plane/crop/rotation/composition cases.
- Review the narrow privileged export helper and its authorization before enabling
  it. The demonstrated foreign-buffer path needs DRM master or CAP_SYS_ADMIN;
  video/render groups are insufficient during VICE. Never take master from VICE
  or grant broad capability to Python/FFmpeg/arbitrary upstream commands.
- Keep names/files/directories user-owned, directory0700/PNG0600, reject traversal
  and symlink attacks, create exclusively and commit atomically. Privileged code
  must not open user-supplied output paths. Preserve readiness/account boundaries.
- Test absent/ambiguous display, stale/changed framebuffer, unsupported format,
  permission failure, unavailable capture, collisions, concurrent commands and
  interrupted writes with no partial success or private diagnostic leakage.
- Measure complete on-Pi PNG latency and gameplay frame-time/audio impact at the
  Pi4 floor. Recheck Menu, text, MC, Covers and VICE against actual HDMI; verify
  repeated F10 return and capture during transitions without modifying lifecycle.
- Keep captures out of shared content by default; screenshots contain whatever is
  visible, potentially sensitive. No automatic collection or transfer.

Keep upstream packaging/security changes and the Product wrapper in separate logical
commits from the USB fix. Version every changed component, construct a later distinct
private candidate and retain its own qualification evidence. Never retrofit either
attempt18 or the USB-only candidate. Stop for explicit owner hardware testing.

Assembly64 remains outside this task: documentation/research only pending provider
and client-id feedback; no Online Library network-client activation.
