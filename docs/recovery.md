# Black-box recovery contract

Status: required architecture for Project CBM 1.1, designed 2026-09-15; builder,
metadata generator, runtime information command and first boot are **not implemented**.
This specification supplements [build/release](build-and-release.md), [provenance](provenance.md)
and [testing](testing.md). It is self-contained; reference projects and conversations
are not recovery dependencies. No 1.0 history or release is changed by this contract.

## 1. Objective and authority

A stranger with only Project CBM repositories and intentionally retained artifacts
must be able to identify the product, explain its design, map a release to inputs,
restore source, reconstruct the build environment, evaluate qualification and resume
the documented next task. A successful build alone does not meet this requirement.

| Term | Question answered |
| --- | --- |
| Black-box recovery | What exists, why, how it was made, what evidence supports it, where it lives and how to resume without conversational memory? |
| Reproducible build | Can declared inputs produce the expected semantic or bitwise output again? State which equivalence was tested. |
| Disaster recovery | Can source, inputs, records and build capability survive loss of GitHub, the workstation or the storage device? |
| Release provenance | Can these particular artifact bytes be traced to exact source, patches, inputs and construction records? |

Complete recovery combines **source + retained external inputs + build recipe and
environment + product artifacts + qualification**. Also required are rationale,
licenses, verification/trust history, schema readers, a portable inventory, access
custody and tested independent backups. Signing-key custody is separate from public
provenance. A known checksum proves integrity against a trusted reference, not who
created it; a URL, tag name or colocated checksum alone is not independent trust.

### Read and resume

1. Read README, AGENTS and CURRENT-STATE. They identify purpose, last completed work,
   current release, protected decisions, known defects and exact next milestone.
2. Read architecture, this contract and build/release; consult provenance for 1.0.
   Read testing/security for evidence limits and change boundaries.
3. Inspect branch/HEAD, recent commits, staged/unstaged/untracked work. CURRENT-STATE
   describes the last completed checkpoint, not proof that newer work is disposable.
   Preserve unknown work; never reset/clean an unfamiliar checkout to match a document.
4. State the active task, verified facts, unknowns and next safe action. Follow the
   owner's current scope. A resume guide does not grant builder/publication authority.

Record material decisions with date, rationale, consequences and supersession in
the relevant architecture section. Keep CURRENT-STATE short; use Git commits and
focused acceptance records for chronology. Do not require an accumulating session
transcript, private source archaeology or another project's repository to understand
the public product or rebuild procedure.

### Protected rationale

| Decision | Why it exists / consequence |
| --- | --- |
| Console, Bash/dialog, SDL2 VICE, ALSA | Existing small appliance model; preserve recognizable behavior and Pi 3 resource headroom before adding framework dependencies |
| Pi 3 floor; Pi 3 through 500+ target | Product scope spans generations; upstream OS support cannot replace per-model qualification, especially 512 MiB Pi 3A+ |
| Separate product and Menu repositories | Product owns OS/build/integration/qualification/public docs; Menu owns independent scripts/assets/interfaces/packaging/tests; explicit dependency mapping prevents source/image drift |
| 1.0 original Trixie; 1.1 current-Trixie builder | Corrects the remembered OS history without inventing a Bookworm line or rewriting releases |
| Immutable releases and forensic recovery refs | Preserve what shipped; reconstructed or normalized source must not be labeled byte-exact history |
| One generated metadata authority | Prevent another VERSION/config/About/CI mismatch; all release identity derives from the same frozen lock |
| Separate embedded identity and final attestation | Prevent hash cycles and avoid claiming hardware qualification before the final image exists |
| Portable locators and independent backups | TheBench and today's Mac are deployments, not permanent prerequisites |

## 2. Recovery scenarios and present coverage

| Scenario | Procedure / required retained material | Coverage at this checkpoint |
| --- | --- | --- |
| A: abandoned for years | Follow the read/resume sequence; project-owned docs explain purpose, rationale, Menu mapping, hardware, state and next work | Documentation available locally; no independent fresh-person comprehension drill yet. New commits are not pushed. |
| B: GitHub lost | Verify recovery index, restore both full bundles and all inventoried refs, recover release JSON/assets/provenance separately | Accepted preservation bundles were restored offline and checked; see section 8. Later checkpoints need their own bundles. |
| C: development Mac lost | Obtain an independent recovery kit, remap logical roots, restore source and verified inputs, install recorded tools | Paths are now explicitly non-normative; independent backup copy not established. TheBench survives only if it is separately available. |
| D: Linux builder lost | Bootstrap a clean compatible Linux environment from retained host/tool inputs and recipe; no hidden installed packages or shell state | Required for 1.1; no builder/environment exists yet. |
| E: only image survives | Read embedded RECOVERY.md/identity/lock/inventories/schema/recipe without boot or network; label authentication and input-availability limits | Required from 1.1; 1.0 needs forensic inspection. Identity/recipe recovery is possible by design, but absent external package/source closure cannot be recreated from hashes alone. |
| F: running system | pcbm-info displays the immutable base-image identity and separately labels live drift, if checked | Interface defined below; not implemented. Base-image identity does not certify an updated machine's current packages. |
| G: upstream inputs vanish | Resolve every lock entry from verified retained source/package/tool closure, not a moving URL or cache | Required before 1.1 release. 1.0 closure is incomplete. |
| H: TheBench lost/corrupt | Restore an independently held recovery checkpoint; verify catalog, artifacts and refs before use | Open disaster-recovery gap; Mac + associated disk alone do not satisfy it. |

## 3. Portable recovery kit and retention

The recovery kit has a plain-text README, a versioned JSON index, manifests and
named snapshots. It records what each artifact is, its role, source/provenance,
license/handling class, relative locator, size, digest, availability and dependencies.
URLs are advisory mirrors; an offline relative locator must resolve required inputs.
Paths are relative to the kit root, cannot escape it, and cannot depend on symlinks
outside it. Keep bundle/source trees complete, including any future submodules or
Git LFS objects: a superproject Git bundle alone would not retain those payloads.

Proposed configurable interfaces for later tooling:

- `--source-root`, `--menu-source`, `--storage-root`, `--archive-root`, `--inputs-root`
  and `--build-root`; explicit CLI values override operator-local configuration.
- The source and Menu need not be siblings. Bulk roots must be explicitly selected,
  validated for capacity/filesystem semantics and recorded privately, never silently
  replaced with internal-disk/temp defaults. Local absolute paths stay out of locks.
- A logical `artifact_id` resolves to `relative_path`, `size_bytes`,
  `digest: {algorithm, value}`, media type, license and retention/availability state.
  Preserve original filenames inside evidence snapshots; locator mappings do not
  authorize reorganizing or renaming historical files.

Current deployment only: source `~/Code/project-cbm` and `~/Code/project-cbm-menu`;
historical evidence `/Volumes/TheBench/Projects/Project CBM`; bulk work
`/Volumes/TheBench/ProjectCBM-Work`. These literal paths are not product requirements.
Existing preservation manifests record absolute `root` as capture context. Their
entries are relative: on a replacement machine, use a verifier with an explicit
root override or a separately documented, provenance-linked working descriptor.
Never edit/re-hash the original manifest to hide relocation or mismatches. The
current inventory utility does not yet provide a root-override option; its exact
whole-tree mode/mtime/xattr checks may also differ on another filesystem. Content
integrity and metadata-fidelity results must be reported separately.

### What must survive independently

| Retain independently | Reason / treatment |
| --- | --- |
| Complete Git refs/objects, unique local work and reviewed patches | GitHub and a workstation are not backups; dirty work needs a separate private patch/untracked archive, not just a bundle |
| Unique 1.0 raw evidence, released XZ, local notes/logs/art/license evidence | Cannot assume they can be recreated; encrypted private history where necessary; deduplicate only new backup transport by verified content identity, never originals |
| Frozen locks, schemas/readers, recipes, environment specs, release metadata/notes | Explain construction and preserve the ability to interpret old releases |
| Exact upstream/builder sources and patches; full .deb closure and corresponding source packages | URLs/snapshot services may disappear; preserve all runtime and build/host dependencies, not only the named applications |
| Authenticated repository metadata, public keys/signatures, trust and key-transition records | Verify old inputs/releases after mirrors or signing keys change; do not bypass expired metadata by disabling verification |
| Exact released artifacts and qualification evidence | Prove what was published/tested; do not replace exact releases with a later approximately equivalent build |

Recreatable material normally excluded from independent backup: verified disposable
worktrees, unpacked copies already represented by retained originals, compiler/pip
caches, failed builds and temporary images. A cache holding the only copy of an old
input must be promoted into retained inputs first. Keep at least the exact release
XZ and raw-image digest; the raw release can be decompressed if that round trip is
verified. The unique pre-shrink raw image is a different artifact and must survive.
Corresponding-source/license obligations and uncertain rights require review; local
retention is not permission to redistribute proprietary or private evidence.

Recommendation, not configured: keep one independent encrypted copy outside the
Mac/TheBench failure domain, preferably offline/off-site, with separately recoverable
unlock/access material and named custody. Verify SHA-256 and inventory after each
accepted checkpoint/release transfer; retain the prior verified checkpoint until
the new one is checked. Keep release and unique historical snapshots indefinitely,
use quarterly full integrity checks and a six-monthly isolated restore drill, and
repeat after medium/custodian changes. Record dates, scope, results and missing
items. Initial recovery-point target: no loss beyond the last accepted checkpoint;
measure restore duration before promising a recovery-time target. No service,
purchase, encryption, rotation or backup destination was provisioned in this task.

## 4. Machine-readable contract (design, not a released schema)

Use UTF-8 JSON with a terminal LF: common offline readers and explicit types suit
manifests better than executable shell fragments or ambiguous configuration syntax.
Store a human-readable field guide alongside it. No network-resolved schema is
required to identify an image. [Design worksheet](recovery-contract.example.json)
uses nulls intentionally and **must never be accepted as an actual release lock**.
Formal JSON Schemas and validators are an early 1.1 implementation task.

Each document has `format` (stable kind) and integer `schema_version`. Schema 1
is the proposed first contract, not a claim that 1.0 used it. Hash exact saved bytes
with SHA-256; never parse/reformat before verification. Define deterministic writer
rules (UTF-8, LF, sorted keys, stable list order, no duplicate keys/NaN/floats) in
the implementation. Do not require a specialized canonical-JSON implementation
merely to verify stored bytes. Integers and decimal strings suffice for measurements.
Document raw-byte digest scope and explicit exclusions; no hidden canonicalization.

| Document | Authoritative fields / relationship |
| --- | --- |
| `release-lock.json` (L) | Product version/candidate, architecture, target hardware policy; exact OS/base or builder recipe; integration source; Menu/VICE/TCPser identities; package closure; patches/config/assets/schema; build environment, flags, retention references, source-date epoch and sealed-image policy |
| `build-record.json` (B) | L digest; actual tool/environment versions, commands/recipe, step outcomes, sanitized logs and sealing results; output package/config inventory checks. Cannot claim final image hashes or post-image qualification. |
| `identity.json` (E) | Product/build identity projected from L; full L digest as build ID; component mapping; B/inventory/schema/recipe-document hashes; qualification policy and external lookup identity. No editable independent VERSION source. |
| `qualification.json` (Q) | Exact raw image digest, E/L digests, test-suite revision, model/revision/RAM/kernel/firmware/EEPROM, test environment and measurements, pass/fail/untested/blocked, reasons/known limits; no hash of a release manifest that contains Q |
| `release-manifest.json` (R) | Exact L/B/E and inventory/source/recipe/Q artifact digests, raw/XZ image sizes/hashes, release designation, qualification/limitations summary and release-notes references |
| `recovery-index.json` | Independent checkpoint inventory: repository IDs/bundles/refs, artifacts/locators, trust/handling class, schema/readme references, availability and completeness gaps; excludes its own digest |

For each component record its independent version; source repository ID/advisory
URL; Git object format and full commit; explicit tag and tag object (where annotated)
plus peeled commit; source archive digest/size; ordered patches and base commit;
build flags/toolchain; binary package version/architecture/hash; license/corresponding
source locator. Menu requires an explicit candidate/release tag, peeled commit and
artifact checksum. Never infer the Menu version from the product number or consume
arbitrary main. TCPser may have a version string differing from its release tags;
record both truthfully. Source hashes and Git object IDs are different fields.

OS identity must distinguish a pinned official image URL/hash from a pi-gen recipe
constructing Lite out of packages. Record pi-gen full commit, stages/config/patches,
APT origins and authenticated index snapshots, full binary and source package
closure and exact kernel/firmware package hashes. Do not claim an official base
XZ was used just because an equivalent stage2 was built.

Freeze L after independent component package acquisition/builds have produced their
known artifact hashes, before final image assembly. Retain component build records
and their input dependencies too. If a needed artifact hash is still unknown, this
is a planning candidate, not a frozen lock. The integration commit identifies the
recipe source frozen before generating L; do not ask a committed lock to contain
the hash of the same Git commit that contains it. Release catalog/tag commits can
follow assembly and must distinguish their identity from the integration commit.

### One-way checksum graph

```text
retained source/environment/packages -> frozen L
L -> image construction -> B + installed inventory + recipe/schema documents
L + B + inventories -> E
L/B/E + local documents -> embedded recovery files -> finalized image I -> XZ
I + E/L identity + tests -> Q
L/B/E + I/XZ + Q + artifacts/notes -> R
R + distributed artifacts -> SHA256SUMS -> detached signature
```

Each arrow is a generation/reference relationship; documents only hash already
finalized predecessors. A file never includes its own digest. In particular:

- E includes neither the final image hash nor R's checksum. Embedding either would
  cause a cycle. It identifies the expected external attestation by build ID/format,
  with an optional advisory URL; R later binds E to the exact image and Q.
- Q is produced after I is frozen and tested. E embeds the qualification policy,
  required tests and status `external-attestation-required`, never an assumed pass.
  External Q/R record actual qualified hardware. Do not modify I after testing to
  insert test results; doing so creates a new candidate needing qualification.
- SHA256SUMS covers distributed payloads including R and Q, excluding itself and
  its detached signature. SBOM references do not hash the containing whole image.
  A runtime package inventory may be embedded; an external full-artifact SBOM can
  describe the recovery metadata package after assembly without a self-hash cycle.
- Use one stable build ID derived from full L SHA-256. A rebuild attempt gets a
  separate attestation/attempt ID and actual UTC time. Reusing inputs does not prove
  equal outputs. Source-date epoch is a deterministic input, not a fabricated date
  of observed execution. A changed input means a new L/build ID.
- Pin a standard SBOM format/version and its offline reader/schema during 1.1 design;
  retain an ordinary JSON package inventory regardless. Field presence is not proof
  of completeness: compare installed packages and component files with the lock.

### Schema evolution

Retain every released schema, field guide, validator source/dependencies and small
test vectors beside its release kit, with an embedded plain-text field guide. Never
rewrite an old manifest into a newer schema as if it were the original bytes.
Derived migrations get new digests and an explicit original-digest link. Preserve
unknown fields when inspecting. Unknown schema versions remain displayable as raw
JSON/text but cannot be declared validated or used for automated reconstruction.
Schema version is independent of product, Menu and configuration versions. Missing
required values are errors in 1.1 locks; historical unknowns use explicit evidence
status in a historical record, never guessed pins or zero-filled fake digests.

## 5. Self-describing images and running-system interface

Proposed authoritative directory: **`/usr/share/project-cbm/recovery/`**, package-owned,
root-owned ordinary readable files, immutable by release policy. `/usr/share` is
appropriate for static data; editable `/etc` configuration must not become the
identity authority. This follows the [FHS static-data guidance](https://refspecs.linuxfoundation.org/FHS_3.0/fhs/ch04s11.html).
No chmod/immutable-filesystem machinery is implemented here, and root compromise
can still alter files. Integrity requires comparing against trusted external hashes.

```text
/usr/share/project-cbm/recovery/
  RECOVERY.md                 plain-text meaning, scope, paths and offline procedure
  identity.json               E, readable directly; no menu/library needed
  release-lock.json           exact public-safe L bytes used to build
  build-record.json           public-safe B summary, not a raw builder transcript
  packages.json               installed package identity inventory
  schemas/                   frozen field guides/schemas needed to read these files
  recipe/                    compact product recipe/config/patch snapshot and rationale
```

The compact recipe snapshot must contain the actual product integration stage,
configuration/sealing/first-boot recipe sources, patch references and reconstruction
instructions from the pinned integration commit. Include Menu source/package identity
and component source locators; do not duplicate all compiler sources/package archives
in the runtime image. Retained full Git bundles and upstream closure live in the
recovery kit. Budget metadata/recipe size during Pi 3 qualification.

Offline procedure: open a copy read-only with a suitable Linux/ext4 recovery tool,
identify the root filesystem by partition/filesystem evidence rather than assuming
partition 2, read RECOVERY.md and identity.json, verify L/B/inventory/recipe references,
and resolve external R/Q by build ID if available. Avoid journal replay/writes to
the evidence image; use forensic read-only tooling or a disposable working copy.
Paragon extFS on today's Mac is optional convenience, not a product dependency.
Neither boot, network, SSH, Menu, jq nor a custom CBM program is required to read JSON.

Only-image limits: E identifies the sealed base and construction recipe; it cannot
prove its own authenticity, reconstruct missing external source bytes, recover
post-image Q, or establish that an already-used/modified image is pristine. Report
these as unavailable/unverified rather than guessing. Existing `/etc/pcbm/version.conf`
is historical runtime configuration; adapting future version displays to E belongs
to 1.1. Do not overwrite Raspberry Pi/Debian `/etc/os-release` as a substitute.

Proposed product-owned **`pcbm-info`** (not implemented):

- Default: offline, unprivileged, read-only summary of product version, full build
  ID, architecture, base/builder/integration and Menu/VICE/TCPser mapping; print
  qualification scope as an external attestation reference, not a compatibility pass.
- `--json`: emit the authoritative E bytes; `--root PATH`: inspect an already
  accessible mounted root without mounting, contacting services or requiring sudo.
- `--verify`: verify local referenced metadata/recipe hashes and E/L consistency;
  a pass means internal integrity only, not publisher authentication/full-disk health.
- Exit 0 on a successful requested operation; 2 for absent metadata, 3 for malformed
  or unsupported schema, 4 for integrity/mapping mismatch. Never fall back silently
  to an invented version from filenames, Menu main or current package versions.
- Label default output “base image identity; live system may have changed”. Any
  later live-inventory comparison is separate opt-in output and never rewrites E.
  Manual/Menu displays consume this same authority; no independently edited values.

### Sealing and first boot evidence

L identifies the sealing and first-boot recipe/policy revision. B records static
checks that builder state, reusable keys/IDs, credentials and unintended content
are absent and that expansion has one owner. Q records two fresh flashes' unique
identity, offline initialization, interrupted/retried first boot and service-policy
results without storing keys/passwords/unique device identifiers publicly. The
recipe describes what generates identity, when completion is recorded and how retry
works. Do not embed test-device identity or mutate E on first boot. A manifest does
not sanitize an image by itself; implementation and tests remain 1.1 work.

## 6. Source and environment disaster recovery

### Restore Git without GitHub

Obtain a verified kit/index and a NEW empty destination. Prefer full standalone
bundles over incremental chains; verify bundle digest against an independently held
catalog before loading it. The accepted baseline has `git/<repo>/after-local.bundle`,
`after-local.json`, before-state bundles/.git archives and live remote snapshots.
The latest accepted design checkpoint must be retained separately, not written into
that sealed preservation archive. A complete restore uses the index's latest
checkpoint, not merely the first file named after-local.bundle found on disk.

Example after setting absolute paths appropriate to the replacement machine:

```sh
git bundle list-heads "$bundle"
git clone --mirror "$bundle" "$new_mirror"
git -C "$new_mirror" bundle verify "$bundle"
git -C "$new_mirror" fsck --full
git -C "$new_mirror" show-ref
git clone --no-hardlinks "$new_mirror" "$new_checkout"
```

Compare **all** restored refs with the index (including tag objects and peeled
commits); verify main, maintenance/1.0, recovered/image-v1.0.0-runtime and Menu
pre-v1-skeleton/backup refs. The mirror preserves all refs; the working clone may
represent non-current branches as remote-tracking refs. Create a local working
branch from its verified restored ref only when needed; never replace a canonical
checkout or fetch into the archived mirror. [Git documents bundle scope](https://git-scm.com/docs/git-bundle)
and [mirror ref preservation](https://git-scm.com/docs/git-clone#Documentation/git-clone.txt---mirror).

Git bundles do not restore the entire worktree, reflog, config/hooks or hosted
release assets/settings. Before-local .git archives preserve additional private
administrative evidence, not a ready-to-trust environment: inspect them isolated,
do not activate hooks/credentials/old absolute worktree paths. Restore release JSON,
assets, notes, provenance, archived public verification keys and qualification from
the kit. Future retention must record applicable hosting settings/protections and
external LFS/submodule payloads. Retain symbolic HEAD/ref targets as well as object
IDs. Credentials for a replacement host are provisioned separately; restoring
source does not authorize pushing or republishing recovered releases.

### Recreate a lost build environment

Before the first 1.1 release, retain an environment recipe that specifies:

- Linux distribution/release and architecture, supported native/emulated mode,
  kernel/privilege/mount/loop-device requirements, minimum tested RAM/disk/CPU,
  filesystem semantics (ownership, permissions, case sensitivity, symlinks/xattrs),
  and resource estimates. Pi build-host capacity is separate from the Pi 3 runtime floor.
- Bootstrap image/ISO/rootfs or OCI digest where used, verification metadata,
  package versions/full host build-dependency closure and corresponding sources,
  toolchain/compressor/filesystem tools, locale/timezone and source-date epoch.
- Full pi-gen source at a commit, integration source, environment config, command
  sequence, compiler flags, ordered patches and a minimal environment capability
  check. No reliance on a home directory, shell history, installed global tools,
  private registries or secrets for offline reconstruction.
- Networked acquisition/authentication followed by assembly from retained inputs;
  prove a rebuild with upstream access unavailable. For expired repository metadata,
  retain original authentication/time evidence and define an offline trust procedure;
  never silently turn signature checks off to get an old build to run.
- A plain-text bootstrap path if the convenience VM/container tooling vanishes.
  Retain the underlying recipe and dependencies, not only a VM snapshot. Bare-metal
  Linux and a suitable VM are deployment choices; macOS/APFS/Paragon are not requirements.

This environment is unimplemented. A future fresh host must pass bootstrap and
input-completeness checks before any reproducibility claim. Exact 1.0 rebuilding
cannot be guaranteed by provisioning a modern Linux machine.

## 7. Historical 1.0 assessment

| Evidence status | Honest 1.0 result |
| --- | --- |
| KNOWN | Exact published XZ/docs/checksum bytes; Trixie 13.4 April 21 base metadata, vendor kernels, installed package inventory and VICE 3.10; existing Git tags/releases |
| RECOVERED | Exact 17-script runtime with manifest/new forensic root tag, VICE build flags/output and TCPser checkout identity, local lineage/log/config evidence and preserved Git state |
| STRONGLY INFERRED | Larger raw image is pre-PiShrink; reusable identity may persist on clones; logs help connect development to release but do not prove every final build step |
| UNKNOWN | Original base-XZ digest, complete source/package/tool closure and final build/shrink command chain, independent VICE tar authentication/patch completeness, some content rights and all repeatable physical qualification |
| UNRECOVERABLE (if loss occurs) | Unique deleted evidence with no surviving copy cannot be regenerated by documentation. No specific historical unknown is currently declared proven unrecoverable; further evidence might exist. |

1.0 is recoverable as exact retained artifacts and source evidence, not as a proven
locked reproducible build or a self-describing 1.1 image. Do not add metadata to
historical images, repoint the formal Menu tag, normalize recovery scripts or fill
unknown fields to make a modern validator pass. An equivalent reconstruction must
have a new candidate identity, explicit deviations and new qualification; it is
never relabeled the exact old release. See [provenance](provenance.md) for hashes.

## 8. Acceptance tests and current evidence

| Test | Required proof / failure case | Current state |
| --- | --- | --- |
| A: context-free entry | Fresh person/agent uses only clone + linked retained kit; reports purpose/rationale/release/Menu/hardware/current state/unknowns/next task correctly; no old sessions or reference repos | Entry links reviewed; independent comprehension drill NOT RUN |
| B: GitHub unavailable | Restore both bundles into new locations, no remote access; compare all refs/tag objects/peeled commits and 17 recovery blob hashes; reject missing-prerequisite/corrupt bundles | PASS for accepted preservation checkpoint: product 5 refs, Menu 8 refs, 17 script hashes; both fsck passed, 2026-09-15 |
| C: offline image | Read mounted root on Linux and another ext4-capable reader with network disabled and no boot/Menu; derive exact mapping and verify local hashes | NOT RUN; 1.1 image does not exist |
| D: lost builder/upstream | Bootstrap fresh Linux using only kit, relocated paths and documented tools; verify complete closure, build twice and compare defined semantic/bitwise result | NOT RUN; builder deferred |
| E: metadata agreement | Generate projections from one L; compare L/B/E/R/inventories; reject a changed Menu pin, absent artifact, stale lock, dirty integration source or wrong digest | DESIGNED; generator/schema validator deferred |
| F: privacy | Public-field allowlist plus secret scans and manual review; synthetic forbidden categories are rejected; inspect actual filesystem sealing independently | Documentation reviewed; automated public-artifact/negative suite NOT IMPLEMENTED |
| G: schema longevity | Offline read old schemas/fixtures, reject unsupported validation, preserve original bytes and unknown fields; detect duplicate keys and tampering | DESIGNED; fixtures/validator deferred |
| H: qualification binding | Q names raw image digest + E/L + suite/hardware identity; changing image bytes invalidates association; PASS/FAIL/UNTESTED/BLOCKED cannot be collapsed | DESIGNED; no hardware tests |
| I: only-image limitation | Remove external R/Q/inputs; still identify release/recipe offline and explicitly report absent qualification/authentication/rebuild inputs | DESIGNED |
| J: checksum graph | Reject self-hashes/cycles and metadata rewritten after final image freeze; verify external checksums/signatures with independently trusted key | DESIGNED |
| K: independent restore | Restore latest checkpoint from independently held medium on a replacement root; compare catalogs; inject missing/corrupt input and verify stop with gap report | NOT RUN; independent backup missing |
| L: running drift | Installed package/update changes cannot rewrite base E or produce a false pristine report; malformed/absent E gets documented exit status | DESIGNED; pcbm-info deferred |

The actual B drill used only two retained full bundles in fresh mirrors under the
current bulk scratch root; no historical/reference tree or canonical checkout was
modified. Their digests are recorded in [provenance](provenance.md) and the external
preservation report. Passing bundle restore does not demonstrate off-site resilience,
image reconstruction or host provisioning. No pi-gen, image build, runtime program,
first-boot or service/privilege change occurred during this design phase.

## 9. Reference-project lessons (optional historical context)

These are observations from read-only old M1 copies on 2026-09-15, not dependencies
or current upstream claims. No fetch/pull/checkout/cleanup/commit was performed there.
The inspected deployment was `/Volumes/TheBench/from-imac-m1/Code/spitfire-ng` and
its `firecomm` sibling. These locations are only research citations; no recovery
step above needs them. Existing source/documentation was studied, not copied.

| Reference snapshot | Apparent state / material inspected |
| --- | --- |
| Spitfire-NG `e595346100b16171ff4b539e2817c4b30a55593b` (2026-09-10 commit) | CURRENT-STATE describes D3 accepted/published; local tracked status lists 27 missing tools. Read AGENTS/current-state/README resume guidance, documentation/decision/reference policies. Incomplete migrated working copy; cached origin alignment is not current remote verification. |
| FireComm `9bb51c6abe7a3dc957e73eb1b0b7430b2d293491` (2026-09-02 commit) | Tracked working state clean; CURRENT-STATE dated September 2. Read AGENTS/current-state, .codex/RECOVERY and DEVELOPMENT-RECOVERY. Not fetched or tested; untracked inventory/current remote freshness not established. |
| CircuitNET-NG kit inside that Spitfire copy | Read README, VERIFICATION and KEY-CUSTODY; no separate top-level CircuitNET repository found in the inspected directory listing. Documentation identifies kit 1.0; service publication is explicitly not verified. |

Adopt: durable current-state/decision rationale; preserve unknown/dirty work;
distinguish current source from shipped artifacts; provenance and reference independence;
actual pass/fail/deferred evidence; generated docs/metadata from a canonical source;
checksum exclusions; checksums vs trusted signatures; custody and historical public
key transitions. The CircuitNET kit already makes its outer checksum external to
avoid self-reference, a principle applied here to whole-image/qualification hashes.

Adapt: application recovery becomes OS/source/package/build-host/boot/sealing and
physical-model recovery. User-data backups, developer backups and public release
kits are distinct. Preserve original artwork and licenses rather than reconstructing
source from generated covers. Source provenance can be public while private corpus,
credentials and raw builder transcripts remain private.

Do not adopt mechanically: large phase/session logs as the entry point, duplicated
manual hierarchies, private-repo-only essential recovery knowledge, automatic push
at session close, app-specific platform builders or a “read-only health check” that
actually compiles/runs programs. FireComm's compiled-check lists are validation steps,
not literally read-only inspection. Its blanket avoidance of artifact-derived source
must allow CBM's explicitly labeled forensic recovery when original Git source is absent.
These boundaries prevent reference conventions from overriding CBM authorization.

## 10. Next milestone and remaining decisions

First 1.1 deliverable after new authorization: turn this contract into versioned
lock/E/R/Q schemas and offline validation fixtures, define the Linux bootstrap/input
retention plan and demonstrate a synthetic acyclic metadata graph. Then implement
the minimal pinned Lite + integration POC with embedded identity/recipe, retaining
the closure and producing test-bound external records from the start. This is part
of the builder's acceptance boundary, not optional release documentation at the end.

Owner choices still open: independent encrypted backup/custody, Linux host/location,
public signing/trust custody and publication policy, exact standard SBOM format,
and measured reproducibility/qualification acceptance. Do not invent those choices
as historical facts. The requirement and proposed metadata/interface design are
documented now; no backup service, Linux environment, schema generator or release
has been provisioned/implemented/published by this task.
