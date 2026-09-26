# Project CBM screenshot feasibility — read-only Pi 4 study

Study of private 1.2.0-dev.1 attempt18, September 25, 2026 (Phoenix). Exact image
basis: [attempt18](../build/private-1.2-dev1-attempt18.json). No packages, programs,
permissions, configuration or screenshots were written onto the Pi. Temporary
Python probes arrived over SSH stdin and used read/query operations only. PNG
encoding and evidence writes happened on the engineering host. The owner drove
the console; no remote key injection, modesetting or VT switching was performed.

**Recommendation:** pursue a small, separately packaged KMS capture component with
a narrow Product wrapper/helper. `pcercuei/kmsgrab` is a useful starting point,
but needs reviewed changes before adoption. Do not install full FFmpeg solely for
this command. **Console and VICE/BASIC pixel capture are demonstrated** using
read-only probes; the packaged command and broader qualification remain outstanding.
Do not ship a command that silently returns fb0 while SDL is displayed.

## Actual display and results

Pi 4 Model B Rev 1.4, Trixie, kernel 6.18.50+rpt-rpi-v8; `vc4-kms-v3d` is enabled.
The display device is **/dev/dri/card1 (vc4-drm)**; card0 is V3D and renderD128 is
its render node. Card numbering must be discovered, not frozen into the command.
HDMI-A-2 is connected/enabled at 1920×1080@60; HDMI-A-1 is disconnected. Observed
scanout uses CRTC114 and plane103, fullscreen at 1:1 scale with no other active plane.
These IDs are observations, not a stable API contract.

| Surface | Evidence and status |
| --- | --- |
| Text console / MC | RGB565 linear vc4drmfb, pitch3840, fb722. Read-only fbdev capture as UID1000 succeeded; owner explicitly confirmed MC PNG matches HDMI. Console-path proof, not every VT/content case. |
| Main Menu | PNG captured after Ctrl+C and visually inspected as Main Menu. Same console framebuffer path; separate owner pixel-for-pixel confirmation not requested. |
| VICE/SDL2 | x64sc owns DRM master on card1; linear ARGB8888 (AR24), pitch7680, 1920×1080. UID1000 GetFB returns metadata but handle0. After owner supplied administrative authentication, read-only GetFB2/PRIME/map succeeded with capture client master0, then privileges were dropped before transfer. Owner confirmed the BASIC PNG matches HDMI, including the requested color/border/scanline comparison, and F10 return works. Moving gameplay timing not tested. |
| fbdev during VICE | Read succeeds but PNG is black, not a valid gameplay capture. The active scanout is a different framebuffer. This backend fails the combined Menu+VICE requirement. |
| Covers | UNTESTED capture. Existing SDL Cover path suggests KMS capture is appropriate; the brief display interval needs coordinated testing. No duration/lifecycle change was made. |
| No display / dual displays | UNTESTED physically. Proposed command must fail clearly for no active display or an ambiguous selection. |

The MC capture took about20ms to read the framebuffer; SSH transfer plus host PNG
encoding took2.9s. Menu read18ms/total2.4s; the invalid VICE fbdev read24ms/total2.4s.
These are proof-of-concept measurements, **not installed on-Pi PNG latency**. The
small capture should be benchmarked on Pi4 with gameplay frame-time/audio impact.

The later authenticated KMS probe captured Menu in14ms, with its PNG hash exactly
matching the earlier fbdev Menu PNG. VICE capture took32ms for export/read and2.46s
including transfer/host encoding: 148,391-byte PNG, SHA-256
`b5bc8009d84610367781834e8d9b82f224f65c9baaad58ddc1156685d867cbb4`.
It captured fb723; transient framebuffer IDs change between launches/flips.
UID0 exported/read the pixels, relinquished supplementary groups and UID/GID before
transfer, and never became DRM master during VICE. No display takeover was used.

## Backend comparison and dependencies

The reviewed [kmsgrab source](https://github.com/pcercuei/kmsgrab/blob/d4c6061a59f4b7ecb6b39f96c7d39a5d5f48b702/kmsgrab.c)
is pinned to `d4c6061a59f4b7ecb6b39f96c7d39a5d5f48b702`, with SPDX GPL-2.0-only.
It exports a framebuffer through PRIME, maps it and writes PNG. It picks the first
dumb-buffer-capable card and active plane, uses legacy GetFB, assumes packed16/32bit
pixels and ignores pitch/modifier/composition details. Its filename open overwrites;
`seteuid(getuid())` does not drop a sudo invocation to the original login user.
It is unsuitable as an unrestricted privileged installed command. Review allocation,
error handling, FD lifetime, color conversion and privilege dropping as well.

Build requirements are C/CMake/pkg-config, libdrm and libpng development files.
Runtime libraries libdrm2, libpng16 and zlib are already installed. Package the
pinned upstream source plus reviewed patches separately; retain corresponding
source, license text, notices and reproducible recipe. Keep the original CBM wrapper
separate; do not copy GPL source into MIT-labelled runtime modules. This study is
not a completed redistribution/package approval or a blanket licensing conclusion.

[FFmpeg kmsgrab](https://ffmpeg.org/ffmpeg-devices.html#kmsgrab) has explicit device,
CRTC and plane selection, but still needs DRM master or CAP_SYS_ADMIN. CPU download
requires a linear, mappable buffer; capture sampling is not synchronized to flips.
It captures a selected plane, not automatically the composited HDMI result. FFmpeg
is absent from this image and adds a larger closure for no demonstrated benefit to
one-shot PNG capture. Its exact build's licensing/dependency closure would need
review if selected; it is not recommended solely for screenshots.

[fbgrab](https://github.com/GunnarMonell/fbgrab) reads fbdev into PNG using libpng/zlib
and documents GPLv2. A fbcat-based path has the same fbdev visibility limitation.
Neither solves the observed VICE mismatch. A console-only fallback is acceptable
only after proving that fbdev is the active scanout; never silently return stale
or black fbdev contents as a successful SDL screenshot. No DispmanX tool is proposed.

## Privilege model

The ordinary user already has video/render access. It can read fb0 and can obtain
an exportable console framebuffer handle when opening the unowned primary device
implicitly becomes DRM master. During VICE, the same probe is not master and gets
handle0. Render/video membership alone is therefore **insufficient** for independent
capture of VICE's active buffer on this installation.

The [kernel GetFB2 contract](https://docs.kernel.org/gpu/drm-uapi.html#drm-ioctl-mode-getfb2)
restricts returned buffer handles to DRM master or CAP_SYS_ADMIN. Do not steal DRM
master from VICE; SDL's [KMSDRM default](https://wiki.libsdl.org/SDL2/SDL_HINT_KMSDRM_REQUIRE_DRM_MASTER)
expects to own it. For independent SSH capture while VICE runs, the proposed model is:

1. Unprivileged `pcbm-screenshot` handles validated naming and user-owned output.
2. A fixed root-owned, readiness-gated helper admits only the configured runtime
   user to capture the active CBM display. It accepts no arbitrary device, path,
   command, process or framebuffer ID. Existing owner authentication remains intact.
3. The helper uses CAP_SYS_ADMIN only for framebuffer-handle access, exports a
   read-only buffer, closes unused handles/descriptors, and permanently drops
   privileges/capabilities before processing pixels. Bound dimensions, memory,
   execution time and retries. No modesets, VT switches or framebuffer writes.
4. Return bounded pixels/PNG over a fixed stdout protocol or caller-owned descriptor;
   never open a caller-supplied filename as root. Avoid PTY transformation of binary
   output. Normal users type one command; a privileged component still exists.

CAP_SYS_ADMIN itself is broad: Linux provides no screenshots-only capability here.
Do not grant it to Python, FFmpeg or the unreviewed upstream binary. A scoped helper
is a design proposal needing security review and explicit approval for the new
privilege boundary; no sudoers, file capability or setuid change was made. A VICE
in-process export could avoid this privilege but would be a separate integration
design, not a proven general console/Cover/gameplay replacement.

## Proposed command contract

`pcbm-screenshot` saves to `/home/pcbm/screenshots/pcbm-<UTC timestamp>-<unique>.png`
and prints only the exact saved path. Optional `pcbm-screenshot my-test.png` is
useful: accept a basename ending in `.png`, reject separators/traversal, never
overwrite an existing file. Directory0700 and PNG0600, safe exclusive creation,
symlink-resistant handling and atomic completion; remove failed partial captures.
Create the directory only when needed as its ordinary owner.

Use the active CBM connector/CRTC and query format, stride, offsets and modifiers
through supported DRM APIs, not debugfs text in the shipped command. Verify a
supported composition: one fullscreen plane is the measured case. Unsupported
tiling, overlays, scaling/rotation or color-management configurations must be
handled correctly or rejected; a raw primary plane is not an unconditional HDMI
screenshot. Bounded retries handle a page flip or display transition. No active
display yields `Screenshot unavailable: no active display.` Other unavailable
cases give similarly concise errors and a failing exit status.

Keep output outside the existing shared `content/screenshots` tree by default.
Screenshots can contain visible addresses, filenames, credentials or personal data;
file permissions do not redact pixels. No background capture, uploads, public logs
or automatic attachments. Host evidence here remains private. Do not expose
unrelated private paths or environment in errors. SSH needs no DISPLAY variable,
desktop or display-ID knowledge. Defer a generic `screenshot` alias and optional
CONTROL action until the command is dependable; neither is necessary for1.2.

## Remaining proof and 1.2 decision

The initial unauthenticated study stopped at handle0. The owner then supplied
temporary administrative authentication, used only over SSH stdin, without storing
it in source, command arguments or evidence. Original bounded Python probe code
ran from command text, not an installed Pi file. Its first PRIME call failed because
the engineering probe used an incorrect CLOEXEC flag; original source/error remain
retained. A distinct v2 corrected the flag to O_CLOEXEC per the kernel contract.
Its first successful capture was Menu (despite the planned VICE filename); metadata
and pixels explicitly identify it as Menu. A later owner-driven VICE opportunity
produced the actual BASIC capture. The owner reported: "Capture matches; F10 return
works." The follow-up snapshot has dialog on tty1, no remaining DRM clients and
no browse mount. No failed result is concealed or called a PASS.

The earlier sealed feasibility evidence preserves its then-BLOCKED result. The
additive `qualification/screenshot-kms-proof-2026-09-25` evidence supersedes that
specific blocker with successful pixel export and owner HDMI/F10 confirmation.
Next: reviewed packaged implementation and performance/error tests.
Cover capture, moving-game timing, headless behavior and broader formats remain
untested. User-driven plain console cases can extend coverage.

This is a useful **conditional 1.2 feature**, especially for qualification, but is
not ready to include yet. Review the narrow privilege and GPL packaging, then
implement/test on a distinct
private candidate. Do not delay the confirmed USB terminal fix on an unproven
screenshot feature or modify attempt18 in place.

Private evidence: `qualification/screenshot-feasibility-2026-09-25` under bulk
storage; includes probes, upstream source/origin hashes, screenshots and display
snapshots. Additive authenticated proof: `qualification/screenshot-kms-proof-2026-09-25`.
Source/evidence recovery: `archive/attempt18-tty-screenshot-2026-09-25`.
Its manifests and offline restore report are completion authority. Independent
custody remains outstanding. The study does not change release/qualification status.
