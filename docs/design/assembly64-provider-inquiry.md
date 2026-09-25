# Assembly64 client ID request — current Discord draft, not sent

Based on the [expanded reference study](assembly64-expanded-study-2026-09-25.md),
the supplied June 14 Discord exchange supports sending Scooby a DM with the desired
ID. The following is the current short draft; the earlier diagnostic email remains
below as historical context. No message has been sent.

> Hi Scooby! I’m developing Project CBM, an open-source Raspberry Pi Commodore
> appliance, and would like to register `project-cbm` for its optional Online
> Library: user-initiated AQL search and selected downloads, with Assembly64
> attribution. Could you allocate that ID? Our own unregistered study ID returns
> JSON `errorCode: 464`; is that expected? Does the registered ID cover search,
> downloads and `/leet/homeserver/all-public-servers` without a user token?
> Please also confirm rate/concurrency limits, caching guidance and required
> attribution/terms. We won’t bundle hosted titles.
> https://github.com/cdaters/project-cbm
> Thanks!

---

# Assembly64 third-party access inquiry — draft, not sent

To: **freabe@gmail.com** (API Support in the retained provider OpenAPI schema)

Subject: Project CBM: diagnosing HTTP 464 on documented Assembly64 GET endpoints

Hello Fredrik / Assembly64 API Support,

Project CBM is an open-source Raspberry Pi Commodore appliance. We would like to
offer an optional, user-initiated **Online Library — Powered by Assembly64**, letting
users search the service and save selected files into their local library.

Project CBM would not bundle or redistribute Assembly64-hosted titles in its image
or repository. Searches and downloads would be initiated by the user. We want to
identify Project CBM honestly and follow your supported third-party access model.

Metadata GETs to `/leet/search/aql/presets` and `/leet/search/categories`, using
`client-id: project-cbm-design-study` and
`User-Agent: Project-CBM/1.2-access-research`, return JSON containing `errorCode: 464`
and a timestamp. We investigated transport compatibility first: forced HTTP/1.1,
no ALPN, an HTTP/2 offer (the server selects HTTP/1.1), HTTP and HTTPS, identity
encoding/Connection close, and Accept `*/*` versus `application/json` all produced
464. An HTTP/2-only TLS offer was refused with `no application protocol`.

The same-identity HTTP/1.1 GET to `/leet/v3/api-docs` succeeds and documents ordinary
GET/JSON for both metadata endpoints. One presets response timestamp is
`1790324727798` (2026-09-25 around 08:25:27 UTC). Which component produces this JSON
464, what condition does it represent, and is there a protocol/routing or documented
request requirement we are missing? We are not assuming it means rejected client
admission. No foreign identity/credential or hosted-title download was used.

Could you confirm:

- Whether this third-party use is supported, and the supported API/base URL or
  other access method, including any registration or authentication process?
- Which client identification/header values Project CBM should use, and what
  HTTP 464 means in this context?
- Rate/concurrency limits, caching expectations, download/size limits, and retry
  or backoff guidance?
- Required attribution, links or notices, any applicable third-party client terms,
  and how clients should track API changes or deprecation?

We will keep the integration disabled until the access expectations are clear.
Thank you for your guidance.

Project CBM
https://github.com/cdaters/project-cbm

## Basis and handling

The [controlled protocol study](assembly64-protocol-study-2026-09-25.md) supplies
the technical reproduction above. The immediate question is diagnosis of the actual
error; the broader questions remain separate and do not prejudge its cause.

The [September 25 reference and Elite II audit](assembly64-reference-audit-2026-09-25.md)
found concrete protocol details and acknowledged provider cooperation with Manager,
but no documented mandatory registration process. The four questions above remain
partially unanswered; this draft seeks clarification of the actual 464 response and
missing policy, without assuming that all clients must request permission.

The address is a published API Support contact, not inferred from a personal account.
Its source is the [provider schema](https://hackerswithstyle.se/leet/v3/api-docs),
retained with an exact hash in the [access findings](assembly64-access-2026-09-24.md).
The owner may edit and send this draft. Nothing has been sent automatically.
Retain any reply privately first, then record the applicable guidance with permission
and source/date attribution. A support reply must resolve the accepted access gate;
the mere existence of an email address or public schema does not open it.
