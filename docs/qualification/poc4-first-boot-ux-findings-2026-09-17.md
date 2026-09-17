# POC4 attempt #3 first-boot findings

Source audit supporting the [lifecycle investigation](poc4-regression-investigation-2026-09-17.md).
These are findings and bounded correction requirements, **not implemented changes**.
The higher-priority lifecycle evidence stop applies. No real credential was requested,
reconstructed or retained. Physical operation durations were not supplied.

## Exact implementation and state

Menu input is `407ced58b711209631cdfb4db6dcd741a555f408`; Product integration is
`b362c70215cef0e2c6c6a845635c47fd39b3ebbf`; runtime package source is
`cf3a289f99bd7599c8e6f1aa3da4753aa733f981`. Relevant source:

- Menu `scripts/pcbm-first-run`, `scripts/pcbm-config`, `lib/pcbm-ui.sh`,
  `lib/pcbm_config_bridge.py` and `tests/test_first_run.py`/`test_config_ui.py`.
- Product `runtime/project_cbm/{setup,setup_status,configuration,config_backend,config_client,wifi}.py`,
  `build/pigen/stage-cbm/files/{first_boot.py,pcbm-first-boot.service,pcbm-console-session}`,
  and `tests/test_runtime_activation.py`/`test_configuration.py`.

There are two successive state owners. Root first boot grows the filesystem and creates
`/var/lib/project-cbm/first-boot/complete.json` before either getty starts. Local interactive
setup then records `region`, `owner`, `network` and `complete` in
`/var/lib/project-cbm/setup/state.json`; a credential-free `status.json` is its readable
projection. `setup-finish` publishes backend readiness. Neither alters installed identity.

The UI is a linear script, not a navigable step state machine. Its visible Back button
is dialog Cancel (return 1), and Escape maps to Back (return 2), but `pcbm-first-run`
handles both with `exit 1`. The session prints an incomplete-setup retry prompt and
waits for Enter. Restart resumes after completed grouped steps, not at the preceding
screen. This is a confirmed explanation for unreliable Back behavior.

## Stage audit

All Pi durations below are **UNMEASURED**. Bounds are existing command/service limits,
not measured elapsed times or guarantees that cleanup finished within them.

| Step / purpose | Current input and Back/Cancel | Work, feedback and bound | Failure/retry and persisted state |
| --- | --- | --- | --- |
| Root initialization / usable card capacity | No dialog; precedes tty1/tty2 | Validate geometry; growpart; resize2fs; create/chown user directories; sync. No named CBM working stage; possible upstream command output. Unit bound 10 minutes, no per-command timeout. | Geometry journal retained; start/size checks protect retries. Completion marker only at end. Both gettys depend on the unit. Successful general first boot does not prove capacity or interruption behavior. |
| Welcome / explain local offline setup | Message; cancellation exits | Immediate message; no long work | No state committed; session asks Enter to retry. |
| Language / choose system locale | Free input prefilled `en_US.UTF-8`; Back/Escape exits | Holds choice in shell memory; no backend work yet | Unsaved value lost on restart. This is the identified UTF-related field, but the exact cause of the owner's Enter surprise is unknown. |
| Keyboard / console keymap | Free input prefilled `us`; Back/Escape exits, not Language | Holds choice in memory; explicitly says next-boot application | No commit yet. Current keyboard still controls password entry. |
| Timezone / wall-clock zone | Free input prefilled `UTC`; Back/Escape exits | Enter triggers one `setup-region`: localedef, update-locale, compile keyboard, timedatectl. No immediate working-state display. Each adapter subprocess allows 60 seconds; client allows 75 seconds total. | Generic setup error. Locale may have applied before a later keyboard/timezone error; region marker saved only after all three succeed. Retry repeats group; partial state is not rolled back. |
| Owner / authenticated administration | Password + confirmation, 12–128 printable characters, no colon; Back exits; mismatch exits after message | `chpasswd` via stdin, verify expected owner/hash presence; no work indicator; 60-second command, 75-second client | Region survives; owner marker only after success. Repeated completed owner step is a no-op; this is not a reset API. Actual owner login/sudo remains physically UNTESTED. |
| Network / optional connectivity | Stay Offline, Ethernet or Configure Wi-Fi; Back exits | `nmcli networking off/on`; no indicator, 60/75-second bounds | Marker saved after command success. Ethernet connectivity is not separately tested. Wi-Fi choice sets a **shell-local** `join_wifi` flag. |
| Finish / persist readiness | No separate confirmation | Initialize preferences; verify prerequisites/owner/sudoers; save complete then publish policy; no stage indicator | Repeated finish can repair interrupted policy publication. If restart occurs after network marker but before entering Wi-Fi UI, `join_wifi` is lost and setup does not resume into Wi-Fi. |
| Wi-Fi country / legal operating region | General Network menu → country confirmation → free uppercase two-letter value; Back returns to Network | Vendor `raspi-config nonint do_wifi_country`; also enables radio; no working indicator; 60/75-second bounds | Generic invalid/failed result. Separate deliberate country action is required; Wi-Fi first-run choice does not guide directly to it. |
| Scan / discover SSIDs | General Network menu → Nearby Wi-Fi; no enforced preceding country step | Rescan command, then cache reader (8-second bound). No scanning indicator. | `apply_setting` does not propagate success as a reliable control result; scan proceeds to cache read after rescan error. Empty/unavailable/malformed output can become the same no-supported-networks message. |
| Select SSID / choose access point | Named WPA networks; Back returns to Network | Cached scan entries, max 32, sorted by strength; input from validated reader | Selecting again requires another scan menu path. Open/enterprise networks intentionally excluded. No credential saved at selection. |
| Password / join selected SSID | Passwordbox, no mask option; Back returns to Network, not SSID selector | Enable networking/radio, write fixed private keyfile, load, activate UUID. No connection indicator. nmcli activation wait 30 seconds; other commands 60 seconds each, overall client 75 seconds. | One generic failed result; connection keyfile may already exist and autoconnect is enabled. No direct retry-password/alternate-SSID/offline choice. Owner can navigate Network manually. |
| Connection confirmation / usable network | No distinct test stage | Activation result only; no explicit link/address/reachability test | Do not imply Internet or external-traffic success. Completion already happened **before** country/scan/enrollment. |

The 75-second client timeout can expire before a multi-command privileged operation
finishes. It is not an aggregate backend deadline or proof of cancellation of descendants.
The serialized backend lock still excludes concurrent mutations, but UI must report
uncertain/in-progress state accurately. Do not introduce retries that race an unfinished
operation. No measured Pi latency justifies increasing limits or adding sleeps here.

## Human-readable region contracts

| Field | Exact old contract | Required later presentation / internal mapping |
| --- | --- | --- |
| Locale | `[a-z]{2,3}_[A-Z]{2}.UTF-8`, then membership in `/usr/share/i18n/SUPPORTED` UTF-8 entries | Human language/region labels; map to the installed supported identifier. The current default is syntactically valid; unsupported default/Enter failure is not established without card evidence. |
| Keyboard | Lowercase layout ID; membership in `/usr/share/X11/xkb/rules/base.xml` | Installed layout descriptions mapped to their IDs (`us`, `gb`, etc.); retain explicit next-boot/current-password-layout explanation. |
| Timezone | Validated zone path below `/usr/share/zoneinfo` | Human region/city selections mapped to installed zone IDs; UTC remains an explicit neutral option. A country can have many zones; do not infer one silently. |
| Wi-Fi country | Uppercase two-letter identifier, membership in `/usr/share/zoneinfo/iso3166.tab` | Country names mapped to existing regulatory identifiers; separately confirm actual place of use and radio enablement. Do not infer country solely from language or hard-code US. |

Examples of labels for later review: United States, United Kingdom, Canada, Australia.
These are examples, not a newly hard-coded catalog. Pagination/search must respect the
shared UI's 128-choice limit. Advanced authenticated administration remains available
for unusual locales, variants or unsupported network modes; normal setup should not
be a raw configuration editor. No corrected mapping or new catalog test exists yet.

## Back, Cancel and safe retry requirements

Later implementation should separate **editing uncommitted choices** from **already
applied system state**. Back before region Apply must return to the prior field with
the entered value retained. After a successful group commit, revisiting must explicitly
show the saved values; it must not pretend they were undone. Do not turn first boot
into a password-reset mechanism or roll back a completed owner's credentials.

Required tests after the lifecycle evidence gate:

- Forward → Back → change → Forward for locale, keyboard and timezone; Cancel/Escape
  at every prompt; useful validation and retry without discarding unrelated values.
- Group operation partial failure, interruption before/after each marker, and failure
  between completion and readiness publication; no duplicate owner initialization.
- Wi-Fi failure → retry password, select another SSID, revisit country/radio, or Stay
  Offline; interruption must preserve a coherent pending network choice.
- Scan failure distinct from empty scan; malformed backend responses fail closed;
  no silently successful flow after rescan/enrollment failure.
- Visible working state **before** the backend starts; bounded aggregate operation
  semantics, truthful uncertain-state results and no racing retries.

## Password transport and the rejected attempt

`pcbm_ui_secret` uses dialog `--passwordbox` without `--insecure` or text explaining
that typed characters are invisible. That source choice explains the absence of masked
feedback; it does not show that keystrokes were lost. A later correction can choose safe
masking supported by the installed dialog or explicitly explain invisible entry. No
password initial value should enter dialog argv, and Back must clear retained variables.

Wi-Fi validation accepts **8–63 printable ASCII characters**, including punctuation,
spaces and backslash. It intentionally implements WPA-personal passphrases, not raw
64-hex PSKs, arbitrary Unicode or enterprise authentication. Do not weaken these
boundaries merely because the first owner attempt failed. Its exact bytes are unknown
and must stay unknown. Country readiness, keyboard-layout mismatch, authentication,
activation failure and unsupported input remain distinguishable possibilities.

Transport is Bash builtin printf → bridge stdin → JSON client stdin → fixed sudo helper
stdin. No credential argv or diagnostic logging. The backend writes only
`/etc/NetworkManager/system-connections/pcbm-wifi.nmconnection` (root, mode 0600),
escaping spaces/backslashes. NetworkManager may retain the intended credential there
even after failed activation. The implementation discards raw nmcli stdout/stderr and
reduces command success to a Boolean; therefore it **cannot currently distinguish
authentication failure from other activation failures**. A safe future result must use
an allowlisted structured reason/status and locally generated messages, never raw errors
that might contain credentials. “Authentication failed” is appropriate only when known.

Existing source fixture covers spaces and representative punctuation (`!`, `#`, `=`,
semicolon, backslash). Retained native attempt-3 `services.py`/`native-services.log`
proves actual NetworkManager keyfile round-trip of generated test input containing
semicolon, backslash and space, plus redaction. It had **no radio** and does not prove
physical AP authentication. Those synthetic credentials are not reproduced here.
Current host baseline reruns cover transport/redaction and malformed-result handling;
no new physical passphrase tests were performed.

## Truthful progress requirements

Replace invisible waits with immediate named stages: Applying region settings;
Configuring keyboard; Setting timezone; Preparing owner account; Configuring Wi-Fi
country; Scanning for Wi-Fi networks; Connecting to the selected network; Saving
configuration. Show Testing connection only if a real, explicitly defined local
connection check runs. Root expansion also needs truthful feedback while it owns boot.
No fake percentage, invented ETA, arbitrary sleep or blanket timeout increase.

Measure elapsed time from dispatch to result on Pi 3B, including worst observed waits,
and distinguish service deadline from command timeout and confirmed completion. At this
checkpoint **no new feedback, timeout, navigation or password correction is implemented**.
