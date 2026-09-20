# Project CBM user guide

Project CBM makes a Raspberry Pi feel like a Commodore computer you can switch on and
use. A keyboard-operated Main Menu chooses machines and content, then VICE runs the
emulated computer. Covers mark the transition between the front panel and each machine.
You can also transfer your files over a home network, use a USB drive, make music and
return to normal Linux administration when you need it.

Project CBM 1.1 uses Raspberry Pi OS Lite arm64 based on Debian 13 (Trixie). These
instructions describe the developing 1.1 appliance. Use the [current candidate and
qualification status](../../CURRENT-STATE.md) when choosing an image: a successful
build does not mean every feature or Raspberry Pi model has been physically tested.
Project CBM 1.1 targets Pi 4-class hardware and newer. Pi 3/Zero-class hardware is
outside this release target. Pi 4 B has an owner-reported C64 performance PASS; the
new RC image and other models still need their own physical qualification.

## Getting started

1. Obtain the image and its matching SHA-256/physical procedure. Verify the complete
   checksum before flashing. On macOS use `shasum -a 256 IMAGE.img.xz`; on Linux use
   `sha256sum IMAGE.img.xz`, replacing the example filename with your actual download.
2. Write the image to the intended expendable SD card with an imaging application.
   Double-check the selected device: flashing erases it. Leave Raspberry Pi Imager's
   OS customization off for this appliance's supported first-boot workflow.
3. Safely eject the card. Connect HDMI, a keyboard and a suitable Pi power supply;
   insert the card and switch on. Ethernet is optional. A controller is not required.
4. Complete the setup screens, choose a password, and optionally join Wi-Fi.
5. Select RUN. After the Cover, the default Commodore machine starts. In VICE, press
   F10 and select Quit to return. Use POWER in the Main Menu when finished.

The card must hold the actual uncompressed image and leave room for your content and
future maintenance. Root-filesystem expansion happens automatically through Project
CBM's first-boot coordinator. Do not select a card solely from an unsupported nominal
minimum. Pi 4 B/400 and Pi 5/500/500+ need their own qualification. See
[hardware status](../supported-hardware.md)
for the distinction between intended support and retained test evidence.

## First boot and your account

Choose language/locale, keyboard layout, timezone and Wi-Fi country. Apply the country
where the Pi will actually operate; it affects which wireless networks are available.
Some keyboard changes take effect after reboot, so use the current keyboard layout
when entering the first password. Password fields show asterisks while you type.

Your administrator login is **`pcbm`**. Choose an owner password of 12-128 printable
characters, excluding colon, and confirm it. This password is used for Remote Access
(SSH) and Advanced administration. There is no universal factory password. You do not
need to invent or remember a separate username. “Owner” on a screen describes your role.
Menu, VICE, files and remote login all use `pcbm`. Your home is `/home/pcbm`;
your appliance library is its `content` folder. No second local account is needed.

Networking can be skipped. To use Wi-Fi, choose an available network and enter its
8-63-character printable ASCII personal-network password. Scanning shows progress and
waits for the radio to become ready within a bounded period. If no network appears,
check the country, range and access point, then retry or continue offline. Enterprise
Wi-Fi and unusual connection types belong in Advanced administration. Ethernet can
use an ordinary home router connection; the appliance does not require interfaces to
be named eth0 or wlan0.

Back revisits the previous setup step; Escape can pause setup. Completed choices are
retained and unfinished setup resumes. The wizard stops rerunning after successful
completion. Do not unplug power while it is expanding the filesystem or saving setup.
If initialization fails repeatedly, preserve the displayed error and follow
[recovery](recovery.md).

## Keyboard and screen navigation

Use the arrow keys to move through dialog menus, Enter to select and Tab to move
between buttons where offered. Back/Cancel return without applying an unfinished edit.
Read confirmation screens before forgetting a network, powering off or entering
Advanced administration. The settings screens show progress while work is in progress;
if a service fails, its status should explain that instead of claiming success.

Function keys belong to the active application. F10 opens VICE's menu while emulating;
Midnight Commander also uses F10 to exit its own file manager. From the Project CBM
Menu, Ctrl+Alt+F2 switches to tty2 and Ctrl+Alt+F1 returns. The current SDL/KMS console
path does not support that keyboard VT shortcut while VICE owns the console: quit VICE
first. This limitation is separate from C64 performance. Do not change Linux keyboard
or console modes to force a switch on a qualification image.

## Main Menu and status

| Entry | What it does |
| --- | --- |
| RUN | Start the saved default machine immediately |
| MACHINES | Launch another machine/profile or change the RUN default |
| CONTENT | Browse and launch recognized games, demos, programs, music or ROM-related files |
| IMPORT | Copy supported content from a removable USB filesystem |
| CONTROL | Configure region, network, services, startup, display/input and Advanced options |
| FILES | Open Midnight Commander to manage your files |
| POWER | Shut down safely |
| REBOOT | Restart safely |

The compact area above the choices shows your default machine, useful connected IP
addresses and relevant service state. With multiple interfaces it can show more than
one address; detailed IP/MAC/interface information remains in System Information.
An IP address means the interface has an address, not that the Internet is reachable.
No connected interface and unavailable information are different conditions.

On service screens, **Off** means the feature is off; **On** requires observed runtime
readiness. **Starting/Pending** means the request and observed state have not converged.
**Unavailable** means required support/readiness is missing; **Failed** means an
observed failure needs attention. Only useful Turn On/Turn Off actions are shown.
After a change the refreshed state is the confirmation—there need not be another
“success” screen to dismiss.

## Machines, Covers and VICE

MACHINES lists the product's registered profiles. The C64, C128, VIC-20, Plus/4, PET,
CBM-II and other profiles use different VICE executables/resources; the name on the
menu tells you which computer you are starting. Changing the RUN default is a saved
preference; launching a different machine once need not change that preference.
CONTROL's startup options choose whether boot enters Menu or attempts the saved machine.

A Cover appears before emulation. It is a transition screen, not the emulator output.
If artwork cannot be displayed, the launcher should still start VICE safely. Once VICE
starts, the emulated machine's keyboard and controls apply. For a simple C64 check,
type `PRINT 2+2` and press Return. You should see `4` promptly.

Press F10 for VICE options, media/drive handling, emulator preferences and Quit.
Choose Quit to return to a responsive Project CBM Menu. Save emulator preferences
inside VICE when you want them to persist; merely changing an option is not always
saving it. The image seeds initial settings but does not overwrite your saved VICE
configuration on every launch. Side margins preserve the complete machine canvas and
correct aspect ratio. Avoid stretching/cropping the picture just to fill every display
pixel. See [VICE details](vice.md) for resource paths and performance tradeoffs.

Games, demos and music should run at their intended speed on qualified hardware. Warp
mode deliberately runs faster and is not a performance-test pass. Consistently slow
music together with slow graphics means the whole emulation is falling behind; it is
not ordinary occasional frame skipping. Record the image identity, machine/profile,
content reference, VICE speed reading and hardware health before changing settings.

## Your content library

See the [content guide](content.md) for folders, supported media, import and safe migration.
Menu, VICE and network transfers use the same `pcbm` identity. SSH/SFTP starts in
`/home/pcbm`: put appliance files in its `content` folder. File Sharing opens that
library directly. Files elsewhere in your home are not automatically listed by CONTENT.


The shared library is `/home/pcbm/content`, with `games`, `demos`, `music`, `programs`, `roms`,
`saves` and `screenshots` subdirectories. Use CONTENT for normal launching and FILES for
file management. Keep related multi-file software together. A filename or extension
alone does not prove compatibility with a machine; choose the matching profile and
use VICE's media controls where needed.

Use content you have the right to use. Project CBM does not make third-party games,
demos, SID music or firmware freely redistributable. A `.sid` music file is not a PRG
and does not automatically become playable through normal autostart; dedicated PSID/
RSID playback is outside the currently implemented launch workflow.

USB import counts actual content files and ignores known macOS/Windows filesystem
metadata, including AppleDouble and Trash. Other hidden content remains eligible;
see the [exact import policy](content.md#usb-import).

To import from USB, insert a supported FAT, exFAT or ext4 partition and choose IMPORT.
Select the intended source/category, review the proposed operation and wait for the
result. Choose a machine family and category. Imported files go to
`category/machine/Imported`; SID files go under `music/c64/Imported`. The importer reads the source through its supervised mount path and
copies admitted content, rather than exposing an arbitrary writable USB mount. Wait
for unmount/cleanup confirmation before removing the drive. If your filesystem or
layout is unavailable, do not guess a device name and force-mount it from an ordinary
menu. Use a supported source layout or qualified Advanced handling.

FILES offers Browse files and Import from USB. Browse files starts Midnight Commander,
a two-panel file manager, with the content library on one side and your home on the
other. USB drives are offered by Import from USB; no manual mounting is needed. Select a panel with Tab,
use arrows/Enter to navigate and read its on-screen function-key labels for copy, move
and delete. Work within your content directories until you are comfortable with it.
Deletion is a real filesystem operation; keep backups. F10 returns from the utility.

## Networking and connecting from another computer

CONTROL → Network shows network-specific information and lets you change the
**Computer Name**, initially `projectcbm`. With Network Discovery enabled, the friendly
name is normally `projectcbm.local`. If you choose another valid name, use that name
in connection commands. The status and connection-help screens generate examples from
current information; use them instead of remembering a stale IP address.

Remote Access and File Sharing are separate opt-in features under Services. Enabling
networking does not automatically enable them. For Remote Access, enable the feature,
wait for On, then use `ssh pcbm@projectcbm.local` or the displayed IP from another
computer. Enter the owner password selected at first boot. The password is not included
in the command. Turn Off Remote Access when you no longer want new remote connections.

For File Sharing, first set its **separate File Sharing password**, then enable the
feature and wait for On. On macOS, Finder → Go → Connect to Server accepts
`smb://projectcbm.local/Project%20CBM`. On Windows, use `\\projectcbm\Project CBM`, or
substitute the displayed address. Sign in as `pcbm`, using the sharing password. The
export is your content library, not the administrator's home or entire Pi filesystem.
See [networking and services](networking.md) for full enable/connect/disable and discovery
troubleshooting workflows.

Network Discovery helps names and services appear on the home LAN. Browsing varies
between clients and network equipment. If the Pi is absent from a browser, try the
explicit name or IP shown by the service. Guest/isolated Wi-Fi, multicast filtering and
different networks can prevent discovery even when a direct connection works.

## BBS, music tools and optional applications

BBS / Modem controls TCPser, the local modem adapter used by emulated software. Its
status, port/baud and connection help are in the relevant service screen. Enabling it
does not connect to a BBS or prove external reachability. Use a BBS endpoint you intend
to contact and configure the matching emulated software; it is not a general public
modem server. Remote BBS/network performance requires its own test.

SID-Wizard is a C64 music editor. Its admitted disk/template and application integration
are separate from third-party music collections. Work on your user copy, save your work
and back it up. StrikeTerm is an optional C64 terminal application admitted for private
engineering; a public image needs its existing rights gate resolved. Neither an installed
application nor a successful launch proves every editor, saving or BBS operation.

## Advanced administration, shutdown and backup

CONTROL → Advanced provides an authenticated owner shell and supported access to
`raspi-config`. Log in as `pcbm` using your owner password. Normal Linux administration
remains available, including authenticated `sudo`. Type `exit` to return from a shell.
Changes to drivers, packages, sessions or privileges can affect the qualified appliance,
so keep a recovery route and record what you changed.

Use POWER or REBOOT instead of pulling the power cable. Wait for shutdown to finish
before removing the card. Back up your content library, saved appliance preferences,
VICE configuration and any important owner files to separate storage. Another folder
on the same card is not a backup. A fresh image plus selective user-data restore is the
preferred route for major/base changes; do not restore old machine IDs, SSH host keys,
account databases or system configuration wholesale.

If boot, keyboard, Cover, sound or Menu return fails, stop repeated testing and preserve
the displayed error and relevant private diagnostics. Do not post passwords, Wi-Fi
profiles, account hashes, private keys or entire logs containing personal data. The
[recovery guide](recovery.md) explains common checks; [accounts and layout](accounts-and-layout.md)
identifies files; the exact candidate procedure defines engineering evidence collection.
[Boot presentation and timing](boot.md) explains the quieter Project CBM startup,
recovery access and the distinction between first and subsequent boots.

See [boot presentation, timing and verbose recovery](boot.md) for the quiet-boot
settings, bounded repeated-initialization correction and physical measurement limits.
