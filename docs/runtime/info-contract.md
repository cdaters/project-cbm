# pcbm-info structured contract 1

Implemented 2026-09-16. Runtime uses Python's standard library; no dialog, daemon,
network requests, sudo, package installation or automatic persistence. Product owns
the collector and minimal installed identity; Menu will own its presentation in
pcbm-config. [Schema](../../schemas/info.schema.json) is developer validation material,
not another copy of the full recovery system in the appliance.

## Interface and semantics

`pcbm-info --json` emits one JSON object and exits 0 when a report, including a partial
report, was produced. Argument/invocation failure exits 2 with a short sanitized error.
No consumer should parse the human output. All fields shown in the schema are present;
JSON object key order is not an interface. There is no collection timestamp, random ID
or hidden telemetry. Live values naturally change between calls.

| Field | Meaning |
|---|---|
| `format` | Constant `project-cbm.info` |
| `schema_version` | Integer 1; incompatible shape/semantics require a new version |
| `built_as` | Allowlisted projection of installed identity, or null |
| `running_on` | Hardware/OS/kernel/memory/storage/display observations |
| `current_state` | Current packages/services/links, legacy configuration and separately labeled new preferences |
| `issues` | Collector name and stable reason code, never raw exception or command stderr |

`null` means unavailable/not established for this collector. `issues` distinguishes
`unavailable_or_invalid` from `not_exposed_by_collector`. An empty display array means
connector interfaces were found but none was connected; no DRM connector interface
produces null. An empty network array means no non-loopback interfaces were observed.
No detected SoC/CPU model may be null without being a malfunction. Unrequested/private
facts are outside the schema, not represented by invented values.

Installed package `installed: false` means the successful/partial dpkg query did not
report it installed (removed/config-files/absent); version is then null. Failure to
query the package database makes the package group null. Current package metadata is
not substituted for immutable built identity. Missing component identities remain
null. A fixture identity retains `fixture: true` and is visibly labeled in human output.

Services expose `LoadState`, `ActiveState`, `SubState`, `UnitFileState` from structured
systemd properties. Missing units, masks, inactive units and failed units are distinct.
A failed systemd query is unknown, not “all services stopped.” Display active mode is nullable: sysfs advertised modes cannot establish it. When
the existing engineering marker and `/usr/libexec/project-cbm-vice/drm-state` are
already present, the collector optionally queries that read-only helper and matches
card/connector IDs to sysfs. It projects only validated width/height/refresh; no modeset,
root, new binary or marker is introduced. Zero/unknown refresh becomes null. Public
images without that engineering helper still work, with mode unavailable; any later
public provider requires separate review. Do not guess from the first advertised mode.

## Sources and cost boundary

| Collector | Source / behavior |
|---|---|
| Build identity | `/usr/share/project-cbm/identity.json`; supported schema 1 projection |
| Current versions | One `/usr/bin/dpkg-query -W` with explicit package/version/install-state fields for the three Project CBM packages |
| OS | `/etc/os-release`, or `/usr/lib/os-release` only if the first is missing; selected keys, parsed quoting without execution; `/etc/debian_version` |
| Model/SoC | `/proc/device-tree/model`, compatible string; no serial/revision whitelist, no marketing-model inference |
| CPU/kernel/architecture/hostname | Selected cpuinfo `model name`, uname; no raw CPU dump |
| Memory | MemTotal/MemAvailable from meminfo, converted from KiB to bytes |
| Root storage | statvfs(`/`): total, free and ordinary-user-available bytes |
| Display | Bounded DRM connector observations; optional existing engineering helper for active mode; no EDID/serial extraction |
| Service state | One fixed systemctl show request for SSH, Samba, TCPser, Avahi, NetworkManager and first boot |
| Network | Bounded sysfs operstate for non-loopback interfaces; no scan, addresses or secrets |
| Settings | Strict literal legacy default/boot files plus separate user preference reader |

Two base command attempts, plus an optional engineering DRM query, have a one-second
timeout each, absolute executable paths,
fixed argv and minimal environment (`LC_ALL=C`). No inherited credentials, shell or
pager. Inputs/output are capped at 64 KiB; connector/interface enumeration is capped
at 64 entries. The fixed trusted OS queries have naturally small output; the cap is
checked after subprocess capture and is not a sandbox for a replaced malicious binary.
Local filesystem/kernel I/O is not given a universal real-time deadline. Missing
interfaces/errors are isolated so the rest of the report survives. No expensive VICE
startup is used to detect a version. No persistent cache/daemon is introduced.

Relevant upstream references, checked 2026-09-16:
[dpkg-query](https://manpages.debian.org/trixie/dpkg/dpkg-query.1.en.html),
[systemctl](https://manpages.debian.org/trixie/systemd/systemctl.1.en.html),
[XDG locations](https://specifications.freedesktop.org/basedir/latest/).

## Privacy and validation

Strict JSON parsing rejects duplicate keys, invalid constants and oversized input.
Identity collection validates the fields it projects; it does not certify the whole
release lock or publisher. Unknown identity keys are discarded, never recursively
copied. Known strings must be bounded printable text or restricted identity tokens.
Current schemas reject unknown report fields. Tests inject secrets into unselected
identity/OS/CPU fields and verify they never appear. These controls complement the
existing image sealing/provenance reviews; a corrupted trusted identity can still
contain false claims, so schema validity is not authenticity.

Do not add serial/MAC/machine-id, IP/SSID, environment, command lines, keys/passwords,
cloud-init or build logs to this report. Hostname and interface names are intentionally
local support facts; callers must review before public sharing. Errors contain codes,
not exception paths or external command stderr. No report is transmitted automatically.

## pcbm-config integration

Invoke `pcbm-info --json` once per information view/explicit refresh. Parse JSON with a
real parser, validate the format/version, and render a concise System Information or
About view from the same data. Keep values separate from shell commands and dialog
formatting. No eval, shell sourcing or `jq`/grep of pretty output. Missing fields/partial
state should display Unknown with optional detail, not abort the configuration UI.
A cached view is session-only and must offer Refresh; no permanent competing identity.

This slice does not implement pcbm-config or wire new detection into every existing
About screen. Future consumers need an interface-version compatibility test. Additive
fields require schema/tests/documentation changes and explicit consumer handling;
strict current consumers must not silently accept an incompatible future version.
