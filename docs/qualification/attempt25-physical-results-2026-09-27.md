# Attempt25 physical results and screenshot review — 2026-09-27 UTC

PRIVATE NON-RELEASE Project CBM **1.2.0-dev.6**, attempt25, Raspberry Pi 4 Model B
Rev 1.4. Owner-reported physical results are recorded below; the agent independently
read installed identity/packages and inspected all **19** named PNGs copied from
the Pi. Source/copy SHA-256 values match. No live patch, configuration change,
new capture, launch, signal, remount or physical test was performed by the agent.

## Exact binding

- Raw: **3095396352 bytes**, SHA-256 `adc26fff5355d587547a72dcba737baab7f931d3d66ac646588151c91bb86d49`.
- XZ: **599632072 bytes**, SHA-256 `77d61462479d26593d60dbce04b1e483365e371103d53664205b97f04f17d671`.
- Installed build/lock: `52f551e722aeb6edcee31f87ccdbc376c0ef1407dcf8c63e733d482ea765ab1a`.
- Frozen Product integration: `decf2b31d2d965391e804791e26b19404b655312`.
- Menu: `5260d5332a2fb45fcb472ff9fb0f3b9fa86610fc`, package `1.2.0~dev5-1+pcbm1`.
- Runtime: `1.2.0~dev4-1`; KMS capture: `1.0.0~dev2-1`.

The retained raw/XZ were independently rehashed during this review. Installed
identity and package versions match the [frozen build record](../build/private-1.2-dev6-attempt25.json).
This associates the owner's flashed candidate with its factory image; it is not a
claim that the used, expanded SD card remains byte-identical to the original image.

## Physical matrix

| Case | Attempt25 result | Evidence and boundary |
| --- | --- | --- |
| Direct/current RUN boot preference and normal reboot | PASS | Owner: artwork releases, Cover appears, VICE visible; normal input/audio; F10/Quit returns visible responsive Menu; no repeated auto-launch loop. |
| External SIGTERM during direct-start C64 | PASS | Owner issued `pkill -TERM -x x64sc` over SSH: VICE exited, Menu returned, physical keyboard remained usable, no display/input recovery. No kernel-mode value was measured in this report. |
| Assembly64 filter UI | PASS | Owner confirms previously broken filter UI now works. No claim of exhaustive combinations or injected provider failures. |
| Assembly64 Server Information | PASS | Owner confirms usable/readable persistent view; PNG shows Central selected, directory information and Refresh/Back. |
| Ordinary FILES → MC | PASS | Owner navigation/manual copy/F10; screenshots show copy prompt, destination entry and return to Files. Safe-unmount observation is recorded with the USB lease case below; ordinary local MC does not itself require a USB lease. |
| FILES → USB → MC and normal release | PASS | Owner navigation/manual copy/F10/safe unmount; PNGs show exFAT partition, read-only workflow, copied SID at destination, release screen, success message and return to Files. |
| Moving VICE/gameplay screenshot | PASS | Owner reports no perceptible slowdown or audio interruption. Two visibly different gameplay frames retained. No instrumented frame-rate, capture latency or tear-free guarantee. |
| Normal-interval C64 Cover screenshot | PASS | PNG shows Project CBM C64 Cover; owner confirms capture without changing normal presentation timing. Not an all-machine Cover qualification. |
| Guided CONTENT Import Parent/Back/readable sizes/hidden IDs | UNTESTED on attempt25 | Earlier attempt24 PASS remains historical. None of these 19 PNGs shows guided Import. Needs one bounded reconfirmation below. |
| FILES → USB partition-picker opaque ID presentation | FAIL (presentation only) | Directly visible in `042242Z`: opaque internal tag beside friendly partition label. Separate from guided Import and from the successful USB/MC lifecycle. |
| Deliberate busy-unmount failure / failed-launch fault injection / provider outage | UNTESTED physically on attempt25 | Normal safe unmount and SIGTERM do not establish these separate failures. Retained automated coverage is not physical PASS. |

The direct-boot and SIGTERM results close the corresponding attempt24 behavioral
failures **on attempt25**. Attempt24's failure, recovery chronology and unmeasured
pre-diagnostic keyboard mode remain unchanged. The filter PASS does not retroactively
prove a precise cause for attempt24's intermittent flash/return symptom.

## What was inspected

All names below have prefix `pcbm-20260927T` and suffix `.png`. Exact bytes/SHA-256
and per-image descriptions are in the [screenshot catalog](attempt25-physical-results-2026-09-27.json).
Originals remain at the owner's screenshot directory; private retained copies are
under `qualification/attempt25-physical-results-2026-09-27/screenshots` in the configured
ProjectCBM-Work root. No captured media is added to Git or distributed with the image.

| UTC name portion | Visible evidence |
| --- | --- |
| 041526Z | Server Information, Central selection, public directory and Refresh/Back. |
| 041719Z | Project CBM C64 machine Cover centered on black background. |
| 041842Z, 041901Z, 041946Z | Files entry, ordinary MC library view and folder navigation. |
| 042042Z, 042057Z, 042131Z | Local copy prompt, destination folder present, return to Files. |
| 042242Z, 042258Z | USB partition selection with visible opaque ID; Mount Read-Only explanation. |
| 042318Z, 042343Z | USB MC root and nested source navigation. |
| 042416Z, 042429Z | SID copy prompt and SID present at destination. |
| 042450Z | Post-F10 mounted read-only screen offering Safe Unmount. |
| 042514Z, 042547Z | “USB released; safe to remove.” then Files. |
| 042956Z, 042959Z | Different C64 gameplay frames, scanlines and side margins visible. |

Still images corroborate rendered states; they do not independently prove key
handling, mount flags, successful file-byte comparison, motion, audio or response
time. Those functional PASS results are explicitly the owner's observations.
No numeric startup/capture timings, repeat-cycle count or exhaustive filter/download
retest was supplied; those measurements/subcases are not silently marked PASS.

## Remaining check and disposition

**Only one focused functional physical reconfirmation remains:** CONTENT → Import
from USB. Enter a nested source folder, exercise both Parent folder and Back,
confirm friendly names without opaque IDs in source/selection views and readable
sizes in preview/review, then End Import / release and return to responsive Content.
An Import-screen screenshot can document the remaining capture context at the same
time. No need to repeat already passed boot, SIGTERM, MC, gameplay or Cover cases.
Do not add BIN to the general allowlist or change the qualification image.

The separate FILES/USB opaque-tag issue is already evidenced; another physical
reproduction is unnecessary. Read-only comparison confirms installed scripts match
Menu source: `scripts/pcbm-import:5` enables `PCBM_UI_HIDE_TAGS=true`, whereas
`scripts/pcbm-usb-browse` does not; shared `lib/pcbm-ui.sh:70` adds `--no-tags` only
when enabled. Thus this is a remaining presentation inconsistency, not evidence
that the guided Import fix regressed. Record it for a separate source correction
and distinct candidate if taken; no correction is made in this qualification update.

Attempt25 can proceed to private engineering review with the above bounded passes,
but is **not recorded as an all-PASS candidate**: Guided Import is pending and the
FILES/USB presentation finding remains open. The fault-injection cases above,
formal timing, multi-display and other hardware are not new blocking checks for
this focused retest and acquire no PASS claim. This is not release approval.

## Preservation and recovery

Additive evidence: `qualification/attempt25-physical-results-2026-09-27`.
Additive checkpoint: `archive/attempt25-physical-results-2026-09-27`; verify its
manifest and offline bundle/refs/peeled-tag/fsck restore report. Earlier factory
checkpoint, attempt18–24 evidence, attempt25 image/packages/lock and stable1.1.0
remain untouched. Independent encrypted custody remains outstanding.
Documentation-only checks apply; source/runtime tests were not rerun for this update.
