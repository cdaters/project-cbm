# Menu framework, organization and efficiency audit

**2026-09-16; proposed design only.** See the [audit overview](appliance-audit-2026-09-16.md)
for source pins, evidence definitions and scope. No benchmark or alternative UI was
installed. Preserve Project CBM's keyboard-first blue console identity.

## Current implementation: observed source

Menu's approximately 2,924 script lines use Bash and ncurses-backed `dialog`.
`pcbm-dialog-lib.sh` supplies shared menus, messages, confirmation, text display,
terminal sizing and state globals, but also machine mapping, configuration writes,
content/USB helpers, service operations and About information.

| Mechanism | Current behavior | Consequence / proposed correction |
|---|---|---|
| Rendering/lists | `dialog --menu`, checklist, textbox, infobox, msgbox, yesno | Keep widgets; separate UI wrappers from domain operations |
| Prompts/input | No consistent shared text/password form; some console `read`, external alsamixer/raspi-config | Add typed input/password wrappers and consistent cancel/error contracts |
| Keyboard | dialog handles arrows/Enter/Escape; globals carry choice/status | Normalize select, back/cancel and actual tool failure; preserve selected row on return |
| Errors | Status often becomes a loop/return; save errors advise broad sudo grants | Show actionable context, preserve values, offer Retry/Back; remove unsafe advice in future source work |
| Terminal size | tput with 80×24 fallback; min/max arithmetic and string-length estimates | Test 80×24 and smaller terminals, wrapped text and display-cell widths; safe too-small message instead of failure loop |
| Cleanup | Repeated clear/stty/tput and cover calls | Restore terminal at ownership transitions, not gratuitously after every widget; measure flicker/cost |
| Text handling | `printf '%b'` and temporary textboxes | Separate trusted formatting from literal filenames/SSID/errors; strip control characters; cleanup traps |
| Launching | Shared `pcbm-run-vice`, validated profiles/argument arrays and diagnostics | Retain one launcher and return contract; do not scatter VICE calls across menus |
| Settings | Root `/etc/pcbm` shell files, user audio shell config, `.asoundrc`, VICE configs | One typed reader/writer per domain; no executable user configuration |
| Machine definitions | Separate cases for labels, tags, covers and profiles | One registry; validate UI/package/launcher agreement in tests |
| Privilege | sudo mkdir/tee, generic services/mount operations in legacy paths | Replace with user-owned preferences or fixed product operations, not broader sudoers |
| Content | NUL-safe recursive find/sort, then whole list in arrays/dialog argv | Keep safe enumeration; paginate/filter before materializing huge lists on 512 MiB systems |

Package dependencies include Bash, dialog, coreutils, util-linux, procps, findutils,
grep, sed, gawk, sudo, alsa-utils and mc. Current installed runtime restrictions mean
some legacy paths cannot work; a script's existence does not mean POC3 qualified it.

Specific issues worth fixing before feature growth:

- CONTROL → SYSTEM → RELEASE calls a privileged release-prep tool that the runtime
  package intentionally does not ship. Release cleanup belongs in the factory, never
  ordinary appliance settings. Do not execute it to test this finding.
- Top-level QUIT exits Menu, but the product session loop starts Menu again. Its
  shell-exit implication is inaccurate in POC3. Provide a deliberate Advanced shell
  action or remove that promise; do not casually break the working session model.
- POWER/REBOOT are duplicated inside SYSTEM. BOOTMODE's legacy consumer is not the
  POC3 product session path. One editable source must drive the actual startup path.
- About contains `Menu system: -e`; CONTROL contains `menu v-e`, despite a version
  variable already existing. Header/About blanket copyright statements are stale.
- Default-machine/bootmode saves use sudo mkdir/tee that the POC policy does not
  grant. Successful launch testing did not qualify these writes.
- Service checks conflate missing, masked, inactive and failure; listing a unit name
  is not proof that it exists. Failure fallback can duplicate “inactive” text.
- Content advertises extensions including SID, ROM and REU but launches through the
  current machine's generic path. Format support is not equivalent to a working
  PSID player, ROM installation or expansion-memory workflow.
- USB import selects the first removable partition and relies on generic privileged
  commands. Device selection, root-device exclusion, mount policy, cleanup and error
  handling need a separate bounded implementation; they are not physically qualified.
- Audio configuration and device enumeration need stable identifiers, validation and
  an explicit policy for existing user `.asoundrc`. Do not blindly overwrite it.
- POC engineering gates correctly explain unavailable NETWORK/BBS operations, but
  some surrounding labels still suggest ordinary setup is available. Fix guidance
  when implementing the relevant source slice, not by enabling masked services.

## Streamlined information architecture

Keep the recognizable main sequence RUN, MACHINES, CONTENT, IMPORT, CONTROL, FILES,
POWER, REBOOT. Retain the existing visible QUIT until an authorized change deliberately
resolves its session semantics; recommendation is to replace it with Advanced → Terminal,
not another always-visible technical action. Keep RUN as the first/default action.
Use short descriptions such as “CONTROL — Settings and system information.” FILES
can say “Advanced file manager” without moving a familiar shortcut immediately.
No new top-level Applications/Diagnostics category is justified yet.

CONTROL should open `pcbm-config` directly. Proposed shallow sections:

| Section | Contents and ownership |
|---|---|
| Machine & Startup | Current/default machine, Menu/emulator boot choice; same registry as MACHINES |
| Picture & Sound | Output/audio preferences, understandable geometry guidance; VICE-specific detail remains in VICE |
| Keyboard & Controllers | Host keyboard and controller status/mapping where implemented |
| Language & Region | Locale/language, keyboard shortcut, timezone, wireless country when relevant |
| Network | Status, Ethernet, Wi-Fi enrollment/country, hostname; deliberate offline state |
| Services | File Sharing (Samba), Remote Access (SSH), Modem/BBS (TCPser); distinct setup/security controls |
| Content & Storage | Capacity, import destination, backup/restore, ROM resource management |
| System Information | Concise authoritative `pcbm-info` view |
| About Project CBM | Project/versions/credits/licenses/support |
| Advanced | Diagnostics, authenticated raspi-config/admin, deliberate terminal access |

Ten short sections can scroll on a standard console. Do not create a third nesting
level merely to fit a screenshot. Shared destinations (e.g. keyboard shortcut) must
invoke the same screen/data, not duplicate editors. ROM management can be linked
from MACHINES when a ROM is missing. POWER/REBOOT remain the main shortcuts, not
repeated configuration categories. A Service is a user capability, not a systemd unit
name. Network connection and enabling a network listener are different decisions.

### Concrete before → after examples

Counts below are selections/screens implied by the design, not measured keystrokes;
arrow-key counts depend on focus and remembered selection.

| Before | Proposed after | Benefit / compatibility cost |
|---|---|---|
| CONTROL → SYSTEM → SHOW → inconsistent version text | CONTROL → System Information | One fewer menu level; authoritative versions |
| CONTROL → NETWORK → external raspi-config, then privilege error in POC | CONTROL → Network → Wi-Fi; validate country/enroll, or Stay offline | Direct task path with bounded authorization; not a wholesale raspi-config clone |
| MACHINES → save default → sudo write failure/advice | Same MACHINES workflow → atomic user-preference save | Familiar workflow, no administrative knowledge |
| CONTROL → SYSTEM → BOOTMODE edits legacy file with unclear consumer | CONTROL → Machine & Startup → Boot behavior, consumed by product session | One effective setting; no second startup mechanism |
| POWER/REBOOT both main and SYSTEM | Keep main shortcuts, remove SYSTEM duplicates | Same frequent-action access, less clutter |
| QUIT promises shell but Menu respawns | Advanced → Terminal with deliberate return instruction | Honest behavior; technical action less prominent |
| CONTENT builds every matching path into one dialog | Choose existing category, then bounded folder/search results with remembered location | Fewer repeated navigation steps and bounded memory; no mandatory new index daemon |
| BBS error says “not installed” regardless of mask/failure | Services → Modem/BBS shows unavailable/off/failed and safe next action | Accurate result; implementation terms stay in Details |
| Add machine by editing labels/covers/validation in several scripts | Add one validated profile record; shared readers generate views | Less drift and one consistent test contract |
| Each setting implements its own temp files/dialog/status checks | Shared typed input and result wrapper; operation-specific validation | Less duplication without a generic privileged command framework |

Retain the current content folders and add subfolders only for real use:
Games, Demos, Programs, Music and existing ROM resource storage. Disk Images is a
format filter, not a duplicate library. StrikeTerm naturally fits Programs →
Communications; SID-Wizard fits Music → Creation. Utilities can be a Programs
subfolder. ROMs are machine resources, not generic autostart media. Qualification
programs stay in their normal private-engineering content paths; detailed diagnostics
belong in Advanced. A future Favorites/Recent shortcut needs evidence of repeated
browsing cost before becoming another top-level category.

## How to judge efficiency improvements

| Dimension | Evidence required before calling a change better |
|---|---|
| User efficiency | Compare selections/backtracking for RUN, choosing a machine, loading content, changing audio and viewing information; preserve focus and cancel without loss |
| Information architecture | Remove duplicate editors/dead actions; task labels should be understandable without knowing script names; keep advanced tasks out of routine setup |
| Implementation efficiency | One UI result contract and one domain operation; fewer duplicated parsers/mappings; no recursive script restart chains or per-screen privilege plumbing |
| Runtime efficiency | Measure cold UI start, repeated view response, peak RSS and bounded content-list behavior on Pi 3; repeat on 512 MiB Pi 3A+ before qualification |
| Maintenance efficiency | A new setting should normally add its schema/operation/view/tests, not patch unrelated scripts; package/interface version checks catch mismatched components |
| Configuration efficiency | One effective value and documented precedence; invalid updates leave prior state intact; user preferences survive launch/reboot and package updates |

Use clear confirmation for destructive actions, credential/security changes and
shutdown during active work; default to the safe choice. Do not demand confirmations
for harmless navigation or every routine preference. Errors should say what failed,
what remained unchanged and what the user can do next, with technical detail optional.
No framework earns credit merely for having more widgets or a newer language.

## Technology comparison

**Recommendation: retain Bash + dialog with a stronger small shared library.**
The current experience physically works on Pi 3B. No measured latency, RAM or UX
problem requires replacing its renderer. The largest defects are ownership, routing,
validation and state handling, which a renderer migration would not automatically fix.

Upstream/package research as of 2026-09-16:

| Candidate | Runtime/dependencies and availability | UX/engineering tradeoff | Decision |
|---|---|---|---|
| Current Bash + dialog | Already packaged; Debian Trixie arm64 dialog 1.3-20250116-1, 505 KiB own installed package, ncurses/dialog libraries additional | Familiar, wide-character widgets, fast process-oriented model; current mixed library is fragile | Keep engine, repair structure |
| Stronger dialog framework | Same runtime, small shared Project CBM code | Forms/help/focus/result conventions, explicit domain separation; easy incremental migration | Preferred |
| whiptail/newt | Trixie 0.52.25-1, whiptail 97 KiB own package; newt/S-Lang/popt additional; already a raspi-config dependency | Lightweight shell dialogs; different options/widget coverage/look, no inherent domain/privilege improvement | No justified migration |
| Gum | Maintained Go shell widgets, MIT; own binary/module retention if used; stable Debian availability not established here | Attractive composable prompts, but terminal behavior/look and widget contracts differ | Defer |
| fzf | Maintained MIT Go fuzzy finder; Debian package available | Useful optional search for large libraries, not a complete settings framework | Consider only after content-list measurements |
| Small C app with ncursesw/libdialog | Debian native libraries; Project CBM arm64 package and C build needed | Potential low runtime cost, full control and familiar rendering; substantial input/state/error/accessibility ownership | Not enough benefit for rewrite |
| Python Urwid | Maintained LGPL library, Debian python3-urwid; Python already in POC | Structured widgets/event loop/testable state; more UI/dependency ownership and startup/import cost to measure | Credible fallback, not preferred |
| Go Bubble Tea | Maintained MIT framework; own compiled app and retained module/toolchain closure | Strong model/update/view separation; terminal compatibility and visual migration work | Defer |
| Rust Ratatui | Maintained MIT library; own binary, backend/event loop and Cargo closure | Good state/widget testing; larger implementation/recovery burden than this menu needs | Defer |

Package sizes are metadata for the named package only, **not total installed closure
or measured RAM**. No candidate has a measured Pi 3A+ RSS/startup result in this audit.
Do not infer that a Go/Rust binary is large in memory merely from its toolchain;
compilers never need ship in the appliance. Likewise shell subprocesses have costs.
Measure peak RSS, process count, startup and repeated interaction on the target.

Sources: [dialog upstream](https://invisible-island.net/dialog/),
[Debian dialog](https://packages.debian.org/trixie/dialog),
[Debian whiptail](https://packages.debian.org/trixie/whiptail),
[newt maintainer](https://github.com/mlichvar/newt),
[Gum](https://github.com/charmbracelet/gum), [fzf](https://github.com/junegunn/fzf),
[Debian fzf](https://packages.debian.org/trixie/fzf),
[ncurses](https://invisible-island.net/ncurses/), [Urwid](https://urwid.org/),
[Debian Urwid](https://packages.debian.org/trixie/python3-urwid),
[Bubble Tea](https://github.com/charmbracelet/bubbletea), [Ratatui](https://ratatui.rs/).
Dialog is LGPL; ncurses uses its permissive MIT-style license. Project CBM Menu
source is MIT; Bash itself is GPL. Keeping them as ordinary separate programs does
not justify relabeling all bundled software with Project CBM's license.
Library/tool licenses must be checked in the exact retained source/package before
adoption; newt/whiptail has component-specific licensing, not one inferred blanket
license. None of these alternatives supplies Project CBM's authorization policy.

### Cross-cutting requirements and evaluation gates

- Keyboard-first, Enter selects, Escape/Back returns one level, Cancel makes no change;
  main-menu Escape must have a clear harmless policy. Remember selection/location.
- No mouse requirement; disable accidental mouse interactions or make them harmless.
  Use clear focus, text labels and contrast; never communicate status through color alone.
- Unicode depends on terminal font, locale and cell width, not just framework claims.
  Provide simple line/ASCII fallback; test wide characters and hostile control bytes.
- Localization needs separated message strings and width-aware wrapping. Do not use
  translated labels as configuration keys. Dialog does not solve CBM translation itself.
- Accessibility requires real keyboard/readability checks; no untested screen-reader
  claim. Offer concise plain-text information output and avoid animation/flashing.
- Test UI with a pseudo-terminal, fixed sizes, fake backend and deterministic key input.
  Test domain logic separately without dialog/root. Cover all dialog exit statuses.
- Cap list memory/argv and slow probes; detect status once per view or on Refresh.
  Avoid background daemons, repeated full-library scans and repeated device probing.
- Packaging remains Menu `all` for shell code; any native migration requires architecture
  builds and retained toolchain/modules. Prefer Debian-provided stable dependencies.
- Recovery includes exact source, package, tests and build dependencies, not only a
  binary. A new framework adds closure/security-update responsibility.

## raspi-config reference: current implementation, not a template to copy

The current upstream default branch is **trixie**, inspected at
`4721a74118ee1eb2c210833ef27c84d7db1ca956` (2026-07-30), not stale master.
[Exact source](https://github.com/RPi-Distro/raspi-config/blob/4721a74118ee1eb2c210833ef27c84d7db1ca956/raspi-config).
It uses `/bin/sh` and whiptail, grouped menus, concise verb descriptions, Select/Back/
Finish, hardware-sensitive entries and reboot-required handling. Shared `get_*`/
`do_*` functions serve interactive and noninteractive paths. Learn these conventions.
Its noninteractive dispatcher invokes named functions/commands; this is not a narrow
security API. Interactive administration expects root. Do not expose the whole tool
through passwordless sudo. Its package split does not separate UI from authority.

POC3 retains raspi-config/core 20260730; core contains `/usr/bin/raspi-config` and
raspi-config adds supporting dependencies/files. The earlier privilege failure was
therefore a product integration gap, not merely disabled networking. Keep Project
CBM's identity and give normal settings a bounded backend instead of reproducing
raspi-config's entire hardware/admin surface.

## Incremental implementation plan after approval

First specify and test result/input/profile/preferences contracts; retain existing
screen text/layout where sound. Extract UI primitives without moving privileged
commands into a “universal helper.” Convert one screen at a time, keeping the shared
VICE launcher. Add System Information from `pcbm-info`; then streamline CONTROL and
remove unsupported runtime actions. Finally add each authorized configuration backend.
For each slice compare common task steps, error recovery, peak memory and response
on Pi 3; qualify 512 MiB separately. Require equal or better measured performance,
not a theoretical architecture claim. Preserve factory/recovery and all POC3 regression
paths. This audit does not authorize any of those changes yet.
