# Project CBM 1.1.0 — owner Pi 4 B final smoke test

Status: **UNTESTED** for this final image. RC4 attempt14 is the owner's accepted
technical basis. This brief check confirms the final image's fresh installation and
unchanged core lifecycle; it does not reopen broad RC4 qualification or add other models.
[Preparation results](../build/final-1.1.0.md) · [Exact identities](../build/final-1.1.0.json).

## Verify the release set

Files below are relative to configured bulk storage, currently
`/Volumes/TheBench/ProjectCBM-Work`. Use `releases/1.1.0/`:

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `project-cbm-1.1.0.img.xz` | 599,290,700 | `8b3738a204da16e148f5674a95f1ffb55a67b8ad1ce1d997b1858594a899c13d` |
| `project-cbm-1.1.0.img` | 3,095,396,352 | `6c9b7599461a41f6ab30b666dd718329c34f863f11a46dfd20d61fe9830d2468` |

Both files represent the same raw image. Before flashing, verify staged `SHA256SUMS`
and `archive/final-1.1.0-2026-09-24/manifest.json.sha256`; the recovery
`restore-report.json` must report PASS. On macOS, from the chosen directory:

```sh
shasum -a 256 -c SHA256SUMS
```

The frozen lock hash is
`68d59a178f723c6648191b0af080c0c83b9ad60997ff4d59f4619c6d2b4a2810`.
Use a backed-up or spare card large enough for the exact raw image and your data.
Flashing erases the selected card. Follow [Getting Started](../release/getting-started.md).
The agent has not flashed or tested physical hardware.

## Minimal smoke procedure

1. On the **Raspberry Pi 4 B**, boot the exact final image. Confirm startup artwork,
   readable first-boot setup, working keyboard, masked password entry and successful
   region/keyboard/timezone/network choices. Confirm normal arrival at Main Menu.
2. Open system information. Confirm Product/Menu **1.1.0**, expected machine selection
   and truthful network/service state. Confirm storage expansion reports usable space
   for this card; report the card capacity and observed available space.
3. RUN the normal C64 profile. Confirm the C64 Cover, complete aspect-preserving BASIC
   canvas, working input, and **F10 → Quit** returning to a responsive Menu. Repeat once.
   Briefly check familiar audio with the retained qualification music or your known media.
4. Open CONTENT and confirm CCGMS and SID-Wizard are present in their expected folders.
   Launch CCGMS; with BBS / Modem deliberately enabled, use the accepted Swift / Turbo DE,
   2400 baud settings and confirm `AT` → `OK`. Return with F10 → Quit and relaunch once.
   The RC4 accepted connection workflow remains the technical basis; repeat a familiar
   BBS connection if convenient or if this smoke suggests a regression.
5. Reboot through the Menu. Confirm setup does not repeat, the saved selections survive,
   startup hands off cleanly, and RUN/return still works. Shut down through POWER.

Use [the RC4 procedure](rc4-pi4b-regression.md) only to investigate an affected area.
Do not repeat broad benchmarking, add new hardware qualification or change the image
to repair a failed smoke test. Stop a failing test and retain the error and matching
diagnostics; exclude passwords, private endpoints, Wi-Fi details and keys from reports.

## Owner report

Report the exact XZ or raw hash, Pi 4 B/RAM, card capacity, and each step as
PASS / FAIL / UNTESTED / BLOCKED. Include observed available storage and concise failure
details if relevant. No individual result is assumed from RC4's overall acceptance.

After reporting, stop for release disposition. This procedure does not authorize a
public push, upload, GitHub Release or publication.
