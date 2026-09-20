# Private RC4 — attempt 14

The owner authorized one bounded final release-polish candidate. RC3 and its frozen
inputs, image and history remain unchanged. **READY TO FLASH: YES after the external recovery manifest and offline restore report
verify PASS. Physical RC4 qualification remains UNTESTED.**
Use the [exact-hash Pi 4 B procedure](../qualification/rc4-pi4b-regression.md).
[Machine-readable results](private-rc4.json) contain all hashes, package identities and limits.

## Scope

- CCGMS 2021 replaces bundled StrikeTerm using the approved one-program disk. The
  verified PRG is unchanged; seven unrelated upstream compilation files are omitted.
  Source, BSD 3-Clause notice, credits and provenance ship with the application.
- Existing x64sc/TCPser integration uses temporary SwiftLink `$DE00`/NMI/IP232 flags
  only for CCGMS. Initial 2400-baud settings and opt-in listener policy are retained.
- G71 discovery uses compatible C64/C128 1571 routing. Legitimate dot-prefixed supported
  content remains visible; known host-OS metadata remains excluded.
- File Sharing's password prompt states that colon is excluded.
- Menu copyright separates MIT code from Craig Daters' release-authorized branding
  and Covers. Artwork bytes remain unchanged. Approved VICE ROM policy and deferred
  signing/formal SBOM/public bootstrap are recorded in [release policy](../release/release-policy.md).

The [CCGMS integration record](../runtime/ccgms-integration.md) retains exact source/PRG
identities and evidence limits. No VICE/TCPser rebuild, Pi3 optimization, new feature,
architecture redesign, final release tag, push or publication is authorized here.

## Validation before freezing

Host Product 244/244 and Menu 102/102 PASS. Native ARM64 Product 244/244 and Menu
102/102 PASS after providing preserved Git history required by two reference tests.
The initial tar-only harness failure is retained; no failing test was waived.
Existing installed lifecycle 12/12 and native service/authentication/SSH/discovery,
network status, MC and import checks PASS. Native CCGMS boots, exchanges text through
VICE/TCPser with a local endpoint, hangs up and exits. G71 autostart works with installed
x64sc/x128 and 1571. New focused final runs and packaged tests are recorded externally.

A real VICE CLI check corrected the ACIA selector spelling to `-myaciadev`; no VICE
code changed. Native probe failures caused by output encoding/monitor handshake were
kept as harness evidence and corrected. Native results are not Pi physical claims.

## Preserved pre-construction freeze failure

Attempt13 produced valid packages but its freeze rejected the CSDb query-bearing
publication URL under the existing credential/query-free origin contract. No lock
was completed and no image construction began. The failed input directory and log
are retained. Attempt14 uses the already verified author publication URL as lock
origin, with the CSDb release reference retained separately in the provenance pin.
No payload, licensing decision or privilege rule changed. Installed Runtime/Menu
payloads are unchanged; a new source export preserves accurate build correspondence.

## Completed candidate gates

Runtime **1.1.0~rc4-1** and Menu **1.1.0~rc4-1+pcbm1** are new; VICE **3.10-1+pcbm4**
and TCPser **1.1.6~beta-1+pcbm1** retain their verified package identities. Both fresh
attempt14 package builds matched attempt13 `.deb` bytes exactly; the corrected origin
changed provenance/factory inputs, not installed package payloads. Original package
and failed-freeze outputs were preserved, not replaced.

The new lock is `inputs/frozen-poc4-attempt14/release-lock.json`, SHA-256
`ced936a75aebf2f45d30052da85ba35f00fe9881d0d59f1938b1d64c84c1d5df`. All 3,157 external kit files match native sizes/hashes;
full semantic/Debian verification passes in the native builder. The failed attempt13
kit's 3,154 files are preserved separately. The one constructed image has correct RC4
filenames and installed identity.

Actual-image **324 checks PASS: 119 main + 20 supplemental + 185 corrective**. This
includes 672 exact installed package/version/architecture identities, 127 ELF objects,
FAT/ext4, both initramfs images, CCGMS-only disk/source/license/provenance, no bundled
StrikeTerm/private admission, user ownership, services, privileges, lifecycle and
shipped manuals. The disk is one unchanged CCGMS PRG; its exact disk/program/source
hashes are in the machine-readable report. Native AT/text/disconnect/relaunch and
C64/C128 G71 BASIC tests pass. Real Pi BBS/keyboard/display workflow remains untested.

Raw and XZ hashes/equivalence pass natively and independently on the external Mac
copy. Build-host inventory is unchanged, update guards and AppArmor are preserved,
capabilities pass before/after, and no build mounts, loops or emulator processes remain.
Root user-available space is about 639 MB before first-boot expansion; maintenance
headroom beyond measured free space and expanded card capacity are not newly qualified.

Historical preservation manifests pass; RC3 raw/XZ/lock are unchanged. Recovery is
`archive/rc4-2026-09-20`, with full Git bundles, exact refs/peeled tags, offline restored
source and fsck verification. Its external manifest and restore report are the final
readiness authority. TheBench is not independent encrypted custody; that limitation
remains explicit. A second folder is not an independent backup.

## Owner next action and release status

Flash the exact new image and perform the affected-area Pi4 B procedure. Preserve
unchanged owner-reported results; do not repeat broad Pi4 benchmarking unless a
regression appears. Required new physical evidence covers CCGMS connection/text/
disconnect/return/relaunch, content/import changes, sharing prompt and core smoke.
G71 without suitable owner media must be reported UNTESTED, with release disposition.

Formal signing, standardized SBOM and public bootstrap remain approved post-1.1 work.
Final source/notices/checksums and publication still require the separate final release
milestone after owner physical qualification. Nothing was pushed or published and
no final 1.1.0 tag was created. Stop here for owner qualification.
