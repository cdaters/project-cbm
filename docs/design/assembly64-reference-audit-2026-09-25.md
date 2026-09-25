# Assembly64 reference and Ultimate Elite II access audit — 2026-09-25

**Expanded evidence:** the [subsequent study](assembly64-expanded-study-2026-09-25.md)
adds a supplied ID-request exchange, a public-discovery announcement and provider
application enum mappings for 464. The earlier negative findings below apply to
this document's original corpus; the new evidence strengthens, but does not prove,
the unregistered-ID explanation.

**Subsequent protocol study:** [controlled GET/ALPN comparison](assembly64-protocol-study-2026-09-25.md)
tests the transport hypothesis with an honest Project CBM identity. HTTP/1.1 is
selected, HTTP/2-only TLS is refused, and the tested metadata variants still return
JSON464 while documentation returns200. Neither admission rejection nor a hidden
backend protocol fault is established. The no-probe statements below describe this
earlier reference-only audit; the later bounded tests have separate retained evidence.

The reviewed material establishes the protocol and two clients' implementation
choices. It does **not** establish a mandatory registration/permission process, nor
does it explain Project CBM's previously observed HTTP 464 responses. None of the
four access questions is completely resolved. Provider clarification remains useful
for those specific unknowns; it is not a newly discovered blanket permission rule.

This is documentation research only. No reference application or firmware was run,
no Assembly64 service query or hosted-title download was made, no foreign identity
or credential was used, and no message was sent. No Product/Menu implementation,
image, package, tag or physical qualification result changes.

## Scope, identities and limits

- Local Ultimate64 Manager: clean `main`, commit
  `a4e55f12d6a08c3a435b1d63ced1c3a2c6f461e8`, version `0.5.2`. GitHub `main`
  independently matched. Searched all 107 tracked files and all 250 locally
  reachable commits, including complete patches, all tracked documentation,
  README, license, workflows, network utilities and device call sites.
- Retrieved all available GitHub issue/PR bodies (182), issue comments (161), PR
  inline comments (6), and releases (43) with pagination. Assembly64 introduction
  PR132, search-fix PR151, improvements PR164 and network-errors PR175 have no
  submitted review records. No separate changelog is tracked. Discussions are
  disabled; the wiki URL redirects to the repository, with no separate wiki shown.
- Reviewed the official Elite II product page, documentation index, firmware
  history, project-status and external-links pages, then the complete checked-out
  official documentation tree at
  `2da134b31b548c56647ebcccf7ef9100cd155ee1`. The source clone has shallow history;
  this is not a claim to have examined every historical documentation revision.
- Extracted all 45 pages of the linked Elite II quick-start PDF; visually verified
  the relevant page 44. Reviewed Assembly64 integration, Wi-Fi, HTTP-target,
  firmware 3.15 and documentation-license material. Searched the other text pages.
- Retrieved the complete, non-truncated official firmware tree listing at
  `ef9937a73c7db391d5434bfda08e96216d7099cc`, then its seven Assembly64-specific
  implementation/header/test files. This is a pinned source inspection, not a
  firmware build or a claim about every historical firmware version.
- Rechecked the operator's public application page and searched the official
  domains for further Assembly64 access documentation. Used the already retained
  September 24 OpenAPI schema; no fresh service probe was necessary.

Negative findings apply to this accessible corpus. Private agreements, deleted
issues, unadvertised documents and server configuration are not observable here.
The exact retained evidence is under configured bulk storage at
`qualification/assembly64-reference-audit-2026-09-25`; `manifest.json` and its SHA-256
sidecar bind the source snapshots, public metadata, website captures and checks.
No source copy was installed into Project CBM or made a build dependency.

## A. EXPLICITLY DOCUMENTED

### Manager authors' statements

The [README at the inspected commit](https://github.com/sandlbn/ultimate64-manager/blob/a4e55f12d6a08c3a435b1d63ced1c3a2c6f461e8/README.md#L189)
thanks Fredrik Åberg for opening the Assembly64 API. More specifically,
[release v0.4.1](https://github.com/sandlbn/ultimate64-manager/releases/tag/v0.4.1)
describes use of the official API and thanks him for opening it “to us.” This is
explicit author attribution to provider cooperation. It does not contain the
operator's access agreement, a general grant to other clients, or a statement
requiring every client to apply.

The source module comment (`src/assembly64.rs:4`) calls its `client-id` header
required. Other comments recommend caching category/compo tables
(`:919`, `:986`) and sequential downloads to be gentle on the shared server
(`src/assembly64_browser.rs:1052`). These are client-author statements, not a
published numeric provider policy.

[PR151](https://github.com/sandlbn/ultimate64-manager/pull/151), linked from issue150,
reports that wildcard search syntax stopped working and changes to quoted phrases.
It supplies evidence of a compatibility change, not a promised notice period or
deprecation policy. The reviewed issues, comments, releases and historical code
contain no Assembly64 registration instructions, HTTP 464 explanation, numerical
rate limits, client terms or required attribution wording.

The [Manager license](https://github.com/sandlbn/ultimate64-manager/blob/a4e55f12d6a08c3a435b1d63ced1c3a2c6f461e8/LICENSE)
is MIT for its software. It does not state Assembly64 service access terms or grant
rights to all hosted content. Ultimate documentation's `notes/license.rst` concerns
copying that documentation under GFDL; it is likewise not an API access policy.

### Official Ultimate and operator documentation

The [Ultimate integration guide](https://1541u-documentation.readthedocs.io/en/latest/howto/assembly.html)
documents support from firmware 3.11, user searches, multi-file entries, downloading
and caching selected files in `/Temp`, dynamic presets, and voluntary donations
toward hosting. Its first-20-results and non-cleaning `/Temp` notes are explicitly
about 3.11; they are not provider rate or storage limits. The guide contains no
third-party registration flow or 464 definition.

The [official documentation index](https://ultimate64.com/documentation) links the
Elite II quick-start manual; page 44 lists Assembly 64 → New Search in the F5 menu.
The [firmware history](https://ultimate64.com/Firmware) describes embedded access
and later file viewing/copying improvements. The
[3.15 notes](https://1541u-documentation.readthedocs.io/en/latest/howto/release_3.15.html)
include Assembly64 browser memory fixes. None establishes Project CBM access terms.
The Ultimate device REST API and webshop registration are separate from Assembly64
service authentication; neither answers this question.

The [operator page](https://hackerswithstyle.se/assembly/) advertises its own desktop
application, local/online file operations and Ultimate integration, without supplying
the four missing third-party policy answers. The retained public OpenAPI describes
routes and an optional `client-id` header, but no global security scheme, 464 meaning,
registration, rates, attribution requirements or deprecation policy. See the
[hashed September 24 schema record](assembly64-access-2026-09-24.md).

## B. DIRECTLY OBSERVED IN CODE

### Complete Manager Assembly64 endpoint inventory

Base: `https://hackerswithstyle.se/leet`, `src/assembly64.rs:18`. All seven operations
use GET through the same helper at line 775; there is no separate login or token
endpoint in this path. Line numbers below refer to the pinned Manager commit.

| Operation | Path relative to base | `src/assembly64.rs` line |
| --- | --- | --- |
| Paged AQL search | `/search/aql/{offset}/{limit}?query={encoded_query}` | 793 |
| Entry files | `/search/entries/{item_id}/{category_id}` | 827 |
| File bytes | `/search/bin/{item_id}/{category_id}/{file_id}` | 851 |
| Search presets | `/search/aql/presets` | 869 |
| Categories | `/search/categories` | 921 |
| Entry metadata | `/search/meta/{item_id}/{category_id}` | 975 |
| Competition types | `/search/compotypes` | 988 |

Historical patches reveal no additional Assembly64 host or authentication endpoint.
The initial integration is commit `314a576`; later relevant changes include
`aa6b1dd` (search), `457735e` (browser improvements) and `51e721d` (folder handling).

### Headers, identifiers and credentials

| Item | Observed behavior and source |
| --- | --- |
| `client-id` | Fixed `u64manager`, `src/assembly64.rs:19,775–776`, attached to all seven operations |
| `User-Agent` | `ultimate64-manager/0.5.2` for this source version; browser lines 65,539 and `src/net_utils.rs:113–122` |
| Library default `Accept` | `*/*`, pinned reqwest 0.11.27 `src/async_impl/client.rs:167`; `Cargo.lock:4575` pins that version |
| Host / HTTP authority | Derived from the request URL by the HTTP transport, not a separate application identity |
| Redirect/proxy-dependent headers | Default reqwest redirects may add `Referer`; system proxy behavior remains enabled. Exact wire headers depend on redirects, protocol and environment; no wire trace was collected |
| Cookies | Cargo enables cookie support, but this client never enables a cookie store; reqwest initializes it to `None` at line 223 |
| Authorization, API keys, tokens, device IDs | No Assembly64 bearer/basic authorization, API key, signing secret, client certificate, login/session bootstrap, serial/MAC/unique device identifier, or per-user credential is constructed or passed in the reviewed path |

Only the first two headers are explicitly configured by Manager for Assembly64.
No explicit Content-Type, Accept-Encoding or service-specific header beyond those
is added by that application path. Library/transport defaults must not be mistaken
for extra provider credential requirements. No inherited browser cookie is supplied.

`src/net_utils.rs:125–134` adds `X-password` for **Ultimate device** operations.
Device discovery identifiers and device configuration retries are also separate.
The browser update function receives optional device connection/password arguments,
but metadata/search/download clients are created using only its User-Agent;
device credentials are used for later device actions, not Assembly64 requests.

Separate adjacent network behavior: `src/csdb_screenshots.rs:17,36–55` requests
`https://csdb.dk/webservice/?type=release&depth=1&id={id}`, then the returned screenshot
URL, using the Manager User-Agent and a 15-second external client
(`src/assembly64_browser.rs:1539`). It does not attach the Assembly64 `client-id`.
`src/assembly64.rs:130–134` constructs browser links to
`https://csdb.dk/release/?id={item_id}`. These are CSDb operations, not additional
Assembly64 endpoints; no CSDb request or scraping was performed in this audit.

### Errors, retries, backoff, rates and caches

- `src/assembly64.rs:801–807` treats **463** as an AQL syntax error. **464** is
  returned as the generic non-success HTTP error, as are other non-2xx statuses
  on the metadata/download routes. No special 464 or 429 handling, Retry-After
  interpretation, automatic client registration, or identity fallback exists.
- No application-level automatic retry/backoff or numeric request-rate limiter
  is present for Assembly64. Reqwest itself can retry certain reusable HTTP/2
  transport failures up to twice (`client.rs:2195–2277`); these are not retries of
  HTTP 464 responses and are not provider policy.
- Defaults: 100 search results per page (`assembly64.rs:20`); 30-second external
  client timeout (`:769–771`). The browser adds a 120-second outer download timeout
  (`assembly64_browser.rs:62,3170–3186`), without replacing the client's 30 seconds.
- Download All awaits files sequentially, checks cancellation between files, and
  records failures while continuing with subsequent files (`:1052–1082`). It does
  not retry the failed file. This is not a global concurrency guarantee: metadata
  refresh batches three tasks (`:609–640`), and initial tab entry also starts search
  (`src/main.rs:956–967`). No minimum inter-request delay is specified.
- Presets/categories/compo types persist in local JSON caches (`:220–301`), with
  cached/baseline fallback on refresh failure (`:642–699`). The successful-preset
  flag suppresses subsequent refreshes within that browser state. No provider TTL,
  ETag/conditional-cache policy or numerical download-size policy is implemented;
  downloaded bytes are read into memory. Local settings/favorites are not API keys.

### Official Elite II / Ultimate firmware comparison

Pinned [official firmware implementation](https://github.com/GideonZ/1541ultimate/blob/ef9937a73c7db391d5434bfda08e96216d7099cc/software/network/assembly.cc)
uses `hackerswithstyle.se` port **80**, with four GET route families:
`/leet/search/aql?query=...`, `/leet/search/aql/presets`,
`/leet/search/entries/{id}/{category}`, and `/leet/search/bin/{id}/{category}/{index}`
(also a path/optional-filename overload for the binary route). See lines 7–12,
121–139,170–188,207–235. This is an implementation observation, not a proposed
change from Project CBM's HTTPS design.

All four request builders explicitly send the same five headers:
`Accept-encoding: identity`, `Host: hackerswithstyle.se`,
`User-Agent: Assembly Query`, `Client-Id: Ultimate`, `Connection: close`
(lines 83–90,128–134,178–184,225–231). No token or unique device identifier is
embedded in those requests. There is a local `U64==2` board-state condition before
connection (35–39); it does not transmit a device identity. No 464 explanation or
provider rate/backoff policy appears in the inspected Assembly64 files. Presets
are reused in memory (92–94). Test helpers' retries concern device REST calls,
not documented permission or retry rules for Assembly64.

The official HTTP-target documentation's `commoserve.files.commodore.net/leet/search/bin`
example (`uci/http_target.rst:199`) illustrates a generic device HTTP facility. It
does not establish that host as a current supported alternate Project CBM endpoint.
Neither that host nor the firmware identity was tried.

## C. INFERRED

1. These clients use simple client-name identification rather than an exposed
   per-device credential exchange for the inspected requests. This makes an
   honest Project CBM implementation technically plausible; it does not demonstrate
   what the server will accept or why it previously returned 464.
2. The Manager release acknowledgment supports cooperation with the provider.
   An allowlist, private approval agreement, mandatory registration, hardware-only
   restriction or transferable access entitlement cannot be inferred from it.
3. Sequential downloads and cache comments suggest load-conscious client design.
   They supply reasonable design examples, not numerical provider limits.
4. The reported search syntax change shows that integration compatibility can
   change. It does not establish a contractual API stability or notice policy.

The earlier access table's phrase **“own admitted identity” was too strong**.
The supported wording is **“its own fixed identity, with an author acknowledgment
of provider cooperation.”** Likewise, no reviewed source says that contacting the
provider is itself mandatory. The actual reason for further clarification is the
unexplained rejection of Project CBM's honest identity and missing operating policy.

## D. STILL UNKNOWN — the four questions

| Original question | What the references answer | What still needs provider confirmation, and why |
| --- | --- | --- |
| 1. Supported third-party use and access method | Public protocol, concrete HTTPS routes, working-client implementation and cooperation acknowledgment | Whether the proposed independent Project CBM client/use is supported; which base/routes are supported for it; whether any registration/authentication is required. Client code cannot expose server-side admission policy or unpublished agreements. |
| 2. Project CBM identity and HTTP 464 | Header name, Manager/Ultimate identity strings, generic handling of 464 | The honest Project CBM client identifier/header requirements; exact meaning/cause and response to the two retained 464s. Neither another client's string nor an optional OpenAPI parameter explains the rejection. |
| 3. Operating limits | Client-selected page size, timeouts, caches and sequential file downloads | Provider rate/concurrency limits, cache expectations/TTL, download/size bounds and retry/backoff rules. Implementation choices are not documented quotas or guarantees. |
| 4. Attribution, terms and change policy | Existing credits, optional donation link, software/documentation licenses, a past compatibility fix | Required attribution/links/notices, applicable third-party service terms and API-change/deprecation channel/notice. Software licenses and acknowledgments do not state these service obligations. |

An authoritative public provider statement could answer these without private
contact. None was found in the exhausted accessible references above. Accordingly,
the [unsent inquiry](assembly64-provider-inquiry.md) remains a way to resolve these
specific questions, not proof that permission-seeking is universally required.
The accepted Project CBM Online Library gate stays unresolved. Physical USB testing
of private attempt18 proceeds independently; no outcome is inferred from the
owner's statement that testing is in progress.
