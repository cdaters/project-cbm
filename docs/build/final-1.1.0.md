# Project CBM 1.1.0 release preparation

## Publication complete

**PUBLISHED:** [Project CBM 1.1.0](https://github.com/cdaters/project-cbm/releases/tag/v1.1.0),
non-prerelease, `2026-09-25T01:57:44Z`. [Exact publication results](published-1.1.0.json)
record all 20 public download hashes/sizes, downloaded-XZ/raw equivalence, published
branch/tag identities, source archive and documentation/page checks. The approved
asset set is unchanged; only the GitHub Release body appends the separately authorized
source/documentation clarification. No tag movement or binary/package rebuild.
The readiness and authorization statements below are historical checkpoints.


## Final physical completion, 2026-09-24

**READY FOR PUBLICATION AUTHORIZATION.** The owner reports the final attempt15
Raspberry Pi 4 B smoke **PASS**, including an actual CCGMS/TCPser BBS connection,
reboot/persistence and shutdown. [Exact attestation](../qualification/final-1.1.0-pi4-owner-pass.json).
No physical check was repeated; the Pi is shut down. No package, frozen input,
image or tag was modified. Only release documentation and qualification records
have advanced. The [publication plan](final-1.1.0-publication-plan.md) identifies
the separate review set, exact assets and proposed Git/GitHub actions.
Owner publication authorization is the only remaining gate; nothing is published.
Earlier preparation observations below retain their historical sequence.

## Original preparation and completed image audit

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

## Completed preparation, 2026-09-24

Initial handoff: **READY FOR OWNER REVIEW, conditional on the external recovery manifest and restore
report verifying PASS. Final-image physical smoke remains UNTESTED.**
[Exact results](final-1.1.0.json) and the [Pi 4 B smoke procedure](../qualification/final-1.1.0-pi4-smoke.md)
bind the final files, source identities and remaining owner action.

The resumed inspection found attempt15 already completed inside the stopped Lima guest.
The construction log ended successfully at 2026-09-21 04:41 UTC, using the frozen kit
and `construct_poc.py --attempt 15`. The external artifact directory had not yet been
populated. No image or frozen package was rebuilt. The existing raw/XZ were exported
into `artifacts/release-1.1.0-attempt-15` under configured bulk storage. Public filename
copies under `releases/1.1.0` contain exactly the same bytes; nothing has been published.

| File in local release staging | Bytes | SHA-256 |
| --- | ---: | --- |
| `project-cbm-1.1.0.img` | 3,095,396,352 | `6c9b7599461a41f6ab30b666dd718329c34f863f11a46dfd20d61fe9830d2468` |
| `project-cbm-1.1.0.img.xz` | 599,290,700 | `8b3738a204da16e148f5674a95f1ffb55a67b8ad1ce1d997b1858594a899c13d` |

Product `v1.1.0` is still `787c275005aaf2c03b2ed769edc815a34ccafc9f`, tag object
`627937867f59b76ea5c3c96fdbb14ebd47ed507f`. Menu `v1.1.0` is still
`7df45cf40eae1ca64cd5740e4b93347e3717bdb4`, tag object
`9f471a2ddd7492d041d9563809e301da9c79ed57`. The attempt15 lock still hashes to
`68d59a178f723c6648191b0af080c0c83b9ad60997ff4d59f4619c6d2b4a2810`.
Post-tag documentation/governance commits do not replace these frozen identities.

### Actual-image and equivalence evidence

The established validators pass **325 checks**: 119 main, 20 supplemental and 186
corrective. All 672 installed package/version/architecture identities match retained
Debian artifacts; the ELF dependency walk checks 127 objects without missing dependencies.
FAT/ext4, systemd/account/service/privilege policy, first-boot state, minimal identity,
CCGMS disk/program/source/notices and source correspondence pass. The final physical
test is not inferred from these read-only/native results.

The complete root and boot inventories compare file bytes, types, permissions, owners,
symlink/device identities and extended attributes. **54,650 entries match; all 21
differences are explained** in external `review-2026-09-24/final-assessment.json`:

- Nine release-documentation/changelog files match the final packages.
- Three installed identity/version files match the frozen final lock.
- Two boot/root references change only to the new matching partition UUID.
- Four dpkg metadata files describe the final Runtime/Menu versions and documentation.
- Three generated caches reflect package versions, changelog observation times, and
  filesystem identities. The decoded APT graph changes only final versions/dependency
  and dpkg status size; all 500 linker auxiliary-cache library records match. Changelog
  indexes change only timestamps and the two final package changelogs.

Runtime/session/launch code, Menu executables, Covers/primary artwork, ELF payloads,
active linker cache, kernel/firmware and both initramfs images remain byte-identical.
Filesystem timestamps/layout, generated cache state and partition IDs prevent a claim
of identical images; this is a qualified-basis equivalence audit, not an independent
reproducibility demonstration.

Fresh-state/privacy inspection finds only the intended `pcbm` home, uninitialized
machine identity, locked account credentials, no completed first-boot marker, no SSH
keys, network enrollment, user history or builder-path/private-key residue. Six library
files are the four original qualification files plus CCGMS and SID-Wizard. No StrikeTerm,
unrelated CCGMS utilities, SID example collection or Finder metadata is installed.
Raw/XZ expanded hashes and sizes match natively and independently on the external Mac copy.

Root filesystem capacity is 2,439,266,304 bytes, with 639,467,520 bytes available to the
unprivileged user before expansion. Future maintenance margin and expanded capacity
depend on the owner's card and first boot; no nominal 8 GB minimum is asserted.

### Host, source, preservation and recovery

Native frozen-kit/Debian verification, original-to-current host package inventory,
masked update units, and capability probes pass. No validation mounts, loop devices
or emulator processes remain. The documented external Lima cache symlink was restored;
the existing VM/disk and all prior construction state remain preserved.

The original staged 1,389 corresponding-source files remain verified. Exact Runtime
and Menu corresponding Debian source bundles are additionally staged from frozen bytes,
alongside source/component inventories, notices, manuals, release notes and checksums.
The staged source archives contain no `.DS_Store` or AppleDouble files. Public technical
reference links identify the frozen source tag; unpublished source/bootstrap access
remains honestly described. No public action was performed.

Historical preservation passes except the owner's explicit non-release-affecting
exception for `TheVerySecond/_notPart/.DS_Store`. Its original file and manifest remain
untouched. It is outside the frozen lock dependency graph and absent from the image.
The other historical inventories pass. Initial cache-parser and evidence-copy harness
errors are retained; corrected checks pass. The empty preliminary APT `dumpavail`
output is not evidence: the nonempty full cache graph supplies the comparison.

Evidence is `qualification/final-1.1.0`. Additive recovery is
`archive/final-1.1.0-2026-09-24`, with exact refs/peeled tags, full bundles, offline
restoration/fsck, retained input/artifact catalogs and checksum manifests. Verify its
external `manifest.json.sha256` and `restore-report.json` before flashing. This is
same-volume recovery; independent encrypted custody remains outstanding.

At the initial handoff, the next action was the owner's final Pi 4 B smoke test.
That test is now PASS as recorded above. Existing RC4 acceptance remains
the physical basis. No new hardware claims, final-tag changes, push, upload or publication.
