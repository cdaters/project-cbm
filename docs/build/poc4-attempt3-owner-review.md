# POC4 attempt #3 — owner review: stopped before construction

2026-09-16. This is the complete report for the bounded Combian/Covers candidate
authorization. **No attempt #3 image exists. Do not flash attempt #2 instead.**
Paths below are relative to configured bulk storage unless explicitly absolute;
this deployment uses `/Volumes/TheBench/ProjectCBM-Work`.

## A. Executive summary

The bounded historical review, two small UI improvements, new versioned Menu package,
native Linux staging and immutable input freeze are complete. 143 Product tests,
65 Menu tests and the launcher checker pass. No architecture was reopened.

Image construction did **not** start. Automatic approval review rejected the privileged
remote build, interpreting an older AGENTS boundary as prohibiting image construction
despite the owner's current explicit authorization. It then rejected a documentation
commit that attempted to reconcile that boundary. The uncommitted AGENTS addendum was
removed; AGENTS is unchanged. No alternate build route was attempted. This is an
**approval-blocked pre-build checkpoint**, not another failed image construction.
Offline image validation and exact-hash physical readiness are consequently pending.

During evidence retention, an incorrect rsync include order descended into two
disposable staging trees. The transfer was stopped. Automatic review rejected both
the broad cleanup and subsequently the two-path cleanup, citing possible evidence
loss. Those partial copies remain at:

- `qualification/poc4-attempt3-2026-09-16/native/environment/`
- `qualification/poc4-attempt3-2026-09-16/native/runtime/`

They are **not recovery evidence or build inputs**. Do not publish, restore or copy
them into another recovery kit: disposable target trees may contain synthetic account,
key or credential state. Permission-denied messages prevented some private files from
copying; that does not establish that every copied file is safe. Bounded top-level
logs/test scripts are retained separately by explicit manifest entries. Owner-approved
cleanup of these exact accidental copies remains necessary; originals in the VM and
all earlier evidence must be preserved. No secret values were printed or committed.

## B. Actual Combian V3.7 review

Reference: `/Volumes/TheBench/Projects/Combian/Combian64 - V37_update_updatedEN/`.
Exactly four files exist: `menu`, `alsa`, `usbcopy`, `fixusb`. Their bytes/metadata were
inventoried and rechecked without modification or execution. This is an update folder,
not a complete Combian installation. The [comparison matrix](../design/combian-v37-bounded-review.md)
and [exact inventory](../design/combian-v37-inventory.json) are part of this report.

Observed: Bash/dialog; eleven machine choices rewriting a launch script; generic fbi
artwork before the menu; dhcpcd/Samba toggles; fixed TCPser invocation and port-derived
kill; sudo mc/raspi-config; shell exit; shutdown/reboot; fixed USB path and games-only
copying; privileged alsamixer/global state save; vendor udev PrivateMounts edit; a
SID-Wizard 1.8 case without a visible matching menu option. INFO/bootmachine and the
referenced artwork/application payloads are absent. StrikeTerm is absent here.

Inferred intent: easy machine selection, networking/file transfer, BBS access, file
management, mixer access, import and owner administration. These are interpretations
of the scripts, not proof of successful historical runtime behavior.

Registry/preferences, shared launcher, NetworkManager, typed service helpers,
authenticated owner administration, normal-user mc and the USB broker already meet
or supersede these needs. Adopted only Advanced Mixer and clearer import destination
feedback. Rejected script rewriting, broad sudo, arbitrary port killing, fixed USB
mount assumptions, vendor-unit edits and framebuffer artwork handling. Additional
historical boot/INFO behavior cannot be established from absent files. Live import
progress and actual VICE/terminal/BBS connectivity remain separate work/tests.

## C. Menu/configuration conclusion

Bash/dialog and the accepted nine-area pcbm-config hierarchy remain. No Main Menu
reorganization or new framework. Picture, Sound and Controllers gains Advanced Mixer;
import completion names its destination. All other navigation stays familiar.

## D. Midnight Commander

Already included in the frozen base closure: **mc 3:4.8.33-1+deb13u1 arm64** plus
**mc-data 3:4.8.33-1+deb13u1 all** from Debian. No fork or rebuild. Exact package hashes
are in section V and the Menu build record. Menu Depends requires mc. FILES invokes
`mc` as the normal appliance user, without sudo; the child exits back to Menu.
Fixture return tests and actual Linux PTY launch as UID 1000/F10 exit pass.
New-image presence cannot be checked until construction; physical console/copy behavior
remains untested. The intended frozen input gate is satisfied.

## E. Advanced ALSA Mixer

Included under Picture, Sound and Controllers because it provides standard available
sound-card controls without adding dependencies. `/usr/bin/alsamixer` comes from
**alsa-utils 1.2.14-1+rpt1 arm64** (Raspberry Pi OS). Direct unprivileged invocation;
Escape exits, F6 selects a card, terminal state is restored. Missing tool/device and
failure have a graceful result. No sudo or `alsactl store`; persistence follows existing
OS policy, not a new promise to save global state. Some digital outputs expose no mixer.
UI success/failure/unavailable tests pass; native executable/package verification passes.
Actual sound-card controls and VICE audio afterward need Pi testing.

## F. Project CBM Covers

Seven unchanged JPEGs are packaged; the following generated identity table records
their exact hashes and profile mappings. Owner-authorized private artwork admission
is retained; no new clearance of constituent third-party graphics/fonts is inferred.

| Cover file | Profiles | SHA-256 |
| --- | --- | --- |
| pcbmcover-c64.jpg | x64, x64sc, xscpu64, x64dtv | `6e5b155eecb6c719f57ecdfba036f11e5ead23327424268d215ab865cdc1f76b` |
| pcbmcover-c128.jpg | x128, x12880 | `c306250c04358b6bc94f97faa9976e714de61710629f3ce2d26c90e66f395367` |
| pcbmcover-cbm2.jpg | xcbm2 | `7d996ead73fa0954dc99037eaf14ecf4c2001541380e86327395862ac3c7012f` |
| pcbmcover-cbm5.jpg | xcbm5x0 | `09c6c01e2ef05ca25038fc0ac8795b3ecb464ebd192f6efa28828fce8ca66068` |
| pcbmcover-pet.jpg | xpet | `25336594429d9c6a55cb711032fba6c4b076c5db416213ab976b228395e387ff` |
| pcbmcover-plus4.jpg | xplus4 | `32a85daa631215e28bb9a39d1b2b14d0b2b8bfc477cad0b602c6b776f40d4afb` |
| pcbmcover-vic20.jpg | xvic | `4cf2660de2d6bd6a952b633d85891cb69d272d789f7c15fb4f9baf70b1d90523` |

Renderer: small Python/ctypes SDL2/SDL2_image helper, installed at
`/usr/libexec/project-cbm-menu/pcbm_cover_view.py`, with `/usr/bin/pcbm-cover` wrapper.
It requests desktop fullscreen, fits artwork proportionally within its presentation
area, centers it against black and releases SDL resources before VICE. Duration 0.75 s,
key may skip; shared launcher enforces 2 s timeout plus 0.5 s kill grace. Missing
artwork/renderer or failed/hung rendering falls through to VICE. No root, fbi, fbset,
ImageMagick, temporary converted image, chvt or display-resolution manipulation.

RUN resolves the current preference; explicit MACHINES launch uses its selected profile;
CONTENT uses its validated actual/forced profile. One shared launcher owns the transition,
so a content-specific C64 launch cannot accidentally display another default's Cover.
Registry mapping is authoritative. Geometry/audio/F10/return defaults remain unchanged.
Cover presentation is wholly separate from deferred power-on boot presentation.

Native installed-package SDL dummy tests: C64 0.768 s; VIC-20 0.765 s; UID 1000;
video subsystem released between runs; actual hung-process kill 2.505 s; measured
process maximum RSS 31,944 KiB. These are VM/headless measurements, not Pi performance.
Fixture tests cover selection/fallback/return. **Physical KMS/VT/VICE handoff is UNTESTED.**

## G. Menu version and Cover identity

Menu **1.1.0_poc4.1**, package **project-cbm-menu 1.1.0~poc4.1-1+pcbm1 / all**;
source `407ced58b711209631cdfb4db6dcd741a555f408`, annotated tag `v1.1.0_poc4.1`,
tag object `003ff32cb3dce01292304511430e541c800f79e6`.
Package SHA-256 `6df8fb42a10b16e12ac114032accc149c49ebf51f0e5f45c34b77d2cefbb2767`.
Requires `project-cbm-runtime-api (= 1)`; information/request contracts remain version 1.
No new runtime API. Exact renderer/mapping/source hashes appear in the JSON companion.

Attempt #2's **1.1.0~poc4-1+pcbm1**, source
`bb8a66ea9da994b30f978ad87d61c9aedb03dad6`, hash
`b1c95d128eb0f9b3d9ba59528ed7be39d7f94cf158933bd74c83f0eecb83999d`, stays immutable.
It lacks the subsequently completed Covers. The new lock cannot consume it as the new
version. Covers implementation predates this bounded review; this work packages it.

## H. First boot

Existing accepted runtime is unchanged: standard machine identity initialization;
guarded actual-root FAT/ext4 growth; tty1 getty/login/PAM starts short retry-safe setup;
region/locale, keyboard, timezone; unique owner password; offline/Ethernet/Wi-Fi choice;
required readiness/completion; Menu. Wi-Fi choice completes required local setup then
opens the normal Network workflow. Networking is not a completion requirement.

Explicit private state and atomic writes guard each completed step. Completion requires
owner authentication readiness and helper readiness. Retry preserves completed state;
completed setup cannot reset the owner password through its initialization operation.
Growth validates partition identity/start/geometry and records success only afterward.
SSH keys are absent in sealed input policy and generated only on deliberate activation.
Keyboard changes take effect on reboot; password entry uses the current keyboard layout.
Actual root expansion/power interruption, firmware/session sequencing and real first-boot
interaction remain physical gates; fixture/native mechanics do not establish them.

## I. Owner administration

`pi` is the unprivileged appliance user (UID 1000); `owner` is the separate administration
account (UID 1001), initially locked until unique password initialization. No preset
password. Passwords travel via private input/stdin, not command arguments or retained logs.
Ordinary authenticated sudo permits owner administration of apt, systemctl, boot files
and raspi-config. Advanced Terminal authenticates into the owner environment; shell
exit returns to the UI. Advanced Raspberry Pi Configuration authenticates and invokes
sudo raspi-config; separate su/sudo authentication may request twice. Wrong/cancelled
authentication returns safely. Native PAM/sudo, terminal return and vendor raspi-config
invocation pass. The owner is not artificially restricted; advanced changes may require
restoring configuration or reflashing if they break the qualified appliance.

## J. Networking

Standard NetworkManager provides Ethernet/DHCP, Wi-Fi and connection persistence.
Initial policy is offline: daemon available, networking/radio disabled until deliberate
selection. Network UI exposes enable/offline, status, country/radio, nearby WPA-personal
SSID selection, password entry, hidden SSID entry, disconnect/forget and hostname.
Country → scan → select SSID → private password → connection needs no Ethernet, shell,
raspi-config UI, DNS or Internet. From Stay Offline, first choose Enable networking.

Validated requests use private NetworkManager keyfiles and exclude credentials from
errors/info/diagnostics. Native parsing, private credential round-trip, no-radio failure,
forget/offline pass; fixture no-Ethernet workflow passes. Saved connection/reconnection
is intended standard NetworkManager behavior, not yet physical evidence. Enterprise/open
networks and unusual IP policies remain advanced administration. **Source/staging is ready
for the no-Ethernet scenario; no flashable candidate exists yet.** Pi country/radio scan,
enrollment, DHCP, reboot/reconnect and real credential-redaction checks remain required.

## K. Services

All optional services default disabled; configuration support does not silently activate
them. Fixed helper operations map friendly names to an allowlist, not arbitrary units.

| Service | Configuration/security | Native result / remaining test |
| --- | --- | --- |
| File Sharing / Samba | Services; content-only `/home/pi/pcbm`, no guest; separate Samba credential store, private stdin enrollment | Credential creation/start/stop pass; client access/scope and physical persistence pending |
| Remote Shell / SSH | Services; deliberate enable generates fresh host keys; owner login, no root login; Unix owner credentials separate from Samba | Key generation/config/start/stop pass; real client/authentication/reboot pending |
| BBS / Modem / TCPser | Services typed settings; validated port/baud, loopback listener; no arbitrary command fragments | Adapter/start/stop/local listener pass; VICE serial driver, StrikeTerm and external BBS interaction pending |
| Local hostname discovery / Avahi | Deliberate mDNS enable/disable; friendly hostname, fixed service | Start/stop pass; LAN discovery pending |

No automatic public inbound BBS exposure. External environment absence is UNTESTED/
NOT APPLICABLE, not automatically a Project CBM failure.

## L. USB import

Broker discovers eligible unmounted USB partitions, excludes system/mounted disks,
revalidates device identity, accepts only supported filesystems and mounts read-only
with nodev/nosuid/noexec (ext4 noload). User selects a device and semantic content
category, never arbitrary source/destination mount paths. Copy runs as UID 1000,
rejects symlinks/unsafe traversal and overwrites, limits transfer/space consumption,
reports counts/errors and unmounts on completion/failure. SID goes to music; other
supported media go to chosen games/demos/programs/music `Imported` folders. Extensions
alone cannot distinguish a game from a demo. New completion text names both destinations.

Native synthetic ext4 source: 2 files/56 bytes copied, 2 unsafe/inaccessible entries
skipped; retry copied none, skipped 4; unmounted and original source hash unchanged.
Only test discovery accepted the loop device; production removable checks were not
relaxed. This supersedes fixed `/media/usb0`, games-only X-Copy without copying its code.
The Combian vendor `PrivateMounts=no` edit is **not required**. Physical USB discovery,
real device filesystems and user workflow still require testing.

## M. Machine and boot preferences

One validated eleven-profile registry owns names/executables/options/video chips/Covers.
User-owned XDG preferences (normally `~/.config/project-cbm`) use validated atomic
writes. Valid new preference wins; supported validated legacy state may initialize once;
otherwise the Project CBM default applies. Legacy bytes are retained, never executed.
Boot Menu or selected machine uses the same authority; direct boot launches once per
session, then Quit/failure returns to Menu rather than restarting indefinitely.
POC3 geometry, F10 → VICE menu → Quit and user preference preservation remain configured.

## N. pcbm-info, System Information, About

Runtime package provides dialog-independent read-only `pcbm-info` and schema-version-1
JSON: BUILT AS identity/package metadata; RUNNING ON detected hardware/OS/kernel/RAM/
storage/display; CURRENT STATE hostname/default machine/boot/network/services. Missing
interfaces return explicit unknown/null, not fabricated hardware facts. No serials,
credentials or arbitrary environment dump. The Menu bridge consumes JSON for grouped
System Information and concise About with credits/license/project guidance, avoiding
duplicate version probes. Native installed interfaces and fixtures pass; actual Pi
facts must be checked on the eventual image. No detection redesign in this pass.

## O. SID-Wizard 1.97

Hermit (Mihály Horváth), accepted authoritative retained archive:
`https://csdb.dk/getinternalfile.php/281063/SID-Wizard-1.97-sources-examples.tar.gz`.
Archive SHA-256 `aeb265f4a778b2acb5aad13e8e98af882888292f749f29f4d18cbf49850e57bc`.
Accepted `LicenseRef-Hermit-WTF` notice and reviewed redistribution basis are unchanged.
Only native SID-Wizard/SID-Maker core plus required notices; no example music, instrument
collections, host apps or full manual. Deterministic D64 SHA-256
`cec93ae1fd5fc846507c1883fd9cb210c6a3c0f40c1c081964e3b8450e26dc44`;
prepared bundle SHA-256 `46872e5c937f681fa161a2acf88937040f2b90a091b03d8153513035bd62223e`.
Immutable template `/usr/share/project-cbm/applications/sid-wizard/`; working disk
`/home/pi/pcbm/music/Creation/SID-Wizard/SID-Wizard-1.97.d64` is user owned.
Normal CONTENT/shared x64sc launcher; no one-off privilege. Native deterministic
preparation, ownership and preservation of existing working state pass. C64 launch,
audio/composition basics and save/relaunch need physical testing. No downgrade to 1.8.

## P. StrikeTerm 2014 Final

Alwyz, author-endorsed retained `st2014final.d64` from
`https://csdb.dk/getinternalfile.php/129890/st2014final.d64`, **174,848 bytes**,
SHA-256 `72b803c54c7892857c0ddb5674dabc841d59a496285975546bef689308940595`.
Prior POC4 comparison established equality with the previously recorded Combian copy.
The newly reviewed four-file folder has no StrikeTerm payload, so provides no new
byte-level corroboration. Exact existing admission/hash checks pass.
Working location `/home/pi/pcbm/programs/Communications/StrikeTerm/StrikeTerm-2014-Final.d64`;
normal CONTENT/shared x64sc launch. **PRIVATE-ENGINEERING-ADMITTED** and
**PUBLIC-RELEASE-RIGHTS-GATE-PENDING** remain explicit. Launch/input/return are physical
tests; BBS networking is separate. No public redistribution clearance is claimed.

## Q. Reference SID/demo content

Requested classic SID tunes, dual-SID/$D420 references and Wonderland XIV remain
**OWNER-SUPPLIED / NOT BUNDLED**. No downloading or new acquisition. Existing validated
IMPORT/CONTENT paths accept lawfully owner-provided supported media. These do not
replace the original Project CBM qualification suite.

## R. PSID/RSID status

SID import routes to music and CONTENT discovers it. Generic `.sid` VICE autostart
is deliberately refused: PSID/RSID data/playback requirements are not ordinary PRG
autostart. A supported player/dispatch and fidelity/dual-SID qualification remain an
explicit later bounded product gate. No SID playback implementation in this work.

## S. Project CBM qualification media

Unchanged source `14e4ade77ec83e0429d194a6b5ecfa5ef7655e75`, private engineering bundle
SHA-256 `61673c45058ba31d2e28c699c631e99173c4e44b8b49c82c83735c2c5614d0af`.
The lock retains `pcbm-smoke.prg`, `pcbm-sid-check.prg`, `pcbm-video-input.prg` and
`pcbm-check.d64` with their original manifest/paths. Not substituted with third-party
media. New-image inclusion remains pending construction/offline validation.

## T. Security validation

Sudoers syntax passes. The appliance group has only exact no-argument configuration/
import helper entry points with versioned stdin requests, plus existing fixed power
policy; no NOPASSWD: ALL, arbitrary shell, generic mount or unrestricted systemctl.
Helpers validate operation/fields/paths/service identifiers, serialize writes and
return bounded results. User preferences need no root. Authenticated owner sudo is
deliberately separate and unrestricted for ordinary owner administration.

Fixtures/native negatives cover arbitrary commands/arguments, shell/path injection,
service allowlists, setup reset refusal and private input handling. No synthetic
password values were retained in logs; no builder credential dumps. Production-image
machine-id/SSH-key/residue checks remain pending because no new image exists. Public
rights checking continues to reject unresolved StrikeTerm public inclusion; Covers
retain their constituent-artwork review limit. Do not treat the accidental staging
copies described in A as sanitized evidence.

## U. Native Linux/build validation

Passed in new disposable native ARM64 Debian staging: actual package reinstall and
API/dependency checks; dpkg configure/audit/verify; APT check; AppArmor configuration;
visudo; first-boot/offline state; real owner PAM/sudo; Terminal and raspi-config;
Samba credential tooling; fresh SSH keys; optional service start/stop; NetworkManager
keyfile parsing/redaction; typed TCPser; USB loop import; installed info/config/boot
interfaces; optional-media preparation/install; mc PTY; SDL Covers lifecycle/timeout.

The original invalid builder-only TMPDIR reproduced both mktemp and AppArmor postinst
failure in a **new copy**. Corrected target environment then passed with `/tmp` mode
1777, 5,211,652,096 bytes staging tmpfs space, mktemp, AppArmor, dpkg and APT. No AppArmor
weakening. The documented explicit host/target boundary remains unchanged: TMP/TEMP/
TMPDIR, HOME/USER/LOGNAME/PATH, XDG, locales, proxies, Python/Git, CBM and loader/shell
variables cannot leak accidentally into target execution.

Pinned pi-gen `6fcca44892d5d4b36f826d2b8fb16d716369fada`; Lima 2.2.0/VZ plain native
ARM64 Debian13, 8 CPUs/10 GiB/160 GiB sparse disk. Host guard before/after staging passes,
inventory digest `352fb0f9ed6503e7570278573c8a04219856d8bde086c66e173c7d51c6dd0aa6`;
no builder package update, automatic-update masks preserved. No build ran, so no
before/after-image-construction claim. VM stopped; no loop devices remained.

Harness-only corrections retained: namespace temporary files fed via stdin rather
than expecting fresh `/tmp` to contain them; alsamixer --help exits zero with no text
on this package, so final assertion verifies exit plus package bytes rather than
inventing output. Initial assertion logs remain. Namespace shutdown reached its stop
timeout after tests and was terminated; this is not a product service failure.

## V. Package identities

| Package | Version / architecture | Source commit/tag or authoritative package source | SHA-256 |
| --- | --- | --- | --- |
| project-cbm-menu | 1.1.0~poc4.1-1+pcbm1 / all | `407ced58b711209631cdfb4db6dcd741a555f408` | `6df8fb42a10b16e12ac114032accc149c49ebf51f0e5f45c34b77d2cefbb2767` |
| project-cbm-runtime | 1.1.0~poc4-1 / all | `cf3a289f99bd7599c8e6f1aa3da4753aa733f981` | `fffbc2bd6b07b800e2562c8fc89a523e7e08df6bf0f7ce76786f9efebde9d303` |
| project-cbm-tcpser | 1.1.6~beta-1+pcbm1 / arm64 | `fe7feff4862406b277e009d14c219f5d16cf1222` | `8b8f8a4f3ec98dddf5bdb347320dad05e1bbe5230e0ee2727248c247a5af584f` |
| project-cbm-vice | 3.10-1+pcbm3 / arm64 | `VICE 3.10 source archive 8e5bac18cbcb9f192380ad3ef881f8790f5b75c41d7b3da65d831985d864d6d1` | `c9d798a591c22faa9ffc3141b7f5177ece36a05e53d9d2c8aae1ce93c22fcfbe` |
| alsa-utils | 1.2.14-1+rpt1 / arm64 | https://archive.raspberrypi.com/debian/pool/main/a/alsa-utils/alsa-utils_1.2.14-1%2brpt1_arm64.deb | `0751d5b8bb6812167c67b6b77e51cb85c97febad540bc75667a4a6a5899e800c` |
| mc | 3:4.8.33-1+deb13u1 / arm64 | https://deb.debian.org/debian/pool/main/m/mc/mc_4.8.33-1%2bdeb13u1_arm64.deb | `3b3e6d73b7305ef77e4ebc5a13277ce36704dc5d7a43d04034710d71429722ac` |
| mc-data | 3:4.8.33-1+deb13u1 / all | https://deb.debian.org/debian/pool/main/m/mc/mc-data_4.8.33-1%2bdeb13u1_all.deb | `b5ee7e2f5108c29a720675b1e0c9809741c85094e638e29b0c27bd56bdcc50bc` |

Menu requires runtime API exactly 1 and standard Bash/dialog/Python3/SDL2/SDL2_image/
coreutils/util-linux/procps/findutils/text tools/sudo/alsa-utils/mc. Runtime provides
API 1; info/config/backend/first boot are runtime/Menu payloads, not invented separate
packages. VICE keeps explicit minimal GL/GLX/Mesa/SDL2/ALSA closure; TCPser keeps its
existing libc dependency. SID-Wizard/StrikeTerm are declared prepared media, not new
Debian packages. All 705 frozen base binary-package descriptors and corresponding
source/host inputs remain in the lock's referenced closure; the [JSON companion](poc4-attempt3-prebuild.json) retains
exact component and relevant standard-utility descriptors. Reused packages were not
rebuilt merely to change hashes.

## W. Candidate identity

**Project CBM 1.1.0-poc.4 / private-engineering-poc4, build attempt 3**. The existing
factory separates attempts; owner permits that convention. Same bounded runtime
milestone, new source/Menu/lock identity. Not byte/input-identical to attempt #2,
not a beta/RC/public release and not a reproducibility proof. Integration source is
`b362c70215cef0e2c6c6a845635c47fd39b3ebbf`.

## X. Frozen release lock

`inputs/frozen-poc4-attempt3/release-lock.json`, SHA-256
`435c6e0d7a5a45eaff3f45af6d384fca5b602139fa9fb640950e2f5e7b4f39a9`.
2,832 object files, fully rehashed; schema/transitive closure/API/optional rights/media
verification passes. Frozen before the blocked construction request; never mutated
afterward. New Menu/source/recipe/build record and integration identity differ; unchanged
runtime/VICE/TCPser/base/qualification/optional inputs remain exact. Frozen input kit and
package/source artifacts are retained on TheBench; no internal large-image fallback.

## Y. Raw image

**NOT PRODUCED.** Path, size and SHA-256 are null, not borrowed from attempt #2.

## Z. Compressed image

**NOT PRODUCED.** Path, size and SHA-256 are null; raw/XZ equivalence NOT RUN.

## AA. Footprint/user capacity

New root used/free/ordinary-user available bytes and installed package-size sum are
**NOT MEASURED** without an image. Cover assets total 1,180,157 bytes; new Menu `.deb`
is 1,100,344 bytes. Source media sizes/hashes are recorded; they are not a substitute
for installed filesystem measurements. No minimum SD-card size is inferred.

## AB. Offline validation

New-image filesystem/FAT/ext4, complete ELF closure, identity/lock sealing, first-boot
state, service policy, applications, Covers, key/residue and raw/XZ checks: **NOT RUN**.
The additional Cover validator has positive and altered-asset negative fixture coverage;
it is not reported as a passed built-image check. Product 143, Menu 65 plus launcher
checker pass; native checks are separately listed in U. Prior attempt #2's successful
offline totals cannot be transferred to attempt #3.

## AC. Preservation

POC1/2: 5,503 baseline entries reverified. POC3 lock/raw/XZ and 2,789 frozen objects
reverified. POC4 attempt #1 checkpoint 23 files/2,834 retained files and attempt #2
checkpoint 25 files/2,874 retained files verify unchanged; their kits contain 2,809
and 2,812 objects respectively. Historical Project CBM preservation manifest rechecked.
Combian four files/metadata unchanged. No earlier qualification records rewritten.
Existing refs/tags remain except intentional feature-head advances and new Menu tag.
POC3 remains the last physically demonstrated Pi 3B foundation.

## AD. Git commits

| Repository | Commit | Purpose |
| --- | --- | --- |
| Menu | `407ced58b711209631cdfb4db6dcd741a555f408` | Versioned Cover candidate; Advanced Mixer/import feedback and tests |
| Product | `b362c70215cef0e2c6c6a845635c47fd39b3ebbf` | Bounded actual V3.7 audit; input freeze and offline Cover validation |
| Menu | `0da0d39d8e80811f0f76f7921274822ce1cd6f8c` | Final frozen-package / approval-blocked continuity |

Final continuity-only commits are recorded in the recovery `restore-report.json` and
the final handoff. They do not change frozen inputs. No authorization-policy commit
was created; the attempted AGENTS addendum is absent.

## AE. Repository status

Product `feature/1.1-build-foundation`; Menu `feature/1.1-debian-package`. Neither
feature branch has an upstream configured, so ahead/behind is not defined; retained
remote-tracking refs are unchanged (no fresh remote comparison claimed). Final clean
status and exact heads are verified in the recovery record. Nothing pushed/published.

## AF. Recovery checkpoint

New checkpoint: `archive/poc4-attempt3-prebuild-blocked-2026-09-16`.
Its `manifest.json.sha256` records the manifest digest without a self-checksum cycle.
Both full Git bundles, exact refs/peeled tags and offline mirror fsck results are in
`restore-report.json`. `retained-evidence.json` enumerates only reviewed bounded files;
the frozen-input manifest inventories all 2,832 input objects. The two accidental
staging-tree copies are explicitly excluded and need approved cleanup. No images or
credential stores belong in the checkpoint. Independent backup/custody outside the
Mac/TheBench failure domain remains unresolved; this is not an independent backup.

## AG. Pi 3B procedure

[Attempt #3 procedure draft](../qualification/poc4-attempt3-pi3b-smoke-test.md) binds the
candidate and frozen lock, but deliberately has **no image hashes and is NOT READY TO
FLASH**. It includes first boot/offline and required no-Ethernet Wi-Fi, owner/admin,
config/info, C64/second/content-specific Covers, mc, Advanced Mixer, VICE geometry,
joystick/audio/owned media, USB, optional services, SID-Wizard and StrikeTerm. Only
after a successful build and full offline validation may exact raw/XZ hashes finalize
it. Do not use attempt #2's image to qualify Covers.

## AH. Remaining uncertainties

- **Approval blocked:** image construction; cleanup of exact accidental staging copies.
- **Physical Pi:** first boot/expansion/interruption, KMS/VT/Cover-to-VICE transitions,
  keyboard/joystick/audio, utilities, USB discovery, state persistence, C64 applications.
- **External environment:** required no-Ethernet Wi-Fi radio/AP, Ethernet, Samba/SSH
  clients, mDNS and authorized BBS endpoint. Missing equipment is UNTESTED, not FAIL.
- **Deferred product:** proper PSID/RSID player; boot presentation/performance after
  successful physical qualification; no new architecture study needed.
- **Public rights:** StrikeTerm unresolved; constituent Cover graphics/font review;
  owner-supplied reference media remain excluded.
- **Independent evidence:** clean-rebuild reproducibility and independent recovery
  custody/restore remain unproven. New inputs differ from prior attempt by design.

## AI. One next owner action

Review and resolve the automatic-approval block for the **already frozen attempt #3**
construction and the exact accidental-copy cleanup described in A. Resume that single
build only after the block is resolved; do not re-freeze inputs, rebuild unchanged
packages, flash attempt #2, or start another milestone. Physical testing follows only
if construction and complete offline validation pass.
