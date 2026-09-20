# RC2 corrections and evidence

RC1 attempt #9 on Pi 4 B passed the core lifecycle and owner reference performance,
but failed primary boot identity, coherent account/content ownership, USB import and
practical file-management usability. The [owner report](../qualification/rc1-attempt9-pi4-owner-report.json)
binds those outcomes to the exact image and lock. Unreported behavior stays UNTESTED.
The candidate is unchanged. Source changes here require a distinct RC2 freeze/build.

## Evidence and decisions

- The authenticated-shell readback matches RC1's lock, integration and all four package
  identities. Two numeric-only logs are privately retained under configured workspace
  `qualification/rc1-attempt9-live-2026-09-19`. Samples 10–21 independently span
  60.089/60.092 seconds, weighted speed 99.998829/99.998327%, minimum
  99.981/99.959%, weighted emulated FPS 50.124081/50.123830. Both metric gates PASS.
  The second log's warp interval is samples 23–31 and is excluded. Numeric extraction
  is an owner readback, not a byte copy of the complete log. The owner supplies the
  separate normal audiovisual observation; telemetry alone cannot identify a payload.
- Live USB inventory shows an unmounted exFAT partition and active udisks2. The exact
  failure screen matches RC1's generic importer failure branch. On native Linux,
  RC1's production `0077` umask and root FAT/exFAT mount produced UID/GID 0, mode 0700;
  the deliberately unprivileged UID1000 worker failed to read it. Both filesystems
  reproduce `copy_failed`. Fixed mount options give only UID/GID1000 access while
  retaining `ro,nodev,nosuid,noexec`. Native tests then copy successfully, preserve
  existing files on retry, unmount and verify unchanged media hashes. ext4 retains
  `noload` and real filesystem permissions. No package or configuration changed on Pi.
- The journal locates 5.134061 seconds from getty activation to PAM session opening.
  RC1's hash-verified installed getty template has `Type=idle`; systemd's installed
  documentation specifies a five-second output-scheduling deferral. RC2 changes that
  service type to `simple`, retaining first-boot ordering, agetty/login/PAM, tty behavior
  and networking waits. This is evidence-supported, not proof of the total physical
  30-second startup cause or an RC2 speed result. Numeric session/Menu phase traces
  distinguish setup, profiles, presentation, status and dialog invocation; physical
  stopwatch/input readiness remains required.
- The exact released v1.0.0 image (SHA-256
  `168a3026eca2bc328e03e47dfbb0cbe17740180504ad7858496df84982e89849`)
  used autologin pi → profile → pcbm-start → Menu → no-argument cover helper, selecting
  numbered primary artwork for a three-second framebuffer presentation. Quiet/rainbow
  settings existed. Its unit links show normal networking/maintenance services and
  no evidenced special fast-boot mask set to copy. Its PiShrink expansion differs from
  the current guarded first-boot owner and is not restored. RC1 still made the old
  no-argument call, but today's wrapper deliberately rejected it. RC2 explicitly uses
  the byte-identical `pcbmcover1.jpg` through current supervised SDL presentation,
  with 1.5 seconds after first frame submission. Existing seven machine artwork files,
  display geometry, preferences and Cover/VICE/F10 return contracts remain intact.

## Single-user contract

The owner explicitly replaces the earlier pi/pcbm split. Fresh RC2 uses pcbm UID1000,
`/home/pcbm`, and canonical `/home/pcbm/content`; this is an account/home policy change
inside the accepted console/session architecture. UID1000 retains runtime device
access. Root remains root. General sudo requires the first-boot password; constrained
passwordless helpers remain fixed. Samba authenticates and writes as pcbm without
`force user=pi`. SSH/SFTP, Menu, VICE, FILES, preferences and diagnostics now belong to
the same user. No in-place rename or destructive content migration is performed on RC1.
Backup/reflash/selective restore is documented in [accounts/layout](../release/accounts-and-layout.md).

FILES offers Midnight Commander on the library/home and the existing safe USB import
workflow. It does not add an unrestricted mount helper or a new automounter. Import
shows persistent working/results UI, fixed failure reasons and confirmed/unconfirmed
source release. The privilege boundary returns no raw exception text or private paths.

## Verification still required

Source tests, native installed account/service/TTY/Cover checks, new package identities,
actual-image gates and recovery must all pass before READY TO FLASH. Native/headless
results cannot establish primary visibility, physical USB success, actual boot saving
or Pi input behavior. RC2 requires one exact-hash Pi 4 B regression procedure. No push,
publication, Pi 3 tuning or unrelated feature work is authorized here.
