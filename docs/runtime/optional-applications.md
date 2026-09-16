# SID-Wizard and StrikeTerm

**Source integration, 2026-09-16; not an image update.** POC1–3 are unchanged.
A later owner-approved candidate must install the matching product/Menu source,
consume the new frozen inputs and complete the [physical procedure](../qualification/optional-applications-procedure.md).
No application playback or modem connectivity is claimed from source tests.

## SID-Wizard: make music on the C64

The selected application is **Hermit's SID-Wizard 1.97, native C64, one SID**, with
SID-Maker for exporting your work. It runs inside VICE; the Linux/Windows/macOS
ports are not included. The prepared core disk contains no example music collection.

In a future integrated candidate:

1. Open **CONTENT → MUSIC → Creation/SID-Wizard/SID-Wizard-1.97.d64**.
2. The content route selects the registry's Commodore 64 (`x64sc`) for this launch.
   Your normal default machine is unchanged.
3. Work on the user-owned disk; keep backups before saving new songs or settings.
   Consult the [upstream native documentation](https://csdb.dk/release/?id=262561)
   for the tracker and SID-Maker. The complete upstream manual is not embedded.
4. Use **F10 → Quit** in VICE to return to Project CBM. VICE preferences, picture
   geometry and audio remain under the existing shared launcher/configuration policy.

The working disk is `/home/pi/pcbm/music/Creation/SID-Wizard/SID-Wizard-1.97.d64`.
The image factory also supplies an immutable reference template under
`/usr/share/project-cbm/applications/sid-wizard/`. Normal launches never recopy it
or overwrite user songs. A future upgrade must preserve existing working disks;
copy a new template deliberately, retaining the old disk. This pass does not add a
restore button or advanced tracker tuning.

## StrikeTerm: owner-supplied communications software

StrikeTerm 2014 Final is Alwyz's C64 terminal based on Novaterm. Its author
[directs users to CSDb](https://1200baud.wordpress.com/2014/05/17/striketerm-2014-final/);
[release 130807](https://csdb.dk/release/?id=130807) identifies `st2014final.d64`.
Project CBM has not established sufficient redistribution permission for the disk,
so it supplies **no StrikeTerm bytes or automatic download**.

For a later candidate with content transfer ready, put a copy you may lawfully use
under `/home/pi/pcbm/programs/Communications/StrikeTerm/`, retaining its D64 filename.
Open **CONTENT → PROGRAMS → Communications/StrikeTerm** and select the disk. This
folder uses Commodore 64 without changing your default machine. Supported input for
this bounded integration is a regular, standard 174,848-byte D64 with a first PRG
directory entry; symlinks, malformed files and other media types are rejected.
These checks validate the launch shape, not the program's authorship or behavior.

Launch, keyboard and return can be tested offline. **BBS connectivity is separate:**
TCPser/network activation, emulated serial hardware, baud/flow control and a local
bridge must be qualified first. No service starts merely because StrikeTerm launches.
Do not put real passwords or a personal dial directory into a distributed template.

## Availability and content rights

Safe USB import and optional file sharing still await the runtime-activation gates
in [pcbm-config](pcbm-config.md). Do not modify a frozen POC to install these files.
Neither application adds a new main-menu item. The [reference content guide](reference-content.md)
covers owner-supplied SID tunes/demos separately. Our original Project CBM
qualification suite remains intact.

[Technical decisions, exact hashes and rights review](optional-applications-contract.md)
explain what is admitted and what remains pending.
