# Attempt26: focused final 1.2.0 Pi4 check

**PRIVATE UNPUBLISHED candidate, all cases UNTESTED until reported.** Use a Raspberry
Pi4 B. Preserve the attempt25 card/evidence; use separate media and complete first
boot on the new image. No in-place update. Stop a failing case and retain evidence;
do not repair this image to obtain a pass.

Raw SHA-256: `2a5d192477eac37c819b267ca05b63d466186504c0b92230819208ad94c4f35a` (3095396352 bytes).

XZ SHA-256: `b2b7836f752d4b5b3a9a7cd5116776dff8f19eceaf4ad155b9541cc2efb69b5d` (599119848 bytes).

[Exact filenames/packages/checks](../build/final-1.2.0-attempt26.md).
First run `pcbm-info --json` and retain the build identity for attempt26 /1.2.0;
record hardware, display, storage and the image hash, without private account/network
values. Never treat earlier attempt25 passes as results for this image.

| Case | Steps and expected result | Status |
| --- | --- | --- |
| F1 USB browsing | FILES → USB Drive. Only friendly partition labels; no internal hexadecimal keys. Select the intended partition, Mount Read-Only. MC arrows/Tab/function keys work. Copy a small permitted file into the correct local library folder, F10, Safe Unmount. Confirm release/safe-removal result. | UNTESTED |
| F2 Guided Import | CONTENT → Import from USB. Choose partition/folder, exercise Parent and Back, scan a known folder. Friendly names only; sizes readable. Confirm selection/review is usable, then cancel/release normally or finish an intentional import. BIN remains unsupported as generic content. | UNTESTED |
| F3 RUN | RUN → normal Cover → visible VICE. Exercise keyboard and audio using known permitted content. F10/Quit returns to responsive Menu. | UNTESTED |
| F4 Direct boot | CONTROL → Machine and Startup → Boot preference → Default emulator. Reboot normally: boot artwork releases, Cover then visible VICE, input/audio normal. F10/Quit returns to responsive Menu without another automatic launch. Restore Menu boot afterward if desired. | UNTESTED |
| F5 Assembly64 | CONTENT → Online Library; search, change a filter, open details, select one small permitted download/save or exercise Already Present. Saved content appears locally. Server Information remains readable until Back. | UNTESTED |

For F1/F2, `pcbm-screenshot` over SSH is useful evidence of the corrected choices;
copy the returned PNG from `/home/pcbm/content/screenshots/` to engineering storage.
Do not include credentials or personal filenames in public evidence. Screenshot
capture and the earlier full attempt25 physical evidence remain recorded separately;
no need to repeat an extended gameplay/capture campaign for this presentation change.
Normal Safe Unmount is required here. Deliberate physical busy-unmount fault injection
is not requested; its native automated test passes and prior physical uncertainty remains.

Report F1–F5 PASS/FAIL against this raw hash, plus any unexpected display, keyboard,
audio, network or exit behavior. No formal timing campaign is required; note visible
lag/regression. Publication is authorized only after all five PASS, all automated
checks remain clean, and the final release audit completes. Other Pi models are not
qualified by this Pi4 result.
