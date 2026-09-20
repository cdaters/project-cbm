# Private RC3 — attempt 12

**READY TO FLASH: YES after the external recovery manifest and offline restore report
verify PASS. Physical RC3 qualification remains UNTESTED.** One image was constructed;
no earlier candidate, tested Pi configuration or retained artifact was changed.
Use the [exact-hash Pi 4 B procedure](../qualification/rc3-pi4b-regression.md).
[Machine-readable results](private-rc3.json) contain the complete identities.

## Physical findings and decisions

The [RC2 owner report](../qualification/rc2-attempt11-pi4-owner-report.json) retains
the exact attempt11 results: core functioning, artwork visible and USB copying;
presentation order, routine boot text and import count/filtering fail. The repeated
20–23-second time is to first meaningful activity. RC1's approximately 30-second
endpoint was interactive Menu; the owner observes improvement, but neither these
stopwatch observations nor the traces isolate its exact cause.

Seven photographs are preserved outside Git with captions and original hashes in
`qualification/rc2-attempt11-polish-2026-09-19`; its manifest SHA-256 is
`59a0fffed9e5fc93c67b51e3625606bccbbf8a411d56af3d440cbb7f74e310bf`.
Read-only SSH verified RC2 identity, installed code, imported filenames and five boot
traces. Primary presentation consumed 4.69–4.96seconds late in initialization; Menu
dialog dispatch occurred at 18.18–18.67seconds uptime. Dispatch is not an interactive
readiness measurement. Completed setup showed Saving configuration, and releasing
the late renderer restored that earlier screen. The HDMI timing/plug icon appears
display-generated; it is not treated as appliance output.

The destination proves unwanted AppleDouble companions and Trash PRG traversal.
The original nine-file source set was initially unavailable because the drive was
absent. The owner later reattached the USB; its unmounted exFAT identity was verified, but
authenticated mounting was unavailable. Original nine-file reconciliation remains
open; this does not change the evidenced metadata defect or its correction. Do not
infer every destination Finder file was copied by import. No user payload is bundled.

## Corrections

- Primary artwork starts at entry into the existing tty1 PAM appliance session,
  the earliest chosen safe point with established unprivileged display/session
  ownership. Setup/preferences/status prepare concurrently behind it. A bounded
  pipe handoff releases artwork only after a three-second visible-frame minimum
  and readiness of the first meaningful UI, then verifies terminal restoration.
  Fresh setup receives one presentation before setup, with no repeat afterward.
- Completed setup retains its idempotent recovery/readiness operation silently.
  Errors remain visible. Tty1 automatic-login/IP prose is suppressed through
  supported agetty options; tty2 recovery behavior remains unchanged.
- A checked initramfs build hook suppresses only successful quiet-branch fsck
  console output. Full logs, nonzero outcomes and verbose recovery remain intact.
  Both exported initramfs images contain the exact hook result. NetworkManager
  wait-online, maintenance and filesystem checks remain enabled.
- Import ignores the narrow documented host-metadata names and AppleDouble `._`
  entries before traversal. Other hidden media remains eligible. Results count
  copied content files separately from ignored metadata; duplicates are preserved.
  Read-only mounting, UID 1000 copy, source integrity and safe unmount remain intact.
- Candidate filename validation rejects stale release names/suffixes before freeze.
  Runtime/Menu become RC3; VICE/TCPser are unchanged.

[Implementation rationale and filter policy](../runtime/rc3-polish.md) explain the
contracts and recovery path. The bounded v1.0.0 review retained its recognizable
primary identity idea, not its obsolete framebuffer/ImageMagick mechanism. No new
graphical owner, Plymouth, service architecture or firmware geometry was introduced.
Pi4 performance, x64sc/SID defaults, seven machine Covers, F10/Quit, account/content,
network/service contracts and privilege boundaries are unchanged.

## Tests and actual-image validation

Host **Product231/231, Menu100/100**; native **Product231/231, Menu100/100**;
installed lifecycle **12/12**. Native service/account/authenticated administration,
SSH enable/use/disable, persistence, local discovery, gateway/DNS, dialog, MC and
import regressions pass. These are native checks, not new physical claims.

New native PTY/SDL tests hold artwork about 3.11seconds when ready immediately and
4.09seconds when readiness arrives at 4 seconds, with verified restoration/reaping.
Actual agetty/login/PAM quiet-prompt behavior passes. FAT/exFAT fixtures copy 9 intended
media files, ignore 9 metadata entries/subtrees, preserve 9 duplicates on retry, retain
legitimate hidden media, enforce UID/GID1000, unmount and leave source hashes unchanged.
Those synthetic counts do not reconstruct the owner's original nine-file observation.
Quiet fsck 0 hides routine output; statuses 1/4/32 and verbose success remain visible;
unexpected vendor text fails the hook. Actual generated initramfs extraction passes.

The final image passes **305 checks:122 main +20 supplemental +163 corrective**,
including **672 installed package identities**, **127 ELF objects**, FAT/ext4 checks,
both initramfs, exact identity, accounts/services, constrained privileges, lifecycle
bytes and shipped documentation. No credential files were read or secrets written into the evidence.
Raw/XZ equivalence passes in the builder and independently on the external Mac copy.
Full frozen-input semantic validation passed natively; all 3111 copied kit files match
native sizes/hashes. The Mac lacks dpkg-deb and does not claim that native semantic test.

Retained fixture corrections: old startup-text/working-dialog assertions were updated;
an ANSI prompt matcher was corrected; restricted-sysfs initramfs testing was repeated
with the factory's generation mode. None is concealed as a physical result. The final
required suites have zero failures. Visual KMS timing, USB usability and new boot order
remain for physical qualification.

## Frozen inputs and artifacts

Integration: `ece07f04c396c1530a179a5980a41b9b0e8a81b9`. Menu tag `v1.1.0_rc3`, object `cbcbb7ad2b4045d32f74ad857aee25916cd389b6`,
peeled source `23f0e0b0a0a77fc4ba565a6dd777543f11cce6c0`. Final continuity commits may advance repository HEADs without
changing these frozen pins. Pinned pi-gen is
`6fcca44892d5d4b36f826d2b8fb16d716369fada`, native Lima/VZ Debian 13 arm64.

All paths below are relative to configured bulk storage, currently
`/Volumes/TheBench/ProjectCBM-Work`.

Lock: `inputs/frozen-poc4-attempt12/release-lock.json`  
SHA-256: `bbcf02a56403c8f19bd42304f985cd5202ac797311a9ddf4cad5ea2eb79e665d`

| Disposition | Package filename (version included) | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| NEW | `project-cbm-menu_1.1.0~rc3-1+pcbm1_all.deb` | 1,294,628 | `194a387412cd425d0b9d4f59695c594142f3cb23835e53bf2035fc77c2ccc685` |
| NEW | `project-cbm-runtime_1.1.0~rc3-1_all.deb` | 67,508 | `592d9ef7da99e897c7c6ed1681f821e0579fdfb721e47b9c611c576104a39fb2` |
| REUSED | `project-cbm-vice_3.10-1+pcbm4_arm64.deb` | 5,069,684 | `a7b77c3b006eb190c64c10cadbfd91ce4152a73523c440496209293da2901dc1` |
| REUSED | `project-cbm-tcpser_1.1.6~beta-1+pcbm1_arm64.deb` | 26,872 | `8b8f8a4f3ec98dddf5bdb347320dad05e1bbe5230e0ee2727248c247a5af584f` |

**RAW**: `artifacts/private-rc3-attempt-12/2026-09-20-project-cbm-1.1.0-rc.3-lite-private-rc3.img`

- Bytes: 3,095,396,352
- SHA-256: `5bde293b5ec6096e2a3bb2f9b31f123a8a07fdc6ac1f9077b510a4ceb5a1702e`

**XZ**: `artifacts/private-rc3-attempt-12/image_2026-09-20-project-cbm-1.1.0-rc.3-lite-private-rc3.img.xz`

- Bytes: 599,157,232
- SHA-256: `ca9f21d6bcfa3cae46921bbc4cd93663e9c7800832a173546d1181789ca8d15b`

Expanded XZ bytes/hash equal the raw image. `SHA256SUMS` accompanies the artifacts.
Construction completed once with exit 0 in 192.76seconds; no claim of independent-build
byte reproducibility is made.

Root filesystem capacity 2,439,266,304bytes; used 1,655,607,296; free 783,659,008;
available to ordinary users 639,377,408. Boot usage 78,419,456bytes. Installed-package
size sum 1,602,472,960bytes. Maintenance margin beyond measured free space and actual
post-expansion user capacity remain unmeasured; there is no invented nominal 8 GB minimum.

## Host integrity and recovery

Before construction, builder capacity was safely increased 224→256GiB after a stopped
full disk/config snapshot verified byte-for-byte. Snapshot manifest:
`build-host/records/pre-rc3-disk-growth-2026-09-19/manifest.json`, SHA-256
`acc1423bbd0495b15d48daeaf451065e6c3e6f6e4c979d4c9f8ead51f75a94a7`.
Capabilities, update guards, AppArmor and identical pre/post package inventory pass.
Inventory SHA-256 `352fb0f9ed6503e7570278573c8a04219856d8bde086c66e173c7d51c6dd0aa6`.
No leftover mounts, loops or emulators; 64,824,492,032bytes free; builder STOPPED.
Prior candidates, failed attempts, locks, packages, protected refs and original
preservation manifests pass verification without replacement.

Recovery checkpoint: `archive/rc3-2026-09-20`. Its external `manifest.json.sha256`
is the checksum authority, avoiding a checksum cycle with this committed report.
Require `restore-report.json` PASS for both complete bundles, exact refs/peeled tags,
symbolic refs/HEAD, offline restored critical files and fsck. Referenced frozen input,
artifact and private qualification bytes are retained; the previous RC2 checkpoint
remains intact. This is another folder on unencrypted TheBench, not independent custody.
An independent encrypted backup/restore drill remains outstanding.

## Release status and next action

Physical qualification is required for boot order/visibility/timing, three-file USB
counts/retry and the preserved core/service/performance behavior. RC2 findings remain
historical FAILs until the new exact candidate is physically tested; host tests do not
erase them. Private rights admissions, public bootstrap/input publication gaps and
independent recovery/reproducibility work remain as documented; this is not a public
release or a newly qualified hardware model.

After the external recovery checks pass, flash the exact RC3 artifact and perform the
Pi 4 B procedure. Stop for owner physical results. Nothing was pushed or published.
