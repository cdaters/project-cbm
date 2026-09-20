# Release documentation source verification

This table records the implementation read for the documentation pass. Product runtime,
Menu and factory sources match the RC3 input commits; documentation-only commits may
advance HEAD. No runtime source was executed as a static documentation test.

| Documented fact | Source authority | Reader document |
| --- | --- | --- |
| Eight Main Menu items and status | Menu `scripts/pcbm-menu`, `lib/pcbm_status_view.py` | User Manual |
| CONTROL's nine sections and all actions | Menu `scripts/pcbm-config`, `scripts/pcbm-audio` | User Manual, Networking |
| Launch/default distinction and 11 profiles | Menu `scripts/pcbm-machines`, Product `runtime/data/profiles.json` | User Manual, VICE |
| Recursive category browser and recognized extensions | Menu `scripts/pcbm-content`, `pcbm-dialog-lib.sh` | Content |
| Media routing, resource rejection, SID refusal | Product `library.py`, `applications.py`; Menu `pcbm-run-vice` | Content, VICE |
| Partition → family → category → automatic copy | Menu `pcbm-import`, Product `importer.py` | Content, User Manual |
| Read-only options, limits, duplicate and metadata policy | Product `importer.py` | Content |
| FILES choices and pane starting paths | Menu `pcbm-files` | User Manual |
| First boot, pause/resume, keyboard timing and password rules | Menu first-run/setup UI; Product `setup.py`, `configuration.py` | Getting Started, User Manual |
| Service states/actions/connections | Menu status view/config; Product service info/backend | Networking |
| User/home/content/share/hostname | Installer, library, configuration policy, Samba template and RC3 offline checks | Accounts/layout, Networking |
| Preferences/audio/VICE/diagnostics paths | Runtime preferences; Menu audio/run-vice; stage files | Accounts/layout, Recovery |
| VICE version/source/flags/patches | Input pin plus `build/packages/vice/debian`, `tools/vice_presentation.py` | VICE, Software |
| Exact installed package list | RC3 actual-image `packages.tsv`, exported by `package_manifest.py` | installed-packages.json |
| Standard stages | Exact pinned pi-gen tar's stage0/1/2 package lists; constructor configuration | Factory |
| stage-cbm effects and outputs | prerun/00-cbm/EXPORT_IMAGE, installer, constructor | Factory, Build Your Own |
| Optional applications/rights | SID-Wizard pin/contract, private StrikeTerm and artwork records | User Manual, Software |

## Command checks and limits

Documentation-specific validation checks shell syntax without running command blocks,
referenced repository script paths, CLI argument names for retained-input/image/export
commands, source-to-Menu names, profiles, key paths and versions. Package recipes and
`dpkg-checkbuilddeps`/`dpkg-buildpackage` usage were inspected; no package builds, target
installers, native service tests or image construction ran in this milestone.

Standard user commands (shasum/sha256sum, PowerShell Get-FileHash, ssh/sftp, rsync and
file-manager controls) were checked against command semantics and primary vendor/manual
references. External graphical instructions link to the vendor because Imager/client
screens vary. Windows execution and a new public build were not performed. Placeholders
are explained before use; blocked commands are not presented as a demonstrated public build.

The relocated official factory walkthrough remains the existing tested private process,
updated for current validator/disk allocation. It is clearly conditional on complete
inputs. Script existence or shell syntax alone is not counted as a successful image build.
