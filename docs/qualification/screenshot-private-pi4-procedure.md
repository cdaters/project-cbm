# Private screenshot / guided-import Pi 4 qualification

Status: procedure prepared; physical results UNTESTED. Use only the new private
candidate and exact hashes in its build record. Never patch or reflash the retained
attempt18/attempt19 qualification artifacts. Product1.1.0 stays stable/published;
this is provisional1.2 private engineering, not a release or support expansion.

After the owner flashes a separate card, verify `pcbm-info --json` against the
candidate's Product/Menu/Runtime/capture identities. Complete normal setup and
explicitly enable SSH. Keep ordinary authenticated owner administration unchanged.

From the engineering Mac, run the following when the requested screen is visible:

```sh
ssh pcbm@projectcbm.local 'time pcbm-screenshot'
```

Record the printed absolute PNG path and elapsed time. Copy that exact file to a
private engineering evidence folder on the Mac with `scp`. View the PNG and compare
it with the HDMI image. Screenshots may contain private filenames or messages;
review before sharing. Do not capture passwords. The command creates only local
files; there is no automatic upload.

| Case | Screen and check | Initial result |
|---|---|---|
| S1 | Main Menu, colors and complete image | UNTESTED |
| S2 | Ordinary text console; cursor/text match | UNTESTED |
| S3 | FILES → Midnight Commander; arrows/Tab/function keys/F10 still work | UNTESTED |
| S4 | CONTENT → Import from USB → source folder/file chooser; only friendly labels visible, no opaque IDs; select intended entry and cancel/release safely | UNTESTED |
| S5 | FILES → USB Drive → partition → Mount Read-Only → MC; screenshot and navigation; F10 → Safe Unmount | UNTESTED |
| S6 | Machine Cover during RUN transition; note unavailable/transition errors and retry once if necessary | UNTESTED |
| S7 | VICE/BASIC, border/colors/full canvas; capture leaves display unchanged; F10 returns to responsive Menu | UNTESTED |
| S8 | Moving C64 gameplay; compare a recognizable frame, note capture latency and any visible/audio disruption; F10 return | UNTESTED |
| S9 | Five repeated explicit captures; unique complete PNGs, no overwrite, unchanged display/lifecycle | UNTESTED |
| S10 | No active HDMI display, using the owner's chosen safe disconnect/shutdown sequence; concise unavailable error, no named partial PNG | UNTESTED |
| S11 | Explicit capture near Cover/VICE/Menu transition; either correct complete image or concise unavailable error, no stale misleading composition or lifecycle damage | UNTESTED |

Record hardware revision, display resolution, exact raw/XZ hash, selected machine,
PNG hash, elapsed time and HDMI comparison for each applicable case. A clear
unsupported-configuration result is a bounded limitation, not a successful capture.
Do not claim multi-display support. Do not repair the image if a case fails: retain
screen/error/PNG evidence and stop the affected case.

Also repeat the ordinary MC/USB/manual-copy/safe-unmount/copied-content/C64/F10
lifecycle from attempt19. Test guided import with duplicate/similar folder labels,
confirm correct selection despite hidden IDs, and retain `.bin` exclusion. Normal
safe-unmount already passed on attempt19; deliberate busy-unmount fault injection
is distinct and remains untested physically. Automated busy/error cleanup does not
convert that to a physical pass. Formal obsolete scan/import timings are not needed;
record actual source-list, scan, copy/release responsiveness and screenshot latency.

For output privacy, inspect `stat -c '%U %a %n' ~/screenshots ~/screenshots/*.png`
(private output only), expecting pcbm/700 and pcbm/600. An explicit existing basename
must fail without changing its prior hash. `pcbm-screenshot ../bad.png` must fail.
No root command, DISPLAY setting or DRM IDs should be needed by the operator.
