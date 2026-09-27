# On-demand screenshots (1.2 runtime contract)

Run `pcbm-screenshot` over SSH as `pcbm`, or `pcbm-screenshot my-test.png`.
The command prints the absolute path only after a complete PNG is saved to
`/home/pcbm/content/screenshots`. The directory is private (0700) and PNGs are 0600,
owned by pcbm. Default names use UTC: `pcbm-20260926T193312Z.png`. Same-second collisions
use `-01`, `-02`, etc.; concurrent captures never overwrite each other.
Existing captures in `/home/pcbm/screenshots` remain untouched.
An optional name must be an ASCII basename ending in `.png`; paths, leading dots,
traversal and overwriting are rejected. No DISPLAY variable is needed.

Screenshots contain whatever is visible, including potentially private filenames,
messages and credentials. Capture is explicit and local: no upload, background
capture, recording, generic alias or Menu action. Copy only PNGs you intend to
share. Screenshots are reachable through the existing authenticated content
SMB share as pcbm; private modes remain compatible because SMB uses the same
account. They are not public. `time pcbm-screenshot` measures qualification
latency; normal use needs only `pcbm-screenshot`. Do not collect screenshots automatically during password entry.

## Backend and privilege boundary

The MIT Runtime wrapper calls exactly `sudo -n -- /usr/libexec/pcbm-kms-capture`
with no arguments and binary stdout over a pipe. Only this fixed command has a
scoped `!use_pty` exception; USB and general sudo policy retain their PTY setting.
There are no file capabilities or setuid binaries. Only pcbm may use this rule.
The separate GPL-2.0-only native helper verifies SUDO_UID/GID 1000, the pcbm account
and root-owned, non-writable, non-symlink activation policy with system_ready=true.

The helper enumerates DRM primary devices and discovers the active vc4 connector,
CRTC, plane and framebuffer. Any incidental master from opening an idle device is
immediately dropped. It does not request master, modeset, switch VTs or write pixels.
The only admitted configuration is one active vc4 display with one full-screen,
unscaled/unrotated linear RGB565, XRGB8888 or opaque ARGB8888 plane and no color
transform/LUT. Other configurations produce a concise unsupported error. No fbdev
fallback exists. It honors pitch/offsets and bounds dimensions to 4096, memory to
64 MiB scanout/256 MiB address space, execution to 10 seconds and stale-frame retries
to three. Normal page flips may change the framebuffer ID; the separate GPL dev2
helper accepts the pinned sampled buffer only if connector/CRTC/plane, mode,
composition and supported layout remain consistent. Actual mode/layout changes
are rejected or retried within the same bound. PRIME synchronization brackets the CPU read. This is not a promise of
tear-free moving-frame capture or qualified multi-display behavior.

All DRM/GEM/PRIME descriptors and mappings are closed before permanently dropping
supplementary groups, real/effective/saved UID/GID and capabilities. Bounding and
ambient capabilities are cleared and no_new_privs is set before libpng processing.
Only then is PNG emitted. The helper opens no caller-supplied path or executable.
The wrapper limits output to 52 MiB and 12 seconds, checks PNG framing/CRC/dimensions,
and writes an anonymous ext4 temporary inode. linkat publishes it atomically without
replacement after successful capture and fsync. Even SIGKILL leaves no named partial
output. Missing/unsupported temporary-inode support fails closed.

The separate `project-cbm-kms-capture` package uses existing libdrm, libpng/zlib and
libcap runtime libraries. Full FFmpeg is not installed for this feature. Exact
source, packaging and GPL license notices accompany the frozen input kit.
[Component provenance](../../components/pcbm-kms-capture/README.md).

The earlier probe demonstrated Menu/MC/VICE BASIC capture, with owner-confirmed HDMI
correspondence. It did not qualify this implementation. New-command physical
qualification, Covers, moving gameplay, latency and transition behavior remain
UNTESTED until the next candidate's owner procedure is completed.

Attempt20 command evidence includes readable Menu/MC/Import captures and owner
latency approximately0.36–0.39s. Moving gameplay failed twice with the conservative
"display changed" error (0.278s each). The dev2 page-flip correction is a new
component and requires fresh physical gameplay/HDMI/audio/lifecycle qualification.
[Attempt20 record](../qualification/attempt20-owner-review-2026-09-26.md).
