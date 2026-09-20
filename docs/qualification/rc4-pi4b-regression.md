# Pi 4 B RC4 final release-polish qualification

**READY FOR OWNER PHYSICAL TEST: YES after the referenced recovery manifest verifies PASS.**
One image was built. RC3 is unchanged. [Complete candidate report](../build/private-rc4.md).

## Exact candidate identity

Project CBM **1.1.0-rc.4**, attempt **14**, `private-engineering-rc4`.
Frozen lock SHA-256: `ced936a75aebf2f45d30052da85ba35f00fe9881d0d59f1938b1d64c84c1d5df`.
Integration: `b723bc9b57d9adc38a4c19ca25982b3ccae65301`.

Paths are relative to the configured bulk workspace (currently `/Volumes/TheBench/ProjectCBM-Work`).

**RAW**: `artifacts/private-rc4-attempt-14/2026-09-20-project-cbm-1.1.0-rc.4-lite-private-rc4.img`

- Bytes: 3,095,396,352
- SHA-256: `9b9db76e42141ad1043cfaeef2ba148ca9e7dbd034de51b4555b5852f0d4a893`

**XZ**: `artifacts/private-rc4-attempt-14/image_2026-09-20-project-cbm-1.1.0-rc.4-lite-private-rc4.img.xz`

- Bytes: 599,761,028
- SHA-256: `f87e0c6fec6a0199974fd77d9624a1d0e851f0e35d1bf1e4577aa852ba79c658`

Raw/XZ equality passes in Linux and independently on the external Mac copy. All
324 actual-image checks pass, including 672 package identities and 127 ELF objects.
Recovery: `archive/rc4-2026-09-20`; verify its `manifest.json.sha256` and PASS restore
report before flashing. This is a private candidate, not a published final release.

On macOS verify the selected download before flashing:

```sh
shasum -a 256 "$CBM_IMAGE"
```

Set `CBM_IMAGE` to one exact path above; compare with its corresponding hash. Flashing
erases the selected card. The raw image and XZ expand to the same image bytes.

## Scope and safety

This procedure targets **Raspberry Pi 4 B**. RC4 changes CCGMS composition/serial
launch options, G71 and dot-prefixed discovery, the File Sharing password prompt and
notices. Retain prior owner-reported PASS evidence for unchanged behavior; this is not
a request to repeat broad Pi4 performance benchmarking. No other model gains qualification.

Back up content and saved settings before flashing; preferably use a separate card.
Do not repair the qualification image in place if a core regression appears. Stop,
record the visible error, preserve the matching launch/boot diagnostics and report it.
Do not publish passwords, saved BBS credentials, private network data or SSH keys.

## Boot and core smoke regression

1. Boot the exact candidate. Check Project CBM artwork → first-boot setup → Main Menu,
   usable keyboard, password masking and network setup. On the next boot, setup must
   not rerun; primary artwork should hand off to Menu without routine Saving configuration
   or successful filesystem/login output. Display-generated HDMI OSD is separate.
2. Check Main Menu's default machine, network and service state. Check tty2/F1 return
   from Menu. RUN C64: correct Cover → BASIC → F10 → Quit → responsive Menu. Repeat
   once. VICE-active VT switching retains its accepted limitation.
3. Check network/service sanity using the previously working configuration: correct
   Computer Name/IP/gateway/DNS, Remote Access/File Sharing state and ordinary connection.
   Use the unified `pcbm` account and `/home/pcbm/content`. Do not assume broad new
   performance failure from ordinary loading; if a real regression appears, preserve
   diagnostics and health measurements before changing settings.

## CONTENT and USB changes

4. Copy a small test set you may use to USB: an ordinary supported D64/PRG, a legitimate
   dot-prefixed media file and a supported file inside a dot-prefixed folder. Include
   known macOS metadata only if already present, or harmless synthetic `.DS_Store`/`._`
   companions. IMPORT → device → C64 → Games. Read the result and removal guidance.
5. Confirm intended content is under `games/c64/Imported`, with meaningful content-file
   counts. Known metadata must be absent. Both legitimate dot-prefixed examples must
   appear in CONTENT and launch with compatible software. Repeat import: existing
   files are preserved. Remove the drive only after successful unmount guidance.
6. If you have suitable G71 media, place C64 media in `games/c64`, C128 media in
   `programs/c128` (or its `80col` folder as appropriate). Confirm CONTENT lists it and
   the matching machine can load it using a 1571. Do not use a C64-only program as
   proof of C128 native-mode compatibility. If no suitable media is available, record
   physical G71 **UNTESTED**; native synthetic C64/C128 evidence is retained separately.
7. File Sharing → Set File Sharing password must visibly say **colon (:) is not accepted**.
   Confirm an otherwise valid password containing colon is rejected without exposure,
   then set a valid separate password and connect using username `pcbm`. Do not include
   the password in the result report. Account password rules are unchanged.

## CCGMS: required affected-area qualification

8. CONTROL → Services → BBS / Modem: turn it on, initial modem port **25232**, speed
   **2400 baud**. It must report actual On. No public incoming BBS listener is intended.
9. CONTENT → PROGRAMS → `c64/Communications/CCGMS/CCGMS-2021.d64`. Confirm the C64 Cover,
   CCGMS Terminal 2021 title, normal keyboard and no unrelated compilation utilities.
10. In CCGMS press F7. Set **Swift / Turbo DE**, **2400**, **Standard**, **Full** duplex.
    Return to the terminal. Type `AT` and Return; require `OK`.
11. Use a known BBS you are permitted to access or an owner-controlled local endpoint.
    Type `ATDT<hostname>:<port>` with its actual hostname and port, then Return. Require
    CONNECT, readable received text and successful text sent from CCGMS. Record endpoint
    type, settings and result without credentials. Native loopback success alone is not
    this physical qualification.
12. Log off at the BBS. For local hangup: pause at least a second, type `+++` without
    Return, pause at least a second, then `ATH` and Return. Confirm disconnect/NO CARRIER.
    Save CCGMS settings using F7 → S, retaining the prompted `CCGMS-PHONE` filename if
    desired; confirm a writable working disk and no permission error.
13. F10 → Quit must return promptly to a responsive Project CBM Menu. Relaunch CCGMS,
    confirm saved settings if saved, and repeat AT/connection/disconnect. Turn BBS / Modem
    off after use and verify actual Off. Ordinary RUN C64 must retain its previous
    non-terminal behavior and default selection.

## Report and stop

Report each affected area as PASS / FAIL / UNTESTED / BLOCKED, bound to the image hash
and Pi4 B. A successful launch is not a successful BBS connection. Do not require every
optional check before reporting a critical boot, input or lifecycle regression.

The release decision requires the affected CCGMS workflow and core smoke regression,
a disposition of any failed/untested changed area, and retained existing qualification.
Do not publish/tag the final release from this procedure. Stop for owner review.
