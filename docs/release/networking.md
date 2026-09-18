# Network and service guide

Project CBM is a single-owner home-LAN appliance. Network services start off until you
choose them. Use real passwords; do not forward its service ports to the Internet.
Credential privacy, protected storage and constrained operations remain in place.
Owners can use authenticated Advanced administration for normal Linux work.

## Computer Name and addresses

CONTROL → Network → Computer Name changes the default `projectcbm`. Use lowercase
letters, digits and internal hyphens, starting with a letter, ending with a letter or
digit, at most 63 characters. Do not enter `.local`. Choose a unique name on your LAN.
Network Discovery supplies local name resolution where the client/network supports
mDNS: normally `projectcbm.local`. A name collision or filtered multicast can change
or prevent discovery. Use the current IP displayed in Network/Services if resolution
fails. Interface names are discovered, never assumed. Multiple connected interfaces
are shown; choose an address reachable from your other computer.

## Read service state

Main Menu gives a compact overview; Services lists all user-facing services. Each
service screen shows actual state, useful actions and contextual connection help.
**Off** means stopped; **On** requires active service and its expected listener.
**Starting / Pending** means enabled or transitioning but not confirmed ready.
**Failed** means the service reports failure. **Unavailable** means it cannot be
observed or is not available in that configuration. A saved preference alone cannot
make the display say On. State is refreshed on returning to a screen; Refresh status
rechecks it. Listener readiness is local evidence, not proof another computer can connect.

An Off service offers Turn On; an On service offers Turn Off. A pending/failed enabled
service can be turned off. Correct the cause before retrying unavailable services,
using System Information or Advanced details. Partial failures are reported; check
current state because part of a compound operation may already have succeeded.

## Remote Access (SSH)

CONTROL → Services → Remote Access (SSH) → Turn On. Confirm home-network access.
The screen shows Computer Name, IP, **Username: owner**, and how to connect. Use the
**owner password selected during first boot**. With Network Discovery on:

```sh
ssh owner@projectcbm.local
```

Otherwise replace the name with the displayed IP. Confirm the host identity when
connecting to your own Pi; a freshly flashed image has new host keys. SSH supplies
an ordinary owner shell, with authenticated sudo for administration. The console
account pi is deliberately not the remote account. Turn Off stops and disables SSH;
test a new connection to verify access is gone. Existing sessions should not be used
to infer whether new connections are accepted. Service choice persists across reboot.

## File Sharing

CONTROL → Services → File Sharing. Set a **separate File Sharing password**; use the
same **owner** username. Samba has its own credential database; a Unix password hash
cannot initialize it. The application does not retain your first-boot plaintext password
or silently reuse it. Changing one password does not change the other.

Turn On explicitly also turns on Network Discovery. After actual On is shown, use
**How to connect** for current addresses. The share is named **Project CBM**:

- macOS Finder → Go → Connect to Server: `smb://projectcbm.local/Project%20CBM`.
- Windows File Explorer address bar: `\\projectcbm.local\Project CBM`.
- If name resolution fails, replace the computer name with the displayed IPv4 address.

Sign in as owner with the separate sharing password. The share exports only
`/home/pi/pcbm`, not the owner's home or the whole filesystem. Writes use the content
owner pi; guest access and links escaping the share are disabled. New content appears
under CONTENT/FILES according to supported type and folder. Credential status “Set”
records successful protected enrollment; externally changing Samba accounts in Advanced
may require setting it again here. Passwords are never displayed in status/help.

Turn Off stops/disables File Sharing; Network Discovery remains independently controlled.
Check a new client connection after disabling. Test write permissions and persistence
on the physical candidate; native tests cannot prove Finder/Explorer behavior.

## Discovery and BBS / Modem

Network Discovery uses Avahi/mDNS. Samba dynamically advertises its SMB service through
Avahi while running; no permanent advertisement claims a stopped share exists. This
is the small supported macOS/Linux discovery path. Windows direct SMB connections are
supported by the workflow; Windows Network browsing varies and is not guaranteed.
No extra WS-Discovery daemon is installed. Local names and discovery need multicast
on the same LAN; guest networks/VLANs often isolate devices. Direct IP is the fallback.

BBS / Modem reports the TCPser runtime state and local emulator endpoint, normally
`127.0.0.1:25232`. Port and speed are editable within validated ranges. It binds
loopback; turning it on does not open a public modem listener. Use the appropriate
VICE/terminal settings and test the intended BBS connection separately.
