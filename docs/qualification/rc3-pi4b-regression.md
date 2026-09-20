# Pi 4 B RC3 presentation and USB regression

This is a PRIVATE engineering candidate. Follow only the exact raw/XZ identity
recorded below. Hardware is Raspberry Pi 4 B; no other model gains qualification.
Do not overwrite the tested RC2 card until its relevant evidence/content is safely
retained. Use a separate card where available. The engineer has not flashed a device.

## Exact candidate identity

Attempt 12; Project CBM 1.1.0-rc.3; private-engineering-rc3.
Lock SHA-256: `bbcf02a56403c8f19bd42304f985cd5202ac797311a9ddf4cad5ea2eb79e665d`.
Integration: `ece07f04c396c1530a179a5980a41b9b0e8a81b9`.

Paths are relative to `/Volumes/TheBench/ProjectCBM-Work`:

**RAW**: `artifacts/private-rc3-attempt-12/2026-09-20-project-cbm-1.1.0-rc.3-lite-private-rc3.img`

- Bytes: 3,095,396,352
- SHA-256: `5bde293b5ec6096e2a3bb2f9b31f123a8a07fdc6ac1f9077b510a4ceb5a1702e`

**XZ**: `artifacts/private-rc3-attempt-12/image_2026-09-20-project-cbm-1.1.0-rc.3-lite-private-rc3.img.xz`

- Bytes: 599,157,232
- SHA-256: `ca9f21d6bcfa3cae46921bbc4cd93663e9c7800832a173546d1181789ca8d15b`

Raw/XZ equivalence and 305 actual-image checks PASS. The recovery checkpoint is
`archive/rc3-2026-09-20`; verify its external manifest/restore PASS before flashing.
See the [complete build report](../build/private-rc3.md).

## Before flashing

Verify the chosen artifact's SHA-256 on the Mac:

```sh
shasum -a 256 "$CBM_IMAGE"
```

Set `CBM_IMAGE` to the exact path below, not a filename guessed from older candidates.
Verify size/hash, then flash with your usual tool. Keep owner content backed up;
third-party reference workloads are owner-supplied, not added to the image.

## Fresh image and startup

1. Start a stopwatch at power-on. Note the first meaningful Project CBM artwork,
   the first setup screen, and interactive Main Menu separately. Photograph any
   unexpected text in order. RC2's reported 20–23 seconds was to meaningful activity;
   do not compare it indiscriminately with a different endpoint.
2. Expect early black/video-establishment time, then primary artwork covering routine
   session preparation. Artwork should remain at least about 3 seconds after it becomes
   visible, or until setup/Menu is ready if longer. Display-generated HDMI timing or
   input overlays are separate; do not score those as Linux output.
3. Fresh boot should go artwork → First Boot Setup → Main Menu. Complete region,
   password and Wi-Fi normally. Password masking, readable ranges and first scan must
   remain usable. A second startup splash after setup is a regression.
4. On subsequent boots expect artwork → Main Menu, without routine filesystem-clean,
   automatic-login/IP, startup prose or Saving configuration dialogs. Setup must not
   rerun. Corrected filesystem errors or actionable failures intentionally remain visible.
5. Confirm the Menu accepts keyboard input and concise current network/service state
   is correct. Check Ctrl+Alt+F2 and Ctrl+Alt+F1 before launching an emulator.

## Core lifecycle and performance

6. RUN Commodore 64, correct machine Cover, x64sc, BASIC sanity, F10→Quit and responsive
   Menu return. Repeat at least three cycles. Check another machine/profile and its
   correct Cover. Check tty switching again after VICE. The existing VICE-active VT
   limitation remains separate; no new PASS is inferred for it.
7. Load the owner-supplied `kong_arcade_oxyron.prg` under normal x64sc. Expect normal
   audio/music and graphics speed on Pi 4 B. Leave a settled non-warp workload for at
   least 60 seconds; preserve the corresponding launch telemetry. No new default/core
   or SID change is introduced. Use the existing performance contract: 12 consecutive
   complete non-warp samples spanning at least 60 seconds, weighted speed 98–102%,
   minimum complete sample at least 95%, and plausible PAL emulated FPS around 50.
   Owner audiovisual judgment remains required. Engineering selects/parses the actual
   interval; do not include F10, loading, warp or quitting intervals in that window.
8. Confirm same account `pcbm`, home `/home/pcbm`, library `/home/pcbm/content` and FILES
   access. Existing preferences/content must stay visible through normal workflows.

## USB count and preservation

9. Use a USB drive containing one ordinary folder with exactly three intended D64
   files. Existing macOS metadata may remain; no need to erase or clean the source.
   If it contains other legitimate supported media, list that expected content first.
10. IMPORT → drive → Commodore 64 → Games. Wait for the persistent result. On a fresh
    destination expect **3 content files copied** for that three-file source. Known
    metadata/Trash must not appear as content or increase the copied-content count.
    Ignored metadata is reported separately. The target is
    `/home/pcbm/content/games/c64/Imported/<original-folder>`.
11. Inspect through CONTENT/FILES or File Sharing. Check those three files and their
    folder, without `._` companions or imported Trash. Other legitimate hidden media
    is not categorically excluded. Optional broader media checks can include PRG,
    tape and cartridge files; SID files retain their music/c64 routing.
12. Repeat the same import. Expect 0 new files and the existing content preserved.
    Confirm the completion screen says the source was unmounted before removal.
    On any failure, follow its release guidance; do not pull a drive whose release
    was not confirmed. No source repair or writable import mount is authorized.

## Services and repeated boot

13. Verify Wi-Fi connection/persistence, Computer Name, IP and detailed gateway/DNS.
    Check Remote Access and File Sharing using pcbm and the existing separate sharing
    password model. Enable/disable state and connection help must remain accurate.
14. Safely reboot twice. Record artwork/order/timing, Menu responsiveness, completed
    setup staying complete, Wi-Fi and selected service-state persistence. Check USB
    import/FILES again if its first result was ambiguous. Optional applications may
    receive focused smoke tests without blocking immediate reporting of a core fault.

## Evidence and stop conditions

If a core regression appears, stop that physical sequence and preserve evidence
before changing settings or reflashing. Report PASS/FAIL/UNTESTED individually.
SSH as pcbm can read its own boot traces and launch diagnostics; no pi password or
permission weakening is needed. Do not send passwords, keys or full private logs.
The engineer can collect allowlisted numeric data through the authenticated alias.

Relevant paths:

- `~/.local/state/project-cbm/boot/boot.*.tsv`: numeric uptime and fixed phases;
  dialog_dispatch means dispatch, and first_input means completed first interaction.
- `~/.local/state/project-cbm/diagnostics/primary-presentation.json`: readiness,
  renderer events and verified terminal restoration.
- `~/.local/state/project-cbm/diagnostics/launch-*/vice.log`: performance records;
  collect only the needed launch and numeric fields under the private evidence policy.

Use System Information for exact installed identity. This candidate must match the
lock below. Keep photographs/diagnostics outside Git and hash/caption relevant files.
Verbose recovery instructions are in the shipped release boot/recovery guide. Preserve
qualification evidence before editing `cmdline.txt`; do not repair the tested artifact
in place to conceal a failure. Stop after reporting this Pi 4 B qualification.
