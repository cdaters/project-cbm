> Later physical status (2026-09-27 UTC): [owner results and reviewed screenshots](attempt25-physical-results-2026-09-27.md). Reported focused cases PASS; guided Import reconfirmation pending; separate FILES/USB opaque-tag presentation finding open. Original build-time status and procedure below are retained.

# Attempt25: direct boot, console restoration and Online Library retest

PRIVATE NON-RELEASE 1.2.0-dev.6. Built and validated; physical UNTESTED.
Raw SHA-256 `adc26fff5355d587547a72dcba737baab7f931d3d66ac646588151c91bb86d49` (3095396352 bytes).
XZ SHA-256 `77d61462479d26593d60dbce04b1e483365e371103d53664205b97f04f17d671` (599632072 bytes).
[Exact paths/packages/build checks](../build/private-1.2-dev6-attempt25.md). Never update attempt24 in place.
Use separate media. Preserve its captures, failures and keyboard-mode chronology.

1. With boot preference Menu, check a responsive Menu, normal RUN/Cover/visible
   C64, F10/Quit and responsive Menu. Confirm arrows, Enter, Tab and function keys.
2. Select boot to current/default RUN machine and reboot normally. Confirm primary
   artwork releases, machine Cover appears, then visible VICE/BASIC or gameplay.
   Check input/audio. F10/Quit must restore visible, physically responsive Menu;
   there must be no repeated auto-launch loop. Repeat once. Record approximate
   startup latency. Merely finding x64sc or a foreground dialog is not PASS.
3. Before any failure recovery, retain read-only tty1 process/session/foreground,
   fd and console-state observations. Query kernel keyboard/display/VT modes using
   read-only ioctls; do not use `kbd_mode -s` as a query. Bind before/after evidence
   to the launch. Compare actual physical keyboard usability as well as mode values.
4. Abnormal-exit case: during a separately identified direct-start C64 session,
   externally terminate only x64sc with SIGTERM. Confirm it is reaped, normal Menu
   appears and physical keyboard works. Do not signal the login or Menu group.
   Stop and retain evidence if display/input fails; do not repair the candidate in
   place. Native tests additionally cover failed launch/renderer and timeout paths;
   those are not physical PASS by implication.
5. Online Library: Group=Censor, then Year, Repository and Category. Each supported
   selector must remain usable; selections must retain prior fields. Back from a
   selector preserves intent. Clear filters, choose again and make a bounded search.
   Verify metadata and a small permitted download/save. Record network errors rather
   than changing identity. Errors require explicit acknowledgment or Retry/Back.
6. Server Information stays visible until Refresh/Back. Check both actions, then
   return to Content. A failed directory call must provide readable Retry/Back;
   it must not silently switch to another server. About/support stays local.
7. Normal FILES/USB/MC navigation, manual copy, F10 and safe unmount; guided Import
   Parent/Back, readable sizes and hidden IDs. BIN remains outside generic import.
8. Capture Menu, Import and moving VICE/gameplay from SSH; compare PNG with HDMI,
   note approximate latency/audio impact and normal F10 return. Existing screenshot
   backend bytes are unchanged, but this new candidate still needs lifecycle retest.

Cover capture is a coordinated bounded engineering observation, not a change to
normal presentation duration. With owner ready to launch RUN normally, a one-shot
SSH observer may wait at most30 seconds for the fixed Cover process, then issue at
most one pcbm-screenshot. Record whether the same Cover process was active before
and after capture; inspect the PNG and compare HDMI. If it captured the following
VICE frame or missed the interval, label Cover capture NOT CAPTURED/UNTESTED, not a
KMS failure. No polling capture loop, forced delay, modeset or automatic game launch.
Repeat only as an explicitly coordinated physical test. A concise transition failure
is permissible; it is not proof that a stable Cover cannot be captured.

Report PASS/FAIL/UNTESTED per case and exact image/hardware. Attempt24's earlier
passes do not establish new-image qualification. No publication or release.
