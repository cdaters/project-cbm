# Assembly64 central and home-server protocol comparison — 2026-09-25

The central service's JSON464 is **not established as an Assembly64-wide protocol
limitation**. A central deployment/client-registration condition remains plausible.
Spiffy's independent server has no central registration dependency, accepts any
client ID by default, and optionally enforces a locally configured ID. That is
source evidence of different admission behavior, not a successful CBM live test.

Recommend a small backend interface inside the already planned Product Assembly64
adapter: one Online Library UI and safe-ingestion path, with server-scoped identity,
capabilities and response handling. This is a design recommendation, not a runtime
change, permission to switch identities, or a claim that every compatible server
is ready to use.

## Sources and scope

- [Provider home-server documentation](https://hub.docker.com/r/freabemania/assembly64-home-server),
  freshly retrieved through the public Docker Hub API. Its description is identical
  to the previous retained study. No container was pulled or started.
- [Spiffy repository](https://github.com/spiffycrew/Spiffy_Home_Assembly_64/tree/ec67f38b59aac60d60694ca90a92d955d1f20c81),
  pinned at `ec67f38b59aac60d60694ca90a92d955d1f20c81`. Its complete tree has three
  files: Readme.md, LICENSE and a 470-line Python implementation; all were read.
  Readme.md identifies GPLv3; the implementation notice permits GPLv3 or later.
  The reference bytes are retained externally only. No implementation was copied
  into Product/Menu, executed, packaged, imported or made a build dependency.
- Existing [expanded access study](assembly64-expanded-study-2026-09-25.md), supplied
  discovery announcement, central OpenAPI snapshot and
  [transport comparison](assembly64-protocol-study-2026-09-25.md) are reused.
  Their successful/failed requests were not repeated. No new catalog or file
  request was made and no message was sent.

New evidence: `qualification/assembly64-home-protocol-2026-09-25` under configured
bulk storage. Acquisition records bind exact source URLs, dates, bytes and hashes.
Static observations below refer to the pinned `spiffy_home_assembly64.py` unless
another source is named. This is reference research, not interoperability testing.

## A. EXPLICITLY DOCUMENTED: distributed discovery and selection

The provider describes multiple independently hosted catalogs and registering a
server as public through its desktop client, or configuring private/local hosting.
Its supplied announcement explicitly invites other applications to retrieve the
directory at `GET /leet/homeserver/all-public-servers` and use those AQL servers.
Together these establish intended discovery and server choice. They do not require
every client to aggregate every server, establish automatic failover, or make a
directory listing a guarantee of availability or identical content.

The earlier capture lists three servers; the latest retained central discovery
requests returned JSON464. Current membership and availability remain unverified.
The desktop `/homeserver/public-servers` subscription-related route and advertised
`/homeserver/all-public-servers` route remain distinct. Server registration in the
directory is also distinct from registering an application's Client-Id.

Spiffy's README describes a minimal local server tested only with C64 Ultimate.
It documents presets, search, entry/file metadata and multipart downloads. It does
not describe directory registration. Its complete source has no registration,
discovery or outbound central-service request. Thus it proves an independent
compatible server implementation exists; it does not prove this particular server
is registered, publicly deployed or fully AQL-conformant.

## B. DIRECTLY OBSERVED: conventions and differences

All paths below include `/leet`. IDs and categories belong to their source server.

| Operation | Central published contract / retained evidence | Spiffy source |
| --- | --- | --- |
| Presets | GET `/search/aql/presets` | Same suffix, lines 341–354 |
| Search | GET `/search/aql/{offset}/{limit}?query=...`; additional variants in Swagger | Same paged suffix or bare `/search/aql`; default 100 entries, lines 356–391 |
| File metadata/list | GET `/search/entries/{itemId}/{categoryId}`, JSON `contentEntry` | Same suffix/envelope; one file per indexed item, lines 393–417 |
| Rich item metadata | GET `/search/meta/{id}/{category}` | Not implemented; dispatch at lines 330–350 has no such route |
| Category/compo tables | `/search/categories`, `/search/compotypes` | Not implemented; use available presets rather than assuming these exist |
| File bytes | `/search/bin/{itemId}/{categoryId}/{fileId}`; Swagger advertises `application/octet-stream` | Three path components, but the first selects the indexed file; third is read as a filename then unused, lines 419–435 |
| Discovery | Advertised `/homeserver/all-public-servers`, outside current Swagger | Not implemented |
| Admission | Registered IDs documented by client/Discord evidence; precise central enforcement unknown | Optional exact Client-Id match, before routing, lines 330–335 |

The provider Docker description promises a full AQL interface, richer optional
metadata and optional protected access. It does not enumerate its actual route
handlers, Client-Id checks or download framing. Do not infer that its binary server
is Spiffy's Python program or has every Spiffy quirk. Those details need a selected
deployment's documentation or controlled interoperability evidence.

**Search → metadata → download:** retain the result's item ID and category; fetch
`entries` to show/select files and sizes; fetch optional richer details only where
supported; then download the selected entry through that backend's route mapping.
Spiffy assigns IDs from scan enumeration (lines 175–202), with category zero and
mtime-derived year/date. The category route component is parsed but unused for
lookup. Its entry list returns a numeric ID, basename, size and timestamp. Do not
treat those IDs as persistent across rescans or use mtime as an authoritative release
year. Do not universalize Spiffy's interchangeable item/file IDs or ignored filename
to the central service, where those distinctions matter.

**Query compatibility is partial:** Spiffy's regex/dictionary parser and matching
logic are at lines 207–234 and 356–380. They are not the guide's complete Boolean
AQL grammar. Repeated keys overwrite; unhandled fields are ignored; `order` controls
name sorting. Its README says `sort`, while the code uses `order`; presets advertise
`date`, but matching handles `year`/`updated`. Missing filters can therefore silently
broaden results. A shared URL shape does not justify advertising unsupported filters
or forwarding the full central query language to every backend.

### Client-Id: identification, access control, or both?

| Service | Evidence-supported interpretation |
| --- | --- |
| Central | Swagger calls it the calling client ID and marks it optional; supplied registration precedent and a working client's registered ID show managed application identities. The provider app's 464 enum includes UNAUTHORIZED, but the exact central gate remains unobserved. Identification is documented; access control is strongly plausible, not yet diagnosed. |
| Spiffy default | `CLIENT_ID=None` and CLI default None (lines 38–39, 452–459): no header required or checked. No central lookup occurs. |
| Spiffy with `--client_id` | Exact header equality gates every GET. Missing/wrong ID produces HTTP404 and JSON `{"error":"No Access"}` via `_set_error`, not 464 (lines 279–281, 330–335). This is an application-ID allowlist, not proof of a secret or cryptographic client identity. |
| Provider home server | Documentation explicitly supports HTTP Basic protected mode and API_USER accounts. Client-Id enforcement is not specified by the reviewed page; it cannot be assumed to match central registration or Spiffy. |

There is no single universal meaning/enforcement rule for Client-Id across this
ecosystem. CBM must use its own honest ID, confirmed where required. An operator
choosing a local allowlist does not authorize CBM to impersonate its allowed client.
The presence of `token` in Spiffy's CORS allow-header list is not token validation;
its GET implementation checks no token, Authorization, cookie or User-Agent.

### Multipart download semantics

Spiffy `_send_multipart_file` (lines 299–316) wraps **one file** in `multipart/mixed`.
The outer Content-Type supplies a boundary. The part has Content-Disposition with
a filename, Content-Type `application/octet-stream`, a blank line and file bytes,
followed by the terminating MIME boundary. `_set_response`/`_send_chunked`
(lines 260–297) then apply HTTP chunked transfer framing to the whole representation.
MIME parts, HTTP chunks and multiple disks in a production are three different things.

The central Swagger advertises raw octet-stream downloads. The supplied historical
central response also shows that type, and Manager consumes response bytes directly.
The retained official firmware's `assembly.cc:17–20` configures a multipart-aware
writer. This suggests clients may encounter different download representations;
it does not prove that the central server currently returns multipart for CBM or
selects representation using Client-Id. That remains an interoperability question.

CBM's proposed download path should:

1. Let the HTTP library handle valid transport framing and status errors first.
2. Inspect the actual response Content-Type. Stream raw octets directly, or decode
   MIME parts using the declared boundary; never save the MIME envelope as a D64.
3. Bound metadata, part counts and sizes; verify completion and expected payload
   size where available. HTTP envelope length is not the file's payload length.
   Filenames are untrusted suggestions for existing safe ingestion, not target paths.
4. Match returned parts to the user's selected files. Spiffy proves single-part
   delivery only. Unexpected additional parts should not silently become downloads.
5. Hash the extracted payload and save successfully before offering the shared
   launch path. Cancellation or malformed/truncated framing must not commit a file.

[RFC 2046 §5.1](https://www.rfc-editor.org/rfc/rfc2046.html#section-5.1) defines MIME
boundaries independently of HTTP transfer framing; use a suitable parser with
bounded streaming rather than copying Spiffy's implementation or its fixed boundary.

**Concrete transport caveat:** Spiffy subclasses BaseHTTPRequestHandler but never
sets `protocol_version`; Python documents its default as HTTP/1.0. Its helper
nevertheless emits Transfer-Encoding: chunked for JSON and files. Static analysis
therefore identifies HTTP/1.0 responses with HTTP/1.1 transfer framing in the
unmodified program. [Python documentation](https://docs.python.org/3/library/http.server.html#http.server.BaseHTTPRequestHandler.protocol_version)
and [RFC 9112 §6.1](https://www.rfc-editor.org/rfc/rfc9112.html#section-6.1) establish
why this framing must be treated as faulty. It was not run to manufacture a pass.
This is a Spiffy-specific compatibility concern; it does not explain the central
nginx JSON464 on metadata GETs. CBM should report incompatible framing and require
a corrected/qualified server, not weaken its transport handling globally.

## C. INFERRED: the appropriate CBM abstraction

Use one narrow interface in the existing Product content adapter:

| Responsibility | Proposed contract |
| --- | --- |
| Directory | Fetch/cache registered-server descriptors separately from querying a catalog; show stale cached lists truthfully if discovery fails |
| Selected backend | Bind server identity, base URL, honest CBM client ID, any separately authorized credentials and verified capabilities |
| Catalog | Presets, supported search/filter/paging, optional details, selected item's file list |
| Transfer | Resolve the backend's opaque item/file IDs and stream decoded payloads into existing ingestion |
| Errors | Preserve HTTP status/provider code and backend name; distinguish unavailable endpoint, admission failure and malformed representation |

Central and compatible-server profiles can share most code while declaring route,
query and representation differences. Avoid a growing collection of guessed endpoint
fallbacks. A 404 can mean Spiffy admission failure, so status alone is insufficient
for deciding a capability is absent. Failures should not silently select another
server, change identity, broaden a query or substitute a similarly named title.

Keep cache keys and provenance scoped to backend plus item/category/file identity.
Do not equate IDs or catalogs across servers. Keep credentials scoped to the selected
origin and revalidate redirects. A directory's historical HTTP URLs do not authorize
lowering CBM's existing HTTPS policy or transmitting credentials in cleartext.
Qualify the intended server's transport before enabling it; no such change is made
here. Let the user select a supported source; federated search is unnecessary for
the first slice. The Menu remains a consumer of the same normalized Product flow.

This is a contained extension of the accepted adapter boundary, not a new daemon,
container dependency, scraper or replacement for the Bash/dialog/VICE architecture.
Original CBM code and original synthetic protocol fixtures can exercise raw/MIME
payloads, chunk splits, invalid boundaries, cancellation, duplicate files and
per-server capability differences without reusing GPL implementation or hosted titles.

## D. STILL UNKNOWN and effect on the central 464

**Yes, the observed 464 could be specific to the central deployment or its
client-registration policy.** Spiffy's independent admission behavior and ordinary
GET/JSON interface show why it must not be generalized to all AQL servers. The
earlier ID-request evidence and provider enum mapping strengthen the registration
hypothesis. Nothing in these two new references identifies the central error's
actual producer or proves that registration alone resolves it.

Remaining external questions are narrower:

- Confirm/allocate `project-cbm`, correlate the retained 464 timestamps, and confirm
  its scope for central search, downloads and discovery.
- Confirm the current directory and intended server-selection contract, including
  whether a central ID has any meaning on independently operated servers.
- Establish each selected server's supported query subset, optional metadata,
  item/file ID semantics, raw versus MIME responses, transport and authentication.
- Confirm applicable provider/server usage and attribution requirements.

A central discovery failure may prevent refreshing the directory; it does not by
itself establish that a previously known, independently authorized server is
inaccessible. Conversely, the existence of a standalone server does not make the
central catalog available elsewhere or authorize using an alternative identity.
No live central/home search-to-download success is claimed for CBM by this study.

## Preservation and next action

The [current inquiry draft](assembly64-provider-inquiry.md) remains unsent. Resolve
central registration and qualify any selected compatible backend before enabling
it. This task changes research/documentation only. Stable 1.1.0, private attempt18,
Menu, builder state and physical qualification remain unchanged.

Additive recovery: `archive/assembly64-home-protocol-2026-09-25`, with evidence
manifest binding and local-bundle offline restore/ref/peeled-tag/fsck verification.
Independent custody remains outstanding. Earlier evidence directories are sealed
and untouched; the new source snapshots stay outside the CBM repositories.
