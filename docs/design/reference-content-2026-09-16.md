# Optional SID/demo reference content

Research date: **2026-09-16**. Metadata and author statements, not media acquisition
or playback qualification. All 17 requested works are **OWNER-SUPPLIED** at this
checkpoint: no sufficient Project CBM redistribution permission was established in
the reviewed sources. This is an admission decision, not a claim that all personal
use is prohibited. [User guide](../runtime/reference-content.md),
[structured findings](reference-content-catalog.json),
[separate application integration](../runtime/optional-applications.md).

## Rights policy

| Class | Project CBM action |
| --- | --- |
| BUNDLED | Project CBM-owned or explicit redistribution-cleared bytes; retain grant, notices, exact hashes and frozen input identity. |
| OPTIONAL ACQUISITION | Rights permit the intended acquisition arrangement; retain source/terms. An upstream link alone does not authorize a downloader or redistribution. |
| OWNER-SUPPLIED | Owner obtains content they may lawfully use. Project CBM provides folder/launch guidance and source references, not the copyrighted bytes. |

The [current HVSC copyright notice](https://www.hvsc.c64.org/info#copyright) says
music remains copyrighted and HVSC cannot license it generally. Named composers
and historical publisher credits need not identify today's rights holder. Permission
given to HVSC does not establish a sublicense to Project CBM. Its FAQ's informal
public-domain wording and archive mirror availability are not per-work grants.
Use the copyright notice unless a rights holder supplies separate explicit terms.

CSDb/scene.org are useful release registries/archives, not automatic license
sources. For every work below, source-page links may identify where the owner can
review/acquire the release under applicable terms; **none is approved for automatic
Project CBM acquisition or embedding**. No author was contacted on the owner's behalf.
Future clearance must cover the chosen version, music/compositions, code, artwork,
examples and any documentation actually distributed. Keep the evidence externally
and a concise reviewed license inventory in source. Never substitute availability,
a checksum, freeware wording or private-candidate status for permission.

## Current HVSC identities

[HVSC #85](https://www.hvsc.c64.org/downloads), dated June 28, 2026, was current
on the research date; its version API also returned 85. The following paths were
verified using individual records from HVSC's own public metadata service. Prefix
each relative path below with `/MUSICIANS/`. Every listed record declares **PAL**;
NTSC compatibility was not established. Models are metadata expectations, not
physical chip/fidelity test results. Subtune numbers use HVSC's one-based display.

| Title | Composer credited by HVSC | Path / metadata record | Format | SID model/address | Subtunes / default |
| --- | --- | --- | --- | --- | --- |
| Donkey Kong | Sascha Zeidler (Linus) | `L/Linus/Donkey_Kong.sid` ([136867](https://www.hvsc.c64.org/api/v1/sids/136867)) | PSID v2 | 8580; one SID | 1 / 1 |
| Legend Intro | Martijn Schutten | `S/Schutten_Martijn/Legend_Intro.sid` ([107971](https://www.hvsc.c64.org/api/v1/sids/107971)) | PSID v2 | unspecified; one SID | 1 / 1 |
| Ode to C64 | Søren Lund (Jeff) | `J/Jeff/Ode_to_C64.sid` ([116552](https://www.hvsc.c64.org/api/v1/sids/116552)) | PSID v2 | 6581; one SID | 1 / 1 |
| Turbo Outrun | Jeroen Tel | `T/Tel_Jeroen/Turbo_Outrun.sid` ([118540](https://www.hvsc.c64.org/api/v1/sids/118540)) | RSID v2 | 6581; one SID | 12 / 1 |
| Commando | Rob Hubbard | `H/Hubbard_Rob/Commando.sid` ([149387](https://www.hvsc.c64.org/api/v1/sids/149387)) | PSID v2 | 6581; one SID | 19 / 1 |
| Ghosts'n Goblins | Mark Cooksey | `C/Cooksey_Mark/Ghosts_n_Goblins.sid` ([156371](https://www.hvsc.c64.org/api/v1/sids/156371)) | PSID v2 | 6581; one SID | 2 / 2 |
| Delta | Rob Hubbard | `H/Hubbard_Rob/Delta.sid` ([104524](https://www.hvsc.c64.org/api/v1/sids/104524)) | PSID v2 | 6581; one SID | 13 / 12 |
| The Last Ninja | Ben Daglish & Anthony Lees | `D/Daglish_Ben/Last_Ninja.sid` ([140487](https://www.hvsc.c64.org/api/v1/sids/140487)) | PSID v2 | 6581; one SID | 11 / 3 |
| RoboCop 3 | Jeroen Tel | `T/Tel_Jeroen/RoboCop_3.sid` ([145743](https://www.hvsc.c64.org/api/v1/sids/145743)) | PSID v2 | 8580; one SID | 20 / 1 |
| Singularity | Carsten Berggreen (Scarzix) | `S/Scarzix/Singularity_2SID.sid` ([131839](https://www.hvsc.c64.org/api/v1/sids/131839)) | PSID v3 | 8580 + 8580; D420 | 1 / 1 |
| Last Party | Sylwester Hasiak (Buddha) | `B/Buddha/Last_Party_2SID.sid` ([124290](https://www.hvsc.c64.org/api/v1/sids/124290)) | PSID v3 | 8580 + 8580; D500 | 1 / 1 |
| Hardtek Jam | Michael (Nobody) | `N/Nobody/Hardtek_Jam_2SID.sid` ([135664](https://www.hvsc.c64.org/api/v1/sids/135664)) | PSID v3 | 8580 + 8580; D420 | 1 / 1 |
| A Pointless Quest | Aidan Crouzet-Pascal (acrouzet) | `A/Acrouzet/A_Pointless_Quest_2SID.sid` ([150087](https://www.hvsc.c64.org/api/v1/sids/150087)) | PSID v3 | 8580 + 8580; D420 | 1 / 1 |
| Rondo Droidissimo | Zack Maxis (manganoid) | `M/Manganoid/Rondo_Droidissimo_2SID.sid` ([157745](https://www.hvsc.c64.org/api/v1/sids/157745)) | PSID v3 | 8580 + 8580; D420 | 1 / 1 |

No payload SHA-256 is available because no SID bytes were acquired. API IDs are
observed lookup identities, not permanent content hashes. A later authorized test
must verify the actual file/header and hash. PSID/RSID are SID-player containers,
not ordinary C64 executables. [HVSC's format specification](https://www.hvsc.c64.org/download/C64Music/DOCUMENTS/SID_file_format.txt)
defines chip-address/version semantics; a stray model flag without a valid second
address does not establish a second SID.

Disambiguation: Linus here is **Sascha Zeidler**, not Linus Åkesson/lft. The requested
Legend Intro is Schutten's exact SID above; a similarly named demo using Compo Tune
is not equivalent. Legend Intro's model is unspecified. Turbo Outrun is **RSID**.
Old game publisher credits are recorded in JSON as historical attribution, not a
verified chain of current copyright ownership.

## Dual-SID variants: do not normalize away differences

- **Singularity:** [Scarzix's release](https://csdb.dk/release/?id=135891), 2015.
  His [own recording description](https://soundcloud.com/scarzix/singularity-upload-v2)
  identifies two 8580s and added recording reverb. That processed recording is not a
  raw SID fidelity oracle or a redistribution grant. HVSC's version uses D420.
- **Last Party:** [Buddha / Vulture Design, 2013](https://csdb.dk/release/?id=120196).
  Current HVSC uses **D500**. CSDb separately lists `Last_Party-d420_2SID.sid`
  (internal file 118585) and a D420 PRG. These are distinct candidates, not a reason
  to relabel the HVSC file. Verify the chosen header/hash later.
- **Hardtek Jam:** [Nobody / mozArt, 2014](https://csdb.dk/release/?id=127557).
  Author comments specify D420; PRG and D64 are also listed. Their bytes and rights
  are not interchangeable with the HVSC SID.
- **A Pointless Quest:** [acrouzet / Genesis Project, 2022](https://csdb.dk/release/?id=224390).
  Author specifies D420. The release's `A_Pointless_Quest_Mono_2SID.sid` name reminds
  us that two chips do not necessarily imply left/right stereo presentation.
- **Rondo Droidissimo:** [Manganoid, Hokuto Force / TempesT, 2025](https://csdb.dk/release/?id=257861).
  Separate D420 and D500 PRG/SID variants exist; author specifies two 8580s. It is a
  medley adapting La Serenissima (Rondò Veneziano) and Droid (Automat), so clearance
  needs underlying composition rights too. HVSC selects D420.
- **Dragon Fighter: Into the Depth:** [Bansai, 2024](https://csdb.dk/release/?id=247170&show=notes).
  Listed files: `df-itd-d420.prg` and
  `Dragon_Fighter_Into_The_Depth_(NES)_2SID.sid`. Author notes describe a C64 port
  of Iku Mizutani's Natsume player, D420, 50 Hz timing adjustments and mono or at
  least 50% stereo crossmix. Exact SID models and original composition ownership
  remain unresolved. Source is linked, but source availability is not licensing.
  No path was established by the current HVSC title query; this is not an exhaustive
  assertion of absence from every archive/alias.
- **Samar 2 SID Music $D420:** [CSDb 219599](https://csdb.dk/release/?id=219599),
  `2-Sid-Music-$D420-SAMAR.d64`. Credits: Data, JCH, Kozaki Soft, Leming, Phobos,
  Randy and Rayden. CSDb lists 11 tunes; this is a collection, not one composition.
  Advertised D420 does not establish each track's SID model/clock or clear all tune,
  arrangement/player/artwork rights. Exact release date, per-track headers and
  current HVSC equivalents remain unverified. Keep the disk identity distinct
  from individually ripped SID files.

## Wonderland XIV

**Censor Design, C64, X 2023**, [CSDb 232980](https://csdb.dk/release/?id=232980).
[Demozoo credits](https://demozoo.org/productions/324783/) identify LMan's project
lead/storyboard, a large code/art team, music by LMan, Magnar, Makke, psych858o and
Swallow, and Bitbreaker's loader. Record full credits by reference. CSDb dates the
release June 4; Demozoo says June 3. The event/release identity is clear; the day
remains discrepant.

The [scene.org archive preview](https://files.scene.org/view/parties/2023/x23/demo/wonderland_14.zip)
lists `wonderland_xiv_s1.d64` through `wonderland_xiv_s4.d64` (192 KiB displayed
per side), in a 751,073-byte ZIP. CSDb's archive is named `Wonderland_14-Censor.zip`.
No byte-equivalence or SHA-256 was established between archives. Preserve all four
sides; do not trim disk geometry or mistake four sides for four simultaneous drives.

[Swallow's July 2023 technical note](https://csdb.dk/release/?id=232980&show=trivia)
recommends the specific historical WinVICE 2.4.29-r31587 C64C setting for intended
sample quality and describes a last-disk SID-quality display. This is dated creator
evidence, **not proof VICE 3.10 fails**, and does not justify downgrading Project CBM.
Community artwork-origin notes on that page are further rights-review leads, not
an infringement determination. No clear Censor redistribution grant or complete
licensed production source was established in the reviewed release/creator material.

Initial **engineering test proposal**, not measured compatibility: PAL C64C/8580,
x64sc, appropriate 1541 true-drive behavior and disk swaps in side order. PAL is
supported by [Magnar's tune metadata](https://csdb.dk/sid/?id=62585) and
[psych858o's tune metadata](https://csdb.dk/sid/?id=62200); full-production PAL/NTSC
behavior, drive details and modern sampled-audio fidelity still need testing against
an owner-supplied exact artifact. Keep native physical display geometry.

Classification: **OWNER-SUPPLIED OPTIONAL DEMO / QUALIFICATION CONTENT**. Useful
for real-world graphics/timing/disk/audio compatibility; not a substitute for the
Project CBM-owned basic qualification suite. Archive availability or another
vendor's inclusion supplies no Project CBM license.

## Implementation findings and bounded future work

Inspected product `158e48f5878f079b7fca0f0001d19bfb930779e3` and Menu
`87a16af19e7329b7cf8dbc16ee9420613f35245f`. CONTENT scans the normal categories
recursively. Its extension list includes SID/MUS, PRG, D64/D81 and other disk/tape/
cartridge formats, but the shared launcher currently uses generic `-autostart`.
Thus SID discovery is **not established PSID/RSID playback support**. ROM/REU files
also need resource-specific handling, not a promise that every listed file autostarts.
Safe automatic USB import remains pending the constrained broker from the
[configuration contract](../runtime/configuration-contract.md).

[VICE's supported VSID resources](https://vice-emu.sourceforge.io/vice_7.html)
include subtunes, video/model metadata handling and second-SID configuration.
A later bounded media dispatcher should inspect the header, use a validated SID
player route (evaluate packaged VSID), respect declared clocks/models/addresses,
and test sound, subtunes and clean return. Do not treat `SidStereo` as a Boolean:
it counts extra chips. Avoid global overrides that silently defeat per-file metadata.
No SID dispatcher or downloader is implemented in this pass. The separately authorized
native D64 application routing does not supply PSID/RSID playback.

Import should validate supported type without guessing whether a D64 is a game,
demo or application: preserve the user's category or ask once. Keep multi-disk sets
and names together; D81 needs an appropriate drive model, not the D64 assumption.
No rights-management UI, filename-triggered download, online scraping or extra
main-menu category is needed. Application work is tracked separately below.

For an authorized reference test, record candidate hash, owner input SHA-256,
source/version, subtune, PAL/NTSC, SID models/count/addresses/mixing, VICE settings,
drive model/true-drive setting and disk order. Record observations separately from
expected behavior. A user-supplied test attestation is external to a frozen image
lock; any future embedded media requires rights admission and a **new** lock/image.
Do not alter POC1–3. No third-party playback pass was added by this research.
