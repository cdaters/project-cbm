# Configure Project CBM

Open **CONTROL** from Main Menu, or run `pcbm-config` in a terminal. Use arrow
keys and Enter; Escape or Back returns one level. No mouse is required.

**Engineering-candidate guide:** the configuration source and native Linux staging
are implemented. Physical behavior is qualified only against a specific frozen image.
POC1–3 are unchanged; POC4 attempt #2 is retained pre-Cover evidence and should not be
physically tested. Use the latest authorized exact-hash procedure in CURRENT-STATE.
Do not install individual scripts onto a frozen qualification image.

## Find a setting

| Area | What it does |
| --- | --- |
| Machine and Startup | Choose your default Commodore machine; choose Menu or direct-emulator startup. |
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
- **Boot preference:** Menu or Default emulator is saved as user intent and applied
  at the next login/boot after setup. Direct startup makes one emulator launch attempt;
  exit or failure returns to Menu rather than trapping the owner in repeated launches.
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

In the activated engineering candidate, no Ethernet cable is required for Wi-Fi:

1. If you previously chose Stay Offline, choose Network → Enable normal networking.
   First boot's Configure Wi-Fi choice already enables networking.
2. Set Network → Wi-Fi country to the country where this Pi is used; confirm radio enablement.
3. Choose Nearby Wi-Fi networks, select your WPA-personal SSID, and enter its password.
   A hidden network can use Join Wi-Fi by name. No Internet access is needed for setup.
4. Review Network → Status. A failed attempt may have saved the connection; inspect
   status before retrying. Disconnect and Forget affect the Project CBM-managed profile.

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
  when the service is ready. The share is the normal `/home/pi/pcbm` content
  tree, with no guest access. The file-sharing account is `pi`. Changing the Unix or
  owner password does **not** change Samba's password, or vice versa.
- **Remote Shell (SSH):** enable only after first boot has initialized a unique
  owner account and fresh SSH host keys. Use that owner account for administration.
- **BBS / Modem:** save the local IP232 port and supported baud, then deliberately
  enable TCPser. Saving alone does not start it. Its bridge listeners bind to loopback;
  configure the compatible VICE serial/terminal driver for the intended BBS test.
  Incoming public BBS hosting is outside this adapter. Actual connectivity is a
  separate qualification test, not established by enabling the service.
- **Local name discovery:** optional mDNS through Avahi, separately enabled. It is
  not a prerequisite for offline use or ordinary numeric-address networking.

Services remain unqualified on hardware in this source pass.

## Content, backup and a terminal

Use Main Menu **CONTENT**, **FILES** and **IMPORT** for content work. Configuration
explains locations and capacity instead of duplicating browsers. IMPORT offers eligible
unmounted USB FAT/exFAT/ext4 partitions, mounts read-only with restricted flags, and
copies supported regular files as the appliance user into validated content folders.
It excludes the running system disk, symlinks and overwriting existing files. Source
cleanup and results are reported; failed unmount requires diagnostics before removal.

See [content locations and reference-media rights](reference-content.md) and
[optional applications and provenance](optional-applications.md) for the bounded
application integration planned for a later candidate.

Keep an external backup of content, user preferences and VICE configuration. For a
major/base upgrade, back up → flash a fresh image → selectively restore and validate.
Do not restore old machine identity, SSH keys or entire system configuration wholesale.

Advanced → Terminal authenticates into the separately initialized `owner` account.
Type `exit` to return. Use ordinary authenticated `sudo`, `apt`/`dpkg`, `systemctl`,
boot configuration and Linux administration there. Main Menu has no confusing QUIT.
Advanced → Authenticated raspi-config uses that account and sudo authentication; it
may ask for the password twice. There is no universal password or unrestricted
passwordless root shell. Complete first-boot owner initialization before these paths.

**Advanced administration may alter or break the qualified Project CBM configuration.
Recovery may require restoring configuration or reflashing the Project CBM image.**

For support, use System Information or [pcbm-info](pcbm-info.md). Engineering
Diagnostics remains separate and is available only when installed. Do not send Wi-Fi
passwords, private keys or complete system configuration files with a support report.

## Standard utilities in the next engineering candidate

Main Menu **FILES** opens Midnight Commander as the normal Project CBM user. Exit
with F10 (or its Quit action) to return. Root file administration belongs in the
separate authenticated Advanced → Terminal session when you deliberately need it.

Picture, Sound and Controllers → **Advanced Mixer (ALSA)** opens standard alsamixer
without sudo. F6 chooses a sound card; Escape exits. Controls depend on hardware;
some digital outputs have no hardware mixer controls. Project CBM does not run a
global alsactl store afterward or promise every mixer adjustment survives reboot.
Normal output selection and VICE audio behavior remain unchanged.

IMPORT reports the selected category's `/home/pi/pcbm/<category>/Imported` folder;
SID files always go into `music/Imported`. Use CONTENT afterward. SID import is not
PSID/RSID playback: unsupported generic SID autostart remains refused.
