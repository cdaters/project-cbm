# Assembly64 third-party access inquiry — draft, not sent

To: **freabe@gmail.com** (API Support in the retained provider OpenAPI schema)

Subject: Project CBM: supported third-party Assembly64 client access

Hello Fredrik / Assembly64 API Support,

Project CBM is an open-source Raspberry Pi Commodore appliance. We would like to
offer an optional, user-initiated **Online Library — Powered by Assembly64**, letting
users search the service and save selected files into their local library.

Project CBM would not bundle or redistribute Assembly64-hosted titles in its image
or repository. Searches and downloads would be initiated by the user. We want to
identify Project CBM honestly and follow your supported third-party access model.

During a small design study, metadata requests to `/leet/search/aql/presets` and
`/leet/search/categories`, using `client-id: project-cbm-design-study`, returned
HTTP 464. We have not attempted to bypass that response or download hosted titles.
We found the public Swagger/OpenAPI documentation but could not establish the
client admission requirements or the meaning of 464.

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

The address is a published API Support contact, not inferred from a personal account.
Its source is the [provider schema](https://hackerswithstyle.se/leet/v3/api-docs),
retained with an exact hash in the [access findings](assembly64-access-2026-09-24.md).
The owner may edit and send this draft. Nothing has been sent automatically.
Retain any reply privately first, then record the applicable guidance with permission
and source/date attribution. A support reply must resolve the accepted access gate;
the mere existence of an email address or public schema does not open it.
