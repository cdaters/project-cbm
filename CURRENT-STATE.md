# RC1 physically qualified with release UX defects — RC2 investigation

[Owner RC1 Pi4 report](docs/qualification/rc1-attempt9-pi4-owner-report.json) records
core Cover/VICE/F10/Menu and reference performance PASS, setup/service/Wi-Fi persistence
PASS, primary boot presentation FAIL, account/content coherence FAIL, USB import FAIL
pending cause and MC practical usability FAIL (launch PASS). First/second Menu stopwatch
~30s; systemd17.668s, tty1~8.261s userspace. Do not add concurrent unit durations or
remove wait-online from the wrong critical path. Unreported functions remain UNTESTED.

Owner authorizes bounded live evidence first, exact v1.0 boot reference review, then
single pcbm runtime/admin identity, usable content/USB, primary presentation and measured
post-getty corrections. No RC2 build until causes/corrections/tests are established.
ONE new private RC2 image is authorized after those gates; then stop for Pi4 testing.
RC1 image, lock, packages, refs and recovery stay immutable. No push/publication.

Live owner readback verifies RC1 identity and supplies two numeric logs, exFAT inventory
and getty/PAM journal. Samples10–21 pass both metric windows; physical audio/visual PASS
is separate. Native RC1 FAT/exFAT reproduction confirms root0077 mount permissions
block UID1000 copying; fixed mount options pass copy/retry/unmount/unchanged-source checks.
Exact installed Type=idle and 5.134061s getty→PAM gap identify a bounded startup deferral;
Type=simple preserves ordering/PAM. Complete power-to-Menu latency is not established.

[RC2 correction contract](docs/runtime/rc2-corrections.md) records decisions/source work.
Single pcbm UID1000/home, /home/pcbm/content, explicit supervised historical primary art,
boot phase trace, FILES/import feedback and corresponding docs/tests are in progress.
Product220/220 and Menu99/99 host tests pass; native account/service/SSH/discovery,
MC, read-only ext4/FAT/exFAT import and terminal lifecycle checks pass. Native fixtures
required overlay-copy ownership and obsolete forced-user expectation corrections;
failed logs remain retained. New-package/image gates remain pending; no RC2 image exists.
Builder is running for disposable diagnostics; RC1/prior artifacts remain untouched.
Next: complete validator/negative tests and native installed single-user/service/boot/
USB/lifecycle tests, clean logical commits/version/package/freeze, then ONE RC2 build,
actual-image validation, recovery and Pi4 exact-hash procedure. READY TO FLASH: NO for RC2.

Earlier RC1 build-readiness entries below are historical, not physical UX acceptance.

# Private RC1 basis complete — Pi 4 B physical test next

**READY TO FLASH: YES after verifying the external recovery manifest/restore PASS.**
[Build report](docs/build/private-rc1.md), [exact results](docs/build/private-rc1.json),
[hash-bound Pi4 procedure](docs/qualification/rc1-pi4b-regression.md).
One image built from integration `8401248a94132b386f9d6804823e0c4e3cd247dc` and Menu
`v1.1.0_rc1` / `4346a350d481f4da3a6abc6524373333637dbb82`.
Runtime1.1.0~rc1-1 and Menu1.1.0~rc1-1+pcbm1 new; VICE3.10-1+pcbm4/TCPser unchanged.
Lock `inputs/frozen-poc4-attempt9/release-lock.json`, SHA-256
`e586ae09b6ff486239dc93f814171f0ce0dd0f0fe8bf8b62f3c06f96a345fd9f`.
Raw SHA-256 `7edc2452529dea92623b07a42036ce74ac7c7b84968d449336cdb4f250578115`;
XZ `84057184795bc05a805e9aa4e8caf971e47f8fbc084396365a671611377798e0`.
External paths/bytes/packages are in the exact report.

Canonical `/home/pi/pcbm`, type-first/machine folders, import/profile routing,
gateway/DNS detail, quiet existing-console presentation and guarded completed-growth
fast path are included. Pi4+ policy follows owner decision; no Pi3 optimization.
Attempt8 Pi4 performance PASS and unchanged boot baseline retained; RC1 physical
behavior remains UNTESTED. Getty9.956s excludes the later network-online wait from
its reported critical path; power-on-to-interactive-Menu remains unmeasured.

Product208/208 +3 validation-followup tests, Menu97/97 on host/native; lifecycle10/10,
seven Covers and native service/import/SSH/discovery/dialog checks PASS. Actual image
283 checks,672 package identities,127 ELF objects, guest/external raw-XZ equivalence,
source/docs/privacy/preservation and host integrity PASS. An inherited validator's old
NM field-list assertion was corrected in separately retained validation-only commits;
frozen inputs unchanged. Initial fixture/validator failures remain retained.
Builder STOPPED; all previous evidence/inputs/refs retained. No push/publication.

Recovery `archive/rc1-2026-09-19` contains full bundles and offline restore/ref/peeled-tag/
fsck verification. Its external manifest is the final checksum authority, avoiding a
Git/manifest cycle. Independent encrypted custody and independent-build reproducibility
remain unresolved. Public redistribution rights and complete public bootstrap/input
publication remain release gates; this is an RC1 basis for private owner qualification.
**Next: flash the exact new image, run the Pi4 procedure, report outcomes. STOP for
owner physical testing.** Do not start another feature/model/architecture milestone.

Earlier entries below are historical checkpoints.

# RC1 final polish in progress — 2026-09-19

The owner changed the 1.1 floor to Pi 4-class and newer, explicitly authorized
quiet presentation/measured safe boot work and one new RC1-basis private candidate.
This supersedes the Pi 3 investigation/attempt9 stop below; preserve those failures.
[Attempt8 Pi4 attestation](docs/qualification/poc4-attempt8-pi4-owner-report-2026-09-19.json):
normal x64sc owner performance PASS, 29 non-warp samples over 145.219 seconds at
weighted 100.002%; final low interval is owner-confirmed quitting. RO card identity
verified before collection; private manifest `daaa83ecadf08c9faffe34c6594ede98a87922d1c241e71e18c6d435d4e28540`.
No unreported function/model is promoted to PASS. Card is now back in the Pi.

Source refinements: `/home/pi/pcbm` remains the independent runtime library;
type-first machine folders/import routing, explicit FILES start location, gateway/DNS
through pcbm-info, quiet firmware/kernel/existing-console text presentation and guarded
completed root-growth fast path. VICE/Covers/session ownership unchanged. Networking
waits are retained. Unchanged Pi4 baseline: kernel2.390s + userspace16.960s =19.351s;
no power-to-Menu stopwatch measurement. Product208/208 and Menu97/97 host tests PASS.
Native Product208/208, Menu97/97, installed lifecycle10/10, seven SDL dummy Covers,
service/SSH/local-discovery/dialog/USB-loop checks PASS. Initial native fixture errors
(missing historical Git metadata and a group-writable synthetic marker) were corrected
and retained; production guards unchanged. Package/freeze/image/recovery gates pending; **READY TO FLASH: NO** for RC1.
New source versions Runtime1.1.0~rc1-1 and Menu1.1.0_rc1 are not frozen yet.
VICE3.10-1+pcbm4 and TCPser will be reused with exact checks.

Builder remains approved native ARM64 Lima/VZ/ext4. Additive stopped-disk/config copy
verified before growth192→224GiB, recovery manifest
`26f9294e0361091dcb8e92203fb491590d632994c5039ccf12f4968fe8574ee1`
at `build-host/records/pre-rc1-disk-growth-2026-09-19`. Full capability and existing
inventory/update guard PASS; no host package updates or retained-state deletion.
Next: finish native tests, clean commits/tags, changed packages, distinct RC1 lock/image,
actual-image gates, verified recovery and exact-hash Pi4 procedure. Nothing pushed.

Earlier entries below are historical checkpoints.

# Attempt #8 pre-test checks complete — ready for owner live A/B

The [readback record](docs/qualification/poc4-attempt8-live-settings.json) now includes
the corrected preferences baseline. Installed identity, both engines, saved VICE seed
and payload match; preferences SHA-256:
`5de2328d7a9ade0d5ca4fb8a80c6ac9bfd76a2b360cd692fe46e9006b72e08f8`.
Next: preserve original slow-run telemetry, then fresh A=x64sc and B=x64 through MACHINES,
matching active workload segments. Collect speed/CPU/clock/throttling and audiovisual
observations; verify hashes after quitting. Do not select DEFAULT or save VICE settings.
Physical A/B UNTESTED; performance blocker/no-attempt9 remain. No appliance changes.
Recovery: `archive/poc4-attempt8-ab-baseline`; external manifest/restore report is authority.

# Attempt #8 settings/payload match; procedure path corrected

[Owner readback](docs/qualification/poc4-attempt8-live-settings.json) confirms the saved
VICE configuration and installed seed match, and the Donkey Kong payload hash matches.
The supplied preference path `.config/pcbm/preferences.json` was a procedure error:
`runtime/project_cbm/preferences.py:location` uses `.config/project-cbm/preferences.json`.
The [A/B procedure](docs/qualification/poc4-attempt8-live-c64-ab.md) is corrected. Obtain
that existing file's before/after fingerprint; do not create/reset anything. Actual
x64 performance remains UNTESTED; attempt8 FAIL and no-attempt9 build remain in force.
Recovery: `archive/poc4-attempt8-settings-readback` (external manifest/restore authority).
No runtime, package, candidate, Menu or default change. Prior evidence remains intact.

# Attempt #8 live identity and both C64 engines verified

[Owner SSH readback](docs/qualification/poc4-attempt8-live-identity.json) matches the
exact attempt #8 installed identity, VICE 3.10-1+pcbm4, and both retained x64sc/x64
binary hashes. Live x64 availability is now confirmed. Earlier pending-identity notes
below describe the previous checkpoint. Configuration/payload hashes and physical
A/B remain pending; performance FAIL/release blocker and no-attempt9 instruction stand.
Next: settings/payload hashes, then the existing bounded physical A/B procedure.
No Pi, package, preference or candidate changes. No new functional/performance PASS.
Additive recovery: `archive/poc4-attempt8-live-identity`; external manifest/restore report
bind final refs and verification. Independent custody remains unresolved.

# Attempt #8 physical performance FAIL — live A/B only

**RELEASE BLOCKER. DO NOT BUILD ATTEMPT #9. READY TO FLASH: NO for a correction.**
[Exact owner report](docs/qualification/poc4-attempt8-pi3b-plus-performance-fail-2026-09-18.json)
and [bounded live A/B procedure](docs/qualification/poc4-attempt8-live-c64-ab.md).
The owner reports the exact attempt8 running on Pi 3 B+: Donkey Kong remains severely
slow in graphics and SID/music, main thread ~99.3%, audio ~3.3%, system idle ~72.6%,
ARM ~1.4 GHz, 58.0 C, throttled=0x0. O3/reSID interpolation did not solve it. The 36.9%
native CPU saving remains native comparison evidence only. Earlier offline READY results
below are historical and do not establish physical performance.

Two new screenshots are privately preserved/hashed/captioned under
`qualification/poc4-attempt8-physical-performance-2026-09-18`, manifest SHA-256
`7bbc02931c399bcab42ec0c220555864778053e7518f8c0904158e66475e8485`.
Capture values differ slightly from the owner readings; both are retained distinctly.
No unreported functional PASS is inferred. Frozen image/lock/packages/recovery unchanged.

Frozen attempt8 contains both x64sc and x64 and a direct MACHINES → Commodore 64 (fast)
launch profile. The initial C64/C64SC settings match. Live readback remains pending:
automated SSH lacks authentication and the computer-use terminal interface is unavailable.
Owner has been asked for identity/package/engine hashes; no credentials requested.

Next: verify live identity/configuration/payload hashes; preserve current failed-run
telemetry; fresh A=x64sc and B=x64 launches through the existing physical Menu, observe
matching segments and numeric speed/CPU/clock/throttling, then verify unchanged preferences.
Do not change DEFAULT or save VICE settings. No third case or hardware-tier policy yet.
No persistent Pi edits, packages, image build, quiet/fast boot, push or publication.

This documentation/evidence checkpoint is retained at
`archive/poc4-attempt8-physical-ab-2026-09-18`; the external manifest and offline
restore report record exact final refs and verification. It adds no candidate.
Independent custody remains unresolved; prior candidate recovery stays intact.

# Attempt #8 performance candidate complete — 2026-09-18

**READY TO FLASH: YES with verified external recovery. STOP FOR OWNER PI 3 B+ TEST.**
[Report](docs/build/private-poc4-attempt8.md), [exact results](docs/build/private-poc4-attempt8.json),
[hash-bound performance procedure](docs/qualification/poc4-attempt8-pi3b-plus-performance.md).
Recovery `archive/poc4-attempt8-final-2026-09-18` is finalized/verified externally; its manifest
and restore report are the authority and must show PASS before flashing.

Attempt #7's below-real-time C64 result remains a release blocker until the new exact
image passes physical performance qualification. The matching private `kong_arcade.prg`,
six captures and read-only card diagnostics are retained externally; no unreported
function is promoted to PASS. The native evidence supports portable -O3 plus reSID
interpolation while retaining x64sc, filters, accuracy resources and working lifecycle.
Native owner-reference CPU cost fell 36.9%; this is not a Pi speed/fidelity PASS.

Default administrator/network username is `pcbm`, Computer Name `projectcbm`; owner
remains the role. Console/content remain pi; Samba has a separate sharing password.
Nine expanded release manuals cover actual user/network/account/VICE/build/factory/
customization/development/recovery workflows. Public-from-source bootstrap and existing
public rights gates are explicitly incomplete. No quiet/fast boot or VT workaround.

Product host/native 195/195; Menu host/native 96/96; installed lifecycle 10/10; ten VICE
cores/hardening checks; final 71.048-second audio/12-sample native telemetry PASS.
Native account/SSH/services/local mDNS/dialog/import/utilities pass within isolated limits.
260 actual-image checks, 672 package identities, 127 ELF objects, filesystems/systemd,
sealing/security/accounts/discovery/docs, raw/XZ equivalence and host integrity PASS.
Builder stopped; remaining guest 36,183,490,560 bytes needs planning before another build.

Integration `9aef29a7e87f7a88bd47d9f01c430aa3eb0c0b21`; Menu `v1.1.0_poc4.6`, peeled
`2ec5f8dcb04b5d86f64a2ce6a96625c3528eac73`, annotated `085ab4bd820709bf0407cdbba35d25060e2541fd`.
New Runtime 1.1.0~poc4.5-1, Menu 1.1.0~poc4.6-1+pcbm1 and VICE 3.10-1+pcbm4;
TCPser and unchanged verified inputs reused. Lock `inputs/frozen-poc4-attempt8/release-lock.json`
SHA-256 `53d2d25f997613434e16fdecc0057eeea88da74783f9487b2501cbec4d1cce57`.
Artifacts in `artifacts/private-poc4-attempt-8`:
raw 3,095,396,352 bytes SHA-256 `e4bb7f03ed26583097f92e8b8d1c2e9e4e3616d4d39940c78f70618ca3a81c40`;
XZ 599,057,044 bytes SHA-256 `892082b4ef8468dab3273b4746350863f9bc75c17e6c2e18a0ef3b4eb62129e4`.
Exact filenames and all package/input hashes are in the report. Prior evidence unchanged.

Next owner action: flash the exact new image and perform the linked Pi 3 B+ performance
procedure. Stop for physical results. Independent encrypted recovery custody and clean
rebuild reproducibility remain open. Nothing pushed/published; no tested-card writes.

# Pi 3 B+ performance correction selected — 2026-09-18

**READY TO FLASH: NO; attempt #8 construction/validation pending.** Attempt #7 has
[owner-reported below-real-time C64 performance](docs/qualification/poc4-attempt7-pi3b-plus-performance-2026-09-18.json).
The verified read-only card matches its exact lock. Six screenshots/diagnostics and the
matching owner-supplied `kong_arcade.prg` are preserved privately outside Git/images.
See [the evidence, comparisons and decision](docs/runtime/c64-performance-2026-09-18.md).

Chosen correction keeps x64sc, SID filters, true-drive/VIC-II accuracy and the working
SDL/ALSA/Cover/session lifecycle. Portable -O3 plus C64 reSID interpolation used 36.9%
less native CPU for the exact reference; that is comparative evidence, not Pi performance
PASS. Bounded numeric speed/FPS telemetry and an explicit physical real-time gate are
added. The Pi 3 floor remains. Quiet/fast boot and active-VICE VT remain separate.

The default administrator/network username becomes `pcbm`; `owner` remains the role.
Console/content stay `pi`, Computer Name stays `projectcbm`, Samba keeps a separate
password. No earlier image/account/evidence is migrated. Release manuals now explain
users, services, installed layout, VICE, actual pi-gen stages, package manifests and
practical customization. Build Your Own distinguishes public release replay, derivatives
and private frozen engineering, with exact public-bootstrap gaps stated honestly.

Host/native Product 195/195 and Menu 96/96 PASS. Native isolated account/authentication,
service enable/disable/restart, SSH password login/disable, local SMB mDNS, real dialog,
USB import, utilities and installed lifecycle 10/10 PASS. Seven Covers decode/present/
release using SDL dummy; three supervised cycles restore terminal/reap children.
Physical graphics/audio/network clients remain UNTESTED. A staging-only bytes/text
fixture error is retained and corrected in a separate continuation, not a product failure.

Next: commit/freeze clean Runtime 1.1.0~poc4.5-1, Menu 1.1.0~poc4.6-1+pcbm1 and VICE
3.10-1+pcbm4; reuse unchanged verified TCPser/assets/closures; build ONE next private
candidate with approved factory, all actual-image/integrity/recovery gates and an
exact-hash Pi 3 B+ performance procedure. No push/publication/card write/physical test.

# Attempt #7 release-readiness candidate complete — 2026-09-18

**READY TO FLASH: YES. STOP FOR OWNER PHYSICAL TEST.**
[Report](docs/build/private-poc4-attempt7.md), [exact results](docs/build/private-poc4-attempt7.json),
[hash-bound Pi 3B procedure](docs/qualification/poc4-attempt7-pi3b-regression.md).
Attempt #6's [owner baseline](docs/qualification/poc4-attempt6-pi3b-owner-report-2026-09-18.json)
now confirms the stated first-boot/Wi-Fi/masking/IP/Covers/VICE/Menu/input/persistence
passes, with active-VICE VT and observed macOS sharing discovery failures. Unreported
functions remain UNTESTED. Attempt #7 has no physical qualification yet.

New Runtime `1.1.0~poc4.4-1` and Menu `1.1.0~poc4.5-1+pcbm1` provide hierarchical actual
service/network status, useful actions, projectcbm Computer Name, explicit owner login
and separate sharing-password help, Samba/Avahi discovery and contextual connection
addresses. Release/user/network/build/factory/customization/developer/recovery guides are
complete. Existing session/Cover/VICE/input path remains; SDL-active VT limitation is
accepted without a fragile workaround. No quiet/fast boot changes.

Frozen integration `33347bb9c11e87e70069da5d160e03ec197efe31`; Menu `v1.1.0_poc4.5`
peeled `4c88fa38ce28c63b6342adfb5d7a084a21248684`. Lock `inputs/frozen-poc4-attempt7/release-lock.json`
SHA-256 `1c25d7f7850c63c41e2730bdaef2deef9cd6d0ccf1321c9b23fd4d9228926b3d`.
Raw SHA-256 `cbab8327981eaf0d1d632d6637d3117fd2c2d68ac6d529c434b52fed995b60ba`.
XZ SHA-256 `b8119c4f3bb1c9361cd4d0c047eaa454447884e36dad9d345b50673ba9e7b687`.
Artifacts: `artifacts/private-poc4-attempt-7`; exact paths/bytes are in the report.

Product host/native 184/184; Menu host/native 96/96; installed lifecycle 10/10 PASS.
Native SSH login/disable, actual services/name/persistence, local SMB mDNS and real dialog
pass within isolated limits. Actual image 253 checks, 672 package identities, 127 ELF
objects, filesystems/systemd, installed identity/docs, raw/XZ equivalence and host-drift
PASS. Full frozen input and external byte checks PASS; no finished image edits.

Recovery: `archive/poc4-attempt7-2026-09-18`, with external manifest, full bundles,
restored exact refs/peeled tags/fsck and retained-input/artifact locators. Its manifest is
the verification authority, avoiding a checksum cycle. Independent encrypted custody,
clean-build reproducibility and existing public rights gates remain open. Nothing pushed
or published. Next owner action: flash the exact image and follow the procedure. Then,
if qualification passes, quiet boot + measured fast boot + final RC polish; no new broad
architecture/feature milestone. Earlier checkpoint readiness applies only to its candidate.

# Release-readiness refinement in progress — 2026-09-18

Attempt #6 now has [owner-reported Pi 3B results](docs/qualification/poc4-attempt6-pi3b-owner-report-2026-09-18.json):
first boot/Wi-Fi/masking/IP/Covers/VICE/Menu lifecycle and stated persistence PASS;
VICE-active keyboard VT switching FAIL, before/after VT PASS. Discovery was not visible
in macOS after enabling sharing. Unreported functions remain UNTESTED.

Attempt #7 source work: actual appliance/service status, state-aware UI, predictable
owner login/help, separate sharing password, projectcbm Computer Name and Samba/Avahi
discovery. SDL console source explains active-VICE VT limitation; no fragile workaround.
Release/user/build/customization documentation is complete. Product host 184/184, native 183/183 before final policy-readiness test
and Menu host/native 96/96 pass; installed lifecycle 10/10, native service enable/disable/
restart, owner administration, import, Computer Name and local SMB mDNS response pass.
Historical-harness hostname/missing-file/overlay-fragment issues were corrected and retained. No quiet/fast boot
changes. Prior candidates and recovery verify; no card evidence claim added.

Next: finish tests/native validation, freeze clean changed Runtime/Menu sources, build
with approved factory, validate actual image and recovery, then stop for exact-hash owner
testing. **READY TO FLASH: NO for attempt #7 until all required gates pass.** Nothing
pushed/published. Earlier READY statements below refer only to their historical candidates.

# Private attempt #6 complete — 2026-09-18

**READY TO FLASH: YES. STOP FOR OWNER PHYSICAL TEST.**
[Build/result](docs/build/private-poc4-attempt6.md),
[exact-hash Pi 3B procedure](docs/qualification/poc4-attempt6-pi3b-regression.md).
[Attempt #5 evidence and corrections](docs/runtime/physical-ux-correction-2026-09-18.md)
record lifecycle/IP PASS, Cover/first scan FAIL and unreported UNTESTED. Read-only card
identity and all 27 photographs/35 copied files verify; no tested candidate mutation.

Attempt6 integration `5992e2a7b1a84cbad016a293624d48aaa7cdd1cf`; Menu `v1.1.0_poc4.4`
peeled `6522111691ce494b00637549365d6a5f2a7773ff`. Runtime `1.1.0~poc4.3-1`,
Menu `1.1.0~poc4.4-1+pcbm1`; unchanged components reused exactly.
Lock SHA-256 `8a5f7c929e73ac38ab42945b2bf22d577eb2b8a9e0500dd69c27f005f75c6de2`.
Raw SHA-256 `bf81b1f95ab65d19753f85fdafbb5a93f45eae68b0bea4208bef62c9d6a2c328`.
XZ SHA-256 `028d9b8b0fbc92bcfe75741b9d842885efda9e194cfbc6d1e8cfe26b8967354f`.
Output directory `artifacts/private-poc4-attempt-6`; see report for exact filenames/bytes.

Product host/native 173/173; Menu host/native 85/85; installed lifecycle 10/10; actual
image 230 checks, 127 ELF objects, 672 package identities, filesystems/systemd and
raw/XZ equivalence PASS. Host capability/inventory/update/integrity gates PASS;
builder stopped. Native masking/ASCII, scan timeout and summary latency pass within
fixture limits. Physical Cover/radio/Pi performance remain UNTESTED for this image.

Recovery `archive/poc4-attempt6-2026-09-18` binds final bundles/refs, offline restore,
peeled tags/fsck, exact inputs/outputs and retained private evidence. Independent
custody/reproducibility/rights gates remain. Quiet/fast boot deferred. Nothing pushed
or published. Next action is solely owner exact-hash Pi 3B testing under the procedure.

# Attempt #6 source checkpoint — 2026-09-18

Attempt #5 Pi 3B owner report is recorded exactly: lifecycle and information IP PASS,
Cover and first scan FAIL; unreported functions UNTESTED. Read-only card identity,
35 diagnostic files and 27 externally retained/captioned photographs are verified.
[Findings and corrections](docs/runtime/physical-ux-correction-2026-09-18.md) describe
Cover timeout/dwell, completed-scan readiness, masked passwords/ASCII prompts and
Main Menu authoritative IP summary. No quiet/fast boot work or lifecycle architecture
change. The tested image, locks, source tags and evidence are unchanged.

Planned distinct candidate: attempt #6; Runtime `1.1.0~poc4.3-1`, Menu
`1.1.0~poc4.4-1+pcbm1` / `v1.1.0_poc4.4`. No frozen lock/image yet. Native dialog
masking/ASCII and old byte-locale reproduction pass. Complete source/installed/native
checks, freeze clean inputs, construct and validate actual image, verify recovery and
prepare exact-hash procedure. Do not flash, push or publish. Physical corrections
remain UNTESTED. Standing private authority applies; historical STOPs below do not.

Builder grew nondestructively from160 to192GiB after a fully hashed stopped APFS
clone checkpoint; host inventory/update masks and full capability gate pass.
Evidence `qualification/poc4-attempt6-2026-09-18`; stopped builder checkpoint
`build-host/records/pre-attempt6-disk-growth` is private and same-volume custody.

# POC4 corrective attempt #5 complete — 2026-09-18 / OWNER REVIEW

**READY TO FLASH: YES. READY FOR OWNER PHYSICAL TEST.**
Project CBM **1.1.0-poc.4 / private-engineering-poc4, attempt 5** passed construction
and all offline gates. [Report](docs/build/private-poc4-attempt5.md),
[exact results](docs/build/private-poc4-attempt5.json),
[hash-bound Pi 3B procedure](docs/qualification/poc4-attempt5-pi3b-regression.md).
This candidate's physical Cover/KMS/VT/input and Wi-Fi behavior remain UNTESTED.
Attempt #4 remains lifecycle PHYSICALLY PASSING within the owner report and Cover FAIL.

Frozen Product integration/runtime `9b0220beaf49dca44862a6e9fe874f5e4fa96e8d`; Menu
`v1.1.0_poc4.3`, peeled `664b0a76b798a64d697e0d2d3baa0d45a5406ebd`. New Runtime
`1.1.0~poc4.2-1` and Menu `1.1.0~poc4.3-1+pcbm1`; other component/input bytes reused
exactly. Kernel tty admission and fixed skip events correct the confirmed alias defect;
Product supervisor/restoration and seven artwork files remain unchanged. pcbm-info is
the sole per-interface network authority; existing information views consume it.

Schema-4 lock `inputs/frozen-poc4-attempt5/release-lock.json`, SHA-256
`4568aa184063aa7e3a0ae5217a98320f68735665f5e08340d48368530c88968e`; all 2,894 objects verify.
Raw `artifacts/private-poc4-attempt-5/2026-09-18-project-cbm-1.1.0-poc.4-lite-private-poc.img`: 3087007744 bytes,
SHA-256 `5385acc822d7f280dd2eb5654368ef282ed941d4dc946368871510d98c752e66`.
XZ `artifacts/private-poc4-attempt-5/image_2026-09-18-project-cbm-1.1.0-poc.4-lite-private-poc.img.xz`: 597605380 bytes,
SHA-256 `3923c319e485bbccad642b8a8b8039fc8acd0694a308ec631aeeffa64ed3e567`. External transfer and raw/XZ equivalence PASS.

220 offline checks, FAT/ext4/systemd, 127 ELF objects and all 672 installed package
identities PASS. Native Product 163/163; Menu host/native 76/76; installed lifecycle
9/9; seven SDL dummy Covers and three renderer/VICE-fixture cycles PASS. Product host
162/163 retains only the known macOS mktemp expectation failure. Native first-boot,
privilege, service, import, kernel alias and synthetic IP/MAC probes pass within their
fixture limits. No physical correction, association or unsupported hardware pass claimed.

Root capacity 2430955520; used 1651560448; ordinary-user available
635531264 bytes before expansion; no minimum card-size inference.
Host before/after inventory and update masks PASS, no drift. Builder stopped; no
remaining factory processes/mounts/loops. Prior evidence/refs and 1,677 historical
entries verify unchanged. Owner governance commits `e098244` / `668ff0a` and AGENTS
preserved. The prior uncommitted-governance handoff below is historical.

Recovery `archive/poc4-attempt5-2026-09-18` binds final refs/bundles, exact offline
restoration/peeled tags/symbolic HEAD/fsck, lock, validation, artifacts and procedure.
Evidence `qualification/poc4-attempt5-2026-09-18`; credential-bearing staging roots
are excluded. Manifest checksum remains external to avoid a recovery hash cycle.
Private/public rights gates, independent encrypted custody and reproducibility remain.
Quiet/fast boot and unrelated design features remain backlog. Nothing pushed/published.

**Next owner action: flash the exact new image and perform the linked Pi 3B physical
regression.** Prioritize visible Cover and preservation of immediate Menu keyboard/VT
return, three cycles; collect diagnostic stages before reboot on failure. Then qualify
first boot, Wi-Fi/network information, media/audio/input, applications/utilities, USB,
services and persistence. Stop for owner review; no physical testing by Codex.

# POC4 attempt #5 source correction and native prebuild — 2026-09-18

Owner committed standing governance at Product `e098244` / Menu `668ff0a`; both
AGENTS files are unchanged. The stale uncommitted-governance handoff below is historical.
The current user instruction authorizes source/package/freeze/build/offline/recovery
through an exact-hash Pi 3B procedure, without push, publication or physical testing.

[Correction contract](docs/runtime/cover-network-correction-2026-09-18.md): kernel tty1
identity/active foreground VT admission replaces the pathname guard; fixed skip events;
Product-owned per-interface IP/MAC/type/state/active SSID and existing Menu consumers.
The passing Product supervisor/terminal restoration path is unchanged. Seven Covers
are unchanged. Attempt #4 lifecycle remains owner-reported PHYSICALLY PASSING and Cover
FAIL; no physical result is inferred for the new source.

Host Product 162/163 (only known macOS mktemp expectation); Menu 76/76. Native Linux
source Product 163/163; Menu 76/76. Native ip/nmcli syntax and synthetic live interface
collection pass. Full capability gate passes; builder inventory matches the retained
baseline and update masks remain enforced. Native installed-package validation and
construction are next. Distinct test roots preserve old builder state.

Candidate plan: POC4 corrective attempt #5 / Product `1.1.0-poc.4`, Runtime
`1.1.0~poc4.2-1`, Menu `1.1.0_poc4.3`. Only these two packages need new bytes.
Attempt #4's 2,872 retained objects, artifacts and card-evidence checkpoint are verified
unchanged in `qualification/poc4-attempt5-2026-09-18/starting-preservation.json`.
No attempt #5 image or frozen lock yet. Continue installed/native validation, commit
exact sources, package, freeze and construct through normal gates. Quiet/fast boot
remain backlog. No push or publication.

# Current checkpoint: standing governance refactor — 2026-09-17

[AGENTS.md](AGENTS.md) now defines standing private-engineering authority and hard
owner gates. It supersedes historical milestone authorization/STOP clauses, including
those quoted in the records below and linked build/recovery/qualification documents.
Those records retain their original evidence and wording; they are not current
permission gates. Use this top entry for current status and next action, and canonical
records for exact candidate identities, technical procedures and evidence limits.

This task changes only both repositories' AGENTS.md and CURRENT-STATE.md. The user
requested review-ready, uncommitted changes: no source correction, commit, tag,
package, image, builder operation, push or publication is part of this cleanup.
The previous complete Product AGENTS is preserved in Git at
`33cf4c8bc2a474082986f0b0098b343516fb54b0:AGENTS.md`; the companion Menu version is at
`a6ecf0a59e8ff5c5b8b94c046aca1eacb003a1b6:AGENTS.md`. Existing qualification/build/
recovery records and all prior CURRENT-STATE text remain unchanged. The existing
`archive/poc4-attempt4-card-analysis-2026-09-17` checkpoint predates these edits;
this governance cleanup does not claim a new verified recovery checkpoint.

Engineering status remains: attempt #4 Pi 3B owner-reported lifecycle PASS, visible
Cover FAIL. The [card review](docs/qualification/poc4-attempt4-card-review-2026-09-17.md)
establishes the `/dev/tty` versus literal `/dev/tty1` admission contract defect and
its high-confidence explanation of the observed failure; corrected physical rendering
is not yet proven. Preserve the passing supervisor/TTY/VICE lifecycle and seven Covers.
Network information remains a proposed authoritative pcbm-info/schema extension with
existing Menu consumers. [Quiet/fast boot](docs/design/boot-experience-backlog-2026-09-17.md)
remains separate, measurement-first backlog; unreported physical tests stay UNTESTED.

**Exact next action for this handoff:** review and commit the two documentation
changes in each repository. The requested uncommitted handoff is a task limit, not
an ongoing owner-approval requirement for private engineering.

**Next engineering action:** correct tty1 device-identity admission and add explicit
Cover guard diagnostics with focused regression tests; extend Product pcbm-info/schema
for bounded per-interface state/type/IP/MAC and appropriate active SSID, with no
credential reads or competing Menu probes. Update existing information views. Then
validate natively, version/package changed components, freeze a distinct private POC4
corrective attempt, build through the approved factory, validate and checkpoint under
standing governance. Preserve previous candidates; bind the next physical procedure
to exact successful image hashes. The owner gate remains physical testing/qualification,
not permission to prepare successive private candidates.

## Historical checkpoints (original text follows unchanged)

# POC4 attempt #4 card diagnostics collected — 2026-09-17 / OWNER REVIEW

**Pi 3B lifecycle remains PHYSICALLY PASSING; visible Cover FAIL.**
[New card review](docs/qualification/poc4-attempt4-card-review-2026-09-17.md) and
[exact diagnostic analysis](docs/qualification/poc4-attempt4-card-analysis-2026-09-17.json)
supersede the collection blocker below without changing the earlier attestation/report.
Owner made rootfs read-only; mount and diskutil agree. Installed identity is byte-exact
with attempt #4's generated frozen-lock projection. Forty-one allowlisted files from
four retained launches copied with source/copy/source hash verification. No card write,
remount, repair, execution, boot access or credential/private-network-profile read.
Used-card engineering evidence, not pristine forensic capture; prior journal behavior
remains unknown under the accepted owner limitation.

Evidence `qualification/poc4-attempt4-physical-2026-09-17/card-evidence`;
inventory SHA-256 `e098884fc5621696b587eb3a24a73e9bf38b7267ac879b65751bafcf46b5adf8`.
All seven assets plus installed wrapper/renderer/lifecycle helper match reviewed bytes.
Retained x128-80col/xvic/xplus4/xcbm5x0 Cover wrappers exit0 in about10ms, no renderer
events, timeout or signal. The Product-supplied terminal descriptor is `/dev/tty`,
rejected by Menu's literal `/dev/tty1` guard before resolution/SDL. Confirmed admission
contract defect; HIGH-CONFIDENCE physical explanation from matching code and records,
with no explicit stored guard-rejection reason. No Cover backend/presentation was
reached by that code path; fixing admission does not yet qualify rendering on the Pi.

All four VICE runs exit0 and both restorations verify without error/mismatch. Recorded
termios/keyboard/display/VT/group state agrees across phases. Parent/foreground group
and session900; separate child PGID/reap flag unavailable, wait/reap inferred from
completed supervisor path. Pre-VICE/during-VICE DRM is1080p60; VICE KMSDRM/OpenGL/ALSA.
These are not Cover-time observations or extra physical audio/geometry passes. Attempt
#3's precise dead-input cause is not retrospectively proven; unreported tests UNTESTED.

Network authority/UI extension and quiet/fast boot backlog remain as documented;
no source/runtime/boot/package/tag/image changes. Current top scopes still describe
the completed one-candidate milestone. Preserve supervisor/TTY/VICE behavior and
correct only Cover admission under a bounded source authorization. AGENTS untouched.
Existing focused results remain3/3 wrapper characterization and9/9 lifecycle PASS;
new evidence hash/identity/phase consistency checks pass, no native run claimed.

New recovery `archive/poc4-attempt4-card-analysis-2026-09-17` retains final refs/bundles,
offline refs/peeled tags/symbolic HEAD/fsck, card evidence and preserved artifact refs.
Prior build and initial physical-review checkpoints remain intact. No push/publication.
**ONE next owner action: authorize source-only Cover admission/diagnostic correction
and the pcbm-info/network-information extension, preserving the passing lifecycle
and excluding a new image build.** STOP for owner review. Earlier dated records follow.

# POC4 attempt #4 physical follow-up — 2026-09-17 / EVIDENCE GATE

**Pi 3B lifecycle: PHYSICALLY PASSING for owner-reported behavior. Cover: FAIL.**
[Additive review](docs/qualification/poc4-attempt4-physical-review-2026-09-17.md) and
[attestation](docs/qualification/poc4-attempt4-pi3b-owner-report-2026-09-17.json) bind
exact attempt #4. Fresh flash/basic setup/Menu/pre-run VT, VICE/F10/Quit, immediate
Menu keyboard and post-return VT pass. Owner reports each available profile returned
to responsive Menu. Attempt #3 dead keyboard/VT is NOT REPRODUCED; its precise cause
is not retrospectively proven. Unreported setup/network/media/application/service/
persistence tests remain UNTESTED. Original build/procedure records stay unchanged.

Read-only card collection is BLOCKED: rootfs on `/dev/disk4s2` is currently writable
in Paragon. Only device/mount metadata read; no card identity/diagnostics/private files,
card writes, remount or repair. Owner asked to make rootfs read-only. Card identity is
UNVERIFIED pending that gate. Master raw/XZ/lock/component identities and two previous
checkpoint manifests rehash correctly. Owner's accepted unknown historical journal
semantics does not establish a currently read-only mount or pristine forensic capture.

Confirmed source mismatch: lifecycle passes an opened `/dev/tty` descriptor, while
Cover admits only a literal `/dev/tty1` result from `tty`. Isolated host PTY reproduces
alias naming; 3/3 wrapper characterization and existing 9/9 lifecycle tests pass.
This is a strong Cover cause hypothesis, not a recovered Pi diagnosis. New phase
records have not been read. Prepared collection refuses writable/mismatched identity.

Network gap confirmed: pcbm-info/schema/UI expose only name/link state. Review proposes
bounded authoritative per-interface type/state/IP/MAC/optional active SSID and reuse
of existing System Information/Network status, without credential reads or Menu probes.
[Quiet/fast boot backlog](docs/design/boot-experience-backlog-2026-09-17.md) is separate,
measurement-first work; known-good getty/PAM/TTY/session must remain intact.

No runtime/source correction, version/tag/package/image or boot change: top scopes
still describe the completed single-candidate milestone; new request conditions code
changes on source-work scope. AGENTS unchanged. Evidence is
`qualification/poc4-attempt4-physical-2026-09-17`; recovery is
`archive/poc4-attempt4-physical-review-2026-09-17`. Manifest/restore report bind final
refs, full bundles, offline refs/peeled tags/symbolic HEAD/fsck, tests and preserved
artifact references. No images duplicated. No push/publication or physical test by Codex.

**ONE next owner action: make rootfs read-only through Paragon and resume allowlisted
attempt #4 evidence collection.** Do not reflash/build another candidate. Review and
explicit bounded source scope are needed before implementing the proposed changes.
Earlier dated checkpoints below retain their original contemporaneous statements.

# POC4 corrective attempt #4 complete — 2026-09-17 / OWNER REVIEW

**READY TO FLASH: YES. READY FOR OWNER PHYSICAL TEST.** One new private engineering
Project CBM **1.1.0-poc.4 / private-engineering-poc4, attempt 4** passed construction
and offline validation. [Report](docs/build/private-poc4-attempt4.md),
[exact results](docs/build/private-poc4-attempt4.json),
[hash-bound Pi 3B procedure](docs/qualification/poc4-attempt4-pi3b-regression.md).
Physical Cover/KMS/VT/keyboard and Wi-Fi behavior remain UNTESTED; no root-cause proof.

Frozen integration `f5511e10154e6db93f472716e9ddefd04abadb26`; Menu `v1.1.0_poc4.2`, peeled
`171e67b3de181074245fb2bdc70cb60af5688b8e`. New Runtime `1.1.0~poc4.1-1`, Menu
`1.1.0~poc4.2-1+pcbm1`; unchanged VICE/TCPser/media/optional inputs reused exactly.
Schema-4 lock `inputs/frozen-poc4-attempt4/release-lock.json`, SHA-256
`b3430b626d5156c582f4e3e457d47916a16b527c3dcf7586a90cae96c3882b72`; all 2,872 retained objects verify.

Raw `artifacts/private-poc4-attempt-4/2026-09-17-project-cbm-1.1.0-poc.4-lite-private-poc.img`: 3087007744 bytes,
SHA-256 `f699595fdd31a7f8125bb1882ce8d468ce7dd1b4734d85986b1962e992875b21`.
XZ `artifacts/private-poc4-attempt-4/image_2026-09-17-project-cbm-1.1.0-poc.4-lite-private-poc.img.xz`: 597616864 bytes,
SHA-256 `076a42911faa24bc4f2d4c225c92d621498261b630e63de35b6c7dc8af0760e2`. Raw/XZ equivalence and external copies PASS.

206 offline checks, FAT/ext4/systemd, 127 ELF objects and 672 package identities PASS.
Product native 156/156; Menu native/host 70/70; installed lifecycle 9/9 plus all seven
SDL Covers and three renderer/VICE-fixture cycles PASS. Product host final 155/156:
the same known macOS mktemp expectation FAIL, not a product/Linux blocker. Initial
154/155 result is retained separately. Native setup/privilege/accounts/services/import
pass within namespace limits; no physical Pi behavior is inferred.

Root capacity 2,430,955,520; used 1,651,539,968; ordinary-user available 635,551,744 bytes
before expansion. No minimum card claim. Before/after host inventory/update guards PASS,
no drift; builder stopped, no build mounts/loops/processes. Lifecycle terminal/Cover
phase diagnostics and corrected first boot are verified in the actual image.

Recovery: `archive/poc4-attempt4-2026-09-17`; manifest/restore report bind final refs,
full bundles, offline refs/peeled tags/symbolic HEAD/fsck, inputs/artifacts and procedure.
Evidence: `qualification/poc4-attempt4-2026-09-17`. Earlier candidates and accepted source
checkpoint verify unchanged, as do 1,677 original historical entries. Both AGENTS files
and owner-scope commits remain intact. Private StrikeTerm/public-rights gate, Cover
constituent rights, independent encrypted custody and reproducibility limits remain.

**ONE next owner action: flash the exact new image and perform the linked Pi 3B
physical regression procedure.** Prioritize responsive Menu/VT before and after
RUN/Cover/VICE/F10/Quit, three cycles; collect diagnostics on failure before reboot.
Then qualify first boot, Wi-Fi, media/audio/input, applications/utilities, USB, services
and persistence. STOP for owner review. No second build, physical test by Codex, other
model, unrelated backlog, boot optimization, PSID/RSID work, push or publication.
Historical checkpoints below retain their original dated wording.

# POC4 corrective attempt #4 preparation — 2026-09-17

Top AGENTS owner scope at `59c36d15d5a5f619895262aa6a02e6c5d9ca31e3` authorizes
one corrective engineering candidate. Menu scope is actually `aeb4350`, not the
prompt's `deb4350`. Both AGENTS files remain unchanged. Both worktrees began clean.
Accepted source checkpoint manifest verifies as
`b79f26c9649e24c4532d1e1545f15e0a142b9ad183c2eab903740187b3744ed3`, with all 73 files
and accepted current source bytes matching. Prior candidate inputs, artifacts,
checkpoints and protected refs rehash correctly; see new external evidence
`qualification/poc4-attempt4-2026-09-17/starting-preservation.json`.

Designation remains **1.1.0-poc.4 / private-engineering-poc4, attempt 4**: a corrective
iteration of the same POC4 milestone, consistent with attempts 2/3 and the recovery
contract's distinct lock/build ID per changed input. No POC5 scope is introduced.
New Runtime package is `1.1.0~poc4.1-1`; new independent Menu is
`1.1.0_poc4.2` / `1.1.0~poc4.2-1+pcbm1`. VICE/TCPser, artwork, qualification media,
optional payloads, upstream factory and package closures are unchanged inputs.
Only package metadata, image date, new freeze recipe and corrective validator change
beyond accepted source. No runtime feature expansion or historical validator mutation.

Prebuild host suites reproduce Product 154/155 (known macOS mktemp expectation FAIL)
and Menu 70/70 PASS. New validator rejects stale/missing/symlinked payloads. Builder
started: native arm64/ext4, roughly 50.9 GiB guest and 919 GiB external free; exact host
package/update guard PASS. No package, lock or image produced yet. Next: build changed
packages, native/install validation, distinct freeze, one construction, complete
offline validation and recovery; then hash-bound Pi 3B owner handoff. Physical tty/KMS,
Cover visibility and Wi-Fi remain UNTESTED. No push or physical testing.

# Project CBM current state

## POC4 run 2 evidence and defensive source corrections — 2026-09-17

[Owner-review report](docs/qualification/poc4-run2-source-review-2026-09-17.md) and
[separate run2 attestation](docs/qualification/poc4-attempt3-run2-2026-09-17.json)
supersede the evidence stop below. Owner accepted read-only engineering extraction
from the used Paragon-mounted card, not pristine forensic capture. Root was verified
currently read-only; installed identity matched exact attempt #3. No card writes,
mount changes, repair, new diagnostics or credential/profile reads occurred.

One slot records x64sc on tty1, UID1000, KMSDRM/OpenGL 1080p60, VICE exit0/no signal.
Before Cover is uninstrumented; before.json is **after Cover, before VICE**. No
postcleanup snapshot exists. Physical Cover and keyboard/VT causes/relationship remain
UNKNOWN. Owner's second run establishes working keyboard/VT before RUN and failure
after return. Nine allowlisted card files and five verified photos are retained in
`qualification/poc4-run2-2026-09-17`; inventory SHA-256
`4852ff9f49f5f785fdead33ec28cdda5dccae2d72a7b63676b4de5f8af5aa23b`.

Source commits (not installed in the frozen candidate):

- Product `77afb0187835df68847e4f897621598ff4485367`: second-run evidence/collection exception.
- Product `83241a145ad69dfb6579d0b6fd88ec83c6e66451`: pre-Cover terminal ownership,
  same-foreground-group bounded Cover, readback restoration and structured diagnostics.
- Product `d7a74bcfde422ca289ab0c9438877e1a89ca3f4d`: retry-safe setup networking,
  fixed result codes, region prevalidation and compound-command budget.
- Menu `be16c4033a748366c01dea8229f4afa0757bddd1`: guarded `run-with-cover` handoff,
  renderer stage telemetry/cleanup and no held-key skip.
- Menu `e3a82eee578691ae1f648c38e06859abfd627f46`: common human-readable choices,
  Back/retry/resume, working feedback, explicit hidden-password explanation.
- Menu `020294c`: three consecutive Menu launch/return fixture cycles.
- Menu follow-ups hide internal selection tags and return Advanced Back to its
  selection screen; exact commits are in the recovery source inventory.

These are defensive correctness/instrumentation changes, **not root-cause proof or a
physical fix PASS**. Host validation: Product 155 tests, 154 PASS and the same pre-existing
unsandboxed macOS mktemp expectation FAIL; Menu 70/70 PASS. Nine focused lifecycle tests
PASS, including real PTY three-cycle restoration and child timeout/signal/reap behavior.
Earlier sandboxed Product full suites passed153/153 before the last two focused tests
were added; do not hide the final retained context-dependent failure. ShellCheck absent;
per-file Bash syntax, Python parsing, JSON, local links and diff/secret scans pass.
Native installed Linux SDL/VT/network/account behavior remains UNTESTED in this slice.

Related recovery: `archive/poc4-run2-source-correction-2026-09-17-verified`. Its manifest binds
final refs/bundles/offline restore/fsck, source inventory, validation and prior evidence
references; original images are not duplicated. Earlier checkpoint's 50 files and its
preserved POC3/POC4 artifact references rehash correctly; run2 copy/photo hashes agree.
Independent encrypted custody remains unresolved. Owner-scope commits 8a93683/be73ff1,
both AGENTS files, protected refs/tags, all frozen candidates/packages/locks and artwork
are unchanged. No package build/version/tag, VM start, image, physical test or push.

**One next owner action:** review the linked source report and authorize a separate
next-candidate milestone. It needs rebuilt/versioned Product runtime and Menu, refreshed
integration/lifecycle/schema/test inputs, native installed validation and the unbound
[physical regression procedure](docs/qualification/poc4-next-candidate-regression-draft.md).
No candidate hashes or READY TO FLASH claim exist for these corrections. Stop at this
explicit build boundary. Remaining application/service/persistence tests stay UNTESTED.
Historical completed checkpoints below retain their original dated statements.

## POC4 attempt #3 physical regressions — 2026-09-17 / EVIDENCE STOP

The owner physically tested exact attempt #3 on Pi 3B. First boot, Menu, VICE,
F10/Quit and visual Menu return passed; **Cover visibility and post-return keyboard,
Ctrl+Alt+F2 and Ctrl+C failed**. mc launched; SID-Wizard/StrikeTerm presence is not
functional qualification. First-boot feedback/navigation/technical input/password UX
defects are recorded. [Additive results](docs/qualification/poc4-attempt3-pi3b-owner-report-2026-09-17.json)
supersede prior physical-UNTESTED claims only for the reported observations.

[Full investigation and owner review](docs/qualification/poc4-regression-investigation-2026-09-17.md)
compares exact POC3/POC4 source/inputs. Base package hashes and VICE are unchanged.
New Cover timeout/SDL cleanup followed by saving already-altered keyboard state is a
strong candidate; **neither physical cause nor a shared cause is confirmed**. No used-card
logs were found in retained evidence, and Cover status/mode data were not logged.
No lifecycle/first-boot source correction was selected at the owner's evidence stop.

5,681 frozen input/image/checkpoint files rehash correctly; a separate 14,163-file
earlier-evidence check also passes (overlapping scopes, not a unique total).
Menu 65/65 baseline tests
and launcher checker pass; Product 142/143 pass, with one existing macOS mktemp
expectation failure. Host/headless tests cannot qualify physical KMS/VT/input behavior.
[First-boot audit](docs/qualification/poc4-first-boot-ux-findings-2026-09-17.md) records
confirmed source defects and required later corrections; no credential bytes retained.

Inputs remain POC3 integration `0a0e271d86c68a969d8b18189c561ed51a8b0e09`, Menu
`897cee7c792b11bfed80168a576f263340f5f57d`; POC4 integration
`b362c70215cef0e2c6c6a845635c47fd39b3ebbf`, Menu
`407ced58b711209631cdfb4db6dcd741a555f408`. Attempt #3 lock SHA-256 remains
`435c6e0d7a5a45eaff3f45af6d384fca5b602139fa9fb640950e2f5e7b4f39a9`;
raw `37d2699c7a639e050e531a4d5a132d4b197e5a60270a969814c573f436036cd8`.
Frozen artifacts, owner-scope commits `8a93683`/`be73ff1`, tags and AGENTS are unchanged.

Evidence: `qualification/poc4-regression-2026-09-17`; recovery:
`archive/poc4-regression-investigation-2026-09-17` under configured external storage.
Its manifest/restore report records final ordinary docs commits, bundles and checks.
Product evidence commit: `8736383` (physical attestation and investigation/procedures).
Menu continuity commit: `1a075433d4217dea1a12f68e311caceafb7cf7b1`.
No new package/version/tag, release lock, image, physical test, VM start or push.
Independent backup/custody and rights gates remain unresolved. The next-candidate
[physical draft](docs/qualification/poc4-next-candidate-regression-draft.md) is unbound,
NOT READY TO FLASH. Dosbian-derived organization remains unaccepted backlog input.

**One next owner action:** [collect existing used-card diagnostic/setup/identity evidence
read-only](docs/qualification/poc4-regression-collect-evidence.md), without reflash or
another VICE launch. If the failed live session still exists, report that before power-off.
Stop for owner review; do not proceed to source changes or candidate construction until
the missing evidence is assessed. Earlier completed checkpoints below retain their
historical wording and do not describe the current physical qualification state.

## POC4 attempt #3 complete — 2026-09-16 / STOP FOR OWNER REVIEW

**Build PASS. READY FOR OWNER PHYSICAL TEST. READY TO FLASH: YES.**
Project CBM **1.1.0-poc.4 / private-engineering-poc4, attempt 3** is built and
fully offline-validated. Physical qualification remains **UNTESTED**.
[Build report](docs/build/private-poc4-attempt3.md),
[exact results](docs/build/private-poc4-attempt3.json),
[hash-bound Pi 3B procedure](docs/qualification/poc4-attempt3-pi3b-smoke-test.md).

Frozen integration `b362c70215cef0e2c6c6a845635c47fd39b3ebbf`; Menu
`v1.1.0_poc4.1`, peeled `407ced58b711209631cdfb4db6dcd741a555f408`.
Lock `inputs/frozen-poc4-attempt3/release-lock.json`, SHA-256
`435c6e0d7a5a45eaff3f45af6d384fca5b602139fa9fb640950e2f5e7b4f39a9`. No frozen input changed.

Artifacts under `artifacts/private-poc4-attempt-3` in configured bulk storage:

- Raw `2026-09-16-project-cbm-1.1.0-poc.4-lite-private-poc.img`, 3,087,007,744 bytes,
  SHA-256 `37d2699c7a639e050e531a4d5a132d4b197e5a60270a969814c573f436036cd8`.
- XZ `image_2026-09-16-project-cbm-1.1.0-poc.4-lite-private-poc.img.xz`, 598,813,860 bytes,
  SHA-256 `4a6bce98e089e3c39246393b7476c687a7818ea5a6b67fa811fb6bee8da5a83e`.

121 main + 20 supplemental + 26 Cover/utility checks, FAT/ext4/systemd integrity,
127 ELF objects, all 672 installed package identities, raw/XZ agreement and external
copy hashes PASS. Root used 1,651,511,296 bytes; ordinary-user available capacity
635,580,416 bytes before expansion. Post-expansion capacity/margins remain UNTESTED.

Both repositories began clean with matching current owner scopes. Historical refs,
POC1–3, attempts #1/#2 and both attempt #3 prebuild/blocked checkpoints verify intact.
The owner had removed the excluded staging copies; no additional cleanup/deletion.
Builder configuration, frozen kit, environment/TMPDIR protection and before/after host
inventory/update guards PASS. Exactly one construction succeeded; VM stopped, no active
build/proxy/mounts/loops. No AppArmor, authentication, package or rights gate weakened.

Recovery: `archive/poc4-attempt3-2026-09-16`; final refs, bundles, manifest and exact
offline restoration/fsck are recorded there. Evidence:
`qualification/poc4-attempt3-construction-2026-09-16`. Both branches remain local.
Earlier artifacts/locks/checkpoints are immutable; earlier stop entries below are history.

SID-Wizard 1.97, privately admitted StrikeTerm, all seven Covers, mc/Advanced Mixer,
first boot/owner/admin/config/info/network/services/USB and original media are installed.
Third-party reference SID/demo media remain unbundled. PSID/RSID playback remains deferred;
StrikeTerm public rights and constituent Cover rights remain separate gates.

**Next owner action:** review, then the exact-hash Pi 3B procedure. First boot/expansion/
interruption, owner UI, real display/audio/input, Cover handoff, USB, applications and
persistence need physical evidence; radio/AP, service clients and BBS need external
environments. Independent rebuild/reproducibility and independent custody remain open.
No automatic physical test, next candidate, other model, boot optimization, SID-player
implementation, push or publication. STOP for owner review.

## POC4 attempt #3 explicit resume — automatic review rejected again / STOP

The owner explicitly authorized the frozen build, narrow AGENTS reconciliation and
exact two-path disposable cleanup. Automatic approval again rejected both the policy
reconciliation commit and the separately submitted exact-path cleanup, describing
owner authorization as untrusted transcript content. Neither command ran. Temporary
AGENTS/CURRENT-STATE reconciliation edits were removed; AGENTS remains unchanged.
No deletion, VM start, input change or build. Both accidental copies still exist.

[Resume report A–AD](docs/build/poc4-attempt3-resume-blocked.md) records exact rejection
reasons and limits. Read-only verification: original lock/checkpoint hashes unchanged,
32 checkpoint files and 25 retained evidence files PASS; both deletion paths resolve
exactly and are explicitly excluded. No accepted evidence removed. Existing prebuild
results remain accepted; no image/physical pass is claimed.

Subsequent stop checkpoint: `archive/poc4-attempt3-resume-blocked-2026-09-16`.
Keep the earlier `archive/poc4-attempt3-prebuild-blocked-2026-09-16` unchanged.
Next: resolve execution approval's refusal to recognize the already-explicit owner
instruction. Do not re-freeze, bypass the review, retry automatically or flash attempt
#2. The prepared attempt #3 procedure stays NOT READY TO FLASH. All original security,
input/host/build/validation stop gates remain. No push/publication.


## POC4 attempt #3 — 2026-09-16 / APPROVAL-BLOCKED BEFORE BUILD

**No attempt #3 image exists. Do not physically test attempt #2 instead.**
Owner authorized the bounded Combian/Covers build. Automatic approval review rejected
construction by treating an older AGENTS boundary as prohibiting image builds, then
rejected an attempted authorization-documentation commit. That uncommitted AGENTS
addendum was removed. AGENTS is unchanged; no alternate build route was attempted.
This is not a new image-construction failure: pi-gen never ran for attempt #3.

[Complete A–AI owner report](docs/build/poc4-attempt3-owner-review.md),
[exact frozen identities/results](docs/build/poc4-attempt3-prebuild.json),
[unbound physical procedure draft](docs/qualification/poc4-attempt3-pi3b-smoke-test.md).
The [four-file actual V3.7 review](docs/design/combian-v37-bounded-review.md) is complete;
only Advanced Mixer and import destination feedback were adopted. No architecture
reopened. Midnight Commander already exists, unprivileged FILES path retained.

Product identity 1.1.0-poc.4 / private-engineering-poc4, attempt 3. Frozen integration
`b362c70215cef0e2c6c6a845635c47fd39b3ebbf`; Menu `v1.1.0_poc4.1`, peeled
`407ced58b711209631cdfb4db6dcd741a555f408`, package `1.1.0~poc4.1-1+pcbm1`, API 1,
SHA-256 `6df8fb42a10b16e12ac114032accc149c49ebf51f0e5f45c34b77d2cefbb2767`.
All seven unchanged Covers are packaged; runtime/VICE/TCPser exact packages reused.
New lock `inputs/frozen-poc4-attempt3/release-lock.json`, SHA-256
`435c6e0d7a5a45eaff3f45af6d384fca5b602139fa9fb640950e2f5e7b4f39a9`, 2,832 objects.
Do not mutate this lock or confuse its distinct inputs with attempt #2.

143 Product / 65 Menu tests and launcher checker pass. Native Linux package/API,
AppArmor/dpkg, owner/authentication, helpers/services, USB loop, optional payloads,
Cover SDL lifecycle/timeout and utility checks pass within documented limits.
Host drift guard passes; VM stopped. Offline image validation NOT RUN; no raw/XZ hashes.
Historical tree, POC1–3, POC4 attempts #1/#2 and existing refs/tags preserved.

Evidence: `qualification/poc4-attempt3-2026-09-16`; recovery:
`archive/poc4-attempt3-prebuild-blocked-2026-09-16`. During evidence transfer, an rsync
filter accidentally copied partial disposable trees into that evidence directory's
`native/environment/` and `native/runtime/`. Transfer stopped; automatic review rejected
cleanup. These two directories are **excluded from recovery/evidence manifests**, may
contain synthetic private state, and must not be published/restored. Exact-path cleanup
needs owner review. Bounded top-level logs/scripts are separately inventoried.
Independent backup/custody remains unresolved.

**Next owner action:** resolve automatic approval for the exact frozen attempt #3
build and those two accidental-copy cleanups. Resume the ONE build only after resolution,
then perform complete offline validation/hash binding/recovery before any Pi test.
Do not rebuild/re-freeze merely to bypass the block. No physical test, other Pi model,
boot optimization, SID-player implementation, push or publication. Earlier checkpoints
below remain historical; their old next-action instructions are superseded by this one.

## Cover source follow-up — 2026-09-16 / STOP

The owner subsequently requested preservation of existing Menu COVERS. The bounded
[cover implementation](docs/runtime/covers.md) is source-complete, with exact unchanged
artwork, registry-driven shared-launcher selection, unprivileged short SDL transition,
and nonfatal bounded fallback. 60 Menu tests/launcher checker and native headless SDL
lifecycle/timeout tests pass. Physical KMS/VT/VICE handoff remains UNTESTED.

**The already-frozen POC4 attempt #2 below does not contain this later work.** Its image,
lock/packages/checkpoint remain immutable. No additional image/package was built.
Source checkpoint: `archive/covers-source-2026-09-16`; native evidence:
`qualification/covers-source-2026-09-16`. Owner identified the existing /covers artwork
as theirs; constituent third-party graphics/fonts have not independently been cleared
for public distribution. See the exact Menu artwork manifest and evidence limits.

**Next owner action:** review the successful attempt #2 plus this source-only follow-up.
If covers are required for the next physical test, authorize new versioned Menu packaging
and a distinct frozen POC4 build attempt; do not retag/reuse attempt #2. Bind the
[cover test addendum](docs/qualification/covers-next-candidate.md) to the new hashes.
No physical test, additional build, other Pi model, boot optimization or publication
has occurred. Earlier completed checkpoints below remain historical records.

## POC4 attempt #2 complete — 2026-09-16 / STOP

**Project CBM 1.1.0-poc.4 / private-engineering-poc4, build attempt 2, is built and
offline-validated. Physical qualification remains UNTESTED.** POC3 remains the previous
physically demonstrated Pi 3B foundation. [Report](docs/build/private-poc4-attempt2.md),
[exact inputs/results](docs/build/private-poc4-attempt2.json),
[exact-hash Pi 3B procedure](docs/qualification/poc4-attempt2-pi3b-smoke-test.md).

Attempt #1 below is immutable FAILED construction evidence, no image. Its root cause
was confirmed by actual native mktemp/AppArmor failure followed by sanitized success.
[Environment boundary](docs/build/environment-boundary.md): fixed factory/debootstrap/
chroot environments, valid target /tmp, no AppArmor or package-check weakening.

Frozen integration: `93d264adf3bac6a397112ecd7349ab8105257852`.
Menu remains `v1.1.0_poc4`, peeled `bb8a66ea9da994b30f978ad87d61c9aedb03dad6`.
All component packages/source mappings and optional/media inputs match attempt #1.
Integration source, declared pi-gen patch and sealing recipe changed; complete inputs
and generated installed identity are not identical.

Lock: `inputs/frozen-poc4-attempt2/release-lock.json`, SHA-256
`27f0e8ca522f745e240d088fc8fe8feab8f98c15eb165d72fad1a9ef18ee3fdf`.
Artifacts under configured bulk workspace `artifacts/private-poc4-attempt-2`:

- Raw `2026-09-16-project-cbm-1.1.0-poc.4-lite-private-poc.img`, 3,087,007,744 bytes,
  SHA-256 `e7c0b971ff3c12c09483477f760a09718a038143384774a7d43eca4a790aa217`.
- XZ `image_2026-09-16-project-cbm-1.1.0-poc.4-lite-private-poc.img.xz`, 597,702,372 bytes,
  SHA-256 `0ced0321d84777a0e65ac4ebbf4bbae7c42f5680ceba37dc16a5820e5ec50bdf`.

142 product + 50 Menu tests and launcher checker PASS; actual Linux package/AppArmor,
owner authentication, helper, setup/offline, service, NetworkManager credential and USB
broker revalidation PASS within documented namespace limits. 121 main + 20 supplemental
offline checks, FAT/ext4 integrity, systemd units, 113 ELF closure objects and raw/XZ
agreement PASS. Host inventory/environment unchanged; VM stopped, no live build mounts,
loops or proxy. No builder credentials/identity or full recovery kit in the image.

SID-Wizard 1.97 core is installed with immutable template/user working disk. StrikeTerm
2014 Final is PRIVATE-ENGINEERING-ADMITTED / PUBLIC-RELEASE-RIGHTS-GATE-PENDING. Public
rights gate remains fail-closed. Requested SID/demo reference payloads are owner-supplied,
not bundled. Generic .sid autostart is refused; dedicated PSID/RSID playback remains open.

Recovery: `archive/poc4-attempt2-2026-09-16`; evidence:
`qualification/poc4-attempt2-2026-09-16`. Checkpoint manifest records final refs, bundles
and verified offline restore. Both feature branches remain local; no push/publication.
POC1–3, historical tags and attempt #1 checkpoint/2,834 retained files verify unchanged.
Independent clean-rebuild reproducibility and independent backup/custody remain open.

**Next owner action:** review the result, then perform the exact-hash attempt #2 Pi 3B
procedure. First boot/interruption recovery, real hardware, owner UI, networking/external
services, USB discovery and optional applications need physical evidence. Stop at failure,
retain diagnostics, do not repair the running candidate. No automatic next build, other
Pi model or publication. Boot optimization stays deferred until this physical gate passes
unless a more important blocker emerges. Earlier checkpoints below are historical.

## Runtime activation: build-integrity stop — 2026-09-16

**No POC4 image exists. STOP for owner review; do not flash, retry or build another
candidate automatically.** POC3 remains the last physically demonstrated Pi 3B
foundation. [Attempt/report](docs/build/poc4-blocked.md), [exact inputs](docs/build/poc4-blocked.json),
[native staging evidence](docs/build/runtime-activation.md).

First-boot/owner administration, the fixed backend, NetworkManager/service adapters,
USB broker, boot preferences and matching runtime/Menu packages are source-implemented.
138 product tests, 50 Menu tests plus the launcher checker pass. Native Debian tests
verified package installation, account/PAM/sudo, helper restrictions, offline setup,
services, private Wi-Fi keyfiles, terminal return and synthetic-media import. This is
not physical qualification or proof that all candidate/runtime gates are complete.

Integration: `cf3a289f99bd7599c8e6f1aa3da4753aa733f981`.
Menu: `v1.1.0_poc4`, peeled `bb8a66ea9da994b30f978ad87d61c9aedb03dad6`.
New schema-4 lock: `inputs/frozen-poc4/release-lock.json`, SHA-256
`99f3985b8eac77398fbc71d66160f91beff50d04f6ae246757a4f081436bfacc`.
The lock and packages remain frozen evidence of this failed attempt.

Image construction failed during upstream stage1 AppArmor package configuration:
the operator invocation exported a builder-only TMPDIR into the target chroot;
`mktemp` could not use that absent path. No AppArmor/security bypass, frozen-input
mutation, image repair or retry was attempted. Host inventory remained pinned; no
build mounts/loops or proxy remain. The VM is stopped. See the report for the exact controlled failure.

SID-Wizard 1.97 core is frozen under its accepted license. Author-endorsed StrikeTerm
2014 Final bytes match the recorded Combian hash and are **PRIVATE-ENGINEERING-ADMITTED;
PUBLIC-RELEASE-RIGHTS-GATE-PENDING**. Neither was delivered in a new image. Requested
reference SID/demo payloads remain owner-supplied. Generic `.sid` autostart is blocked;
a dedicated PSID/RSID player remains a later gate.

Branches: product `feature/1.1-build-foundation`; Menu `feature/1.1-debian-package`.
Recovery checkpoint: configured bulk storage `archive/runtime-activation-blocked-2026-09-16`;
exact final refs, bundles and restoration verification are in its manifest. Build
logs: `qualification/poc4-build-blocked-2026-09-16`; final packages: `packages/poc4-final`.
POC1–3 and historical refs remain immutable. No push/publication or physical test.
Independent backup/custody and independent clean rebuild remain unresolved.

**Next owner action:** review the stopped attempt and authorize a bounded build-host
versus chroot environment fix, regression test and new attempt location/input identity
as needed. `/tmp` inside the external-backed Linux guest is not the Mac's internal
`/private/tmp`. Do not remove AppArmor or weaken security to get an image. Complete
remaining staging/offline/qualification-procedure gates before any physical test.
Boot presentation/performance stays deferred until a new candidate physically passes.

Earlier sections below are completed historical checkpoints and do not supersede
this stop or the private StrikeTerm decision.

## Optional applications and reference-content addendum — 2026-09-16 / STOP

Configuration maturation below remains complete. The owner additionally authorized
SID-Wizard/StrikeTerm source integration and rights/provenance research for selected
SID/demo references. [User guide](docs/runtime/optional-applications.md),
[exact input/rights/factory contract](docs/runtime/optional-applications-contract.md),
[reference findings](docs/design/reference-content-2026-09-16.md).

SID-Wizard **1.97 native one-SID core** is admitted under its author's explicit
permissive notice. Source hash/member selection and deterministic D64/tar are retained;
no example music, host application or full manual is installed. Schema 3 declares
optional source/recipe/rights/payload inputs; schemas 1/2 and frozen locks remain intact.
The stage installs a template/notice and fresh user working disk only when declared.
No new full candidate lock, package, image, upstream binary rebuild or physical pass.

StrikeTerm 2014 remains **OWNER-SUPPLIED**: source/version/author references resolved,
complete-disk redistribution permission and upstream-byte comparison unresolved.
CONTENT now asks the profile authority to route the two application folders to
validated x64sc without changing the user's normal default. Shared launcher, F10,
geometry, session, diagnostics, audio and privilege policy are unchanged.

All **17 requested SID/demo references remain OWNER-SUPPLIED**. HVSC #85 metadata
establishes 14 exact SID paths; Last Party's HVSC version is D500, not D420. No requested
reference media was acquired. Wonderland XIV is a four-side D64 production; no clear
redistribution grant or current VICE compatibility was established. SID discovery
still does not establish PSID/RSID playback: a validated SID-player route remains
future product work. Safe USB import remains pending the constrained broker.

120 product tests and 44 Menu tests plus the launcher checker pass. Actual admitted
source/subset hashes, deterministic preparation and small-directory staging verified.
Mac routing median: 0.058 ms warm / 25.2 ms new process plus registry; not a Pi budget.
[Validation](docs/runtime/optional-software-validation.json),
[performance](docs/runtime/optional-software-performance.json),
[future application physical procedure](docs/qualification/optional-applications-procedure.md).

Product branch: feature/1.1-build-foundation. Menu: feature/1.1-debian-package.
Menu source commit: `9f74202986ed16fde9f9b1f9da8cace70e784b72`.
Exact output refs/bundles are recorded in the verified external checkpoint
`archive/optional-content-2026-09-16` under the configured bulk workspace.
Retained inputs: `inputs/optional-software-2026-09-16` (input fragment, not a full lock);
original source review: `inputs/optional-software-review-2026-09-16`.
Prior checkpoints and POC1–3 remain immutable. Independent backup/custody unresolved.

**Next owner action:** review this addendum, then authorize first-boot/owner-account
and runtime activation integration in Linux staging, including matching versioned
packages and these optional-content contracts. SID/PSID/RSID dispatch, safe import
and service/modem gates require implementation/qualification; no new architecture
study. Do not automatically build POC4, test hardware, enable services or publish.

## Configuration maturation complete — 2026-09-16 / STOP

The final concentrated Menu/configuration architecture pass is source-complete.
[User guide](docs/runtime/pcbm-config.md), [implementation and activation contract](docs/runtime/configuration-contract.md),
[checkpoint/results](docs/runtime/configuration-maturation.md).

CONTROL opens the coherent Bash/dialog pcbm-config. Nine shallow task areas separate
normal settings, System Information, About and Advanced. pcbm-info JSON remains the
information authority. Registry/default preferences and POC3 launcher/geometry are
preserved. Terminal is a returning child shell; dead QUIT and competing legacy startup,
status/version, generic USB mount and broad service paths are retired. Audio settings
are parsed as data and saved atomically, not sourced as shell.

Product now implements schemas, unprivileged JSON client, fixed validated root adapters
and separate authenticated owner/raspi-config dispatch. Normal UI never asks for broad
sudo; owner administration uses a separate initialized account and ordinary authenticated
sudo. No root helper/policy/sudoers/account or service was installed in this source pass.

**Pending runtime activation:** matching versioned packages, first-boot owner credentials,
trusted helper/policy setup, NetworkManager and each service's explicit readiness.
Boot intent still needs its session consumer; typed TCPser settings need a fixed launch
adapter; safe USB import needs the constrained broker defined in the contract. These
are pending implementation/integration gates, not claims of working runtime features.
Services remain off/masked in POC3. No new image/package, VM start, Pi test or publication.

108 product tests, 43 Menu tests plus the launcher checker pass. Schema/syntax/link/
privacy/size/tag checks and sudoers syntax pass. Mac fixture timings are retained;
real dialog, Linux installation/account/service behavior and Pi performance are untested.
POC1–3 artifacts and historical evidence remain unchanged; all existing tags are intact.

Branches: product feature/1.1-build-foundation; Menu feature/1.1-debian-package.
Menu source commit: `87a16af19e7329b7cf8dbc16ee9420613f35245f`.
Recovery: configured bulk workspace archive/configuration-maturation-2026-09-16,
with exact source commits/ref inventories, both bundles and verified offline restoration.
Preservation report: qualification/configuration-maturation-2026-09-16/preservation.json.
Prior checkpoints remain immutable; independent backup/custody is still unresolved.

**Next owner action:** approve first-boot/owner-account and runtime activation integration
in a disposable Linux staging target. Complete exact package/dependency/authentication/
network/service gates and the required storage/modem/boot consumers before a later
explicitly approved candidate. No more Menu framework/architecture study is recommended.
Do not automatically build POC4, change POC1–3, enable services, optimize boot, include
optional software, test another Pi or push. Earlier sections below are historical
completed checkpoints and do not replace this current state.

## System Information and machine consumers complete — 2026-09-16 / STOP

Menu source commit: `4feda57c2ff1f5d0807a6873c0b88b5d84435bd8` on
`feature/1.1-debian-package`; product stays on `feature/1.1-build-foundation`.

Read the [source checkpoint](docs/runtime/information-machines-slice.md),
[user workflow](docs/runtime/information-and-machines.md) and
[consumer contract](docs/runtime/information-machines-contract.md).

CONTROL now has a read-only System Information view consuming pcbm-info JSON. MACHINES,
RUN, cover selection and the shared content default use the product registry/preferences.
Missing user state imports a validated legacy default once; valid new state wins.
Malformed state is preserved with explicit backed-up recovery. No sudo to choose a
default. Boot preference remains inactive; dormant pcbm-start migration is deferred.

86 product tests and 26 Menu tests plus the launcher checker pass. Syntax/schema/link/
privacy/size/ref checks pass; source/fixture Mac timings are recorded, not Pi budgets.
No real dialog/Linux installation or new physical qualification. POC1–3 and all existing
tags remain unchanged. No VM start, package/image build, POC4, service change or push.

Recovery: configured bulk workspace `archive/information-machines-2026-09-16`, with
exact commits/ref inventories, both bundles and verified offline restoration. Earlier
checkpoints remain intact; independent backup/custody is still unresolved.

**Next owner action:** review this slice, then authorize the bounded About/current-status
cleanup described in the checkpoint. Broader CONTROL/settings work and any future
package/image/hardware work require their own scope. The preceding foundation and POC
sections below are historical completed checkpoints, not the present consumer state.

## First runtime foundation slice complete — 2026-09-16 / STOP

Owner-approved boundaries now have their first bounded source implementation:
[checkpoint](docs/runtime/foundation-slice.md), [user guide](docs/runtime/pcbm-info.md),
[JSON information contract](docs/runtime/info-contract.md), and
[user preference/profile contract](docs/runtime/preferences.md).

- `runtime/bin/pcbm-info` is read-only, standalone and independent of dialog: human
  output or schema-1 JSON separates built identity, running hardware and current state.
  Missing data is explicit; no network probes, secrets, daemon or Python runtime extras.
  Optional active display mode uses the already-present engineering DRM helper only.
- User-owned typed preferences use XDG config, private permissions, validation, locking,
  atomic replacement and explicit malformed-data recovery. Reads never create state.
  **Not yet wired into the existing Menu/boot consumers**; no automatic legacy import.
- Eleven-profile registry now supplies info/preference validation. Existing Menu/
  launcher mappings remain unchanged until a targeted compatibility migration.
- Menu's opt-in Bash/dialog library defines selection/Cancel/Back/error/result contracts;
  no broad menu reorganization or privileged backend was implemented.

75 product tests (35 new), 10 Menu UI tests, the existing launcher checker and 24
per-file Bash syntax checks pass. Python 3.14.5/Bash 3.2 on macOS; no native Linux
integration or hardware pass claimed. CLI median 43.56 ms, observed peak 21.64 MiB;
these are Mac measurements, not Pi 3/3A+ budgets. ShellCheck unavailable.

Product remains feature/1.1-build-foundation; Menu remains feature/1.1-debian-package
at `fa2e5d8ef46f20c18a7e9735beee1cd1ac5961e3`.
No package/image was built, VM started, POC4 created, services enabled or code pushed.
POC1–3 and existing tags are unchanged. Recovery checkpoint:
`archive/runtime-foundation-2026-09-16` under configured external bulk storage, including
both bundles, exact source identities, test/performance/preservation evidence and
offline restoration report. Prior checkpoints remain intact. Independent backup remains
unresolved; this checkpoint alone is not a second custody location.

**Next owner action:** review this source slice, then authorize the targeted information
view and machine-preference/registry consumer migration described in the checkpoint.
No broad configuration redesign, first boot, network/service implementation, optional
software, new image or additional hardware testing is authorized automatically.
The POC3 physical/audit results below remain the preceding completed checkpoint.

## POC3 physical pass and product audit — 2026-09-16 / STOP

**Exact POC3 passed the owner's bounded Pi 3B appliance/geometry smoke test.**
The [additive physical attestation](docs/qualification/poc3-pi3b-owner-report-2026-09-16.json)
supplements the unchanged planned/build records below. Boot/Menu, both VT directions,
x64sc/C64 rendering and corrected geometry/pillarboxing, keyboard, smoke/SID/video-input
PRGs, all three expected SID tones, joystick, D64, F10/Quit/return and reboot passed.
No new failure was reported. Other machines/models/PAL–NTSC comparisons, measured mode,
network/services/setup, broader persistence and clean-rebuild reproducibility remain
unestablished. POC1's precise cause and POC2's exact scaling component remain unconfirmed.

Seven owner photographs were inspected read-only and copied with verified hashes to
`qualification/poc3/pi3b-owner-report-2026-09-16/photos/` beneath configured bulk storage.
The adjacent `evidence.json` SHA-256 is
`f9aef329cf04fb37ef4b11cf7ced0198050625cd5e8368f2502f8985655de422`.
Originals at `/Volumes/TheBench/temp/0?-poc3*.jpg` remain unchanged. No images in Git;
still photos do not prove audio/movement/input transitions. POC3 raw/lock/package
identities remain exactly those in the completed build checkpoint below.

[Product audit and recommended work order](docs/design/appliance-audit-2026-09-16.md)
is the current design checkpoint, with linked Menu/framework, Combian/optional-software
and boot studies. Recommendation: retain familiar Bash/dialog, streamline CONTROL,
separate read-only pcbm-info from configuration UI and narrow product backends, consolidate
preference ownership, and measure boot before optimization. Concrete before/after
workflows cover fewer levels, duplicate actions, unsupported commands and safe saves.
StrikeTerm redistribution remains unverified; SID-Wizard inclusion is conditional on
exact release/license/source review. No optional software acquired or embedded.

POC3 is a suitable basic factory + bounded Pi 3B appliance foundation, **not a release,
beta/RC, all-model qualification or reproducibility proof**. No runtime changes, VM
start, POC4, other-model test, service/SSH enablement or publication occurred. Menu stays
unchanged at `5cf863312a62ac458d5f6c362a9e81b9d14ec20c` on feature/1.1-debian-package.
Product stays on feature/1.1-build-foundation. Documentation/JSON/link/content checks
and external preservation verification are recorded with the additive audit checkpoint:
`archive/poc3-pi3b-product-audit-2026-09-16` (manifest and offline Git restore report).
Earlier checkpoints are retained unchanged; no duplicated image archive is needed.

**Next owner action:** review the proposed boundaries/navigation and authorize one
bounded next implementation slice. Suggested first slice: read-only pcbm-info plus
shared UI/result and preference contracts, then separately approved offline setup and
narrow privileged operations. Do not infer POC4/build or broad modernization approval.
Independent custody/backup, signing/SBOM choices, measured budgets, historical input
closure/build-chain gaps and independent clean rebuild remain unresolved.

The sections below are completed historical checkpoints, not current status or authorization.

## Completed POC3 build checkpoint (before physical test)

**Private POC3 built and offline-validated; physical POC3 remains UNTESTED.**
[Completed build record](docs/build/private-poc3.md), [exact results](docs/build/private-poc3.json),
[presentation policy/findings](docs/build/poc3-design.md) and
[hash-bound Pi 3B procedure](docs/qualification/poc3-pi3b-smoke-test.md) are the current
checkpoint. The [planned physical matrix](docs/qualification/poc3-pi3b.json) has no passes yet.

POC2's Pi 3B core launch/audio/media/return/VT/reboot passes and geometry failure
remain unchanged. POC3 seeds per-chip true aspect + desktop fullscreen once, preserves
saved user preferences and adds bounded presentation/DRM diagnostics. Menu/TCPser,
first boot, tty/getty/PAM, F10/menu/Quit, privileges, service masks and media remain
unchanged. No SSH. Root cause is still unconfirmed: software reference geometry works;
actual Pi/SDL/KMS/display scaling needs the new physical evidence.

- Integration: `0a0e271d86c68a969d8b18189c561ed51a8b0e09`.
- Lock: `inputs/frozen-poc3-final/release-lock.json`, SHA-256
  `3f3180f50e5c990ad63fc3d564a56bbd86b80f9b38c6a4aff7b42ed9438b9f5e`.
- Raw: `artifacts/private-poc3/2026-09-16-project-cbm-1.1.0-poc.3-lite-private-poc.img`,
  3,095,396,352 bytes; SHA-256 `9a8b1e0465c93981dfa6b09772e9e3fbf5c487a915bba0046b5de034f9331f33`.
- XZ: `artifacts/private-poc3/image_2026-09-16-project-cbm-1.1.0-poc.3-lite-private-poc.img.xz`,
  596,947,568 bytes; SHA-256 `e7d9657bfbb1124b38c2f1f3479698e24a34be7234db80d766f189da946ace3c`.
- VICE: `3.10-1+pcbm3`, SHA-256 `c9d798a591c22faa9ffc3141b7f5177ece36a05e53d9d2c8aae1ce93c22fcfbe`.
  Menu `v1.1.0_poc2` / peeled `897cee7c792b11bfed80168a576f263340f5f57d`, TCPser
  and original MIT media are reused exactly; all identities are in the build record.

40 macOS/native Linux tests and Menu launcher tests passed. 12 software-reference
cases cover 11 profiles plus PAL/NTSC; saved preferences/CLI precedence passed.
85 read-only image checks, filesystems/systemd units and 113 ELF dependencies passed.
2,789 frozen objects and raw/XZ agreement verified. 5,503 POC1/POC2 baseline files
and the original 1,677-entry historical manifest remain unchanged. POC2 photographic
evidence references/hashes remain in its formal record, not embedded in Git.

An initial assembly was rejected for builder inventory drift from inherited automatic
APT updates. Its old lock/artifact/log remain separate, **not accepted for flashing**.
The corrected lock retains the exact host supplement; before/after inventory guards
and masked builder update units now prevent accepting that drift. These are builder-only
controls, not changed appliance service policy. See the build record for limitations.

Bulk locators above are relative to configured ProjectCBM-Work. Recovery:
`archive/milestone1-private-poc3-2026-09-16`; detailed evidence: `qualification/poc3`.
Builder is stopped. Product remains `feature/1.1-build-foundation`; Menu remains
`feature/1.1-debian-package` without changes. Nothing published. Independent backup,
clean rebuild, acceptance budgets and full settings UX remain unresolved.

**Next:** owner review, then exact-hash Pi 3B geometry + bounded regression test.
If geometry fails, collect diagnostics and stop without manual repair. No physical
test by this task, POC4, other model, SSH or broader modernization. The completed
POC2 sections below are prior checkpoints, not current authorization/status.

## Completed POC2 review

Updated 2026-09-16 — **POC2 physical Pi 3B smoke test completed; geometry defect remains.**
[Formal physical results](docs/qualification/poc2-pi3b.json) and
[aspect-ratio investigation / narrow POC3 proposal](docs/qualification/poc2-pi3b-aspect-analysis.md)
are the current qualification authority. Boot/Menu/input, diagnostic VT in both
directions, RUN/x64sc, C64 rendering and observed stability, keyboard, F10 menu,
Quit/return, PRG, original SID tones, video/input program, D64 and basic reboot
passed. **Correct aspect-ratio preservation FAILED:** horizontal widescreen stretch.
Joystick was unavailable. Other profiles/models, PSID/RSID, broader configuration
persistence, first-boot interruption, services/setup and clean-rebuild reproducibility
remain UNTESTED. No full model/release qualification follows from this bounded test.

The [completed build checkpoint](docs/build/private-poc2.md) and
[exact artifact results](docs/build/private-poc2.json) remain unchanged historical
build evidence. No POC2 image, lock, package, media or POC1 record changed. VM remains
stopped. No runtime fix, POC3, additional-model test, networking, release or push.

POC1 remains immutable: Pi 3B boot/Menu/input PASS, x64sc display/console recovery
FAIL, later VICE qualification UNTESTED. All 2,731 baseline files, including the
[physical record](docs/qualification/poc1-pi3b-2026-09-15.json), rehash unchanged.
Its physical cause remains unconfirmed. POC2 adds explicit GL runtime, standard
getty/login/PAM tty1, unprivileged shared RUN/content/F10-menu-quit behavior, bounded
persistent diagnostics, non-root tty2 and original declared media. Full settings/
privilege UX remains deferred; masked services are not failures. No broad sudo.

- Integration: `2b894ad187f0b603d2e0c9965aba242073e2cb90`.
- Lock: `inputs/frozen-poc2/release-lock.json`, SHA-256
  `bc1c6e16c32d6285973933b8d50371899bc18e5407dd654c9a14d1187eb194ac`.
- Raw image: `artifacts/private-poc2/2026-09-16-project-cbm-1.1.0-poc.2-lite-private-poc.img`, 3095396352 bytes,
  SHA-256 `ef221dc09ea65d3976f88e65cde8f153a9c32989be09c6b35d545b111ccb7467`.
- XZ image: `artifacts/private-poc2/image_2026-09-16-project-cbm-1.1.0-poc.2-lite-private-poc.img.xz`, 596406680 bytes,
  SHA-256 `757aca812835c676d75eaad651b6739fc79461c25c8aa7426524f6692a6b3d9f`.
- Menu input: `v1.1.0_poc2`, peeled `897cee7c792b11bfed80168a576f263340f5f57d`,
  package SHA-256 `e29bc3598f3be0869f79184250f88a03f4c59f1304a20a428223bac58c97bd11`.
- Original MIT media: source `14e4ade77ec83e0429d194a6b5ecfa5ef7655e75`,
  bundle SHA-256 `61673c45058ba31d2e28c699c631e99173c4e44b8b49c82c83735c2c5614d0af`.

Paths are relative to configured bulk storage, currently TheBench/ProjectCBM-Work.
34 macOS/native Linux tests, shared Bash launcher tests, 79 image checks, read-only
filesystem/unit checks and 112 ELF-object closure checks passed. All 2,738 retained
objects rehashed, XZ/raw agree, historical 1,677-entry manifest and existing tags
are unchanged. Reference software-rendered VICE checks demonstrate original-media
loading/execution and generated SID samples, not physical audio/input/graphics.
Supported no-color stdout logging avoids a reproduced VICE 3.10 logger crash; this
does not retrospectively diagnose POC1's physical failure. Exact limitations and
package/source/build identities are in the checkpoint above.

Current branches remain product feature/1.1-build-foundation and Menu
feature/1.1-debian-package. Later validation/continuity commits do not alter frozen
input identities. Final Git bundles/ref inventories and offline restore evidence:
`archive/milestone1-private-poc2-2026-09-15`; detailed evidence: `qualification/poc2`.
Independent encrypted backup remains unresolved. Existing historical/preservation/
POC1 checkpoints are untouched.

**Investigation:** the frozen image has no VICE geometry configuration/arguments;
upstream 3.10 nevertheless defaults to per-chip true aspect mode (2). Historical
v1.0 has explicit window sizes/filtering, but no explicit aspect/fullscreen setting.
Leading hypothesis: implicit windowed KMS mode selection plus downstream scaling;
actual renderer/mode/resource capture is missing. Do not claim adding mode 2 alone
fixes it. Prefer true per-chip aspect + explicit desktop-resolution fullscreen,
with bars where needed, without hard-coded 4:3 or HDMI-resolution hacks.

**Next:** owner authorization for a narrow POC3 geometry/defaults/measurement change,
new frozen candidate and offline validation, followed by owner Pi 3B geometry and
regression testing before other models. STOP pending that decision. Full settings/
privilege redesign remains deferred. Four owner-supplied photos are now retained
and visually reviewed under `qualification/poc2-pi3b-photos-2026-09-16`, with
per-file hashes/captions in the formal physical record. They corroborate visible
C64/media output and stretching; no diagnostic reports or confirmed cause. All
result classifications and frozen candidate identities remain unchanged.

This review's small evidence is under `qualification/poc2-pi3b-owner-report-2026-09-15`;
additive Git recovery/ref/offline-restore checkpoint:
`archive/poc2-pi3b-review-2026-09-15`. Earlier checkpoints retain their original
meaning. Photo-supplement source recovery: `archive/poc2-pi3b-photos-2026-09-16`.
This top section supersedes older physical-pending statements below.

## What shipped

| Item | Verified baseline |
| --- | --- |
| Product | Project CBM v1.0.0, original Trixie console appliance |
| OS/base | Raspberry Pi OS Lite 64-bit, Debian 13.4 Trixie; 2026-04-21 reference, pi-gen `4ad56cc850fa60adcc7f07dc15879bc95cc1d281`, stage2 |
| Kernels | arm64 vendor 6.12.75 v8 and 2712; no device EEPROM qualification implied |
| VICE | Source-built 3.10 SDL2 under /usr/local, direct ALSA; retained build output matches installed x64sc |
| TCPser | 1.1.6_beta, retained checkout `fe7feff4862406b277e009d14c219f5d16cf1222`; full integration unqualified |
| Menu shipped | Exact 17 scripts recovered at `a4148db54001790eaddb4e31104917c16149b181`, annotated `recovered/image-v1.0.0-runtime` in companion repo |
| Formal Menu | Existing v1.0.0 peels to `399c6158caa8ed2762744d512c1841b94ad64403`; 12 script matches, five differences, extra experimental screenshot helper |
| Source lineage | Historical v6.1/v6.3/v6.4 -> v6.5/GoldMaster/for65. v6.5 source equivalence is not byte identity or a full installed configuration snapshot |

[Provenance and hashes](docs/provenance.md) distinguish fact, inference and unknown.
No known Bookworm generation exists. No pre-existing Menu commit matches all
shipped bytes; the new root recovery commit records recovery, not invented ancestry.

## Development and maintenance

- Canonical main fast-forwarded 26 commits each: product `46fbf47` -> `493229c`;
  Menu `f185d91` -> `b7e4d85`, followed by local continuity commits. Full IDs and
  preservation records: [provenance](docs/provenance.md).
- The eight unpublished preservation/continuity commits received an owner-authorized
  metadata-only privacy repair. Current refs and verified replacement bundles are in
  [privacy reconciliation](docs/privacy-reconciliation-2026-09-15.md). Both main branches and Menu recovery/maintenance refs are published. Product
  maintenance/1.0 remains intentionally local/bundled; public product v1.0.0 is the
  authoritative maintenance baseline. GH007 rejected new branch creation because
  of historical commit email metadata; do not retry, rewrite v1.0.0 or weaken privacy.
  GitHub release assets are unchanged.
- Product maintenance/1.0 starts at immutable product v1.0.0 `46fbf47d66596b2f3d0f6ab53d26bdd90632c73c`.
  Menu maintenance/1.0 starts at the exact recovery commit above, not formal Menu
  v1.0.0. It contains scripts and provenance only, not an installable image recipe.
- 1.0.x = original Trixie generation, important/security fixes only. 1.1.x = current
  Trixie reproducible-build/modernization generation. No 1.0.1 exists or is approved.
- Work from short feature branches off main when 1.1 is authorized. Repository
  separation, immutable releases, explicit input pins and Pi 3 floor are protected.

## Qualification and known problems

Goal: Pi 3B/3A+/3B+, 4B/400, 5/500/500+ where technically supportable. Pi 3 is
the performance floor; 3A+ needs a separate 512 MiB memory qualification. The
historical audit did not qualify hardware. Exact POC1 failed x64sc/console recovery;
exact POC2 now passes bounded Pi 3B emulation/return/audio/media checks with an
aspect-ratio failure. This is not full model qualification; other models and
performance budgets remain unqualified. See [testing](docs/testing.md) and the new physical record.

Verified static/integrity checks cover image hashes, runtime extraction/lineage,
Git preservation and individual Bash syntax. They do not qualify boot, graphics,
audio, controllers, IP232, USB/NVMe or cloned identity behavior.

Known issues are cataloged in [security](docs/security.md): baked identity/SSH keys,
cloud-init and builder residue; broad sudo; TCPser default mismatch; inconsistent
Samba service policy; USB import safety; non-idempotent installer; writing docs-sync
dry run/deletion risk; version-display and CI/version mismatch; source/release
divergence; PiShrink/manual build limitations; content/license provenance gaps.
Current guidance is corrected in [v1.0 notes](docs/v1.0-current-notes.md); no runtime
fixes were applied. Historical audit/release notes/assets/checksum bytes are preserved.

## POC1 direction and next task (historical; superseded above)

Keep the console Bash/dialog -> SDL2 VICE -> ALSA appliance, with product-owned
integration and an independently versioned Menu. ADR-0001 selects writable ext4
with logical system/user-data separation, existing
content paths, external component .deb builds and backup/reflash/validated restore.
No mandated 8 GB minimum: measure footprint, initialization/maintenance margin and
free user capacity. Separate USERDATA and immutable roots are deferred.

Milestone 1 reached its first controlled-build checkpoint on
`feature/1.1-build-foundation`. The image uses integration commit
`024db4985202ef0675b12e12b8982af91c6d6ad3`; later validation/docs commits do not
change its frozen identity. Menu packaging is on `feature/1.1-debian-package` at
`77a708019c9d8a11e657d7e5d2dde7b7ecb340ba`, local annotated `v1.1.0_poc1`.
Both published main branches and existing release/recovery tags are unchanged.

Real lock: `inputs/frozen-poc1/release-lock.json` under the configured bulk root;
SHA-256 `703aa6e1b0d278262a2dc83c31740b3c589788e3953e3ac822e948133529d566`.
Private raw/XZ and records: `artifacts/private-poc1`. Raw SHA-256
`ae8d2032736e1d3ae2e49d4370aa62d00fc06f9fc567e70e400491900d45bf9f`;
XZ SHA-256 `b9adaaa55a7543441607fc90f7651cc35588f9c024e8a160110d857919ef2a06`.
26 macOS/Linux tests and 50 offline image checks passed at construction. Physical
Pi 3B boot/Menu now passed; x64sc display and console recovery failed. First-boot
expansion/identity measurements and later VICE qualification remain UNTESTED.
This is a controlled build, not reproducibility proven.

Read-only analysis found missing desktop GL runtime (v1 used the OpenGL renderer),
a direct tty service without the previous PAM/login session, and differing kernel/
Mesa stacks. SDL has a GLES fallback, so no root cause is confirmed without runtime
logs. POC1 raspi-config calls also lack an authorization path; this is a separate
setup UX gap, not a failure of intentionally masked services. The required 1.1
setup UX is offline-capable with narrowly authorized operations, not broad sudo.

Next: owner review of the bounded POC2 proposal and authorization before fixes,
engineering diagnostics, media creation or rebuilding. Do not modify frozen POC1,
restart the builder, modernize broadly or publish anything. Product remains on
feature/1.1-build-foundation; Menu working branch is feature/1.1-debian-package at
99063f8299192877f7d17d0ccd9635f135b89fdc (the frozen POC1 input stays the earlier
77a7080 commit above). This analysis changes product documentation/records only.
Both retained raw-image hashes were reverified; inspected package/launcher payloads
match the frozen image. Documentation JSON/local links/diff and immutable-tag
checks are recorded in the analysis checkpoint; no physical rerun was performed.
Private detailed comparison and additive source checkpoint are retained under
qualification/poc1-pi3b-2026-09-15 within the configured external workspace.
Earlier build/recovery checkpoints remain unchanged; no image is duplicated.

### Black-box recovery requirement

Read [recovery](docs/recovery.md) for scenarios A–H, historical confidence levels,
portable storage, independent backup/restore and acceptance tests. A future developer
must recover the product from CBM repositories/retained artifacts alone, without old
sessions, the original Mac or reference projects.

Full project recovery belongs in repositories and retained build/release infrastructure.
1.1 carries only minimal `/usr/share/project-cbm/identity.json`, generated from the
same frozen lock: product/Menu/VICE/base/TCPser mapping, integration/build ID and config
schema identity, with external provenance lookup. The generator is implemented; its 1,443-byte output is installed and verified
offline in the private POC. No full lock, recipes, schema corpus,
archives or package closure merely for recovery in the appliance. Proposed pcbm-info
reads E; it is not implemented. Final image hashes/qualification stay external to
avoid cycles. A final manifest hashing the image cannot have its digest embedded in
that image; use a predecessor digest/build-ID lookup. JSON worksheet is design-only.

The accepted preservation bundles were restored into fresh mirrors without GitHub:
all 5 product refs, 8 Menu refs and 17 recovered script hashes matched; fsck passed.
Owner accepted repository-only cold-start comprehension on 2026-09-15. Offline 1.1 identity now passes on the private image. An independent clean Linux
rebuild and independent-medium restore remain unperformed. Host-only schema/privacy negatives pass using synthetic fixtures. Read-only lessons from Spitfire/FireComm/CircuitNET are summarized in recovery.md; CBM does not depend
on them. Spitfire's migrated reference copy has missing tools.

Current local paths are deployment choices, not architecture. Independent encrypted
backup/custody, Linux bootstrap environment, signing custody and standard SBOM format
remain open. At that earlier checkpoint no infrastructure was provisioned. The earlier design checkpoint remains
separate from the sealed preservation archive. The additive privacy-reconciliation
checkpoint now retains all eight replacement commits, including the architecture
work, with full offline restore checks. See its record for subsequent checkpoint phases.

## Evidence and storage

- Original history (read-only by policy): `/Volumes/TheBench/Projects/Project CBM`.
- New bulk work: `/Volumes/TheBench/ProjectCBM-Work/{inputs,packages,builds,cache,artifacts,qualification,scratch}`.
- Durable inventory/Git snapshots/recovery: `ProjectCBM-Work/archive/preservation-2026-09-15`.
- Additive design checkpoint/bundles: `ProjectCBM-Work/archive/black-box-design-2026-09-15`.
- Original assets/extraction: `ProjectCBM-Work/archive/audit-2026-09-14/workspace`.
- [Reconciled audit](docs/audit-2026-09-15.md); original report retained externally.

TheBench is ~2 TB APFS with ~1.13 TB available at preservation time. Check actual
space/mount before work. The approved guest supplies ext4 in its external sparse disk. One device is not an
independent backup; owner review of a second encrypted backup destination remains.
Unknowns: original base-XZ identity/full input lock, complete raw-to-shrunk command
chain, VICE upstream tar provenance/patch state, content licenses and all physical
qualification. Public availability/credential remediation and any new release need
separate owner review. These do not prevent starting an explicitly authorized POC.

## Final architecture phase checkpoint (historical, pre-rewrite IDs)

Inputs: product main `7f9c4a363cf19154a9637ed8b251049bf23723e0`; Menu main
`c3746a12e6146f880c49979df8da2a3567200924`. Both began clean. Exact historical release,
Menu recovery refs and rehashed bundle locators are in [provenance](docs/provenance.md#recovery-bundle-locators-and-digests).
Research dated 2026-09-15 is cited in ADR-0001; it is not a future release input lock.
Current policy now distinguishes project recovery, minimal installed identity,
reproducible builds and disaster recovery. Roadmap and user-facing content/service/
credential/hardware guidance are reconciled; historical evidence is not rewritten.

Validation and exact commit lookup are recorded in [phase validation](docs/architecture-phase-validation.md).
No builder, Linux provisioning, packaging, runtime/first-boot change, image, push or
release. Stop after documentation commits. Independent backup/custody, Linux bootstrap,
signing custody, SBOM format, measured acceptance budgets and historical 1.0 input/
build-chain gaps remain open. Implementation is the next separately authorized task.

## Milestone 1 pre-approval checkpoint (historical)

Contract implementation commit: `e4d1556` (resolve full ID in Git); later design/handoff
commit follows on the same local feature branch. Feature work is not pushed or merged.
The 15 host-only tests passed, including published tag identities, strict JSON/schema
validation, malformed/missing pins, safe locators, minimal-identity projection and
workspace refusal cases. No physical Pi, Linux capability or real input-closure pass
is claimed. The old worksheet remains visibly historical and fails lock validation.

Current source recovery is additive under archive/milestone1-contracts-2026-09-15;
its checkpoint.json and separate SHA-256 identify the final branch tip, bundles,
validation/research/test-dependency artifacts and exact next step. Read its README
after verifying the catalog. Published synchronization bundles remain under
archive/privacy-reconciliation-2026-09-15/published, checkpoint SHA-256
`6ff18bafcc57a7e054a22fff66efedd3618ea6bd1a6f9dedf2c6d1bacdbc255c`.

Recommendation awaiting approval: Lima/VZ plain arm64 Debian VM, 8 vCPUs, 12 GiB RAM,
160 GiB sparse ext4 disk on TheBench, explicit external download/cache placement.
UTM is the main alternative. Approval must precede host installation/provisioning;
exact bootstrap/input pins and actual Linux capability tests remain future work.

## Milestone 1 approved host checkpoint (historical, before package work)

Lima 2.2.0, source `de0816ea4bdc5267b428ab21025889b8dd785526`; pinned dated
Debian cloud bootstrap and checksums in build/host/inputs.json. Instance `cbm` is
running on VZ, plain mode, no host mounts/container platform. Disk and state:
`ProjectCBM-Work/build-host/lima/cbm/disk`; cache: `ProjectCBM-Work/cache/lima`.
Actual root is ext4; Debian 13 kernel `6.12.95+deb13-cloud-arm64`. The guest is
infrastructure, not Raspberry Pi qualification or a release base image.

20 host tests passed. Full loop/partition/ext4/mount/chroot/device/xattr tests,
APT HTTPS/authenticated metadata/install/remove/source, Git acquisition and 1 MiB
bidirectional SSH/rsync hash test passed. Two probe defects (admin PATH and xattr
read permissions) were corrected; original failed logs retained. APT export excludes
transient lock/partial files after initial permission errors; important inputs were
catalogued. No host capability workaround was needed. All details and limitations:
[capability record](docs/build/lima-capability-2026-09-15.md).

Retained bootstrap inputs: `ProjectCBM-Work/inputs/build-host/`; 82-file inventory
and raw private infrastructure logs: `ProjectCBM-Work/build-host/records/`.
Next: retain and select exact pi-gen arm64/VICE/Menu/TCPser inputs and package-build
closure, then implement the smallest locked POC factory. Do not claim a frozen real
release lock, complete source/package closure, image, reproducibility or hardware pass.

## Private component packages and retention work (historical, before input freeze)

Successful private Debian candidates retained under `ProjectCBM-Work/packages/poc1/`:

- VICE `3.10-1+pcbm1`, arm64; SHA-256
  `674c40040965b689d08cdc225f8954c0fb2433ef68459f51aa7f6360b1710d20`.
- Menu `1.1.0~poc1-1+pcbm1`, all; SHA-256
  `3f7557cdbdd44922954a6e640a1bcb3a96f446f6dbe6631afe667aa5e5d5f0fd`.
  Companion feature/1.1-debian-package at `77a708019c9d8a11e657d7e5d2dde7b7ecb340ba`;
  local-only annotated v1.1.0_poc1 object `e265f3cbb995ad0a9a7748987b2d9c88019aa787`.
  Formal and forensic tags/main are unchanged. Menu packaging relocates required
  command paths to /usr/bin and excludes release-prep, screenshot and unreviewed art.
- TCPser `1.1.6~beta-1+pcbm1`, arm64; SHA-256
  `8b8f8a4f3ec98dddf5bdb347320dad05e1bbe5230e0ee2727248c247a5af584f`.

Exact source selection is in build/inputs-poc.json (NOT a frozen release lock).
pi-gen arm64 `6fcca44892d5d4b36f826d2b8fb16d716369fada` and TCPser
`fe7feff4862406b277e009d14c219f5d16cf1222` sources/bundles are externally retained.
VICE needs dos2unix, xa65, SDL2-image and evdev development dependencies; those
configure findings are now in the recipe. Out-of-tree compilation avoids source
contamination; native CPU optimization is explicitly disabled. Build logs and .dsc,
source archives, .buildinfo, .changes and debug .debs are retained outside Git.

Pinned pi-gen stages 0/1/2 completed in an input-resolution-only run with all image
exports disabled. No final appliance has been constructed. Resolved base is Trixie
13.7 with raspberrypi-sys-mods 1:20260914 and vendor kernel metapackages
1:6.18.50-1+rpt1. Actual vendor early resize hooks require the `resize` kernel argument;
first-boot draft removes that argument and coordinates one explicit growth owner.
Full source/host package retention and a frozen replay-capable input kit remain in
progress. Seventeen old bootstrap .deb versions were absent from today's indexes;
exact-version Debian snapshot recovery is underway, without upgrades/substitution.
Inspect newer dirty scripts/state and build-host/records before resuming. Next:
complete/verify retention, freeze real lock, review/test integration and first boot,
then one private image and offline validation. No publication or physical Pi test.

## Frozen factory implementation checkpoint (historical, before first image)

26 contract/retention/geometry tests pass on macOS and native Debian, with no skips.
The initial Linux test copy omitted a worksheet and Git refs; the complete copy now
passes. This was a test setup error, not a required Linux capability failure.
Exact old host binaries (17) and sources (10) were recovered via Debian snapshots.
All remaining runtime source acquisition completed, with explicit libftdi1 source-name
reconciliation. Unneeded rpi-connect-lite is excluded before construction because its
source entry was unavailable; original failed discovery records remain unchanged.

The minimal factory is in tools/{freeze_poc_inputs,retained_inputs,construct_poc,
install_poc_stage}.py and [integration notes](build/pigen/README.md). A frozen kit
contains content-addressed direct inputs and nested source/package/metadata catalogs.
Source .dsc SHA-256 payload lists and actual .deb identities are checked. Final assembly
runs with loopback-only networking and frozen APT transport; absent inputs fail closed.
Two explicit pi-gen patches exclude Connect and prevent export-time user rename/
package upgrades. They do not rewrite upstream history or bypass APT authentication.

Private POC policy: local pi console Menu, locked passwords, no broad sudo, no baked
credentials; SSH/Samba/TCPser/Avahi/NetworkManager disabled. Binaries are installed,
but network configuration and privileged Menu controls remain incomplete. No cover
art/private historical content is imported. First boot owns root growth and seeds
user state; pure geometry tests pass, actual first boot remains physically untested.
Next: commit this input recipe, archive that commit, freeze/verify/export the real kit,
construct one private image, validate offline, retain results and STOP for owner review.

## Final POC1 recovery checkpoint (historical)

`ProjectCBM-Work/archive/milestone1-private-poc1-2026-09-15` is the additive current
checkpoint: README, checkpoint.json plus SHA-256, both full Git bundles/ref lists,
offline mirror restoration/fsck results and validation/remote-ref records. Its exact
final branch tips are recorded externally to avoid a self-referential commit hash.
The frozen kit has 2,697 rehashed objects; images and component artifacts remain in
their existing external locations, without duplicating historical images.

Original historical manifest verifies all 1,677 entries unchanged. Both formal v1.0.0
tags, Menu recovery refs and published main refs are unchanged. Product maintenance/1.0
remains local/bundled. Independent encrypted custody remains unresolved; a second
folder on TheBench is not an independent backup. Current VM is stopped, not deleted.
