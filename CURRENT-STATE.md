# Project CBM current state

## POC3 completed — 2026-09-16 / STOP for owner review

**Private POC3 built and offline-validated; physical POC3 remains UNTESTED.**
[Completed build record](docs/build/private-poc3.md), [exact results](docs/build/private-poc3.json),
[presentation policy/findings](docs/build/poc3-design.md) and
[hash-bound Pi 3B procedure](docs/qualification/poc3-pi3b-smoke-test.md) are the current
checkpoint. The [planned physical matrix](docs/qualification/poc3-pi3b.json) has no passes yet.

POC2's Pi 3B core launch/audio/media/return/VT/reboot passes and geometry failure
remain unchanged. POC3 seeds per-chip true aspect + desktop fullscreen once, preserves
saved user preferences and adds bounded presentation/DRM diagnostics. Menu/TCPser,
first boot, tty/getty/PAM, F10/menu/Quit, privileges, service masks and media remain
unchanged. No SSH. Root cause is still unconfirmed: software reference geometry works;
actual Pi/SDL/KMS/display scaling needs the new physical evidence.

- Integration: `0a0e271d86c68a969d8b18189c561ed51a8b0e09`.
- Lock: `inputs/frozen-poc3-final/release-lock.json`, SHA-256
  `3f3180f50e5c990ad63fc3d564a56bbd86b80f9b38c6a4aff7b42ed9438b9f5e`.
- Raw: `artifacts/private-poc3/2026-09-16-project-cbm-1.1.0-poc.3-lite-private-poc.img`,
  3,095,396,352 bytes; SHA-256 `9a8b1e0465c93981dfa6b09772e9e3fbf5c487a915bba0046b5de034f9331f33`.
- XZ: `artifacts/private-poc3/image_2026-09-16-project-cbm-1.1.0-poc.3-lite-private-poc.img.xz`,
  596,947,568 bytes; SHA-256 `e7d9657bfbb1124b38c2f1f3479698e24a34be7234db80d766f189da946ace3c`.
- VICE: `3.10-1+pcbm3`, SHA-256 `c9d798a591c22faa9ffc3141b7f5177ece36a05e53d9d2c8aae1ce93c22fcfbe`.
  Menu `v1.1.0_poc2` / peeled `897cee7c792b11bfed80168a576f263340f5f57d`, TCPser
  and original MIT media are reused exactly; all identities are in the build record.

40 macOS/native Linux tests and Menu launcher tests passed. 12 software-reference
cases cover 11 profiles plus PAL/NTSC; saved preferences/CLI precedence passed.
85 read-only image checks, filesystems/systemd units and 113 ELF dependencies passed.
2,789 frozen objects and raw/XZ agreement verified. 5,503 POC1/POC2 baseline files
and the original 1,677-entry historical manifest remain unchanged. POC2 photographic
evidence references/hashes remain in its formal record, not embedded in Git.

An initial assembly was rejected for builder inventory drift from inherited automatic
APT updates. Its old lock/artifact/log remain separate, **not accepted for flashing**.
The corrected lock retains the exact host supplement; before/after inventory guards
and masked builder update units now prevent accepting that drift. These are builder-only
controls, not changed appliance service policy. See the build record for limitations.

Bulk locators above are relative to configured ProjectCBM-Work. Recovery:
`archive/milestone1-private-poc3-2026-09-16`; detailed evidence: `qualification/poc3`.
Builder is stopped. Product remains `feature/1.1-build-foundation`; Menu remains
`feature/1.1-debian-package` without changes. Nothing published. Independent backup,
clean rebuild, acceptance budgets and full settings UX remain unresolved.

**Next:** owner review, then exact-hash Pi 3B geometry + bounded regression test.
If geometry fails, collect diagnostics and stop without manual repair. No physical
test by this task, POC4, other model, SSH or broader modernization. The completed
POC2 sections below are prior checkpoints, not current authorization/status.

## Completed POC2 review

Updated 2026-09-16 — **POC2 physical Pi 3B smoke test completed; geometry defect remains.**
[Formal physical results](docs/qualification/poc2-pi3b.json) and
[aspect-ratio investigation / narrow POC3 proposal](docs/qualification/poc2-pi3b-aspect-analysis.md)
are the current qualification authority. Boot/Menu/input, diagnostic VT in both
directions, RUN/x64sc, C64 rendering and observed stability, keyboard, F10 menu,
Quit/return, PRG, original SID tones, video/input program, D64 and basic reboot
passed. **Correct aspect-ratio preservation FAILED:** horizontal widescreen stretch.
Joystick was unavailable. Other profiles/models, PSID/RSID, broader configuration
persistence, first-boot interruption, services/setup and clean-rebuild reproducibility
remain UNTESTED. No full model/release qualification follows from this bounded test.

The [completed build checkpoint](docs/build/private-poc2.md) and
[exact artifact results](docs/build/private-poc2.json) remain unchanged historical
build evidence. No POC2 image, lock, package, media or POC1 record changed. VM remains
stopped. No runtime fix, POC3, additional-model test, networking, release or push.

POC1 remains immutable: Pi 3B boot/Menu/input PASS, x64sc display/console recovery
FAIL, later VICE qualification UNTESTED. All 2,731 baseline files, including the
[physical record](docs/qualification/poc1-pi3b-2026-09-15.json), rehash unchanged.
Its physical cause remains unconfirmed. POC2 adds explicit GL runtime, standard
getty/login/PAM tty1, unprivileged shared RUN/content/F10-menu-quit behavior, bounded
persistent diagnostics, non-root tty2 and original declared media. Full settings/
privilege UX remains deferred; masked services are not failures. No broad sudo.

- Integration: `2b894ad187f0b603d2e0c9965aba242073e2cb90`.
- Lock: `inputs/frozen-poc2/release-lock.json`, SHA-256
  `bc1c6e16c32d6285973933b8d50371899bc18e5407dd654c9a14d1187eb194ac`.
- Raw image: `artifacts/private-poc2/2026-09-16-project-cbm-1.1.0-poc.2-lite-private-poc.img`, 3095396352 bytes,
  SHA-256 `ef221dc09ea65d3976f88e65cde8f153a9c32989be09c6b35d545b111ccb7467`.
- XZ image: `artifacts/private-poc2/image_2026-09-16-project-cbm-1.1.0-poc.2-lite-private-poc.img.xz`, 596406680 bytes,
  SHA-256 `757aca812835c676d75eaad651b6739fc79461c25c8aa7426524f6692a6b3d9f`.
- Menu input: `v1.1.0_poc2`, peeled `897cee7c792b11bfed80168a576f263340f5f57d`,
  package SHA-256 `e29bc3598f3be0869f79184250f88a03f4c59f1304a20a428223bac58c97bd11`.
- Original MIT media: source `14e4ade77ec83e0429d194a6b5ecfa5ef7655e75`,
  bundle SHA-256 `61673c45058ba31d2e28c699c631e99173c4e44b8b49c82c83735c2c5614d0af`.

Paths are relative to configured bulk storage, currently TheBench/ProjectCBM-Work.
34 macOS/native Linux tests, shared Bash launcher tests, 79 image checks, read-only
filesystem/unit checks and 112 ELF-object closure checks passed. All 2,738 retained
objects rehashed, XZ/raw agree, historical 1,677-entry manifest and existing tags
are unchanged. Reference software-rendered VICE checks demonstrate original-media
loading/execution and generated SID samples, not physical audio/input/graphics.
Supported no-color stdout logging avoids a reproduced VICE 3.10 logger crash; this
does not retrospectively diagnose POC1's physical failure. Exact limitations and
package/source/build identities are in the checkpoint above.

Current branches remain product feature/1.1-build-foundation and Menu
feature/1.1-debian-package. Later validation/continuity commits do not alter frozen
input identities. Final Git bundles/ref inventories and offline restore evidence:
`archive/milestone1-private-poc2-2026-09-15`; detailed evidence: `qualification/poc2`.
Independent encrypted backup remains unresolved. Existing historical/preservation/
POC1 checkpoints are untouched.

**Investigation:** the frozen image has no VICE geometry configuration/arguments;
upstream 3.10 nevertheless defaults to per-chip true aspect mode (2). Historical
v1.0 has explicit window sizes/filtering, but no explicit aspect/fullscreen setting.
Leading hypothesis: implicit windowed KMS mode selection plus downstream scaling;
actual renderer/mode/resource capture is missing. Do not claim adding mode 2 alone
fixes it. Prefer true per-chip aspect + explicit desktop-resolution fullscreen,
with bars where needed, without hard-coded 4:3 or HDMI-resolution hacks.

**Next:** owner authorization for a narrow POC3 geometry/defaults/measurement change,
new frozen candidate and offline validation, followed by owner Pi 3B geometry and
regression testing before other models. STOP pending that decision. Full settings/
privilege redesign remains deferred. Four owner-supplied photos are now retained
and visually reviewed under `qualification/poc2-pi3b-photos-2026-09-16`, with
per-file hashes/captions in the formal physical record. They corroborate visible
C64/media output and stretching; no diagnostic reports or confirmed cause. All
result classifications and frozen candidate identities remain unchanged.

This review's small evidence is under `qualification/poc2-pi3b-owner-report-2026-09-15`;
additive Git recovery/ref/offline-restore checkpoint:
`archive/poc2-pi3b-review-2026-09-15`. Earlier checkpoints retain their original
meaning. Photo-supplement source recovery: `archive/poc2-pi3b-photos-2026-09-16`.
This top section supersedes older physical-pending statements below.

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
the performance floor; 3A+ needs a separate 512 MiB memory qualification. The
historical audit did not qualify hardware. Exact POC1 failed x64sc/console recovery;
exact POC2 now passes bounded Pi 3B emulation/return/audio/media checks with an
aspect-ratio failure. This is not full model qualification; other models and
performance budgets remain unqualified. See [testing](docs/testing.md) and the new physical record.

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

## POC1 direction and next task (historical; superseded above)

Keep the console Bash/dialog -> SDL2 VICE -> ALSA appliance, with product-owned
integration and an independently versioned Menu. ADR-0001 selects writable ext4
with logical system/user-data separation, existing
content paths, external component .deb builds and backup/reflash/validated restore.
No mandated 8 GB minimum: measure footprint, initialization/maintenance margin and
free user capacity. Separate USERDATA and immutable roots are deferred.

Milestone 1 reached its first controlled-build checkpoint on
`feature/1.1-build-foundation`. The image uses integration commit
`024db4985202ef0675b12e12b8982af91c6d6ad3`; later validation/docs commits do not
change its frozen identity. Menu packaging is on `feature/1.1-debian-package` at
`77a708019c9d8a11e657d7e5d2dde7b7ecb340ba`, local annotated `v1.1.0_poc1`.
Both published main branches and existing release/recovery tags are unchanged.

Real lock: `inputs/frozen-poc1/release-lock.json` under the configured bulk root;
SHA-256 `703aa6e1b0d278262a2dc83c31740b3c589788e3953e3ac822e948133529d566`.
Private raw/XZ and records: `artifacts/private-poc1`. Raw SHA-256
`ae8d2032736e1d3ae2e49d4370aa62d00fc06f9fc567e70e400491900d45bf9f`;
XZ SHA-256 `b9adaaa55a7543441607fc90f7651cc35588f9c024e8a160110d857919ef2a06`.
26 macOS/Linux tests and 50 offline image checks passed at construction. Physical
Pi 3B boot/Menu now passed; x64sc display and console recovery failed. First-boot
expansion/identity measurements and later VICE qualification remain UNTESTED.
This is a controlled build, not reproducibility proven.

Read-only analysis found missing desktop GL runtime (v1 used the OpenGL renderer),
a direct tty service without the previous PAM/login session, and differing kernel/
Mesa stacks. SDL has a GLES fallback, so no root cause is confirmed without runtime
logs. POC1 raspi-config calls also lack an authorization path; this is a separate
setup UX gap, not a failure of intentionally masked services. The required 1.1
setup UX is offline-capable with narrowly authorized operations, not broad sudo.

Next: owner review of the bounded POC2 proposal and authorization before fixes,
engineering diagnostics, media creation or rebuilding. Do not modify frozen POC1,
restart the builder, modernize broadly or publish anything. Product remains on
feature/1.1-build-foundation; Menu working branch is feature/1.1-debian-package at
99063f8299192877f7d17d0ccd9635f135b89fdc (the frozen POC1 input stays the earlier
77a7080 commit above). This analysis changes product documentation/records only.
Both retained raw-image hashes were reverified; inspected package/launcher payloads
match the frozen image. Documentation JSON/local links/diff and immutable-tag
checks are recorded in the analysis checkpoint; no physical rerun was performed.
Private detailed comparison and additive source checkpoint are retained under
qualification/poc1-pi3b-2026-09-15 within the configured external workspace.
Earlier build/recovery checkpoints remain unchanged; no image is duplicated.

### Black-box recovery requirement

Read [recovery](docs/recovery.md) for scenarios A–H, historical confidence levels,
portable storage, independent backup/restore and acceptance tests. A future developer
must recover the product from CBM repositories/retained artifacts alone, without old
sessions, the original Mac or reference projects.

Full project recovery belongs in repositories and retained build/release infrastructure.
1.1 carries only minimal `/usr/share/project-cbm/identity.json`, generated from the
same frozen lock: product/Menu/VICE/base/TCPser mapping, integration/build ID and config
schema identity, with external provenance lookup. The generator is implemented; its 1,443-byte output is installed and verified
offline in the private POC. No full lock, recipes, schema corpus,
archives or package closure merely for recovery in the appliance. Proposed pcbm-info
reads E; it is not implemented. Final image hashes/qualification stay external to
avoid cycles. A final manifest hashing the image cannot have its digest embedded in
that image; use a predecessor digest/build-ID lookup. JSON worksheet is design-only.

The accepted preservation bundles were restored into fresh mirrors without GitHub:
all 5 product refs, 8 Menu refs and 17 recovered script hashes matched; fsck passed.
Owner accepted repository-only cold-start comprehension on 2026-09-15. Offline 1.1 identity now passes on the private image. An independent clean Linux
rebuild and independent-medium restore remain unperformed. Host-only schema/privacy negatives pass using synthetic fixtures. Read-only lessons from Spitfire/FireComm/CircuitNET are summarized in recovery.md; CBM does not depend
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
space/mount before work. The approved guest supplies ext4 in its external sparse disk. One device is not an
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

## Milestone 1 approved host checkpoint (historical, before package work)

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

## Private component packages and retention work (historical, before input freeze)

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

## Frozen factory implementation checkpoint (historical, before first image)

26 contract/retention/geometry tests pass on macOS and native Debian, with no skips.
The initial Linux test copy omitted a worksheet and Git refs; the complete copy now
passes. This was a test setup error, not a required Linux capability failure.
Exact old host binaries (17) and sources (10) were recovered via Debian snapshots.
All remaining runtime source acquisition completed, with explicit libftdi1 source-name
reconciliation. Unneeded rpi-connect-lite is excluded before construction because its
source entry was unavailable; original failed discovery records remain unchanged.

The minimal factory is in tools/{freeze_poc_inputs,retained_inputs,construct_poc,
install_poc_stage}.py and [integration notes](build/pigen/README.md). A frozen kit
contains content-addressed direct inputs and nested source/package/metadata catalogs.
Source .dsc SHA-256 payload lists and actual .deb identities are checked. Final assembly
runs with loopback-only networking and frozen APT transport; absent inputs fail closed.
Two explicit pi-gen patches exclude Connect and prevent export-time user rename/
package upgrades. They do not rewrite upstream history or bypass APT authentication.

Private POC policy: local pi console Menu, locked passwords, no broad sudo, no baked
credentials; SSH/Samba/TCPser/Avahi/NetworkManager disabled. Binaries are installed,
but network configuration and privileged Menu controls remain incomplete. No cover
art/private historical content is imported. First boot owns root growth and seeds
user state; pure geometry tests pass, actual first boot remains physically untested.
Next: commit this input recipe, archive that commit, freeze/verify/export the real kit,
construct one private image, validate offline, retain results and STOP for owner review.

## Final POC1 recovery checkpoint (historical)

`ProjectCBM-Work/archive/milestone1-private-poc1-2026-09-15` is the additive current
checkpoint: README, checkpoint.json plus SHA-256, both full Git bundles/ref lists,
offline mirror restoration/fsck results and validation/remote-ref records. Its exact
final branch tips are recorded externally to avoid a self-referential commit hash.
The frozen kit has 2,697 rehashed objects; images and component artifacts remain in
their existing external locations, without duplicating historical images.

Original historical manifest verifies all 1,677 entries unchanged. Both formal v1.0.0
tags, Menu recovery refs and published main refs are unchanged. Product maintenance/1.0
remains local/bundled. Independent encrypted custody remains unresolved; a second
folder on TheBench is not an independent backup. Current VM is stopped, not deleted.
