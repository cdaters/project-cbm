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
