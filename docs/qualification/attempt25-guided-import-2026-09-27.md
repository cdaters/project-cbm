# Attempt25 Guided Import physical PASS — 2026-09-27 UTC

**PRIVATE NON-RELEASE 1.2.0-dev.6, Raspberry Pi 4 B.** This additive report closes
Guided Import's pending row in the [earlier physical matrix](attempt25-physical-results-2026-09-27.md).
The earlier report and sealed evidence retain their original chronological scope.

Installed identity was read again and matches build/lock
`52f551e722aeb6edcee31f87ccdbc376c0ef1407dcf8c63e733d482ea765ab1a`.
This is the same attempt25 raw SHA-256
`adc26fff5355d587547a72dcba737baab7f931d3d66ac646588151c91bb86d49`
(3095396352 bytes), XZ SHA-256
`77d61462479d26593d60dbce04b1e483365e371103d53664205b97f04f17d671`
(599632072 bytes). Factory hashes were verified in the preceding review; no image
rebuild or mutation occurred here.

## Results

| Case | Result | Basis |
| --- | --- | --- |
| Back | PASS | Explicit owner physical report. |
| Parent folder selection | PASS | Explicit owner physical report; source views also show Parent folder. |
| Hidden opaque IDs | PASS | Owner confirmation plus direct inspection of partition, source, file selection, category, machine and review screens. |
| Human-readable sizes | PASS | Owner confirmation; review displays 512.2 KB for three selected files. |
| Select all supported files | PASS | Preview changes from zero selected to all three D64 files selected. |
| Explicit category/machine and destination review | PASS | Category and machine choices precede review under games/c64; no filename-based inference claimed. |
| Import completion and normal release | PASS, UI-reported result | Final retained screen: Saved 3; Already Present 0; not completed 0; USB released, safe to remove. No independent file-byte comparison was performed. |
| Guided Import screenshot context | PASS | All twelve retained 1920×1080 PNGs are readable and show the workflow. No measured latency or new HDMI comparison claim. |

The agent copied and viewed all twelve named PNGs. Each copy's size and SHA-256
matches the original over SSH. Exact names, hashes, byte counts and descriptions
are in the [addendum catalog](attempt25-guided-import-2026-09-27.json).
Private copies remain under `qualification/attempt25-guided-import-2026-09-27/screenshots`
in ProjectCBM-Work. Screenshots remain outside Git and image payloads.

Chronological screenshot suffixes (prefix `pcbm-20260927T`, extension `.png`):
044202Z Content entry; 044223Z partition; 044238Z root; 044254Z c64 folders;
044307Z games folder; 044321Z selected source; 044343Z preview; 044356Z select all;
044448Z category; 044523Z machine; 044536Z review; 044557Z saved/released result.
The parent Content menu's readable action tags are distinct from opaque internal
IDs; the guided Import screens show friendly labels without the opaque tags.

## Current disposition

**No focused functional physical checks remain for attempt25.** The supplied result
closes Parent/Back, readable sizes and hidden IDs; no repeat of completed cases is
requested. The [separate FILES → USB partition-picker presentation FAIL](attempt25-physical-results-2026-09-27.md)
remains open. This does not undo USB navigation/copy/release PASS, and this addendum
does not declare that defect fixed or the entire candidate all-PASS.

Candidate may advance to private engineering review with the known presentation
finding. Any source correction belongs to a separate change/distinct candidate,
not an in-place attempt25 patch. Deliberate busy-unmount, injected failures, formal
timing, multi-display and other-model coverage retain their previously stated
limits; they are not additional requests in this focused retest. No release begins.
BIN remains outside generic guided import; this sequence tests D64 media only.

No live configuration, package, USB mount or file-content changes were made by the
agent. Original Pi captures, prior attempts, stable1.1.0 and previous seals remain
unchanged. Additive recovery: `archive/attempt25-guided-import-2026-09-27` in
ProjectCBM-Work, with source bundles, offline restore/ref/tag/fsck checks and a
manifest. Same-volume recovery is not independent encrypted custody; that remains
outstanding. Documentation checks only; no runtime tests rerun for this update.
