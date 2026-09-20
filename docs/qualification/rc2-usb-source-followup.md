# RC2 USB source follow-up — 2026-09-20

The owner reconnected the tested drive and refreshed sudo authentication. Read-only
SSH collection verified unchanged RC2 attempt11 installed lock
`9831849a3fd12c12528e09d1b7f265d9b03e48ca2819b99f0dfe4583156e7581` before inspection. The device is a USB-backed exFAT
partition, 62,757,928,960 bytes, initially unmounted. Collection mounted it temporarily
with `ro,nodev,nosuid,noexec` and UID/GID 1000 permissions, verified the actual mount
options, listed names/types/sizes only, and unmounted it in cleanup. A separate
lsblk readback confirms it is unmounted. No payload contents, credentials, import,
preferences or persistent configuration were read/copied/changed by this collection.

## Exact relevant source set

| Location | Files | RC2 eligible | RC3 eligible |
| --- | --- | ---: | ---: |
| `Legacy-of-The-Ancients` | `LOTA0.D64`, `LOTA1.D64`, `LOTA2.D64` | 3 | 3 |
| Same folder | Their three `._LOTA*.D64` AppleDouble companions | 3 | 0 |
| `.Trashes/501` | `kong_arcade_oxyron.prg` and its `._` companion | 2 | 0 |
| Total | Current eligible source files | 8 | 3 |

There are 124 total inventoried entries including Spotlight, Trash and filesystem
event metadata. Applying the exact RC3 filename policy to this retained inventory
leaves the three intended D64 files. This is a policy comparison, not a physical
RC3 import test. No content rights or redistribution admission changes.

The source now corroborates the AppleDouble/Trash contamination previously found
in the destination. It does **not** completely reconstruct the owner's reported
count of nine: the present source contains eight RC2-eligible files. No ninth item
or historical source change is invented. RC3's existing correction remains appropriate;
no source/package/image change or additional candidate is needed.

The first collector invocation stopped before mounting because PATH-only lsblk JSON
was flat; the successful retry explicitly requested its tree structure. Both device
and candidate checks stayed mandatory. Read-only mounting is verified; a whole-device
before/after hash was not taken, and no stronger forensic claim is made.

## Evidence and continuity

Private evidence: `qualification/rc2-usb-source-2026-09-20` under configured bulk
storage. Manifest SHA-256: `1782b92cd1aecfcdfa2b81df82ff4a90efccb0f9471357d89205b56f09f8f09c`. Full names include host-generated identifiers
and remain outside Git. The previous photograph/live-evidence and RC3 recovery
manifests remain unchanged. Additive recovery:
`archive/rc3-usb-evidence-2026-09-20`.

RC3 attempt12 raw/XZ/lock/package identities and ready-to-flash status are unchanged.
Continue with the [exact Pi4B procedure](rc3-pi4b-regression.md), including three-file
copy/count and duplicate/unmount checks. Stop for owner physical qualification.
