# Collect existing POC4 attempt #3 evidence

This procedure supports the [regression investigation](poc4-regression-investigation-2026-09-17.md).
It is for owner review and execution. Do not reflash the tested card, launch VICE again,
repair its terminal, enable SSH or change its installed packages to collect evidence.
The frozen master image is already retained; the useful new material is on the used SD card.

Prefer offline collection from the stopped card. It does **not** require booting the Pi.
If the Pi is still running in the failed state, do not power-cycle merely to follow this
guide: live state is volatile. Report that fact first; arrange a separate bounded capture
plan using an already available access route. No working remote access is assumed.

## Offline collection on a Linux/ext4-capable machine

Use an existing Linux environment with automount disabled. The Mac cannot natively read
ext4; this guide does not authorize installing a filesystem driver or provisioning a new
host. Keep the tested card separate from the immutable raw/XZ master.

1. Identify the card and its Linux root partition with `lsblk -o NAME,PATH,SIZE,FSTYPE,MOUNTPOINTS`.
   Match the removable card by its known capacity and its FAT boot/ext4 root layout.
   Do not guess a disk name or select the inspection computer's root. If the card was
   already mounted writable, record that event; do not call that a pristine read-only capture.
2. Substitute the **verified root partition** below. The placeholder is deliberately
   non-executable as a real device choice. Choose an existing external output directory
   appropriate to the inspection computer; no deployment-specific mount name is required.

```sh
card_root=/dev/REPLACE_WITH_VERIFIED_CARD_ROOT_PARTITION
case "$card_root" in /dev/REPLACE_*) exit 1 ;; esac
inspect_dir=$(mktemp -d /tmp/pcbm-card-inspect.XXXXXXXX)
sudo mount -t ext4 -o ro,noload "$card_root" "$inspect_dir"
findmnt -no SOURCE,FSTYPE,OPTIONS --target "$inspect_dir"
```

Confirm `ro` and `noload` (some kernels display the equivalent `norecovery`). Do not use
fsck repair, journal replay or a normal writable mount. Mounting is a host operation;
these flags prohibit filesystem writes to the card. Hardware write protection adds
assurance if available. The mountpoint contains no copied image.

3. Read only the immutable identity first:

```sh
sudo cat "$inspect_dir/usr/share/project-cbm/identity.json"
```

Its release-lock SHA-256 must be
`435c6e0d7a5a45eaff3f45af6d384fca5b602139fa9fb640950e2f5e7b4f39a9`.
If it disagrees, stop and report the identity mismatch. The **used card's whole-disk
hash will differ** from the master after normal first boot; do not compare that hash
to the raw master as though setup writes were corruption.

4. List the existing diagnostic and setup files without generating new ones:

```sh
sudo find "$inspect_dir/home/pi/.local/state/project-cbm/diagnostics" -maxdepth 2 -type f -printf '%P\n'
sudo find "$inspect_dir/var/lib/project-cbm/setup" -maxdepth 1 -type f -printf '%f\n'
sudo find "$inspect_dir/var/lib/project-cbm/first-boot" -maxdepth 1 -type f -printf '%f\n'
```

Missing directories are useful evidence; report absence. The expected paths and their
questions are below. Copy only existing allowlisted files to a **new private external
directory**. Do not copy the entire home, `/etc`, journal or NetworkManager connections.
If using a graphical Linux file manager, preserve the relative paths and filenames and
copy these files from the read-only mount. A terminal alternative for the primary logs,
after verifying the directory exists, is:

```sh
evidence_dir=/REPLACE_WITH_EXISTING_PRIVATE_EXTERNAL_OUTPUT_DIRECTORY
case "$evidence_dir" in /REPLACE_*) exit 1 ;; esac
capture_dir=$(mktemp -d "$evidence_dir/pcbm-attempt3-card.XXXXXXXX")
sudo tar -C "$inspect_dir" -cf "$capture_dir/diagnostics.tar" -- \
  home/pi/.local/state/project-cbm/diagnostics
sudo chown "$(id -u):$(id -g)" "$capture_dir/diagnostics.tar"
chmod 600 "$capture_dir/diagnostics.tar"
sha256sum "$capture_dir/diagnostics.tar"
```

The `chown`/`chmod` apply only to the new output archive, never to the card. Retain it
privately and review before sharing: launcher redaction reduces risk but cannot promise
that every free-form VICE log is free of private filenames or identity. Do not paste
unreviewed logs into Git or chat. AP names, addresses and device IDs are not needed for
the first investigation pass. No credential should be present in the intended diagnostic
format; stop sharing if unexpected sensitive material is found.

5. Copy the identity and existing `setup/state.json`, `setup/status.json`,
   `first-boot/complete.json` and `first-boot/growth.json` into the private output with
   their relative paths. These contain no intended credentials; `growth.json` includes
   a disk identifier and should stay private. Record each file's size and SHA-256.
   Absence is recorded, not repaired. Unmount after collection:

```sh
sudo umount "$inspect_dir"
rmdir "$inspect_dir"
```

## What each artifact can determine

| Exact installed path | Question answered / limit |
| --- | --- |
| `/home/pi/.local/state/project-cbm/diagnostics/launch-*/record.json` | Actual profile/executable, launcher/VICE PIDs, UID, approved environment, spawn/exit phase, exit status, termination signal, monotonic times. Only four launch directories retained; preserve all before another run rotates them. |
| Same directories: `before.json`, `sample-0.json` through `sample-2.json` | Session list, tty, selected process names/states/wait channels, graphics/audio service observations and DRM mode when readable. `before` means **after Cover**, before VICE. Samples occur only for launches long enough to reach them. |
| Same directories: `vice.log` | Bounded 128 KiB tail, VICE errors and opt-in SDL presentation/renderer/mode resources. A saved log does not show Cover's backend or prove terminal restoration. |
| `/home/pi/.local/state/project-cbm/diagnostics/snapshot.json`, `report.json` | Exist only if `pcbm-diagnostics` was previously invoked. The report includes its then-latest launch; no assumption that these exist. |
| `/usr/share/project-cbm/identity.json` | Bind the used card's base identity to attempt #3. Does not certify subsequent live changes. |
| `/var/lib/project-cbm/setup/state.json`, `status.json` | Completed region/owner/network markers and completion/readiness projection; no passwords. Cannot reconstruct navigation history or individual operation elapsed times. |
| `/var/lib/project-cbm/first-boot/growth.json`, `complete.json` | Growth journal and root-growth completion marker. No proof of measured free capacity or interruption test. |
| `/var/log/journal/` **presence only initially** | Whether persistent first-boot/NM journal evidence may survive. Do not transfer all journal contents. If present, arrange a bounded, privately reviewed extraction of the relevant unit/time window next. |

The frozen candidate has **no Cover log**, no stored Cover exit status or timeout reason,
no persisted saved keyboard mode/termios, no foreground-group capture and no automatic
post-cleanup snapshot. Those bytes cannot be recovered from an unlogged event. Booting
the card later cannot reconstruct them. Never request the failed Wi-Fi credential.

If normal tty2 access already works in the existing session, the installed user command
`pcbm-diagnostics` generates `snapshot.json` and `report.json`; it does not repair settings
but **does write those reports on the card**, and its snapshot belongs to that later time.
Prefer collecting existing files first. Do not reboot or repeat RUN just to make this
command accessible under this collection request.

If existing evidence does not distinguish the causes, report the gap again and obtain
owner review of a tightly scoped live-state/diagnostic plan. Do not substitute speculative
cleanup, a new image, or an invented physical pass.
