# RC3 bounded presentation and USB polish

[RC2 physical evidence](../qualification/rc2-attempt11-pi4-owner-report.json) is
bound to attempt11. The running qualification image stays unchanged. RC3 retains
pcbm UID1000, `/home/pcbm/content`, the VICE configuration and machine Cover lifecycle.

## Boot presentation

RC2 put primary artwork after first-run processing. Completed first-run still called
`setup-finish` with a working dialog; returning from KMS restored that previous
console screen. Five actual traces place the primary operation at 4.69–4.96 seconds,
including driver initialization, a 1.5-second dwell and release. The latest renderer
record confirms KMSDRM/opengl, first submission at2185ms and successful terminal
restoration. These observations explain the late presentation and repeated screen;
they do not establish the complete cause of the physical20–23-second stopwatch time.

The exact retained v1.0.0 reference used a login/profile/Menu-owned three-second
primary image, not an earlier initramfs graphical owner. Its useful idea is a
recognizable primary identity. RC3 preserves the accepted SDL/KMS and login/PAM
architecture rather than restoring its framebuffer/ImageMagick implementation.

The earliest chosen ownership point is entry into the local tty1 PAM
appliance session: device permissions, controlling terminal and foreground process
group already exist. Moving graphics before this point would require another console
owner and new ownership transitions. RC3 instead starts the existing unprivileged SDL
renderer immediately and prepares setup/preferences/status concurrently in that same
session. Anonymous pipes carry readiness and release acknowledgments only. The first
meaningful setup/error/Menu screen waits for renderer exit/reaping and verified tty
restoration. Artwork remains at least three seconds after its first submitted frame,
or until the screen is ready, whichever is later. Startup-to-machine hands off before
the existing machine Cover/VICE path. Fresh setup does not trigger a second splash.
Missing/failed artwork falls through; a30-second supervision budget and TERM/KILL
cleanup prevent a lost preparation/renderer from holding the display indefinitely.
Physical visibility and handoff smoothness still require the new exact-image test.

Completed setup retains its idempotent privileged readiness check and crash-recovery
activation; it omits the routine working dialog. Failures remain visible. Getty keeps
normal login/PAM, Type=simple and first-boot ordering; `--skip-login --noissue --nohostname` removes
routine tty1 identity/IP prose. Detailed network information remains in pcbm-info/UI.
No NetworkManager wait, maintenance unit or filesystem check is disabled.

The existing vendor initramfs `quiet` branch passes fsck output through logsave to the
console even on a clean filesystem. A narrowly checked build hook suppresses only a
zero-status result's console copy, retaining the full fsck log. Every nonzero result,
including corrected errors, remains visible with unchanged status handling. Unexpected
vendor script bytes fail construction. Removing `quiet` from the firmware partition's
single-line `cmdline.txt` restores the unchanged verbose filesystem-check path; remove
`loglevel=4` and `systemd.show_status=auto` too for fuller startup diagnostics. Recovery
VT/access remains as documented. HDMI timing/input overlays in the photographs appear
to be external display OSD and are not treated as Linux output.

## USB content counts and metadata policy

The actual imported directory contains intended D64 files, AppleDouble companions and
content from macOS Trash. The drive was absent at collection; the original nine-file
source set is not yet completely reconciled. Finder metadata currently in the SMB
folder is not automatically attributed to import.

Import skips entries with the exact names `.DS_Store`, `.Spotlight-V100`, `.Trashes`,
`.fseventsd`, `.TemporaryItems`, `.VolumeIcon.icns`, `.AppleDouble`,
`System Volume Information`, `$RECYCLE.BIN`, and names beginning `._` (AppleDouble).
A matching directory is not traversed. Other hidden files and directories remain
eligible under the normal media-extension policy. No format-directory hierarchy is
added. The UI reports content files actually copied, existing/unsupported entries
skipped, and host metadata entries/subtrees ignored separately. An ignored subtree
counts as one ignored entry; its hidden descendants are never counted as user content.

No source is modified, existing destination file replaced, or old imported metadata
silently deleted. The read-only FAT/exFAT UID/GID options, ext4 noload, unprivileged
copy worker, bounded transfer/free-space checks and confirmed unmount remain intact.
