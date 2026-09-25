# Assembly64 expanded access study — 2026-09-25

**Home-server follow-up:** [central/home protocol comparison](assembly64-home-protocol-2026-09-25.md)
adds the complete pinned Spiffy reference, optional local Client-Id gating, raw versus
multipart download semantics, a concrete framing caveat and the proposed narrow
backend interface. Central JSON464 is not an established protocol-wide limitation.

Project CBM Online Library is technically feasible as an independently implemented
client. The expanded evidence explicitly supports third-party applications and
shows a concrete practice of requesting a dedicated client ID by Discord DM.
Requesting `project-cbm` is now justified. Registration is the leading access
hypothesis, but neither the current 464 response nor the references establish that
issuing an ID is the only remaining external dependency.

This supplements the [reference audit](assembly64-reference-audit-2026-09-25.md)
and [protocol comparison](assembly64-protocol-study-2026-09-25.md). Their earlier
negative findings describe the smaller corpus available then. No foreign client
ID, credential or device identity was used. No reference software was executed,
hosted title downloaded, provider contacted, runtime changed or image rebuilt.

## Evidence scope and provenance

Evidence is retained under configured bulk storage at
`qualification/assembly64-expanded-study-2026-09-25`. Source filenames below are
relative to that directory unless explicitly identified as repository files.

- Fresh official Swagger UI, initializer, configuration and OpenAPI JSON. The
  schema remains 41,034 bytes, SHA-256
  `72529a92d0b1753ba8c768a61528ff638c52968c85eed2ab11e98ad680dd1846`.
- Supplied `AQL_Guide.md`, 14 guide screenshots and four subsequently supplied
  conversation/server-discovery images, copied read-only from the owner's
  `AQL Guide` directory in the historical evidence tree. The four later filenames
  begin `ChatGPT Image Sep 25, 2026`; they are treated as owner-supplied captures,
  not independently authenticated Discord/Facebook exports. All were visually read.
- Existing clean Manager source at `a4e55f12d6a08c3a435b1d63ced1c3a2c6f461e8`;
  the preceding audit already exhausts its tracked source/history and available
  issues/comments/releases, and the official Ultimate Elite II documentation.
- Historical `assembly64` directory and copied application JAR, SHA-256
  `3eec77896ac9c259e2e3e81d2f971422ae47019395e2f413c5c54121a79f8c26`.
  Static class/constant inspection only; possession is not a distribution grant.
- [a64-cli 1.1.1 release directory](https://releases.kephster.org/a64-cli/1.1.1/),
  manifest and Linux arm64 ZIP. Its SHA matches the fetched manifest; signature
  trust was not independently established. The ZIP has one executable and no
  source/docs. Limited binary-string inspection is not a complete client audit.
- [RetroNAS wiki](https://github.com/retronas/retronas/wiki/assembly64),
  [provider home-server documentation](https://hub.docker.com/r/freabemania/assembly64-home-server),
  and switcher source at `9966f70d3112a660ffd9c99e8eae3cec6ca7384b`.
- Additional working-client reference: u64deck README/server source at
  `b7e6b02c5ec5821edebb5d5261355215ffdbf0bc`. RetroTool README at
  `b5dd5ae30b3e0221f49cc06c24cb8cd03f7982f6` and official ARRM documentation
  were reviewed for UX only.

The original historical files remain unchanged. The initial guide copy failed
while its location changed; that interruption is retained. `javap` was unavailable
because the host has no Java runtime; retained failure records are not passes.
A small read-only classfile parser instead retains enum initializer instructions,
resolved constants and method bytecode. No Java runtime was installed.

## A. EXPLICITLY DOCUMENTED

**Third-party use:** the supplied guide, line 3, describes AQL as an open API
available to applications and names integrations beyond the main desktop client.
The first guide screenshot corroborates this text. The supplied Assembly64-branded
August 3 post explicitly invites other applications to use public-server discovery.
This materially answers intended third-party use; “open API” is not a blanket
license for redistributing hosted content.

**ID procedure:** the supplied image ending `02_28_52 PM.png` shows a developer
asking how to register their own client. In `02_29_14 PM.png`, Scooby/G*P replies
on June 14, 2026: “ping me in dm which id you want.” The same conversation later
reports a working client after a CORS correction. This documents an actual
request-by-DM practice. It does not show the private allocation reply, prove all
endpoints enforce registration, or allocate any ID to Project CBM.

Independently, the pinned [u64deck README, line 1124](https://github.com/zildac/u64deck/blob/b7e6b02c5ec5821edebb5d5261355215ffdbf0bc/README.md#L1124)
explicitly calls its dedicated client ID registered. Manager's README and release
notes acknowledge provider cooperation but do not describe its allocation exchange.
The a64-cli author describes a unique Client-Id in the
[0.2.1 release discussion](https://csdb.dk/release/?id=255744&show=review);
that historical statement does not establish the current binary's exact value or
registration procedure. No other client's ID should be adopted by Project CBM.

**Discovery:** the supplied Assembly64-branded post and separate response capture
identify `GET https://hackerswithstyle.se/leet/homeserver/all-public-servers`.
They describe registered AQL servers as usable by other applications with a common
AQL interface. The response capture shows No Auth, status 200 and these entries:

| ID | Description | URL in the supplied capture |
| --- | --- | --- |
| 53 | Public Domain Wares | `http://pd-wares.freabe.org` |
| 55 | GP ZeroDay | `http://bureus.asuscomm.com:7070` |
| 59 | IDreamIn8Bits | `http://a64.idi8b.com` |

These are a historical screenshot list, **not a verified current/live list**.
The August 3 post does not show its year. Today's discovery requests returned
464, so current membership, reachability and HTTPS availability remain unverified.
No listed server was contacted and no HTTP security downgrade was introduced.

**Home servers:** provider Docker documentation supports public registration and
private hosting, with the AQL interface. Protected mode can require HTTP Basic
authentication on every request; API_USER access and administrator roles are
distinct. Local content and optional `info.json` determine available metadata.
Thus a common interface does not promise identical catalogs, fields or credentials.
The RetroNAS wiki describes running the desktop client through RetroNAS Desktop;
it supplies no independent client-ID/access procedure.

**Protocol:** the [current Swagger](https://hackerswithstyle.se/leet/swagger-ui/index.html)
documents ordinary HTTP GET operations. Search operations list `client-id` as
optional and no security requirement. No global security scheme, 464 definition,
mandatory HTTP/2 or gRPC framing is declared. The schema also contains separate
account/login operations; their existence does not make tokens mandatory for search.
Runtime enforcement may be stricter than the published optional-header declaration.

## B. DIRECTLY OBSERVED IN CODE / RESPONSES

**Central API contract:** base `https://hackerswithstyle.se/leet/`.

| Function | GET path relative to that base |
| --- | --- |
| Paged AQL search | `search/aql/{offset}/{limit}?query=...` |
| Query presets | `search/aql/presets` |
| Categories / competition types | `search/categories`, `search/compotypes` |
| Item metadata | `search/meta/{id}/{category}` |
| File list / individual entry | `search/entries/{itemId}/{categoryId}`, `search/entry/{itemId}/{categoryId}/{fileId}` |
| File bytes | `search/bin/{itemId}/{categoryId}/{fileId}` |
| Whole-item ZIP / existence | `search/zip/{itemId}/{categoryId}`, `search/{itemId}/{categoryId}/exist` |

Use the published schemas rather than assuming that every download is a single
disk or that IDs are filenames. The public-server discovery route is absent from
this OpenAPI snapshot and must be documented separately.

**Manager:** `src/assembly64.rs` defines all seven previously audited operations,
its fixed client ID and `ultimate64-manager/0.5.2` User-Agent. The read/download
path adds no user token, API key, cookie, device identifier or account login.
Its 463 handling differs from generic errors, including 464. Metadata caches and
sequential downloads are observed implementation choices, not provider quotas.
Exact line anchors and the full header inventory remain in the reference audit.

**u64deck:** `server.py:4536–4542` uses its fixed client ID and a firmware-style
User-Agent, plus identity content encoding. No token is in that header builder.
The adjacent comment's claim that this User-Agent is expected is a client-author
claim, not a provider requirement. Project CBM did not send either identity.

**Desktop application:** `HomeServerRepository` contains both a subscriptions
workflow and `/leet/homeserver/public-servers`. This differs from the specifically
advertised `/all-public-servers`; the two must not be conflated. SearchRepository
builds search/preset/category/entry/meta requests around a host parameter, supporting
host selection. RemoteRepository contains client-ID, user-token and optional Basic
authorization handling. These desktop capabilities do not prove that every read
operation needs all three. Separate richer metadata routes in
ServerMetaDataService (`/search/metadata/...`, `/metadata/...`) are not the same
published contract as `/search/meta/...`; do not assume home-server equivalence.

**Provider-specific error evidence:** the retained desktop JAR's
`se/light/assembly64/model/exception/ErrorCode.class` enum initializer assigns
464 to **both `LINK_ERROR` and `UNAUTHORIZED`**. It assigns 422 to `NOT_REGISTERED`
and 421 to `INVALID_TOKEN`; these names do not identify which registration/token
context applies. `java-errorcode-mapping.json` retains the decoded instructions.
The duplicated numeric value and unknown server version prevent a unique diagnosis,
but this is now concrete provider-application evidence relevant to 464.

**Live bounded discovery checks:** honest User-Agent
`Project-CBM/1.2-access-research`; no credentials. The earlier desktop route
`/public-servers` returned JSON464 with the CBM study ID. The newly supplied
`/all-public-servers` also returned JSON464 with `project-cbm-design-study`, and
with the optional client header omitted. All response bodies, headers and request
records are retained. No current list was obtained; the screenshot's No Auth UI
does not reveal all its custom headers or prove anonymous success today.

The earlier transport tests remain valid: HTTP/1.1 is selected; HTTP/2-only ALPN
fails; HTTP/HTTPS and reference-compatible GET/header semantics still yield 464.
No tested transport change resolves the error. The supplied CORS conversation also
shows a historical HTTP/1.1 200 download; its browser CORS issue does not explain
the current native HTTP JSON464. There is no evidence for switching to POST/gRPC.

**Switcher:** its request hook rewrites Ultimate/Commodore client IDs and Host to
switch catalogs. It is not an allocation mechanism or a public-server discovery
implementation. It was inspected only, never installed, run or copied into CBM.

**CLI:** the 1.1.1 binary contains the central base URL, a `Client-Id` header name
and metadata/artifact routes. Strings alone cannot establish request control flow,
the configured ID, its authorization, or which operations require login. The
release author's credential-handling claims are not evidence that normal AQL reads
universally require an account. We did not execute the downloaded binary.

## C. INFERRED

1. A dedicated client-ID registration is the strongest next access hypothesis:
   the DM exchange, independently documented registered client and provider-app
   `UNAUTHORIZED` mapping are mutually consistent. It remains a hypothesis about
   **this** response until provider confirmation or an approved-ID comparison.
2. Normal central search/download likely uses an admitted application ID without
   individual-user login, given two reference header builders and the schema.
   No successful read/download with a Project CBM ID has established this yet.
3. Public-server selection can be implemented dynamically: retrieve the advertised
   directory, select a server and use its AQL search surface. Treat IDs/categories
   as server-scoped; confirm supported routes/capabilities and credential handling.
   A selected server's credentials must not be forwarded to another host.
4. No architecture or Pi 4 constraint has been identified that prevents Online
   Library. Independent query construction, JSON parsing, paging, file selection,
   bounded downloads, caching, safe existing ingestion and launch integration are
   technically straightforward. Feasibility is not an implemented/validated feature.

## D. STILL UNKNOWN — exact provider questions

| Earlier inquiry topic | Answer now supported | What still requires confirmation |
| --- | --- | --- |
| Third-party use and access | Explicitly intended; dedicated IDs are used; a DM request procedure is evidenced | Allocate `project-cbm`; confirm it covers central AQL, downloads and public discovery, and whether any account/token is needed |
| Identification / 464 | Own ID is appropriate; provider-app enum includes UNAUTHORIZED as 464 | Whether an unknown/unallocated ID caused these exact responses; current correct requirements, including any required honest UA format |
| Usage policy | Client examples cache metadata and avoid parallel bulk work; protected home servers can require Basic auth | Numeric rate/concurrency/download limits, cache expectations, retry/backoff and any server-specific constraints |
| Attribution / terms / change handling | Existing clients acknowledge Assembly64; published interface supports independent implementation | Required wording/links, applicable client terms, API version/change notification and any restrictions relevant to CBM distribution |

The repository contains client behavior, not the provider's current allocation
database, request logs or full operating policy. The screenshots show a precedent,
not the private agreement or a grant to CBM. Swagger omits enforcement and discovery
details. Therefore an ID is a likely necessary administrative step, **not proven to
be the only external dependency**. Successful central read/download and discovery
checks with the assigned identity are still needed. Per-server transport/auth and
the lack of a verified current server list are separate integration uncertainties.

## Independent implementation and UX

Implement the interface from Swagger and AQL documentation, with original CBM code:
query encoding, typed response handling, paging, error messages, caching, selected
file streaming and existing safe ingestion. No need to copy Manager, firmware,
switcher, CLI or desktop implementation, package their binaries, or reuse identities.
Software licenses and API availability do not grant blanket rights to hosted titles.
No new redistribution admission is made by this study.

| Reference / current CBM requirement | Useful Online Library behavior |
| --- | --- |
| [RetroTool](https://github.com/dgateles/retrotool) selective scraping, matching and resumable progress | Explicit selection, clear progress, preserving existing data, reliable retry; no hidden bulk acquisition |
| [ARRM](https://jujuvincebros.fr/wiki/arrm/doku.php?id=arrm_relooked_en:start) filtering, metadata editing and backups | Clear filters, visible provenance, repairable metadata and reversible library changes |
| Accepted CBM content design | CONTENT → Online Library; provider attribution inside; search/filter/results → choose files → Save to Library or Save & Run |
| Existing CBM safe ingestion | Already Present for identical bytes, Keep Both for different bytes, truthful cancellation/offline errors, save before the shared VICE launch |

RetroTool/ARRM enrich and manage existing libraries; they are not replacements for
Assembly64's catalog/content API. Avoid turning the Pi console into a scraper suite.
Artwork scraping, background collection sync and another metadata-provider account
are not requirements for the first Online Library slice. A server selector is
feasible but remains a proposal beyond the existing single-provider access gate.

## Checkpoint

The [short Discord draft](assembly64-provider-inquiry.md) is prepared, not sent.
Next: the owner requests the dedicated ID and missing operational guidance; retain
the reply, then perform bounded checks using only the confirmed CBM identity.
Runtime implementation remains outside this research task. Pi 4 attempt18 testing
continues independently; no new physical result has been supplied.

The evidence manifest and additive recovery at
`archive/assembly64-expanded-study-2026-09-25` bind this checkpoint to source,
bundle verification, offline restore, refs, peeled stable tag and fsck checks.
Independent custody remains outstanding. Product 1.1.0 tags/artifacts and private
attempt18 are unchanged; Menu/reference repositories and unknown local work remain
untouched. Documentation checks are recorded with the evidence; no runtime tests
were needed for this documentation-only change.
