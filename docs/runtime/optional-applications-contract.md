> Current 1.1.0 owner decisions: [release contents and notices](../release/release-policy.md).
> CCGMS replaces StrikeTerm in the new candidate; artwork permission and the VICE ROM,
> signing, formal SBOM and public-bootstrap decisions supersede earlier tentative gates below.
> Historical candidates, rights observations and evidence remain unchanged.

# Optional applications: admission and integration contract

Decision/research date: **2026-09-16**. Extends the completed
[Combian/optional-software audit](../design/combian-and-optional-software-2026-09-16.md).
That audit remains evidence of the earlier review; this record resolves the native
SID-Wizard core license/input question. No Combian code or media was copied.

## SID-Wizard selection

Select **SID-Wizard 1.97 native C64 one-SID core**, released by Hermit (Mihály
Horváth), with SID-Maker. [Author's release and comments](https://csdb.dk/release/?id=262561)
identify June 24, 2026, a chord/tempo-table correction and further enhancements.
The current author release list did not establish a newer native release. The
1.97.1 macOS port is a separate host port, not a newer C64 choice.

The acquired authoritative source archive's `native/manuals/ChangeLog.txt` and
`native/sources/Makefile` resolve a naming trap: native files retain `1.9` in their
filenames, while APPVERSION=1.9 and SUBVERSION=7 identify this release. Do not rename
those upstream member identities in provenance. Native changes since 1.8 include
instrument/chord/tempo-table navigation and multi-SID export corrections; 1.97 also
repairs a later chord-table regression. The latter was not evidence of a 1.8 bug.
Piano-roll/high-resolution GUI and some platform fixes concern host ports; do not
advertise them as native C64 features. There is no demonstrated VICE/Project CBM
compatibility reason to retain 1.8. Prefer the maintained source and corrected native
line, subject to the physical gate, rather than the remembered Combian version.

### Exact admission

The reviewed archive's `native/README.txt` explicitly grants permissive use of the
SID-Wizard tool under Hermit's WTF wording; the top README corroborates that intent.
Record **LicenseRef-Hermit-WTF**, retaining the actual notice rather than inventing
an SPDX version. Native README attributes the tool to Hermit with Soci's help and
identifies Hermit's graphic tools. The native source dependency list identifies
program/graphics code; separately linked example music in the interactive manual
is **not** part of the chosen two-program set.

Admit only these verified upstream members plus the native README notice:

| Member under `SID-Wizard-1.97-sources-examples/native/` | Bytes | SHA-256 |
| --- | ---: | --- |
| `application/SID-Wizard-1.9.prg` | 33130 | `dbf1d495d8c7986e632276df39f550440ad149f1de87f4ddfbe6933aea9cdb82` |
| `application/SID-Maker-1.9.prg` | 16799 | `dba39fee3b081439fcee59764a3a2685de4fc2c4abf51db7868518a1ad908f16` |
| `README.txt` | 3880 | `e0ca3e28b9106d497bb25d49ddf81ad33c92408a0dc08125e356951a66ef4b39` |

[Author-linked source archive](https://csdb.dk/getinternalfile.php/281063/SID-Wizard-1.97-sources-examples.tar.gz):
6,140,658 bytes, SHA-256
`aeb265f4a778b2acb5aad13e8e98af882888292f749f29f4d18cbf49850e57bc`.
Acquired over HTTPS from the author's CSDb release. No detached signature or separately
published upstream SHA-256 was established; this is a retained first-acquisition hash,
not a claim of cryptographically authenticated authorship.

The whole archive is retained privately as source/review material. **Its sample
music, instrument banks, interactive/manual content and host binaries are not
blanket-approved for appliance distribution.** Do not apply the core grant to every
third-party asset merely because it occurs in that archive. A future expanded subset
needs its own review. No requested HVSC SID or Wonderland media was acquired.

The [reviewed pin](../../build/optional/sid-wizard.json) fixes source/member hashes,
rights basis and runtime location. No upstream installer, Makefile or C64 program
was executed. Native assembly sources and rebuild directions are retained; upstream
names 64tass and c1541, plus compiler/compression tooling. A pinned independent native
rebuild remains **unproven**. Current preparation extracts verified release binaries
and constructs the small disk deterministically, not a claim of source-to-binary
reproducibility. Native PAL/NTSC handling exists in source; VICE 3.10 load/save/audio,
actual runtime RAM/CPU and each video standard remain physically untested here.

## StrikeTerm disposition

**OWNER-SUPPLIED, not an admitted build input.** Identity: StrikeTerm 2014 Final,
Alwyz, [May 17 author announcement](https://1200baud.wordpress.com/2014/05/17/striketerm-2014-final/),
[CSDb 130807](https://csdb.dk/release/?id=130807). The author reports source-drive
loss in 2015 and points users to CSDb in 2018. A proposed 2015 release is not an
established shipped version. No complete exact-2014 source or later maintained
StrikeTerm release was established. CCGMS Future remains a separately researched
alternative, not a silently selected successor.

The author's [2013 manual](https://1200baud.wordpress.com/striketerm-2013-documentation/)
calls that version freeware and its Novaterm 9.6c base public domain, while reserving
manual reproduction rights. It credits multiple serial/transfer-driver contributors.
These statements do not clearly grant Project CBM redistribution of the complete
2014 disk and included third-party routines. Do not bundle or automatically acquire
it. An owner may follow the author-endorsed release source under applicable terms;
this is not a Project CBM license grant. No outreach was sent.

The earlier read-only Combian comparison established a 174,848-byte
`st2014final.d64`, SHA-256
`72b803c54c7892857c0ddb5674dabc841d59a496285975546bef689308940595`,
identical between the two local extracts. This is **historical local identity only**:
no new upstream disk was acquired and byte equality to the author-endorsed CSDb
copy remains unresolved. Combian's menus advertise the application; no working
StrikeTerm-specific launch/runtime was demonstrated in the audit.

[VICE's RS232 guidance](https://vice-emu.pokefinder.org/wiki/RS232) discusses
StrikeTerm/Novaterm and SwiftLink/Turbo232/IP232. Treat bridge endpoint, driver,
baud/flow control and connect/load order as explicit future tests. Do not copy
historical ports or launch TCPser implicitly. Author-page user reports of reversed
handshake labels are a test lead, not a confirmed defect in our untested setup.
The complete D64 may contain configuration/dial-directory state: keep it user-owned,
back it up and exclude private dialing credentials from diagnostics/distribution.

## Source implementation

No new main-menu entry or plugin system. Existing CONTENT categories remain:

- Music → Creation → SID-Wizard (admitted one-SID core working disk).
- Programs → Communications → StrikeTerm (owner-supplied D64 only).

`pcbm-profiles content-profile ABSOLUTE_FILE` is a small extension of the existing
structured profile interface. It validates a regular, canonical file below the
content root. The two exact folder prefixes require a standard D64 and select the
validated registry's `x64sc`; ordinary content retains the user's current default.
No preference is written. Symlink/traversal/control-character paths, unsupported
application media and missing registry entries fail without running VICE. File
contents/filenames cannot supply executable names, shell fragments or launcher
arguments. This is structural validation, not a C64 malware scanner.

Menu's content consumer calls that interface, then the existing shared launcher.
The launcher, POC3 geometry defaults, F10 menu key, diagnostics, tty/session and ALSA
policy are unchanged. No global SID/clock/drive preference is forced. User-adjusted
VICE settings may therefore affect an application; qualification must record the
actual C64/video/SID/drive configuration. File race/mutation by its owning user is
not an authenticity boundary; the launcher still uses fixed validated executables
and quoted argv. No privileged operation was added.

## Frozen-input factory

`tools/optional_software.py` is an **offline** preparer/verifier. It reads only
hash-verified allowlisted regular archive members; it never extracts arbitrary
paths or runs upstream commands. It creates an original standard 35-track D64 with
SID-WIZARD first and SID-MAKER second, leaving free space for user work. No music or
unreviewed sample banks enter the disk. Repeated preparation produces identical bytes.

Use the existing guarded external workspace. In a **new, unfrozen input-kit folder**:

```bash
python3 tools/optional_software.py "$RETAINED_SOURCE" "$NEW_KIT" \
  --workspace-config "$WORKSPACE_CONFIG" > "$NEW_KIT/optional-software.json"
```

`NEW_KIT` must exist within the configured mounted workspace. The tool refuses a
folder with `release-lock.json`; never point it at POC1–3. Source/code/notices/objects
are preserved by SHA-256; the returned object supplies the new lock's
`optional_software` field. Use **release-lock schema 3** for that new candidate.
Schemas 1/2 retain their previous semantics and reject optional software. Schema 3
requires the reviewed SID-Wizard entry; original qualification media may independently
remain declared. It cannot admit StrikeTerm or HVSC content by changing a title.

The input graph is one-way: source + reviewed pin + preparation recipe → optional
payload; frozen lock references all four. Final image/qualification hashes remain
external. `verify_kit` reconstructs and compares the exact payload, including notices.
The stage consumes it only when declared; no existing lock was edited. Installed
minimal identity remains bound to the full input-lock digest; an application-specific
small manifest identifies the template. There is no full recovery kit in the image.

The stage installs the immutable template/manifest and notice under `/usr/share`,
and seeds the normal user content copy once during fresh image construction, owned
by the appliance user. Existing files or redirected destinations fail closed rather
than overwrite songs. Source archives/recipes/extra examples stay external. About's
future package integration must point to the retained notice; no long license dump
or duplicated version detector is added.

Prepared input set: configured bulk workspace
`inputs/optional-software-2026-09-16/optional-software.json`.
[Exact inputs and offline results](optional-software-validation.json).
The prepared tar is **184,320 bytes**, SHA-256
`46872e5c937f681fa161a2acf88937040f2b90a091b03d8153513035bd62223e`.
The working D64 is **174,848 bytes**, SHA-256
`cec93ae1fd5fc846507c1883fd9cb210c6a3c0f40c1c081964e3b8450e26dc44`.
The template and initial copy consume about 342 KiB plus notice/manifest before
filesystem overhead. Package/image size and running memory are not measured.

## Validation and remaining gates

Tests cover deterministic disk allocation/chains, exact PRG round-trip, upstream/
member hash rejection, archive/member allowlists, destination symlinks, existing
user-state preservation, frozen-kit refusal, schema/rights/version allowlists,
profile mapping/default preservation and actual content-browser success/failure.
Existing information/configuration/launcher/security/POC3 tests remain applicable.
Fixtures do not qualify physical application behavior. The real admitted input was
also verified and installed into a small disposable directory fixture only.

Pending: matching versioned Menu/product packages, subsequent full candidate lock,
normal runtime activation, independent C64 assembly reproduction, physical application
load/save/audio/return, StrikeTerm upstream equality/permission and modem connectivity.
The separate SID/PSID/RSID dispatcher and safe USB broker remain product work; this
native D64 integration does not implement either or reopen Menu architecture.

Final source checks: **120 product tests, 44 Menu tests plus launcher checker pass**.
[Mac fixture timings](optional-software-performance.json): routing 0.058 ms median
with loaded registry, 25.2 ms including a new process/registry. Pi 3/3A+ performance
remains unmeasured. No new runtime dependency, daemon or repeated hardware probe.
