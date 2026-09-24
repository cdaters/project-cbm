# Final 1.1.0 USB import — owner disposition, 2026-09-24

## Candidate and owner report

This decision applies to final attempt15, Product/Menu 1.1.0, with the exact
[final image identities](final-1.1.0-pi4-smoke.md#verify-the-release-set):

- Raw SHA-256: `6c9b7599461a41f6ab30b666dd718329c34f863f11a46dfd20d61fe9830d2468`.
- XZ SHA-256: `8b3738a204da16e148f5674a95f1ffb55a67b8ad1ce1d997b1858594a899c13d`.

The owner reports the final Pi 4 smoke test is in progress and everything tested
so far works. USB import copied supported files from multiple directories and
unmounted the source afterward. This is a bounded owner report, not an overall
smoke PASS or evidence that every checklist item has been completed.

## Accepted behavior and documentation verification

The owner explicitly accepts the following documented 1.1.0 behavior:

- IMPORT scans the selected USB partition recursively for supported regular file
  types, subject to documented metadata exclusions and operation limits. It has
  no source-folder or per-file selection screen; choosing the category starts it.
- Relative source paths are preserved under the selected category and machine's
  `Imported` directory. SID files instead route to `music/c64/Imported`.
- Existing destination names are skipped, without content comparison/replacement.
- The source is mounted read-only for import and automatically unmounted on
  cleanup. Removal is safe only after release is confirmed; uncertainty requires
  leaving the drive connected until safe shutdown.
- FILES / Midnight Commander browses the library and home. IMPORT does not leave
  USB media mounted for subsequent browsing.

The [release content guide](../release/content.md#usb-import) already states that
all eligible files in the chosen partition are considered, subfolders are kept,
and there is no separate per-file selection screen. Its nested destination
examples and whole-source-tree explanation describe recursive path preservation.
The supported-type table, metadata exclusions, limits and SID exception qualify
that scope. The [FILES guide](../release/user-guide.md#files-and-midnight-commander)
explicitly describes USB access through Import rather than automatic MC mounts.
No scan-semantics documentation correction is required for 1.1.0.

Repository and staged `releases/1.1.0/docs/release/content.md` bytes match SHA-256
`4d32eb42182d260443ec3f5cde4cb0250536c2b742ab9ea63eec23b20db4d18a`.
The prior read-only Pi inspection also matched this installed guide and the
Runtime/Menu import implementation to the final source. No import, mount or
runtime modification was performed by the investigation.

## Known reporting limitation — deferred, nonblocking

`runtime/project_cbm/import_client.py` discards `ignored_metadata` on successful
results and converts failures into a generic result, losing structured `error`
and `source_unmounted` information. The Menu can therefore omit accurate metadata
counts and report drive release as unconfirmed even when cleanup succeeded.
The guide's statement that results distinguish ignored metadata overstates what
the current client delivers; this limitation is retained openly here.

The owner accepts deferral because this fails conservatively and does not affect
imported content, filesystem safety, runtime behavior or release integrity.
Do not change frozen packages, final images, release tags or the candidate for
this issue. The [four post-1.1.0 tasks](../design/post-1.1-roadmap.md#usb-import-and-content-ingestion--owner-deferred-2026-09-24)
record the reporting fix, selection UX, shared-ingestion consideration and
separate USB browsing workflow. No architectural or UI changes are implemented.

## Next action

Continue only the unfinished [owner Pi 4 smoke checks](final-1.1.0-pi4-smoke.md#minimal-smoke-procedure)
on the existing image. Retain item-level owner results, hardware/card details and
observed free space before recording overall completion. Previously completed
checks need not be repeated. Publication remains separately owner-gated.
