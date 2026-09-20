# Accounts and installed system layout

[Documentation index](../README.md) · [User Manual](user-guide.md) · [Developer guide](development.md)

The normal account is **pcbm**, UID 1000, home **/home/pcbm**. Menu, VICE, Covers, FILES,
SSH/SFTP and library ownership all use this account. **Owner/Administrator** describes
your role; **projectcbm** is the default Computer Name. Those are not three user accounts.

## Passwords and access

First boot asks for your administrator password, not a username choice. It unlocks the
pcbm account for authenticated remote/general administration. Local consoles use autologin
as pcbm; they do not grant an unrestricted root shell. Root's password is locked and
root SSH login is disabled. General `sudo` uses the first-boot administrator password.
Advanced administrator/raspi-config entry deliberately asks again even if a prior
sudo session was cached. Ordinary appliance actions use limited helpers after setup.

File Sharing authenticates **pcbm with its separate sharing password**. Samba stores
that credential independently; it is not automatically the administrator password.
The share exposes only the library. SFTP starts in your home, so open `content`.
See [connection examples](networking.md) for everyday use.

The user is created through pi-gen's `FIRST_USER_NAME`. Product's installer writes
getty/profile policy and adds normal administrator and fixed-operation group membership.
`configuration-policy.json` names both owner/appliance roles as pcbm. Changing those
contracts requires more than renaming a home directory.

## User files

| Path | What is here? | Should users edit it? |
| --- | --- | --- |
| `/home/pcbm/content` | Main library; File Sharing exports this directory | Yes; use CONTENT/FILES/import or another computer |
| `/home/pcbm/content/games/c64/Imported` | Example C64 games import destination, with source subfolders | Yes; organize copies here |
| `/home/pcbm/content/music/c64/Imported` | All imported SID files | Yes; storage does not imply a SID player |
| `/home/pcbm/content/saves` and `/home/pcbm/content/screenshots` | Suggested storage areas | Yes; choose them explicitly in applications where needed |
| `/home/pcbm/.config/project-cbm/preferences.json` | Default machine and boot preference | Usually through Menu or pcbm-preferences; schema/permissions matter |
| `/home/pcbm/.config/vice/sdl-vicerc` | Saved VICE resources | Prefer VICE's settings UI and save action |
| `/home/pcbm/.local/share/vice` | VICE user data/keymap lookup | Advanced personal data; back up if used |
| `/home/pcbm/.local/state/vice` | VICE user state/log location | Inspect selectively; not general content |
| `/home/pcbm/.config/pcbm/audio.conf` | Persisted HDMI/audio selection | Prefer Audio output and test |
| `/home/pcbm/.asoundrc` | Generated ALSA default device | Advanced; audio selection may regenerate it |
| `/home/pcbm/.local/state/project-cbm/boot` | Numeric boot phase traces | Read for diagnosis; do not treat dispatch time as physical readiness |
| `/home/pcbm/.local/state/project-cbm/diagnostics` | Launch, Cover, terminal and VICE diagnostic records | Read selectively; review privacy before sharing |

A backup of the SMB share does not include these preferences. See [backup](recovery.md).
Personal files outside `content` remain yours but are not scanned by CONTENT.

## Installed programs, assets and system configuration

| Path | What is here? | Should users edit it? |
| --- | --- | --- |
| `/usr/bin/pcbm-*` | Menu commands and Runtime entry points | Modify source/package rather than installed code |
| `/usr/bin/x64sc` and other VICE executables | Commodore emulators | Rebuild/select packages for code changes |
| `/usr/share/project-cbm/runtime` | Product Python code, data and command implementations | Source/package change |
| `/usr/share/project-cbm/runtime/data/profiles.json` | Machine/profile registry | Source/package change; customizers must preserve schema |
| `/usr/share/project-cbm/vice-defaults.ini` | Initial VICE template | Image build input; saved user settings are separate |
| `/usr/share/project-cbm/identity.json` | Installed version/component/build record | Read-only reference; do not relabel an image by editing it |
| `/usr/share/project-cbm/owned-paths.txt` | Integration-managed file list | Read-only engineering reference |
| `/usr/share/project-cbm/applications` | Optional application templates/manifests | Work on library copies instead |
| `/usr/share/project-cbm-menu/covers` | Primary artwork and machine Covers | See source-based customization |
| `/usr/share/project-cbm-menu` | Shared shell UI/setup libraries | Source/package change |
| `/usr/libexec/project-cbm-menu` | Status/formatting helpers and Cover renderer | Source/package change |
| `/usr/libexec/project-cbm` | Console/first-boot/lifecycle integration | Advanced source change; affects safe return |
| `/usr/libexec/pcbm-config-root` and `/usr/libexec/pcbm-import-root` | Fixed privileged operations | Do not broaden permissions to repair UI problems |
| `/usr/libexec/project-cbm-vice/drm-state` | Read-only display-state helper | Engineering tool |
| `/etc/project-cbm/configuration-policy.json` | Setup/account/action policy | Advanced; not ordinary preferences |
| `/etc/project-cbm/modem.json` | Local modem port/baud | Prefer BBS / Modem settings |
| `/etc/pcbm` | Version and older boot/default import configuration | Prefer current preferences; inspect migration only deliberately |
| `/etc/hostname`, `/etc/hosts` | Computer Name and local mapping | Prefer Network → Computer Name |
| `/etc/NetworkManager/system-connections` | Protected connection profiles | Advanced and private; never publish credentials |
| `/etc/ssh/sshd_config.d/20-project-cbm.conf` | SSH access policy | Advanced administrator changes |
| `/etc/samba/smb.conf` | Project CBM content share | Prefer service controls; advanced custom exports are your responsibility |
| `/etc/sudoers.d/pcbm-operations`, `/etc/sudoers.d/pcbm-power` | Limited appliance/power permissions | Advanced security boundary; keep general administration authenticated |
| `/etc/systemd/system/getty@tty1.service.d/autologin.conf` | Main console login override | Core session behavior; change carefully |
| `/etc/profile.d/pcbm-console.sh` | Starts appliance from the intended session | Core session behavior |
| `/usr/lib/systemd/system/pcbm-first-boot.service` | Initial filesystem/system preparation | Core image integration |
| `/usr/lib/systemd/system/tcpser.service` | Modem bridge unit | Prefer service controls |
| `/var/lib/project-cbm/setup` | First-boot state | Do not restore blindly over a fresh image |
| `/var/lib/project-cbm/first-boot` | Filesystem/system initialization markers | Do not fabricate completed setup |
| `/var/lib/project-cbm/sharing-status.json` | Sharing username/password-set status, not the password | System-managed |
| `/run/project-cbm/import` | Temporary read-only import mount/work state | Do not manually change during import |
| `/usr/share/doc/project-cbm-runtime/release` | Guides shipped with that Runtime package | May predate newer repository documentation |
| `/boot/firmware/cmdline.txt` | Kernel command line, including quiet options | Advanced; keep one line and back up first |
| `/etc/initramfs-tools/hooks/pcbm-quiet-fsck` | Image's successful-fsck output hook | Build integration; failures/verbose path retained |

## System services

NetworkManager manages connections; ssh serves remote terminals, smbd serves File
Sharing, avahi-daemon supplies local discovery and tcpser supplies the modem bridge.
`pcbm-info` reports their observed state for Menu. Linux getty/login/PAM owns tty sessions;
the shared launch supervisor handles Cover → VICE → return. The first-boot service and
wizard have separate system-preparation and user-choice responsibilities.

Sensitive credential databases and connection files are not support attachments or
build inputs. [Security](../security.md) and [configuration contracts](../runtime/configuration-contract.md)
provide the precise developer rules behind these paths.
