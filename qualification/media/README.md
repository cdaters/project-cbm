# Project CBM qualification media 0.1.0

Original MIT-licensed BASIC V2 diagnostics. Build with Python's standard library:

```sh
python3 qualification/media/build.py EXTERNAL_OUTPUT --revision FULL_SOURCE_COMMIT
```

The output directory must not exist. The build produces three PRGs, one 35-track
D64 and a deterministic archive with per-file hashes/license/source revision.
Do not commit generated binaries. The source commit, archive hash and private
engineering profile become declared release-lock inputs before image construction.

Use CONTENT → Programs/Music/Demos → Qualification, with default machine C64/x64sc.
Read each program's on-screen instructions. Smoke should print a successful load/
execution message and arithmetic result 4. Audio should play three separate original
SID tones (triangle, saw, pulse); it is mono, not a stereo-channel or SID-file-player
test. Video/input shows 16 color cells, a moving star, changing key codes and joystick
port 2 states. Lack of a joystick means UNTESTED. D64 contains the same smoke PRG.
F10 opens VICE's menu; select Quit emulator and confirm to return to CBM.

Structural and determinism tests are implemented. Independent runtime validation
is **pending**, so the suite must not yet be described as known-good C64 software.
Record later reference emulator/version/configuration and observed results separately.
The license permits redistribution, but product inclusion is initially private
engineering only; decide public examples/diagnostics later on their demonstrated value.
