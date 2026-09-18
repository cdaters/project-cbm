# Troubleshooting and recovery

Start with CONTROL → System Information and the relevant Network or Services screen.
The normal UI shows useful state; Advanced retains technical details. Do not paste
passwords, private keys, complete journals or saved Wi-Fi connection files into issues.

- No IP: check the cable or Wi-Fi country/connection. Retry a bounded scan; continuing
  offline is valid. An IP without Internet access may still work for local sharing.
- Cannot log in remotely: SSH username is owner and uses the first-boot owner password.
  File Sharing uses owner and a separate sharing password. Check actual service On.
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
