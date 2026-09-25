# Assembly64 HTTP 464 protocol investigation — 2026-09-25

**Result: reproduced; cause unresolved.** Treat 464 as an unexplained endpoint
failure, not evidence of rejected client admission. The bounded protocol tests
below did not identify a client-side HTTP-version, method, compression or Accept
correction. Nor did they establish a gRPC requirement. The tested public TLS
endpoint selects HTTP/1.1 and refuses an HTTP/2-only ALPN offer.

This follows the owner's instruction to investigate transport compatibility before
assuming admission requirements. It supersedes causal implications in earlier
research, while preserving all original observations and evidence. It does not
implement Online Library or change a private/stable image, package or tag.

## Method and reference equivalence

At 08:25–08:27 UTC, sent eight sequential GET requests: seven to the two previously
tested metadata endpoints and one to the public OpenAPI document. Also performed
one TLS handshake offering only HTTP/2, with no application request. No automatic
retries, POSTs, content downloads or provider messages occurred.

Every GET used the same honest identity:

```text
User-Agent: Project-CBM/1.2-access-research
client-id: project-cbm-design-study
```

No Manager, Ultimate or Swagger identity was used. No token, cookie, Authorization
header, device identifier, client certificate or copied credential was supplied.
Certificate/hostname verification remained enabled for HTTPS. The firmware-style
cleartext HTTP comparison sent only the public metadata request and honest labels;
it is not a proposed product transport downgrade.

Manager at `a4e55f12d6a08c3a435b1d63ced1c3a2c6f461e8` uses GET, no request body,
the same HTTPS host/path, `Accept: */*` through reqwest, and its own UA/client-id.
Sources: `src/assembly64.rs:775–776,868–875`,
`src/net_utils.rs:113–122`, `src/assembly64_browser.rs:539`,
`Cargo.toml:31`, `Cargo.lock:4575`. See the
[full reference audit](assembly64-reference-audit-2026-09-25.md).

Reqwest 0.11.27's default TLS features do not themselves include
`native-tls-alpn`; that is a separate feature. Its ALPN configuration is conditional
on that feature (`src/async_impl/client.rs:344–357`). Manager's direct dependency
does not explicitly request it. We tested both no-ALPN HTTP/1.1 and an offer of
`h2,http/1.1`, without assuming the feature composition of a distributed binary.
These are equivalent application/protocol semantics with a different honest
identity, not a claim of byte-identical TLS fingerprints or execution of Manager.

The official firmware at `ef9937a73c7db391d5434bfda08e96216d7099cc` uses HTTP/1.1,
port 80, `Accept-encoding: identity`, `Connection: close` and no Accept header.
Its request shape was reproduced with Project CBM identification. See
`software/network/assembly.cc:7–12,83–90` in the retained reference evidence.

Tooling: macOS curl 8.7.1 with HTTP/2/nghttp2 support; Python verified TLS sockets
for the no-ALPN request and HTTP/2-only handshake. Curl configuration loading was
disabled. No proxy environment variables were present. Curl commands, TLS traces,
request/response headers, bodies, timestamps, versions and hashes are retained
privately. Requests had bounded connection/read duration and response size; redirects
were not followed, and none was returned. No runtime or builder was started.

## Observed results

`presets` below means `/leet/search/aql/presets`; the hostname is always
`hackerswithstyle.se` with matching Host/SNI and no endpoint/IP substitution.

| Case / retained record prefix | Request variation | Actual result |
| --- | --- | --- |
| `presets-http1` | HTTPS GET, forced HTTP/1.1, Accept `*/*` | HTTP/1.1 464 |
| `presets-http2` | HTTPS GET, HTTP/2 offered with HTTP/1.1 fallback | Server selects HTTP/1.1; HTTP/1.1 464 |
| `h2-only-tls` | TLS ALPN offers only `h2`; no HTTP request | TLS alert `no application protocol` |
| `firmware-http-semantics` | HTTP port 80 GET; identity encoding, close connection, no Accept | HTTP/1.1 464 |
| `https-identity-encoding` | Same firmware header semantics over HTTPS | HTTP/1.1 464 |
| `categories-http1` | HTTPS GET `/leet/search/categories`, Accept `*/*` | HTTP/1.1 464 |
| `schema-control` | HTTPS GET `/leet/v3/api-docs`, same UA/client-id/Accept | HTTP/1.1 200; valid OpenAPI JSON |
| `presets-no-alpn` | HTTPS HTTP/1.1 GET without ALPN; Manager-style headers | HTTP/1.1 464 |
| `presets-accept-json` | HTTPS HTTP/1.1 GET, Accept `application/json` | HTTP/1.1 464 |

All seven metadata errors are 43-byte JSON objects containing only `errorCode: 464`
and a changing numeric `timestamp`. Responses identify
`Server: nginx/1.24.0 (Ubuntu)` and `Content-Type: application/json`. They provide
no explanatory message, `WWW-Authenticate`, `Retry-After`, redirect, or protocol
upgrade instruction. This does not identify which application/proxy layer generated
the JSON or expose any backend load-balancer configuration.

The response CORS list permits headers including `token` and `client-id`, and
methods including GET, POST and OPTIONS. A CORS allow-list is not a requirement to
send a token or to replace a documented GET with POST. No speculative gRPC/POST
request was needed to reproduce either reference client.

## Documented endpoint requirements

The fresh [OpenAPI response](https://hackerswithstyle.se/leet/v3/api-docs) is byte-for-byte
identical to the September 24 retained schema: 41,034 bytes, SHA-256
`72529a92d0b1753ba8c768a61528ff638c52968c85eed2ab11e98ad680dd1846`.
Both metadata operations document **GET**, an optional `client-id` header and JSON
results. Neither declares a required request body/query parameter, operation
security requirement, gRPC framing or HTTP/2 requirement. There is no global
security scheme or documented 464 explanation. All tested requests match those
published operation requirements. Documentation success does not prove metadata
access, but it supplies a control using the same host, TLS, HTTP version and identity.

[IANA](https://www.iana.org/assignments/http-status-codes/) leaves 452–499 unassigned.
Consequently, 464 has no universal standardized cause.
[AWS ALB documentation](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-troubleshooting.html#http-464-issues)
does define its own 464 as a request/target-protocol incompatibility, including
HTTP/1.1 to HTTP/2 or gRPC targets and non-POST HTTP/2 requests to gRPC targets.
That made protocol negotiation a useful hypothesis to test. It does **not** establish
that this nginx-fronted service uses ALB or that its JSON 464 has AWS's meaning.
The backend may include invisible intermediaries; response headers cannot rule
those in or out. No provider-specific 464 definition was found in the reviewed
public documentation or reference code.

## Conclusions and remaining uncertainty

| Hypothesis | Evidence-supported conclusion |
| --- | --- |
| Merely enable HTTP/2 at the client | No supported fix demonstrated: the public TLS endpoint selects HTTP/1.1 and refuses an HTTP/2-only ALPN handshake. A negotiated HTTP/2 service response was therefore not available for comparison. |
| Reference client secretly requires HTTP/2 | No evidence: Manager's default feature path need not offer ALPN, firmware explicitly uses HTTP/1.1, and both corresponding request forms reproduce 464 with the honest CBM identity. |
| Wrong HTTP method / gRPC request expected | GET is the published and reference method; the published operations return ordinary JSON. No evidence supports changing them to POST/gRPC. Hidden backend misconfiguration is not excluded. |
| HTTPS versus HTTP, compression, keep-alive, Accept or ALPN difference | The bounded variants above did not change the metadata result. This is not an exhaustive test of every possible TLS/client fingerprint or network path. |
| Missing documented parameter/header/body | None identified in the current schema; the optional client-id was supplied honestly. No unstated credential requirement is inferred from the CORS header list. |
| Client admission rejection | Not established. Identity values were held constant, and no server-side policy/logs or explanatory error were available. The 464 observations alone cannot establish this cause. |

The most specific remaining technical question is: **which component returns
`{"errorCode":464,"timestamp":...}` for these documented GETs, and what condition
does that component mean by 464?** A backend trace/configuration or provider error
definition could distinguish routing/protocol misconfiguration, an undocumented
request requirement, application validation, or a service policy. This is a request
for diagnosis, not an assumption that Project CBM needs admission permission.

A precise example for correlation is the HTTPS presets HTTP/1.1 GET at response
timestamp `1790324727798` (2026-09-25 around 08:25:27 UTC), with the two honest
identification headers above and `Accept: */*`. No message has been sent. The
[inquiry draft](assembly64-provider-inquiry.md) now points to this technical evidence.

## Evidence and preservation

New evidence is at `qualification/assembly64-protocol-study-2026-09-25` under
configured bulk storage. `results.json` binds the eight request results to body
hashes; `schema-requirements.json` records the two operation contracts. The original
September 24 observations and September 25 reference audit are unchanged externally.
`manifest.json` and its SHA-256 sidecar seal the new evidence.

Additive source recovery is `archive/assembly64-protocol-study-2026-09-25`, with
bundle verification and offline restore/ref/peeled-tag/fsck checks. Independent
custody remains outstanding. Physical attempt18 testing is unaffected; no new
physical result or public release/support claim is made.
