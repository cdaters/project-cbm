# Troubleshooting and recovery

Start with CONTROL → System Information and the relevant Network or Services screen.
The normal UI shows useful state; Advanced retains technical details. Do not paste
passwords, private keys, complete journals or saved Wi-Fi connection files into issues.

- No IP: check the cable or Wi-Fi country/connection. Retry a bounded scan; continuing
  offline is valid. An IP without Internet access may still work for local sharing.
- Cannot log in remotely: SSH username is pcbm and uses the first-boot owner password.
  File Sharing uses pcbm and a separate sharing password. Check actual service On.
- Name not found or missing Finder entry: check Network Discovery; use the displayed IP.
- Cover/VICE regression: F10 → Quit if possible; preserve allowlisted diagnostics before
  another launch. Ctrl+Alt+F2 is supported at Menu, not while this VICE/SDL build is active.
- Invalid preferences: MACHINES/configuration offers explicit recovery; preserve the bad
  file if investigating. User preferences live in the pi account's configuration directory.
- Need a shell: CONTROL → Advanced → Owner administration, or tty2 with owner credentials.
  Ordinary Linux administration remains available. Changing low-level session/display
  settings can break return to Menu and requires your own testing.

Back up `/home/pi/pcbm` content and user preferences to independent storage. Keep any
credentials/configuration backups private and encrypted. If reflashing, use a verified
image, complete setup again, then restore selected content/preferences. Do not restore
an old whole `/etc`, machine identity, credential database or first-boot state blindly.
There is no universal password recovery secret. An owner with physical storage control
can recover Linux offline or reflash after preserving data.

During formal qualification, use the exact procedure and read-only evidence policy;
do not repair the tested card in place. Developer recovery includes source bundles,
retained inputs, image hashes and offline restore checks; see [repository recovery](../recovery.md).
A second folder on the same drive is not an independent backup.

## A practical content backup

Use File Sharing to copy the entire `Project CBM` share to an independent disk on your
other computer, including games, demos, music, programs and saves. Eject/disconnect the
share after copying and open a few files from the backup to check it. A copy on the
same SD card does not protect against card failure. Keep more than one dated backup
if you frequently change emulator save files.

The share intentionally does not expose configuration or credentials. For a complete
personal backup, an administrator should also preserve `/home/pi/.config/pcbm`,
`/home/pi/.config/vice` and any personal files under `/home/pcbm`. Those files may contain
local paths or preferences; keep them private. Use ordinary authenticated Linux tools
or a safely shut-down card. An encrypted full-card backup is useful for personal
recovery, but includes passwords, Wi-Fi details and machine keys and must never be
published as a Project CBM release image.

After a fresh flash, complete first boot, copy content back through File Sharing or
USB import, and restore preferences selectively. Do not overwrite working preferences
with a malformed file. VICE preferences can also restore older performance settings;
check C64 sampling before using old settings to assess a new candidate's performance.

## Slow emulation or audio

Slow pitch/tempo together with slow graphics suggests the emulator is below real time,
not simply dropping display frames. Check the exact machine/profile, whether warp or
pause is active, and the current release's performance qualification. Power supply,
thermal throttling and CPU clock are useful evidence but are not automatic explanations.
The Pi 3 B+ performance correction is still awaiting physical qualification. Preserve
the image identity and a brief description of the workload before experimenting.
Engineering instructions use numeric speed measurements; see [VICE](vice.md).

## If the appliance will not start

Check power, display connection and the flashed image's hash before changing system
configuration. If Menu appears, use its shutdown/reboot actions rather than removing
power during writes. If the card is readable but setup/session behavior is broken,
preserve content first. A fresh verified image plus selective content restoration is
often simpler than recovering many unknown system changes. Keep the failing card or
backup intact until its useful data and diagnostic evidence are secured.

There is no factory master password. If you lose the owner password, physical access
allows ordinary Linux offline recovery; it also means physical possession is part of
the security model. Do not follow instructions that publish shadow files or replace
the appliance with unrestricted passwordless administration. During formal candidate
qualification, stop and preserve evidence instead of repairing that candidate in place.
