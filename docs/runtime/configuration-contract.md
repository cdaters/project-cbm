# Current release refinement

See [networking guide](../release/networking.md) for the complete user workflow.
`pcbm-info --json --appliance` owns bounded network/service observations (schema 1);
Menu presents them without probing. First-boot/SSH account is `pcbm`; pi owns
console/content. File Sharing separately enrolls `pcbm`, forces content writes to pi,
and explicitly enables Avahi discovery on sharing opt-in. On requires unit activity
and the expected listener; credentials and private stores never enter the projection.
Default Computer Name is projectcbm, changeable through the existing validated helper.
The rest of this contract retains request/privilege/recovery boundaries.

# Configuration implementation and activation contract

2026-09-17 source addendum: [run2 review](../qualification/poc4-run2-source-review-2026-09-17.md).
Common selections/Advanced, explicit working/hidden-password feedback and retry-safe
first boot are now source-implemented. During incomplete setup only fixed
`setup-wifi-country`, `setup-wifi-rescan`, `setup-wifi-enroll` requests can use Wi-Fi
after region/owner/network markers and owner-ready verification; network policy and
input validation remain enforced. This does not activate unrelated services or ordinary
system operations early. Region/network may be reapplied before completion; owner
enrollment remains non-resettable. Fixed `wifi_failed` / `wifi_country_required` results
do not claim a positively identified authentication failure. Compound command budgets
are 65s below client 75s. Matching Menu/runtime versions are required in a future lock.

2026-09-16. This completes the owner-approved configuration architecture pass.
[User guide](pcbm-config.md) • [source checkpoint](configuration-maturation.md) •
[accepted audit](../design/appliance-audit-2026-09-16.md).

## Boundaries and organization

- **pcbm-menu** preserves the keyboard-first front door. CONTROL invokes pcbm-config.
- **pcbm-config** (Menu repository) is Bash/dialog presentation and orchestration.
  It has nine shallow task areas, shared Back/Cancel/error handling and confirmation
  for changes to connectivity, listeners and authenticated administration.
- **pcbm-info** (product repository) remains the sole read-only product/runtime
  collector. System Information and About consume its versioned JSON, not pretty
  output. No dialog dependency, daemon, network lookup or duplicate detector.
- **pcbm-config-operation** validates a closed JSON request, sends it to one fixed
  helper through stdin and returns a closed JSON result. Neither UI nor client is root.
- **pcbm-config-root** is the product's fixed-operation root backend, **not installed
  or authorized by this source pass**. It has no command-line arguments.
- **pcbm-admin** provides a returning child shell or separately authenticated owner
  administration. This is deliberately outside the normal-operation root API.

The registry and atomic JSON preferences remain authoritative for machine choice.
Compatibility CONTROL/network/BBS/system/boot entries redirect to the coherent UI;
they no longer contain competing configuration implementations. Dormant pcbm-start
now delegates to Menu rather than implementing a second boot engine. The old
firstboot-check command delegates to read-only info; it is not an initializer.
Main Menu retains RUN/MACHINES/CONTENT/IMPORT/CONTROL/FILES/POWER/REBOOT. Terminal
moves to Advanced, and duplicate system power/service/status/version paths are retired.

## Ownership and supported operations

| Setting | Authority / operation | Source status |
| --- | --- | --- |
| Default machine | `$XDG_CONFIG_HOME/project-cbm/preferences.json` (default `~/.config`), validated registry ID | Implemented; migrated path retained |
| Boot preference | Same user-owned JSON; `menu` or `emulator` | Implemented; active session consumer |
| Audio | User `~/.config/pcbm/audio.conf`, AUTO/HDMI intent and bounded numeric legacy fields | Data-only parsing and atomic mode-0600 save; existing ALSA resolver retained |
| VICE geometry/input | Existing initialized per-profile VICE user configuration | Unchanged POC3 policy; UI explains VICE controls |
| Hostname | Fixed hostnamectl command, lowercase single label | Implemented; validated hostnamectl and local hosts alias update |
| Locale | Installed `/usr/share/i18n/SUPPORTED` UTF-8 member; localedef + update-locale | Adapter implemented; new-session effect |
| Keyboard | Installed XKB base.xml layout; fixed `/etc/default/keyboard` XKBLAYOUT update | Adapter implemented; compile with setupcon for next boot |
| Timezone | Named file confined to `/usr/share/zoneinfo`; timedatectl | Adapter implemented |
| Wi-Fi country | Installed ISO country; fixed raspi-config noninteractive country operation | Adapter implemented; explicit radio-enable confirmation |
| Network | Fixed NetworkManager commands, one managed WPA personal connection | Implemented; NetworkManager activation and bounded scan readiness |
| Optional services | Fixed aliases/units below, deliberate enable/disable | Implemented; actual unit/listener state and bounded confirmation |
| Samba password | smbpasswd stdin for fixed owner account `pcbm` | Implemented; separate from Unix credentials |
| TCPser settings | Root-owned `/etc/project-cbm/modem.json`, typed port/baud | Validated intent consumed by loopback launch adapter |
| Power/reboot | Fixed systemctl poweroff/reboot | Implemented; fixed system operation |
| USB import / ROM copy | Constrained removable-media broker | Implemented; isolated read-only source/copy/unmount |

Malformed primary preferences use the existing explicit backed-up recovery contract;
valid new state wins over imported legacy state. Audio's older format is read only as
known data, never sourced/evaluated; malformed data falls back to automatic selection
without changing the file. An explicit audio save replaces it atomically. Generated
ALSA configuration still uses the existing resolver/write mechanism; it is not newly
claimed crash-safe. Separate audio compatibility storage avoids an unrelated migration.

A keyboard change preserves existing model, variant, options and comments, replacing
only XKBLAYOUT. Advanced variants can be incompatible with a new layout: compile
failure reports an uncertain result, not success. setupcon runs `--save-only
--keyboard-only`; there is no forced tty takeover during Menu/VICE use. Full variants
and desktop input configuration remain Advanced work. This is Debian console-setup,
not an assumption that systemd vconsole configuration is interchangeable with it.

## JSON and security contract

Schemas: [requests](../../schemas/configuration-request.schema.json),
[results](../../schemas/configuration-result.schema.json),
[trusted activation policy](../../schemas/configuration-policy.schema.json).
All are version 1, reject unknown properties and duplicate JSON keys. Semantic
validation adds installed-catalog checks and length/character constraints.

Example (non-secret) request:

```json
{"schema_version":1,"operation":"hostname","values":{"value":"project-cbm"}}
```

Results have `format`, `schema_version`, `status`, `message`. Status is `ok`,
`invalid`, `pending`, `unavailable`, `failed`, `busy`, `credentials_required`,
`saved_pending` or `saved_restart`. Exit 0 means confirmed success or clearly labeled
saved intent; 2 means no confirmed success. A failed multi-step operation can partly
apply: messages explicitly direct users to inspect current state before retrying.
These operations are not advertised as transactional rollback. A root lock serializes
mutations; repeated service enable/disable and same-value saves are safe intentions.

The backend accepts at most 4096 bytes and exactly one request; no paths, units, argv,
commands, shell fragments or arbitrary config keys are accepted. Validators run before
any operation. Actual commands use absolute argv, no shell, a fixed minimal environment,
timeouts and suppressed raw stdout/stderr. HOME is the trusted `/run/project-cbm`
directory so root utilities cannot pick up the calling user's configuration.

The root entry uses Python isolated mode and a fixed installed product module path.
The future package must own the entry, modules, policy and all ancestors as root with
no group/world write or symlinks. The backend checks the policy path's trust chain,
lock ownership/type and fixed managed-file parents. Writes use a private temporary
file, fsync, atomic replacement and directory fsync. No arbitrary filesystem target
is derived from a request. Do not run the development source with sudo.

[The sudoers recipe](../../runtime/config/sudoers.example) permits only the root-owned
helper **with no arguments** to the `pcbm-operators` group. No generic rm, tee, mkdir,
mount, umount, systemctl, shell or `NOPASSWD: ALL`. sudo input/output recording is
disabled for this one command because its stdin can carry a password. Command/audit
records may identify that the helper ran, never record the request body.

Secret handling:

- Bash disables tracing; passwords come from dialog's password box into a pipe.
  They are not program arguments, exported variables or UI temporary files.
- Python never prints request values. Backend, client and UI return fixed messages,
  rejecting or discarding untrusted response text and errors.
- Samba receives the password over stdin. It does not update an owner's Unix password.
- NetworkManager gets a root-only mode-0600 keyfile at one fixed path. Secrets are
  necessary inside that protected credential store; they are not release identity.
- pcbm-info and engineering diagnostics do not read those credential files. Do not
  add raw nmcli connection dumps, user environments or command traces to diagnostics.
- No claim of secrecy from root, an authenticated owner, terminal recording outside
  this application, or same-account process debugging. Normal support exports omit
  credentials; the Pi remains the owner's machine.

## Network and service gates

Policy file: `/etc/project-cbm/configuration-policy.json`. The example is all-disabled.
`system_ready` requires completed account/system initialization; `network_ready`
requires a tested NetworkManager integration; `ready_services` lists only prepared
services. UI preflight avoids asking for secrets when system/network setup is pending.
The backend rechecks readiness independently. Missing/malformed/unsafe policy fails
closed. No runtime policy, sudoers rule, user/group or service is installed in this pass.

Aliases are immutable API names mapped to exact units:

| User concept | Alias | Unit |
| --- | --- | --- |
| Remote Shell | ssh | ssh.service |
| File Sharing | sharing | smbd.service |
| BBS / Modem | modem | tcpser.service |
| Local name discovery | discovery | avahi-daemon.service |

Only enable/disable with `--now` is exposed, never an arbitrary unit or `unmask`.
Readiness is capability, not activation: it must not automatically start listeners.
Engineering masks remain an independent boundary and produce a failed operation.

The managed Wi-Fi connection is one fixed UUID, a connection identifier rather than
a host/build identity. Inputs are printable bounded SSID and WPA personal password;
keyfile escaping prevents new keys/sections. The typed interface intentionally excludes
open/enterprise Wi-Fi and ambiguous numeric byte-array SSID notation. Standard DHCP/
DNS/Ethernet are NetworkManager's responsibility, not a custom CBM stack. Country
selection uses the pinned Raspberry Pi vendor adapter, whose radio-enabling effect
is explicitly confirmed. Failed enrollment can leave a saved auto-connect profile;
users can disable networking. No silent deletion of unrelated connections.

Before marking individual services ready, the future integration must verify:

- **Samba:** root-managed, testparm-validated global/share configuration, no guest
  access, fixed `/home/pi/pcbm` share, no outside symlink traversal. The example fragment
  is not a complete smb.conf. A separate Samba account/password is needed; enabling
  checks pdbedit account presence without requesting hashes. Readiness must attest an
  enabled usable passdb entry, not merely assume Unix password changes synchronized it.
- **SSH:** fresh host keys and an initialized authenticated owner account, deliberate
  authentication policy, no reusable builder keys, no empty/default password.
- **TCPser:** replace the current free-form TCPSER_ARGS unit contract with a fixed argv
  adapter consuming typed modem intent; verify IP232 meaning, loopback/listener binding,
  port conflicts and stop/start behavior. Until then omit `modem` from ready_services.
  This pass does not wire saved JSON into the frozen POC unit or claim a working modem.
- **Avahi:** explicit discovery opt-in and tested interaction with enabled networking.

Hostname activation also requires local self-resolution (for example correctly
configured libnss-myhostname), so renaming does not create sudo/hostname lookup errors.
The adapter does not rewrite arbitrary /etc/hosts content.

## Owner administration and first boot

The owner is not prevented from normal Raspberry Pi administration. A separate,
non-autologin owner account uses Debian/PAM authentication and the normal authenticated
sudo group policy. The appliance account `pi` runs Menu/VICE and narrow operations;
it does not get unrestricted passwordless root. Names and passwords are initialized
locally, never baked into the image. No universal owner password is supplied.

Advanced → Terminal waits for an unprivileged child Bash (no login startup loop).
Advanced → Owner shell uses `su --login OWNER`; raspi-config uses that account plus
`sudo -k -- /usr/bin/raspi-config`. Authentication may occur twice. Neither path uses
the normal privileged helper. `exit` returns to configuration. Accounts not yet
initialized produce a useful pending state. Existing authenticated Linux logins are
not removed or restricted by this design.

Implemented retry-safe first-boot requirements:

1. Preserve the existing single expansion/identity initialization owner; do not stack
   another partition expander. Seal generic machine-id/SSH keys as already designed.
2. Offer locale/language, keyboard and timezone with sensible choices; defer optional
   tuning. Ensure installed catalogs, console-setup and local hostname resolution work.
3. Create the owner account with locally supplied credentials using secure stdin/PAM
   mechanisms; no logging, known password or copying VM account identity. Verify usable
   authenticated login/sudo before setting system_ready. Retries must not reset a
   completed owner's credentials. Recovery access must remain available after failure.
4. Initialize the unprivileged appliance account and fixed group/helper/policy ownership;
   preserve existing user preferences. Keep service readiness separate from opt-in.
5. Offer **Stay Offline / Skip Network**. Ask country/network only when Wi-Fi is wanted;
   reuse the same validation/backend, not a second privileged implementation.
6. Persist completion of each step atomically. Failed/aborted steps leave clear pending
   state. Resume without redoing secrets or activating services unexpectedly.

Boot preference activation is later product session integration: read validated user
intent once on login, optionally launch the selected emulator once, then fall back to
Menu on failure or normal exit. Never loop an emulator endlessly or override user
VICE preferences. This source pass deliberately leaves the working getty/PAM/VT path
unchanged; changing the preference currently records intent only.

## Removable-media and restore contract

Generic legacy USB mount helpers are removed. IMPORT and ROM-copy entry points explain
pending safe activation. This is an intentional restriction of automatic privileged
operations, not of authenticated owner file administration. CONTENT and FILES remain.

The future small storage broker must enumerate eligible partitions and accept only
an opaque selection/major:minor identifier from that enumeration. Under a lock it
must re-resolve the live device; prove USB ancestry/eligibility; exclude actual root,
boot and their parent disks, loop/DM/network devices; and reject swapped/hot-unplugged
selections. The removable bit or `/dev/sd*` naming alone is insufficient evidence.

It mounts only allowlisted filesystems, read-only/nodev/nosuid/noexec, at a fixed
root-owned private staging path with fixed options. No caller path, mount option or
filesystem name. Copying into validated user-owned category roots happens unprivileged:
regular allowed content only, no device nodes, symlink escape or traversal. Unmount
only the broker's recorded mount, never arbitrary/forced unmount. Gate on fixtures and
Linux removable-media tests for root exclusion, races, symlinks, full disk, collisions,
interrupted copy and cleanup. Until implemented and tested, no mount operation is in
the current request schema. This work is a product reliability gate, not another UI study.

Backup/restore remains backup → fresh image → selective validated restore. User data
and VICE settings have different ownership from release identity, machine-id, host keys
and system accounts. A future restore mechanism must respect those boundaries.

## Packaging, tests and extension rules

Menu owns UI/scripts, dialogs and request presentation. Product owns schemas, registry,
preferences/info, privileged operations and OS/service integration. Debian packaging
must install the matching product runtime and independently versioned Menu together;
new Menu routes require these new commands. **Do not publish/rebuild the old Menu
package version with changed content.** A later candidate needs new exact package
identities/hashes and a frozen lock. Source examples are not installed configuration.

Runtime additions use Python standard library and Bash/dialog already present. Future
activation dependencies include sudo, util-linux su, systemd, locales, console-setup,
xkb-data, raspi-config/ISO data, NetworkManager and chosen service packages. Verify exact
paths/versions in the pinned Linux guest; do not infer Linux integration from Mac tests.
No configuration daemon or background telemetry is added. No probes on every submenu;
info collection occurs only when requested. Mutations use a bounded encoder/client/
response formatter, prioritizing validated interfaces over micro-optimization.

An extension adds an explicit operation/schema, pure validator, fixed adapter, tests,
readiness rule, privacy review and concise UI. It may not add arbitrary commands,
paths or unit names as an escape hatch. Keep collectors in pcbm-info and preferences
in their existing authority. New schema semantics require versioned compatibility.
See [testing instructions](../testing.md) and checkpoint results. Tests inject fake
Linux methods and fake dialog/TTY responses; they do not change the host or qualify Pi.

## Authoritative references checked 2026-09-16

The architecture above is a Project CBM decision. Interface details below are upstream
documentation; actual pinned Linux/package behavior remains a runtime activation gate.

- [NetworkManager keyfile](https://networkmanager.dev/docs/api/latest/nm-settings-keyfile.html)
  and [nmcli](https://networkmanager.dev/docs/api/latest/nmcli.html): credential storage,
  connection reload/activation and standard networking.
- [Debian console-setup](https://manpages.debian.org/trixie/console-setup/setupcon.1.en.html):
  keyboard-only saved configuration without forced live console takeover.
- [Raspberry Pi raspi-config source](https://github.com/RPi-Distro/raspi-config/blob/4721a74118ee1eb2c210833ef27c84d7db1ca956/raspi-config):
  keyboard and country behavior, including radio enablement. We use only its fixed
  country backend for a normal operation; full raspi-config remains authenticated.
- [sudoers](https://manpages.debian.org/trixie/sudo/sudoers.5.en.html): no-argument rule,
  environment and I/O logging boundaries; [hostnamectl](https://manpages.debian.org/trixie/systemd/hostnamectl.1.en.html)
  for system hostname operations.
- [Samba smbpasswd](https://www.samba.org/samba/docs/current/man-html/smbpasswd.8.html):
  separate Samba password administration and stdin interface.
