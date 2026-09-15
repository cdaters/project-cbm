# Security, defects and provenance follow-up

These are audit findings, not fixes. Preservation changed no runtime behavior.
Historical images are PRIVATE-HISTORICAL even when previously published; publication
does not establish clean identity or redistribution rights. Preserve originals,
review derived public artifacts separately, and never export keys/password hashes,
cloud-init user-data or shell-history contents into Git, logs or chat.

| Finding | Evidence / limitation | Later acceptance requirement |
| --- | --- | --- |
| Baked identity | Nonempty machine-id; three SSH private host-key types present | Two independently booted flashes have distinct machine IDs/host keys |
| cloud-init state | Processed instance state and completed SSH semaphore | One retry-safe first-boot owner; test Imager/custom-image/offline flows |
| Builder residue | Shell history, VICE/TCPser build trees and development packages remain | Sealed image excludes builder/private state; retain corresponding source separately |
| Broad sudo | Arbitrary root tee/mount/rm/mkdir permissions | Fixed-purpose validated helpers, negative privilege tests, user-owned preferences |
| TCPser mismatch | Enabled unit contradicts documented disabled default | Explicit opt-in policy; listener review and controlled IP232 connection tests |
| Samba inconsistency | SMB-only config vs nmbd helper and other enabled links | Coherent enabled/active/absent policy; test Samba credentials separately from Unix password |
| USB import | RM-bit selection, writable mount, fragile cleanup/filenames/skips | Root/boot exclusion, explicit device selection, read-only constrained mount and reliable cleanup/reporting |
| Installer | Resets preferences, no alternate root, sudoers installed before validation | Idempotent offline-root installation; validate before activation |
| Docs sync | --dry-run can write; --apply rsync --delete can remove public-only pages | Do not execute until corrected; product repo owns docs, consume pinned input |
| Version display | Formal Menu CONTROL/SYSTEM produce literal -e/v-e; image RELEASE has no handler | Test rendered product/menu versions against manifest; remove release prep from end-user flow deliberately |
| CI/versioning | Builds 6.5 ZIP, watches menu-v* despite VERSION 1.0.0 / v1.0.0 | Correct triggers/naming and verify contents, identity and behavior |
| Release/source drift | Five script changes + extra helper in formal Menu; distinct docs ZIPs | Explicit tag/commit/hash mapping and reconciliation changelog |
| Manual build/PiShrink | No complete lock; live-card sanitation; SD-specific expansion fallback | Clean builder, retained package closure, one expansion owner; USB/NVMe tests |
| Content/license | ROMs, media, scans and third-party artwork/fonts found | Per-file rights/source inventory before redistribution; no blanket no-ROM claim |
| Other fragility | Launch-path divergence, large scans/argument limits, numeric audio devices, service-status errors | Focused behavior tests and physical qualification, with Pi 3 cost limits |

Presence of identity state is verified; reuse after first boot is a strong concern
requiring two-device testing, not a fabricated runtime observation. Enabled links
do not prove running services. No passwords were tested and no exploit was attempted.

VICE is GPL software; preserve its corresponding source/license/build flags. The
retained tarball hash identifies a recovered input, not independently authenticated
upstream origin. Project-owned source/docs use the repository MIT grant; it does
not grant rights to ROMs, fonts, logos, cover source art, screenshots of third-party
content or other media. Personal-use font filenames/licenses are evidence requiring
review, not permission to relicense a complete artwork archive.

TheBench is unencrypted with ownership disabled. Directory modes do not provide
encryption. Detailed manifests, logs, Git administrative backups and release draft
metadata stay private externally. A second independent encrypted backup destination
needs owner selection. Do not delete historical duplicates or keys from originals.

Before any public artifact: review content provenance, first-boot identity/account
state, service exposure, privilege boundaries and qualification. Owner review is
needed for any change to existing public image availability or a maintenance release;
neither was performed. See [full audit](audit-2026-09-15.md#k-risks-and-unresolved-questions).

## Public recovery metadata boundary

[Black-box recovery](recovery.md) must never embed passwords/password hashes,
private SSH/signing keys, API credentials, personal shell history, user files,
private network credentials or sensitive builder-machine identifiers. Do not publish
raw builder environment dumps, home paths, hostname/IP/MAC/serial identity, account
or network config, private registry URLs/tokens, or unique test-device identities.
Use build IDs, synthetic test IDs, source commits and sanitized toolchain facts.

Public-field allowlists, secret-pattern scans and manual review complement each
other; scans alone do not prove safe publication. Verify the actual sealed filesystem
separately. Historical private archives retain original evidence under encryption/
access policy and are not public recovery kits. Public Git history and legacy assets
also require review; a bundle inherits its history's visibility, not a blanket
public label. Keep public verification keys/signatures/trust transitions; private
signing recovery and unlock custody belong in a separate protected procedure.
Checksums and matching embedded metadata do not prove publisher authenticity.
The authoritative lock itself must be public-safe from construction; do not redact
it into a different embedded copy after computing its digest. Acquisition credentials
stay outside declared content inputs and all logs/locks. Public build records are
generated summaries; private raw transcripts never become embedded recovery material.
