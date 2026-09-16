# Runtime activation / private POC4 attempt — stopped

2026-09-16. **No new image exists. This milestone is incomplete.** The owner-required
build-integrity stop was exercised. Do not test another Pi, flash a guessed artifact,
retry the build, optimize boot or publish. POC3 remains the physically demonstrated
Pi 3B baseline. [Machine-readable inputs/results](poc4-blocked.json).

## Executive result and blocker

Source/runtime integration, meaningful native Linux staging, matching Debian packages
and a schema-4 frozen input lock were completed. The new image build failed in
upstream pi-gen **stage1**, before the Project CBM integration stage or image export.

The invocation incorrectly exported the builder-only environment value
`TMPDIR=/srv/project-cbm/staging/runtime-activation`. pi-gen's target chroot inherited
it. AppArmor 4.1.0-1's package configuration called `mktemp`, which could not create
its file because that path does not exist inside the target root. dpkg returned 1;
APT/build returned 100. This was an operator invocation/environment-boundary error,
**not evidence that AppArmor, Lima/VZ, the frozen package closure or the Pi is defective**.

No package-maintainer-script bypass, AppArmor removal, input mutation, partial-image
repair or build retry was performed. The complete failed tree is retained in the
Linux guest at `builds/private-poc4`; it is not a usable appliance. No artifact export
directory was created. Post-failure checks confirmed the pinned host package inventory
and masked update units, no build loop devices/mounts and no frozen-input proxy process.

Build evidence under configured external bulk storage:

- `qualification/poc4-build-blocked-2026-09-16/poc4-build.log` — SHA-256
  `a2c5e9391f803d877145bbd002f542ab8b042c370a2dc9d73d670e27e39c3c91`.
- `qualification/poc4-build-blocked-2026-09-16/apt-frozen.log` — SHA-256
  `793a0ba196d92792d8a78a7325021cb32513da124aea7a13d5c1e95888893567`.
- The earlier source-package exclusion failure is preserved separately. Its corrected
  attempt produced the packages below; it did not bypass dpkg source consistency.

## Implemented source and native evidence

Detailed decisions and test limitations are in [runtime-activation.md](runtime-activation.md).

| Area | Implementation / evidence | Remaining limitation |
| --- | --- | --- |
| First boot | Existing sole root-growth owner; root-owned region → owner → network → finish state, atomic markers; offline completes; completed setup cannot reset owner password | Real boot ordering/power loss and complete UI on Pi untested |
| Owner administration | Locked `owner` UID1001, ordinary authenticated Debian sudo; no preset password; password through PAM stdin | New image not constructed; physical owner login untested |
| Advanced | Authenticated `su --login owner` returning shell; authenticated sudo raspi-config | Native pseudo-terminal success/failure/return and vendor noninteractive invocation passed; full Pi UI pending |
| Normal privilege | Fixed schema-1 JSON requests; no-argument root helpers limited to `%pcbm-operators`; no generic command/path/unit API; pi removed from sudo group during construction | Stage activation not reached in image build |
| Network | Standard NetworkManager, initial networking/radio off; fixed WPA-personal keyfile; country, discovery, disconnect/forget, hostname | Native keyfile/secret/offline tests pass; hardware Wi-Fi/Ethernet/DHCP untested |
| Services | Deliberate Samba, SSH, TCPser and mDNS enable/disable; all default off; explicit preset policy | Native start/stop passed; LAN/SSH login/BBS functionality untested |
| Samba | Separate Samba password via stdin, fixed content-only share | No assertion Unix and Samba credentials synchronize |
| SSH | Owner-only login, root login denied, fresh keys on explicit enable | Native keys/config/start-stop pass; no image keys shipped because no image exists |
| TCPser | Typed port/baud; loopback IP232 and loopback ephemeral inbound listener; no trace flags | Outgoing modem design; no public inbound-BBS setting or real BBS test |
| USB import | Allowlisted USB partition discovery, revalidation, read-only mount (`noload` for ext4), UID1000 bounded copy, no overwrite/symlink traversal, cleanup | Synthetic loop copying passed with explicit test discovery; actual USB/hot unplug pending |
| Boot preference | User-owned preference; at most one direct profile launch, then Menu on exit/failure | Static contract only; physical boot preference untested |
| Information/configuration | Existing pcbm-info JSON, System Information/About and Bash/dialog configuration packaged together with API dependency | Installed info JSON and fixture UI tests pass; new image absent |
| Geometry/media | Existing VICE package, getty/PAM, defaults, diagnostics and owned qualification suite retained as inputs | POC3 passes do not qualify changed runtime |

Passwords are excluded from command arguments, results and evidence. Synthetic
native-test credentials were invalidated; generated staging SSH keys were removed.
The disposable root, Samba databases, journals and credential stores are **not recovery
artifacts**. The namespace harness needed a forced stop after its 20-second timeout;
MainPID was zero afterward and no namespace/build mounts or loops remained. This does
not establish appliance shutdown behavior. No host container platform was installed.

The source suite passes **138 product tests + 50 Menu tests**, plus the shared launcher
checker. Native final package installation, dependency/payload verification and sudoers
syntax passed. Do not describe all milestone validation as complete: target image,
full first-boot UI, application working-copy runtime and physical services remain gates.

## Optional applications and reference content

**SID-Wizard 1.97:** accepted author archive SHA-256
`aeb265f4a778b2acb5aad13e8e98af882888292f749f29f4d18cbf49850e57bc`.
Only native SID-Wizard/SID-Maker and retained notice; no example music, instruments,
host tools or full manual. Exact member identities and permissive author notice remain
in [the accepted pin](../../build/optional/sid-wizard.json). Deterministic D64:
`cec93ae1fd5fc846507c1883fd9cb210c6a3c0f40c1c081964e3b8450e26dc44`.
Payload tar: `46872e5c937f681fa161a2acf88937040f2b90a091b03d8153513035bd62223e`.
Frozen-input verification regenerated/compared the payload in Linux. Intended immutable
template: `/usr/share/project-cbm/applications/sid-wizard/SID-Wizard-1.97.d64`;
pi-owned working disk: `/home/pi/pcbm/music/Creation/SID-Wizard/SID-Wizard-1.97.d64`.
Source tests preserve existing state; actual application editing/save/relaunch remains
untested. No new image contains it yet.

**StrikeTerm 2014 Final, Alwyz:** 174,848-byte D64 from the author's endorsed
[CSDb artifact](https://csdb.dk/getinternalfile.php/129890/st2014final.d64), SHA-256
`72b803c54c7892857c0ddb5674dabc841d59a496285975546bef689308940595`.
It matches the previously recorded Combian copy. See
[the private admission record](../../build/optional/striketerm.json).
Classification stays **PRIVATE-ENGINEERING-ADMITTED / PUBLIC-RELEASE-RIGHTS-GATE-PENDING**.
The exact bytes are frozen, but the integration stage never ran. Intended working disk:
`/home/pi/pcbm/programs/Communications/StrikeTerm/StrikeTerm-2014-Final.d64`.
No launch, VICE compatibility or BBS connectivity pass is claimed. The public-purpose
rights checker rejects this input; owner permission for private testing is not public
redistribution clearance.

All requested third-party SID/demo references, including Wonderland XIV, remain
**OWNER-SUPPLIED / NOT BUNDLED**. Their bytes were not acquired. Normal SID import is
retained; the shared launcher explicitly refuses generic `.sid` autostart. Correct
PSID/RSID playback remains a separate bounded product gate.

## Frozen inputs and packages

Candidate **attempt**: `1.1.0-poc.4 / private-engineering-poc4`.
Integration: `cf3a289f99bd7599c8e6f1aa3da4753aa733f981`.
pi-gen: `6fcca44892d5d4b36f826d2b8fb16d716369fada`, existing arm64/Trixie closure.
Menu tag `v1.1.0_poc4`: object `ddd6b681b9ce5d8bd6887eefb8357968bcc41373`,
peeled `bb8a66ea9da994b30f978ad87d61c9aedb03dad6`.

Lock: `inputs/frozen-poc4/release-lock.json`, SHA-256
`99f3985b8eac77398fbc71d66160f91beff50d04f6ae246757a4f081436bfacc`.
This is frozen failed-attempt evidence, not a released or bootable candidate.
The Menu depends on `project-cbm-runtime-api (= 1)` and the runtime provides it;
retained-input verification checks that interface dependency.

| Package | Version / architecture | SHA-256 |
| --- | --- | --- |
| project-cbm-runtime | 1.1.0~poc4-1 / all | `fffbc2bd6b07b800e2562c8fc89a523e7e08df6bf0f7ce76786f9efebde9d303` |
| project-cbm-menu | 1.1.0~poc4-1+pcbm1 / all | `b1c95d128eb0f9b3d9ba59528ed7be39d7f94cf158933bd74c83f0eecb83999d` |
| project-cbm-vice (unchanged) | 3.10-1+pcbm3 / arm64 | `c9d798a591c22faa9ffc3141b7f5177ece36a05e53d9d2c8aae1ce93c22fcfbe` |
| project-cbm-tcpser (unchanged) | 1.1.6~beta-1+pcbm1 / arm64 | `8b8f8a4f3ec98dddf5bdb347320dad05e1bbe5230e0ee2727248c247a5af584f` |

Source/binary/buildinfo/changes/logs: `packages/poc4-final`. Full component descriptors
and optional inputs are in the JSON report. New source archives are retained alongside
the kit; no complete recovery kit, source tree or development cache was put in an image.

**Raw/XZ path, size, SHA-256: unavailable — no image produced.** Offline image checks,
filesystem integrity/raw-XZ agreement, installed footprint and post-expansion content
capacity were not measured. No minimum card size is established. Independent clean
rebuild reproducibility remains unproven.

## Storage, preservation and recovery

Lima 2.2.0/VZ, Debian 13 arm64, 8 vCPU/10 GiB, 160 GiB sparse disk; guest kernel
6.12.107+deb13-cloud-arm64. VM remains disposable. State/disk on TheBench under
`build-host/lima`, cache under `cache/lima`, Linux build work under `/srv/project-cbm`.
No large build data was redirected to the Mac internal SSD.

Measured free space before/after: internal 81,100,800,000 → 77,004,800,000 bytes;
TheBench 1,036,288,000,000 → 1,028,096,000,000 bytes. These are observed host totals,
not proof every change was attributable to this task. Disk logical size 171,798,691,840;
allocated 82,562,383,872 bytes; guest free 79,943,655,424 bytes. Failed pi-gen execution:
42.99 seconds, maximum RSS 173,716 KiB, no swaps. These are not full-build budgets.

New checkpoint: `archive/runtime-activation-blocked-2026-09-16`. It records exact final
repository refs, bundles and offline restoration, plus preservation and retained-input
verification. POC1–3 baseline images/locks/packages remain unchanged. All 5,503 POC1/2 baseline entries and 2,789 POC3 input objects were rehashed;
POC3 raw/XZ/lock hashes match. The new kit has 2,809 verified objects. The VM is stopped.
No existing tag, release, published history or historical qualification record was rewritten; no push.
Independent backup/custody remains unresolved: this checkpoint is on the same device.

## Exact next owner action

Review this failure and authorize a bounded construction-environment correction and
fresh attempt. The recommended correction is to separate builder temporary paths from
target-chroot environment, test that boundary, and give package scripts a valid target
`/tmp`. Linux guest `/tmp` is inside the TheBench-backed virtual disk; it is not the
Mac internal `/private/tmp`. Do not remove AppArmor or bypass its maintainer script.

Keep this failed tree/lock/logs immutable. Use a new attempt directory and, if recipe
bytes change, a new declared integration identity/lock; never overwrite this lock.
Finish remaining staging and offline gates. Only after an image passes should the
[physical procedure outline](../qualification/poc4-pi3b-plan.md) be bound to its exact
raw/XZ hashes and submitted for owner Pi3B testing. No physical testing is ready now.
