# Project CBM 1.1.0 release preparation

The owner accepted [qualified RC4](../qualification/rc4-owner-release-acceptance.json)
as the final technical basis. The exact RC4 compressed hash was independently verified
before preparation. Individual checklist observations were not supplied and are not
invented. The original procedure, lock, image and recovery remain unchanged.

Only final version/package metadata, factory identity admission and final documentation
are changed. Runtime, console/session scripts, Menu executables and artwork are
byte-identical to the qualified sources. VICE/TCPser/CCGMS/SID-Wizard are reused.
The final image will receive a complete file-by-file equivalence/privacy/fresh-install
and content audit; any unexplained runtime difference stops promotion.

Pre-package validation: host and native Product244/244, Menu102/102; native installed
lifecycle/services/authenticated administration/SSH/discovery/network/import PASS.
Source-only test archives preserve their own chronology; final committed/frozen source
and packages require subsequent checks. Documentation505 checks PASS.

Final public staging, full validation, exact tags/identities, recovery and the minimal
Pi4 smoke procedure are completed in the final result record. No public action is
implied: commits/tags/upload/GitHub Release/publication remain prohibited here.

## Source and notices

The public binary release must be accompanied by exact component/source identities,
package inventory, SHA-256 and applicable notices. Stage retained corresponding-source
bytes, not a pointer to a private kit or an invented written offer. Preserve ordinary
Debian/Raspberry Pi notices and their exact source artifacts. Preserve VICE patches/
build recipe, TCPser source, Project code, and accepted CCGMS/SID-Wizard source/notices.
The unchanged VICE package retains its older engineering-era disclaimer; the explicit
current upstream-ROM release policy supersedes that historical planning notice and
does not assert a new ROM license. This does not require rebuilding VICE binaries.

## Deferred

[Post-1.1 roadmap](../design/post-1.1-roadmap.md): Assembly64, public bootstrap,
signing, formal SBOM, extra hardware qualification and screenshots. These are not
release blockers. Pi4 B is qualified; other model claims remain appropriately limited.
