# Bring your own Commodore content

Project CBM's private qualification candidates include our original smoke, SID-tone,
video/input and D64 checks. Those tiny tests establish basic operation. They do not
prove PSID/RSID playback or the fidelity of commercial music and scene demos.

The requested famous SID tunes and **Wonderland XIV** are not being added to the
image. Downloadable does not mean redistributable: [HVSC explains its copyright
limits](https://www.hvsc.c64.org/info#copyright). Use copies you may lawfully use.
The [reference catalog](../design/reference-content-2026-09-16.md) links exact
upstream identities and records which variants need special settings.
[SID-Wizard and StrikeTerm](optional-applications.md) have separate application decisions.

## Where files belong

Paths below are beneath the default `/home/pi/pcbm` content folder.

| Content | Suggested folder |
| --- | --- |
| SID files | `music/Reference/<composer>/` |
| Wonderland XIV, all four original D64 sides | `demos/Reference/Wonderland-XIV/` |
| Other demos, including runnable PRGs or disk sets | `demos/<name>/` |
| Games and their disk images | `games/<name>/` |
| Programs/utilities | `programs/<name>/` |
| Machine ROM resources you may use | `roms/` (resource setup, not ordinary program launch) |

Use **CONTENT → Music / Demos / Programs / Games** to browse recursively. Keep a
multi-disk production in one folder with the original side names. Disk format is
not a category: D64/D81 files belong with the program/game/demo they contain.

The intended transfer workflow is USB **IMPORT**, or deliberately enabled file
sharing, into these folders. **Current source status:** safe USB import awaits its
constrained storage broker; file sharing awaits runtime activation. Neither is
being enabled on frozen POC3. A later candidate's instructions must identify which
transfer methods are ready. Do not repair qualification images to try new content.

**Playback limits:** C64 PRG/D64 loading is physically demonstrated for our basic
suite. Select the appropriate machine before launching your content. Other disk
formats/drive combinations still need qualification. `.sid` files are discoverable,
but reliable PSID/RSID and dual-SID playback needs the planned validated SID-player
route; renaming a SID to PRG is not a solution. Wonderland's full disk/audio behavior
is also unqualified. When enabled, use VICE's disk controls for side changes and
F10 → Quit to return. No network connection is required for local media playback.

## Three clear content classes

- **Bundled:** owned by Project CBM or cleared for redistribution; exact inputs
  and notices are recorded before an image is built.
- **Optional acquisition:** the relevant rights support the intended upstream
  acquisition arrangement; no automatic downloader is implied.
- **Owner-supplied:** Project CBM supplies guidance, not the media bytes.

Our original qualification suite stays separate from third-party reference media.
Project CBM never downloads a tune/demo simply because a filename matches a favorite.
Back up your content and working disks; keep original acquisition copies separately.
