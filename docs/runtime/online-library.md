# Online Library — private 1.2 development

CONTENT > Online Library is powered by Assembly64. An Internet connection is
required to search and download; saved files remain available offline in Browse
Library. This is an original client of the published API, using the provider-
registered `client-id: cbm` and an honest Project CBM User-Agent. The owner confirmed
registration on 2026-09-26. No reference-client code or identity was copied.

## User-directed flow

Search by plain title/name, optionally group, repository, category or year. The
latter choices come from the selected server's published presets; unsupported query
operators are rejected, never silently ignored. Results are paged 20 at a time.
Choose a release, read its details, select each needed file/disk, and choose a
library category and machine explicitly. Shared is available when uncertain; file
names/extensions do not establish compatibility.

Prepare Save downloads only the selected files into private anonymous temporary
storage. Review the exact destination, Already Present and Keep Both outcome, then
choose **Save to Library**. Back can change selection/destination; temporary data
is discarded on cancellation/session exit. Files retain relative folders; a
conflicting set goes into one numbered sibling collection. No automatic launch:
use the existing Browse Library launcher after saving. Save & Run is deferred.

Limits for this first slice: 32 MB per file, 64 MB and 100 files per selection,
1,000 file entries per release, 20 results per request, at most 1,000 result offset.
Unsupported/oversize entries are counted, not silently made importable. BIN remains
outside the general allowlist. Sizes use 1024-byte steps with familiar MB labels.

## Backends and networking

A server profile owns its URL, identity, supported filters, discovery capability
and download representations. Only **Assembly64 Central over HTTPS** is enabled.
Server Information reads the public directory independently. Listed home/public
servers are shown as not qualified for selection; their HTTP URLs do not cause a
connection, security downgrade or automatic failover. Failure of discovery does
not disable searches against Central. Qualifying another profile is future work.

Python's existing standard-library HTTP client handles HTTP framing. No aria2,
FFmpeg, shell curl, proxy credential inheritance, cookies, bearer tokens or redirect
following. One online session/request sequence and one selected download at a time;
no crawling, background fetches or mirrored catalog. Requests have an 8-second I/O
timeout, 45-second elapsed deadline checked between bounded reads, byte limits and
cancellation checks. No automatic network retry; the user chooses Retry. HTTP429
imposes a 5–300 second cooldown (60 seconds without a numeric Retry-After). This is
our conservative policy, not a claimed provider quota. Presets/discovery are cached
in session memory for ten minutes, metadata/search for five minutes, max32 entries.

The published central file endpoint returns application/octet-stream. A profile may
also admit multipart/mixed: parse MIME separately from HTTP chunks, require exactly
one selected part, validate the suggested filename without using it as a path,
reject nesting/extra parts and unsupported encodings. Validate size and basic format
plausibility before staging. This does not certify emulator compatibility or safety
of untrusted media. Other server-specific representations require qualification.

## Privilege, storage and privacy

The adapter runs as ordinary pcbm after setup readiness. It has no sudo rule,
capability, service or listener. No caller-supplied URL, command or filesystem root.
The shared ingestion planner/writer owns path safety, free-space checks, atomic
publication, duplicate handling and truthful partial results. An exclusive shared
job lock protects plan/review/save; descriptors and anonymous staging are closed on
exit. A process crash cannot leave named staging payloads. Completed library files
survive a later cancellation/failure. A private 0700 ingestion state directory
holds 0600 provenance journals including backend, release, selected paths and
saved hashes. They are outside the content share. Search/preset caches are memory
only. Hosted files are never bundled with the appliance image.

## Evidence and remaining limits

Bounded requests on 2026-09-26 to the current OpenAPI, presets, search, categories,
public directory, release metadata and file list all returned HTTP200 with `cbm`.
The previous metadata JSON464 was resolved for these tested requests. This supports
an identity-dependent central access explanation; it does not assign a universal
meaning to HTTP464 or establish every home-server policy. No hosted title was
fetched for throughput or testing. Private exact bodies/statuses are retained at
`qualification/assembly64-cbm-live-2026-09-26` on registered external storage.

Wire authority: [official Swagger](https://hackerswithstyle.se/leet/swagger-ui/index.html),
[current OpenAPI](https://hackerswithstyle.se/leet/v3/api-docs). The supplied AQL guide
is complementary syntax documentation. Physical search/download and Pi footprint/
latency remain unqualified until the new image is tested. Formal provider quotas,
attribution beyond the supplied branding, and independently operated server access
policies remain unknown. Provider questions are deferred until after owner testing;
no message is sent automatically and no redistribution right is inferred.
