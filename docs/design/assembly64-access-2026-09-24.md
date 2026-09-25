# Assembly64 access reconnaissance — 2026-09-24

**Gate: UNRESOLVED. No Online Library network client is implemented.** USB work
continues independently. This addendum supplements the accepted
[design study](content-ingestion-online-library.md); it does not replace it.

## Qualification-preparation review

**September 25 correction:** the subsequent
[reference/Elite II audit](assembly64-reference-audit-2026-09-25.md) exhausts the
accessible local code/history, public issues/releases and official documentation.
The historical phrase “own admitted identity” below overstates the evidence: the
Manager uses a fixed identity and its author acknowledges provider cooperation.
No source establishes mandatory registration or contact for every third-party
client. Project CBM's observed 464 and the four specific operating-policy questions
remain unresolved; provider clarification is useful for those reasons.

The legitimate next step is an owner-sent inquiry to the published API Support
contact. A [concise technical draft](assembly64-provider-inquiry.md) is prepared;
it has not been sent. USB image/qualification preparation does not open the network
implementation gate. The official Ultimate guide and operator page were reviewed
again; neither resolves third-party client admission. The web reader could not
reopen the schema, so schema facts below remain attributed to the retained, hashed
September 24 retrieval, not a claimed fresh response. No service probe was repeated.

| Subject | Established source fact | Still unknown |
| --- | --- | --- |
| Public schema | OpenAPI 3.1.0, API version 1.0, publicly linked Swagger documentation | Public third-party use/admission terms |
| Service endpoints | HTTPS base `https://hackerswithstyle.se/leet/`; `/search/aql/{offset}/{limit}`, `/search/aql/presets`, `/search/categories`, `/search/entries/{itemId}/{categoryId}`, `/search/meta/{id}/{category}`, `/search/compotypes`, `/search/bin/{itemId}/{categoryId}/{fileId}` documented | Which routes Project CBM may use, API change/deprecation expectations |
| HTTP 464 | Two prior metadata requests with honest study identity received 464; schema does not document it | Meaning, cause, retry expectations; it is not proven to mean registration or hardware admission |
| Client identity | Search schema describes optional `client-id`; reference Manager uses its own admitted identity | Project CBM's accepted ID, registration/authentication and identification requirements |
| Usage | No rate/usage policy found in reviewed schema/docs | Rate/concurrency limits, caching, download/size limits and backoff |
| Attribution | Project design proposes “Powered by Assembly64” | Whether that wording/link/notices satisfy provider requirements |
| Third-party expectations | Reference Manager thanks the provider for API access | Permission or supported access process for another client; service stability commitment |
| Contact | Schema's API Support email is `freabe@gmail.com` | Response/admission guidance; no contact has been made |

Endpoint documentation is not an access grant. No foreign client ID, Swagger default
identity, private token, circumvention, content download or CSDb scraping is used.

## Source facts

The local Ultimate64 Manager reference remains commit
`a4e55f12d6a08c3a435b1d63ced1c3a2c6f461e8`. Its README thanks Fredrik Åberg for API
access and links the provider's [Swagger UI](https://hackerswithstyle.se/leet/swagger-ui/index.html).
Its endpoint, search, metadata, file/download, error-handling and client-identity
observations in the accepted design still match the local source. No code was copied.

The provider's publicly linked Swagger initializer points to its configuration,
which points to the [OpenAPI schema](https://hackerswithstyle.se/leet/v3/api-docs).
Read-only documentation requests with User-Agent `Project-CBM/1.2-access-research`
succeeded. No content/metadata service query, foreign client ID, credentials,
registration request, provider message or hosted-title download was made.

The retrieved schema identifies an HTTPS production base and API version 1.0.
It documents paged AQL search, presets, categories, release file listings, metadata,
competition types and binary-file routes. Search operations describe a `client-id`
header, optional in the schema, with the Swagger UI's own default. That default was
not used as a Project CBM identity. API Support contact: **freabe@gmail.com**.

There is no global security scheme, documented HTTP 464 response, explicit third-party
client registration procedure, rate limit, attribution requirement or stability
commitment in this schema. These absences do not prove unrestricted service access.
The earlier two HTTP 464 observations remain unresolved and were not repeated.

The [official Ultimate guide](https://1541u-documentation.readthedocs.io/en/latest/howto/assembly.html)
still documents search and release/file navigation, including multi-file entries.
The [operator page](https://hackerswithstyle.se/assembly/) describes its own application;
it does not supply the missing client admission terms. A schema's metadata image
fields are not permission to fetch arbitrary URLs or introduce CSDb scraping.

Retained documentation: `qualification/content-1.2-development-2026-09-24` under
configured bulk storage. `assembly64-openapi.json`: 41,034 bytes; SHA-256
`72529a92d0b1753ba8c768a61528ff638c52968c85eed2ab11e98ad680dd1846`.
The accompanying research JSON records endpoint/schema facts. One sandbox request
could not resolve DNS; an authorized documentation retry succeeded. That transient
host observation does not establish appliance Internet behavior.

## Inferences and next step

A public schema establishes useful protocol facts, but its optional-header annotation
does not resolve the observed rejection of an honest CBM client identity. It is
inappropriate to infer admission from another client's working identifier or from
missing security annotations. The access gate therefore remains closed.

Provider guidance should confirm: the accepted Project CBM client identifier and any
registration; permitted third-party use; 464/error meanings; rate, caching and download
limits; attribution; and API change expectations. The listed API Support address is
a concrete contact path. Sending a message requires separate instruction; none was
sent. No owner decision is required to continue USB development. Enabling Online
Library remains conditional on evidence satisfying the accepted access gate.
