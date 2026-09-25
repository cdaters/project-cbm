# Content ingestion and Online Library — design for owner review

Status: **OWNER-ACCEPTED DESIGN / NOT IMPLEMENTED**. Study and acceptance date: 2026-09-24.
Scope: post-1.1.0 design only. No release, runtime, Menu, package, image or tag
changes. This document develops the existing [post-1.1 roadmap](post-1.1-roadmap.md),
including its four owner-deferred USB tasks; it does not create a second backlog.

## Owner acceptance — 2026-09-24

The owner accepts this design as the architectural basis for post-1.1.0 content
work, with the decisions below taking precedence over earlier alternatives in the
study. Acceptance authorizes recording the design, not implementing it in this task.

- **Navigation:** CONTENT contains Browse Library, Import from USB, Online Library,
  Recent Additions and Help. Remove the visible top-level IMPORT item when the new
  UX is implemented; no duplicate shortcut merely for familiarity. Internal command
  compatibility may remain. Additional visual paths require evidence from UX testing.
- **Online identity:** use Online Library, identify Assembly64 inside it (for example,
  “Powered by Assembly64”), and never make Assembly64 a top-level Main Menu item.
- **Internet/offline:** show “Internet connection required” and explain that Assembly64
  is accessed over the Internet while previously saved content remains available
  offline. Provide Retry and Back/Return, reliable connectivity/service distinctions
  where possible, and readable errors without raw exceptions.
- **USB import:** device/partition → folder or whole partition → scan → preview →
  file/folder selection → classification/destination review → explicit Import →
  results → safe unmount. Scanning never triggers copying. Preserve relative folders;
  ambiguous classifications require a visible fallback and user choice.
- **USB browsing:** a separate read-only FILES/USB/MC session with deliberate Safe
  Unmount. IMPORT retains automatic safe unmount. Writable USB browsing is out of scope.
- **Saving and launch:** Save & Run saves successfully to the library first, then
  uses the existing validated machine/profile/Cover/VICE path. Require an explicit
  choice when compatibility is uncertain; no initial temporary-only download mode.
- **Duplicates:** identical bytes at the same destination mean Already Present;
  different bytes mean Keep Both. Surface matching copies elsewhere without breaking
  release sets. Keep conflicting multi-disk sets in sibling directories. No automatic
  destructive replacement and no hardlink deduplication of mutable disk images.
- **Provider access:** no known owner-provided Assembly64 access arrangement or
  contact exists. HTTP 464 remains unresolved. Before online implementation
  qualification, establish legitimate access, identification/registration, service
  and rate expectations, and attribution. Never impersonate another client/hardware
  or copy its identifiers, credentials or private tokens. Later preparation may
  research this; no provider research or contact is authorized by this record alone.
- **Reference code:** retain ultimate64-manager as a design reference; prefer an
  independent small CBM client. Any implementation reuse first needs provenance and
  license review.
- **Version:** provisional feature milestone **Project CBM 1.2.0**. The reporting fix
  may be its first groundwork; do not create 1.1.1 solely for that defect absent an
  urgent maintenance need. No version/tag/release is created by this acceptance.
- **Guidance:** built-in descriptions, Internet notice, first-use/contextual help,
  key/action hints, summaries, duplicate/offline messages, safe-removal advice and
  beginner-friendly external manuals are required feature deliverables.

Approved sequence: (1) reporting fix and contracts; (2) shared safe primitives and
USB discovery/preview/selection; (3) redesigned USB UX under CONTENT; (4) read-only
FILES/MC browsing; (5) Assembly64 search/browse/Save after legitimate access and
service expectations are resolved; (6) Save & Run through existing launch routing.
No phase is implemented or qualified by this document.

## Recommendation in brief

Make CONTENT the home for browsing and acquiring library content. Offer **Browse
Library**, **Import from USB**, and **Online Library**, with Assembly64 identified
inside Online Library. Keep FILES for deliberate file management and a separate
read-only USB browsing session.

Share an unprivileged ingestion plan, classification evidence, destination policy,
collision handling, atomic file writes and results. Keep USB mount/discovery and
Assembly64 queries/download transport separate. Save before optional Run, using
the existing Product profile resolver and shared Menu/Cover/VICE launch path.

Do not guess game/demo/application from PRG or disk extensions. Show uncertainty
and ask for a batch destination. Keep folders and multi-disk releases together.
Do not overwrite existing content automatically or introduce a parallel online
library filesystem. No online archive extraction or screenshots in the first slice.

**External readiness limitation:** two metadata-only HTTPS requests using a distinct
Project CBM study client identifier received HTTP **464**. The meaning was not
documented in the sources inspected. A working API agreement/client identity,
service expectations and live response contract remain to be established before
online integration can be qualified. This does not prevent reviewing the design
or later independent USB work. No foreign client identity was impersonated and
no Commodore content was downloaded during this study.

## Evidence and method

Labels throughout: **Fact** = inspected code/documentation or observed request;
**Inference** = conclusion with stated limits; **Proposal** = future behavior.
Code inspection establishes implemented reference behavior, not live API promises.

Local inspected identities, with tracked trees clean before this study:

| Repository | Inspected HEAD | Notes |
| --- | --- | --- |
| Product | `6251fc96df8e3f4c3646eedd5c3dad39834db9dc` | Local publication-completion records; `.qwen/` and `memory/` remain untracked |
| Menu | `7df45cf40eae1ca64cd5740e4b93347e3717bdb4` | Published Menu source |
| ultimate64-manager | `a4e55f12d6a08c3a435b1d63ced1c3a2c6f461e8` | Local design reference, clean; upstream `sandlbn/ultimate64-manager` |

Product `v1.1.0` still has tag object
`627937867f59b76ea5c3c96fdbb14ebd47ed507f`, peeling to
`787c275005aaf2c03b2ed769edc815a34ccafc9f`. Menu tag object
`9f471a2ddd7492d041d9563809e301da9c79ed57` peels to its HEAD above.
The public documentation snapshot remains `f185bc353428a1ab9bb4b6e1ab49143c73b3a57a`.
No requalification or repeat release checks were needed for this design study.

Primary local reading:

- Product [importer](../../runtime/project_cbm/importer.py),
  [client](../../runtime/project_cbm/import_client.py),
  [library](../../runtime/project_cbm/library.py),
  [profiles](../../runtime/project_cbm/profiles.py),
  [application policy](../../runtime/project_cbm/applications.py),
  [network information](../../runtime/project_cbm/network_info.py).
- Menu, at the pinned identity above: `scripts/pcbm-menu`, `pcbm-content`,
  `pcbm-import`, `pcbm-files`, `pcbm-machines`, `pcbm-run-vice`,
  `lib/pcbm-ui.sh` and the configuration bridge.
- [Content manual](../release/content.md), [architecture](../architecture.md),
  [configuration contract](../runtime/configuration-contract.md),
  [security](../security.md), [build contract](../build-and-release.md),
  [testing](../testing.md), [USB owner disposition](../qualification/final-1.1.0-usb-import-disposition.md).
- Product `tests/test_content_library.py`, `tests/test_import_metadata.py`,
  `tests/native/import_fat.py`, `tests/native/import_metadata.py`; Menu
  `tests/test_optional_content.py`, `test_release_polish.py`, `test_ui_contract.py`.

## A. Current state

### Navigation, library and launch — facts

Main Menu has RUN, MACHINES, CONTENT, IMPORT, CONTROL, FILES and power actions.
RUN launches the saved default. MACHINES launches a profile or changes that default.
CONTENT currently opens Games, Demos, Music, Programs and ROMs, recursively listing
supported files by relative path. FILES offers Midnight Commander (MC) on the local
library/home or a shortcut to the same USB importer. Its USB item is not a mounted
USB browser.

The library is `/home/pcbm/content/<category>/<family>/...`. Families are `c64`,
`c128`, `vic20`, `plus4`, `pet`, `cbm2`, `cbm5x0`, and `shared`. ROMs omit Shared;
initial Music folders omit PET/CBM-II. Screenshots and Saves are storage folders,
not CONTENT categories. Existing arbitrary subfolders and legacy files directly
under categories remain supported.

Product `library.content_profile` maps recognized folders to installed registry
profiles, retaining a compatible RUN variant. `c128/80col` selects the VDC profile.
Shared/legacy paths use RUN's default; this is not universal compatibility.
CCGMS and SID-Wizard have narrowly recognized application paths. G71 has explicit
C64/C128 and 1571 handling. ROM/BIN/REU resources are rejected for generic autostart;
the shared launcher also refuses SID. MUS recognition does not provide a dedicated
music player. Menu calls `pcbm-profiles`, then `pcbm-run-vice`, which uses the
existing supervised Cover/VICE lifecycle. Remote metadata cannot supply launch flags.

### USB boundary — facts

`pcbm-import` → unprivileged `pcbm-import-operation`/`import_client.py` → fixed
sudo `pcbm-import-root` → Product importer. This is a short-lived broker/helper,
not an existing online or content daemon. Root discovers and mounts; a fork drops
supplementary groups/GID/UID to pcbm (1000) before traversal/copy.

- Only unmounted USB partitions on eligible `sd*` disks, with USB sysfs checks;
  the whole disk is excluded if it or a child is mounted. Root/boot disks are
  excluded by this policy. Selection uses opaque tokens bound to disk sequence,
  device identity and rediscovery, not a caller-supplied `/dev` path.
- FAT (`vfat`), exFAT, ext4 only. Fixed `ro,nodev,nosuid,noexec`; ext4 adds `noload`
  to prevent journal replay. FAT/exFAT synthesize pcbm-only access; ext4 retains
  source permissions. No root copying to bypass unreadable ext4 directories.
- The selected partition root is recursively scanned. The machine/category
  selection starts copying immediately. No source picker or preview exists.
- Eligible extensions: `.prg .p00 .t64 .tap .d64 .d71 .d81 .g64 .g71 .x64 .sid`
  `.crt .d67 .d80 .d82 .g41 .p64 .mus` (case insensitive).
- Only regular files; no symlink traversal. Exact host metadata names/subtrees
  and AppleDouble companions are excluded, not all dotfiles. Relative source
  folders are retained beneath `<category>/<family>/Imported`; SID overrides
  routing to `music/c64/Imported` for current clients.
- Same destination name is skipped without a content comparison. Copy uses an
  exclusive temporary file, fsync and non-overwriting link into place. A failed
  operation can leave completed files, but does not replace existing content.
- Limits include 16 discovery entries, depth 12, 10,000 visited entries, 2 GiB
  transferred per operation, and 256 MiB destination margin. These are safety
  bounds, not demonstrated ideal UX limits for future large libraries.
- Cleanup reaps the worker and attempts ordinary unmount. Automatic release is
  intentional. An uncertain/failed release requires conservative removal guidance.
- The client drops `ignored_metadata` on success and collapses structured errors
  and `source_unmounted` on failure. The existing roadmap already records the fix.

**Inference:** format recognition and semantic classification must be separate.
A `.prg` can represent many purposes, including a ROM-related payload; disk geometry
does not prove program type or machine. The JiffyDOS import was consistent with
1.1.0 rules. It does not justify changing the published image.

### Reuse and refactor recommendations

Reuse filesystem/device policy, no-follow descriptor traversal, bounded validation,
ordinary-user copying, atomic no-overwrite commit, metadata exclusions, library and
profile authorities, shared launcher and existing UI/results conventions.

Separate traversal from copying; represent discovery as a bounded reviewable
snapshot. Separate plan validation, transfer and result transport. Replace the
single blocking UI operation with cancellable, supervised jobs. Add versioned,
bounded paging/progress contracts: a 4 KiB request/8 KiB reply should not be enlarged
into an arbitrary full-tree root request. ROOT never interprets provider metadata.

The current CONTENT browser materializes a full recursive list. Page browsing and
selection as part of this work; avoid passing entire USB trees as dialog arguments.
The newer `pcbm-ui.sh` has explicit success/cancel/back/failure states and bounded
menus. Reuse it; extend it deliberately for checklists/progress rather than
inventing a second UI toolkit. Existing contextual messages are useful precedent;
there is no universal F1 help contract to claim is already available.

## B. External reference findings

### Official Ultimate documentation — facts and lessons

Firmware 3.11 introduced integration. Its guide describes F6/F5 search, editable
fields and dynamic server presets, followed by release entries and their files.
A release may contain multiple disks. Run downloads into `/Temp` then mounts;
the guide explicitly describes the original 20-result limit and accumulating
temporary files. Those are 3.11 observations, not universal current API limits.
See [official Assembly64 guide](https://1541u-documentation.readthedocs.io/en/latest/howto/assembly.html)
and [3.11 announcement](https://github.com/GideonZ/ultimate_releases/blob/master/changes_3.11.txt).

The [firmware history](https://www.ultimate64.com/Firmware) records later support
for viewing text and copying Assembly64 files in 3.14d. The
[3.15 notes](https://1541u-documentation.readthedocs.io/en/latest/howto/release_3.15.html)
report temporary-upload cleanup, Assembly64 browser memory fixes and network
resource/timeout improvements. This does not prove every old Assembly64 cache issue
is fixed. Lessons: distinguish release/file, expose Save separately from Run,
design cancellation/cleanup first, and bound repeated browsing memory.

Inspected official firmware source at
[`ef9937a73c7db391d5434bfda08e96216d7099cc`](https://github.com/GideonZ/1541ultimate/tree/ef9937a73c7db391d5434bfda08e96216d7099cc):
`software/network/assembly.cc` uses HTTP port 80 at `hackerswithstyle.se`, the
`/leet/search` family and `Client-Id: Ultimate`. This snapshot uses unpaged
`aql?query=`. `software/userinterface/assembly_search.cc` contains built-in query,
result and file-navigation help, warns about download delay and supports closing
search. It frees JSON result trees; listing failures become an error state.
Its repository license is GPLv3. These source facts are not a recommendation to
copy its HTTP transport, UI keys or code into CBM.

### Local Ultimate64 Manager — facts

Pinned reference:
[`sandlbn/ultimate64-manager@a4e55f12d6a08c3a435b1d63ced1c3a2c6f461e8`](https://github.com/sandlbn/ultimate64-manager/tree/a4e55f12d6a08c3a435b1d63ced1c3a2c6f461e8).
`src/assembly64.rs` is a Rust HTTPS/JSON client. `src/assembly64_browser.rs` owns
desktop navigation, persistent presets/categories, filters, favorites, detail
views, download actions and Ultimate device handoff. `src/net_utils.rs` supplies
HTTP timeout policy. Project CBM does not need its desktop framework or device API.

Observed request base: `https://hackerswithstyle.se/leet`, with `client-id: u64manager`.
These are code-observed endpoints, not a published service SLA:

| GET path after base | Reference use / response |
| --- | --- |
| `/search/aql/{offset}/{limit}?query=...` | Paged search; array of release records; default page size 100 |
| `/search/aql/presets` | Dynamic `repo`, `category`, `subcat` groups, names and AQL keys |
| `/search/categories` | Source/category table; parser also accepts a legacy ID-to-name map |
| `/search/entries/{item_id}/{category_id}` | `contentEntry` list of file `id`, `path`, `size` |
| `/search/meta/{item_id}/{category_id}` | Release metadata |
| `/search/compotypes` | Competition labels |
| `/search/bin/{item_id}/{category_id}/{file_id}` | File bytes |

Release fields include ID/category, title, group, handle, year, source/site ratings,
updated/released dates, event/place/compo and site category. Many are optional.
Source category is not simply CBM's Games/Demos/Music classification. IDs need their
category context. File paths and sizes describe individual members of a release.

Search forms produce AQL (name/source/category/rating/recency/sort); raw AQL is also
available. An empty form becomes a latest-first query. HTTP 463 maps to an AQL
syntax error. Network/timeout/JSON failures have readable messages, although raw
transport errors are logged. Preset failures retain cached/baseline choices.
This is useful degradation, not offline access to remote content.

The client removes same-name/group/year hits within each page. **Do not copy that
as identity logic:** distinct releases can share those fields. Retain composite
provider/category/item IDs; optionally group visually without discarding variants.

Downloads buffer the entire response, then write a sanitized filename into a
category directory, flattening path separators. `tokio::fs::write` can replace
an existing file. Batch cancel is checked between files. ZIP extraction and Run /
Mount / copy-to-device are separate actions. These policies are unsuitable defaults
for CBM; use streaming, mid-file cancellation, preserved relationships and explicit
collision handling. No reference source was copied.

Screenshots in this client come from **CSDb's separate XML webservice**, for selected
CSDb-derived categories, followed by an image request. They are not evidence of an
Assembly64 screenshot endpoint. Neither that dependency nor a console image viewer
belongs in the initial slice. A text metadata/details view is sufficient.

### Service observations and confidence limits

The [Assembly64 operator page](https://hackerswithstyle.se/assembly/) describes
search/filtering and local/online file management for its own application. It does
not establish that every desktop feature is available to a third-party API client.
No sufficiently explicit third-party API contract, client registration procedure,
rate limit, metadata license or redistribution grant was located in the inspected
official pages. Absence from this review is not proof no terms exist.

Read-only study requests: operator homepage returned 200; `/leet/search/aql/presets`
and `/leet/search/categories` each returned 464 with
`client-id: project-cbm-design-study`. `assembly64.com` did not resolve from the
study host. Search, entry listing and binary downloads were consequently not
live-tested. No retry storm, enumeration or alternative client-ID probing occurred.

**Inference:** service onboarding or another access condition may apply; 464 alone
does not establish why. **Proposal:** confirm the supported HTTPS hostname, honest
CBM client identifier, allowed usage, rate/caching expectations and error meanings
with the operator before enabling a distributed client. Do not promise authentication,
Range resume, checksums, screenshots or non-C64 coverage without evidence.

## C. Proposed information architecture

```text
Main Menu
  RUN                       (existing default-machine action)
  MACHINES                  (existing launch/default selection)
  CONTENT
    Browse Library
      Games / Demos / Programs / Music / ROM Resources
    Import from USB
    Online Library
      Assembly64 — Internet connection required
      Search / Browse by category / Latest / Recent downloads / Help / Back
    Recent additions
    Help / Back
  FILES
    Library — Midnight Commander
    USB Drive — Browse read-only
    Safe removal / Help / Back
  CONTROL and power actions (existing responsibilities)
```

| Placement option | Assessment |
| --- | --- |
| A. Assembly64 at top level | Very visible, but duplicates acquisition navigation and gives one provider disproportionate prominence |
| B. CONTENT → Online Library | **Recommended:** browsing and acquiring content are adjacent; local browsing stays usable offline |
| C. IMPORT → Online source | Technically possible, but importing local files and searching a remote catalogue are different user tasks |
| D. Separate Library hub replacing CONTENT | Adds renaming/migration cost without sufficient immediate benefit |

Use **Online Library** and the factual description **Content from Assembly64**.
The owner accepts “Powered by Assembly64” as example wording; confirm provider attribution requirements before distribution;
do not imply endorsement. One provider needs no provider-selection screen. Internally
use a provider identifier so a future provider does not alter storage/ingestion rules.

Move visible top-level IMPORT into CONTENT when redesigned selection ships. Retain
the `pcbm-import` entry point as a redirect to that same flow for script compatibility;
do not retain two conflicting implementations. FILES → USB becomes browsing, with
explicit text about the change and an Import shortcut only if usability testing
demonstrates need. Keep RUN and MACHINES fast and independent of networking.

## D. Proposed content-ingestion architecture

```text
USB adapter: partition → protected mount → scoped, bounded discovery ─┐
                                                                  ├→ candidates
Online adapter: HTTPS → query pages → release details/file list ─────┘
  → metadata/type evidence → selection → destination plan → review
  → obtain bytes → validate/hash → final collision decision → atomic commit
  → per-file and job results → USB release (when applicable) → optional Run
```

Discovery may identify collisions by path/size, but equality requires bytes. USB
can hash a candidate before writing; an online file normally must be downloaded
before equality is established. Do not force download before preview just to make
both sources execute the same sequence.

### Ownership and proposed modules (names are tentative)

| Component | Owner / privilege | Responsibility |
| --- | --- | --- |
| Content UI and bridge | Menu / pcbm | Paged choices, safe text, progress, help, results, navigation |
| Ingestion coordinator | Product / pcbm | Versioned job/selection/plan, validation, limits, cancellation |
| Media classifier | Product / pcbm | Format evidence, supported actions, uncertain semantic hints |
| Library planner/writer | Product / pcbm | Extend `library.py`; destinations, hash comparison, no-overwrite commit |
| Local provenance/index | Product / pcbm | Small rebuildable lookup/history; never library existence authority |
| USB access supervisor | Product / narrowly privileged | Device tokens, fixed mounts, leases, process cleanup, confirmed unmount |
| USB discovery adapter | Product / pcbm worker | Scoped no-follow traversal, opaque candidate IDs, source revalidation |
| Assembly64 adapter | Product / pcbm | Validated HTTPS/JSON, query paging, metadata, bounded byte streaming |
| Launch handoff | Existing Product + Menu path / pcbm | Resolve registry/profile, validate committed media, Cover/VICE/return |

Use small Python modules and versioned structured IPC alongside Bash/dialog. No new
web server, plugin system, catalogue daemon or root network process. A bounded USB
supervisor is justified by mount lifetime, not by online-library architecture.

### Data contracts

Candidate: opaque ID; source kind/session; original relative name; safe display
name; byte size or explicit unknown; release/group membership; provider/category/
item/file IDs where applicable; format; proposed purpose/family with evidence;
supported actions; warnings. Never accept remote executable options or root paths.

Plan: schema version, job/session IDs, discovery generation, selected candidate IDs,
scope, user-approved purpose/family, displayed final paths, collision policy and
resource totals. Large selections are validated in bounded pages referencing the
session manifest; Menu cannot substitute arbitrary filesystem paths.

Result: explicit success/partial/cancelled/failed status; committed, identical,
kept-both, skipped, unsupported, ignored-metadata, failed and unattempted counts;
bytes; per-file bounded detail; destination; stable error codes; USB release state
(`confirmed`, `failed`, `unknown`, or `not_applicable`). Exit status does not erase
the result. Missing release evidence never becomes “safe to remove.”

Job lifecycle: discover → review → ready → transferring → committing → releasing
→ finished. Cancellation stops acquisition, removes only owned partial files,
preserves committed files, reaps workers and releases USB. A compact private journal
records completed work so a crash can be reconciled without pretending a batch was
atomic. File commit is atomic; an entire release/batch may be partial and must say so.

For review across several screens, USB needs a lease, not today's one-call mount.
Use a supervised job/session tied to the caller and disk generation. Idle review
may renew the lease; caller loss/expiry triggers worker stop and ordinary unmount.
Resuming an expired session requires rediscovery and rescanning. Only one owner per
device; import and browsing may not contend for the same disk. Fixed lifecycle
operations only, with a service-owned private runtime directory. No arbitrary
mount, filesystem, destination, PID or command may cross the privileged boundary.

## E. USB experience and classification

### Import journey — proposed

| Step | What appears | Available actions / rules |
| --- | --- | --- |
| 1. CONTENT → Import from USB | Short explanation: scan, review, choose, copy; source stays read-only | Continue, Help, Back |
| 2. Partition selection | Sanitized drive/partition description, filesystem, capacity; excluded/busy explanation | Refresh, Select, Back; multiple partitions selected separately |
| 3. Scope | **Choose a folder** or **Scan whole partition**; show root/folder plainly | Folder navigation bounded to lease; Back; choosing folder is recommended for mixed drives |
| 4. Scan | Visited/found counts, current safe relative folder, limits | Cancel and release; no copying; limit reached offers narrower scope, never silent truncation |
| 5. Preview | Compatible-file count/bytes, format groups, folder tree, ignored/unsupported counts | Select Files, Select Folders, Select All Compatible, Clear, Details, Back |
| 6. Classification | Selected groups with purpose/machine suggestions and their confidence/evidence | Apply choice to group, edit exceptions; no hidden directory-name authority |
| 7. Destination review | Human label and path preview, space estimate, collision defaults, selected totals | Import, Change selection/destination, Cancel; no copy until Import |
| 8. Transfer | Files/bytes completed, current file, bounded progress | Cancel; committed files retained and reported |
| 9. Result and cleanup | Saved/skipped/identical/conflict/error counts and separate USB release result | Details, Open destination, Run eligible item, Done; unmount attempted before final result |

“Select All” is an explicit choice within the displayed scope, never a default
copy of the whole device. Folder selection includes eligible descendants and shows
counts; expanding a folder does not select it. Mark multi-disk groups and warn
when selection omits discovered siblings without inventing release semantics.

Preserve paths relative to the displayed scan root, under a named import folder:
`games/c64/Imported/<collection>/<relative path>`. Show the chosen collection name
before commit; retaining a scoped root folder name avoids losing context. Reusing
a collection on retry preserves deterministic destinations. Reject unsafe source
components with clear counts rather than silently mangling them into collisions.
**Do not offer flattening initially**: it breaks collections and creates avoidable
collisions. Existing 1.1.0 Imported trees are untouched.

### Classification rules — proposed

Keep four separate concepts: **format**, **purpose**, **machine family**, and
**launch eligibility**. Valid format does not prove all the others.

| Material | Evidence / safe treatment |
| --- | --- |
| PRG/P00 | Program/container format; load address alone does not identify machine or game/demo. Ask purpose/family or retain unclassified; do not autostart merely because it is PRG |
| D64/D67/D71/D81/D80/D82/G64/G71/G41/X64/P64 | Disk image / drive-format hints. Validate structure where practical; no Games default from extension. Preserve sets; keep G71 launch restriction |
| TAP/T64 | Tape/container headers may provide machine-format evidence; require reviewed mapping and version checks. Do not treat all tapes as C64 games |
| CRT | Validate recognized cartridge header/type; propose family only for explicitly supported type mapping. Cartridge hardware may remain incompatible with the selected VICE profile |
| SID | Valid PSID/RSID gives strong C64 music evidence; show routing to Music/C64. Store only: dedicated playback remains outside this work |
| MUS | Music-format hint only; no promised playback or reliable family from suffix alone |
| ROM/BIN/REU, firmware/update files | Not eligible for first-slice bulk import or Download & Run. Explain resource/manual configuration; deliberate FILES management remains possible |
| ROM-like PRG / suspicious filename | Label “purpose unknown”; filename may suggest review but never prove firmware/game identity. No automatic installation or VICE ROM-setting changes |
| Directory names | Optional visible hints, including `games/c64`; never authoritative. User-confirmed known library layout can suggest a mapping; no automatic tree stripping |
| Assembly64 metadata | Visible source-derived suggestions; audited category mapping, unknown categories fall back safely. A source ID is not a compatibility guarantee |

User choices take precedence over hints, subject to hard format/launch restrictions.
When purpose is unknown, offer **Programs — Unclassified** as an explicit fallback
(described as unsorted content, not an assertion it is an application). Use Shared
when the machine is unknown. Require a machine choice before optional Run; do not
silently launch a newly unknown download with an unrelated RUN default.

This cannot reliably identify every misnamed JiffyDOS PRG. Preview and scoped
selection solve the user's control problem; a semantic classifier cannot guarantee
content identity from these formats. No AI classification or speculative blacklist.

### Deliberate USB browsing — proposed

FILES → USB Drive → choose partition → **Browse read-only** → MC, with USB on one
panel and the local library on the other → exit MC → **Safe Unmount** (default),
Browse again, or Help. Main Menu return first attempts unmount. Successful result:
“USB released. You can remove it.” No persistent mount after normal exit.

Reuse the USB access supervisor's fixed mount policy and exclusive disk lease.
Expose a stable, pcbm-accessible session path beneath a fixed `/run` USB area; do
not require users to type it. Root-owned session bookkeeping remains separate from
the browsable directory. FAT permissions remain synthesized, ext4 remains native;
unreadable ext4 content stays unreadable. Support only FAT/exFAT/ext4 initially.

MC runs as pcbm, never sudo. Its copy-to-library operations are ordinary file
management and do not automatically receive ingestion classification/provenance.
Warn that MC's copy/overwrite prompts are its own. The USB filesystem rejects writes;
rename/delete/edit attempts on the source fail. `noexec` does not stop an interpreter
from reading scripts: it is a mount protection, not a sandbox. Do not add automatic
execution or privileged associations for source files.

On MC crash/caller disconnect, reap supervised children and attempt release. If an
external process still holds the mount, report Busy and offer Retry or safe shutdown;
never force/lazy-unmount and claim removal is safe. Sessions do not auto-remount
after reboot. Shutdown ordering terminates session users then unmounts; recovery
reconciles tracked mounts by actual device/session identity, never just a reused
device name. Do not unmount another application's drive. Show per-partition status;
“remove drive” is allowed only after all CBM sessions on that physical disk are
released. Writable USB browsing/export is excluded from this proposal's first slice.

## F. Online Library, storage, duplicates and Run

### Online journey — proposed, contingent on provider access

| Step | What appears | Actions / behavior |
| --- | --- | --- |
| 1. CONTENT → Online Library | Description, **Internet connection required**, Assembly64 attribution | Continue on first use, Help, Back; no background network traffic before entering |
| 2. Connection attempt | “Connecting to Assembly64…”; local network status from `pcbm-info` plus bounded real service request | Cancel; failures offer Retry, Network settings, Back |
| 3. Online home | Search, Browse by category, Latest, Recent downloads | Search is primary; Browse/Latest are bounded filtered queries, not a crawl of the whole catalogue |
| 4. Search form | Name, optional type/source/year where confirmed; clear labels, no AQL knowledge | Search, Clear filters, Help, Back; preserve form on errors |
| 5. Results | Title, group/year if known, source/type; stable release IDs behind display | Details, next/previous page, refine search, Back; avoid false total counts |
| 6. Release details | Available metadata, source, file list/sizes/formats; unknown fields omitted or marked | Select compatible files, select compatible release set, view safe text if later supported, Back |
| 7. Save plan | Destination/category/machine suggestions, size/space and collisions; selected set | **Save to Library**, **Save & Run** when eligible, Change, Back |
| 8. Download | Bytes and selected-file progress, service attribution | Cancel; bounded sequential transfer; no partial file offered to launch |
| 9. Result | Saved location, completed/skipped/failed members, selected launch file | Open Library, Run, Retry failed, Back to results; query/selection retained |

Prefer the label **Save & Run**, with help explaining “download, save, then run.”
Do not have two indistinguishable Download/Save buttons. A completed download is a
permanent ordinary library file. There is no temporary play-only mode initially.
Recent downloads is local job history, available offline; it is not an Assembly64
API capability. Recent additions also includes USB.

No supported Internet connection does not prevent opening Help, Recent downloads
or the local library. Show a cached catalogue only if implemented later and clearly
labelled stale/offline; do not present it as live search.

### Connectivity and service errors

Use a hybrid: immediately show the feature shell, consume Product network status,
then make one cancellable useful HTTPS request on entry (e.g. presets). Reuse that
success briefly, but handle failures on every operation. No arbitrary ping or
third-party “Internet test” endpoint. A LAN address is not proof of Internet, and
an unreachable provider is not proof the Internet is down.

- No connected interface/address: explain no network connection; offer Settings.
- DNS/timeout/unreachable: “Cannot reach Assembly64. Check your connection or try
  again later.” State uncertainty instead of guessing which party failed.
- TLS/certificate error: explain secure connection failure; suggest clock/network
  check, never disable verification or fall back to HTTP.
- 5xx: service could not complete request; Retry/Back, bounded backoff.
- 429: respect Retry-After, show wait and Back; no busy-loop retries.
- 401/403/unknown 464: service access unavailable for this client, not “offline.”
  Do not invent a login flow or switch IDs. Retain sanitized diagnostic code.
- Schema/response change: readable unsupported-response error, local library still
  works. Never turn parse failure into an empty successful result.
- Empty result: “No matches. Try a shorter name or fewer filters.” No error state.

### Duplicate and collision policy

**Default: preserve existing files.** Use SHA-256 while streaming; before treating
an existing file as equal, validate its current identity and contents. VICE/MC may
have changed it since ingestion. Size/mtime/index/provider ID alone is insufficient.

| Situation | Default | Other deliberate action |
| --- | --- | --- |
| Same destination, same bytes | Skip as Already present | View existing location |
| Same destination, different bytes | Keep both with deterministic suffix; show final path | Skip; explicit Replace deferred from first slice |
| Same bytes elsewhere in library | Show Existing copy; do not silently remove a required set member | Use existing for a single item, or keep a copy within this release |
| Same provider/category/item/file downloaded again | Check indexed local file still exists and is unchanged; avoid redundant fetch when contract permits confidence, otherwise validate fresh bytes | Retry/download anew if modified, missing or identity changed |
| Same filename across USB/Assembly64 | Compare actual bytes, not source/title | Same rules as any collision |
| Same title, differing release/source IDs | Keep distinct release sets | User may compare metadata; never title-based automatic deletion |

For a conflicting multi-file release, prefer a new sibling release directory for
the whole set rather than renaming individual disks. Preserve internal filenames.
Do not hardlink mutable disk images for deduplication: one program's saves could
alter another copy. No global dedup scan at startup; hash on ingestion and on-demand
comparison, with a rebuildable index. Index hits elsewhere are advisory until
revalidated. Comparison initially means names, size, SHA equality, date and source,
not a binary/disk semantic diff.

No prompt per identical file. One review summarizes conflict policy; exceptional
items appear in results. Keep Both/Skip can be set for the batch. A future Replace
would need explicit approval, preserved prior bytes and race-safe revalidation;
ordinary MC remains an advanced route in the meantime.

### Storage and provenance

Keep the purpose-first library. Suggested online destination:

```text
/home/pcbm/content/games/c64/Downloaded/<title>--<short-stable-release-key>/...
/home/pcbm/content/demos/c128/80col/Downloaded/<release>/...   (explicit VDC choice)
/home/pcbm/content/programs/shared/Downloaded/<release>/...  (unknown machine)
```

The stable key derives from the complete provider/category/item identity, with
collision detection. Preserve validated relative member paths. Review normalized
remote names before saving; reject absolute/traversal names, and resolve names that
normalize to the same destination without silent loss. Do not add format directories
or a parallel `/home/pcbm/Assembly64` tree. “Downloaded” leaves room for a future
provider; provider identity belongs in details, not a mandatory top-level folder.

Private metadata under `~/.local/share/project-cbm/content/` stores versioned
per-job provenance and a small SQLite index (standard-library facility, not a server).
Record library-relative path, hash/size, provider/release/file/source IDs, retrieval
time and confirmed user classification. USB records need no serial/UUID or full
host path; omit those by default. Store source attribution without inventing license
grants. Unknown license remains unknown. Do not put metadata sidecars among disks
or inside emulated media. Preserve a bounded local history with Clear History.

Files remain usable without the index. Reconciliation marks moved/deleted/modified
files; it never deletes user content or re-downloads automatically. Backup/restore
can include provenance separately. If metadata write fails after a file commit,
report “file saved; source record incomplete,” then reconcile on the next operation.

### Download & Run routing

Only run committed, revalidated local content. Release download success and launch
success are separate results. Ask which member to start when multiple disks/files
exist; retain the whole selected set for later VICE disk changes. An incomplete set
does not auto-run; allow an explicit standalone run only when the user understands
what completed and the selected media passes normal checks.

Use `pcbm-profiles content-profile`/registry and the existing shared launcher, with
a validated per-launch profile choice where needed. Preserve compatible RUN variants;
never change the saved RUN default to accommodate a download. Display the resolved
machine before launch. C64 normally uses x64sc; C128 supports explicit 40/80-column
choice; VIC-20, Plus/4, PET, CBM-II and CBM-II 5x0 require their registered profiles
and appropriate media. Do not promise Assembly64 has coverage for every CBM machine.

Unknown/contradictory metadata: Save is available; Run requires explicit compatible
profile selection or stays unavailable. SID/MUS playback, ROM/REU installation,
unsupported CRT types and arbitrary firmware are not unlocked by downloading them.
Do not import provider `.cfg` settings or scripts, enable services, or construct
VICE arguments from text fields. On F10/Quit, return through the same terminal
restoration path to the result/library context. A failed launch preserves saved data.

Apply the same ambiguity check when reopening a newly ingested unclassified item
through Browse Library, not only from the download result. Preserve the established
RUN-default fallback for legacy files; do not pretend missing provenance proves a
machine. Show the chosen profile and allow correction before launching ambiguous
new acquisitions. Loss of advisory metadata must still leave a visible machine
choice available, rather than silently asserting compatibility.

## G. Built-in guidance — draft text, not shipped UI

Use existing dialog messages/textboxes and explicit Help rows. Every selection
screen shows Back; Escape means Back/Cancel, not a raw backend exit status. Proposed
checklist hint: “Space: select · Enter: continue · Esc: back.” Validate this against
the actual dialog widget before documenting the keys as implemented. Working views
show progress and Cancel; cancellation waits for cleanup and reports its outcome.

| Context | Draft wording |
| --- | --- |
| CONTENT description | “Browse your library, import USB files, or find software online.” |
| USB description | “Scan a USB drive, review supported Commodore files, then choose what to copy into your library. Your USB drive stays unchanged.” |
| USB first use | “Choose a folder to scan, or scan the whole partition. Nothing is copied until you select Import. Keep the drive connected until Project CBM confirms it is released.” |
| Scope preview | “Scanning: [folder]. Includes its subfolders. [N] compatible files found; nothing copied yet.” |
| Unknown classification | “The file format is recognized, but its computer and purpose are unknown. Choose them, or save it as unclassified. This does not guarantee it will run.” |
| Online description | “Find and save Commodore software from Assembly64. Internet connection required.” |
| Online first use | “Search, browsing and downloads use the Internet. Files you save stay in your library and work offline. Assembly64 receives your searches and download requests. Only download content you are entitled to use.” |
| Offline | “No network connection is available. Connect in CONTROL to search Assembly64. Your saved library is still available.” Actions: Network settings / Retry / Back |
| Service uncertain | “Cannot reach Assembly64. Check your connection or try again later.” Retry / Back |
| Access rejected | “Assembly64 did not accept this client's request. Online access is unavailable. Your local library is unchanged.” Details / Back |
| Save & Run help | “Save these files to your library, then start the selected file using [machine]. Your RUN default will not change.” |
| Identical | “Already present: [N] files match existing copies. No extra copies were made at those destinations.” |
| Different collision | “These names already exist with different contents. Keep Both preserves both versions.” Keep Both / Skip / Details |
| Existing elsewhere | “A matching copy exists at [library location]. Keep this release together, or use the existing copy.” |
| Success | “Saved [N] files to Games → C64 → [folder]. Already present: [N]. Kept both: [N].” Open Library / Run eligible file / Done |
| Partial/cancel | “Stopped after saving [N] files. Those files are kept. [N] failed; [N] were not attempted.” Details / Retry remaining / Done |
| USB safe | “USB released. You can remove the drive.” Only after all relevant release checks succeed |
| USB uncertain/busy | “USB release was not confirmed. Leave it connected. Close programs using it and Retry, or shut down safely before removal.” |
| USB browser | “Browse USB read-only. Copy files to your library with Midnight Commander. Exit Midnight Commander to safely release the drive.” |
| Storage failure | “Not enough free space to finish safely. Completed files are kept. Free space in FILES, then retry the remaining files.” |

Help covers Games/Demos/Programs/Music in plain language, unknown machine handling,
disk sets, safe removal, offline use, saved locations and collision defaults. Keep
technical paths in Details, not required user decisions. Results always distinguish
saved files from launched programs and metadata exclusions from failed content.

## H. Documentation plan for later implementation

Do not edit shipped manuals now to imply these proposals exist. Implementation must
update built-in help and external docs together, with links from the existing index.

| Exact Product document | Future change |
| --- | --- |
| `docs/README.md` | Index new guides and implemented-version boundaries |
| `docs/release/getting-started.md` | First USB import; optional online path; offline library remains useful |
| `docs/release/user-guide.md` | New CONTENT/FILES navigation and key conventions |
| `docs/release/content.md` | Classification, preserved paths, destinations, existing-library compatibility, duplicate policy |
| `docs/release/usb-import.md` (new) | Scope/preview/selection, supported formats/filesystems, cancellation and safe release |
| `docs/release/online-library.md` (new) | Assembly64, Internet/privacy, search/detail/save, service errors, attribution, limits |
| `docs/release/download-and-run.md` (new when implemented) | Permanent save, machine choice, multi-disk start, unsupported media, launch failures |
| `docs/release/files-and-usb.md` (new) | Read-only MC workflow, copy semantics, exit/unmount and busy recovery |
| `docs/release/networking.md` | Outbound HTTPS requirement, diagnostic limits, no inbound listener requirement |
| `docs/release/troubleshooting.md` | DNS/TLS/schema/access/space/cancel, file collisions and uncertain USB release |
| `docs/release/accounts-and-layout.md` | Downloaded folders and private index/provenance locations |
| `docs/release/recovery.md` | Back up content/provenance; reconcile index; interrupted-job recovery |
| `docs/runtime/content-ingestion-contract.md` (new) | Versioned candidates/plans/results, lease and cancellation model, security boundaries |
| `docs/security.md`, `docs/provenance.md` | Reviewed provider/network policy, metadata privacy and actual code reuse/rights evidence |
| `docs/testing.md`, future qualification records | Fixture/native/Pi evidence and measured resource limits |

Menu owns its help text, UI bridge contract and focused tests; Product owns the
manuals. Do not revive the historical public-docs sync script. This design and the
existing roadmap are planning authority until replaced by an accepted contract.

## I. Security, privacy, licensing and resource controls

### Controls proposed for implementation

- All parsing, downloads, hashing and library writes run as pcbm. Privileged code
  owns only fixed local device/mount/session operations and worker supervision.
  An online-only job never invokes sudo or enables a network service.
- Treat USB names, JSON fields and media as hostile input. Validate schemas,
  lengths, counts, path components, scalar types and nesting. Strip terminal
  control sequences from display text; preserve original provenance safely without
  interpreting markup, shell expansions or dialog options. Opaque IDs are UI tags.
- Use descriptor-relative no-follow path resolution throughout, not just a prior
  `resolve()` check. Reject symlinks/special files in sources, destinations and
  staging. Check file/device identity again after preview and before commit; a
  changed source requires review, not silent use of the old plan.
- HTTPS with certificate/hostname verification. Fixed reviewed service endpoints;
  percent-encode validated path IDs/query fields. No arbitrary URL import. Validate
  redirects to an explicit HTTPS host set; no loopback/private/link-local redirect
  targets. A provider-supplied link is display metadata, not fetch authority.
- Do not use the official firmware's plaintext HTTP fallback. No automatic external
  config, host executable, firmware or post-download script execution. No archive
  extraction initially. Later ZIP support would need member/count/expanded-byte/
  ratio/depth limits, traversal and link rejection, name collision handling and
  independent qualification; it is not a side effect of supporting downloads.
- Stream to exclusive job-owned partial files on the destination filesystem;
  validate expected size where trustworthy, actual format and complete stream,
  hash and fsync, then commit without overwrite races. Provider hashes, if later
  supplied and validated, add evidence; locally computed SHA does not authenticate
  the publisher. Detect HTML/error bodies posing as media where format permits.
- No public logs of searches, USB filenames, network identity or library manifests.
  Keep bounded private error codes and user-requested details. No telemetry or
  automatic query-history persistence; provenance/history can be cleared. Explain
  the remote service sees client IP and requested searches/files. TLS does not
  hide requests from the service.

### Suggested initial budgets — proposals, to measure on Pi 4

Keep existing USB depth/entry/2 GiB transfer limits and 256 MiB minimum free-space
margin initially; do not silently widen them. Apply byte caps to downloads even if
Content-Length is absent or false. Space reservation covers full staging plus final
files that coexist and a conservative floor: at least 256 MiB, raised when measured
maintenance/first-boot needs require it. Recheck while writing; another application
can consume space after preview. No unsupported fixed SD-card minimum.

Use one foreground transfer at a time. Proposed network budgets: 5-second connect,
15-second metadata request, 30-second inactivity timeout and 10-minute per-file
ceiling, with Cancel processed within one second plus bounded cleanup. These are
targets to validate, not claims about the service or current hardware. Retry only
idempotent reads, at most twice automatically with backoff; access/schema errors
require an explicit recovery path. Respect longer provider rate limits.

Cancellation therefore needs an interruptible transport or a supervised ordinary-user
worker whose socket can be closed/worker terminated and reaped; merely timing out
the UI while an uncontrolled download continues is insufficient. USB release waits
for source readers to stop. The UI must distinguish “Cancelling” from completed cleanup.

Initial UI result pages: 20–50 rows, configurable backend fetch ceiling 100;
bounded metadata responses (e.g. 2 MiB), no whole-catalogue fetch. Cache presets and
categories only after validation, with timestamps/expiry, e.g. 24 hours and a 16 MiB
total metadata budget. Stale metadata cannot authorize download routing. Search
pages may live in session memory; no persistent search log by default. No image
cache or thumbnail work initially.

Partial files are private and outside CONTENT listings; completed files move once,
avoiding a second full SD write. Cleanup targets only recorded owned temporaries,
never wildcard-deletes user content. After interruption offer retry; do not promise
HTTP Range resume until the service's validator/range behavior is established.
Any later resume must verify entity identity. Clear expired metadata independently
of saved content. Limit journal/history size; hash while transferring to avoid extra
reads. Rehash existing files only when comparison/reuse requires it.

### Licensing/provenance disposition

The reference manager's `LICENSE` and Cargo manifest declare MIT, copyright 2026
Marcin Spoczynski. MIT requires preservation of its copyright/permission notice
when copying substantial code. Its Assembly64 module says several behaviors were
ported from `u64ctl/src/u64mui/assembly64.c`; that antecedent's provenance/license
has not been independently audited here. Do not assume the top-level MIT label
clears every inherited fragment. Official Ultimate firmware is GPLv3. Recommend
an independent small implementation of documented/verified protocol behavior,
with reference attribution, rather than code translation or copying. Any later
reuse needs a file-level origin/license review and corresponding notices/source
handling. This study redistributes neither implementation.

Project CBM would distribute its client, not the Assembly64 desktop software,
catalogue dump, screenshots or hosted titles. Downloads are explicit user requests
into user storage, never image/factory inputs. Availability does not establish
redistribution rights or entitlement to use every title. Record the actual source
and known license information without a blanket permission claim. Confirm service
access, attribution and branding expectations before distribution; no operator
contact or agreement is implied by this study. Synthetic or explicitly licensed
test media is required for fixtures and redistributable test archives.

## J. Test and validation plan

No proposed behavior is marked tested. This study inspects existing tests; it does
not run privileged/native/image tooling or infer new physical qualification.

| Layer | Cases / acceptance evidence |
| --- | --- |
| Pure unit tests | Candidate/plan/result schema bounds; extension versus semantics; unknown metadata; every family/profile; C128 80col; G71; resource/SID rejection; stable paths; exact/other-path hash matches; local edits invalidate reuse |
| USB fixture tests | Nested/mixed trees, scoped root, files/folders/all selection, empty/unsupported files, recognized metadata versus legitimate dotfiles, huge trees/depth/entry caps, unreadable directories, malformed/long/control/Unicode names |
| Writer/fault tests | No-overwrite races; identical/different collisions; whole-set Keep Both; symlink replacement attacks; source changes after preview; short/growing reads; disk-full before/during fsync/commit; interruption at every journal transition; metadata failure after commit |
| Broker/client/Menu boundary | Success/partial/error/cancel survive both process status and JSON validation; all counts preserved; unknown fields bounded; missing/failed unmount stays conservative; setup gate, unknown/stale token, wrong caller, invalid paths/options rejected |
| Native isolated Linux | FAT/exFAT/ext4 source bytes unchanged before/after success/failure; actual mount flags/UID; no root/boot or mounted-disk admission; stale diskseq/device reuse; disconnect/replug; multiple partitions; busy unmount; caller crash; shutdown cleanup |
| MC lifecycle | Read-only source and writable library; forbidden source writes; F10/exit returns to release screen; child/shell holding mount causes honest Busy; import/browser exclusion; stale session recovery; no forced release claim |
| Offline network fixtures | No interface, DNS, timeout, refused TCP, TLS errors, access 401/403/464, rate 429 with Retry-After, 5xx, cancellation; no raw exception/secret/URL dumps; Back always available |
| API fixtures | Valid/empty/large pages; missing/wrong-type fields; unknown categories; malformed JSON; response caps; duplicate IDs with different source/category; changed schema; no provider-title dedup data loss |
| Download fixtures | Wrong size, false Content-Length, endless/slow stream, HTML instead of media, unsafe redirects/paths, interruption, changed remote entity, low space, repeat downloads, cross-USB duplicate, incomplete multi-disk set |
| UI/contract tests | Keyboard only; visible scope and count; no implicit select-all; preserved selection after Back/retry; terminal-control escaping; small screen paging; real dialog Cancel; help and manuals match actual labels/actions |
| Launch integration | Existing launcher only; no saved-default change; no remote flags/config; all registry families routed or safely rejected; selected disk member; failed launch preserves files; repeated Cover/VICE/F10 return |

Use local fake HTTP servers and retained sanitized schema fixtures for deterministic
tests. Live tests are a small, rate-respecting contract smoke after provider access
is established, with a rights-cleared download; they are not dependencies of every
unit test. Native Linux tests cover mount/kernel semantics that macOS mocks cannot.

Future owner-authorized Pi 4 qualification: visible preview/checklist readability,
USB hot removal and safe-removal feedback, MC lifecycle, real Ethernet/Wi-Fi online
and offline recovery, cancellation under load, storage pressure, and representative
saved-media launch/Cover/F10/audio/input/return. Record exact candidate hashes and
tested profiles. The 1.1.0 PASS does not qualify new UI/network behavior or every
machine. Measure menu latency, time-to-first-page, peak RSS, scan time and SD writes
for defined trees (100/1,000/10,000 entries); no unbounded memory growth across
repeated searches/downloads. Set measured acceptance budgets before freezing a
candidate. Normal RUN/MACHINES must incur no online startup cost.

## K. Migration and compatibility

Published 1.1.0, its hashes/tags/20 assets and original behavior remain untouched.
No background migration, scanning, deduplication, reclassification or folder moves.
Existing Imported/category/legacy trees remain browsable under current routing.
New jobs create new destinations only after review; they never retrofit provenance
claims onto old files. Optional index rebuilding is explicit, bounded and disposable.

Keep Product registry/ordinary preferences authoritative and VICE settings user-owned.
No new default or implicit service activation. Version the new ingestion IPC and
negotiate capability before showing new Menu actions; an older installed runtime
gets an unavailable explanation rather than a malformed request. The reporting fix
can preserve schema-1 semantics with optional validated fields; review compatibility
in both repositories before adopting a larger job/session protocol.

The new content source does not change CCGMS/TCPser setup or replace CCGMS. User
files copied through SFTP, file sharing or MC continue to work without a database.
Backup/restore guidance must preserve content independently from advisory metadata.

## L. Implementation phases and version strategy — for later approval

| Phase | Bounded outcome | Exit evidence |
| --- | --- | --- |
| Preparation | Design accepted; later resolve Assembly64 access/terms without impersonation before Phase 5 qualification | Accepted scope and documented service contract/remaining limits |
| 1. Reporting correctness and contracts | Fix the existing roadmap client/result loss and establish contracts needed by later work | Full broker/client/Menu success and failure transport tests |
| 2. USB discovery/plan vertical slice | Separate scan/selection/transfer, bounded sessions, shared safe writer/results; design shared structures using real USB needs | Fixture and native safety/cancel/cleanup tests; no unused provider framework |
| 3. USB UI and content navigation | Scoped preview, explicit selection, destinations, classification evidence, collisions, help | Dialog/usability and Pi 4 measures; preserve current libraries |
| 4. Explicit USB browsing | Reuse proven access supervisor for MC sessions | Native lifecycle plus owner physical safe-removal workflow |
| 5. Assembly64 Save to Library | Small HTTPS adapter, search/pages/details, supported-file selection, provenance, offline/retry | Verified service access/terms and deterministic/live contract tests |
| 6. Save & Run | Existing launch path, explicit ambiguous routing and member selection | Profile/lifecycle tests plus representative owner hardware checks |

Screenshots, generic ZIP extraction, advanced AQL, writable USB browsing, automatic
title-specific settings and additional providers are separate later decisions, not
requirements for the first online slice. Phase 4 can be prioritized independently;
phase 5 must not delay a useful qualified USB improvement solely for abstraction.

[Build policy](../build-and-release.md) requires semantic Product versions, independent
Menu versions and exact dependency identities. It does not assign this feature a
number. **Recommendation:** a small reporting-only fix could be patch maintenance
if separately requested; the redesigned acquisition UI and Online Library are an
additive feature milestone, provisionally **1.2.0**, not assumed 1.1.1. This is a
version recommendation, not a created release. No need for a major version while
libraries, launch/default behavior and component boundaries remain compatible.

In a subsequent implementation task, use distinct private source/package/lock/attempt
identities for changed inputs and required host/native/actual-image/Pi gates. Never
replace a finished 1.1.0 artifact. Product/Menu versions may differ; pin actual
compatibility. Publication remains a separate owner authorization.

## M. Owner decisions resolved; external preparation remains

The owner accepted CONTENT as the sole normal acquisition home, the six-phase
sequence and provisional 1.2.0 direction. There is no known existing Assembly64
contact/access arrangement. These preference questions are closed; do not reopen
or duplicate them during routine implementation planning.

The unresolved external facts are legitimate client access/identification, HTTP
464 meaning, supported endpoint/schema behavior, usage/rate/cache expectations and
attribution. Resolve these in a later implementation-preparation phase, without
impersonating another client. No agreement, service permission or provider contact
is claimed. See the acceptance record above for the controlling decisions.

## Original design-study checkpoint (historical)

Deliverable is this proposal, with a link from the existing roadmap. Existing runtime,
Menu, tests, public manuals and release records are not modified. Checks for this
document are local link existence, proposal/current-state distinction, whitespace,
file size and accidental sensitive-data review. No tests of unimplemented features,
new hardware PASS, provider permission or API availability are claimed.

Study validation: 17 local links across this draft and its roadmap reference resolve;
sections A–M, fenced blocks and whitespace checks pass. Sensitive-pattern scan and
manual review found no private credentials or device/user content. The original roughly
61 KiB design is intentionally outside the shipped user-manual set. Existing tests
were inspected, not run as evidence for proposed functionality. Only the new design
file and the four-line roadmap reference changed; they remain an uncommitted review
draft. Product source HEAD, both release tags and the Menu/reference worktrees remain
unchanged. No CURRENT-STATE or historical release/recovery record was rewritten;
this review checkpoint and the roadmap link record the bounded design-only work.

Original next action was owner design review; that review is now complete as recorded
above. Next engineering milestone is Phase 1 groundwork for provisional 1.2.0, only
in a subsequent implementation task. This documentation task implements no phase.
