# Content library and USB import

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
| C64 disk game | `games/c64/My Game.d64` | CONTENT → GAMES → `c64/My Game.d64` |
| C64 PRG demo | `demos/c64/My Demo.prg` | CONTENT → DEMOS → that path |
| VIC-20 program | `programs/vic20/My Program.prg` | CONTENT → PROGRAMS → that path |
| C128 software | `programs/c128/My Program.d71` | CONTENT → PROGRAMS; uses a C128 profile |
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

CONTENT scans each category recursively and shows relative filenames. A leading dot
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
| Resources | `.bin`, `.rom`, `.reu` | No | Browse/store, then configure in VICE; not automatic programs |

Do not rename a file's extension to force compatibility. ROMs and memory resources
require deliberate VICE settings. PSID/RSID playback has not been integrated into the
normal Menu. SID-Wizard is a music editor launched from its D64, not a SID player.

## USB import

1. Put the desired files on a USB drive. FAT, exFAT and ext4 partitions are recognized.
   Keep a backup; Project CBM imports supported regular files, not every kind of file.
2. Insert it, then select **IMPORT** (or FILES → USB).
3. Choose the source partition from **Import from USB**. If absent, return and reopen
   IMPORT after insertion. Already mounted partitions and the running system disk
   are intentionally excluded.
4. Choose the **Content machine**, or Shared for an unclassified collection.
5. Choose Programs, Games, Demos or Music. Selecting the category starts the copy;
   there is no separate per-file selection screen. All eligible files in that partition
   are considered, keeping their subfolders.
6. Leave the drive connected while the working screen is shown. Read **Import complete**
   or **Import incomplete**, including its drive-release message.
7. Remove the drive only after release is confirmed. If release is uncertain or failed,
   leave it connected and shut down safely before removal.
8. Open CONTENT → your category. Files are under `<machine>/Imported/...`.

For example, three D64s inside `My Game` imported as C64 Games go to
`/home/pcbm/content/games/c64/Imported/My Game/`. A fresh destination should report
three content files copied. Repeating it preserves existing files and copies none
of those three again. Same-name destinations are skipped, not compared/replaced;
rename or organize a newer version deliberately with FILES.

The source is mounted read-only. FAT/exFAT permissions allow copying as pcbm; ext4
journal replay is disabled. Import skips symlinks/special files and unsupported file
types. One operation is limited to 2 GiB and keeps 256 MiB free at the destination.
A failure can leave already copied files in place. Read the persistent error before
retrying; do not assume a partly completed transfer copied everything.

SID files always route to `music/c64/Imported`, even when another destination category
or machine was selected. Other files use the selected destination. To transfer a
library already arranged as `games/c64`, use File Sharing; import would preserve that
whole source tree beneath the selected Imported folder rather than flattening it.

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
