# Project CBM current state

Updated 2026-09-15 — owner approved the Lima/VZ build host. The native ARM64
Debian 13 guest is provisioned on TheBench and its Linux capability gate **passed**.
[Approved recipe and reconstruction](docs/build/lima-build-host.md) and
[capability evidence](docs/build/lima-capability-2026-09-15.md) are current authority.
[ADR-0001](docs/adr/0001-base-distribution-and-image-architecture.md) remains accepted.
Three private component packages now build; no Project CBM image or physical Pi pass exists yet.

## What shipped

| Item | Verified baseline |
| --- | --- |
| Product | Project CBM v1.0.0, original Trixie console appliance |
| OS/base | Raspberry Pi OS Lite 64-bit, Debian 13.4 Trixie; 2026-04-21 reference, pi-gen `4ad56cc850fa60adcc7f07dc15879bc95cc1d281`, stage2 |
| Kernels | arm64 vendor 6.12.75 v8 and 2712; no device EEPROM qualification implied |
| VICE | Source-built 3.10 SDL2 under /usr/local, direct ALSA; retained build output matches installed x64sc |
| TCPser | 1.1.6_beta, retained checkout `fe7feff4862406b277e009d14c219f5d16cf1222`; full integration unqualified |
| Menu shipped | Exact 17 scripts recovered at `a4148db54001790eaddb4e31104917c16149b181`, annotated `recovered/image-v1.0.0-runtime` in companion repo |
| Formal Menu | Existing v1.0.0 peels to `399c6158caa8ed2762744d512c1841b94ad64403`; 12 script matches, five differences, extra experimental screenshot helper |
| Source lineage | Historical v6.1/v6.3/v6.4 -> v6.5/GoldMaster/for65. v6.5 source equivalence is not byte identity or a full installed configuration snapshot |

[Provenance and hashes](docs/provenance.md) distinguish fact, inference and unknown.
No known Bookworm generation exists. No pre-existing Menu commit matches all
shipped bytes; the new root recovery commit records recovery, not invented ancestry.

## Development and maintenance

- Canonical main fast-forwarded 26 commits each: product `46fbf47` -> `493229c`;
  Menu `f185d91` -> `b7e4d85`, followed by local continuity commits. Full IDs and
  preservation records: [provenance](docs/provenance.md).
- The eight unpublished preservation/continuity commits received an owner-authorized
  metadata-only privacy repair. Current refs and verified replacement bundles are in
  [privacy reconciliation](docs/privacy-reconciliation-2026-09-15.md). Both main branches and Menu recovery/maintenance refs are published. Product
  maintenance/1.0 remains intentionally local/bundled; public product v1.0.0 is the
  authoritative maintenance baseline. GH007 rejected new branch creation because
  of historical commit email metadata; do not retry, rewrite v1.0.0 or weaken privacy.
  GitHub release assets are unchanged.
- Product maintenance/1.0 starts at immutable product v1.0.0 `46fbf47d66596b2f3d0f6ab53d26bdd90632c73c`.
  Menu maintenance/1.0 starts at the exact recovery commit above, not formal Menu
  v1.0.0. It contains scripts and provenance only, not an installable image recipe.
- 1.0.x = original Trixie generation, important/security fixes only. 1.1.x = current
  Trixie reproducible-build/modernization generation. No 1.0.1 exists or is approved.
- Work from short feature branches off main when 1.1 is authorized. Repository
  separation, immutable releases, explicit input pins and Pi 3 floor are protected.

## Qualification and known problems

Goal: Pi 3B/3A+/3B+, 4B/400, 5/500/500+ where technically supportable. Pi 3 is
the performance floor; 3A+ needs a separate 512 MiB memory qualification. All
hardware cells remain unqualified by this audit: no physical Pi tests or measured
performance budgets exist. See [testing](docs/testing.md) and its retained matrix.

Verified static/integrity checks cover image hashes, runtime extraction/lineage,
Git preservation and individual Bash syntax. They do not qualify boot, graphics,
audio, controllers, IP232, USB/NVMe or cloned identity behavior.

Known issues are cataloged in [security](docs/security.md): baked identity/SSH keys,
cloud-init and builder residue; broad sudo; TCPser default mismatch; inconsistent
Samba service policy; USB import safety; non-idempotent installer; writing docs-sync
dry run/deletion risk; version-display and CI/version mismatch; source/release
divergence; PiShrink/manual build limitations; content/license provenance gaps.
Current guidance is corrected in [v1.0 notes](docs/v1.0-current-notes.md); no runtime
fixes were applied. Historical audit/release notes/assets/checksum bytes are preserved.

## Direction and next task

Keep the console Bash/dialog -> SDL2 VICE -> ALSA appliance, with product-owned
integration and an independently versioned Menu. ADR-0001 selects writable ext4
with logical system/user-data separation, existing
content paths, external component .deb builds and backup/reflash/validated restore.
No mandated 8 GB minimum: measure footprint, initialization/maintenance margin and
free user capacity. Separate USERDATA and immutable roots are deferred.

Milestone 1 is active on `feature/1.1-build-foundation`, created from verified main
`29933789ec8d29bd55f2b00cbcf309132058413f`; Menu remains clean main at
`bb4f24fadae6e852bf29fb0e32ad8ced9db7268c`. Host-only schemas/generator/validators
and 20 tests are implemented; retention, packaging, integration and first-boot
designs are documented. Owner approved Lima/VZ with 8 vCPU, **10 GiB RAM**, 160 GiB
sparse disk. Core and full Linux/transfer/package capability tests passed. Continue
Milestone 1 with exact pi-gen/component inputs, retained closure, versioned packages,
real lock, minimal integration/first-boot and one private POC image/offline validation.
Stop on a required capability failure or after that image; no automatic physical Pi
testing, broad modernization or release publication. See the
[approved host](docs/build/lima-build-host.md) and [build sequence](docs/build-and-release.md#new-session-first-task).
No real release lock, retained candidate input closure, package recipe/stage exists. The Linux host is now available; its complete
build dependency closure is not yet frozen. Synthetic fixtures cannot be used as build inputs.

### Black-box recovery requirement

Read [recovery](docs/recovery.md) for scenarios A–H, historical confidence levels,
portable storage, independent backup/restore and acceptance tests. A future developer
must recover the product from CBM repositories/retained artifacts alone, without old
sessions, the original Mac or reference projects.

Full project recovery belongs in repositories and retained build/release infrastructure.
1.1 carries only minimal `/usr/share/project-cbm/identity.json`, generated from the
same frozen lock: product/Menu/VICE/base/TCPser mapping, integration/build ID and config
schema identity, with external provenance lookup. The host-only generator is implemented;
it has not been installed in any image. No full lock, recipes, schema corpus,
archives or package closure merely for recovery in the appliance. Proposed pcbm-info
reads E; it is not implemented. Final image hashes/qualification stay external to
avoid cycles. A final manifest hashing the image cannot have its digest embedded in
that image; use a predecessor digest/build-ID lookup. JSON worksheet is design-only.

The accepted preservation bundles were restored into fresh mirrors without GitHub:
all 5 product refs, 8 Menu refs and 17 recovered script hashes matched; fsck passed.
Owner accepted repository-only cold-start comprehension on 2026-09-15. Offline 1.1
identity on an actual image, clean Linux rebuild and independent-medium restore
remain unperformed. Host-only schema/privacy negatives pass using synthetic fixtures. Read-only lessons from Spitfire/FireComm/CircuitNET are summarized in recovery.md; CBM does not depend
on them. Spitfire's migrated reference copy has missing tools.

Current local paths are deployment choices, not architecture. Independent encrypted
backup/custody, Linux bootstrap environment, signing custody and standard SBOM format
remain open. At that earlier checkpoint no infrastructure was provisioned. The earlier design checkpoint remains
separate from the sealed preservation archive. The additive privacy-reconciliation
checkpoint now retains all eight replacement commits, including the architecture
work, with full offline restore checks. See its record for subsequent checkpoint phases.

## Evidence and storage

- Original history (read-only by policy): `/Volumes/TheBench/Projects/Project CBM`.
- New bulk work: `/Volumes/TheBench/ProjectCBM-Work/{inputs,packages,builds,cache,artifacts,qualification,scratch}`.
- Durable inventory/Git snapshots/recovery: `ProjectCBM-Work/archive/preservation-2026-09-15`.
- Additive design checkpoint/bundles: `ProjectCBM-Work/archive/black-box-design-2026-09-15`.
- Original assets/extraction: `ProjectCBM-Work/archive/audit-2026-09-14/workspace`.
- [Reconciled audit](docs/audit-2026-09-15.md); original report retained externally.

TheBench is ~2 TB APFS with ~1.13 TB available at preservation time. Check actual
space/mount before work. No Linux build filesystem exists. One device is not an
independent backup; owner review of a second encrypted backup destination remains.
Unknowns: original base-XZ identity/full input lock, complete raw-to-shrunk command
chain, VICE upstream tar provenance/patch state, content licenses and all physical
qualification. Public availability/credential remediation and any new release need
separate owner review. These do not prevent starting an explicitly authorized POC.

## Final architecture phase checkpoint (historical, pre-rewrite IDs)

Inputs: product main `7f9c4a363cf19154a9637ed8b251049bf23723e0`; Menu main
`c3746a12e6146f880c49979df8da2a3567200924`. Both began clean. Exact historical release,
Menu recovery refs and rehashed bundle locators are in [provenance](docs/provenance.md#recovery-bundle-locators-and-digests).
Research dated 2026-09-15 is cited in ADR-0001; it is not a future release input lock.
Current policy now distinguishes project recovery, minimal installed identity,
reproducible builds and disaster recovery. Roadmap and user-facing content/service/
credential/hardware guidance are reconciled; historical evidence is not rewritten.

Validation and exact commit lookup are recorded in [phase validation](docs/architecture-phase-validation.md).
No builder, Linux provisioning, packaging, runtime/first-boot change, image, push or
release. Stop after documentation commits. Independent backup/custody, Linux bootstrap,
signing custody, SBOM format, measured acceptance budgets and historical 1.0 input/
build-chain gaps remain open. Implementation is the next separately authorized task.

## Milestone 1 pre-approval checkpoint (historical)

Contract implementation commit: `e4d1556` (resolve full ID in Git); later design/handoff
commit follows on the same local feature branch. Feature work is not pushed or merged.
The 15 host-only tests passed, including published tag identities, strict JSON/schema
validation, malformed/missing pins, safe locators, minimal-identity projection and
workspace refusal cases. No physical Pi, Linux capability or real input-closure pass
is claimed. The old worksheet remains visibly historical and fails lock validation.

Current source recovery is additive under archive/milestone1-contracts-2026-09-15;
its checkpoint.json and separate SHA-256 identify the final branch tip, bundles,
validation/research/test-dependency artifacts and exact next step. Read its README
after verifying the catalog. Published synchronization bundles remain under
archive/privacy-reconciliation-2026-09-15/published, checkpoint SHA-256
`6ff18bafcc57a7e054a22fff66efedd3618ea6bd1a6f9dedf2c6d1bacdbc255c`.

Recommendation awaiting approval: Lima/VZ plain arm64 Debian VM, 8 vCPUs, 12 GiB RAM,
160 GiB sparse ext4 disk on TheBench, explicit external download/cache placement.
UTM is the main alternative. Approval must precede host installation/provisioning;
exact bootstrap/input pins and actual Linux capability tests remain future work.

## Milestone 1 approved host checkpoint (current)

Lima 2.2.0, source `de0816ea4bdc5267b428ab21025889b8dd785526`; pinned dated
Debian cloud bootstrap and checksums in build/host/inputs.json. Instance `cbm` is
running on VZ, plain mode, no host mounts/container platform. Disk and state:
`ProjectCBM-Work/build-host/lima/cbm/disk`; cache: `ProjectCBM-Work/cache/lima`.
Actual root is ext4; Debian 13 kernel `6.12.95+deb13-cloud-arm64`. The guest is
infrastructure, not Raspberry Pi qualification or a release base image.

20 host tests passed. Full loop/partition/ext4/mount/chroot/device/xattr tests,
APT HTTPS/authenticated metadata/install/remove/source, Git acquisition and 1 MiB
bidirectional SSH/rsync hash test passed. Two probe defects (admin PATH and xattr
read permissions) were corrected; original failed logs retained. APT export excludes
transient lock/partial files after initial permission errors; important inputs were
catalogued. No host capability workaround was needed. All details and limitations:
[capability record](docs/build/lima-capability-2026-09-15.md).

Retained bootstrap inputs: `ProjectCBM-Work/inputs/build-host/`; 82-file inventory
and raw private infrastructure logs: `ProjectCBM-Work/build-host/records/`.
Next: retain and select exact pi-gen arm64/VICE/Menu/TCPser inputs and package-build
closure, then implement the smallest locked POC factory. Do not claim a frozen real
release lock, complete source/package closure, image, reproducibility or hardware pass.

## Private component packages and retention work (in progress)

Successful private Debian candidates retained under `ProjectCBM-Work/packages/poc1/`:

- VICE `3.10-1+pcbm1`, arm64; SHA-256
  `674c40040965b689d08cdc225f8954c0fb2433ef68459f51aa7f6360b1710d20`.
- Menu `1.1.0~poc1-1+pcbm1`, all; SHA-256
  `3f7557cdbdd44922954a6e640a1bcb3a96f446f6dbe6631afe667aa5e5d5f0fd`.
  Companion feature/1.1-debian-package at `77a708019c9d8a11e657d7e5d2dde7b7ecb340ba`;
  local-only annotated v1.1.0_poc1 object `e265f3cbb995ad0a9a7748987b2d9c88019aa787`.
  Formal and forensic tags/main are unchanged. Menu packaging relocates required
  command paths to /usr/bin and excludes release-prep, screenshot and unreviewed art.
- TCPser `1.1.6~beta-1+pcbm1`, arm64; SHA-256
  `8b8f8a4f3ec98dddf5bdb347320dad05e1bbe5230e0ee2727248c247a5af584f`.

Exact source selection is in build/inputs-poc.json (NOT a frozen release lock).
pi-gen arm64 `6fcca44892d5d4b36f826d2b8fb16d716369fada` and TCPser
`fe7feff4862406b277e009d14c219f5d16cf1222` sources/bundles are externally retained.
VICE needs dos2unix, xa65, SDL2-image and evdev development dependencies; those
configure findings are now in the recipe. Out-of-tree compilation avoids source
contamination; native CPU optimization is explicitly disabled. Build logs and .dsc,
source archives, .buildinfo, .changes and debug .debs are retained outside Git.

Pinned pi-gen stages 0/1/2 completed in an input-resolution-only run with all image
exports disabled. No final appliance has been constructed. Resolved base is Trixie
13.7 with raspberrypi-sys-mods 1:20260914 and vendor kernel metapackages
1:6.18.50-1+rpt1. Actual vendor early resize hooks require the `resize` kernel argument;
first-boot draft removes that argument and coordinates one explicit growth owner.
Full source/host package retention and a frozen replay-capable input kit remain in
progress. Seventeen old bootstrap .deb versions were absent from today's indexes;
exact-version Debian snapshot recovery is underway, without upgrades/substitution.
Inspect newer dirty scripts/state and build-host/records before resuming. Next:
complete/verify retention, freeze real lock, review/test integration and first boot,
then one private image and offline validation. No publication or physical Pi test.
