# Cover qualification addendum — awaiting a new candidate

**Do not use POC4 attempt #2 to qualify covers.** It predates this source correction.
Before testing, replace this pending binding with the next approved frozen candidate's
Menu version/peeled commit/package hash, release-lock hash, raw/XZ hashes and exact
full Pi 3B test procedure. Never add covers to a flashed/frozen image manually.

Use the full first-boot/runtime and POC3 regression procedure as well as these checks.
No physical result is claimed here; every row starts UNTESTED.

| Test | Expected observation | Result |
| --- | --- | --- |
| RUN with C64 default | Existing C64 Project CBM cover, then x64sc | UNTESTED |
| Additional profile (VIC-20 suggested) | Select using MACHINES, RUN shows matching cover and VICE machine | UNTESTED |
| Explicit machine launch, where exposed | Cover follows selected profile | UNTESTED |
| C64-forced CONTENT application with other default | C64 cover; default preference unchanged | UNTESTED |
| Cover presentation | Proportions reasonable, no stretching/cropping; short transition | UNTESTED |
| VICE handoff | No stale cover, black-screen lockup or incorrect VICE geometry | UNTESTED |
| Keyboard and tty1/tty2 | Input and console switching still work | UNTESTED |
| F10 → VICE menu → Quit | Clean, usable Project CBM Menu | UNTESTED |
| Repeated launch | Correct cover, VICE and return again | UNTESTED |
| Audio and original qualification media | Existing regression behavior preserved | UNTESTED |

Restore the intended default machine through MACHINES after the additional-profile test.
Do not change display/VICE settings to repair a failure. If handoff fails, use tty2 and
the candidate's diagnostic snapshot procedure, retain the launch record and stop.
A missing cover with successful VICE launch is a cover failure, not a VICE failure.
Record machine/profile, monitor mode, whether artwork appeared, duration impression,
transition, VT/input and return separately. Photos establish visible artwork/geometry;
timing, input, audio and return remain operator observations unless separately captured.

This tests machine-launch COVERS only. Rainbow/kernel messages and system boot splash
remain outside scope. No new model or broader machine qualification is implied.
