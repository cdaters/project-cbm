# Accounts, configuration and installed files

Project CBM separates the person who administers the appliance from the account that
runs its front panel. **Owner / Administrator is a role. `pcbm` is the default login
name. `projectcbm` is the default Computer Name.** The usual remote command is
`ssh pcbm@projectcbm.local` when Network Discovery and Remote Access are enabled.

## Accounts and passwords

| Account | Purpose | Home | Authentication |
| --- | --- | --- | --- |
| `pi`, UID 1000 | Local Menu, Covers, VICE and shared content | `/home/pi` | Console autologin; Unix password locked; no general passwordless administration |
| `pcbm`, UID 1001 | Owner login and administration | `/home/pcbm` | Password chosen at first boot; normal authenticated `sudo` membership |
| `root` | System services and fixed privileged helpers | `/root` | Locked password; SSH root login disabled |

First boot asks for an owner password, not a username. The username is fixed to keep
connection instructions predictable. The owner password authenticates SSH, tty2 and
Advanced administration. File Sharing uses **the same username and a separate password**
because Samba maintains a separate credential database. Neither password is displayed
by status/help screens. Password input is masked; secret values travel through protected
standard input, never command arguments or diagnostics. No universal factory secret is
installed. On first boot, the owner account is initially locked until setup succeeds.

The account name is created in `tools/install_poc_stage.py`; its fixed UID/home/shell
contract is checked by `runtime/project_cbm/config_backend.py`. The stage writes
`/etc/project-cbm/configuration-policy.json`, whose `owner_user` field is consumed by
setup, authenticated administration and `pcbm-info`. SSH's `AllowUsers` and Samba's
`valid users` select `pcbm`. Samba writes content as `pi` so imported and shared files
remain usable by the local appliance. The `pcbm-operators` group and
`/etc/sudoers.d/pcbm-operations` grant the console only fixed validated operations;
they do not grant arbitrary shell, editor or filesystem commands as root.

Earlier private images used the literal username `owner`. Their recovery records still
refer to that account. Fresh images use `pcbm`; this is not an in-place account migration.
When restoring content, preserve the new image's account database, policy, host keys and
setup state. Do not copy old `/etc/passwd`, `/etc/shadow` or Samba databases wholesale.

## Installed layout

| Path | What it contains / who owns it |
| --- | --- |
| `/home/pi/pcbm/{games,demos,music,programs,roms,screenshots,saves}` | User content; locally usable and shared through File Sharing |
| `/home/pi/.config/pcbm` | Validated appliance preferences; user-owned |
| `/home/pi/.config/vice/sdl-vicerc` | Saved VICE resources, initially seeded only if absent |
| `/home/pi/.local/share/vice` | VICE user data/keymap lookup location |
| `/home/pi/.local/state/vice` | VICE user state/log location |
| `/home/pi/.local/state/project-cbm/diagnostics` | Bounded private engineering launch/terminal/Cover/VICE evidence |
| `/home/pcbm` | Owner shell files; outside the File Sharing export |
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
locked local appliance account and its profile enters `pcbm-console-session`. The
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
