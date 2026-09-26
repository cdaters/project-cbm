# Attempt20 owner physical review — 2026-09-26

PRIVATE NON-RELEASE, Raspberry Pi 4 B. Exact Product 1.2.0-dev.3 / attempt20:
raw SHA-256 `014e9598453e9361984559ac060583dbfb76947ba51206d704c6773e2175d330`.
[Immutable identities](../build/private-1.2-dev3-attempt20.json).

Owner-reported PASS: ordinary MC; FILES USB partition selection, read-only mount,
arrows/Tab/function keys, manual copy, F10, normal Safe Unmount; copied demo launch
in C64, VICE F10 and responsive Menu; normal reboot/shutdown/runtime behavior.
Guided CONTENT Import PASS: partition/source navigation, Scan/Preview/Select/Review/
Import, explicit category/machine, PRG supported, BIN unsupported including zero-
supported scans, explicit selected-file import and safe release. Opaque internal
IDs are now physically hidden: attempt19 presentation defect fixed in attempt20.

Screenshot command works on the Pi. Owner reports approximately 0.36–0.39 seconds
for tested captures, without identifying every screen covered. Eleven existing
PNGs were copied read-only and SHA-256 matched to the Pi; originals remain untouched.
Private evidence: `qualification/attempt20-physical-review-2026-09-26` on registered
external storage. Screenshots contain local information and are not committed.
They show Main Menu, ordinary MC, partition/source navigation, zero-supported and
mixed-supported Import previews, safe-release messages and a three-disk preview.
Review confirms readable images and hidden IDs; PNG inspection alone does not prove
HDMI correspondence, audio impact, gameplay behavior or a capture during transition.

UX findings retained: raw `59850 MiB`, generic titles, zero-supported selection
controls and Back leaving the import lease. Correct these only in a new candidate.
BIN remains intentionally excluded; ROM management is a separate design problem.

Remaining screenshot physical coverage: text console, USB MC, Cover, VICE/BASIC,
moving gameplay, repeated/transition captures and per-case HDMI/color/audio/lifecycle
comparison where not explicitly reported. No-display testing may remain UNTESTED
if it requires disruptive setup. Deliberate busy-unmount fault injection is optional;
normal Safe Unmount already PASS. Earlier attempt18 FAIL and attempt19 bounded
results remain historical evidence; no existing image has been modified.

## Additional engineering capture

A new on-demand Main Menu PNG was collected over SSH at 20:15:32 UTC on 2026-09-26.
Remote `time pcbm-screenshot` measured 0.379 seconds real, 0.281 user and 0.066 sys.
It is readable and retained privately alongside the earlier captures. This is one
Main Menu timing sample, not a moving-game/audio or HDMI comparison pass. Only
screenshot output was written; installed packages/scripts and old captures remain
unchanged. The ordinary command remains `pcbm-screenshot`; `time` is instrumentation.

## Moving C64 gameplay capture: FAIL

Owner left VICE running moving C64 gameplay on HDMI. Two explicit SSH captures
both exited1, `Screenshot unavailable: display changed during capture.`, each
0.278s real. Neither produced a completed PNG. No HDMI image comparison is possible
for these attempts; disturbance/audio/F10 observations await the owner report.
Private exact timing/status evidence: `moving-game-capture-failure.json` beside the
retained screenshots. No live software was changed.

The dev1 GPL helper requires identical framebuffer IDs before/after the CPU copy.
That rejects normal page flips as well as real display transitions. The observed
failures are consistent with this overly strict condition; no privileged instrumented
binary was installed to log the Pi's exact changing IDs. A separate GPL dev2 helper
will admit an exported, pinned scanout sample when connector, CRTC, plane, display
mode, composition and supported pixel layout remain consistent. It still rejects
unsupported composition/format and bounds stale/mode retries. Native fixtures now
exercise successful continuous page flips and rejected mode/layout changes. Physical
moving-game success remains UNTESTED until the new image is qualified; tear-free
moving-frame capture is not promised.
