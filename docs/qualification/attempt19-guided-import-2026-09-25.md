# Attempt19 guided USB Import: owner results and visible-ID defect

Recorded September 25, 2026 (Phoenix). **PRIVATE NON-RELEASE.**
[Structured physical report](attempt19-guided-import-2026-09-25.json) binds the owner's
observations to Pi 4 B, Product `1.2.0-dev.2`, attempt19:

- Raw SHA-256 `f69fbee34448936d9df942ab0c8ce990b9ccd3a85e66b95d232f0d7c8caa8d44`.
- XZ SHA-256 `00e88150f5d2105f89182e14e14ed27517a672cb57c6134598dcfa451dfe0fca`.
- Build ID `1b69db05988dc3435b3460eb045a91c7dcca4fcfe7a7d8b3eebb846e2c2d37ce`.

## Physical results

**PASS for the reported guided-import behaviors:** CONTENT → Import from USB is
present and functional; source-folder navigation exposes `c64/roms` and nested
folders; scanning the reported JiffyDOS C128 directory recognizes its one `.prg`
and reports its `.bin` files unsupported. An unsupported-only directory reports
zero supported files. Machine and category remain explicit choices; C128 is not
inferred from names. Explicit Import saved the selected `.prg` and safely released
USB. This confirms the two-workflow finding in the prior installed UI audit and
resolves the earlier observation that CONTENT Import appeared absent.

These are bounded U1/U2/U3/U4-related observations, not complete passes of those
fixture-based procedures. Whole-partition counts/paging, no-copy snapshots,
selection/deselection/Back variants, prescribed hierarchy/hashes/journal checks,
U5 duplicate/Keep Both and U6 whole-partition Select All remain unreported. B2
busy-unmount remains unperformed; normal safe release has passed in both reported
workflows. Earlier MC/C64/demo/F10/Menu PASS is retained; normal reboot/shutdown was
also reported good in the preceding owner follow-up. Copied-file hashes/relaunch
specifically after reboot and formal timings have not been separately attested.

**FAIL — guided-import presentation:** opaque hexadecimal folder identifiers appear
beside friendly names. Attempt19 retains this physical UX defect. Correct labels
should show only folder/file names and friendly actions such as Scan this source
and Parent folder. Backend identifiers must remain distinct and stable even when
visible names are similar or identical after truncation.

## Format policy stays unchanged

The Product `ingestion.EXTENSIONS` allowlist deliberately excludes `.bin`; discovery
checks the lowercased extension against that same allowlist. Raw binary is semantically
ambiguous and can represent ROM/firmware resources rather than ordinary runnable/media
content. `.prg` recognition establishes a supported format, not machine compatibility,
ROM suitability or proof this particular file was executed successfully.

Do not broaden the allowlist to accommodate ROM images. Future ROM management would
need a separate design with explicit ROM type, target machine and VICE configuration
semantics. No such feature, ROM payload collection or distribution decision is made
here. See the [accepted resource exclusion](../design/content-ingestion-online-library.md)
and [development guide](../development/content-1.2.md).

## Presentation correction and qualification boundary

`pcbm-import` now opts into the existing `PCBM_UI_HIDE_TAGS=true` UI contract.
Every guided-import dialog receives `--no-tags`: device tokens, folder/file IDs,
category/machine keys and action tags remain internal. Dialog still returns the
selected tag, so FIFO requests, backend mapping and duplicate handling are unchanged.
Descriptions, counts, file details, review and result messages already use friendly
fields; no runtime model or formatter change is needed. This switch is scoped to
the importer process, not a global Menu policy.

The behavioral regression creates different folders/files whose 60-character labels
collide, selects the second folder and file, verifies the exact IDs in backend
requests and confirms only the intended file is saved. It checks hidden-tag mode
on every guided-import menu, including device, preview, actions and destination.
A separate real-dialog test uses TERM=linux with a controlling PTY, identical/similar
labels and three different returned tags; screen output must contain the labels
and no tags. Synthetic test content contains no supplied ROM bytes.

Menu correction commit: `f9c4607d884a5573a943a9e1c1dd01832ca6dece`. Native Menu **109/109 PASS**, including
real dialog/PTY rendering and tag return; host **108 PASS, one native-only skip**.
Existing Product ingestion **21/21 PASS**. The real-dialog test removes color
rendition sequences before checking text because dialog colors mnemonic letters
separately. Initial environment/harness failures are retained, followed by the
successful complete native run. No host package installation was needed.

Read-only SSH reconfirmed attempt19 identity and the unchanged installed importer/
allowlist. At that snapshot the Import mount was absent and the browse mount was
active exFAT with `ro,nodev,nosuid,noexec`; it was left untouched. This later snapshot
does not replace the owner's successful earlier release observations.

This is a source correction only. Before deployment it needs a distinctly versioned
Menu package and fresh private candidate; never patch attempt19 or replace its package.
The fix is not physically qualified by the owner's pre-fix observations. Runtime
and its format allowlist are unchanged. Screenshot and Online Library remain separate.

Evidence: `qualification/attempt19-guided-import-ui-2026-09-25`; the preceding read-only
UI audit remains at `qualification/attempt19-installed-ui-audit-2026-09-25` under bulk
storage. Additive recovery: `archive/attempt19-guided-import-ui-2026-09-25`; manifests
and offline bundle/ref/peeled-tag/fsck report bind completion. Independent encrypted
custody remains outstanding. Attempt18 failed evidence and attempt19 artifacts remain
unchanged; no release or publication begins.
