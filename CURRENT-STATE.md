# Project CBM current state

Updated 2026-09-15 — preservation/reconciliation/continuity accepted; first-class
black-box recovery design added as a required part of the 1.1 builder architecture.
No 1.1 builder, runtime changes, image build or release publication performed.

## What shipped

| Item | Verified baseline |
| --- | --- |
| Product | Project CBM v1.0.0, original Trixie console appliance |
| OS/base | Raspberry Pi OS Lite 64-bit, Debian 13.4 Trixie; 2026-04-21 reference, pi-gen `4ad56cc850fa60adcc7f07dc15879bc95cc1d281`, stage2 |
| Kernels | arm64 vendor 6.12.75 v8 and 2712; no device EEPROM qualification implied |
| VICE | Source-built 3.10 SDL2 under /usr/local, direct ALSA; retained build output matches installed x64sc |
| TCPser | 1.1.6_beta, retained checkout `fe7feff4862406b277e009d14c219f5d16cf1222`; full integration unqualified |
| Menu shipped | Exact 17 scripts recovered at `1cd5e0d378a4066f239c92a30aafdd97cb415dcf`, annotated `recovered/image-v1.0.0-runtime` in companion repo |
| Formal Menu | Existing v1.0.0 peels to `399c6158caa8ed2762744d512c1841b94ad64403`; 12 script matches, five differences, extra experimental screenshot helper |
| Source lineage | Historical v6.1/v6.3/v6.4 -> v6.5/GoldMaster/for65. v6.5 source equivalence is not byte identity or a full installed configuration snapshot |

[Provenance and hashes](docs/provenance.md) distinguish fact, inference and unknown.
No known Bookworm generation exists. No pre-existing Menu commit matches all
shipped bytes; the new root recovery commit records recovery, not invented ancestry.

## Development and maintenance

- Canonical main fast-forwarded 26 commits each: product `46fbf47` -> `493229c`;
  Menu `f185d91` -> `b7e4d85`, followed by local continuity commits. Full IDs and
  preservation records: [provenance](docs/provenance.md).
- Continuity commits and new recovery/maintenance refs are local, also preserved
  in TheBench bundles; no push was performed. GitHub release assets are unchanged.
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
No fixes were applied in this phase.

## Direction and next task

Keep the console Bash/dialog -> SDL2 VICE -> ALSA appliance, with product-owned
integration and an independently versioned Menu. The next milestone is a pinned
pi-gen arm64 Lite + small CBM stage + packaged VICE 3.10 + pinned Menu candidate +
pinned TCPser proof-of-concept. Read the exact [new-session handoff](docs/build-and-release.md#new-session-first-task).
No full release-lock mechanism or Linux build environment has been implemented.

### Black-box recovery requirement

Read [recovery](docs/recovery.md) for scenarios A–H, historical confidence levels,
portable storage, independent backup/restore and acceptance tests. A future developer
must recover the product from CBM repositories/retained artifacts alone, without old
sessions, the original Mac or reference projects.

1.1 must generate offline-readable /usr/share/project-cbm/recovery/ identity,
lock, inventory, schema and compact recipe data from the same frozen inputs.
Proposed pcbm-info reads that authority; it is not implemented. Final image hashes
and post-image qualification attestations remain external to avoid hash cycles.
Only-image identification cannot replace missing external input bytes or prove
qualification. JSON field contracts and a design-only worksheet are documented;
production schemas/validators/generator remain an initial POC task.

The accepted preservation bundles were restored into fresh mirrors without GitHub:
all 5 product refs, 8 Menu refs and 17 recovered script hashes matched; fsck passed.
Fresh-person comprehension, offline 1.1 image, clean Linux rebuild, schema/privacy
negative tests and independent-medium restore remain unperformed. Read-only lessons
from Spitfire/FireComm/CircuitNET are summarized in recovery.md; CBM does not depend
on them. Spitfire's migrated reference copy has missing tools.

Current local paths are deployment choices, not architecture. Independent encrypted
backup/custody, Linux bootstrap environment, signing custody and standard SBOM format
remain open. No infrastructure was provisioned. This additive design checkpoint is
separate from the sealed accepted preservation archive.

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
