# Project CBM 1.1 User Manual

[Documentation index](../README.md) · [Getting Started](getting-started.md)

Project CBM is a Commodore computer collection operated from a keyboard Menu. It
starts the emulator for you, keeps your content in one library, and offers ordinary
setup and network tasks without requiring Linux commands. You can still use Linux
when you want to. This manual describes the current 1.1 release-candidate software;
final physical qualification is ongoing, and 1.1 has not yet been publicly released.

For the first power-on, follow [Getting Started](getting-started.md). You do not need
the builder or developer guides to use an image.

## Keyboard and navigation

| Key or action | What it does |
| --- | --- |
| Up/Down arrows | Move through a list |
| Left/Right or Tab | Move between buttons or fields where the screen offers them |
| Enter | Activate the highlighted item/button |
| Space | Toggle a checkbox or radio choice when one is shown; in text input it types a space |
| Back, Cancel or Return | Leave that screen or revisit the previous step, as its label says |
| Escape | Cancel/return; during first boot it pauses setup. At Main Menu it leaves the Menu open |
| F10 inside VICE | Open the emulator menu; choose Quit to return |
| Ctrl+Alt+F2 at Project CBM | Switch to the Linux console; Ctrl+Alt+F1 returns to the appliance |

A selected list row and a selected button are different. If Enter seems to activate
Back rather than your choice, use Tab to move focus to the intended button. Small
keyboards may require Fn for function keys. Project CBM needs a usable text display
of at least 40 columns by 12 rows.

Switching Linux consoles while VICE is active is a known limitation of this graphics/input
setup. The normal route is **F10 → Quit**, then switch consoles from Project CBM.

## Main Menu

Above the choices, **Default** names the machine RUN will start. Network information
shows connected Ethernet/Wi-Fi addresses, or a disconnected/unavailable message. When
relevant, a compact line shows File Sharing, Remote Access (SSH) and BBS / Modem state.
Inactive services need not occupy a line. A connected address is not a promise of
Internet access. Detailed information belongs in CONTROL.

| Item | What happens when you choose it | Use it when… |
| --- | --- | --- |
| **RUN** | Starts the saved default machine after its Cover | You want your usual Commodore computer |
| **MACHINES** | Lists machines to launch and a DEFAULT action | You want a different machine now or a new RUN default |
| **CONTENT** | Opens Games, Demos, Music, Programs and ROMs lists | You want to find and launch a file in your library |
| **IMPORT** | Selects a USB partition, machine and category, then copies supported files | You brought content on a USB drive |
| **CONTROL** | Opens configuration, status and Advanced access | You want to change settings or check the system |
| **FILES** | Offers Midnight Commander or USB import | You want to organize files rather than launch them |
| **POWER** | Asks for confirmation, then shuts down | You are finished and will remove power |
| **REBOOT** | Asks for confirmation, then restarts | You need a fresh start or want a new keyboard setting to take effect |

## RUN and VICE basics

The fresh default is **Commodore 64**. RUN starts that profile, not whichever file you
last browsed. A **Cover** is the artwork identifying the machine before emulation.
It is cosmetic: if unavailable, the emulator should still start after safe cleanup.
Customizers can [replace Covers](customization.md#replace-a-machine-cover).

VICE is the software emulating the Commodore computer. Its BASIC prompt accepts
Commodore commands, not Linux commands. F10 opens VICE's own menu. Arrow keys and
Enter navigate it; Back/Escape return through its menus. Choose **Quit** to end the
emulated session and return to Project CBM. Launches from MACHINES or CONTENT may
return first to their calling list; use Return to reach Main Menu.

CONTENT is usually the easiest way to start a disk or program. For manual operation,
start the appropriate machine, press F10 and use VICE's media/autostart or drive
attachment entries. Select the image in the file selector and choose the desired
autostart/attach action. Attaching a disk alone does not always start its program.
C64 users can list an attached drive-8 disk with `LOAD "$",8` then `LIST`, or load its
first program with `LOAD "*",8,1` and `RUN` where that program expects it. Other
machines/media can require different commands; follow the software's instructions.

VICE also controls emulated joysticks, keyboard mapping, drives, RAM expansions,
PAL/NTSC and sound chips. Do not change several unfamiliar settings at once. Use
VICE's settings save action when you want a choice to survive another launch; Project
CBM keeps saved settings instead of resetting them each time. Back up those preferences
before experimenting. [Technical VICE reference](vice.md) is optional reading.

## MACHINES

Selecting a machine in the ordinary MACHINES list **launches it now**. It does not
change RUN. To change RUN, choose **DEFAULT — Set the machine used by RUN**, then the
machine. The Main Menu's Default line confirms the saved choice; it persists after
reboot. The current default has an asterisk in the list.

| Display name | What it represents / typical use | Media notes |
| --- | --- | --- |
| Commodore 64 | Normal C64; the recommended starting choice for games and demos | PRG/P00, disk, tape and cartridge images appropriate to C64 |
| Commodore 64 (fast) | Alternate C64 emulation core with different accuracy tradeoffs | Same broad C64 media; not a guarantee that demanding software behaves identically |
| SuperCPU 64 | C64 with CMD SuperCPU expansion | Software written for that expansion; ordinary C64 software may also work |
| Commodore 64 DTV | Direct-to-TV C64 variant | DTV-specific software and compatible C64 material |
| Commodore 128 (40 column) | C128 using the VIC-II display | C128 programs/disks and their required drive configuration |
| Commodore 128 (80 column) | C128 using the VDC display | 80-column C128 applications; choose this when the program requires VDC output |
| Commodore VIC-20 | VIC-20 home computer | VIC-20 programs/tapes/cartridges; RAM expansion requirements matter |
| Commodore Plus/4 | TED-family Plus/4 computer | Plus/4 programs and supported media; C64 files are not interchangeable |
| Commodore PET | PET business/educational computer | PET BASIC/programs and disks matching the selected drive/model |
| Commodore CBM-II | CBM-II business computer | Its own software, including business-drive disk images |
| Commodore CBM-II 5x0 | VIC-II-equipped CBM-II 5x0 family | Software for that family, not ordinary C64 compatibility by filename |

Project CBM exposes the two C128 display profiles and the C64 alternatives above.
It does not offer a separate PAL/NTSC switch in MACHINES; that is a VICE setting.
The [technical profile/media table](vice.md#profiles-and-media) maps these names to
executables and distinguishes browsable files from safe automatic launch.

## CONTENT and IMPORT

CONTENT → **GAMES**, **DEMOS**, **MUSIC**, **PROGRAMS** or **ROMS** shows matching files
recursively, with paths such as `c64/My Game.d64`. Select the file directly; there is
no extra machine submenu in CONTENT. Its folder identifies the intended machine.
Shared/unclassified files use the saved RUN default. Selecting content does not save
a new default. ROM and memory-resource files can be browsed but need VICE settings
rather than generic automatic launch. SID files can be stored/imported; generic SID
music playback is not implemented.

The library is **/home/pcbm/content**. In File Sharing it is the top of the **Project CBM**
share. In an SFTP client it is the `content` folder inside your home. See the
[content guide](content.md) for concrete paths, media limits and the complete USB walkthrough.
IMPORT reads the USB source without changing it, preserves duplicates and reports
whether the drive was safely released. Do not remove it until the result says so.

## FILES and Midnight Commander

FILES opens **Files and USB**. Choose **LIBRARY — Browse files with Midnight Commander**
for the file manager, or **USB — Import from USB into the library** for the same import
workflow as Main Menu. Midnight Commander is a two-pane file manager for organizing
files with the keyboard. One pane starts in the library and the other in your home.

Use arrows and Enter to open a directory; `..` goes up. Tab changes panes. Insert
marks/unmarks files for a multi-file operation. F5 copies to the other pane, F6 moves
(or lets you enter a new name), F7 creates a directory, F8 deletes, and F10 quits.
Read the source/destination and confirmation before accepting a copy, move or delete.
Deletion is not a backup. F1 opens help. These are the default controls documented in
[Midnight Commander's manual](https://source.midnight-commander.org/man/mc.html).

USB drives are presented through Import, not automatically as mounted folders inside
Midnight Commander. Import first, then organize the copies in the library. This keeps
ordinary USB transfer independent of Linux mount commands.

## CONTROL

CONTROL opens **Project CBM Control**. Back/Escape leave each submenu. Ordinary changes
use the normal pcbm session after first boot; you are not repeatedly asked for the
administrator password. General administrator tools under Advanced do require it.

### Machine and Startup

**Choose default Commodore machine** opens the same default selector as MACHINES.
**Boot preference** offers **Menu (recommended)** or **Default emulator**. The preference
is saved for the next login/boot. With Default emulator, Project CBM makes one launch
attempt, then returns to Menu when it quits or fails. Changing the default alone does
not change this boot preference.

### Picture, Sound and Controllers

**Audio output and test** offers Automatic connected HDMI, First HDMI output, Second
HDMI output, Speaker test, System Information and Back. Select the connected output,
then test it. The chosen audio configuration persists in your user settings. A display
without speakers may need another audio arrangement configured through Advanced.

**Advanced Mixer (ALSA)** opens the system's sound mixer. Some digital outputs have no
hardware volume control. Escape closes the mixer; its persistence follows the system's
ALSA settings. **Display / VICE picture settings** explains aspect-correct fullscreen
and directs you to F10 in VICE. **VICE keyboard and controller settings** similarly
explains where to configure emulator input. They are guidance screens, not new graphics
or joystick control panels. Host keyboard layout is in the next section.

### Language, Keyboard and Region

Choose **System language/locale**, **Console keyboard layout** or **Timezone** and select
from the offered choices. Language/time changes are applied through the system; restart
sessions as needed. Keyboard configuration is saved for the next boot. Changing it does
not retype or translate an existing password. Regional choices persist.

### Network

The [network guide](networking.md#network-controls) explains all of these actions:
Network information (IP/MAC and status), Computer Name, Wi-Fi country and radio,
Nearby Wi-Fi networks, Join Wi-Fi by name (WPA personal), Disconnect Project CBM Wi-Fi,
Forget Project CBM Wi-Fi, Enable normal networking, and Stay offline (disable connections).
Settings act immediately except where a screen says otherwise. Going offline can end
an SSH or File Sharing connection, including the one you are currently using.

### Services

**File Sharing**, **Remote Access (SSH)**, **Network Discovery**, and **BBS / Modem** each
open a status screen. Off offers Turn On; On offers Turn Off. Starting / Pending,
Unavailable and Failed distinguish a service still starting, one that cannot be
observed/used, and one that failed. Refresh status rechecks it; How to connect shows
addresses and instructions. Saved intent and actual running state are different.

File Sharing also has Set / change File Sharing password. BBS / Modem also has Modem
port and speed. All service settings persist. See [services](networking.md#services)
for credentials, connection examples, effects and how to turn them off.

### Content and Storage

**Capacity and free space** opens System Information. **Content locations / USB import**
explains where the library lives and how to reach it. **Backup and restore guidance**
explains selective backup/reflash/restore; it is guidance, not an automatic backup tool.
Use the [backup steps](recovery.md#back-up-your-files) before changing an SD card.

### System Information and About Project CBM

**System Information** helps you find the current IP, check the Pi model/version,
inspect network state, or see storage and service information. It includes available
identity/OS/kernel/hardware, machine/profile, storage, interfaces/IP/MAC/gateway/DNS,
networking, sound/device and service observations. Missing or unavailable data is
reported honestly rather than guessed. **About Project CBM** gives the installed
product/component/build information and project links. Neither screen changes settings.
For a problem report, quote the relevant values rather than posting a whole private
configuration dump.

### Advanced

- **Terminal (pcbm; exit returns)** opens your ordinary Linux shell. Type `exit` to return.
- **Administrator shell (password required)** opens authenticated administration. It can
  change the operating system. Type `exit` when finished.
- **Authenticated raspi-config** opens Raspberry Pi's advanced configuration tool with
  your password. Use Project CBM's normal settings first when they cover the task.
- **Engineering diagnostics** runs available diagnostic reporting; read its privacy
  guidance before sharing output. It is not a repair button.
- **Administration and recovery guidance** explains normal Linux access and backups.

This is your computer. The normal username is **pcbm**, home **/home/pcbm**. SSH uses
the administrator password chosen during setup; `sudo` asks for that password before
running general administrative commands. Local console autologin is not a locked
workstation. Use sensible home-network passwords and enable remote services only when
needed. See [accounts and paths](accounts-and-layout.md) when you want the technical detail.

## Optional applications

**SID-Wizard 1.97** is a C64 music-creation tool, not a generic player for downloaded
SID files. Open CONTENT → MUSIC and choose
`c64/Creation/SID-Wizard/SID-Wizard-1.97.d64` when included. It starts normal C64 emulation.
Save your own work on writable working disks and back them up; F10 → Quit leaves VICE.
The selected core tool has established project license evidence; unrelated examples,
songs and add-ons are not automatically included.

**CCGMS 2021** is a Commodore 64 terminal for calling bulletin board systems (BBSs).
Open CONTENT → PROGRAMS → `c64/Communications/CCGMS/CCGMS-2021.d64`. Project CBM
starts the C64 with the modem interface this application needs. Enable BBS / Modem
first, then follow the [CCGMS connection walkthrough](networking.md#bbs--modem).
The supplied disk contains CCGMS alone; its program is unchanged from Alwyz's release.
Your saved phone book and settings belong to your working disk, so back it up with
other content. F10 → Quit returns to Project CBM. Remote BBS availability and account
requirements are controlled by each BBS operator.

There is no general Applications or TOOLS Main Menu entry. Other software can be used
through content or Advanced as appropriate; installation alone does not create a Menu item.

## Common tasks

| I want to… | Steps |
| --- | --- |
| Play a C64 D64 game | Copy it to `content/games/c64`; CONTENT → GAMES → `c64/filename.d64` |
| Run a PRG demo | Put it in `content/demos/<machine>`; CONTENT → DEMOS → the file |
| Make VIC-20 my default | MACHINES → DEFAULT → Commodore VIC-20; check Main Menu Default |
| Import a USB disk | IMPORT → partition → machine → Games/Demos/Programs/Music; read the result |
| Find imported files | CONTENT → category → `<machine>/Imported/...` |
| Copy from Mac or Windows | CONTROL → Services → File Sharing; set its password, turn it on, then [connect](networking.md#file-sharing) |
| Find my IP | Read Main Menu, or CONTROL → Network / System Information |
| Use SSH | Turn on Remote Access; use How to connect with username pcbm |
| Change Wi-Fi | CONTROL → Network → Nearby Wi-Fi networks |
| Change Computer Name | CONTROL → Network → Computer Name |
| Return from emulation | F10 → Quit; Return if a machine/content list is shown |
| Restart | Main Menu → REBOOT → confirm |
| Finish using it | Main Menu → POWER → confirm, wait for shutdown, then remove power |

## Backups, upgrades and help

Project CBM release upgrades use **back up → flash a new image → complete setup →
restore selected user data**. There is no Menu-driven in-place OS release upgrade.
Your portable library is separate from system packages, which the new image replaces.
Keep content, saved emulator settings and personal work on another device before
reflashing. See [backup and recovery](recovery.md) and [troubleshooting](troubleshooting.md).
