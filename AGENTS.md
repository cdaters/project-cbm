# Project CBM Development Rules

Project CBM is a Raspberry Pi Commodore appliance. Preserve its personality, user
control, reliable console-to-emulator lifecycle and long-term recoverability.
Prefer clear, maintainable engineering with measurable benefit on the Pi 4 performance floor.

## Authority and continuity

This file is the standing repository governance. It replaces all former
milestone-specific authorization, one-candidate limits and STOP/owner-review
clauses in earlier AGENTS revisions. Those clauses, including dated copies in
CURRENT-STATE and build/recovery/qualification records, describe historical scope;
they do not restrict the private engineering authority below. Their technical
requirements, evidence and permanent protections remain applicable.

Read [CURRENT-STATE.md](CURRENT-STATE.md) for the latest checkpoint and exact next
action, then the relevant canonical documents linked here. Inspect actual refs and
dirty work before resuming; preserve unknown work even when newer than the record.
Current user instructions define the task and may narrow it (for example, review
only or leave uncommitted). Standing authority is not an instruction to expand a
task into unrelated backlog work. Tool/sandbox permissions still apply.

Keep changing status, candidate identities, results, blockers and next actions in
CURRENT-STATE and canonical build/qualification/recovery records, not AGENTS.md.
Change this file only when durable governance changes. Old sessions and reference
projects are not required continuity or build/recovery dependencies.

## Standing private engineering authority

Within the requested outcome and these protections, Codex may autonomously
investigate, implement fixes, run tests, make logical local commits, version and
package changed components, freeze distinct private engineering candidates, build
with the approved Lima/VZ + pinned pi-gen factory, validate, checkpoint and iterate.
Successive private candidates do not require fresh owner authorization or an
AGENTS edit. Routine reversible implementation and packaging choices are delegated.

On an integrity failure, halt the affected build or validation, retain the failed
attempt and diagnose it. Do not bypass a failing gate or label the candidate ready.
An evidence-supported correction and a distinct retry are authorized once required
gates pass. Escalate if recovery requires a hard-gated action below, or if missing
owner input prevents safe progress; a historical STOP is not such a blocker.

## Hard owner gates

Require explicit owner approval before:

- pushing any branch/tag or publishing releases, images, packages or public docs;
- deleting, overwriting or destructively changing historical evidence, frozen
  inputs/outputs, recovery records or unexported builder state;
- weakening security, credential privacy, privilege boundaries or exposure policy;
- replacing the agreed architecture, build platform or major component boundaries;
- resolving an unapproved third-party redistribution decision or broadening a
  private-use admission into public redistribution;
- rewriting published history or moving/replacing an existing protected tag/asset;
- physical device testing/flashing or advancing physical qualification/support
  claims beyond exact, retained owner-reported results.

Approval never substitutes for test evidence or a rights grant. Recording a supplied
owner test report additively needs no second approval. Private iteration, local
commits and new private version tags are not push or publication permission.

## Product and repository boundaries

- This repository owns OS/runtime integration, accounts/services, image construction,
  release locks and identity, VICE/TCPser/Menu mapping, hardware policy, qualification,
  artifacts, recovery, release notes and authoritative product documentation.
- [project-cbm-menu](../project-cbm-menu/AGENTS.md) owns independently versioned Menu
  scripts/assets, presentation/interfaces, packaging and focused tests. Its
  public-docs mirror is historical, not a competing product authority.
- Preserve Raspberry Pi OS Lite arm64/Trixie, pinned arm64 pi-gen, writable ext4
  and logical user-data separation under [ADR-0001](docs/adr/0001-base-distribution-and-image-architecture.md).
  Read its evidence-based review triggers before foundation changes.
- Keep Bash/dialog, console getty/login/PAM/session ownership, SDL2 VICE and ALSA.
  VICE owns emulation, per-chip geometry and user emulator preferences; retain F10,
  complete aspect-preserving canvas and reliable return. Retain x64sc as the normal C64 core; qualify its performance on the Pi 4 floor.
- Project CBM 1.1 targets Pi 4-class hardware and newer (Pi 4 B/400, Pi 5/500/500+
  where supportable); qualify each model separately. Pi 3/Zero-class hardware is
  outside the 1.1 release target. Preserve historical results; do not resume Pi 3
  optimization. OS support does not establish CBM qualification.
- The read-only product `pcbm-info` JSON is the system-information authority.
  Menu/configuration UI consumes it without duplicate probes or human-output parsing.
  Product registry and validated user preferences own machine/profile selection.
  Keep one shared unprivileged VICE launch path and one first-boot/expansion owner.
- Preserve user-owned ordinary preferences, atomic validated writes and explicit
  recovery of invalid state. Valid new state wins; missing state may import legacy
  once. Saved intent is not effective runtime state. See
  [architecture](docs/architecture.md) and [configuration](docs/runtime/configuration-contract.md).
- Preserve COVERS terminology, the seven existing artwork files/names/provenance,
  registry mapping and shared transition ownership. Capture terminal state before
  Cover; supervise, bound and reap it; restore/verify before and after VICE. Missing
  or failed Cover must allow VICE to proceed without weakening terminal safety.
  No root/framebuffer/resolution workaround. See [Covers](docs/runtime/covers.md).
- Streamline UI when benefits are concrete: predictable Back/Cancel/retry/resume,
  truthful working/error feedback and equal or better measured Pi 4 responsiveness.
  Historical menu layout is not immutable; major architecture changes remain gated.

## Versioning, immutable candidates and the factory

Follow [build and release](docs/build-and-release.md), [host recipe](docs/build/lima-build-host.md)
and [host/target environment boundary](docs/build/environment-boundary.md).

- Product and Menu have independent versions. 1.0.x is important/security maintenance
  of the original arm64 Trixie line; 1.1.x is the reproducible-build generation.
  Never invent a Bookworm lineage or relabel forensic recovery as a release.
- Pin the Menu version/tag, annotated tag object where applicable, peeled full commit
  and package SHA-256. Never consume arbitrary main or an unverified tag alone.
- Every changed frozen input set needs a distinct lock/build/attempt identity and
  output directory. Version/rebuild affected components; reuse unchanged components
  only with exact identity and compatibility checks. Never add bytes to a finished
  image or replace a frozen package, tag, lock or failed attempt.
- Freeze clean committed source, integration, recipes/patches, schemas, rights/assets,
  exact authenticated binary/source package closure and toolchain/bootstrap inputs.
  Retain actual bytes; URLs, caches and synthetic fixtures are not real input pins.
  Missing inputs, dirty source or hash/version/schema mismatch fail the freeze.
- Use the approved native arm64 Debian Lima/VZ plain-mode guest and external-backed
  ext4 storage. Repository recipes are authority; the VM is disposable infrastructure.
  No container stack, host shares or architecture workaround to evade capability gates.
- Verify workspace/capability gates and host inventory/update guards before and after
  construction, including failures. Separate acquisition from frozen assembly.
  Intentional host updates require retained inputs, revalidation and a new lock.
  Keep builder settings out of the appliance; preserve sanitized target environments,
  AppArmor, package authentication and verification. Never leak builder TMPDIR/state.
- Validate actual installed image contents, package/ELF closure, filesystems/systemd,
  identity and diagnostics; verify raw/XZ equivalence, sizes and exact hashes.
  Measure footprint, maintenance/first-boot margin and free user capacity; do not
  impose an unsupported nominal 8 GB minimum.
- A successful build is not proven reproducibility. Compare independent clean builds
  from identical declared inputs and explain differences before making that claim.

## Storage, security, preservation and rights

- Canonical source/docs stay in configured Git roots (currently ~/Code). Large inputs,
  packages, images, trees, caches, temporary build state and qualification evidence
  stay on mounted /Volumes/TheBench/ProjectCBM-Work. Verify mount identity and capacity;
  never silently fall back to the internal SSD. Use configured roots and portable
  relative locators so replacement machines need neither original absolute path.
- /Volumes/TheBench/Projects/Project CBM is original evidence: no edits, renames,
  normalization, deduplication, cleanup or execution in place. Preservation manifests
  and bundles are in ProjectCBM-Work/archive/preservation-2026-09-15. Verify manifests
  after preservation work; never regenerate a baseline to conceal a mismatch.
- Exclude `.DS_Store` Finder metadata from Git, active source/build staging and
  release artifacts. Remove it from active areas when safe. Preserve sealed
  historical files/manifests; record a Finder-only mismatch as an owner-authorized
  non-release-affecting exception after verifying it is outside the frozen release
  dependency graph and cannot affect the image or qualified-basis equivalence.
- TheBench is unencrypted APFS with ownership disabled; permissions are not encryption,
  and APFS is not a Linux rootfs. Separate private history from derived public inputs.
  Record sensitive-file presence/type, never contents, in reports or Git. Exclude
  credentials, password hashes, private keys, history and private device/network data
  from public records; keep allowlisted engineering diagnostics private.
- Follow [security](docs/security.md). Normal operations use fixed, validated,
  readiness-gated privileged helpers; preserve authenticated owner administration.
  No universal credentials, unrestricted passwordless root or broad sudo/file commands.
  Protect secret transport/storage and keep secrets out of argv, logs and metadata.
  Preserve deliberate service/listener opt-in and first-boot identity/account gates.
- Do not execute legacy installers, docs-sync (even --dry-run), release-prep,
  privileged image tooling or historical/runtime scripts as a documentation/static check.
- Follow [provenance](docs/provenance.md) and the
  [optional-input contract](docs/runtime/optional-applications-contract.md). Preserve
  corresponding source, licenses and exact payload/recipe/rights hashes. Freeware,
  downloads, archive inclusion or possession do not establish redistribution rights.
  Existing private admissions remain private unless explicitly superseded by the owner;
  apply the recorded [1.1 release policy](docs/release/release-policy.md) for artwork,
  CCGMS composition, upstream VICE ROMs and deferred release engineering;
  original qualification media stays distinct from third-party references. No automatic
  content downloader/scraper or blanket MIT relicensing of third-party content.

## Recovery, qualification and session close

- [Recovery](docs/recovery.md) is a product/infrastructure responsibility. Retain full
  source/input/build/product/qualification records externally. One frozen lock drives
  construction and minimal offline-readable installed identity; keep image hashes
  and later attestations external with an acyclic checksum graph. No full lock,
  recipes, archives or package closure in the appliance merely for recovery.
- Create additive recovery checkpoints with exact refs, bundles, manifests and verified
  offline restore/ref/peeled-tag/fsck checks. GitHub and caches are not permanent
  storage. Independent copies and restore drills remain required; another folder on
  TheBench is not independent custody. Report incomplete recovery honestly.
- Follow [testing](docs/testing.md): focused behavioral/native checks for relevant
  changes, per-file Bash syntax checks, JSON/link validation, diff whitespace, changed
  file sizes and secret-pattern review. Do not execute runtime tools as static tests.
  Report known contextual failures separately; neither hide them nor invent passes.
- Bind physical procedures and results to exact image hashes, hardware and tested
  behavior. Use PASS/FAIL/UNTESTED/BLOCKED accurately. Static, VM/headless or offline
  checks cannot prove visible Cover, Pi input/VT/audio/network behavior or another
  model's support. Preserve failures and uncertainty; stop a failing physical test
  for evidence collection rather than repairing the qualification artifact in place.
- Before commits, check effective author/committer identity and local overrides;
  use the contributor's GitHub noreply identity when email privacy is enabled. Never
  disable privacy, hard-code an operator email or treat GH007 as rewrite permission.
- After meaningful work, update CURRENT-STATE with the checkpoint, checks/limits,
  canonical evidence/recovery references and exact next action. Update relevant
  build/qualification/decision docs additively; keep historical statements intact.
  Leave clear Git status and logical local commits unless the user requests review
  without committing. Explain confirmed, inferred and unresolved facts in plain
  English; prefer canonical links and usable how-to guides over duplicated history.
