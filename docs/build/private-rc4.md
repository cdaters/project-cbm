# Private RC4 — attempt 13

The owner authorized one bounded final release-polish candidate. RC3 and its frozen
inputs, image and history remain unchanged. This record is updated with exact final
identities after construction and validation; until then **READY TO FLASH: NO**.

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

Host Product 243/243 and Menu 102/102 PASS. Native ARM64 Product 243/243 and Menu
102/102 PASS after providing preserved Git history required by two reference tests.
The initial tar-only harness failure is retained; no failing test was waived.
Existing installed lifecycle 12/12 and native service/authentication/SSH/discovery,
network status, MC and import checks PASS. Native CCGMS boots, exchanges text through
VICE/TCPser with a local endpoint, hangs up and exits. G71 autostart works with installed
x64sc/x128 and 1571. New focused final runs and packaged tests are recorded externally.

A real VICE CLI check corrected the ACIA selector spelling to `-myaciadev`; no VICE
code changed. Native probe failures caused by output encoding/monitor handshake were
kept as harness evidence and corrected. Native results are not Pi physical claims.

## Remaining gates

Changed Runtime/Menu package builds, clean-source freeze, complete actual-image and
raw/XZ verification, host integrity, recovery checkpoint and hash-bound physical
procedure must all pass before READY TO FLASH. Pi4 B affected-area qualification
remains the owner's next task after those gates. Unchanged earlier owner results are
retained, without inferring unreported RC3 or RC4 PASS results.
