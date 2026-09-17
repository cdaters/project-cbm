# POC4 attempt #3: construction and offline validation

**Build PASS. READY FOR OWNER PHYSICAL TEST. READY TO FLASH: YES.**
Project CBM **1.1.0-poc.4 / private-engineering-poc4, attempt 3** is constructed from
the previously frozen inputs. No physical Raspberry Pi test was performed. Stop for
owner review; no next candidate, boot optimization, push or publication is authorized.

[Exact results](private-poc4-attempt3.json),
[hash-bound Pi 3B procedure](../qualification/poc4-attempt3-pi3b-smoke-test.md),
[accepted prebuild record](poc4-attempt3-owner-review.md),
[builder/chroot boundary](environment-boundary.md).
All bulk locators below are relative to configured storage, currently
`/Volumes/TheBench/ProjectCBM-Work`.

## Frozen identity and preconstruction

Lock: `inputs/frozen-poc4-attempt3/release-lock.json`.
SHA-256: `435c6e0d7a5a45eaff3f45af6d384fca5b602139fa9fb640950e2f5e7b4f39a9`.
Integration: `b362c70215cef0e2c6c6a845635c47fd39b3ebbf`.
Menu: `v1.1.0_poc4.1`, peeled `407ced58b711209631cdfb4db6dcd741a555f408`;
package `1.1.0~poc4.1-1+pcbm1`, SHA-256
`6df8fb42a10b16e12ac114032accc149c49ebf51f0e5f45c34b77d2cefbb2767`.
Pinned pi-gen: `6fcca44892d5d4b36f826d2b8fb16d716369fada`.
No lock, package, Cover artwork, target input or rights classification changed.

Both repositories began clean at Product `c7afb01` and the Menu ref recorded in
`preconstruction.json`. Current AGENTS scopes agree. All 2,832 kit objects, schema,
transitive catalogs, native Debian metadata, runtime API and optional/qualification
media verified. Guest recipe bytes match the frozen integration archive. Protected
refs, POC1/2's 5,503 baseline entries, POC3 lock/raw/XZ/2,789 objects, POC4 attempt #1
and #2 checkpoint/retained files, both attempt #3 blocked checkpoints and the original
1,677-entry historical tree verified unchanged. The two excluded accidental copies
were already absent after owner removal; no additional deletion/cleanup was performed.

TheBench was mounted with 1,007,616,000,000 bytes available at preflight. Established
Lima 2.2.0/VZ plain arm64, 8 CPUs/10 GiB/160 GiB configuration matched the repository.
Guest ext4 had 64,120,471,552 bytes available; no conflicting attempt #3 build/output,
active construction, mounts or loops. Full host package inventory and five masked
update units passed before construction, in the factory afterward, and after offline
validation. Host inventory digest remains
`352fb0f9ed6503e7570278573c8a04219856d8bde086c66e173c7d51c6dd0aa6`.

## Construction and security

Exactly one invocation used the established isolated network namespace and sanitized
`env -i` entry into `construct_poc.py ... --attempt 3`. Frozen transport supplied all
packages. The accepted debootstrap/chroot `/tmp` boundary, hostile-variable regression
protection, AppArmor and package-error handling stayed intact. Retained actual native
TMPDIR/AppArmor regression evidence verified; three non-mutating boundary tests passed.
No staging/package rework or repeated image invocation was necessary.

pi-gen exited 0 after **168.91 seconds**; maximum individual-process RSS **513,004 KiB**,
no swap. AppArmor 4.1.0-1 configured successfully. As in attempt #2, upstream APT reported
an unavailable pseudo-terminal for its terminal log and three unavailable GCC changelogs.
These nonfatal notices did not bypass package configuration or verification.
The VM was stopped after confirming no remaining construction/proxy processes, build
mounts or loops. Guest available storage after construction: 54,603,558,912 bytes.

## Exact retained artifacts

| Artifact | Relative path | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| Raw | `artifacts/private-poc4-attempt-3/2026-09-16-project-cbm-1.1.0-poc.4-lite-private-poc.img` | 3087007744 | `37d2699c7a639e050e531a4d5a132d4b197e5a60270a969814c573f436036cd8` |
| XZ | `artifacts/private-poc4-attempt-3/image_2026-09-16-project-cbm-1.1.0-poc.4-lite-private-poc.img.xz` | 598813860 | `4a6bce98e089e3c39246393b7476c687a7818ea5a6b67fa811fb6bee8da5a83e` |

XZ decompression hashes to the exact raw SHA-256. The raw hash is unchanged after
read-only inspection. Both external retained copies independently rehash correctly.

## Offline validation

**121 main + 20 supplemental + 26 Cover/utility checks PASS.** Read-only FAT/ext4
integrity and systemd unit checks PASS; **127 ELF objects** have no missing dependency.
All **672 installed package versions/architectures** match the 709 declared component
and base Debian package descriptors. No image repair or target execution was used.

Checks cover minimal lock-bound identity; incomplete first boot; machine-ID/SSH-key,
credential and builder-residue sealing; separate initially locked owner and authenticated
sudo; exact narrow helpers; runtime API, pcbm-info/config/About, preferences and boot
consumers; NetworkManager's offline initial policy, Wi-Fi enrollment absence and optional
services disabled; USB import; original qualification media; POC3 VICE geometry/F10;
SID-Wizard template/user disk and private StrikeTerm template/user disk/admission notice.

All seven unchanged Covers and exact registry, shared launcher, wrapper and renderer
match frozen hashes. Mapping, proportional desktop presentation, unprivileged execution,
timeout/fallback, mc normal-user path, Advanced Mixer without global store, import
feedback, SDL dependencies and utility versions pass. Cover hardware handoff remains
physical UNTESTED; accepted native headless lifecycle tests are separate evidence.

| Root before expansion | Bytes |
| --- | ---: |
| Filesystem capacity | 2430955520 |
| Used | 1651511296 |
| Free including reserved blocks | 779444224 |
| Available to ordinary user | 635580416 |
| Installed package-size sum | 1598556160 |
| Seven Cover assets | 1180157 |

Post-expansion capacity and first-boot/maintenance margin depend on actual media and
remain unmeasured. No arbitrary minimum card capacity is inferred.

## Rights and remaining validation

SID-Wizard 1.97 contains only the reviewed native core and notices. StrikeTerm 2014
Final remains **PRIVATE-ENGINEERING-ADMITTED / PUBLIC-RELEASE-RIGHTS-GATE-PENDING**.
Cover constituent graphics/font public rights remain unresolved. Owner-supplied SID/demo
reference media remain unbundled. Generic SID autostart is refused; supported PSID/RSID
playback remains deferred. No public distribution clearance follows from this build.

The exact Pi 3B procedure is ready for owner review/testing. Actual first boot/expansion,
interruption/retry, owner UI/authentication, display/Cover/VT transitions, VICE/audio/input,
mc/mixer, USB hardware discovery, persistence and applications remain UNTESTED. No-Ethernet
Wi-Fi requires an owner-controlled AP; Ethernet, SSH/Samba clients, mDNS and BBS require
suitable external environments. Independent clean rebuild/reproducibility and independent
encrypted backup/custody remain unproven.

## Recovery and owner handoff

Evidence: `qualification/poc4-attempt3-construction-2026-09-16`.
Recovery: `archive/poc4-attempt3-2026-09-16`; its `manifest.json.sha256` records
the manifest digest for integrity checking, not publisher authentication. `restore-report.json`
records final commits, full bundles, exact offline refs/peeled-tag comparison and fsck.
The checkpoint retains bounded evidence and artifact/input locators, with no extra image
copies or disposable credential trees. Earlier checkpoints remain immutable. TheBench
is still one failure domain, not an independent backup. Both feature branches stay local.

STOP for owner review. Use only the exact-hash attempt #3 procedure; no automatic
physical test, next build, other Pi model, boot optimization, PSID/RSID work or publication.
