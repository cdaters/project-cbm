# Release refinement decisions — 2026-09-18

The [attempt #6 owner report](../qualification/poc4-attempt6-pi3b-owner-report-2026-09-18.json)
is additive and bound to its exact raw/XZ hashes. Its first boot, Wi-Fi, masking, prompt
ranges, Main Menu IP, correct visible Covers, VICE/Menu/input lifecycle and reported
persistence pass on Pi 3B. VICE-active Ctrl+Alt+F2 fails; before/after emulator switching
passes. Discovery after enabling sharing was not visible in macOS; successful client
authentication was not reported. No SD-card diagnostic acquisition is claimed here.

## Bounded references and decisions

Read-only v1.0 Menu network/control/share source already offered status and connection
examples but hard-coded historical names/accounts and simultaneous start/stop actions.
The supplied local Dosbian 4.0 menu/configurator demonstrates useful contextual connection
information. Retain those user ideas; copy no code, artwork, passwords or private machine
state. Current structured Product authority, atomic preferences, protected secret transport,
restricted operations and frozen factory are retained. Reference paths/hashes are private
in `qualification/poc4-attempt7-2026-09-18/starting-preservation.json`.

Keep existing owner UID1001/account and pi console/content identity. SSH uses the first-boot
owner password; File Sharing enrolls owner separately through protected stdin. Samba cannot
recover a plaintext password from the Unix hash and first boot does not retain plaintext.
Changing account names would add migration complexity without improving predictable login.
UI now states the username and applicable password explicitly. Samba forces writes to pi
within the existing content-only share; no guest or owner-home export.

Product `pcbm-info --json --appliance` owns bounded network/unit/listener observations and
safe enrollment metadata. Menu formats Main/Menu/network/service levels, shows only useful
On/Off actions, refreshes actual state after operations, and supplies current connection
examples. On requires active unit plus expected listener, not just enabled preference.
This is local readiness; remote reachability remains a client qualification question.
Default Computer Name becomes projectcbm through the image stage and stays changeable.

Use existing Samba/Avahi dynamic `_smb._tcp` advertisement, with `mdns name = mdns`.
File Sharing opt-in explicitly enables discovery; disabling sharing leaves independent
discovery available. No static stale advertisement or new WS-Discovery daemon. Direct
SMB/SSH name/IP help is primary; platform browsing and multicast restrictions remain
physical tests. Retained Samba source 4.22.11 confirms the advertisement path.

## VICE-active VT decision

Retained SDL 2.32.4 source (`SDL_evdev_kbd.c`, `SDL_evdev.c`, `SDL_kmsdrmvideo.c`) shows
that keyboard muting sets KDSKBMODE K_OFF so evdev exclusively processes keys; `k_cons`
is empty and the console key path has no VT_ACTIVATE implementation. VT_PROCESS release/
acquire callbacks and KMS DRM release/reacquire support exist, but do not supply that
missing key-triggered activation. This explains why tty2 works before/after VICE while
its shortcut fails during SDL ownership. It is not evidence tty2 is broken.

`SDL_INPUT_LINUX_KEEP_KBD` is explicitly a debugging escape: leaving kernel keyboard
processing alive leaks emulator keystrokes into the console. Reject that workaround,
root/chvt helpers and a private SDL/input rewrite for this release. No clean supported
runtime correction was found in the pinned backend. Preserve the physically passing
Cover/VICE/Menu/keyboard/geometry/session path; document F10 → Quit before switching.
The desired same-running-session VT shortcut remains an optional future upstream-led
improvement, not a reason to destabilize the appliance.

Source tar SHA-256: SDL `d364cded8bf41f3f503014d3fb6473f1a7077ff468da1638dae4a6bec6ef2277`;
Samba `4379aa4bc6c453bfa55697556d6195ab69b1cad71e5fdfaf2c53849d96d40f0a`.
Selected read-only extractions remain in the private evidence directory. No broad web
research or third-party code copying was needed.

Rainbow and kernel/userspace startup output remain observed. Quiet boot/presentation
and measured fast boot remain separate deferred work; no getty/PAM/TTY changes here.
