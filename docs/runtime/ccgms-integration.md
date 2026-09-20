# CCGMS 2021 application integration

The owner approved a CCGMS-only application disk for 1.1.0. This replaces StrikeTerm
in new candidates, while retaining RC3 and all historical evidence unchanged. The
[release policy](../release/release-policy.md) records the settled rights decisions.

## Exact inputs and composition

[ccgms.json](../../build/optional/ccgms.json) is the input authority. Publication:
[CSDb release 198392](https://csdb.dk/release/?id=198392), Alwyz, 24 December 2020;
[author publication](https://1200baud.wordpress.com/2020/12/24/ccgms-2021-released/).
The exact D64 and published source were acquired and reviewed before integration.

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| Upstream compilation D64 | 174848 | `103ebd7e129a5e2d4125be3c3c93d2945f480393428d2525d334c2cd06d0353c` |
| Unchanged CCGMS 2021 PRG | 22963 | `baab211ac345aa9b486f70bbf1f7dfdfa7d056a67229dfad5668b7c8e0879076` |
| Published 2021 source | 133216 | `201c98d03db53f649a9e9a18eb62a7b9b24e5051db3c5af1c32a410e02ef3d18` |
| Preserved BSD 3-Clause notice | 2053 | `5e20bda180d6dc4738f6ae232257a9b96d0d2834a0492db09964b9681eb56520` |

`tools/ccgms_application.py` checks the entire upstream disk, follows only its exact
CCGMS entry's sector chain, verifies the extracted program hash, then builds a fresh
standard D64 with one PRG. It neither rewrites the program nor copies compilation free
sectors. The seven unrelated files and decorative entries are absent. No further
rights investigation of those omitted files is required.

Both published source and exact program About text identify BSD 3-Clause licensing.
Craig Smith's applicable notice and Alwyz's attribution are retained. Same-release
source/version/credit correspondence is established; a bit-identical source rebuild is
not claimed. The pinned CRT is review evidence only and is not shipped.

The frozen optional input contains deterministic disk, source, license, provenance and
manifest. The image gets a pristine system disk, a UID/GID1000 user working copy in
`/home/pcbm/content/programs/c64/Communications/CCGMS`, and source/notices under
`/usr/share/doc/project-cbm-ccgms`. Original third-party payloads remain outside Git.
RC3's private StrikeTerm input remains verifiable through RC3's frozen recipe; it is
not a required member of the new release lock or installed image.

## Serial configuration

`applications.content_options()` recognizes the canonical CCGMS application folder.
The existing shared launcher consumes fixed newline-separated argv, without shell
re-parsing or a second emulator lifecycle. CCGMS selects `x64sc`. VICE adds ACIA
SwiftLink mode 1, base `$DE00`, NMI, device 0 (`-myaciadev 0` in this exact VICE build),
and IP232 to the loopback port from validated `/etc/project-cbm/modem.json`.

Use CCGMS **Swift / Turbo DE**, **2400 baud**, **Standard** firmware, **Full** duplex
with the existing initial TCPser speed. This requires no Ultimate Ethernet interface,
VICE rebuild, TCPser redesign, automatic listener enablement or global preference
rewrite. The typed existing modem backend remains responsible for port/speed changes.
Users opt into BBS / Modem and may save CCGMS's own `CCGMS-PHONE` on their working disk.
Changing CCGMS preferences does not change the pristine system copy.

## Evidence and limits

Native ARM64 testing boots the actual unchanged program through installed VICE,
uses its own F7 modem menu, receives `OK`, connects via TCPser to a synthetic loopback
endpoint, exchanges text, disconnects and exits. `tests/native/ccgms_serial.py` preserves
that test using a new disposable output directory. It is restricted to the established
native staging namespace. No public BBS or physical Pi is contacted by that test.

C1541 creates original synthetic G71 media; installed x64sc and x128 with 1571 drives
complete autostart. C64 G71 routing avoids inheriting SuperCPU/DTV defaults; C128 keeps
its applicable display variant. Other machine families reject automatic G71 launching.
The focused unit suite covers input tampering, exact one-program composition, existing
user data, application-specific settings, port validation and routing.

These results do not qualify real Pi display/audio, keyboard shortcuts, remote BBSs,
file-transfer protocols or every G71 image. The new exact-hash Pi4 procedure requires
CCGMS connection/send/receive/disconnect/return/relaunch and affected content regression.
