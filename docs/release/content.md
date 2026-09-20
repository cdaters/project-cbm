# Content library, media and migration

The Project CBM library is **`/home/pi/pcbm`**. Menu, VICE, CONTENT, USB IMPORT,
FILES and the **Project CBM** network share use this same root. `pi` runs the local
appliance; `pcbm` is your administrator/SSH login. Its home, `/home/pcbm`, stores your
shell files and is not automatically browsed or exported as appliance content.
An SSH/SFTP connection normally starts in that administrator home. Use File Sharing
for the simplest network content transfer; sign in as `pcbm` with the separate
File Sharing password. The share writes files as `pi`, keeping them usable locally.

## Folders and examples

Content type comes first, then machine. This preserves the familiar GAMES, DEMOS,
MUSIC, PROGRAMS and ROMS menu and lets one USB import choose a category and machine.
A machine-first layout would group one machine neatly but require changing the
existing category menu and relocating established libraries. No such relocation is
needed. Machine folders also tell CONTENT which profile to launch.

```text
/home/pi/pcbm/
  games/c64/My Game.d64
  games/vic20/My Game.prg
  demos/c64/My Demo.prg
  demos/c128/80col/My Demo.d81
  programs/pet/My Program.prg
  programs/cbm2/My Program.d80
  programs/cbm5x0/My Program.prg
  programs/plus4/My Program.prg
  music/c64/Creation/SID-Wizard/SID-Wizard-1.97.d64
  programs/c64/Communications/StrikeTerm/StrikeTerm-2014-Final.d64
  music/c64/Imported/My Tune.sid
  roms/c64/My Legally Supplied ROM.rom
  games/shared/Unclassified Disk.d64
  screenshots/
  saves/
```

Example third-party filenames do not represent included or licensed content.
StrikeTerm retains its private-engineering/public-redistribution gate.

`games`, `demos` and `programs` provide c64, c128, vic20, plus4, pet, cbm2, cbm5x0
and shared folders. `music` initially provides c64, c128, vic20, plus4 and shared;
PET/CBM-II software that generates sound can still be kept in its programs folder.
`roms` provides the seven machine families; ROMs are machine-specific resources.
You may create additional folders for your own collection.

**Shared** is an explicitly unclassified or intentionally cross-machine collection.
It does not mean a disk works on every machine. Shared and older unclassified paths
use the RUN default when launched; choose that default appropriately. Files within
recognized machine folders choose a compatible profile without changing RUN. C64
normally uses x64sc; an already selected C64 variant remains selected for ordinary
C64 content. `c128/80col` explicitly selects the 80-column profile. SID-Wizard and
StrikeTerm application disks use the normal C64/x64sc profile.

## Formats are files, not another folder layer

A `.prg` or `.p00` program, tape image (`.tap`/`.t64`), cartridge (`.crt`) or disk
image (`.d64`, `.d71`, `.d81`, `.d80`, `.d82` and other VICE formats) already identifies
its media format. No disk/tape/cart/prg subdirectories are required. Use titles,
collections or publishers as additional folders if useful to you.

An extension is not a machine identifier. A PRG can target several different machines;
a D64 may contain C64 or another machine's software. Put it in the correct machine
folder. C128 double-sided/1581 disks, PET/CBM-II business-drive images, VIC-20 memory
expansions, Plus/4 cartridges and C64 cartridges require matching VICE hardware/media
settings. Importing a file is not proof of compatibility. For media requiring explicit
drive/model/expansion configuration, launch the machine and attach it through F10.
ROM, raw `.bin` and REU resources are not generic autostart programs; configure them
inside VICE. PSID/RSID player integration remains a separate deferred feature: SID
files can be stored/imported, but CONTENT does not claim general SID playback.

## USB IMPORT

Choose the USB partition, machine and content category. Supported regular files are
copied beneath `category/machine/Imported`, preserving source subfolders. SID files
always go to `music/c64/Imported`. Existing destination files are skipped, never
replaced. Symlinks, special files and unsupported types are skipped. The source is
mounted read-only; follow completion or failure guidance before unplugging it.
An unclassified collection may use Shared, then be organized later with FILES.
A source already containing category/machine folders is not silently flattened:
copy an already organized library tree through File Sharing to avoid nesting that
whole tree beneath one import destination.

## Older content and misplaced SSH uploads

Existing category-level files and folders remain browsable recursively. Nothing
automatically moves, deletes or scans your administrator home. Earlier SID-Wizard and
StrikeTerm folder locations still work; fresh images seed the new C64 locations.
Keep an independent backup before reorganizing your own library. FILES starts at the
canonical root; VICE also starts there, but its file browser can navigate elsewhere.

For ordinary transfers, connect to the Project CBM share and copy selected files into
its category/machine folders. You do not need to type `/home/pi/pcbm` in Finder.
For a deliberate administrator copy of the observed misplaced demo folder, after
backing it up, these commands copy regular files without replacing existing files:

```sh
sudo install -d -o pi -g pi /home/pi/pcbm/demos/c64
sudo rsync -rt --ignore-existing --chown=pi:pi -- \
  /home/pcbm/demos/c64/ /home/pi/pcbm/demos/c64/
```

Run this on your own configured appliance, not on an immutable qualification card
being preserved. It is an authenticated owner action, not a new passwordless helper.
The source is retained; review copied files before any later manual cleanup. Do not
copy the whole administrator home, SSH keys, configuration databases or credentials.
For a new SD image, complete first boot and copy selected content back from your
backup/share; retain the new account and service configuration.

## Builders and derivatives

`runtime/project_cbm/library.py` owns the root, family-to-profile selection and fresh
hierarchy. `tools/install_poc_stage.py` creates that hierarchy. `applications.py`
recognizes current and legacy application folders; `importer.py` enforces constrained
copy destinations. The Menu consumes Product's `pcbm-profiles content-families` and
`content-profile` interfaces. Samba's single export is declared in
`runtime/config/file-sharing.example.conf` and the shared VICE launcher keeps its
working directory at the library root.

Changing the hierarchy requires Runtime and affected Menu package builds, updated
optional-input recipes/manifests where application paths change, a new frozen image,
and import/content/lifecycle tests. Adding lawful user files requires no package build.
Keep deeper emulator/account/TTY changes separate from organizing a content collection.
