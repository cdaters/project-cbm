# Project CBM 1.1 documentation readiness

> **Post-release update — 2026-09-24:** Project CBM 1.1.0 is published; final Pi 4 B
> owner qualification passed. Product/Menu refs, corresponding-source archives,
> inventories and notices are public. See the [publication record](../build/published-1.1.0.json)
> and [current user documentation](../README.md). The initial public build bootstrap
> remains incomplete. The dated audit below is preserved; its pending-publication
> and pending-qualification statements describe the earlier checkpoint.

> Historical documentation checkpoint. Current release decisions and changed application
> composition are in [release policy](../release/release-policy.md); final candidate validation
> and physical status are recorded in [CURRENT-STATE](../../CURRENT-STATE.md).


[Documentation index](../README.md) · [Source verification](source-map.md) · [Public-build audit](public-bootstrap.md)

This documentation-only review describes the current RC3 software. Owner physical
qualification is ongoing. It does not declare Project CBM 1.1 publicly released or
advance any hardware/function qualification result.

## Reader outcomes

| Audience | Result | Remaining boundary |
| --- | --- | --- |
| Image user | Ready for review: short download-to-BASIC path and complete Menu manual, content/USB, file manager, networking/services, optional software, troubleshooting, backup/reflash and shutdown | Final download publication and physical qualification; real screenshots still to capture/review |
| Source builder | Architecture, prerequisites, package commands, pi-gen stages, output/validation and troubleshooting explained; official working procedure separated | **Public source-to-image build BLOCKED.** Unpublished 1.1 refs and initial input/bootstrap workflow are missing; see the specific audit |
| Customizer | Worked examples for Computer Name, Covers, machine/VICE defaults, application/package addition, first boot, services and branding explain edited files, rebuild scope and checks | Complete derivative image construction shares the public bootstrap gap; non-generic application/profile additions require code/contracts, not just a new JSON entry |
| Contributor | Product/Menu ownership, interfaces, source layout, tests, versions, factory and recovery have clear entry points | Current 1.1 source publication remains necessary for outside contribution to this implementation |

## Navigation and changed files

The top-level README introduces the appliance and routes readers to the documentation
index. The index has separate Use, Build, Customize/Develop and Engineering paths.

**Created:**

- `docs/release/getting-started.md`: hardware, checksums, flashing, setup, first C64 and shutdown.
- `docs/release/troubleshooting.md`: user-first checks for boot, input, network, USB, VICE and power problems.
- `docs/release/screenshot-checklist.md`: real capture plan with privacy/rights requirements.
- `docs/release/software-components.md` and `installed-packages.json`: deliberate software choices and the 672-package actual-image inventory.
- `docs/build/official-factory-walkthrough.md`: existing detailed command workflow moved out of the beginner guide and corrected against current scripts.
- `docs/documentation/public-bootstrap.md`, `source-map.md` and this record: public gaps, verification and outcomes.
- `tools/check_release_docs.py` and `tests/test_release_documentation.py`: documentation-only validation and parser regressions.

**Substantially rewritten:** `README.md`, `docs/README.md`, and the release guides
`user-guide.md`, `content.md`, `networking.md`, `recovery.md`, `boot.md`,
`build-your-own.md`, `factory.md`, `accounts-and-layout.md`, `vice.md`,
`customization.md` and `development.md`.

**Light checkpoint correction:** Product `CURRENT-STATE.md`. Historical qualification
records and Menu documentation/source are preserved. No unnecessary second documentation
index or competing Menu manual was created.

## Actual software correspondence

The manual covers all eight Main Menu items: RUN, MACHINES, CONTENT, IMPORT, CONTROL,
FILES, POWER and REBOOT. It covers all eleven registered profiles, launch versus saved
default, the nine CONTROL areas and their declared actions. Service states and connection
help come from current source rather than proposed screens.

Paths use the unified pcbm account, `/home/pcbm` home and `/home/pcbm/content` library.
The layout reference covers content/imports, preferences, audio/VICE settings, diagnostics,
assets, executables, system configuration and installed identity. Networking explains the
actual `Project CBM` share and separate File Sharing password. VICE documentation covers
3.10 source/build flags and patches, SDL/KMS/ALSA, resources, profiles, lifecycle and the
Pi 4 performance floor without claiming universal workload or model qualification.

The [source map](source-map.md) names the inspected implementation. The package JSON
was generated from RC3's retained actual-image package list, not from expected dependencies.
New repository manuals are not claimed to be present in the already-built RC3 image.

## Newcomer walkthrough results

**A — Pi 4, card and Mac/Windows computer:** the reader can find the release location,
understand that final 1.1 is not published yet, choose/check an image, flash without
unsupported customisation, connect hardware, finish setup, RUN into C64 BASIC and use
F10/Quit. Content gives an IMPORT → partition → machine → category walkthrough and its
`<category>/<machine>/Imported` destination. Networking provides password setup, enable,
Finder/File Explorer connection and direct-IP fallback. POWER and backup/reflash are
explained. This is a documentation walkthrough, not a new physical test.

**B — public repositories only:** the reader can understand the image recipe and host
requirements. Today the walk stops at acquiring the reviewed 1.1 source refs. Even with
those refs supplied, it stops again at initial public input/lock creation. Therefore a
fresh public build to a bootable image is **not demonstrated**. The official retained-kit
procedure cannot substitute for that result. The precise missing pieces and classifications
are in the public-build audit; no fictional build command was added to conceal them.

## Validation and limitations

The documentation checker validates titles/fences, local links and heading anchors,
script references, shell example syntax, declared CLI flags, Menu/profile/control labels,
key paths/accounts, package versions, the image-bound package manifest and private/stale
wording patterns. Five focused parser tests cover wrapped links, examples, headings and
anchors. A second human review checks progression, explanations, audience boundaries,
real examples and readable formatting.

Command blocks were not executed as installers, package builds or runtime tests. Bash
syntax checking and source inspection verify their form and supported options; they do
not establish public build success. Windows and graphical client instructions were not
executed on a Windows machine. Existing native/physical results remain historical evidence,
not new documentation-test passes. Final validation: **471 checks, 21 documents, 169 local links, 28 shell blocks and
five parser tests PASS**. JSON/Python syntax and diff-whitespace checks pass. All
pre-existing non-documentation tracked files match the task-start hashes; all Menu
files match. RC3 raw/XZ, four component packages, lock and 46 directly referenced
frozen input objects passed read-only size/hash verification. The external evidence
is `qualification/release-docs-2026-09-20`, with manifest SHA-256
`0c4ef3d643650c9fee59304f45106c2694df341074e387a64b4fc6ec0cb1a135`.
The additive recovery checkpoint is `archive/release-docs-2026-09-20` beneath the
configured bulk workspace; its final external manifest/restore report is authoritative.

## Release review still required

The specific publication/bootstrap/rights/verification gaps are listed once in the
[public-build audit](public-bootstrap.md). In particular, the current private image contains
artwork and StrikeTerm material whose public redistribution must be resolved. Source and
corresponding-source/input publication, public bootstrap, release verification material
and final physical qualification remain genuine release work.

Documentation inspection also found three product edge cases for owner review: G71 import
versus CONTENT filtering, legitimate hidden imported files versus CONTENT visibility, and
the File Sharing prompt's omitted colon restriction. Workarounds/actual rules are documented;
none was silently changed in this milestone. These do not erase the established core
physical results or constitute a new product implementation milestone.

Final screenshots remain a documentation follow-up, not a reason to delay the text manual.
Independent encrypted recovery custody remains an engineering obligation; another checkpoint
on the existing disk is not independent custody.

## Scope and next action

RC3 runtime changed: **NO**. RC3 packages changed: **NO**. RC3 image changed: **NO**.
RC3 hashes changed: **NO**. New image built: **NO**. Anything pushed: **NO**.

Review the manuals and finish the exact RC3 physical qualification. Address the explicitly
identified publication/build/rights decisions before public release claims. This milestone
ends with documentation commits and an additive recovery checkpoint; it does not start
another candidate or engineering milestone.
