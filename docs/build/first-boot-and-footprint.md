# First-boot and footprint contracts

Design only, 2026-09-15. No first-boot unit/script, account flow, expansion mechanism,
Samba/TCPser change or image is implemented. Keep writable ext4 and the existing
/home/pi/pcbm content path. Systemd plus the shared Bash launcher contract remains
the selected lifecycle mechanism, without a user hook/plugin framework.

## One owner and upstream reconciliation

The product owns one policy and ordering graph; reuse upstream mechanisms where
correct. The research pi-gen revision is
`6fcca44892d5d4b36f826d2b8fb16d716369fada`.
Its [export finalizer](https://github.com/RPi-Distro/pi-gen/blob/6fcca44892d5d4b36f826d2b8fb16d716369fada/export-image/05-finalise/01-run.sh)
removes the D-Bus machine-id and writes `uninitialized` to /etc/machine-id.
Its cloud-init stage is conditional. Neither observation proves a complete CBM
first-boot flow. Inspect the chosen vendor packages/units for root resize, user rename,
SSH generation and cloud-init before choosing which mechanism owns each operation.
Do not stack PiShrink, cloud-init growth and a custom resize service.

Systemd [machine-id semantics](https://manpages.debian.org/trixie/systemd/machine-id.5.en.html)
distinguish missing, empty and `uninitialized` files for first-boot detection; an empty
file alone is not interchangeable with the first-boot marker. Follow the chosen version,
not a generic “truncate everything” recipe. [Image sealing guidance](https://systemd.io/BUILDING_IMAGES/)
separates reusable image preparation from machine-specific initialization.

## Construction versus first boot

| Construction/sealing | First boot / retry contract |
| --- | --- |
| Install packages/templates/identity; establish root-owned defaults and intended content directories | Check/create user-owned preference/content directories without overwriting existing choices |
| Remove reusable machine-id/D-Bus state according to chosen systemd/vendor semantics | Let systemd establish one fresh persistent machine-id; never regenerate it on a later failed-step retry |
| Remove host SSH keys and builder authorized keys/credentials; do not copy host home directories | If SSH is selected, generate missing host keys once, preserve valid keys, and gate listener readiness on account/credential policy |
| Remove stale cloud-init instance state/semaphores and reusable random-seed data through reviewed sealing | Run only the chosen offline user/config path; secrets entered locally stay outside release lock/build logs |
| Record one expansion owner and partition/filesystem expectations | Discover actual mounted root and parent partition/device, verify supported layout, then grow only that root partition/filesystem |
| Remove build logs/caches, source/development trees and build-only service overrides; audit installed dependencies | Use bounded local diagnostics; never put recovery archives in the appliance |
| Generate /usr/share/project-cbm/identity.json once from the frozen lock | Never modify installed base-release identity; initialization progress is separate state |

Default pi account/content paths and upstream first-user rename/setup need explicit
integration: do not assume a baked password or an unattended rename preserves Menu
paths. Keep SSH/Samba readiness gated, with no assumption that SSH defaults on. Samba
credentials are separate from Unix credentials; test both change directions rather
than asserting password synchronization. Exact defaults and UI flow remain open.

## Retry-safe state design

Use a root-owned state directory such as /var/lib/project-cbm/first-boot/, separate
from /usr/share identity. A single coordinator acquires an exclusive lock and records
versioned per-step completion only after verifying its postcondition. Atomically
replace state files and sync where durability matters. Treat markers as evidence to
recheck, not permission to skip a broken postcondition. Do not infer failure means
“start over and overwrite everything.” Failed prerequisite gates Menu/network readiness
and exposes an offline diagnostic path without claiming successful initialization.

Growth: root may be SD, USB or NVMe; never hard-code mmcblk0. Refuse ambiguous roots,
unexpected mapper/encrypted layouts or mounted-device mismatches until implemented.
Already-expanded media is a no-op. If partition growth requires reboot, persist that
phase and verify the new geometry after reboot before filesystem growth. Interrupted
partition changes need inspection/recovery; do not keep blindly issuing mutations.
Do not shrink, create USERDATA or repartition unrelated devices. Handle no extra space
as an explicit success/no-growth or insufficient-margin result per qualified policy.

Account/user-state steps preserve existing IDs, keys, credentials and user choices.
Write the overall completion marker only after all required postconditions pass.
Systemd starts dependent services only after completion; optional services remain
opt-in according to the frozen policy. Shutdown is orderly but cannot promise final
writes on power loss. Later launcher tests must cover failure/exit console restoration;
SIGKILL/power loss require startup recovery, not just shell traps.

Required tests after implementation: first boot offline; second boot no-op; interrupted
run after every step; disk full/read-only failures; two independently flashed identities;
existing user configuration preservation; SD/USB/NVMe actual-root expansion; repeated
missing/existing SSH-key cases; intended service/listener states. None has been run.

## Footprint measurement plan

No fixed 8 GB minimum. Record candidate/lock ID, medium usable bytes, measurement
phase, command/tool versions and whether values are apparent or allocated bytes.

| Measure | Future evidence hook |
| --- | --- |
| Compressed and raw image size | Exact stat bytes and SHA-256 of finalized XZ/raw artifacts |
| Root used/free before initialization | Read-only offline filesystem metrics; separate partition capacity from allocated file bytes |
| Root used/free after initialization | Filesystem statistics immediately after success and after a normal reboot |
| Runtime package footprint | Installed dpkg inventory/Installed-Size plus measured filesystem use; shared files/dependencies avoid double counting |
| Project-owned footprint | Stage/package ownership inventory, apparent and allocated file sizes |
| User-content capacity | Root free bytes less measured first-boot/update/log/cache safety margin; report current content use separately |
| Peak maintenance margin | Peak space during package operations, initialization, logs/cache/swap growth, then full-disk failure behavior |

Typical evidence sources are stat, filesystem tools, df, du and dpkg-query, but exact
commands must be qualified on the Linux image (macOS tools differ). Publish machine-
readable measurements externally alongside candidate qualification. Set supported
minimum usable storage only from actual measurements and a safe margin; no arbitrary
nominal card label drives the architecture. Performance/boot/RAM/space budgets remain
unmeasured and require owner agreement and physical Pi 3/3A+ evidence.
