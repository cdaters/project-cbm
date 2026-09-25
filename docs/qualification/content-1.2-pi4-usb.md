# Pi 4 B — private 1.2 USB/content qualification

**September 25 physical update:** B1 on exact private attempt18 is **FAIL**:
USB MC keyboard navigation fails while ordinary FILES MC works. See the
[owner report and read-only investigation](attempt18-pi4-usb-b1-investigation.md).
Stop B1 for evidence collection; do not repair the qualification image in place.
The procedure below is retained as the original test expectation.

**NON-RELEASE. Physical results: UNTESTED.** Do not flash until the
[candidate record](../build/private-1.2-development.md) supplies a completed image,
exact raw/XZ hashes, validation and verified recovery. Source tests alone are not an
image. Use a separate microSD card; retain the stable 1.1 card and all user backups.
This procedure qualifies the tested Pi 4 B and these workflows, not other models
or a public 1.2 release. Flashing/testing remains an explicit owner action.

## Prepared attempt18 basis — 2026-09-25

Image preparation is complete: [exact output record](../build/private-1.2-dev1-attempt18.json).
This is owner-controlled testing on a separate card, not a public release or a physical
PASS. Verify external recovery at `archive/private-1.2-dev1-attempt18-2026-09-25-r2`.

- Build ID: `4d8bfbea304b5505b51f4fc4fab8cbf66541bea70fdc8a54f1f1287675863a79`.
- Raw: `2026-09-25-project-cbm-1.2.0-dev.1-lite-private-1.2-dev1.img`,
  3,095,396,352 bytes; SHA-256 `428da6e67c5f82aa3a09fdbdc54d12e0d6cf8fc78abd0bc25a779c728351e557`.
- XZ: `image_2026-09-25-project-cbm-1.2.0-dev.1-lite-private-1.2-dev1.img.xz`,
  598,567,740 bytes; SHA-256 `74f1b438301a491f21149acfce2e4280e232aa8707fb50a1e03b02e26b9f7010`.
- Both files: `artifacts/private-1.2-dev1-attempt-18` under registered bulk storage.

All procedure cases below remain **UNTESTED** until exact-image owner reports arrive.

## Record the basis

Record date, Pi model/RAM, power supply, keyboard/display, card size, selected image
filename and SHA-256, installed product/build ID, Runtime/Menu package versions,
USB make/capacity/filesystem and partition count. Keep serial numbers and network
details private. Verify the chosen image before flashing with `shasum -a 256` on
macOS or `sha256sum` on Linux; compare the exact artifact hash, not its filename.
Complete first boot on the spare card. Check CONTROL → About and System Information.
From CONTROL → Advanced → Terminal, these read-only checks establish installed state:

```sh
pcbm-info --json
dpkg-query -W project-cbm-runtime project-cbm-menu
cat /etc/pcbm/engineering-poc
```

Expected initial identity: `1.2.0-dev.1`, `private-engineering-1.2-dev1`;
Runtime `1.2.0~dev1-1`, Menu `1.2.0~dev1-1+pcbm1`. Compare the build ID against the
completed candidate record. A mismatch is BLOCKED; do not test a different image
under this procedure's identity. No sudo, SSH enablement or network is needed below.

## Prepare original test media

Use a known-good **exFAT** USB drive with enough free space. Do not format, repartition
or erase an existing drive for this test. Prefer a spare with only the fixture;
on a drive with unrelated files, preserve them and record additional scan counts.
The whole source must stay below the existing 2 GiB / 10,000-entry / depth-12 limits.
If that is not possible, use another suitable drive; do not delete personal data.

The repository helper generates original BASIC PRGs and D64s without downloads:

```sh
python3 qualification/usb-1.2/prepare.py "$CBM_NEW_FIXTURE_DIRECTORY"
```

Choose a new directory on the registered external workspace. The helper refuses an
existing output. Copy **only the contents of `usb-root`** onto the USB root, including
the synthetic hidden metadata. Refuse an existing `CBM12-USB-QUAL` or `Variants`
directory rather than merging with unknown content. Retain `manifest.json` and
LICENSE off the USB. Eject it normally from the preparation computer.

The prepared fixture has 35 files: 30 supported files, two unsupported files and
three ignored metadata entries (one entry is a directory containing a marker).
There are no third-party titles. `Variants/CBM12-USB-QUAL` has the same four selected
relative names as the main collection; only `Set/disk1.d64` has different bytes.
The two fixture disks form a synthetic collection, not a claim about a commercial
multi-disk loader. Do not use these tests to establish compatibility of every format.

| Scan scope | Supported | Unsupported | Metadata entries/folders |
| --- | ---: | ---: | ---: |
| Whole partition, fixture alone | 30 | 2 | 3 |
| `CBM12-USB-QUAL` | 26 | 2 | 3 |
| `CBM12-USB-QUAL/Set` | 2 | 0 | 0 |
| `Variants/CBM12-USB-QUAL` | 4 | 0 | 0 |

Host-added metadata can increase the ignored count. Explain any difference using
the USB listing; an unexplained supported/unsupported discrepancy is FAIL.

## U1 — Baseline and real device detection

1. Without USB connected, open CONTENT → Import from USB. Expect no eligible source,
   then return to Menu. CONTENT offers Browse Library, Import from USB and real Help;
   no visible top-level IMPORT, Online Library or Recent Additions placeholder.
2. Connect the exFAT drive. Repeat Import. Identify the actual partition by label,
   size and filesystem. The system SD card must not be offered. If using multiple
   drives/partitions, record all eligible entries and deliberately choose the fixture
   partition. Do not create partitions to obtain this optional extra coverage.
3. Read CONTENT → Help, including supported formats, uncertain machine/category,
   scanning versus Import, read-only source and safe-removal guidance.

For scan/cancel evidence, use the local second console **Ctrl+Alt+F2**, returning to
Menu with **Ctrl+Alt+F1**. First create a new private evidence directory:

```sh
umask 077
mkdir /home/pcbm/usb-qual-dev1
find /home/pcbm/content -xdev -printf '%y %P\n' | LC_ALL=C sort > /home/pcbm/usb-qual-dev1/before-tree.txt
find /home/pcbm/content -xdev -type f -exec sha256sum -- {} + | LC_ALL=C sort > /home/pcbm/usb-qual-dev1/before-bytes.txt
```

If the evidence directory already exists, retain it and use a fresh named run directory
consistently in all commands. These snapshots read the small fresh-image library,
including hidden files; they do not change it. Do not launch content or run another
writer between snapshots. Abort the test if either find/hash command reports an error.
Library listings may contain private filenames; retain them privately.

## U2 — Whole-partition discovery and cancellation

1. Select the real partition, leave source scope at **Whole partition**, and choose
   **Scan this source**. Record elapsed scan time and counts from the table.
2. Preview both pages using **More files / Previous files**. Check that filenames,
   format/size and Unknown / Unclassified information are legible. Unsupported and
   metadata entries must be counted and absent from the selectable file list.
3. Before Import, switch to tty2 and repeat the two snapshot commands with output
   names `scan-tree.txt` / `scan-bytes.txt`. Run:

```sh
cmp /home/pcbm/usb-qual-dev1/before-tree.txt /home/pcbm/usb-qual-dev1/scan-tree.txt
cmp /home/pcbm/usb-qual-dev1/before-bytes.txt /home/pcbm/usb-qual-dev1/scan-bytes.txt
```

   Both must return zero with no output: no new payload, directory or temporary file,
   and unchanged existing bytes. A preview count alone is not proof of no copying.
4. Return to tty1 within five minutes and cancel/back out before Import. Expect
   confirmed release and **USB released; safe to remove.** Verify in tty2:

```sh
findmnt --mountpoint /run/project-cbm/import/source
```

   Expect no mount row (exit 1 means no match). Compare fresh `cancel-*` snapshots
   against `before-*` as above. No content may have been copied. Remove/reconnect
   only after release confirmation, then start a fresh session. If release is not
   confirmed, leave the drive connected and follow the failure rule below.

## U3 — Folder scan, all/individual/folder selection, deselection and review

1. Choose source folder `CBM12-USB-QUAL`, then **Scan this source**. Expect 26/2/3
   rather than the whole-partition 30 supported files. `Variants` must be excluded.
2. Open `Single/hello.PRG`, **Select this file**: selected count 1. Open
   `Set/disk1.d64`, **Select this folder and descendants**: count 3; both disks selected.
3. Choose **Select all supported files**: count 26. Open `Skip/unwanted.prg`,
   **Deselect this file**: count 25. Open a `Pages/pageNN.prg`, **Deselect this folder
   and descendants**: count 4. This also exercises page navigation and folder scope.
4. **Clear selection**: count 0 and no Import action. Re-select `Single/hello.PRG`,
   folder `Set`, and `Nested/Child/nested.prg`: count 4. Confirm `Skip` and `Pages`
   are unselected. No filename-based game/machine claim should appear.
5. **Review destination → Programs — Unclassified → C64**. C64 is deliberate here:
   these fixtures were authored as C64 BASIC. Review must show four files and
   `programs/c64/Imported/CBM12-USB-QUAL`, Already Present 0, and no Keep Both yet.
   Use Back once, verify selection survives, then review again.
6. At the final review, take `review-*` snapshots and compare with `before-*`.
   They must still match. Choose **Import selected files** only after this check.

## U4 — Explicit import, hierarchy and release

Expect Saved 4, Already Present 0, not completed 0, then confirmed safe removal.
Verify no mount row at `/run/project-cbm/import/source`. In CONTENT → Browse Library
and FILES → Library confirm exactly this new collection:

```text
programs/c64/Imported/CBM12-USB-QUAL/
  Single/hello.PRG
  Nested/Child/nested.prg
  Set/disk1.d64
  Set/disk2.d64
```

No extra `CBM12-USB-QUAL/CBM12-USB-QUAL` nesting, `Skip`, `Pages`, unsupported files,
metadata, JSON bookkeeping or `.pcbm-ingest-*` temporary files belong there.
The private journal is under `/home/pcbm/.local/state/project-cbm/ingestion`, outside
normal content; inspect only this fixture's records when collecting diagnostics.
Hash the four destination files and compare with their matching paths in the host
fixture manifest. Read-only source access and successful release must be truthful.

## U5 — Identical duplicates and conflicting collection

1. Reconnect if removed. Repeat the **same folder, same four selections and same
   Programs/C64 destination**. Review: Already Present 4, new bytes 0. Explicit Import:
   Saved 0, Already Present 4, release confirmed. No numbered sibling or extra copies.
2. Start again; choose `Variants/CBM12-USB-QUAL`, scan and select all four. Choose
   Programs/C64. Review must say **Keep Both** and show
   `programs/c64/Imported/CBM12-USB-QUAL (2)`. Import saves the complete selected set.
3. Confirm both directories contain the four paths above. Original disk1 retains
   version-one hash; sibling disk1 matches variant hash. Disk2 and the PRGs match
   their original hashes in both directories. Never mix just a replacement disk1
   into the original set. No existing file is overwritten.
4. On the Pi, `stat -c '%i %h %n'` on each collection's `Set/disk2.d64` must show
   different inode numbers and link count 1. Do not modify a disk to test this.
5. Repeat the variant import: Already Present 4 in the same `(2)` sibling, no `(3)`.
   Confirm automatic release after each attempt.

## U6 — Whole-partition Select All import

Scan the whole partition again. **Select all supported files**, then deliberately
choose **Programs — Unclassified → Shared** and review. Shared is an explicit test
destination, not a machine inference. Import the 30 supported files. Expected root:
`programs/shared/Imported/USB Import`, with both `CBM12-USB-QUAL/...` and
`Variants/CBM12-USB-QUAL/...` retained. All nested groups and both disks remain intact;
the unsupported files and three metadata entries are absent. Matching bytes already
in another destination do not erase meaningful source structure. Confirm release.

## B1 — FILES read-only browsing and safe unmount

1. FILES → USB Drive → select the actual partition → **Mount Read-Only**.
   Midnight Commander must show USB on the left and the local library on the right.
   Browse into `CBM12-USB-QUAL/Set`, open the directory listing, then navigate back.
2. With the **left USB panel active**, press **F7** and attempt to create the new
   fixture-only directory `CBM12-WRITE-MUST-FAIL`. It must fail as read-only. Do not
   rename/delete/edit an existing file. Unexpected success is FAIL; retain the marker
   as evidence, stop this case, and leave existing user files untouched.
3. In tty2, `findmnt --mountpoint /run/project-cbm/import/browse` must show exFAT and
   `ro,nodev,nosuid,noexec`. The Import mountpoint must not be mounted. Return to tty1.
4. **F10** exits MC to **USB Drive — mounted read-only**; it must not claim safe
   removal yet. Choose **Browse Read-Only again**, exit F10, then **Safe Unmount**.
   Require confirmed safe-removal text and no browse mount row. Remove/reconnect and
   repeat once to catch stale-session confusion. Back from the mounted menu also
   attempts release; test once and require the same confirmation.

## B2 — Bounded busy/unmount failure (fixture drive only)

This uses a process working directory to hold the read-only mount busy; it neither
writes to USB nor removes it while mounted. Use the local tty2 console, no new SSH
exposure. If a second console is unavailable, record **UNTESTED** with reason.

1. Start B1 and leave MC open. Switch to tty2 and run as ordinary `pcbm`:

```sh
python3 -c 'import os,time; assert os.geteuid()==1000; os.chdir("/run/project-cbm/import/browse"); print("Holding test mount for 120 seconds",flush=True); time.sleep(120)'
```

2. Return to tty1 promptly. F10, then Safe Unmount **within 60 seconds**. Expected:
   busy/could-not-release failure and **Drive release was not confirmed. Leave it
   connected until a safe shutdown.** No safe-removal assertion. The mount remains;
   already saved library content remains intact. Record actual wording and timings.
3. After the helper exits on its own, return to Menu and perform normal shutdown,
   leaving USB connected until fully powered down. This workflow does not promise
   an in-session retry after a failed broker cleanup. Do not use forced/lazy unmount,
   kill another user's process or unplug to clear the failure.
4. Power on with USB connected; no stale browse/import mount should be present.
   A fresh FILES session must detect it, browse read-only and unmount successfully.
   If the helper expired before Safe Unmount, the case is inconclusive, not PASS;
   repeat only from a fresh confirmed session.

## R1 — Local content, RUN, persistence and appliance lifecycle

Before USB tests and again after them:

1. CONTENT → Browse Library must list the existing local content. Launch the
   image's original `pcbm-smoke.prg` qualification program through Programs; record
   actual visible output. Test one previously working, permitted local C64 title
   if available, without adding it to the image or distributing it.
2. **F10 → Quit emulator → confirm** returns to responsive Menu. RUN → C64 starts
   normal x64sc/BASIC with the expected Cover. Repeat F10/Quit/Menu twice.
3. Launch imported `Single/hello.PRG`: expected `CBM USB HELLO`; return via F10/Quit.
   Browse both new multi-disk directories and confirm both files are available.
4. With sessions cleanly released, choose normal **Reboot**. Setup must not repeat;
   saved files/hashes, local browsing and normal launch must persist. No USB session
   automatically remounts. Reconnect and complete one fresh read-only session.
5. Choose normal **Shutdown**, wait for completed power-off before disconnecting
   USB/power. The busy case's shutdown does not replace this normal-clean-session check.

## T1 — Pi 4 responsiveness and reporting

Record seconds for device list, whole scan (30 files), folder scan (26), preview
page change, file selection, destination plan, copy, MC entry/exit and safe unmount.
Repeat the small UI actions three times and report their range, not an invented
average or a faster host result. Record missed keys, redraw/flicker, blocked Cancel,
or any delay without useful feedback. Existing sessions have a five-minute idle
and thirty-minute total limit; restart instead of treating an expired review as a
fresh session. These small fixtures establish a bounded baseline, not a large-library
performance claim. Unexpected hangs or input loss are FAIL; stop and retain evidence.

Use PASS / FAIL / UNTESTED / BLOCKED for each of U1–U6, B1, B2, R1 and T1. Report
scan/selection/result counts, snapshot comparisons, copied hashes, source manifest
agreement, removal wording and timings against the exact image/build ID. After
confirmed unmount, check fixture files on the preparation computer against the retained
manifest; ignore unrelated host-created metadata and never normalize owner files.

On a core boot/input/launch regression, unexpected source write, wrong-destination
write or false safe-removal assertion: stop the affected test, preserve the visible
message and allowlisted diagnostics, and report. Do not patch the qualification
image in place. Do not test low-space exhaustion, forced media removal, filesystem
corruption or destructive errors on owner media. Their automated coverage remains
separate. Assembly64 access is unrelated to readiness for these USB tests.

After reporting, **STOP for review**. No release/support claim follows automatically.
