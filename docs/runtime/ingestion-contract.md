# Content ingestion contracts — provisional 1.2.0

This development contract implements the accepted [design](../design/content-ingestion-online-library.md).
Project CBM 1.1.0 remains the current stable release; these changes are not in its
packages or qualified image.

## Phase 1: importer results

`pcbm-import-operation` accepts the existing bounded schema-1 requests. It returns
only validated fields from the fixed broker, never stderr, arbitrary messages or
exception text. Requests remain limited to 4 KiB and broker replies to 8 KiB.

| Result | Exit | Fields in addition to `schema_version: 1` |
| --- | --- | --- |
| Device list | 0 | `status: ok`, at most 16 validated token/label pairs in `devices` |
| Completed import | 0 | `status: ok`, nonnegative integer `copied`, `skipped`, `bytes`, `ignored_metadata`, `source_unmounted: true` |
| Incomplete import | 2 | `status: failed`, allowlisted `error`, `source_unmounted` boolean or null |

Error codes are `access_denied`, `space`, `limit`, `depth`, `entries`, `copy_failed`,
`mount_failed`, `unmount_failed`, and `unavailable`. A structured broker failure
with exit 2 is parsed normally. Unknown codes, mismatched exit/status, invalid
types, transport failures and malformed responses produce `unavailable` with
`source_unmounted: null`. Only literal `true` confirms cleanup. `unmount_failed`
cannot assert successful cleanup. Missing metadata count means zero; older Menu
consumers can ignore the added success cleanup field. A new client with an older
broker that omits successful cleanup confirmation fails conservatively.

The broker emits successful cleanup only after ordinary unmount returns and its
fixed source path is no longer mounted. Completed files survive later copy or
cleanup failure. Counts on failed imports are not available from the existing
worker and are not fabricated. The existing Menu error formatter explains partial
completion and only reports safe removal for confirmed cleanup. No UI redesign,
source mount-policy change, overwrite or elevated copying is part of this phase.

## Validation and physical scope

`tests/test_import_result.py` exercises the actual client entry point and existing
Menu formatter using synthetic replies: success/metadata, partial failure,
cleanup failure, malformed data, exit disagreement and timeout. Existing content
and metadata copy tests remain applicable. Host tests do not qualify USB hardware.

On a later distinct development image, the bounded Phase 1 Pi 4 check is one
FAT/exFAT import containing content plus host metadata, one controlled incomplete
copy, and one busy cleanup failure: verify counts, retained completed files and
conservative removal guidance. Bind results to that image hash; do not modify or
repeat qualification against the published 1.1.0 image. Physical status: UNTESTED.

## Phase 2: unprivileged ingestion and USB discovery

`ingestion.py` owns source-neutral items, explicit category/machine planning,
selected-destination hashing, collision decisions and streaming safe writes.
`usb_discovery.py` owns no-follow USB traversal and revalidated file opening;
`ingest_session.py` coordinates review/selection and private provenance. None mounts
media or downloads network content. Source adapters supply streams, not commands.

Extensions identify a supported format only. Candidate summaries report category
and family as `unknown`. Review requires explicit category/family. Programs/Shared
is the offered Unclassified fallback, not a claim of application type or universal
machine compatibility. Unlike the compatibility importer, this explicit-choice
workflow does not silently reroute SID files on extension evidence alone.

Scan opens only directories and stats entries. It neither reads payloads nor writes
content, destination folders or provenance. A failed/limited scan exposes no partial
candidate snapshot. Whole-partition or folder scope is selected using opaque folder
IDs. Preview/selection pages contain at most 20 items; no full tree enters dialog
arguments. All, clear, individual and folder-descendant selections are supported.
Rescan invalidates selection and plan. Folder selection is anchored by a discovered
file ID, never a caller-supplied path. Root folder IDs are session-local.

Existing bounds remain: 16 eligible partitions, depth 12, 10,000 visited entries,
2 GiB scanned eligible bytes and 256 MiB destination margin. Narrow the scope when
limits are reached; results are never silently truncated. A directory iterator is
bounded before sorting. Known metadata subtrees count once; ordinary dot directories
remain eligible. Symlinks and special files are excluded. Removed/changed files
invalidate access; no-follow descriptors and nonblocking regular-file checks avoid
following a replacement symlink or hanging on a substituted FIFO.

Selected paths remain beneath `<category>/<family>/Imported/<collection>`. A scoped
folder supplies its collection name once; a whole partition uses `USB Import`.
No flattening or migration of existing content occurs. Hashing examines selected
same-size collision candidates only. Same-path equal bytes are Already Present.
Any unequal collision moves the entire selected collection into a predictable sibling,
for example `USB Import (2)`, retaining disk-set relationships. A retry checks those
siblings and reuses identical files. The initial implementation does not search/hash
unrelated library trees for duplicate bytes. It never hardlinks existing or source
content; atomic publication links only a newly written temporary inode and removes
its temporary name. Destination changes after review fail with `plan_changed`.

Each save streams at most 1 MiB at a time, checks cancellation between chunks,
checks space again, fsyncs and commits without replacement. Partial/cancelled results
preserve completed files. Counts distinguish saved, Already Present, failed and
unattempted items; `kept_both` describes collection separation. A failed provenance
write after file commit is reported as partial, never as an absent file.

Private append-only per-job JSONL journals live outside content at
`/home/pcbm/.local/state/project-cbm/ingestion`, mode 0600. They contain pending
owned temporary paths, saved source-relative names, destination, UTC time, size and
SHA-256, followed by the job result. They support later Recent Additions; no UI
feature or database is claimed yet. Normal cancellation/failure removes the owned
partial file. After a power loss, an unfinished journal identifies possible partial
files; automatic crash reconciliation is not yet implemented. Do not delete or
classify a saved file solely from an incomplete journal.

### USB session wire and privilege boundary

The existing fixed sudo helper additionally accepts one schema-2 `session` request
with an enumerated device token. It retains the exclusive import lock, verifies
USB ancestry/device/disk sequence, and mounts at its existing fixed source location.
FAT/exFAT/ext4 policies and UID/GID 1000 copying are unchanged. No source path,
mount option, destination path, PID, URL or executable enters the root request.

A fork drops supplementary groups and GID/UID before reading the review protocol.
The unprivileged worker accepts newline-delimited operations `folders`, `scan`,
`page`, `select`, `plan`, `import`, `cancel`; requests are at most 4 KiB and replies
8 KiB. Only `import` writes payloads. A 300-second idle lease and 1,800-second total
supervisor deadline bound review. EOF, cancellation and expiry return for cleanup;
a busy operation polls for a cancel request between work units. Re-entry after an
expired session needs fresh discovery. One session is active at a time, conservatively
preventing import/browse contention across partitions.

The parent reaps the worker, attempts ordinary unmount and checks actual mount state
before emitting the final schema-2 result with `source_unmounted`. TERM grace and
KILL/reap are bounded; a worker still blocked in kernel I/O cannot produce confirmed
safe removal. Unmount failure preserves the worker's completed counts and marks
cleanup false. No forced/lazy unmount, root content parsing or Internet access is added.
Shutdown uses existing process termination and normal filesystem unmount; no mount
is configured to persist or remount at boot. Real shutdown timing remains a native/
physical qualification item.

### Phase 2 checks and limits

Twenty-one shared/discovery tests and six broker-adapter tests cover empty/nested/
scoped trees, dot/metadata names, mixed-case extensions, symlinks/FIFOs, traversal,
limits, selection/pages, low space, duplicates, conflicting sets, cancellation,
changed/removed media, partial copy/provenance failure, multiple partitions,
system/non-USB exclusion and cleanup failure. Full host regression: 279 PASS.
Privileged calls are mocked; this is not native mount or physical qualification.

Bounded Pi procedure for a later exact-hash development image: FAT/exFAT representative
media, two partitions, whole/folder scan, cancel before Import, select/deselect,
unknown classification, multi-disk import/retry/conflict, removed media and busy
unmount. Verify no payload appears before Import, source bytes remain unchanged,
and F10/Menu regression on one existing C64 launch still passes. Physical UNTESTED.
