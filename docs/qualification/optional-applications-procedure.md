# Optional applications: later-candidate physical checks

**Procedure only, 2026-09-16. Not authorization to test or modify POC1–3.**
Before use, bind this procedure to a newly approved image's raw/compressed SHA-256,
frozen lock digest, Menu/product versions and optional-software input. No such image
is built by the current source pass. Start with the Pi 3B gate; other hardware is
not inferred qualified.

## SID-Wizard core

Expected prepared D64: 174,848 bytes, SHA-256
`cec93ae1fd5fc846507c1883fd9cb210c6a3c0f40c1c081964e3b8450e26dc44`.
This hash describes the initial copy; user saves legitimately change the working disk.
The immutable template and frozen input retain the original identity.

1. Record candidate identity, Pi model/display, C64 model, PAL/NTSC, SID model and
   drive configuration. For an initial test use the candidate's documented single-SID
   C64 settings; do not silently normalize a user's prior VICE preferences.
2. Boot to Menu; verify tty2 recovery and return. Choose a different ordinary default
   machine if the approved test permits preference changes, to exercise the override.
3. Discover **CONTENT → MUSIC → Creation/SID-Wizard/SID-Wizard-1.97.d64**.
   Confirm the native tracker appears under x64sc with correct geometry/full canvas.
   Capture visible version; do not confuse the upstream `1.9` filename with archive 1.97.
4. Check keyboard navigation and editing. Following upstream native instructions,
   create a simple original instrument/note pattern and listen. Record the actual
   settings/actions and observable tone; incomplete audio work stays UNTESTED.
   Do not use a copyrighted example tune as the test fixture.
5. Where practical save that original work onto the working disk, reopen it and
   check retained notes. Record Save/Reopen separately from launch and audio. SID-Maker
   export is an additional explicit test, not inferred from merely including its PRG.
6. F10 → VICE menu → Quit → responsive Project CBM Menu. Confirm the ordinary
   default-machine preference has not changed. Confirm tty2 still works.

Check the owner notice exists under `/usr/share/doc/project-cbm-sid-wizard/` and the
working copy is user-owned. Do not overwrite songs with the template during normal
launch or recovery. No claim of SID fidelity, multi-SID support, all PAL/NTSC modes,
MIDI hardware or full composition workflow follows from these bounded checks.

## StrikeTerm, only with an authorized owner copy

Record owner-supplied acquisition source, exact disk SHA-256/size and its private
custody location outside Git. Do not embed the disk into the already-frozen candidate.
Use a procedure that explicitly permits normal user-content transfer; this is
external reference input, not a retroactive change to base identity.

1. Place a standard D64 under `programs/Communications/StrikeTerm/` using an available,
   approved transfer method. An absent file should produce no dead main-menu item.
2. Discover it under CONTENT → PROGRAMS. Confirm validated x64sc launch, complete
   geometry, application screen and keyboard. Do not dial a real BBS in this test.
3. F10 → Quit → responsive Menu; ordinary default unchanged. Capture diagnostics on
   failure without editing system configuration.
4. Keep serial/TCPser/network enablement, bridge setup, handshake behavior, dialing,
   authentication and file transfers **UNTESTED** until separately authorized.

If either application fails, record what passed, failed and remained untested,
collect bounded engineering diagnostics and stop that test. Never repair the running
qualification image or infer another Pi/model/software version passed.
