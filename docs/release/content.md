# Content library and USB import

This page describes **Project CBM 1.2.0**. For 1.1.0 behavior, use the manual at its preserved release tag.

**CONTENT** offers Browse Library, Import from USB, Online Library and Help.
[Search Assembly64](online-library.md) or follow the USB steps below.

[Documentation index](../README.md) · [User Manual](user-guide.md)

Your library is **/home/pcbm/content**. You do not need to type that Linux path when
using File Sharing: the **Project CBM** share opens directly into it. SFTP starts in
`/home/pcbm`, where you open the `content` folder. Files elsewhere in your home are
personal files but are not automatically listed by CONTENT.

## Where files belong

Project CBM sorts first by purpose, then by machine. Use any useful subfolders below
that level: a game title, publisher or collection works well. You do not need separate
`disk`, `tape`, `cart` or `prg` folders; the file extension already describes its format.

| Your file | Example location under `/home/pcbm/content` | How to find it |
| --- | --- | --- |
| C64 disk game | `games/c64/My Game.d64` | CONTENT → Browse Library → GAMES → `c64/My Game.d64` |
| C64 PRG demo | `demos/c64/My Demo.prg` | CONTENT → Browse Library → DEMOS → that path |
| VIC-20 program | `programs/vic20/My Program.prg` | CONTENT → Browse Library → PROGRAMS → that path |
| C128 software | `programs/c128/My Program.d71` | CONTENT → Browse Library → PROGRAMS; uses a C128 profile |
| C128 80-column software | `programs/c128/80col/My Program.d81` | That extra `80col` folder selects the VDC profile |
| SID music file | `music/c64/My Tune.sid` | Stored/listed, but generic SID playback is not available |
| Legally supplied ROM resource | `roms/c64/My Resource.rom` | Configure it in VICE; not a generic autostart file |
| Unclassified disk | `games/shared/Unknown.d64` | Uses RUN's default; choose the correct computer first |

Example names describe your own content, not bundled games or a redistribution grant.

```text
/home/pcbm/content/
  games/c64/My Game.d64
  demos/c64/My Demo.prg
  demos/c64/Imported/My USB Folder/My Demo.prg
  programs/vic20/My Program.prg
  programs/c128/80col/My Program.d81
  music/c64/Creation/SID-Wizard/SID-Wizard-1.97.d64
  music/c64/Imported/My Tune.sid
  roms/c64/My Resource.rom
  screenshots/
  saves/
```

Games, Demos and Programs initially have `c64`, `c128`, `vic20`, `plus4`, `pet`,
`cbm2`, `cbm5x0` and `shared` folders. Music initially has `c64`, `c128`, `vic20`,
`plus4` and `shared`. PET/CBM-II programs that make sound can live in Programs.
ROM resources have the seven machine families, without Shared. Screenshots and Saves
are useful storage folders; CONTENT does not list them as separate categories or
promise every application saves there automatically.

**Shared means unclassified or deliberately shared material**, not universal machine
compatibility. An extension cannot tell C64 and VIC-20 PRGs apart. Recognized machine
folders choose a matching profile without changing RUN. If RUN already uses a variant
within that family, it stays the preferred variant, except the explicit C128 `80col`
folder and the two recognized C64 application disks. Older files directly beneath a
category remain browsable and use RUN's default.

## Launching files

CONTENT → Browse Library scans each category recursively and shows relative filenames. A leading dot
in a legitimate file or folder name does not hide supported content; known host
metadata remains excluded. There is no
intermediate machine picker. Select `c64/My Game.d64` from GAMES to launch it with a
C64 profile. The shared launcher passes ordinary media to VICE's autostart facility.
Whether it starts correctly depends on the program, selected machine, drive and memory
configuration. For multi-disk software, use VICE's F10 media controls to change disks.

| Format group | CONTENT lists | USB imports | Automatic-launch limits |
| --- | --- | --- | --- |
| Programs | `.prg`, `.p00` | Yes | Must target the selected computer and required RAM |
| Tapes | `.tap`, `.t64` | Yes | Requires compatible machine/tape support |
| Disks | `.d64`, `.d67`, `.d71`, `.d80`, `.d81`, `.d82`, `.g64`, `.g41`, `.x64`, `.p64` | Yes | Drive type and software matter; attach manually in VICE when necessary |
| G71 disk | Listed | `.g71` is imported | C64/C128 profiles; Project CBM selects a 1571 drive for this launch |
| Cartridges | `.crt` | Yes | Only where the selected VICE machine can handle that cartridge |
| Music | `.sid`, `.mus` | Yes | SID is explicitly refused by the generic launcher; MUS recognition is not a promised music-player workflow |
| Resources | `.bin`, `.rom`, `.reu` are outside generic content import | No | Store using FILES or file sharing and configure deliberately in VICE |

Raw `.bin` can represent ROM or firmware data. Project CBM has no guided ROM-management
workflow; ROM type, target machine, expected size and VICE settings require separate
care. FILES can copy a file without making it an importable or runnable program.

Do not rename a file's extension to force compatibility. ROMs and memory resources
require deliberate VICE settings. PSID/RSID playback has not been integrated into the
normal Menu. SID-Wizard is a music editor launched from its D64, not a SID player.

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


## FILES → USB Drive

Choose a partition, then **Mount Read-Only**. Midnight Commander shows the USB source
and your local library. Press **F10** to exit; choose **Safe Unmount**, **Browse
Read-Only again**, or Help. Back also attempts release. Remove the drive only after
confirmation. If it is busy or release is unknown, leave it connected until safe
shutdown. Reboot does not remount the session.

USB rename/delete/write operations are refused. Midnight Commander runs as your
normal user; any manual copy into the library uses its own overwrite prompts and
does not use guided Import history. Use CONTENT → Import from USB for reviewed
selection, duplicate handling and recorded results. The browser is not an execution
sandbox: do not manually execute content you do not trust.

One CBM USB session is active at a time, with a thirty-minute total limit and a
five-minute idle review timeout. Close other sessions before choosing another
partition. Source removal or browser failure ends the session and attempts cleanup;
missing confirmation always requires conservative removal.

## Host metadata and counts

Operating systems create housekeeping files on removable drives. Import ignores these
exact names: `.DS_Store`, `.Spotlight-V100`, `.Trashes`, `.fseventsd`, `.TemporaryItems`,
`.VolumeIcon.icns`, `.AppleDouble`, `System Volume Information`, `$RECYCLE.BIN`, and
names starting `._` (AppleDouble companions). Matching folders are not traversed.
Other hidden files are not broadly discarded if they are supported media.

Results distinguish copied content, skipped existing/unsupported entries, and ignored
metadata entries or subtrees. A skipped metadata directory counts as one ignored
entry, not every file hidden inside it. Previously imported metadata is not deleted
from your library. CONTENT has its own display filter; FILES can show files that
CONTENT does not list. See [troubleshooting](troubleshooting.md#content-and-usb).

For transfer from another computer, use [File Sharing](networking.md#file-sharing).
For protection before reorganizing, follow [backup and recovery](recovery.md).
