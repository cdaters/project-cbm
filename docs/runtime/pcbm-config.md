# Configure Project CBM

Open **CONTROL** from Main Menu, or run `pcbm-config` in a terminal. Use arrow
keys and Enter; Escape or Back returns one level. No mouse is required.

**Source checkpoint, not an image update:** this interface has fixture coverage,
not physical qualification. POC1–3 are unchanged. Settings that need first-boot
accounts, installed helpers or prepared services report **Pending runtime
activation** until a later candidate supplies them. Do not install these scripts
piecemeal onto a frozen qualification image.

## Find a setting

| Area | What it does |
| --- | --- |
| Machine and Startup | Choose your default Commodore machine; save a future boot preference. |
| Picture, Sound and Controllers | Choose/test audio output; find VICE picture, keyboard and joystick settings. |
| Language, Keyboard and Region | System locale, console keyboard layout and timezone. |
| Network | Status, hostname, Wi-Fi country/enrollment, enable networking or stay offline. |
| Services | File Sharing, Remote Shell (SSH), BBS / Modem and local name discovery. |
| Content and Storage | Capacity, content locations and backup/restore guidance. |
| System Information | Concise product, hardware and current-state information from pcbm-info. |
| About Project CBM | Description, credits, licenses and project/support links. |
| Advanced | Terminal, authenticated owner shell/raspi-config, diagnostics and administration guidance. |

System Information and About scroll on smaller terminals. The interface requires
at least 40 columns by 12 rows; 80×24 is the normal console target.

## Everyday choices

- **Default machine:** Machine and Startup → Choose default. This is the machine
  RUN starts; it does not convert or move your content. Selection belongs to your
  user account and requires no sudo. [Preference migration](information-and-machines.md)
  preserves valid existing choices.
- **Boot preference:** Menu or Default emulator is saved as user intent. Current
  engineering sessions still start at Menu. Applying this preference awaits the
  next session/first-boot integration; it is not effective boot state yet.
- **Audio:** choose automatic detection or an available HDMI output, then test it.
  VICE-specific picture/input preferences remain in VICE via F10. Project CBM's
  initial true-aspect defaults preserve the emulated geometry, including unused
  side areas on a widescreen display. Saved VICE preferences remain yours.
- **Region:** use an installed UTF-8 locale such as `en_US.UTF-8`, a keyboard layout
  such as `us` or `gb`, and a timezone such as `America/Phoenix`. Locale affects new
  sessions; translations of Project CBM menus are not supplied yet. Keyboard layout
  is saved for the next reboot. Unusual variants remain an Advanced setting.

## Offline or connected

Project CBM does not require a network. Network → Stay offline disconnects
NetworkManager connections, including Ethernet; it can terminate remote sessions.
It is not a claim of radio isolation or a firewall. Keeping networking disabled
never prevents local emulation.

Once runtime activation is complete, to use Wi-Fi:

1. Set Network → Wi-Fi country to the country where the Pi is actually used.
   This Raspberry Pi operation also enables the radio; the screen asks first.
2. Choose Join Wi-Fi, enter the exact network name and WPA personal password,
   then confirm. The password is hidden and is not included in Project CBM reports.
3. Review Network → Status. A failed attempt may have saved the connection;
   inspect status before retrying.

The first interface manages one Project CBM WPA personal connection. It accepts
8–63 ASCII password characters. Enterprise/open networks, static addresses and
unusual configurations use authenticated owner administration with standard
NetworkManager tools. Existing owner-managed connections are not deleted.
Network status does not require online access. Hostname is a short lowercase name,
for example `project-cbm`; full DNS administration belongs in Advanced.

## Optional services

Nothing is enabled simply by opening its settings. Enable/Disable asks for
confirmation and never bypasses engineering-image masks.

- **File Sharing:** set a separate Samba password, then deliberately enable sharing
  when the service is ready. The planned share is the normal `/home/pi/pcbm` content
  tree, with no guest access. The file-sharing account is `pi`. Changing the Unix or
  owner password does **not** change Samba's password, or vice versa.
- **Remote Shell (SSH):** enable only after first boot has initialized a unique
  owner account and fresh SSH host keys. Use that owner account for administration.
- **BBS / Modem:** typed port/speed settings can be saved after system initialization.
  They remain pending until a safe TCPser launch adapter and listener policy are
  integrated. Saving does not start TCPser or rewrite its historical command line.
- **Local name discovery:** optional mDNS through Avahi, separately enabled. It is
  not a prerequisite for offline use or ordinary numeric-address networking.

Services remain unqualified on hardware in this source pass.

## Content, backup and a terminal

Use Main Menu **CONTENT**, **FILES** and **IMPORT** for content work. Configuration
explains locations and capacity instead of duplicating browsers. Safe automatic USB
import/ROM copying awaits a constrained storage broker; the old generic passwordless
mount path has been retired. No removable device is mounted by this source interface.

See [content locations and reference-media rights](reference-content.md) and
[SID-Wizard / owner-supplied StrikeTerm](optional-applications.md) for the bounded
application integration planned for a later candidate.

Keep an external backup of content, user preferences and VICE configuration. For a
major/base upgrade, back up → flash a fresh image → selectively restore and validate.
Do not restore old machine identity, SSH keys or entire system configuration wholesale.

Advanced → Terminal opens an ordinary unprivileged shell. Type `exit` to return to
configuration. Main Menu no longer offers QUIT that immediately restarts the Menu.

Advanced → Authenticated owner shell uses your separately initialized owner account.
There you can use ordinary `sudo`, `apt`/`dpkg`, `systemctl`, boot configuration and
Linux administration. Advanced → Authenticated raspi-config uses that account and
sudo authentication; it may ask for your password twice. No universal password or
unrestricted passwordless root shell is supplied. Until owner initialization exists,
these entries explain the pending requirement; an existing authenticated Linux login
remains usable independently.

**Advanced administration may alter or break the qualified Project CBM configuration.
Recovery may require restoring configuration or reflashing the Project CBM image.**

For support, use System Information or [pcbm-info](pcbm-info.md). Engineering
Diagnostics remains separate and is available only when installed. Do not send Wi-Fi
passwords, private keys or complete system configuration files with a support report.
