# Project CBM 1.1.0 RC1 basis — private attempt #9

**READY TO FLASH: YES only with the verified recovery checkpoint below.**
[Exact results](private-rc1.json) · [Pi 4 B physical procedure](../qualification/rc1-pi4b-regression.md).
All **283 actual-image checks**, package/ELF closure and raw/XZ equivalence
pass. This is a private RC1 basis, subject to owner physical qualification; it is not a
published release. The recovery manifest/restore report is the final external authority.

## Physical baseline and policy

The [exact attempt8 Pi4 report](../qualification/poc4-attempt8-pi4-owner-report-2026-09-19.json)
records normal x64sc playing the private Oxyron reference correctly. Retained telemetry:
29 consecutive non-warp samples,145.219s, weighted100.002%, minimum99.977%. The final
20.357% interval was owner-confirmed quitting and remains preserved. Saved VICE settings
differ from the fresh seed (including VICIIGLFilter=1); no preference was changed for
evidence collection. Card/removable identity and read-only mount were verified first.
No live hardware-health values were recovered from that offline card. No unreported
function or another model is qualified. Pi3 failures remain intact; the owner explicitly
changed the1.1 release floor to Pi4-class and newer. No further Pi3 tuning/core switch.

Unchanged Pi4 boot: kernel2.390s + userspace16.960s =19.351s. Getty tty1 at9.956s follows
NetworkManager service4.143s, not wait-online5.966s. The latter gates Samba/graphical
readiness. Power-to-interactive-Menu was not measured. Timing details are in the JSON.

## Final decisions and changes

- Canonical library **/home/pi/pcbm** remains owned by runtime pi. Administrator/SSH
  **pcbm** retains **/home/pcbm**. Existing code already specified the runtime library;
  the owner's reference was uploaded to the administrator home, outside that library.
  No unsupported claim of an automatic account-driven library move is made.
- Type-first categories and machine subfolders preserve the v1.0.0/user menu model:
  demos/c64, games/vic20, programs/pet, etc. Machine-aware import/profile routing and
  FILES' explicit library start remove ambiguity. Shared means intentionally unclassified
  or cross-machine material, using RUN's default; no format-folder sprawl. Existing
  files are not moved/deleted. [Content guide](../release/content.md) documents safe
  optional copy from misplaced administrator uploads and supported media distinctions.
- SID-Wizard/StrikeTerm working disks use music/c64/Creation and
  programs/c64/Communications. Upstream disk/source bytes and rights classifications
  remain unchanged; only path-bearing manifests/recipes changed. No owner demo is bundled.
- Gateway/DNS join the existing bounded pcbm-info device query and detailed views;
  Main Menu stays concise. Menu adds no network probes or credential reads.
- Quiet firmware/kernel/service presentation and simple Project CBM console text use
  the existing login session. Root/console/KMS/getty/PAM/first-run/Cover/VICE owners
  remain unchanged. A protected valid completion marker now skips repeated root growth
  and global sync. Native completed calls took about13ms; Pi speedup is UNTESTED.
  Network readiness, Samba, EEPROM, swap and filesystem checks remain enabled as before.
- Normal C64 remains x64sc with the exact attempt8 VICE package. No fidelity/geometry/
  audio/keyboard/F10 or active-VICE VT workaround was introduced.

## Validation and limits

Product208/208 and Menu97/97 pass on host and native ARM64 Linux. Three additional
validation-only tests pass on both. Installed lifecycle10/10, seven SDL dummy Covers,
three repeated cycles, real isolated service transitions, owner authentication/SSH,
local SMB mDNS, real dialog sizes, USB-loop import/no-overwrite/symlink/ownership and
read-only-source checks pass. These do not qualify physical KMS/Wi-Fi/client discovery.

An initial test checkout lacked historical Git fixtures and used a group-writable
synthetic marker under the builder umask; both fixture failures are retained/corrected.
Preconstruction then caught an inherited validator requiring the old NM field list.
The external RC1 validator now requires the exact expanded allowlist, rejects secret/
connection probes and never executes target code. Initial failure and corrected passes
are retained; frozen integration/packages/lock were not rewritten. Validation source
SHA-256: `a26c66fb20bade34dd74b970fa43f35b641139f2d805e840a10e4617a80d0b10`.

Actual image:121 main +20 supplemental +142 refinement =**283 checks**, **672** installed
package/version/architecture identities and **127 ELF objects**. FAT/ext4, identity,
first-boot/account/service/discovery/privilege/security/lifecycle/docs/boot/content
contracts pass. Build170.19s, peak503092KiB. Host inventory/update/capability guards pass
before/after; builder stopped with all earlier state retained. One image constructed.
Independent-build byte reproducibility and independent backup custody are not claimed.

Root user-available space before expansion: **639598592 bytes**;
conservative native/package allowance leaves **619601604 bytes**.
This is not a physical first-boot peak or whole-OS-upgrade guarantee; actual expanded
capacity depends on media. No unsupported nominal card minimum is imposed.

## Packages and frozen input

| Package | Status | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| project-cbm-menu_1.1.0~rc1-1+pcbm1_all.deb | NEW | 1106844 | `ff5cca1f1305a2d9b79c76a8a303bf2f4dcc82eb35c9a2a7bc377b86a602eeb9` |
| project-cbm-runtime_1.1.0~rc1-1_all.deb | NEW | 65952 | `9dbeb0e27b7f1925fe906bad5ac353afbe34e286318a9d9d6dac7a131ce875c7` |
| project-cbm-tcpser_1.1.6~beta-1+pcbm1_arm64.deb | REUSED | 26872 | `8b8f8a4f3ec98dddf5bdb347320dad05e1bbe5230e0ee2727248c247a5af584f` |
| project-cbm-vice_3.10-1+pcbm4_arm64.deb | REUSED | 5069684 | `a7b77c3b006eb190c64c10cadbfd91ce4152a73523c440496209293da2901dc1` |

Integration `8401248a94132b386f9d6804823e0c4e3cd247dc`. Menu annotated `v1.1.0_rc1` object
`ae7abc27abf11141e53442251c5e2706bf7e274f`, peeled
`4346a350d481f4da3a6abc6524373333637dbb82`.
Lock: `inputs/frozen-poc4-attempt9/release-lock.json`; SHA-256 `e586ae09b6ff486239dc93f814171f0ce0dd0f0fe8bf8b62f3c06f96a345fd9f`.
All 3033 retained objects verify after external transfer.
Package manifest: `qualification/rc1-2026-09-19/packages.json`;
SHA-256 `121fa312638b83cf277fdd610e1c6b6a76b8e2aeb62f90c152e3a94070e6d51d`.

## Artifacts and recovery

Paths below are relative to the configured external bulk workspace.

Raw: `artifacts/private-rc1-attempt-9/2026-09-19-project-cbm-1.1.0-rc.1-lite-private-rc1.img`; **3095396352 bytes**;
SHA-256 `7edc2452529dea92623b07a42036ce74ac7c7b84968d449336cdb4f250578115`.

XZ: `artifacts/private-rc1-attempt-9/image_2026-09-19-project-cbm-1.1.0-rc.1-lite-private-rc1.img.xz`; **599213904 bytes**;
SHA-256 `84057184795bc05a805e9aa4e8caf971e47f8fbc084396365a671611377798e0`.

Guest and external raw/XZ equality **PASS**. Qualification records:
`qualification/rc1-2026-09-19`. Recovery: **archive/rc1-2026-09-19**; verify its manifest
and offline restore report PASS. Full bundles/ref/tag/fsck restoration, retained inputs,
artifacts and original preservation are required. The stopped pre-growth disk/config
checkpoint is `build-host/records/pre-rc1-disk-growth-2026-09-19`, manifest
`26f9294e0361091dcb8e92203fb491590d632994c5039ccf12f4968fe8574ee1`.
TheBench is not independent custody; preserve an independent encrypted copy separately.

## Documentation and RC assessment

The [release entry point](../README.md) links [user manual](../release/user-guide.md),
[network/services](../release/networking.md), [Build Your Own](../release/build-your-own.md),
[factory/pi-gen](../release/factory.md), [customization](../release/customization.md),
[VICE](../release/vice.md), [accounts/layout](../release/accounts-and-layout.md),
[content](../release/content.md), [boot](../release/boot.md),
[development](../release/development.md) and [recovery](../release/recovery.md).
Eleven release documents,79 local links and explicit source paths pass the audit.
The actual private package/freeze/build walkthrough was exercised. Public bootstrap
and rights-cleared input publication remain explicitly incomplete, not hidden behind
private predecessor kits.

- **RELEASE BLOCKER:** public redistribution rights and public build bootstrap/input
  delivery remain unresolved; no failing RC1 offline gate remains.
- **PHYSICAL QUALIFICATION REQUIRED:** exact Pi4B procedure, including fresh seeded
  performance, quiet boot/recovery, timing, content/import and network/service regression.
- **DOCUMENTATION FOLLOW-UP:** append actual owner outcomes and eventual authorized
  public versioned input/manifest guidance.
- **OPTIONAL POST-1.1:** supported VICE-active VT, justified Windows browsing improvement
  and further measured boot optimization. No new feature milestone is started.

Nothing pushed or published. Flash the exact new image and perform the hash-bound
Pi4B RC1 procedure, then report outcomes. Stop for owner physical testing.
