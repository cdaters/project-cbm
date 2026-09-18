# Private POC4 attempt #7 — release-readiness refinement

**READY TO FLASH: YES. Stop for owner Pi 3B physical testing.**
[Exact results](private-poc4-attempt7.json), [physical procedure](../qualification/poc4-attempt7-pi3b-regression.md).
All 253 actual-image checks and raw/XZ equivalence pass. This new candidate's physical
behavior is UNTESTED. Nothing pushed or published. Recovery verification is recorded
externally under `archive/poc4-attempt7-2026-09-18`; its manifest/restore report is the
checkpoint authority. Independent custody is still open.

## Baseline, decisions and implementation

[Attempt #6 owner report](../qualification/poc4-attempt6-pi3b-owner-report-2026-09-18.json)
records only the supplied Pi 3B results: first boot/Wi-Fi/masking/range rendering/Main
Menu IP/correct visible Covers/VICE/Menu/input and reported persistence PASS. Active-VICE
VT shortcut and observed macOS sharing discovery FAIL. Unreported behavior is UNTESTED.

[Bounded decisions](../runtime/release-refinement-2026-09-18.md): keep useful contextual
connection help from v1.0/Dosbian ideas, copy no third-party implementation/default
passwords. Main Menu is compact; Network/Services and each service add authoritative
actual state, useful actions and connection help. On requires activity and the expected
listener. Normal wording uses Computer Name, File Sharing, Remote Access and Network
Discovery. `pcbm-info --json --appliance` is the single authority; Menu does not probe.

Default Computer Name is projectcbm and remains editable. Existing owner account/UID
is preserved; SSH uses the first-boot owner password. File Sharing clearly uses a
separate password for owner, with writes mapped to pi inside the content-only share.
Sharing opt-in explicitly enables existing Avahi discovery; Samba dynamically advertises
SMB. No new discovery daemon, no guest share, no password in argv/logs/diagnostics.

Pinned SDL disables kernel keyboard processing and leaves its console-switch key handler
empty. Its debug keep-keyboard option would leak keys into the console. No fragile VT
workaround was applied; F10 → Quit before switching is the accepted limitation. Covers,
VICE geometry, getty/PAM/TTY/session ownership and all seven artwork bytes are unchanged.
Rainbow/startup output and quiet/fast boot remain deferred separately.

## Source, packages and lock

Integration `33347bb9c11e87e70069da5d160e03ec197efe31`. Menu `v1.1.0_poc4.5`,
peeled `4c88fa38ce28c63b6342adfb5d7a084a21248684`, annotated object
`5e80d20cddbeb1a52dc5c3e1d0dc3576f31cc110`. Clean source was exported by the documented
factory helper. Only Runtime and Menu were rebuilt; VICE/TCPser, base/host closures,
pi-gen/patches, artwork and existing optional/private admissions reuse verified bytes.

| Package | Version | Input | Bytes | SHA-256 |
| --- | --- | --- | ---: | --- |
| menu | 1.1.0~poc4.5-1+pcbm1 | NEW | 1106552 | `de724923dc088838cfaea9c7699b28e3a8df86b623a385caec61b08c7eef0f5a` |
| runtime | 1.1.0~poc4.4-1 | NEW | 42324 | `822165eb18ed75aea402ff5868d73b1cd2cf822e8286dd510deb65dd992744ae` |
| tcpser | 1.1.6~beta-1+pcbm1 | REUSED | 26872 | `8b8f8a4f3ec98dddf5bdb347320dad05e1bbe5230e0ee2727248c247a5af584f` |
| vice | 3.10-1+pcbm3 | REUSED | 4650184 | `c9d798a591c22faa9ffc3141b7f5177ece36a05e53d9d2c8aae1ce93c22fcfbe` |

Exact filenames and corresponding-source records are in the JSON result and frozen
lock. Lock `inputs/frozen-poc4-attempt7/release-lock.json`, schema 4, 2,956 objects;
SHA-256 `1c25d7f7850c63c41e2730bdaef2deef9cd6d0ccf1321c9b23fd4d9228926b3d`.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `artifacts/private-poc4-attempt-7/2026-09-18-project-cbm-1.1.0-poc.4-lite-private-poc.img` | 3087007744 | `cbab8327981eaf0d1d632d6637d3117fd2c2d68ac6d529c434b52fed995b60ba` |
| `artifacts/private-poc4-attempt-7/image_2026-09-18-project-cbm-1.1.0-poc.4-lite-private-poc.img.xz` | 598188816 | `b8119c4f3bb1c9361cd4d0c047eaa454447884e36dad9d345b50673ba9e7b687` |

Locators are relative to configured bulk storage, currently `/Volumes/TheBench/ProjectCBM-Work`.
Raw/XZ equivalence passes in the builder and after external transfer; finished images
were not edited. Controlled construction took 157.35 seconds, process peak RSS 510832 KiB.
This is not proof of independent-build bit-identical reproducibility.

## Tests and limits

Product host/native **184/184**; Menu host/native **96/96**; installed lifecycle **10/10**.
Native actual service start/stop, listener confirmation, enabled/restart persistence,
Computer Name/local resolution, safe enrollment and content-share boundaries pass.
Real owner/password SSH login and refusal after disabling pass. Samba/Avahi responds to
a local SMB mDNS query on a synthetic isolated interface. Real dialog service screens
render/cancel at 40x12, 80x24 and 100x36. Native import/MC/ALSA-tool availability and
network/tty fixtures pass within their recorded scope. Status refresh took 49.67-50.62 ms
in the VM; no Pi timing claim. Physical client SMB authentication, Finder/Explorer,
radio, reboot persistence and optional utilities remain explicit procedure items.

Actual image: **121 main + 20 supplemental + 112 refinement = 253 checks PASS**;
672 package identities, 127 ELF objects, FAT/ext4 checks, systemd, exact installed
identity/payload/docs, service/account/discovery/security/privilege and lifecycle PASS.
Host inventory/update/capability guards pass before/after; no build mounts/loops remain.
Initial source fixture/schema and native harness errors are retained with corrected
passes. macOS lacks dpkg-deb; full kit/package metadata verification ran in Linux,
and every external object/descriptor byte was separately hashed. No gate was bypassed.

Root capacity 2430955520, used 1651630080, user
available 635461632 bytes before expansion; boot used
78420992 bytes. Native overlay writes 16293888;
changed packages compressed 1148876 plus installed
1522688 bytes. Reserving those measured amounts leaves
616496180 bytes. This is not a full OS upgrade
or physical first-boot peak guarantee; no nominal card minimum is invented.

## Documentation and readiness

Current entry: [documentation](../README.md). Authoritative guides:
[user](../release/user-guide.md), [networking/services](../release/networking.md),
[Build Your Own](../release/build-your-own.md), [pi-gen factory](../release/factory.md),
[customization](../release/customization.md), [developer](../release/development.md),
[user recovery](../release/recovery.md), [engineering recovery](../recovery.md).
The seven release guides ship in the Runtime package. Old 1.0 entry points are labeled
historical. The real build commands were exercised; the retained private-kit prerequisite
and public-bootstrap/rights limits are explicit. Source checks cover syntax, JSON,
links/paths, sizes, secret patterns, whitespace and unchanged governance.

- **RELEASE BLOCKER:** existing public redistribution gates must be resolved or gated
  content omitted before a public release. No publication is authorized here.
- **PHYSICAL QUALIFICATION REQUIRED:** the exact-hash Pi 3B procedure; then the separate
  quiet boot, measured fast boot and final RC polish milestone. No other model claims.
- **DOCUMENTATION FOLLOW-UP:** add physical outcomes. Release/user/build/customization
  guides are complete for this implementation.
- **OPTIONAL POST-1.1 IMPROVEMENT:** supported active-VICE VT handling and Windows browse
  enhancement if justified. Independent rebuild/custody verification remains open.

This candidate can be the release-candidate basis after physical qualification and the
planned final polish; it is not a public RC declaration. Owner: flash the exact new
image and perform the linked procedure. Stop early on a critical regression and preserve
evidence. Do not repair the qualification image or start another feature milestone.
