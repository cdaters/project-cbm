# Public build and release gap audit

> **Post-release update — 2026-09-24:** Project CBM 1.1.0 is published; final Pi 4 B
> owner qualification passed. Product/Menu refs, corresponding-source archives,
> inventories and notices are public. See the [publication record](../build/published-1.1.0.json)
> and [current user documentation](../README.md). The initial public build bootstrap
> remains incomplete. The dated audit below is preserved; its pending-publication
> and pending-qualification statements describe the earlier checkpoint.

This is an engineering release-readiness record, separate from the user manual.
Audit date: 2026-09-20. No runtime, packages, factory implementation, lock or image
changed during the documentation milestone. RC3 remains in owner physical qualification.

## Owner policy update — 2026-09-20

The historical audit below records the findings at the documentation checkpoint.
Its earlier tentative gate classifications are superseded by the [owner release policy](../release/release-policy.md).
Public bootstrap, formal SBOM and signing are post-1.1.0. Artwork permission is established.
The known upstream VICE ROM permission-documentation gap is accepted under the recorded
policy. StrikeTerm is replaced by an approved CCGMS-only disk in the next candidate.

Remaining publication work is the final candidate's physical qualification, exact image
checksums/source identities, applicable corresponding source and notices, current user
documentation and separately authorized release publication. Public source-to-image
bootstrap remains incomplete and must not be advertised as complete.

### Historical audit (gate classifications superseded)

## Can a stranger build 1.1 from public inputs today?

**No.** Public Product refs inspected with `git ls-remote --heads --tags` contain main
`29933789ec8d29bd55f2b00cbcf309132058413f` and v1.0.0; public Menu main is
`bb4f24fadae6e852bf29fb0e32ad8ced9db7268c`. The reviewed 1.1 integration/Menu source
refs are not publicly advertised. The local RC3 recipe and private input kit can build
an image, but that does not make the public-first-build route complete.

The new [Build Your Own](../release/build-your-own.md) explains the product and
component commands first, then stops explicitly at missing sources/bootstrap inputs.
The complete existing [official procedure](../build/official-factory-walkthrough.md)
is separate. No fictional public wrapper or generic unconfigured pi-gen invocation is offered.

## Required work before public release/build claims

| Gap | Evidence / consequence | Classification and concrete completion |
| --- | --- | --- |
| Publish reviewed 1.1 Product/Menu source refs | Public ref inspection lacks them; public clone cannot inspect/use current recipes | **MUST FIX BEFORE PUBLIC RELEASE:** owner-authorized source publication with release refs and notices |
| Public initial-input/bootstrap workflow | `freeze_private_candidate.py` requires a verified predecessor attempt; `construct_poc.py` expects its lock/object layout and allowlisted private identities | **MUST FIX BEFORE PUBLIC RELEASE** for promised public Build Your Own: provide an initial acquisition/lock workflow and public/derivative identity route, exercised on a fresh environment. Factory implementation changes are outside this milestone |
| Public dependencies/source package acquisition | Current kits contain actual authenticated Debian/Raspberry Pi packages, source archives, URL maps and metadata; URLs alone do not reproduce exact inputs | **MUST FIX BEFORE PUBLIC RELEASE:** publish legally distributable release input/catalog material with a documented acquisition route. Separate exact release replay from deliberate fresh-mirror derivative builds |
| Project CBM-built component/corresponding source outputs | Private VICE/Runtime/Menu/TCPser package bytes exist; public users cannot assume access | **MUST FIX BEFORE PUBLIC RELEASE:** publish the required source, patches/licenses/build records and release artifacts, or a fully exercised source construction route. Prebuilt `.deb` convenience downloads are not intrinsically required for a source-only derivative |
| Primary and machine artwork rights | Menu artwork manifests reserve review of constituent graphics/fonts | **MUST FIX BEFORE PUBLIC RELEASE:** establish rights or select replacements and review their resulting product effect; no blanket MIT assertion |
| StrikeTerm redistribution | Private-image inclusion is distinct from public permission | **MUST FIX BEFORE PUBLIC RELEASE:** obtain permission or exclude it from public distribution. Do not advertise the private disk as bundled in public 1.1 |
| Actual third-party/ROM/media inventory | Existing provenance/security policy requires per-file review, not a no-ROM assumption | **MUST FIX BEFORE PUBLIC RELEASE:** confirm the public image's exact software/resource/content scope and notices, including VICE corresponding source and the admitted SID-Wizard core subset |
| Release verification material | Policy references package inventory/SBOM and detached-signature/trust records; the new installed inventory is not a complete standardized SBOM/signing workflow | **MUST FIX BEFORE PUBLIC RELEASE under current policy:** finalize the standard inventory/SBOM/signature and public verification instructions; do not claim already-signed releases |
| Physical release qualification | RC3 owner testing is ongoing | **MUST FIX BEFORE PUBLIC RELEASE:** record final results and disposition of actual defects. No documentation edit promotes an untested function/model to PASS |

These are explicit release decisions/work, not permission to change RC3 in a documentation
pass. An immutable already-built RC3 cannot silently lose an application or gain refreshed
on-device manuals. The owner must decide publication packaging and any product implications.

## Official-factory-only and optional work

- The original developer's absolute disk paths, private predecessor chronology and stopped
  VM are **not public requirements**. A replacement workflow should use configured roots
  and public inputs, not require copies of personal infrastructure.
- The exact Lima VM/toolchain snapshot is needed for exact official replay. A hobby derivative
  can use a separately validated native arm64 Debian host; it need not reproduce every old
  recovery checkpoint. Host validation still matters for claiming an equivalent build.
- Independent encrypted custody and offline restore drills remain engineering recovery
  obligations. They are not prerequisites for a user to copy games or build a personal package.
- Independent clean-build comparison is required before claiming proven byte reproducibility.
  It is not valid to label a single successful build reproducible; do not invent a new
  runtime blocker solely because a stronger future comparison is desirable.
- Screenshots improve the manual and need review/capture. They do not prevent its text
  from being useful; see [checklist](../release/screenshot-checklist.md).

## Documentation-discovered product mismatches

No implementation correction was made here.

| Finding | Exact source correspondence | Release impact |
| --- | --- | --- |
| G71 accepted by import but absent from CONTENT extension list | Product `importer.py` includes `.g71`; Menu `pcbm_content_extensions()` omits it | Content discoverability edge case. Documented workaround is FILES/manual VICE. Owner release review; no claim of normal G71 auto-launch |
| Legitimate hidden media can import but not appear in CONTENT | Import uses narrow `HOST_METADATA`; Menu `pcbm_filtered_find()` prunes `.*` directories/files | User can inspect/rename through FILES. Review consistency before promising all imported media is browsable |
| Sharing password prompt omits colon restriction | Menu says printable characters; `configuration.py` rejects colon for sharing-password and setup-owner | Minor guidance mismatch; manual states the actual restriction. Record for owner decision rather than change the UI here |

## Newcomer walkthrough

**User:** can identify the download location and current unreleased status, choose hardware,
verify/flash, connect peripherals, complete setup, RUN C64 and return, import a D64, locate
Imported files, turn on sharing and shut down using only release guides. Actual download
of final 1.1 remains blocked until publication; screenshot and physical release review remain.

**Builder:** can understand the recipe, host needs, repository responsibilities, component
package commands and customization examples. Starting with today's public repos fails at
obtaining the reviewed source refs; with those supplied, it next fails at first-image
input/bootstrap creation. Therefore source-to-bootable-public-image walkthrough is **BLOCKED**,
not PASS. The official retained-kit workflow is documented but is not counted as public success.
