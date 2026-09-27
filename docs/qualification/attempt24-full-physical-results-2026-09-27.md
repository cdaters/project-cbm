# Attempt24 additional physical results and live review

PRIVATE NON-RELEASE 1.2.0-dev.5, Pi 4 B. Same installed identity as the
[earlier review](attempt24-owner-review-2026-09-27.md): lock
`ee0308da672c783cf3142e7a581b80344e42cc3605f227b7d8f18cb50dd62819`, raw
`754b34e4ab1abd0af65d97956546f295036a4a418b15c20d7f3dd0f14fd1ba7c`, XZ
`efb7f642b91160b2143abd7f958509f2ffc2f8d618667ba697a4c1f01955f051`.

Owner supplied the additional results below. The agent copied and viewed all eight
named PNGs directly from the live Pi, checked installed implementation and made
bounded metadata-only requests using the installed registered `cbm` adapter.
No installation, configuration, keyboard-mode change, download, firmware change,
USB remount or image repair was performed. Two independent SSH controlling-PTY
sessions exercised installed Online Library; HUP ended only those test sessions.
HDMI Menu and its session were not signaled or controlled.

| Case | Result and scope |
| --- | --- |
| Central search, metadata/results, hosted download and Save to Library | Owner physical PASS using registered cbm. No throughput/quota/other-server-policy qualification. |
| Guided Import sizes, Back, Parent Folder, unsupported-only explanation, hidden IDs | Owner physical PASS. |
| Ordinary FILES / USB browse / MC regression | Owner physical PASS for reported normal behavior. Deliberate busy-unmount fault injection remains separate and UNTESTED. |
| Gameplay screenshot command, no noticeable slowdown/audio interruption | Owner physical PASS, bounded to the reported game/session. No instrumented latency or general performance claim. |
| About & Support display and Back | Owner physical PASS; supplied PNG shows correct attribution/support links. |
| Direct boot to current/default machine | FAIL; display-release ordering independently diagnosed. Post-TERM keyboard failure and contaminated mode evidence remain as in the earlier chronology. Owner additionally reports normal reboot returned to Menu. This is not a corrected direct-boot PASS. |
| Year/other preset filters after Group; Server Information flash/return | Earlier owner physical FAIL; intermittent trigger not established. Current SSH reproductions retain Year and Server Information. Owner subsequent HDMI Repository retest shows a stable list. Do not erase the earlier failure or claim a precise unobserved cause. |
| Cover screenshot | UNTESTED: too brief to time manually, not a capture FAIL. |

## What the retained PNGs establish

The two original Import captures are byte-identical to the previous retained copies:
`pcbm-20260926T235133Z.png` shows one supported PRG and three unsupported entries;
`pcbm-20260926T235302Z.png` shows zero supported files and four unsupported entries.
Neither displays a selectable BIN. The installed `ingestion.EXTENSIONS` excludes
BIN, shared USB discovery uses that allowlist, and the installed `pcbm-roms` is a
compatibility notice (not a separate ROM importer). Current Menu/adapter source
hashes match installed files. Therefore neither a ROM-specific BIN import context
nor a broadened generic allowlist is established in this image. The owner's contrary
interpretation is retained in the original request rather than silently rewritten.

BIN is a legitimate possible ROM format; file browsing/manual copy can expose any
file. That is distinct from guided import and correctly configuring a ROM resource
in VICE. The general allowlist remains unchanged; ROM role/machine/size/configuration/
restore semantics need a separate design. Directory names do not infer machine type.

`pcbm-20260927T000246Z.png` is the retained blank direct-boot screen.
The four game captures show:

- `023155Z`: white scanlined canvas with black side margins; by itself it cannot
  establish what game content should have been visible at that instant.
- `023217Z`: EA startup logo.
- `023250Z`: Legacy of the Ancients title artwork.
- `023328Z`: the game's selection menu.

The recognizable frames corroborate game-display capture. Moving gameplay and
lack of noticeable audio/performance impact are owner observations; a still PNG
cannot independently establish motion, audio or frame-rate performance. None of
these images is a Project CBM machine Cover.
`pcbm-20260927T025137Z.png` shows About & Support Assembly64.

## Online investigation and correction scope

Installed backend currently returns nine repositories, twelve categories and
47 year values (1980–2026), and a four-entry public directory. Existing selected
server remains Central; directory entries were not queried. Valid preset parsing,
client admission and server replies succeeded. Current installed SSH TERM=linux
PTY tests at 100x30 and 240x67 show a usable Year list after Group=Censor, and
Server Information remains until acknowledgment. No transient cause is proven.

Source review identifies real silent-return paths on preset rendering errors and
shared dialog validation/error results. Also, the backend permits 128 presets but
adding Any produces 129 choices, beyond the shared dialog limit. The live year list
has only 47 entries, so that boundary bug is not evidence of this physical trigger.
New Menu correction provides explicit acknowledged errors, preserves previous
filters, pages large lists within the existing bound, and offers persistent Server
Information with Refresh/Back. Installed tests must include delayed replies, a
failed directory call, explicit retry, persistence and retained multi-filter state.
Do not merely add sleep or label the original intermittent trigger explained.

## Evidence and next candidate

Private evidence: `qualification/attempt24-full-owner-review-2026-09-27` under
ProjectCBM-Work: exact owner request, eight PNGs, installed-source hashes/allowlist/
metadata responses and SSH terminal traces. Prior evidence and sealed manifests
remain untouched. No hosted media was copied into build inputs or tests.

The separate Product direct-boot handoff fix and Menu presentation correction are
intended for a new dev6/attempt25 candidate after all gates. Existing Runtime and
GPL capture packages may be reused only after exact unchanged-input checks.
All physical claims above apply to attempt24, not the next image.
