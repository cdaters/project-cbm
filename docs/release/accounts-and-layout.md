# Accounts, configuration and installed files

Project CBM uses one normal appliance account: **`pcbm`, UID 1000, home
`/home/pcbm`**. Menu, Covers, VICE, Midnight Commander, SSH/SFTP and imported files
all use this identity. **Owner / Administrator describes your role; `projectcbm`
is the default Computer Name.** With Remote Access and Network Discovery enabled,
connect using `ssh pcbm@projectcbm.local`.

## Accounts and passwords

| Account | Purpose | Authentication |
| --- | --- | --- |
| `pcbm`, UID 1000 | Local appliance, content, remote login and owner administration | Local console autologin; first-boot password for SSH and general `sudo` |
| `root` | System services and fixed privileged helpers | Locked password; SSH root login disabled |

First boot asks you to choose a password, without an extra username decision.
There is no factory password. The account is locked until you set its password;
optional network services remain off until enabled. Local tty1/tty2 access remains
an ordinary getty/login/PAM session. Autologin gives local access as `pcbm`, not root.
Advanced Terminal opens your normal shell; Advanced Owner Administration and vendor
configuration require the owner password through `sudo -k`, even if a previous
sudo authentication was cached.

File Sharing uses **username `pcbm` and a separate File Sharing password**, because
Samba maintains a separate credential database. Both passwords are masked when typed.
They travel through protected standard input, never command arguments, status text,
logs or diagnostics. The share exports only `/home/pcbm/content`, not your entire
home. SSH/SFTP starts in `/home/pcbm`: open its clearly named `content` folder to add
files for CONTENT and FILES. No account switch or second password is needed to read
your own launch diagnostics.

The factory creates `pcbm` through pi-gen's `FIRST_USER_NAME`; UID/home/shell and
sudo-group membership are checked by `runtime/project_cbm/config_backend.py`.
`tools/install_poc_stage.py` installs the root-owned account/readiness policy,
getty drop-ins, service definitions and filesystem ownership. Policy retains both
`owner_user` and `appliance_user` roles with the same value, `pcbm`.
`pcbm-info` supplies the username shown in connection help. Samba authenticates
and writes as `pcbm`; no forced switch to another user's identity is needed.

The `pcbm-operators` group permits only fixed, validated appliance operations.
`/etc/sudoers.d/pcbm-operations` does not grant arbitrary editors, shell commands or
mount commands. Debian's ordinary `%sudo` policy supplies password-authenticated
administration. Existing credential readiness, atomic writes and service opt-in
remain in force.

### Moving from an earlier image

RC2 is a fresh-image account model, not an in-place rename of a running RC1 card.
Back up user content and preferences before flashing. Earlier `pi`-based libraries
at `/home/pi/pcbm` map to `/home/pcbm/content`; preserve the existing category/machine
folders beneath them. Restore through File Sharing as `pcbm`, or copy your selected
files as `pcbm`, so ownership matches the new runtime. Review conflicts and keep
both copies until verified. Do not restore old `/etc/passwd`, `/etc/shadow`, sudoers,
Samba databases, host keys or setup completion state. Never move or alter an older
qualification card or recovery checkpoint in order to migrate it.

The [content guide](content.md) defines the type-first hierarchy. Files elsewhere
in your home remain ordinary personal files, but the appliance scans the `content`
folder. VICE starts there; saved emulator browsing choices remain yours.

## Installed layout

| Path | What it contains / who owns it |
| --- | --- |
| `/home/pcbm/content/{games,demos,music,programs,roms,screenshots,saves}` | User content; locally usable and shared through File Sharing |
| `/home/pcbm/.config/project-cbm/preferences.json` | Validated appliance preferences; user-owned |
| `/home/pcbm/.config/vice/sdl-vicerc` | Saved VICE resources, initially seeded only if absent |
| `/home/pcbm/.local/share/vice` | VICE user data/keymap lookup location |
| `/home/pcbm/.local/state/vice` | VICE user state/log location |
| `/home/pcbm/.local/state/project-cbm/diagnostics` | Bounded private engineering launch/terminal/Cover/VICE evidence |
| `/home/pcbm` | One appliance/owner home; its `content` child is the File Sharing export |
| `/home/pcbm/.local/state/project-cbm/boot` | Numeric console/Menu startup phase timestamps; no input or passwords |
| `/etc/project-cbm/configuration-policy.json` | Root-owned activation/readiness and account policy |
| `/etc/project-cbm/modem.json` | Validated local modem port/baud settings |
| `/etc/pcbm` | Product version and legacy boot/default-machine import files |
| `/etc/hostname`, `/etc/hosts` | Computer Name and local hostname mapping |
| `/etc/NetworkManager` | NetworkManager configuration and protected connection profiles |
| `/etc/ssh/sshd_config.d/20-project-cbm.conf` | Owner-only SSH access and root-login exclusion |
| `/etc/samba/smb.conf` | Authenticated `Project CBM` content share |
| `/var/lib/project-cbm/setup` | Private first-boot state and safe setup-status projection |
| `/var/lib/project-cbm/first-boot` | Filesystem expansion/initialization state |
| `/var/lib/project-cbm/sharing-status.json` | Username/password-set indicator, never the password |
| `/usr/bin/pcbm-*` | Menu commands and Runtime entry points |
| `/usr/share/project-cbm/runtime` | Product Python runtime and command implementations |
| `/usr/share/project-cbm/runtime/data/profiles.json` | Installed machine/profile registry |
| `/usr/share/project-cbm/identity.json` | Minimal offline-readable candidate identity |
| `/usr/share/project-cbm/vice-defaults.ini` | Image's initial VICE settings template |
| `/usr/libexec/project-cbm` | Image integration, first boot and launch supervisor |
| `/usr/libexec/project-cbm-menu` | Menu presentation helpers and Cover renderer |
| `/usr/libexec/project-cbm-vice/drm-state` | Unprivileged engineering display-state reporter |
| `/usr/share/project-cbm/applications` | Retained application templates/manifests |
| `/usr/share/doc/project-cbm-runtime/release` | Installed copies of these practical guides |
| `/run/project-cbm/import` | Temporary supervised USB import mount state |

Use the [configuration contract](../runtime/configuration-contract.md) for exact
schemas and write rules. Sensitive stores include `/etc/shadow`, NetworkManager keyfiles
and Samba credential databases. They belong in protected system storage, not support
reports, Git, screenshots or build inputs.

## Boot and session ownership

The image uses Linux console getty, login and PAM. A tty1 getty drop-in logs in the
pcbm appliance account and its profile enters `pcbm-console-session`. The
session runs incomplete first boot before starting Menu or the saved emulator boot
preference. There is one direct-boot launch attempt; failures return to the front panel.
Menu and VICE remain ordinary user processes in that session. The shared launcher
captures terminal state before Cover, supervises/reaps the renderer, restores state,
runs VICE, and restores/verifies again before returning. This is why display/input
changes require repeated physical launch/quit testing, not merely a successful build.

`pcbm-first-boot.service` owns root-filesystem growth. The retryable setup wizard owns
region, password and network choices. The stage excludes competing cloud-init setup
and removes development tools from the final filesystem. Units/configuration are
installed by the stage from `build/pigen/stage-cbm/files` and Runtime policy templates.

## Network and service configuration

NetworkManager owns connection state. Wi-Fi setup waits for readiness and completed
scans with bounded working feedback. Region and regulatory-domain setup precede it.
Optional SSH, Samba, Avahi discovery and TCPser services start disabled; turning on a
feature changes saved intent and then observes actual service/listener state. `pcbm-info`
is the read-only structured authority for UI state, addresses and connection examples.
An enabled preference alone is not enough to report On. Starting/Pending, Unavailable
and Failed are meaningful states, not variants of On.

Avahi provides mDNS name resolution and local service discovery; Samba advertises its
SMB service through its Avahi integration. Direct macOS SMB URLs and Windows UNC paths
remain available if browsing is inconsistent. No extra Windows discovery daemon is
installed solely to populate Explorer. TCPser is a local emulator modem endpoint,
separately enabled; its default listener is loopback. See [networking](networking.md)
for user workflows and [security](../security.md) for the exact boundaries.
