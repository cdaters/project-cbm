# Actual Combian V3.7 utility review

Read-only review, 2026-09-16. Owner-specified directory:
`/Volumes/TheBench/Projects/Combian/Combian64 - V37_update_updatedEN/`.
This is a four-file update directory, not a complete bootable distribution. No
script was executed or copied into Project CBM. Its files and original metadata
remain untouched. [Inventory](combian-v37-inventory.json) records exact identities.

**Observed** below means directly visible in these four scripts. User-requirement
interpretations are **inferred intent**, not claims of historical runtime success.
Previously inspected `fromCombian64_v37` and fan-v5 extracts are separate evidence;
this record does not attribute their additional material to this directory.

## Functional comparison

| Combian feature | Observed implementation | Inferred user requirement | Current Project CBM equivalent | Status | Action |
| --- | --- | --- | --- | --- | --- |
| Main Menu | Bash/dialog, fixed 50×92, flat sections, 46 choice rows | Recognizable keyboard front door | Main Menu plus nine accepted task areas | EQUIVALENT | Preserve CBM organization; no architecture change |
| Default machine | Eleven selections replace line 3 of bootmachine with sed/sudo/mv | Choose emulator and startup default | Eleven-profile registry, validated user preferences, shared launcher | PROJECT CBM ALREADY BETTER | All profiles covered; no new mapping |
| RUN/return | bootmachine plus recursive menu calls; emulator output discarded | Launch and return conveniently | Shared unprivileged launcher, diagnostics, deliberate return | PROJECT CBM ALREADY BETTER | Preserve |
| Cover | fbi displays one combiancover.jpg before menu loop | Appliance visual identity | Seven registry-selected Project CBM launch Covers using SDL | EQUIVALENT | Different timing/design; keep CBM Covers, no Combian asset reuse |
| Network | Enable/disable dhcpcd; labels claim dynamic/static/boot-time effects | Choose connectivity versus offline use | NetworkManager, first-boot offline choice, country/scan/enrollment, Ethernet/status/hostname | HISTORICAL / SUPERSEDED | No dhcpcd; no inference that disabling DHCP establishes static addressing |
| Samba | systemctl enable/disable smbd only | File transfer with PC/Mac | Typed File Sharing actions/status, content-only share, separate credentials | PROJECT CBM ALREADY BETTER | Preserve; test external clients physically |
| TCP over IP | Integer flag; background sudo tcpser with fixed ports/baud; port-derived kill -9 | C64 terminal/BBS connectivity | Typed TCPser service settings, loopback listeners, explicit service control | PROJECT CBM ALREADY BETTER | Preserve. VICE serial/driver compatibility remains a separate physical test; not all-machine connectivity proof |
| Midnight Commander | sudo mc | Familiar file management | FILES invokes mc as normal pi user; child exits back to Menu | EQUIVALENT | Retain standard package; no root default |
| X-Copy | Fixed /media/usb0, glob list, unquoted copy, games-only destination, unconditional success message | Insert USB, copy content, know where it went | Constrained USB discovery/read-only mount, user copy, categories, SID routing, counts/error/cleanup | USEFUL SMALL IDEA | Add exact destination folders to success message; no broker redesign |
| USB visibility fix | Vendor systemd-udevd PrivateMounts yes→no edit and reboot | Make removable files accessible | Explicit broker mount in its own operation; no udev-triggered importer | HISTORICAL / SUPERSEDED | No vendor edit; real USB discovery remains physical gate |
| ALSA helper | sudo alsamixer followed by sudo alsactl store | Access available sound-card mixer controls | Existing output selection/test; mixer previously only via terminal | USEFUL SMALL IDEA | Add unprivileged Advanced Mixer; no global store |
| raspi-config | sudo raspi-config | Owner access to Pi administration | Normal pcbm-config; Advanced authenticated owner/raspi-config | EQUIVALENT | Keep separate authentication boundary |
| QUIT/shell | Exit script with farewell | Reach shell | Advanced → Terminal, authenticated owner session, exit returns | EQUIVALENT | No main-menu QUIT restoration |
| Power/reboot | sudo shutdown commands | Convenient safe shutdown | Main shortcuts, fixed validated power operation | EQUIVALENT | Preserve |
| INFO | Calls absent info helper | Product description/status | pcbm-info, System Information, About | NEEDS MORE EVIDENCE | Historical helper unavailable here; no CBM omission |
| SID-Wizard | W case launches 1.8 D64 through x64; W absent from options | Music creation | CONTENT → Music → Creation, 1.97 native core working D64 | PROJECT CBM ALREADY BETTER | Do not revert or add unreachable shortcut |
| StrikeTerm | No occurrence or payload in these four files | Communications application (established separately) | Admitted exact 2014 Final D64 through normal CONTENT/x64sc | NEEDS MORE EVIDENCE | Cannot corroborate byte equality from this directory; prior verified relationship retained |
| Boot startup | Menu edits and calls external bootmachine; boot/profile files absent | Selected machine at startup | Preference consumer with Menu fallback | NEEDS MORE EVIDENCE | Do not infer actual historical boot timing/session from absent files |

No other user-facing utilities or hidden payload files were found in this directory.
No Combian source, cover, font or media is admitted as a build input. Donationware/
noncommercial wording in the menu is historical evidence, not permission to copy it.

## Bounded decisions

Only two runtime additions result: **Advanced Mixer** under Picture, Sound and
Controllers, and **explicit import destination feedback**. No hierarchy change,
new helper privilege, package framework, new file manager or network stack.

Standard [alsamixer](https://manpages.debian.org/trixie/alsa-utils/alsamixer.1.en.html)
provides keyboard-operated card/control access; F6 selects a card and Escape exits.
It is already supplied by `alsa-utils 1.2.14-1+rpt1`. The UI calls it directly as the
appliance user and returns; unavailable controls/devices fail gracefully. It does not
invoke [alsactl store](https://manpages.debian.org/trixie/alsa-utils/alsactl.1.en.html).
Persistence follows existing OS policy and is not a new global-save promise.
Some digital outputs have no hardware mixer controls; the normal audio route remains.

Midnight Commander is already in attempt #2's retained package inventory:
`mc 3:4.8.33-1+deb13u1 arm64`, `mc-data 3:4.8.33-1+deb13u1 all`.
Menu Depends requires mc and alsa-utils. FILES calls mc without sudo. Frozen input
and offline image checks must confirm these same identities and executable paths.
No rebuild/patch of these Debian packages is justified.

USB asks for an eligible partition and semantic destination because PRG/disk file
extensions cannot tell a game from a demo/program. SID files go to music. This is two
necessary choices, not arbitrary paths. Completion now shows selected
`/home/pi/pcbm/<category>/Imported` and the SID `music/Imported` exception. Existing
read-only/nodev/nosuid/noexec mounting, ext4 noload, symlink refusal, source revalidation,
UID-1000 copying, no overwrite and unmount remain unchanged. It does not rely on udev
mount visibility or edit systemd-udevd. Live progress beyond the existing activity
message/counts is deferred; do not expand this into a media-manager project.

## No-Ethernet path and remaining limits

First boot → Configure Wi-Fi enables NetworkManager, completes required local setup,
then opens Network. Set country/radio, choose Nearby Wi-Fi, select a WPA-personal SSID,
enter password; inspect status. No shell, raspi-config UI, Ethernet or Internet is
required by this path. When starting from Stay Offline, deliberately Enable normal
networking first. Hidden WPA-personal SSIDs can be entered by name. Enterprise/open
networks and arbitrary IP policy remain advanced administration. Fixture coverage
checks UI requests/redaction; Pi radio/country/DHCP/reconnection remain physical tests.

Samba, SSH, mDNS and TCPser remain deliberate opt-ins. Owner Terminal/raspi-config
remain authenticated; normal settings use fixed operations. Combian's unqualified
TCP-over-IP-for-all-machines wording is not copied. Project CBM's service supplies a
local bridge; actual VICE serial selection, terminal driver and BBS interaction need
separate qualification. Public incoming BBS hosting is outside this bounded adapter.

StrikeTerm stays PRIVATE-ENGINEERING-ADMITTED / PUBLIC-RELEASE-RIGHTS-GATE-PENDING.
SID-Wizard stays the accepted 1.97 subset/template/working disk. Reference SID/demo
payloads remain owner-supplied; generic SID autostart stays refused. No licensing
research is reopened, no optional payload expanded, no boot presentation optimized.
