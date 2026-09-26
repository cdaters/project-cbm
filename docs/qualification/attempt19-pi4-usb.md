# Attempt19: Pi 4 USB terminal qualification

**Guided Import follow-up:** CONTENT Import is physically confirmed present. Nested
folder navigation, supported `.prg` / unsupported `.bin` filtering, explicit machine/
category, selected-file Import and safe release PASS for the reported observations.
Opaque identifiers visible beside folder names are a separate **presentation FAIL**.
See [the bounded result and source correction](attempt19-guided-import-2026-09-25.md).
The full U1–U6 fixture matrix is not thereby passed or superseded; earlier blanket
UNTESTED wording below predates this report. Attempt19 remains unchanged.

**Owner physical update — September 25:** B0/B1 PASS for reported normal/USB MC
navigation, read-only mount, copy and safe release. Copy → C64 demo → F10 → responsive
Menu also PASS. See the [exact attestation and remaining cases](attempt19-pi4-owner-pass-2026-09-25.md).
U1–U6/B2/T1 and full R1 remain UNTESTED beyond the reported subset. Unreported detailed
B0/B1 substeps remain UNTESTED. The pre-test status and procedure below are historical
expectations, not a claim that all steps have now passed.

**PRIVATE NON-RELEASE — physical UNTESTED.** This procedure binds only the new
Project CBM `1.2.0-dev.2` / `private-engineering-1.2-dev2` attempt19 image.
Attempt18 remains **B1 FAIL**, preserved without repair. Stable 1.1.0 is unchanged.
Owner flashing/testing is the next action; no physical PASS follows from native tests.

## Verify the candidate

Use a separate microSD card; retain the attempt18 card, stable card and user backups.
[Build record](../build/private-1.2-dev2-attempt19.json) supplies source/package identity
and recovery at `archive/private-1.2-dev2-attempt19-2026-09-25` under registered bulk
storage. Verify its manifest and restore report before testing.

Both artifacts are in `artifacts/private-1.2-dev2-attempt-19` under that bulk root:

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `2026-09-26-project-cbm-1.2.0-dev.2-lite-private-1.2-dev2.img` | 3,095,396,352 | `f69fbee34448936d9df942ab0c8ce990b9ccd3a85e66b95d232f0d7c8caa8d44` |
| `image_2026-09-26-project-cbm-1.2.0-dev.2-lite-private-1.2-dev2.img.xz` | 599,040,204 | `00e88150f5d2105f89182e14e14ed27517a672cb57c6134598dcfa451dfe0fca` |

Check the selected file with `shasum -a 256` (Mac) or `sha256sum` (Linux), then flash
only the separate owner-selected card. Complete first boot. From the ordinary terminal:

```sh
pcbm-info --json
dpkg-query -W project-cbm-runtime project-cbm-menu
cat /etc/pcbm/engineering-poc
```

Expect Runtime `1.2.0~dev2-1`, Menu `1.2.0~dev1-1+pcbm1`, the product/candidate above,
and build ID `1b69db05988dc3435b3460eb045a91c7dcca4fcfe7a7d8b3eebb846e2c2d37ce`.
A mismatch is BLOCKED. Record image hash, hardware/RAM, keyboard/display, power supply,
card capacity and USB filesystem privately. Do not post device/network identifiers.

## B0 — Ordinary FILES baseline

Without USB mounted, use the ordinary FILES → Midnight Commander path. Verify Up,
Down, Tab, F3 viewer/return, F9 menu/dismissal and F10 exit. Open only a harmless text
file for F3; do not edit files. Confirm return to Menu and responsive navigation.
Record PASS/FAIL. Failure here stops the USB comparison for evidence collection.

## B1 — Exact failed workflow, corrected candidate

Use the same known-good partition from attempt18 where possible. No formatting,
repair, write or fixture change is required. The original optional fixture preparation
is in [the USB/content procedure](content-1.2-pi4-usb.md#prepare-original-test-media).

1. FILES → USB Drive → select the actual USB partition → Mount Read-Only.
2. In MC, press Up/Down several times: the highlight must move, without literal
   escape characters. Tab must change the active panel between USB and the library.
3. Use F3 on a harmless text file if present, then F10 to leave its viewer. Verify
   F9 opens MC's menu and Escape dismisses it. Do not rename/delete/edit/copy USB data.
4. Press literal Ctrl+C and record the behavior. MC handles its own keyboard and can
   consume Ctrl+C; it is **not required to exit**. Continue arrows/Tab and F10 normally.
   Signal cleanup is a separate test below; MC commonly maps VINTR to Ctrl+G.
5. F10 from MC must return to the mounted USB choices. The drive is still mounted
   here: do not remove it. Choose Browse Read-Only again and repeat navigation/F10.
6. Choose Safe Unmount. Expect a verified release message. Check no browse mount
   remains using the read-only checks below. Only then remove/reconnect the drive.
7. Repeat a complete mount/browse/F10/release cycle. Recheck ordinary FILES MC and
   Menu input. Record B1 PASS only for the exact image and observed steps.

During MC, an existing SSH session or local tty2 can collect read-only evidence:

```sh
ps -eo pid,ppid,sid,pgid,tpgid,tty,stat,args
findmnt --mountpoint /run/project-cbm/import/browse -o TARGET,SOURCE,FSTYPE,OPTIONS
```

The mount must include `ro,nodev,nosuid,noexec`. For the identified MC PID, inspect
`/proc/PID/fd/0`, `fd/1`, `fd/2` with `readlink`. All must resolve to its caller's
console (`/dev/tty` is an alias); MC PGID must equal that terminal's TPGID and share
its caller's session. A root sudo broker may still have an inner PTY; MC must not.
Capture only allowlisted environment fields if needed, never the whole environment.
Return tty2→tty1 with Ctrl+Alt+F1; switching VT does not itself end the lease.

After release, `findmnt --mountpoint /run/project-cbm/import/browse` must produce no
row (exit 1 means no matching mount). Check the process list for orphan MC/broker
processes. Directory existence alone does not mean a mount remains. No successful
release claim may appear if unmount failed.

## B2 — Cancellation and failure cases

First test Back/Cancel before mounting, and Back after F10 from MC. The latter must
attempt release; inspect the mount afterward. Normal MC and Menu must remain usable.

Native installed-path tests already exercise foreground SIGINT, HUP, PTY disconnect,
bridge/worker crash, no orphan MC, no leaked lease and truthful busy-unmount failure.
Those are **not physical results**. Do not kill an arbitrary PID, unplug a mounted
USB, reboot as a substitute for evidence or force/lazy-unmount it. If controlled
on-Pi fault injection is desired, leave MC open and coordinate exact live PIDs with
read-only inspection first; mark unperformed physical fault cases UNTESTED.

An optional busy-unmount case should be last and coordinated: another normal-user
process deliberately holds a cwd on the read-only browse mount. Release must report
failure and tell the owner to leave the drive connected until safe shutdown, never
claim safe removal. Do not create this holder casually or apply a manual repair to
make the candidate appear to pass. Retain evidence before any recovery.

## Regression and reporting

After B0/B1/B2, exercise RUN → Cover → VICE → F10 → Menu and repeat USB browse. This
checks the physical lifecycle intersection; screenshot capture is not in this image.
For broader content qualification, use U1–U6, B1–B2, R1 and T1 from the original
[USB/content procedure](content-1.2-pi4-usb.md), substituting only this candidate's
identity and a fresh evidence directory (for example `usb-qual-dev2`). Its attempt18
identity/status remains historical. Cases not performed stay UNTESTED.

Report each case as PASS/FAIL/UNTESTED/BLOCKED with exact image hash. On failure,
stop that case, leave the USB connected if release is uncertain, and preserve the
screen/process/mount observations. Do not patch this image or weaken protections.
No physical result or performance/support claim transfers from a different candidate.
