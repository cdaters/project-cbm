# Content workflows in provisional 1.2.0 development

These features are development source, not a released or Pi-qualified image.
Project CBM **1.1.0 remains the stable release**. Its [content manual](../release/content.md)
describes the released behavior. This guide describes the new Menu/runtime pair.

## CONTENT

- **Browse Library** opens the existing local category browser and launch routing.
- **Import from USB** scans, previews and imports your selected content.
- **Help** explains scanning, formats, classification, duplicates and safe removal.

Online Library and Recent Additions are omitted until their implementations are
ready. Existing saved files remain usable offline. There is one normal visible
Import path, under CONTENT; the internal `pcbm-import` command remains available.

## Import from USB

1. Connect a FAT, exFAT or ext4 USB drive and choose **CONTENT → Import from USB**.
2. Choose a partition. Mounted disks and the running system disk are excluded.
3. Choose a folder or **Scan this source** for the whole partition. The source
   remains read-only. **Scanning does not copy anything.**
4. Review supported, unsupported, metadata and unreadable-folder counts. Use
   **Select all**, individual file actions or **Select this folder and descendants**.
   Deselect unwanted files or clear the selection. Pages contain up to 20 entries.
5. Choose **Review destination**. Select the category and machine explicitly.
   If unsure, use **Programs — Unclassified** and **Shared**. These are unsorted
   destinations, not a claim that every machine can run the content.
6. Review the selected count, new byte estimate, Already Present count and library
   destination. Choose **Import selected files** to copy, or return to selection.
7. Read the result. Completed files remain available even if a later file fails
   or you cancel. Remove the drive only when its release is confirmed.

During a longer scan, plan or import you can cancel. Back before Import never copies
payloads. An idle review session expires after five minutes, and a complete session
is bounded to thirty minutes. Start again to rescan after expiry. Leave USB connected
if release is unknown or busy; shut down safely before removing it.

Files go into `/home/pcbm/content/<category>/<machine>/Imported/<collection>`.
The selected source folder supplies its collection name; whole-partition scans use
`USB Import`. Relative folders stay together. Nothing is flattened or migrated.

Identical bytes at the same destination are **Already Present**. Different bytes
use **Keep Both**, placing the selected collection in a numbered sibling directory.
Include every disk you need when selecting a multi-disk title. Mutable disk images
remain independent files; changing one does not change another copy.

One scan/import is limited to 2 GiB, depth 12 and 10,000 encountered entries; the
library retains at least 256 MiB of free-space margin. Choose a smaller source
folder when a limit is reached. A limited scan does not offer incomplete results
as though it had scanned everything.

## Formats and uncertain classification

Supported formats, case-insensitively: PRG/P00 programs; T64/TAP tapes;
D64/D67/D71/D80/D81/D82/G64/G71/G41/X64/P64 disk images; CRT cartridges;
SID/MUS music. Format recognition does not guarantee compatibility or playback.
ROM/BIN/REU resources and archives are outside bulk import.

A `.prg` does not establish game, demo, application or machine. Discovery displays
Unknown/Unclassified and uses your explicit category/machine choice. No filename
classification, AI classification, archive extraction or automatic launch occurs.
Known host metadata is ignored; ordinary dot-prefixed content remains eligible.
Symlinks and special files are excluded. Unreadable ext4 folders remain unreadable;
Project CBM does not copy content as root to bypass their permissions.

## Development validation

The [runtime contract](../runtime/ingestion-contract.md) describes IPC, safeguards,
provenance, checks and the bounded physical procedure. Runtime source package version
is `1.2.0~dev1-1`; Menu source version is `1.2.0_dev1` / `1.2.0~dev1-1+pcbm1`.
No package/image/tag/release exists for these changes. Native and physical results
must be reported separately from host fixtures.

## FILES → USB Drive

Choose a partition, then **Mount Read-Only**. Midnight Commander shows the USB source
and your local library. Press **F10** to exit; choose **Safe Unmount**, **Browse
Read-Only again**, or Help. Back also attempts release. Remove the drive only after
confirmation. If it is busy or release is unknown, leave it connected until safe
shutdown. Reboot does not remount the session.

USB rename/delete/write operations are refused. Midnight Commander runs as your
normal user; any manual copy into the library uses its own overwrite prompts and
does not receive ingestion history. Use CONTENT → Import from USB for reviewed
selection, duplicate handling and provenance. The browser is not an execution
sandbox: do not manually execute content you do not trust.

One CBM USB session is active at a time, with a thirty-minute total limit and a
five-minute idle review timeout. Close other sessions before choosing another
partition. Source removal or browser failure ends the session and attempts cleanup;
missing confirmation always requires conservative removal.
