# POC4 attempt #4: Pi 3B physical follow-up

The [owner attestation](poc4-attempt4-pi3b-owner-report-2026-09-17.json) establishes
**PHYSICALLY PASSING lifecycle behavior on the tested Raspberry Pi 3B**. The attempt
#3 dead-keyboard/dead-VT regression was **NOT REPRODUCED**. Cover visibility remains
**FAIL**. This does not retrospectively prove attempt #3's precise root cause.

This is additive evidence. The original attempt #4 [build record](../build/private-poc4-attempt4.md),
[offline result](../build/private-poc4-attempt4.json), [physical procedure](poc4-attempt4-pi3b-regression.md),
frozen inputs, packages, images and recovery checkpoint retain their original bytes
and contemporaneous UNTESTED statements. This report supersedes those statements
only for the specific owner-reported physical observations below.

## Exact candidate and reported behavior

Product 1.1.0-poc.4 / private-engineering-poc4, corrective attempt 4; integration
`f5511e10154e6db93f472716e9ddefd04abadb26`. Menu `v1.1.0_poc4.2`, peeled
`171e67b3de181074245fb2bdc70cb60af5688b8e`.

- Lock: `b3430b626d5156c582f4e3e457d47916a16b527c3dcf7586a90cae96c3882b72`.
- Raw: `f699595fdd31a7f8125bb1882ce8d468ce7dd1b4734d85986b1962e992875b21`.
- XZ: `076a42911faa24bc4f2d4c225c92d621498261b630e63de35b6c7dc8af0760e2`.

Fresh flash, fundamentally completed first boot, Menu keyboard and both VT directions
before RUN pass. RUN, VICE launch, F10/Quit, visual Menu return, immediate Menu keyboard,
Ctrl+Alt+F2 and tty2→tty1 after return pass. The owner additionally launched each
available machine/profile and returned to a responsive Menu; Menu F1/F2 VT switching
continued to work. No per-profile list or explicit three-cycle log was supplied.
No tested launch visibly displayed its Cover. Actual dates/timings/peripherals beyond
the reported Pi 3B are not inferred. Codex did no physical testing.

## Card collection gate

The owner accepts read-only **engineering runtime evidence from the used card**, with
unknown historical Paragon journal-replay semantics. This is not pristine forensic
evidence. The card was safely shut down before Mac insertion.

Device metadata identifies `/dev/disk4`, removable USB, with root `/dev/disk4s2`,
31,682,706,944 bytes at offset 545,259,520, Paragon `ufsd_ExtFS` mounted at
`/Volumes/rootfs`. Crucially, `diskutil info` reports **Volume Read-Only: No** and the
mount listing has no `read-only` flag. Boot is separately mounted at `/Volumes/bootfs`.
Only mount/device metadata was inspected. No card file, identity, diagnostic, boot
file, credential or network profile was read; no mount change, repair or write ran.
Reading through a writable mount could update filesystem metadata, contrary to the
owner's no-modification instruction. The owner was asked to make rootfs read-only
through Paragon. Collection is **BLOCKED pending verified read-only access**.

Consequently the used card's exact installed identity remains **UNVERIFIED**; it is
not appropriate to interpret diagnostics from it yet. The retained master images,
lock, seven component/input identities and two prior recovery manifest hashes have
been rechecked successfully (12 references). Master verification is not card identity
verification or a hash comparison against a first-boot-modified card.

Prepared `collection-script.py` in the new external evidence directory requires a
read-only mount and byte-exact generated attempt #4 identity before collecting the
existing allowlisted phase files. It has not been executed against the card. It
records source/copy/source hash agreement, missing files and known public Cover/
wrapper/renderer/lifecycle payload hashes. It executes no appliance program and
reads no credential/profile stores. Noowners mount permissions are not proof of
runtime Linux readability. Detailed private evidence remains outside Git.

## Cover finding and cause classification

**Confirmed source contract mismatch; physical cause not yet confirmed.**

Product `engineering.py:run_launch` opens `/dev/tty` when no input descriptor is
supplied, then passes that descriptor as Cover stdin. Menu `scripts/pcbm-cover`
requires `tty` output to equal `/dev/tty1`; any other value exits 0 before registry
resolution, asset selection or renderer invocation. A descriptor opened through the
controlling-terminal alias can identify as `/dev/tty`, even though its session is
attached to tty1. This is a strong, specific explanation for silent nonvisibility.

An isolated real macOS pseudoterminal experiment reported inherited stdin
`/dev/ttys001`, opened alias `/dev/tty`, and `tty` output `/dev/tty`. Three isolated
checks against the actual wrapper, relocating only the profile resolver and supplying
controlled tty outputs, confirm: alias silently skips resolution; tty1 reaches it;
tty2 is rejected. These establish the source behavior and host alias mechanism, not
the actual Pi failure. No SDL renderer or appliance command was run in this probe.

Pending card evidence: Cover invocation and PID, selected profile/path, existence/
readability, child process-group observation, backend/DRM, monotonic start/end, exit
status, timeout/termination/reap, pre-Cover terminal state, post-Cover state and restore,
VICE launch/exit and final restore are all **NOT COLLECTED**. Do not fill these with
source expectations. Source stores no independent child PGID or explicit reap boolean;
completed Cover records follow `wait()`. Parent/foreground groups and timing can
support a bounded inference once collected. SDL presentation telemetry would still
not prove visible pixels. No new live state can be reconstructed after shutdown.

Expected discriminating evidence for this hypothesis is exit 0, no renderer events
and a short Cover interval alongside `/dev/tty` phase records. That combination plus
matching installed wrapper bytes would support early guard rejection. Different
findings require a different diagnosis; absent events alone are not conclusive.

Recommended source correction, after evidence and source authorization: keep tty1-only
and unprivileged admission, but determine the controlling terminal's actual device
identity instead of comparing an alias pathname. Prefer a narrow Cover admission fix
that leaves the now-passing shared supervisor, terminal capture/restoration, process
group, timeout, reaping and VICE launch untouched. Validate the chosen Linux device
query in native staging; do not remove the tty guard, force VT switching, broaden
privileges, extend timeout blindly or alter VICE geometry/audio/F10 to show artwork.
Add alias/tty1/tty2/no-tty, guard diagnostic and full-wrapper/supervisor regression
coverage, plus the existing repeated lifecycle tests. A future physical test must
establish both Cover visibility and preserved immediate input/VT response.

## Network information and boot backlog

The requested IP/MAC gap is confirmed in source. Product `runtime/project_cbm/info.py`
collects only `interface` and `operstate` from sysfs into `current_state.network_links`.
The strict [schema](../../schemas/info.schema.json) admits only those two properties.
Menu `lib/pcbm_info_view.py` renders that limited data. CONTROL → Network → status
already calls System Information; it has no independent IP detector to repair.

Smallest coherent extension: Product supplies bounded, validated per-interface
records with name, interface type, operational/connection state, IPv4/IPv6 addresses
and prefix lengths, current MAC and an optional safe active Wi-Fi SSID. Separate link,
NetworkManager connection, address assignment and Internet reachability; do not call
an active NetworkManager service or an address proof of Internet access. Preserve
unknown/unavailable states and distinguish an empty address list from collection
failure. Use fixed read-only local commands/sysfs, timeouts and output/count limits;
never read saved connection files, request secrets, perform scans or initiate networking.
Do not equate a connection profile's arbitrary name with its SSID.

Extend the authoritative schema and text output together, with synthetic multi-address,
IPv6 link-local, disconnected/unavailable, malformed/control-character, timeout and
secret-exclusion tests. Menu renders only those fields, safely wraps long IPv6 values,
and preserves compatibility with old reports. The existing Network status entry can
reuse this view; no new top-level SHOW IP item or duplicate probes are needed.
**Recommended, not implemented under the completed candidate scope.** No card network
configuration was examined and no private IP/MAC/SSID is included in Git.

[Boot-experience backlog](../design/boot-experience-backlog-2026-09-17.md) records the
rainbow/startup-message observation and separates quiet presentation from measured
power-on-to-interactive-Menu performance. No boot/session change was implemented.

## Scope, tests, recovery and next step

The top Current owner scopes still authorize the completed single corrective candidate
(Product `59c36d1`, Menu `aeb4350`). The new owner request authorizes this additive
physical investigation but explicitly conditions source changes on current source-work
scope. Neither top section opens a subsequent source milestone. Therefore no runtime,
Menu, schema, package version/tag, lock, image or boot behavior changed. AGENTS remains
untouched. Bounded source correction and the network extension are review proposals;
no extra candidate is authorized. Documentation/evidence work does not reopen building.

Focused characterization: **3/3 PASS**. Existing Product lifecycle suite: **9/9 PASS**.
Real host PTY alias experiment: reproduced. Native Linux/Pi alias probe: NOT RUN.
The initial sandbox denied `/dev/tty` access; the authorized unsandboxed isolated
host experiment succeeded. No full suite rerun is claimed for documentation-only work;
the historical Product macOS mktemp failure retains its existing classification.

New evidence: `qualification/poc4-attempt4-physical-2026-09-17`; new recovery:
`archive/poc4-attempt4-physical-review-2026-09-17`, relative to configured external
workspace. The sealed manifest and restore report bind final refs, bundles, tests,
this report and preserved artifact references without duplicating images. Independent
encrypted custody remains open. Earlier candidate/evidence/checkpoints remain intact.

No package impact from this documentation checkpoint. A subsequently authorized Cover
admission change requires new Menu bytes/version/tag; a network collector/schema/UI
change requires matching new Runtime and Menu packages. Integration/diagnostic changes,
if needed after evidence, require a new integration identity. VICE, TCPser, artwork,
qualification media and optional payloads have no identified change requirement;
reuse remains subject to exact hash/compatibility checks. No versions are reserved.

Remaining physical qualification includes Cover visibility/aspect/default/explicit/
CONTENT routing; explicitly recorded three-cycle regression; geometry/media/audio/
VICE input/joystick; detailed setup/Back/retry/resume; Wi-Fi association/persistence;
SID-Wizard, StrikeTerm, Midnight Commander, mixer, USB, Samba, SSH, TCPser, mDNS and
preferences/service/network/reboot persistence. Each remains UNTESTED unless separately
reported. StrikeTerm's private admission/public-rights gate is unchanged.

**One next owner action: make rootfs read-only through Paragon and resume allowlisted
attempt #4 evidence collection.** Source correction selection follows the actual
records and requires the bounded source scope to be authorized. Do not reflash, build
or retest merely to replace the missing collection. STOP for owner review.
