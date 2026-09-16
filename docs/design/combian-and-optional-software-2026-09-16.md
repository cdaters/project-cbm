# Combian reference and optional Commodore applications

**Research: 2026-09-16. Recommendation only; no software acquired or embedded.**
Local reference: `/Volumes/TheBench/Projects/Combian/`, inspected read-only.
No historical scripts executed, no files reorganized, no credential/history contents inspected or disclosed.
The directory's 939-entry read-only baseline is retained with this audit's external
evidence. Local copies are evidence, not Project CBM source or distribution permission.

## Combian: observed versus inferred

The extracted `fromCombian64_v37/usr/local/bin/menu` is a Bash/dialog front panel
bearing Carmelo Maiolino's Combian identity. It has a large fixed-size, largely flat
menu (50×92 requested, 46 menu rows), section-like blank entries, machine choices,
network/service operations, raspi-config, file management and power commands.
Profile startup runs a selected emulator, then Menu. A framebuffer cover is shown
with a delay. The source edits a line in the bootmachine script to change the default;
RUN manages TCPser with shell/background/port-based process operations and suppressed
output. Some paths recursively restart the menu. These are observations of code,
not claims that every branch works on modern Raspberry Pi OS.

The v3.7 menu has a SID-Wizard launch case (`W`) pointing at the 1.8 D64, but `W` is
absent from its visible option list. Other local menu text advertises StrikeTerm and
SID-Wizard as ready to use; that does not prove this extracted menu can reach them.
No verified working StrikeTerm-specific launcher was established. Do not invent a
Combian runtime test from its included files.

The local `fromCombian64_v5` README/BUILD_INFO and menu identify a **fan-built
continuation** inspired by Combian 3.7. Its grouped menus and `/etc/combian5` state
must not be attributed to Carmelo's original implementation. It also has broad sudo
writes and inconsistent `music`/`musics` references. Its presence here is not evidence
of an official upstream Combian v5 release.

| General idea | Useful lesson for Project CBM | Avoid copying |
|---|---|---|
| Emulator plus recognizable console front panel | Keep immediate RUN and machine switching, Commodore identity | Fixed oversized menu and flat administrative clutter |
| Included creative/communications tools | Useful tasks beyond games, accessible through content workflows | Assuming included binaries have redistributable rights |
| Default-machine/startup choice | One understandable preference | Editing executable launcher lines as configuration |
| Appliance startup presentation | Intentional brief identity while starting | Unconditional delays and hidden failures |
| Services near emulator usage | Explain modem/file-sharing capabilities in user terms | Port-based kill-9, suppressed errors, arbitrary service/root commands |
| Central settings | Shallow consistent grouping | Recursive menus, duplicate state and privileged UI |

Combian v3.7 info describes donationware/personal modification and commercial
restrictions. This is not an open-source grant for copying menu code, artwork or
media into Project CBM. Retain ideas, write original code, request permission if
specific expression/assets are ever desired. Project CBM's current smaller front
door and shared unprivileged launcher are already stronger foundations; different
organization alone does not make Combian superior.

## StrikeTerm2014

**Identity:** StrikeTerm 2014 Final by **Alwyz**, C64 terminal software derived from
Novaterm 9.6. The author's [2014 release announcement](https://1200baud.wordpress.com/2014/05/17/striketerm-2014-final/)
is dated May 17, 2014; later comments report loss of the development drive/source.
A planned 2015 version is not evidence that it shipped. The author's
[release forum post](https://www.lemon64.com/forum/viewtopic.php?t=52121) describes
IP-BBS/CommodoreServer-oriented changes and hardware support. No verified later
StrikeTerm release or complete exact-2014 source closure was established here.

The author's [2013 documentation](https://1200baud.wordpress.com/striketerm-2013-documentation/)
calls that version freeware and identifies Nick Rossi's public-domain Novaterm base;
it also reserves rights in the manual. These statements do **not** establish an
explicit redistribution grant for every byte of the 2014 disk or documentation.
Availability in Combian or on a download site is insufficient. The audit did not
fetch the release disk or source archives.

**Recommendation:** initially support owner/user-supplied media, after a future
technical integration test. Do not bundle the Combian disk or offer an automatic
Project CBM download until exact release permission and provenance are established.
If permission arrives, retain its text, exact artifact/source identity and SHA-256;
keep third-party notices separate from Project CBM's license. This is an unresolved
redistribution gate, not a conclusion that all personal use is prohibited.

Runtime is a C64 application under VICE, not a Linux executable. VICE's
[RS232 reference](https://vice-emu.pokefinder.org/wiki/RS232) explicitly mentions
StrikeTerm/Novaterm for SwiftLink/Turbo232 and describes IP232 connections to a local
modem simulator. A future Project CBM profile must validate the chosen emulated serial
hardware, baud/flow control, TCPser bridge and connection lifecycle; generic disk
autostart is not proof of modem functionality. The reference also cautions about
loading/connection order. Keep external listeners opt-in, prefer a local emulator
bridge, and test disconnect/error handling without granting the C64 program root.
No networking/service behavior changed in this audit.

A credible separately evaluated alternative is
[CCGMS Future](https://github.com/mist64/ccgmsterm): source/build/tests are available,
with user-port and SwiftLink-family support described upstream. The observed release
is Future 0.2 (2022), not evidence of active 2026 maintenance. It is not automatically
a StrikeTerm successor or a replacement decision. Exact license and capability
review is required before selecting any alternative. There is no established
Project CBM compatibility reason to mandate the historical 2014 build today.

## SID-Wizard 1.8 and current versions

**Identity:** Hermit / Mihály Horváth's native C64 music tracker. The author's
[SourceForge project](https://sourceforge.net/projects/sid-wizard/) points to later
release locations. [SID-Wizard 1.8](https://csdb.dk/release/?id=165302) is a 2018 release.
The [1.97 release page](https://csdb.dk/release/?id=262561) records June 24, 2026 and
includes author discussion and source/example references. Thus 1.8 is not the latest
identified release. Legacy author web/GitHub links were not all reachable; preserve
exact retained inputs and permission rather than relying on permanent URL availability.

A [source fork](https://github.com/anarkiwi/sid-wizard) retains Hermit's notices,
identifies a permissive WTF license, and shows native source/64tass-based construction.
This is positive evidence of source availability/licensing, **not verification that
this fork equals the author's exact 1.8 archive** or that every included tune, manual,
instrument bank and third-party asset shares one grant. Before distribution obtain
and review the chosen authoritative release's actual license/source/notices and
artifact hashes. No release archive was downloaded during this audit.

**Recommendation:** conditionally include a verified native C64 SID-Wizard core in
a later optional application bundle; evaluate current 1.97 against 1.8 before choosing.
Use 1.8 only for a demonstrated compatibility/workflow reason or owner preference,
not because the Combian folder names it. The local folder also contains a 1.9 disk,
so a folder name is not a clean release identity. Desktop/Linux ports mentioned in
current release discussion do not establish arm64 compatibility or a need for a
second host application in this console appliance.

Integration should use Music → Creation → SID-Wizard through the normal content
browser and shared unprivileged launcher. Preserve an immutable verified template,
create a user-owned working disk for songs/preferences, and explain Save/Export.
Test load, edit, audible output, save, reopen and export, with PAL/NTSC timing and
6581/8580 choices explicit. Multi-SID editions need separate tests; POC3's three
voices on one SID do not qualify two/three-SID operation. Include only licensed core
and required examples, not an arbitrary music collection.

## Existing reference-copy identities (not accepted build inputs)

The following files are byte-identical between the local v3.7 and fan-v5 extracts.
This comparison establishes **local equality only**, not equality to upstream or
permission to redistribute. Hashes were computed without changing the originals.

| Filename | Bytes | SHA-256 |
|---|---:|---|
| `st2014final.d64` | 174848 | `72b803c54c7892857c0ddb5674dabc841d59a496285975546bef689308940595` |
| `SID-Wizard-1.8.prg` | 29029 | `06cbcf66bb8a740487487e28441e27dddfa04d771e43f3a5d621e447a675add0` |
| `SID-Wizard-1.8-disk1.d64` | 174848 | `915019a135600dc36bfe8c510601aeb3cb92a36c9ca9fe01f8cb0cb6d702d28d` |

Paths relative to each extract's `home/pi/combian64`: StrikeTerm is under
`programs/StrikeTerm2014/`; SID-Wizard is `musics/SidWizard1.8/` in v3.7 and
`music/SidWizard1.8/` in fan-v5. These tiny individual files do not measure the total
optional bundle or runtime RAM/CPU. Exact upstream agreement, modifications, chosen
release source and legal closure remain unverified.

## Future admission checklist, not current authorization

For each selected application record author, authoritative source, version/revision,
source availability, exact SHA-256, license/permission, retained notices, expected
machine/serial/audio resources and tested workflow. Separate immutable template from
user saves, and make missing optional media a helpful prompt rather than a broken
menu entry. Never interpolate a filename or downloaded metadata into shell commands.
An embedded bundle becomes a frozen release-lock input; it cannot be added to an
already qualified image. A user-supplied artifact remains outside the base identity.
