# Private dev6 / attempt25: direct boot and Online Library retest

PRIVATE NON-RELEASE Project CBM 1.2.0-dev.6. Built and validated; physical UNTESTED.
[Exact record](private-1.2-dev6-attempt25.json),
[focused Pi4 procedure](../qualification/attempt25-pi4-directboot-online.md),
[attempt24 physical evidence](../qualification/attempt24-full-physical-results-2026-09-27.md).

Frozen Product `decf2b31d2d965391e804791e26b19404b655312`; Menu `5260d5332a2fb45fcb472ff9fb0f3b9fa86610fc`,
annotated `v1.2.0_dev5` object `2b4893068bc9ec42b1e4cfdcd78ffe20128bac30`.
Lock `52f551e722aeb6edcee31f87ccdbc376c0ef1407dcf8c63e733d482ea765ab1a`. One build; reproducibility not claimed.

Product fix4bde3bb waits for primary artwork release/reap/console restoration before
capturing the shared launcher's baseline and starting machine Cover/VICE. The old
race selected offscreen and captured K_OFF instead of the original Unicode baseline.
Post-TERM mode still was not measured before the owner's state-changing diagnosis;
no retroactive scancode-mode claim is made. This change lives in Product image
integration; it does not change the Runtime Debian payload.

Menu5260d53 adds explicit acknowledgment of invalid/empty presets and dialog errors,
retains existing filters, bounds preset pages and holds Server Information until
Refresh/Back. Current live responses and SSH selectors worked; owner Repository
retest also worked. The original transient flash trigger remains unconfirmed.
Do not claim a demonstrated provider or client-admission fault, or that a longer
sleep fixed it. BIN policy, backend networking, privilege boundaries and FTP policy
are unchanged. Original physical failures remain in the record.

## Packages and verification

Only Menu rebuilt: `1.2.0~dev5-1+pcbm1`, 1303824 bytes,
SHA-256 `7a66edb52b6bdbcb3677bea3214d393e7ceac4f6c304afbb089b5c8bf72eb114`.
Runtime `1.2.0~dev4-1` and separate GPL KMS `1.0.0~dev2-1` reuse exact packages
from21 through24. Complete component descriptors, source/effective modes and hashes
match. Their original corresponding-source/offline compile and GPL scenario evidence
remain applicable; no unneeded rebuild or new license admission.

Native Product353/Menu122, zero skips. Installed USB11, screenshot12, Online8 PASS,
including slow presets, multi-filter retention, directory failure/retry/persistence,
shared writer and HUP cleanup. 372 image checks plus4 exact boot/Online installed
checks,7 privacy checks and11 KMS security/ELF checks PASS. All673 installed package
identities match retained inputs; full ELF closure and raw/XZ equivalence PASS.
3330 exported frozen-kit files verified.
PTY/modeled ioctl tests are not physical KMS/keyboard qualification.

## Exact output files

Relative to configured ProjectCBM-Work:

- Raw: `artifacts/private-1.2-dev6-attempt-25/2026-09-27-project-cbm-1.2.0-dev.6-lite-private-1.2-dev6.img`
  3095396352 bytes; SHA-256 `adc26fff5355d587547a72dcba737baab7f931d3d66ac646588151c91bb86d49`.
- XZ: `artifacts/private-1.2-dev6-attempt-25/image_2026-09-27-project-cbm-1.2.0-dev.6-lite-private-1.2-dev6.img.xz`
  599632072 bytes; SHA-256 `77d61462479d26593d60dbce04b1e483365e371103d53664205b97f04f17d671`.

Root capacity 2439266304 bytes; used
1655738368; available to user before expansion
639246336. First-boot expanded capacity and
maintenance margin require physical measurement; no nominal card minimum is inferred.

## Preservation and handoff

Host capability/update guards and inventory unchanged. Stable1.1.0 and attempts
18/19/20/21/24 raw/XZ hashes verified unchanged. Earlier failures, tags, frozen
inputs and evidence are retained. Attempt24's live software was not patched.
No publication, hosted-media bundling, FTP failover or provider message.

Recovery `archive/private-1.2-dev6-attempt25-2026-09-27` binds both repository bundles,
exact refs/peeled tags/fsck, inputs/packages/images/tests and physical evidence.
Verify its external manifest and restore report. TheBench is same-volume unencrypted
custody; independent encrypted backup/restore remains OUTSTANDING. STOP for Pi4
physical testing. No new feature or release follows automatically.
