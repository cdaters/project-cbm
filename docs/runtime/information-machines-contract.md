# Information and machine consumers: developer contract

2026-09-16; source-only. Product owns `pcbm-info`, the profile registry and preference
operations. Menu owns JSON presentation, dialogs and launch dispatch. Neither UI
requires privileged settings or a new daemon. Read [the user workflow](information-and-machines.md).

## System Information boundary

Menu `lib/pcbm_info_view.py` reads **only** bounded `pcbm-info --json` contract 1.
It rejects duplicate keys, nonfinite numbers, excessive input and wrong format/version.
It projects selected fields with type/length/control-character checks. Missing or
malformed optional fields become Unavailable; no raw exception, collector stderr,
unknown JSON key or diagnostic dump is rendered. It does not import the collector or
probe Linux. Future pcbm-config must reuse this boundary rather than detect versions
or hardware again. Built identities never become guesses from the running machine.

`pcbm-system-info` collects once, formats once, and opens the shared scrolling textbox.
A private temporary directory (0700, files 0600) is removed on exit, including failure
and Back. No persistent report/cache or automatic refresh loop. Partial successful
reports remain useful; invocation/contract failure gives a concise retry message.
Group headings are PROJECT CBM, HARDWARE, SYSTEM and CONFIGURATION. Detailed diagnostics
and future About/license material stay separate. Reentry is the explicit refresh action.

The formatter wraps whole values, including long IDs, using character cell widths
and combining marks; unusual terminal/font Unicode behavior still needs real-console
review. The shared helper measures `stty size` at entry, validates bounds and caps its
widget at 100×22. `--textbox` provides scrolling and a Back button. Enter/acknowledgment,
Cancel and Escape are normalized per [Menu UI contract](../../../project-cbm-menu/docs/UI-CONTRACT.md).
Upstream reference checked 2026-09-16: [Debian dialog manual](https://manpages.debian.org/trixie/dialog/dialog.1.en.html).
No actual dialog/Pi rendering pass is inferred from argument/wrapping tests.

## Registry interface 1

`runtime/data/profiles.json` is validated once per command. The root-owned product
runtime supplies these interfaces (exit 0 success, 2 sanitized operation error):

| Command | Machine-readable output |
|---|---|
| `pcbm-profiles list` | JSON `{schema_version:1, profiles:[...]}` |
| `pcbm-profiles resolve ID` | Validated profile JSON |
| `pcbm-profiles resolve ID --launch-fields` | VICE basename, then zero or more approved flags, one token per line |
| `pcbm-profiles resolve ID --cover` | Single validated cover asset name |
| `pcbm-profiles default` | Tab-separated ID, name, preference status, one line |
| `pcbm-profiles default --id-only` | Single validated ID |
| `pcbm-profiles menu` | First line `state<TAB>ID<TAB>name<TAB>status`; subsequent lines `profile<TAB>ID<TAB>name<TAB>description` |
| `pcbm-profiles initialize` | JSON selection after optional missing-file initialization |

The line/tab interfaces are explicit Bash transport contracts, not human output to
scrape. Fields cannot contain tabs/newlines/control characters. No eval, shell sourcing,
word splitting into commands or user-supplied executable paths. The registry owns labels,
order, description, executable, flags, chips, recommended status and cover asset.
A separate **security allowlist of VICE package entry points** rejects `xevil` as well
as paths/shell fragments; it is not another machine-label table. Allowed flags remain
empty or exactly `-80col` for the existing x128-80col profile. Unknown IDs fail before
an emulator runs. Adding a future entry point requires explicit package/security review.

MACHINES derives both lists from one registry snapshot per display. Main Menu reads
ID and label together, avoiding separate processes for the same state. Cover selection
also uses the registry. The Bash launcher resolves the selected profile and preserves
its argv atoms. Everything after resolution retains POC3's home/XDG paths, SDL ALSA,
F10=291, content/JiffyDOS handling, engineering diagnostics and terminal restoration.
No geometry/resource defaults, tty/PAM configuration or content/media paths are changed.
The no-argument `pcbm-boot` compatibility entry uses the same preference reader.

## Preference authority and migration

Use the [preference contract](preferences.md). The data schema remains version 1;
`default_machine` is now applied by migrated consumers, `boot_preference` remains desired
but inactive. `pcbm-info` reports the same read-only resolved selection as RUN, with
source `user`, `legacy_configuration` or `defaults`. This is source-interface activation,
not proof that a frozen POC image was updated.

Precedence: valid user preferences → validated literal legacy default → the registry's
recommended profile. The legacy reader accepts a bounded literal ID from
`/etc/pcbm/default-machine.conf`, never executes it and never writes it. Missing-file
initialization runs at Menu/MACHINES entry. It rechecks under the existing writer lock,
so a concurrent completed user selection wins. It writes only the new user file. That
file is the durable completion state; no second migration flag/source of truth exists.
Changing/deleting legacy state later does not alter a valid saved preference.

Malformed new state is retained and reported, with safe compatibility fallback. It is
**not** silently replaced or treated as successfully saved. Explicit recovery uses the
existing bounded private backup and atomic replacement mechanism, saving the selected
profile in the same locked update. `pcbm-preferences set default_machine ID --recover
--confirm` is the CLI equivalent. Contention/write failure does not authorize sudo or
unsafe fallback; re-read before retrying if durability confirmation failed.
`pcbm-info` never initializes, repairs or otherwise writes preferences. It reads one
atomic preference snapshot per report, so the selected machine and reported preference
values cannot disagree merely because a writer saves between two reads.

## Remaining legacy consumers and future removal

- Dormant `pcbm-start` still reads the legacy default and has old launch dispatch;
  current product getty/session runs Menu directly. Migrate/retire this alongside the
  explicit **boot-preference activation** slice, before ever enabling direct boot.
- `pcbm-cover` owns artwork/fallback handling; registry supplies the requested asset.
  Artwork existence and additional content-format compatibility are not invented here.
- CONTENT still owns category/path/format logic; it shares the migrated default reader
  and now reports unavailable selection instead of hard-coding x64sc fallback.
- Legacy SYSTEM/SHOW About, CONTROL version/status probes and boot-mode labels still
  duplicate detection. The new INFO view is authoritative; retire duplicate probes
  in the next bounded About/status cleanup. No new information source is added there.
- The legacy library still sources root-owned version.conf and contains unrelated USB,
  ROM, network, power and service helpers. No grant or call path to those operations was
  added. Replacing those belongs to later validated narrow-backend work.

## Installation/extension gate

Install the product [runtime tree and command links](../../runtime/README.md) including
`pcbm-profiles` together with the new Menu scripts/library/formatter. Menu's Debian
metadata now declares Python 3.11+ and the new presentation files. No product runtime
package name/version has yet been assigned: the next packaging gate must encode the
matching interface dependency and validate installed paths before producing artifacts.
The current old Menu version/tag must **not** be rebuilt with these new bytes.

For a new profile, review VICE entry point/options/chips and artwork, change registry
and schema/validation as needed, extend expected coverage and argv tests, then qualify
it. Do not add a case table to MACHINES/Main Menu/launcher. Content relationships remain
future validated metadata, not a plugin system. Installed runtime ships no schemas,
fixtures, test environment or repository history.
