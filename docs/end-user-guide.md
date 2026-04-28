# Project CBM End-User Guide

**Version covered:** Project CBM 1.0.0  
**Build covered:** 2026.04.26  
**Repository:** https://github.com/cdaters/project-cbm  
**Author:** Craig Daters

Project CBM is a ready-to-boot Raspberry Pi image for people who want a fast, simple Commodore-style computer environment without having to build a Linux system from scratch, download emulators, or install a desktop environment. It uses the VICE emulator family to run classic Commodore machines from a friendly menu.

The goal is simple:

> Power on. Boot fast. No nonsense. Just Commodore.

This guide is written for normal/beginner Raspberry Pi users. You do not need to be a Linux expert. If you can flash an SD card, plug in a keyboard, and follow a menu, you are in the right place.

---

## Table of contents

1. [What Project CBM does](#what-project-cbm-does)
2. [What you need](#what-you-need)
3. [Download and flash the release image](#download-and-flash-the-release-image)
4. [Important first-boot information](#important-first-boot-information)
5. [First things to do after booting](#first-things-to-do-after-booting)
6. [How the menu works](#how-the-menu-works)
7. [Using the Commodore emulator](#using-the-commodore-emulator)
8. [Project CBM folder layout](#project-cbm-folder-layout)
9. [Included starter content](#included-starter-content)
10. [Main Menu reference](#main-menu-reference)
11. [Machines Menu reference](#machines-menu-reference)
12. [Content Menu reference](#content-menu-reference)
13. [Import Menu reference](#import-menu-reference)
14. [Control Panel reference](#control-panel-reference)
15. [Network Menu reference](#network-menu-reference)
16. [BBS / Modem Menu reference](#bbs--modem-menu-reference)
17. [ROM import reference](#rom-import-reference)
18. [System Menu reference](#system-menu-reference)
19. [Boot Mode Menu reference](#boot-mode-menu-reference)
20. [Adding your own files](#adding-your-own-files)
21. [Using network file sharing](#using-network-file-sharing)
22. [Using SSH](#using-ssh)
23. [Troubleshooting](#troubleshooting)
24. [Security notes](#security-notes)
25. [Legal notes](#legal-notes)

---

## What Project CBM does

Project CBM turns a Raspberry Pi into a small, menu-driven Commodore machine launcher.

It can:

- Boot directly into the Project CBM menu.
- Start several Commodore machines using VICE.
- Optionally boot directly into your favorite saved default machine (as opposed to the Project CBM menu).
- Browse and launch games, demos, music, programs, and ROM-type files (work-in-progress).
- Import files from a USB drive.
- Share the Project CBM folders over your home network using Samba.
- Show network information such as IP address, gateway, DNS, and Samba status.
- Launch Raspberry Pi configuration tools (raspi-config).
- Shut down and reboot safely from the menu.
- Run optional BBS / modem features using TCPser (TCP-to-Serial).
- Displays a splash screen before launching or returning from an emulator.

Project CBM is intended to feel more like a small retro appliance than a normal Linux desktop. The Pi boots, the menu appears, and you choose what you want to do.

---

## What you need

You will need:

- A supported Raspberry Pi for the released Project CBM image (Pi 3 through Pi 5 supported).
- A microSD card.
- A keyboard.
- A display connected by HDMI.
- A power supply appropriate for your Raspberry Pi.
- Optional: Ethernet cable for the easiest first network connection.
- Optional: USB drive for importing games, demos, music, programs, or ROM files (i.e., JiffyDOS).
- Optional: Game controller or joystick, depending on your VICE setup.

A mouse is usually not required for the Project CBM menus.

---

## Download and flash the release image

Before Project CBM can boot, you need to write the release image to a microSD card.

The Project CBM release image is:

```text
pcbm-v1.0.0-rpi3-5.img.xz
```

This file is a complete Raspberry Pi system image. It already includes Raspberry Pi OS Lite, Project CBM, the menu system, VICE, the Project CBM folder layout, and the included starter content.

Important: writing the image will erase the selected microSD card. Make sure you choose the correct card.

### Recommended method: Raspberry Pi Imager

Raspberry Pi Imager is the easiest option for most users.

1. Download `pcbm-v1.0.0-rpi3-5.img.xz` from the Project CBM GitHub Releases page.
2. Install and open Raspberry Pi Imager on your Windows, macOS, or Linux computer.
3. Insert your microSD card into your computer.
4. When asked to choose a Raspberry Pi device, select the Raspberry Pi model you plan to use.
5. When asked to choose an operating system, choose the custom image option, then select `pcbm-v1.0.0-rpi3-5.img.xz`.
6. When asked to choose storage, select your microSD card.
7. If Imager offers extra system customization options, skip them unless the Project CBM release notes specifically tell you to use them. Project CBM is already preconfigured.
8. Write the image and allow Imager to verify it when finished.
9. When Imager says it is done, safely eject the microSD card.
10. Put the microSD card into your Raspberry Pi.
11. Connect HDMI, keyboard, and optionally Ethernet.
12. Power on the Raspberry Pi.

Project CBM should boot directly into its main menu.

### Alternative method: Balena Etcher or another image writer

Balena Etcher and similar tools can also write compressed Raspberry Pi image files.

Use the same basic process:

1. Select `pcbm-v1.0.0-rpi3-5.img.xz` as the image.
2. Select the correct microSD card as the target.
3. Start the write/flash process.
4. Let the tool finish and verify the card if it offers verification.
5. Eject the card, insert it into the Raspberry Pi, and power on.

### Do not copy the file to the SD card

Do not drag `pcbm-v1.0.0-rpi3-5.img.xz` onto a blank SD card like a normal file. That will not make a bootable Project CBM card.

The image must be written with an imaging tool. Think of it as stamping an entire tiny computer world onto the card, not just saving a document to it.

### First boot after imaging

On first boot, connect:

- HDMI display
- USB keyboard
- Power supply
- Optional Ethernet cable

Ethernet is the easiest first network option because Project CBM is set to request an IP address automatically when plugged into a network.

WiFi is intentionally left unconfigured so each user can set their own country, network name, and password after booting.

---

## Important first-boot information

The release image is intended to boot directly into Project CBM.

Default information:

| Item                        | Default                                     |
|-----------------------------|---------------------------------------------|
| Linux user                  | `pi`                                        |
| Default password            | `cbm-ready`                                 |
| Host name                   | `pcbm`                                      |
| Default Project CBM machine | Commodore 64, accurate/recommended emulator |
| Default emulator profile    | `x64sc`                                     |
| Default boot mode           | Project CBM menu                            |
| Project CBM content folder  | `/home/pi/pcbm`                             |
| VICE emulator menu key      | `F10`                                       |
| SSH                         | Enabled by default                          |
| Samba file sharing          | Enabled by default                          |
| TCPSer (BBS / Modem)        | Disabled by default                         |
| WiFi                        | Intentionally left unconfigured             |

Important: change the default password after your first successful boot. Leaving the default password in place is fine for a quick first test, but it should not stay that way on a normal home network.

---

## First things to do after booting

On first boot, Project CBM should appear automatically on the Pi screen.

Recommended first steps:

1. **Confirm the menu appears.**  
   You should see the Project CBM Main Menu.

2. **Change the default password** 
   Go to:  
   `CONTROL` -> `SYSTEM` -> `CONFIG`  
   This opens Raspberry Pi configuration. Use the `1 System Options`  -> `S3 Password` password option to change the password for the `pi` user.

3. **Set your keyboard, locale, and WiFi country if needed.**  
   Go to:  
   `CONTROL` -> `SYSTEM` -> `CONFIG`  
   or  
   `CONTROL` -> `NETWORK` -> `CONFIG`-> `RASPI-CONFIG` 
   and the  `5 Localization Options` menu to set these if needed

4. **Use Ethernet for the simplest first network test.**  
   If an Ethernet cable is plugged in, Project CBM should automatically request an IP address from your router.

5. **Check your network address.**  
   Go to:  
   `CONTROL` -> `NETWORK`  
   The network screen shows the host name, IP address, gateway, DNS server, network status, and Samba status.

6. **Try the starter content.**  
   Go to:  
   `CONTENT` -> choose a category -> choose a file.

   If a file does not launch as expected, set the correct default machine first, then try again.

7. **Remember the VICE menu key.**  
   Project CBM sets the VICE emulator UI key to `F10` instead of the usual `F12`.

---

## How the menu works

Project CBM uses simple keyboard menus.

| Key | What it does |
|---|---|
| Arrow keys | Move through menu choices |
| Enter | Select highlighted item |
| Tab | Move between buttons in dialog boxes |
| Space | Select or unselect items in checklist screens |
| Esc | Go back or cancel |
| F10 | Open the VICE emulator menu while inside an emulator |

Most menus have a `RETURN` option that takes you back to the previous menu.

If you are in a checklist, such as the USB import screen, use **Space** to mark items before pressing **Enter**.

---

## Using the Commodore emulator

Project CBM uses VICE to emulate Commodore machines.

When you launch a machine or a file:

1. Project CBM clears the screen.
2. It may show a Project CBM cover (or splash) image.
3. VICE starts.
4. When you quit VICE, Project CBM returns to the menu.

While inside VICE:

- Press `F10` to open the VICE menu.
- Use the VICE menu to attach disks, change joystick settings, reset the machine, or quit the emulator.
- When you quit the emulator, Project CBM should return to the Project CBM menu.

### Important content-launching note

The Content menu launches files using the **current default machine**.

For example, if the default machine is C64SC and you launch a C128 demo, it may not work correctly. Set the correct default machine first:

`MACHINES` -> `DEFAULT` -> choose the machine you want

Then return to `CONTENT` and launch the file.

That one little detail is the brass key under the mat.

---

## Project CBM folder layout

Project CBM stores user content under:

```text
/home/pi/pcbm
```

Main folders:

```text
/home/pi/pcbm/games
/home/pi/pcbm/demos
/home/pi/pcbm/music
/home/pi/pcbm/programs
/home/pi/pcbm/roms
```

Recommended subfolder examples:

```text
/home/pi/pcbm/games/c64
/home/pi/pcbm/games/c128
/home/pi/pcbm/demos/c64
/home/pi/pcbm/demos/c128
/home/pi/pcbm/music/c64
/home/pi/pcbm/programs/c64
/home/pi/pcbm/roms
```

Project CBM scans folders recursively. That means you can organize content inside subfolders and the menu should still find compatible files.

---

## Included starter content

The starter release is intended to include a small amount of legal starter content so users can try Project CBM immediately.

Included examples may include:

- A few C64 demos.
- A couple of C128 demos (for 80 column mode).
- A couple of freeware C64 games.
- SidWizard 1.8 in the C64 music folder.
- StrikeTerm2014 in the C64 programs folder.

Suggested places to explore:

```text
/home/pi/pcbm/demos
/home/pi/pcbm/games/c64
/home/pi/pcbm/music/c64
/home/pi/pcbm/programs/c64
```

Starter content is there so users are not staring into an empty retro cave with only a blinking cursor for company.

---

## Main Menu reference

The Main Menu is the first menu most users will see.

| Menu item | What it does |
|---|---|
| `RUN` | Starts the saved default Commodore machine immediately. |
| `MACHINES` | Lets you choose a Commodore machine to start, or set the default machine. |
| `CONTENT` | Browses and launches games, demos, music, programs, or ROM files from `/home/pi/pcbm`. |
| `IMPORT` | Imports files or folders from a USB drive into Project CBM content folders. |
| `CONTROL` | Opens settings for network, file sharing, BBS/modem, ROMs, and system options. |
| `FILES` | Opens Midnight Commander, a two-panel file manager. |
| `QUIT` | Exits Project CBM and returns to the Linux command line. |
| `POWER` | Safely shuts down the Raspberry Pi. |
| `REBOOT` | Restarts the Raspberry Pi. |

### RUN

`RUN` starts whatever machine is saved as the default.

The default in this build is:

```text
Commodore 64 (Recommended for games and demos)
```

Technically, that is the VICE `x64sc` emulator.

### FILES

`FILES` opens Midnight Commander. This is a text-based file manager. It is useful for copying, moving, renaming, and inspecting files directly on the Pi.

If you are not comfortable with file managers or Linux paths yet, you can ignore this option and use the USB Import menu or Samba file sharing instead.

### POWER and REBOOT

Always use `POWER` before unplugging the Pi unless the system is completely frozen. Raspberry Pi systems can corrupt SD cards if power is pulled while the card is being written to.

---

## Machines Menu reference

The Machines Menu lets you start a Commodore machine directly or choose which machine Project CBM should use by default.

Path:

```text
Main Menu -> MACHINES
```

| Menu item | What it does |
|---|---|
| `C64` | Starts the Commodore 64 using the faster VICE C64 emulator. Best for slower systems. |
| `C64SC` | Starts the more accurate Commodore 64 emulator. Recommended for games and demos. |
| `SCPU64` | Starts a Commodore 64 with CMD SuperCPU emulation. |
| `C64DTV` | Starts Commodore 64 DTV emulation. |
| `C128` | Starts the Commodore 128 using the 40-column VIC display. |
| `C12880` | Starts the Commodore 128 in 80-column VDC mode. |
| `CBM2` | Starts CBM-II emulation. |
| `CBM5` | Starts CBM-5x0 emulation. |
| `VIC20` | Starts VIC-20 emulation. |
| `PLUS4` | Starts Plus/4 emulation. |
| `PET` | Starts PET emulation. |
| `DEFAULT` | Opens a submenu where you choose the saved default machine. |
| `RETURN` | Returns to the Main Menu. |

### Choosing a default machine

Path:

```text
MACHINES -> DEFAULT
```

The default machine is used by:

- `RUN`
- the optional direct-machine boot mode
- the Content launcher

If you mostly use C64 software, leave this set to `C64SC`.

If you are testing C128 demos, set it to `C128` or `C12880` before launching those files from the Content menu.

---

## Content Menu reference

The Content Menu lets you browse and launch files from Project CBM folders.

Path:

```text
Main Menu -> CONTENT
```

| Menu item | Folder | What it does |
|---|---|---|
| `GAMES` | `/home/pi/pcbm/games` | Browses game files. |
| `DEMOS` | `/home/pi/pcbm/demos` | Browses demo files. |
| `MUSIC` | `/home/pi/pcbm/music` | Browses music and SID-related files. |
| `PROGRAMS` | `/home/pi/pcbm/programs` | Browses utility and application files. |
| `ROMS` | `/home/pi/pcbm/roms` | Browses ROM-type files. See ROM notes below. |
| `RETURN` | none | Returns to the Main Menu. |

Project CBM searches these folders recursively, so machine-specific subfolders are fine.

### Compatible file types

The Content menu looks for these file types:

```text
.d64 .d67 .d71 .d80 .d81 .d82
.g64 .g41 .x64 .p64
.t64 .tap .crt .prg .p00
.sid .mus .bin .rom .reu
```

### How files are launched

When you choose a file, Project CBM launches it using the current default emulator and VICE autostart.

For example:

- C64 game file + C64SC default = usually good.
- C128 80-column demo + C64SC default = probably wrong.
- SID file + C64SC default = often fine, depending on the file and VICE behavior.

If something fails or looks wrong, set the default machine to the correct system and try again.

---

## Import Menu reference

The Import Menu copies content from a USB drive into Project CBM folders.

Path:

```text
Main Menu -> IMPORT
```

| Menu item | What it does |
|---|---|
| `IMPORT` | Scans for a removable USB drive and opens a browser/checklist. |
| `RETURN` | Returns to the Main Menu. |

### How USB import works

1. Put files on a USB drive.
2. Plug the USB drive into the Raspberry Pi.
3. Choose `IMPORT` from the Main Menu.
4. Choose `IMPORT` again in the Project CBM Import screen.
5. Project CBM mounts the first removable USB partition it finds.
6. A checklist-style browser appears.
7. Use **Space** to select files or folders.
8. Press **Enter** or choose OK.
9. Choose the destination: `games`, `demos`, `music`, or `programs`.
10. Project CBM copies the selected files or folders.

### USB browser options

| Option | What it does |
|---|---|
| `ALL` | Imports everything in the current USB folder. |
| `[Parent Directory]` | Moves up one folder. |
| `[Folder] foldername` | Selects a folder. If one folder is selected, Project CBM asks whether to browse into it or import it. |
| `[File] filename` | Selects a file for import. |

### Folder behavior

If you select exactly one folder, Project CBM asks:

| Option | What it does |
|---|---|
| `BROWSE` | Opens that folder so you can look inside. |
| `IMPORT` | Imports the whole folder and its contents. |
| `CANCEL` | Goes back to the USB browser. |

### Import destinations

| Destination | Copies into |
|---|---|
| `games` | `/home/pi/pcbm/games` |
| `demos` | `/home/pi/pcbm/demos` |
| `music` | `/home/pi/pcbm/music` |
| `programs` | `/home/pi/pcbm/programs` |

ROM import is handled separately under:

```text
CONTROL -> ROMS
```

Project CBM also tries to ignore common junk files created by macOS and Windows, such as `.DS_Store`, `._*`, `Thumbs.db`, and similar metadata files.

---

## Control Panel reference

The Control Panel groups the more system-like parts of Project CBM.

Path:

```text
Main Menu -> CONTROL
```

| Menu item | What it does |
|---|---|
| `NETWORK` | Shows network status, tests connectivity, and controls Samba file sharing. |
| `AUDIO` | Intended for audio output selection and testing. See maintainer notes. |
| `BBS` | Controls TCPser for BBS or modem-style connectivity, if installed. |
| `ROMS` | Imports ROM files from USB. See ROM notes. |
| `SYSTEM` | Opens system settings, boot mode, about screen, shutdown, and reboot options. |
| `RETURN` | Returns to the Main Menu. |

The Control Panel also shows useful status information:

- Project CBM version and build.
- Samba status.
- TCPser status.
- Audio mode, if configured.

---

## Network Menu reference

The Network Menu shows current network information and lets you control Samba file sharing.

Path:

```text
Main Menu -> CONTROL -> NETWORK
```

The top of the screen shows:

| Field | Meaning |
|---|---|
| Host name | The Pi name on the network. Default: `pcbm`. |
| IP address | The address assigned by your router. |
| Gateway | Usually your router. |
| DNS Server | The server used to look up internet names. |
| Network | Whether Project CBM appears connected. |
| Samba | Whether Samba file sharing is active. |

Menu options:

| Menu item | What it does |
|---|---|
| `TEST` | Tests gateway, internet, and DNS connectivity. |
| `SAMBAON` | Starts Samba file sharing. |
| `SAMBAOFF` | Stops Samba file sharing. |
| `RESTART` | Restarts the active network stack, if Project CBM can detect it. |
| `CONFIG` | Opens Raspberry Pi configuration. Useful for WiFi, locale, keyboard, and other settings. |
| `RETURN` | Returns to the Control Panel. |

### Network test results

`TEST` checks three things:

| Test | What it means |
|---|---|
| Gateway | Can Project CBM reach your router? |
| Internet | Can Project CBM reach the internet by IP address? |
| DNS | Can Project CBM resolve a name such as `google.com`? |

If gateway works but DNS fails, your Pi may be connected but unable to resolve website names.

### WiFi setup

WiFi is intentionally left unconfigured in the release image.

To configure WiFi:

```text
CONTROL -> NETWORK -> CONFIG
```

or

```text
CONTROL -> SYSTEM -> CONFIG
```

In Raspberry Pi configuration, set the WiFi country first if needed, then configure wireless LAN.

Ethernet is the easiest first connection. If Ethernet is plugged in, Project CBM should automatically request an IP address from your router.

---

## BBS / Modem Menu reference

The BBS / Modem Menu controls TCPser.

Path:

```text
Main Menu -> CONTROL -> BBS
```

TCPser is a tool that can act like a bridge between old modem-style software and modern network connections. In plain English: it can help terminal programs behave as if they are using a modem, while actually connecting over a network.

Menu options:

| Menu item | What it does |
|---|---|
| `START` | Starts the TCPser service. |
| `STOP` | Stops the TCPser service. |
| `RESTART` | Restarts the TCPser service. |
| `STATUS` | Shows TCPser service status. |
| `RETURN` | Returns to the Control Panel. |

This is an advanced feature. Most users can ignore it unless they want to use terminal software, modem-style connections, or BBS-related features.

The included starter program StrikeTerm2014 is a good place for adventurous users to begin exploring this world.

---

## ROM import reference

Path:

```text
Main Menu -> CONTROL -> ROMS
```

In this release, this option starts a ROM import process directly.

It searches a USB drive for:

```text
.bin
.rom
```

Then it copies selected ROM files into:

```text
/home/pi/pcbm/roms
```

Use this for custom ROM files that you legally own, such as a licensed JiffyDOS ROM.

Important: the ROM import option copies ROM files into place, but it does not currently provide a full ROM manager, ROM viewer, or JiffyDOS activation menu.

---

## System Menu reference

The System Menu contains system settings, Project CBM information, boot behavior, and safe power options.

Path:

```text
Main Menu -> CONTROL -> SYSTEM
```

| Menu item | What it does |
|---|---|
| `CONFIG` | Opens Raspberry Pi configuration. |
| `BOOTMODE` | Chooses whether Project CBM starts at the menu or directly in the default machine. |
| `SHOW` | Shows Project CBM version, build, credits, network info, default machine, and active custom ROM. |
| `POWER` | Safely shuts down the Pi. |
| `REBOOT` | Restarts the Pi. |
| `RELEASE` | Reserved for maintainer/release-preparation use. Most users can ignore this option. |
| `RETURN` | Returns to the Control Panel. |

### CONFIG

`CONFIG` launches Raspberry Pi configuration.

Common things to set here:

- Password
- Keyboard layout
- Locale
- Time zone
- WiFi country
- Wireless LAN
- Hostname, if you want to rename the Pi

### SHOW

`SHOW` displays useful information:

- Project CBM name
- Version
- Build
- Author
- Repository
- Host name
- IP address
- Gateway
- Default machine
- Boot mode
- Active custom ROM
- Credits

### POWER

Use this before unplugging the Pi.

### REBOOT

Use this after changing certain settings, or if something needs a clean restart.

---

## Boot Mode Menu reference

The Boot Mode Menu controls what happens when Project CBM starts on the main console.

Path:

```text
Main Menu -> CONTROL -> SYSTEM -> BOOTMODE
```

| Menu item | What it does |
|---|---|
| `MENU` | Project CBM boots to the Main Menu. This is the recommended default. |
| `MACHINE` | Project CBM boots directly into the saved default machine. When VICE exits, it returns to the menu. |
| `STATUS` | Shows current boot mode, raw config value, default machine, and config file path. |
| `RETURN` | Returns to the System Menu. |

### MENU mode

This is best for most users.

The Pi boots to:

```text
Project CBM Main Menu
```

### MACHINE mode

This is best if you want the Pi to behave like a dedicated Commodore machine.

The Pi boots directly into the saved default machine. For example, if the default machine is C64SC, the Pi boots straight into a Commodore 64 emulator.

When you quit the emulator, Project CBM returns to the Main Menu.

### Important relationship between Default Machine and Boot Mode

These are separate settings:

| Setting | What it controls |
|---|---|
| Default Machine | Which Commodore machine is used by `RUN`, Content launches, and Machine Boot Mode. |
| Boot Mode | Whether Project CBM starts at the menu or starts the default machine automatically. |

To boot directly into a C128:

1. Go to `MACHINES` -> `DEFAULT` -> choose `C128`.
2. Go to `CONTROL` -> `SYSTEM` -> `BOOTMODE` -> choose `MACHINE`.
3. Reboot.

---

## Adding your own files

You can add files in three main ways:

1. USB Import menu
2. Samba network file sharing
3. Midnight Commander file manager

For most users, USB Import and Samba are easiest.

### Recommended file organization

Use simple folders by machine:

```text
/home/pi/pcbm/games/c64
/home/pi/pcbm/games/c128
/home/pi/pcbm/demos/c64
/home/pi/pcbm/demos/c128
/home/pi/pcbm/music/c64
/home/pi/pcbm/programs/c64
```

Project CBM scans recursively, so you can create deeper folders if you want.

### Use clear filenames

Readable names make the Content browser much easier to use.

Good:

```text
Sam_Journey.d64
C128-Demo-Example.d71
SidWizard1.8.prg
```

Less helpful:

```text
disk1.d64
new.prg
stuff.tap
```

---

## Using network file sharing

Samba file sharing lets you copy files to Project CBM from another computer on your home network.

Default values:

| Item | Value |
|---|---|
| Host name | `pcbm` |
| Samba share name | `Project CBM` |
| Shared folder | `/home/pi/pcbm` |
| Username | `pi` |
| Password | `cbm-ready` until you change it |

After you change the Pi password, use the new password for Samba too.

### From macOS

In Finder:

1. Choose **Go** -> **Connect to Server**.
2. Try:

```text
smb://pcbm.local/Project%20CBM
```

If that does not work, use the IP address shown in the Network menu:

```text
smb://192.168.x.x/Project%20CBM
```

3. Log in as user `pi`.

### From Windows

In File Explorer's address bar, try:

```text
\\pcbm.local\Project CBM
```

If that does not work, use the IP address shown in the Network menu:

```text
\\192.168.x.x\Project CBM
```

Log in as user `pi`.

### From Linux

In your file manager, try:

```text
smb://pcbm.local/Project%20CBM
```

or use the IP address:

```text
smb://192.168.x.x/Project%20CBM
```

---

## Using SSH

SSH lets you log into the Pi command line from another computer.

Default SSH example:

```bash
ssh pi@pcbm.local
```

If the host name does not resolve, use the IP address shown in the Network menu:

```bash
ssh pi@192.168.x.x
```

Default password:

```text
cbm-ready
```

Change that password after first boot.

Most users do not need SSH for normal Project CBM use. It is mainly useful for troubleshooting, updates, and advanced customization.

---

## Troubleshooting

### I do not see the Project CBM menu

Try these:

1. Make sure the Pi has booted fully, it may take a moment to display.
2. Make sure the keyboard and display are connected.
3. Press Enter once in case the screen is waiting.
4. If you are at the Linux command line, type:

```bash
pcbm-menu
```

or:

```bash
/usr/local/bin/pcbm-menu
```

### I launched a C128 file and it does not work

The Content menu uses the current default machine. Set the correct default first:

```text
MACHINES -> DEFAULT -> C128
```

or:

```text
MACHINES -> DEFAULT -> C12880
```

Then launch the file again.

### I cannot find the Pi on the network

Try:

1. Plug in Ethernet.
2. Go to `CONTROL` -> `NETWORK`.
3. Look for the IP address.
4. Use the IP address instead of the host name.
5. Run `TEST` in the Network Menu.
6. Restart the Pi.

### Samba file sharing does not appear

Try:

```text
CONTROL -> NETWORK -> SAMBAON
```

If that does not work, use the IP address directly.

Also remember that the actual share name in the attached Samba config is:

```text
Project CBM
```

### WiFi is not working

WiFi was intentionally left unconfigured.

Go to:

```text
CONTROL -> NETWORK -> CONFIG
```

Set your WiFi country, then configure wireless LAN.

### I am asked for a sudo password

Some Project CBM menu functions may request administrator permission for actions such as shutdown, reboot, Samba control, mounting USB drives, or saving configuration files.

If you are asked for a password, enter the current password for the `pi` user.

### USB Import says no USB drive was found

Try:

1. Use a normal USB flash drive.
2. Make sure it has a readable partition.
3. Try FAT32 or exFAT if your current format is not recognized.
4. Unplug and replug the drive.
5. Restart Project CBM or reboot the Pi.

### Content does not show in the menu

Check:

1. Is the file in the right folder under `/home/pi/pcbm`?
2. Is it one of the supported file types?
3. Did it copy into a subfolder? That is okay, but check the folder path.
4. Did Samba or USB import skip it because it was hidden or a metadata file?

### VICE opens, but I cannot find the emulator menu

Press:

```text
F10
```

Project CBM sets the VICE UI key to F10.

### I want to return to the Project CBM menu from an emulator

Press `F10`, open the VICE menu, and choose the quit option. When VICE exits, Project CBM should return to its menu.

### I accidentally exited to the Linux command line

Type:

```bash
pcbm-menu
```

or reboot:

```bash
sudo reboot
```

---

## Security notes

Project CBM is meant for trusted home networks.

Do:

- Change the default password.
- Keep SSH and Samba on your private network only.
- Do not expose SSH or Samba directly to the internet.
- Use `POWER` before unplugging the Pi.
- Keep a backup of important content.

Do not:

- Leave the default password in place long-term.
- Put the Pi on public WiFi with SSH and Samba enabled unless you understand the risk.
- Forward router ports to SSH or Samba.

---

## Legal notes

Project CBM does not include or distribute copyrighted ROMs, commercial software, disk images, or game collections.

Users are responsible for making sure they have the legal right to use any ROMs, games, demos, music, programs, or disk images they add.

Freeware, public domain software, homebrew projects, and user-owned backups are the safest places to begin.

VICE is developed by the VICE Team. Raspberry Pi OS is developed by the Raspberry Pi OS developers. Commodore names and software remain owned by their respective rights holders.

---