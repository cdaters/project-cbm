# POC4 attempt #4: collected Cover and terminal evidence

**The missing Cover is explained with high confidence by the tty admission guard:
the supervisor passes `/dev/tty`, but the wrapper accepts only the literal name
`/dev/tty1` and silently exits before resolving artwork or starting SDL.** The exact
installed code and all four retained launch records agree with that explanation.
There is no explicit stored guard-rejection reason, so the executed branch is inferred
from code plus runtime evidence. This does not prove how the renderer will behave once
admitted, nor retrospectively establish attempt #3's keyboard/VT root cause.

The owner-reported attempt #4 Pi 3B lifecycle remains **PHYSICALLY PASSING** for the
reported behavior; visible Cover remains **FAIL**. See the immutable [owner attestation](poc4-attempt4-pi3b-owner-report-2026-09-17.json).
This additive report supersedes the collection blocker and evidence gaps in the
[earlier review](poc4-attempt4-physical-review-2026-09-17.md), whose original text and
recovery checkpoint remain unchanged. [Machine-readable analysis](poc4-attempt4-card-analysis-2026-09-17.json)
records exact per-launch times and observations. No physical test was performed by Codex.

## Collection and exact identity

After the owner changed Paragon's mount, both `mount` and `diskutil info` confirmed
`/dev/disk4s2` at `/Volumes/rootfs` **read-only**. The collection script checked the
mount again immediately before and after reading. No remount, repair, card write,
card program execution, boot-partition access, credential/network-profile read or
unrelated private-file read was performed by Codex. Collection is engineering evidence
from a used card, **not pristine forensic evidence**; historical journal replay and
writable-mount behavior remain unknown under the owner's accepted limitation.

The installed `/usr/share/project-cbm/identity.json` matched the exact generated
projection from the verified frozen lock, byte for byte, before any diagnostics were
interpreted. All four embedded launch identities match the same lock. This identifies
the base candidate, not an assertion that the used card equals the sealed raw image.

| Binding | SHA-256 / identity |
| --- | --- |
| Candidate | 1.1.0-poc.4 / private-engineering-poc4, corrective attempt 4 |
| Integration | `f5511e10154e6db93f472716e9ddefd04abadb26` |
| Menu | `v1.1.0_poc4.2`, peeled `171e67b3de181074245fb2bdc70cb60af5688b8e` |
| Lock | `b3430b626d5156c582f4e3e457d47916a16b527c3dcf7586a90cae96c3882b72` |
| Raw image | `f699595fdd31a7f8125bb1882ce8d468ce7dd1b4734d85986b1962e992875b21` |
| Compressed image | `076a42911faa24bc4f2d4c225c92d621498261b630e63de35b6c7dc8af0760e2` |
| Card evidence inventory | `e098884fc5621696b587eb3a24a73e9bf38b7267ac879b65751bafcf46b5adf8` |

Private evidence resides at
`qualification/poc4-attempt4-physical-2026-09-17/card-evidence`, relative to configured
external workspace `/Volumes/TheBench/ProjectCBM-Work`. It contains **41 allowlisted
files**: identity and the four retained launch slots, with source/copy/source hash
agreement. Eight periodic sample files and top-level snapshot/report were absent;
missing samples correspond to shorter runs or the final unused sample interval.
No new snapshot was generated. Four slots are the configured retention maximum;
they do not enumerate every machine the owner tested.

The installed wrapper, Python renderer and Product lifecycle helper match the reviewed
source hashes. All seven known Cover files exist, match their exact artwork hashes,
and report mode0644 through Paragon. Files were readable through this read-only reader.
The noowners mount does not itself prove Linux UID1000 access or ACL behavior. In the
recovered execution path, the wrapper exits before attempting to read artwork.

## What the four launches establish

| Recorded profile | Registry-derived expected artwork | Cover wrapper PID | Cover interval, ms | VICE PID | VICE exit |
| --- | --- | ---: | ---: | ---: | ---: |
| x128-80col | pcbmcover-c128.jpg | 1641 | 10.082006 | 1672 | 0 |
| xvic | pcbmcover-vic20.jpg | 1709 | 10.019195 | 1740 | 0 |
| xplus4 | pcbmcover-plus4.jpg | 1759 | 9.997893 | 1790 | 0 |
| xcbm5x0 | pcbmcover-cbm5.jpg | 1810 | 10.036503 | 1841 | 0 |

Artwork locators are beneath `/usr/share/project-cbm-menu/covers/`. These are derived
from the authoritative registry and recorded launch profiles, **not stored observations
of a selected/opened Cover path**. Guard rejection occurs before registry resolution.
The retained launches were ordinary profile launches (`content_requested=false`);
CONTENT routing is not established by these records.

For every retained launch:

- Cover wrapper was spawned as UID1000. It exited0 with `events=[]`, `timeout=false`,
  `killed=false`, `termination_signal=null`. The approximately10ms whole-wrapper
  interval is incompatible with the intended0.75s normal display loop.
- No renderer initialization, video-driver, renderer, presented or released event
  exists. The matching code's early tty check explains the silent successful exit.
  No Cover SDL backend, renderer PID, texture load or submitted frame is established.
  Do not copy VICE's backend into the Cover result.
- Parent session, process group and foreground group are all900. The wrapper inherits
  the group by the inspected `Popen` call; there is no independently stored child PGID.
  There is no explicit reap flag, but final Cover records are saved only after the
  supervisor's wait/reap path returns. No timeout or signal termination was necessary.
  A powered-down card cannot independently show a later live process census.
- Pre-Cover descriptor name is `/dev/tty`. The separate pre-VICE snapshot, whose `tty`
  command inherits the supervisor's original stdin, reports `/dev/tty1`. This is the
  crucial alias-versus-real-stdin distinction, not evidence that the user was on the
  wrong virtual terminal.
- Numeric terminal state is keyboard3, display0, VT mode `[0,0,0,0,0]`. The entire
  recorded termios array, tty, groups/session and keyboard/display/VT modes are equal
  before Cover, after Cover, after VICE and in both restored-state snapshots.
- Both restoration records report `attempted=true`, `verified=true`, `errors=[]`,
  `mismatch=[]`. All four VICE records end in `phase=exited`, status0, no termination
  signal. A retained intermediate “still running” observation is historical sampling
  text; the final phase/status is authoritative, not evidence of a surviving hang.
- The after-Cover/before-VICE snapshot shows connected HDMI and active1920×1080@60.
  Two longer runs also have two samples each with the same active mode. These are
  not Cover-time DRM samples. VICE telemetry reports KMSDRM/OpenGL and ALSA for all
  four profiles; it does not prove Cover initialization, perceived geometry or sound.
- Login sessions exist for tty1 and tty2; Menu sleeps in `do_wait` before VICE, an
  expected waiting ancestor. Immediate keyboard/VT response after return remains
  the owner's dynamic observation, supported by the restoration records.

The logs establish successful process return and terminal readback in the four
retained cycles. They do not physically qualify every machine, an explicitly recorded
three-cycle procedure, geometry, audio, joystick, optional applications or networking.

## Cause and smallest correction proposal

The confirmed source defect is a pathname-based tty guard that cannot admit the
controlling-terminal alias deliberately supplied by Product. The host alias experiment
and three wrapper characterization checks already retained in the earlier checkpoint
reproduce the distinction; the new card records now show the same descriptor on the Pi,
correct installed bytes, early successful exits and absence of renderer stages.
**High-confidence immediate cause of these missing Covers: guard rejection before
SDL.** The instrumentation lacks an explicit guard reason, so that last branch
attribution remains an evidence-supported inference rather than a captured trace.

Correct only Cover admission: identify the actual controlling tty1 device through a
validated Linux mechanism, preserving unprivileged execution and rejection on tty2,
PTYs, nonterminal input and missing/unavailable identity. Do not merely add `/dev/tty`
as an accepted string: that alias can refer to another controlling terminal. Retain
registry selection and immutable artwork. Emit a bounded fixed guard outcome before
renderer initialization so a future skip cannot look like a successful presentation.
The existing supervisor can retain a fixed `stage` event without arbitrary strings.

Leave the now-passing Product capture/restoration, foreground group, deadlines,
termination/reaping and shared VICE launch intact. Do not force a VT change, relax
privileges, lengthen the bound blindly or alter geometry/ALSA/F10. Before packaging,
prove tty1 direct/alias admission and rejection cases under native Linux, exercise the
actual wrapper and supervisor together, and rerun the existing three-cycle lifecycle
and SDL failure/timeout cleanup tests. Then a separately authorized new candidate
must physically establish Cover visibility and continued immediate Menu/VT response.
No image may be patched in place to test this proposal.

No runtime correction was implemented: current top owner scopes still describe the
completed single-candidate milestone, and the physical task explicitly conditions
source correction on current source-work authorization. Neither AGENTS was modified.
Source implementation, including the narrow pcbm-info/network view extension, needs
an explicit bounded source milestone; building another image remains separately gated.

## Other requirements, validation and preservation

The [earlier network analysis](poc4-attempt4-physical-review-2026-09-17.md#network-information-and-boot-backlog)
remains applicable: enrich pcbm-info's structured authority and schema, then render
those fields in existing System Information/Network status. No competing Menu detector,
new top-level SHOW IP, saved-credential read, scan or network activation is proposed.
No actual card IP/MAC/SSID was collected. The [quiet/fast boot backlog](../design/boot-experience-backlog-2026-09-17.md)
remains backlog only, with measured timing and preserved getty/PAM/TTY/session behavior.

Source unchanged: earlier **3/3 wrapper characterization** and **9/9 lifecycle tests**
remain the focused results; not represented as new native/physical passes. New evidence
validation checks all copied hashes, embedded identities, expected source/art bytes,
four completed lifecycle records and terminal equality/restoration consistency. No
full suite rerun or elimination of the known macOS mktemp test failure is claimed.

New recovery: `archive/poc4-attempt4-card-analysis-2026-09-17`. Its manifest/restore
report binds final source refs, full bundles, offline refs/peeled tags/symbolic HEAD/
fsck, the private card evidence and unchanged earlier checkpoint/artifact references.
It is distinct from both the immutable attempt #4 build checkpoint and the earlier
writable-mount investigation checkpoint. No historical report, image, lock, package,
artwork, card or previous recovery record was mutated. No push/publication, builder
start, new package/version/tag or physical test by Codex occurred. Independent encrypted
custody remains unresolved.

No package bytes change in this investigation. Future Cover source work requires a
new Menu version/tag/package; the proposed network authority/UI changes require new
Runtime and Menu packages and refreshed applicable schemas/integration inputs. VICE,
TCPser, artwork and qualification/optional payloads have no identified change need.
StrikeTerm private admission/public-rights gate remains unchanged.

**One next owner action: authorize the bounded source-only Cover admission/diagnostic
correction and pcbm-info/network-information extension, preserving the working lifecycle
and excluding another image build.** All separately unreported physical tests remain
UNTESTED. STOP for owner review.
