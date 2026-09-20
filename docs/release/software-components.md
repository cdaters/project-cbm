# Software in Project CBM

[Documentation index](../README.md) · [Build Your Own](build-your-own.md) · [VICE details](vice.md)

Project CBM combines upstream Linux packages with four separately packaged components.
Keeping them separate makes it possible to update the Menu without rebuilding the emulator,
or reuse an unchanged emulator while fixing system integration. “Reused” means the same
verified package bytes, not a freshly compiled binary with an old version label.

## Deliberately selected components

| Component | What it does / why it is here | Source and installation |
| --- | --- | --- |
| Raspberry Pi OS Lite 64-bit / Debian 13 Trixie | Minimal Linux base without a desktop | Pinned arm64 pi-gen stages and Debian/Raspberry Pi packages |
| Raspberry Pi kernels/firmware | Boot, Pi devices and graphics support | Pi v8 and 2712 kernel/firmware packages, installed through standard stages |
| Project CBM Runtime | Setup, preferences, profiles, status, constrained privileged operations | Product source, `build/packages/runtime/debian` |
| Project CBM Menu | Keyboard Menu, configuration presentation, content/FILES, Covers | Menu repository, its `debian` package |
| VICE 3.10 | Commodore emulation | Verified upstream source plus Product's Debian recipe and two diagnostic patches |
| TCPser 1.1.6 beta lineage | Emulated modem bridge | Pinned go4retro source and Product's TCPser recipe |
| Midnight Commander (`mc`) | Two-pane file management | Distribution package required by Menu |
| NetworkManager (`network-manager`) | Ethernet/Wi-Fi connections | Distribution package; Product applies setup/service policy |
| Samba (`samba`, `smbd`) | Authenticated SMB content share | Distribution packages plus Product share configuration |
| OpenSSH (`openssh-server`) | Remote terminal/SFTP | Distribution package with opt-in service and pcbm access policy |
| Avahi (`avahi-daemon`) | Local names and discovery | Distribution package, separately enabled; SMB advertisement integration |
| `dialog` and Bash | Keyboard-driven text UI | Distribution packages required by Menu |
| SDL2 and SDL2_image | VICE/primary/Cover presentation | Distribution libraries; development headers only needed on builder |
| Mesa/DRM/GBM libraries | Console graphics/rendering | Distribution packages, including dynamically loaded runtime dependencies |
| ALSA / `alsa-utils` | Audio devices, mixer and speaker test | Distribution libraries/tools; VICE uses SDL audio through ALSA |
| `udisks2`, filesystem utilities, `rsync` | Storage management and transfer support | Lite/component dependencies; import has its own read-only broker |
| `cloud-guest-utils` | Filesystem preparation support | Explicit target installation; does not mean cloud-init setup is enabled |
| SID-Wizard 1.97 core | C64 music creation | Selected upstream binary/source/license subset, placed on a working D64 |
| StrikeTerm 2014 Final | Optional C64 BBS terminal | Present in private test inputs only; public redistribution remains unresolved |

Development tools from intermediate stages are removed where specified by the installer.
The final package inventory, rather than the list above or upstream stage lists, tells
you exactly what was installed.

## Exact package reference

The current reviewed 1.1 candidate uses Runtime **1.1.0~rc3-1**, Menu
**1.1.0~rc3-1+pcbm1**, VICE **3.10-1+pcbm4**, and TCPser **1.1.6~beta-1+pcbm1**.
The base reports Debian 13.7. These technical versions identify the candidate reviewed
for this manual; they are not a claim that a final 1.1 release was published.

[installed-packages.json](installed-packages.json) contains all 672 installed
package/version/architecture records, package size metadata, source-inventory checksum
and the raw image hash they were measured from. It was generated from actual-image
validation output, not a proposed apt list. It includes no payloads or credentials.
This repository reference is not automatically added to the already-frozen image.

For a new build, the existing documentation-safe exporter accepts the validator's TSV:

```sh
python3 tools/package_manifest.py "$PROJECT_CBM_PACKAGE_TSV" \
  --image-sha256 "$PROJECT_CBM_IMAGE_SHA256" "$PROJECT_CBM_PACKAGE_MANIFEST"
```

Run from Product; set these variables to the actual validator inventory, raw-image hash
and a new output filename. This produces an inventory, not a license-compliance audit
or proof that every program works. Official releases must also provide the needed source,
licenses and broader release materials.

## Software and content rights

Project-owned source uses the repository's [license](../../LICENSE.md). Upstream packages
keep their own licenses. VICE is GPL software: corresponding source, patches and build
information must accompany its distribution as required. The established provenance
records, rather than a generic license label on this repository, control third-party files.

The selected SID-Wizard core has explicit author-license evidence retained by the project.
Its supplied songs/examples, manuals and unrelated add-ons are not automatically part of
that selection. StrikeTerm's private-use availability does not establish public redistribution
permission. Primary artwork and machine Covers include material whose embedded graphics/font
rights still require public-release review. They must be cleared or replaced with suitable
art before being promised as redistributable assets.

ROMs, games, demos and music are separate content questions. Do not assume every VICE
data file or every owner-supplied reference is project-owned, and do not assume all ROMs
are absent merely because users can add their own. Review the actual image's asset/license
inventory and [provenance](../provenance.md). Users should supply additional material they
are entitled to use. This guide grants no new third-party rights.

The [public-release audit](../documentation/public-bootstrap.md) lists genuine remaining
publication work. Normal users can focus on [adding their own content](content.md).
