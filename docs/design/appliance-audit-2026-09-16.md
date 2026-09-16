# Project CBM appliance audit and proposed next work

**2026-09-16 — owner-review design, not implementation authorization.**
Preserve Project CBM's personality; organize and streamline the machinery. No POC4,
framework migration, service enablement or additional physical testing occurred.
ADR-0001 remains the foundation authority.

## Read this audit

- [Physical POC3 attestation](../qualification/poc3-pi3b-owner-report-2026-09-16.json)
- [Menu implementation, alternatives and concrete workflow changes](menu-framework-audit-2026-09-16.md)
- [Combian and optional Commodore software](combian-and-optional-software-2026-09-16.md)
- [Boot presentation and measurement](boot-experience-audit-2026-09-16.md)
- [Existing setup/privilege findings](../qualification/setup-ux-review.md)

Evidence labels used throughout: **Observed** means inspected repository/artifact
bytes; **owner report** means physical observations supplied by the tester;
**upstream** means linked documentation/source researched on the date above;
**recommendation** is engineering judgment; **unmeasured/untested** identifies a gap.
Current source inspected: product `a78c0dd77b5c471b6e8d70665f48446fcf9af27e`, Menu
`5cf863312a62ac458d5f6c362a9e81b9d14ec20c`. Menu scripts/debian/configs have no diff
from frozen Menu `897cee7c792b11bfed80168a576f263340f5f57d`.

## POC3 qualification and foundation assessment

Exact candidate: **1.1.0-poc.3 / private-engineering-poc3**. Raw SHA-256:
`9a8b1e0465c93981dfa6b09772e9e3fbf5c487a915bba0046b5de034f9331f33`.
The attestation also records the compressed image, lock and all photograph hashes.
It supplements the unchanged planned matrix and completed build evidence.

| Area | Physical Pi 3B result |
|---|---|
| Boot, automatic Menu, Menu rendering/keyboard | PASS |
| tty1 → tty2 → tty1 | PASS |
| RUN → x64sc, C64 rendering and keyboard | PASS |
| Intended geometry, no horizontal stretching, unused side areas | PASS on this display |
| Smoke PRG | PASS |
| SID PRG, audible SID output, all three expected voices/tones | PASS |
| Video/input PRG, keyboard and joystick test | PASS |
| D64 loading and smoke execution | PASS |
| F10 → VICE menu → Quit → clean Project CBM return | PASS |
| Normal reboot → automatic Menu | PASS |
| New failures within this bounded test | None reported |

Pillarboxing means unused vertical areas at the sides of the emulated picture.
Photographs corroborate those margins and visible test screens. Seven originals
were inspected and verified copies retained under configured bulk storage at
`qualification/poc3/pi3b-owner-report-2026-09-16/photos/`; the adjacent `evidence.json`
records filenames, SHA-256, captions and evidentiary limits. No photos are in Git.
Audio, joystick actions and keyboard transitions are owner observations, not facts
proved by a still photograph. The actual test date, monitor model/mode and runtime
renderer capture were not supplied; the record date is not invented as a test date.

**Still untested/not established:** other Raspberry Pi models; other VICE machines;
controlled PAL/NTSC comparison; precise DRM/SDL mode capture; PSID/RSID playback,
SID fidelity/stereo; interrupted first boot; independent clean rebuild; broader
configuration persistence; network enrollment/Wi-Fi/Samba/SSH/TCPser/Avahi; full
settings/privilege work. Separate subtests not explicitly reported remain untested
in the detailed matrix. Joystick is now PASS for this bounded test, unlike POC2.
Intentionally disabled services and visible boot messages are not failures.

**Recommendation: accept POC3 as the basic appliance foundation.**

- The automated factory builds a controlled private image from retained inputs.
- Pi 3B physically demonstrates usable launch, presentation, input, original media,
  audio, emulator return and reboot, including the POC3 geometry correction.
- POC1's black-screen failure and POC2's stretched display remain historical facts.
  POC2 changed both graphics dependencies and session ownership; no single POC1
  root cause is thereby proven. POC3's successful policy does not identify the
  precise POC2 downstream scaling component without runtime evidence.
- Product setup, privilege boundaries, content operations, support UX and measured
  acceptance budgets remain substantial work. Pi 3A+ needs separate 512 MiB tests.
- This is neither a release, beta nor RC. One controlled build is not proof of
  reproducibility; independent clean reconstruction and comparison remain required.

## Recommended component boundary

Keep Bash + dialog and the recognizable front door. Strengthen its shared code
before adding more settings. Avoid a new application framework without measured
benefit on Pi 3/3A+.

| Component | Responsibility | Owner |
|---|---|---|
| `pcbm-menu` | Familiar front door, navigation, machine/content selection and shared unprivileged launcher | Menu repository |
| `pcbm-config` (proposed) | CONTROL's coherent settings experience; forms, explanations, confirmation and rendering results | Menu repository |
| `pcbm-info` (proposed) | Read-only product/runtime information, stable JSON interface plus human CLI | Product integration repository |
| Configuration backend (proposed) | Typed validation and explicitly authorized OS operations | Product repository |
| VICE | Emulator resources and saved emulator preferences | VICE, seeded once by product |

The UI must not duplicate identity/hardware detection. `pcbm-info` supplies CLI and
System Information/About; configuration UI renders it. The UI never becomes root.
Prefer a small standard-library Python information/backend implementation where
structured parsing warrants it (Python is already used by this image), with Bash
remaining the menu layer. This is a proposed choice, not a framework migration or
an instruction to replace every shell utility with Python.

### Information contract

A versioned JSON response should have distinct `built_as` and `running` objects.
`built_as` derives from `/usr/share/project-cbm/identity.json`, the existing minimal
installed authority. Preserve its release/build/integration/base/component/schema
identities exactly. `running` reports actual state and collection errors separately.
Do not rewrite build identity after an admin package update. Show both expected and
currently installed component versions when they differ.

| Runtime fact | Read-only source / qualification limit |
|---|---|
| Model, SoC, CPU, architecture | Device-tree model/compatible, kernel/CPU interfaces and dpkg architecture; omit serial/UUID |
| Memory | Linux MemTotal, labeled usable memory; do not equate reserved-memory-adjusted value with physical marketing capacity |
| OS/Debian/kernel | Parse os-release and debian_version as data; uname; never source an arbitrary mounted OS file as shell |
| Current VICE/Menu/TCPser package | dpkg metadata; do not start SDL/VICE merely to find a version |
| Hostname and root capacity/free | Kernel hostname, findmnt/statvfs; identify actual root filesystem, not a hard-coded SD device |
| Display | Read-only DRM connector/mode provider where available; report unavailable/permission-limited, not guessed |
| Default machine and boot behavior | Same effective preference reader as launcher/config UI |
| Services | Distinguish absent, masked, disabled, inactive, active and failed |
| Network | Link/enrollment/status only when available; no network requirement or automatic scan/contact |

Unknown is a supported result with a reason. Bound execution time and output;
partial detection failure must not blank System Information. Provide concise text
by default and an explicit `--json` interface with schema version. No secrets,
Wi-Fi passwords, private keys, full environment or builder-specific paths. Local
network addresses/SSID may be useful on-screen; diagnostic export should redact
identifiers by default and explain any optional detail. Full recovery archives,
package closure and build history stay outside the appliance.

System Information should fit a concise screen: Project CBM/build, Menu/VICE,
Pi model, OS/kernel, memory/storage, display, network/services summary. Add Details
for longer fields. About should give a short description, authorship, version,
project/support URLs, license and third-party credits, with further notices accessible
on demand. Do not repeat blanket “no copyrighted software” claims: license-compliant
software is still copyrighted. Detailed Linux state belongs in Advanced → Diagnostics.

## Configuration ownership: reduce competing truth

Observed current state is fragmented: `/etc/pcbm/default-machine.conf` and bootmode
are shell-style settings written through sudo; audio uses a separate user shell
configuration and `.asoundrc`; VICE has per-profile saved resources; product owns
release identity, first boot and session startup. The POC session bypasses the older
Menu startup script. A single setting can therefore be editable yet not affect the
actual boot path. These are static gaps, not newly asserted physical failures.

Proposed precedence:

1. Package defaults under `/usr/share/project-cbm/` are read-only vendor data.
2. Product system configuration under `/etc/project-cbm/` is validated, root-owned
   and changed only through an authorized operation or authenticated admin.
3. Personal appliance preferences under `$XDG_CONFIG_HOME/project-cbm/` (normally
   `~/.config/project-cbm`) are user-owned typed data with schema versions.
4. VICE owns supported emulator preferences in the established profile config;
   initialize once, preserve thereafter. Do not duplicate them in competing files.
5. Ephemeral session state is not persisted as a second default.

Use one reader/writer per domain and atomic writes. Validate enum/range/type,
reject duplicate/unknown security-sensitive fields, and preserve the prior valid
configuration on error. Default machine, personal startup mode and audio preference
normally need no root privilege. Distinguish a preferred output from actual ALSA
availability. A future migration must read existing settings as data, back them up,
record schema transition and never repeatedly overwrite legitimate user choices.
Do not migrate frozen POC systems during qualification. Machine profile metadata
should be one declarative registry consumed by selection, launcher validation,
labels and tests; product integration owns how it maps to packaged VICE resources.

## First boot and privilege architecture

Keep platform initialization (identity/expansion, already implemented) distinct from
an eventual short human setup. One coordinator owns retry/completion state; do not
stack the legacy Menu firstboot-check with another wizard.

Essential first-use choices: language/locale, keyboard, timezone; then **Stay offline**
or optional Wi-Fi setup. Ask regulatory country only when wireless is requested;
do not infer it from language/timezone. Ethernet may simply use normal OS behavior
when networking is enabled by deliberate product policy. Optional services, backups,
emulator tuning and account administration belong in CONTROL later. Cancel/skip must
not mark a failed privileged operation successful. Re-enter unfinished setup safely;
finish offline without a network account or passwordless raspi-config workaround.

Recommended execution boundary:

- UI collects data without privilege; common preferences stay unprivileged.
- Root-owned helpers accept a small named operation and bounded typed input, recheck
  authorization and current state, then call fixed OS APIs/commands with argument
  arrays. No shell fragments, eval, sourced input, arbitrary paths or unit names.
- A narrowly enumerated sudo policy can authorize these specific helpers for the
  appliance operator. Any active-local-session restriction must be enforced in the
  backend, not merely inferred by UI visibility. Document the local physical-user
  trust assumption; don't accidentally authorize remote sessions equivalently.
- Validate hostname/locale/timezone/country and service-specific policy. Use locking,
  atomic changes, explicit success/cancel/validation/authorization/failure outcomes,
  and a reboot-required indication. No success dialog after a failed write.
- Network enrollment can use standard NetworkManager mechanisms; send secrets by
  protected input channels, never command-line arguments or logs. Samba credentials
  remain a separate passdb operation from Unix password changes.
- SSH, Samba and TCPser have separate deliberate settings and fixed operations.
  Never grant arbitrary `systemctl`, `rm`, `tee`, `mkdir`, `mount`, `umount`, root
  shell execution or `NOPASSWD: ALL`.
- Authenticated raspi-config remains Advanced Administration once an intentional
  admin credential path exists. Its broad interactive/noninteractive dispatcher
  must not be an unrestricted passwordless backend.

[NetworkManager's CLI](https://networkmanager.dev/docs/api/latest/nmcli.html) and
[polkit](https://manpages.debian.org/trixie/polkitd/polkit.8.en.html) are standard options,
but a console has no assumed graphical authentication agent. Evaluate specific
policy actions if using polkit; choosing it does not itself create narrow privilege.
The simpler initial recommendation is a few fixed Project CBM helpers, not a general
privileged daemon. Root backend code should receive dedicated negative tests.

## Proposed work order for owner decision

1. Approve the interface boundaries and streamlined navigation in this audit.
2. Implement read-only `pcbm-info`, shared UI/result conventions and one preference
   registry/reader, with tests. Repair misleading/absent runtime actions and About
   data through source/package changes in a separately authorized milestone.
3. Implement the minimum offline setup and narrow backend, feature by feature;
   network/services need explicit policy and credential tests before enablement.
4. Improve content browsing/import and optional applications only after ownership,
   compatibility and rights gates. No automatic bundling of the Combian copies.
5. Measure boot/interaction, then improve quietness and proven critical-path costs.
   Continue hardware and reproducibility qualification under their own authorization.

Do not package all of this into an unbounded POC4. Each slice should preserve the
POC3 launch/session/geometry/media/return behavior and produce a reviewable test plan.
Independent custody/backup, signing custody, SBOM selection, measured budgets,
historical v1.0 input closure/build-chain gaps and clean rebuild remain unresolved.
