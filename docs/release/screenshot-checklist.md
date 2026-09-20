# Release screenshot checklist

[Documentation index](../README.md)

Capture real final-release screens after their behavior is physically checked. Do not
simulate screenshots or reuse an older screen whose labels differ. Keep originals and
a hash/caption record outside Git; choose only reviewed, appropriately sized publication
copies. Existing physical photographs contain private network information and are not
silently repurposed. Artwork, emulator media and application screens need appropriate
rights/provenance before publication. Screenshot completion does not block text review.

| Suggested filename | Screen and purpose | Required state / privacy |
| --- | --- | --- |
| `boot.png` | Primary artwork establishes identity | Real boot; rights reviewed; no monitor overlay if avoidable |
| `setup-welcome.png` | Introduce initial setup | Fresh setup; no secret field or typed password |
| `main-menu.png` | Show all eight choices and status | Default C64; use a controlled example network, redact private addresses |
| `machines.png` | Explain launch versus DEFAULT | Current-default marker visible |
| `content.png` | Show category and relative file paths | Original/lawfully publishable example media |
| `import-result.png` | Explain content count and drive release | Three-file example; no private filenames/device identifiers |
| `control.png` | Show configuration sections | All real labels readable |
| `network.png` | Show address/gateway/DNS hierarchy | Controlled or redacted IP/SSID/MAC/name |
| `services.png` | Explain actual state | Mixed Off/On only if truly running |
| `file-sharing.png` | Show connection help | Password status only, never secret; safe example addresses |
| `remote-access.png` | Show SSH command and account | No password, key or private address |
| `system-information.png` | Show version/model/troubleshooting value | Review all network and host details |
| `c64-basic.png` | First emulator session | BASIC/original example, no third-party game |
| `files.png` | Introduce two-pane file manager | Only example library/home filenames |

Capture failed behavior separately as engineering evidence, not as the manual's normal
screen. Follow [the user workflow](user-guide.md) so the pictures form a coherent sequence.
