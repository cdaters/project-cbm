# Attempt19 Pi 4 B: owner-confirmed USB fix and copy/launch lifecycle

Recorded September 25, 2026 (America/Phoenix); the test date was not separately
supplied. **PRIVATE NON-RELEASE; partial physical qualification.**
[Structured owner attestation](attempt19-pi4-owner-pass-2026-09-25.json) records the
reported results without expanding them into unreported test cases.

## Exact candidate and evidence basis

Project CBM `1.2.0-dev.2`, `private-engineering-1.2-dev2`, attempt19, Raspberry Pi 4 B.
The owner identifies this exact candidate. Hashes are taken from the retained
[candidate record](../build/private-1.2-dev2-attempt19.json):

- Raw SHA-256: `f69fbee34448936d9df942ab0c8ce990b9ccd3a85e66b95d232f0d7c8caa8d44`.
- XZ SHA-256: `00e88150f5d2105f89182e14e14ed27517a672cb57c6134598dcfa451dfe0fca`.
- Lock/build ID: `1b69db05988dc3435b3460eb045a91c7dcca4fcfe7a7d8b3eebb846e2c2d37ce`.

This update records an owner report. No new agent live-device inspection, running-card
hash, key injection or mount inspection is claimed. RAM/revision, USB filesystem,
demo identity/format/hash, timings and screenshots were not supplied in this report.

## Confirmed PASS

| Case | Owner-confirmed physical result |
| --- | --- |
| B0 | Ordinary FILES → Midnight Commander navigation works. |
| B1 | FILES → USB Drive → Mount Read-Only, USB MC keyboard navigation, copy from USB into Project CBM content, and safe unmount/release work. |
| Copy/launch/return | Copy → safe release → C64 launch → copied demo runs → F10/emulator exit → responsive Project CBM Menu. |

**The attempt18 USB MC terminal defect is physically confirmed fixed in attempt19.**
Attempt18 remains B1 FAIL with its original image, logs and historical records intact.
B0/B1 PASS applies to the reported observations; it does not attest every individual
key, optional diagnostic or fault-injection substep in the longer procedures.

## Remaining physical qualification

The [attempt19 procedure](attempt19-pi4-usb.md) supplies the current image identity.
U1–U6/R1/T1 and the original busy B2 steps are defined in the
[USB/content procedure](content-1.2-pi4-usb.md). Its attempt18 identity/results remain
historical; use attempt19's identity and a fresh evidence directory for further tests.

| Case | Status | Still to demonstrate on attempt19 |
| --- | --- | --- |
| U1 | UNTESTED | CONTENT Import no-device state, correct partition selection/system-SD exclusion, UI/help; multiple partitions if available. FILES detection alone does not establish the Import path. |
| U2 | UNTESTED | Whole-partition counts, preview paging/filtering, snapshots proving scan makes no copies, cancellation and verified Import release. |
| U3 | UNTESTED | Folder scope/counts, select/deselect/clear, retained selection through Back, destination review and no writes before explicit Import. |
| U4 | UNTESTED | Explicit CONTENT Import four-file results, exact hierarchy, exclusions/journal/temp-file checks, matching hashes and Import release. Manual MC copy is a different path. |
| U5 | UNTESTED | Already Present, Keep Both for a complete conflicting collection, unchanged originals, independent inodes and repeat handling. |
| U6 | UNTESTED | Whole-partition Select All of 30 supported fixture files into Shared; hierarchy/exclusions and release. |
| B2 | UNTESTED | Busy release fails truthfully within the bound, safe shutdown/restart and fresh-session recovery. Attempt19's additional cancellation/disconnect/crash cases are also physically untested. |
| R1 | UNTESTED as a complete case | Local library/original smoke checks before and after; Cover/BASIC and repeated exits; imported hello/multi-disk fixture; reboot/file-hash persistence, no stale remount, fresh USB session and normal clean shutdown. The reported C64/demo/F10/responsive-Menu subset is PASS. |
| T1 | UNTESTED | Actual timings and three-repeat ranges for listing/scanning/paging/selection/planning/copy/MC/release; redraw, cancellation and feedback observations. Qualitative responsive Menu is PASS, not a timing result. |

Also unreported within the detailed B0/B1 procedure: individual Up/Down/Tab/F3/F9/MC-F10
checks, literal Ctrl+C, repeated browse/reconnect cycles, Back release, deliberate
write-refusal test, observed mount flags and process/terminal ownership, and post-release
mount/orphan inspection. Keep those substeps UNTESTED without withholding the owner's
bounded B0/B1 PASS. Source fixture hashes after removal also remain unreported.
Native tests retain their native PASS; they do not fill these physical evidence gaps.

## Preservation and next action

Attempt19 artifacts, frozen inputs, packages and build-time validation record remain
unchanged. Its original physical UNTESTED statement describes build time; this additive
report supplies the later partial physical result. Stable 1.1.0 remains unchanged.
No release, screenshot or Online Library implementation begins from this report.

Evidence: `qualification/attempt19-pi4-owner-pass-2026-09-25` under registered bulk
storage. Additive recovery: `archive/attempt19-pi4-owner-pass-2026-09-25`, with exact
refs/bundles, offline restore/peeled-tag/fsck and manifest verification. This is
same-volume recovery; independent encrypted custody remains outstanding.

Await further owner results. Continue only desired remaining cases on this exact
candidate; stop any failing case for evidence and do not repair the image in place.
