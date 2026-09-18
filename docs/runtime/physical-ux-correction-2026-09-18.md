# Attempt #5 physical findings and attempt #6 correction

The [exact owner report](../qualification/poc4-attempt5-pi3b-owner-report-2026-09-18.json)
binds Pi 3B observations to attempt #5. Boot/setup completion, Menu, RUN, VT switching,
VICE, F10/Quit, responsive return, other unnamed profiles, StrikeTerm launch, later
boot, setup persistence and information-system IP visibility pass within that report.
Visible Cover and initial Wi-Fi scan fail. Unreported behavior remains UNTESTED.

## Evidence and Cover

All 27 original photographs are retained byte-for-byte with hashes/captions outside
Git at `qualification/poc4-attempt5-physical-2026-09-18`. Network-bearing photographs
remain private. A dark-screen photograph has no reliable launch-phase/timing binding.
The initial writable Paragon mount blocked card collection. After the owner changed
it, both mount and diskutil verified read-only before/after collection. Installed
identity is byte-equal to the frozen lock-derived projection, verified before diagnostic
interpretation. The allowlisted 35-file inventory hashes to
`c1a5e4102ee6af1968394e5899cf73ef59b3b97a90211b96f29e67bfa89a0bf4`.
No card write, remount, executable, credential store or broad journal collection occurred.
This is used-card engineering evidence, not a pristine forensic acquisition.

Three retained slots admit Cover, resolve valid artwork and initialize SDL KMSDRM.
Wrapper, renderer, supervisor and all seven artwork hashes match frozen attempt #5.
The x64sc and x128 slots exhaust the two-second total limit, then the half-second
TERM grace, ending SIGKILL/137 after approximately 2.591 and 2.587 seconds. Their
last event is video initialization; the old diagnostics cannot distinguish decoder,
window or renderer initialization. The xvic slot reaches OpenGL renderer and first
present at 503 ms within the renderer, releases at 1302 ms, and exits zero. Its total
wrapper duration is 2.258 seconds and timeout is marked true. Thus startup outside
the rendering loop also consumes the old total budget. Submission does not prove
visible output; the owner still reported invisible Cover, so visibility remains FAIL.

All three pre-Cover baselines are keyboard mode 3 and VT_AUTO. The killed paths
leave mode 4/VT_PROCESS, and the supervisor restores/read-verifies the exact baseline
before VICE. Every retained VICE exit is zero and final restoration passes. Preserve
that owner, getty/PAM/session, foreground group and restoration path.

Attempt #6 bounds the whole Cover process at six seconds plus the existing 0.5-second
TERM/KILL grace, with immediate progress on normal completion. Six seconds is a
conservative qualification budget, not a measured Pi startup completion time. Fixed
elapsed phase markers now bracket decoder/window/renderer/texture/presentation/release.
The 0.75-second dwell starts after first present returns, so slow first submission
cannot consume the display interval. No renderer architecture, resolution, privilege,
artwork or VT workaround changes. Actual visibility and cold-start timing need the
new hash-bound physical test; no claim that all physical causes are resolved offline.

## First Wi-Fi scan

The old backend returns after `nmcli device wifi rescan` accepts a request; the UI
immediately reads a cached AP list with `--rescan no`. NetworkManager distinguishes
request acceptance from completion: Wireless `LastScan` advances when a scan finishes.
This is a concrete readiness/cache race consistent with the photographed empty first
list and successful manual retry. The card retained no first-scan readiness trace;
radio/regulatory delay versus already-running automatic scan cannot be identified
retrospectively. Do not claim a measured driver or regulatory-domain fault.

The backend now waits up to ten seconds for a managed ready Wi-Fi device, captures
its D-Bus `LastScan`, requests a scan, and polls for a newer completed scan. It accepts
completion of an automatic scan even if the explicit request was busy. At most two
requests per ready adapter, five seconds apart, fit within a 25-second compound
operation deadline; command timeouts use remaining time. No long blind sleep.
Failure to confirm completion is an explicit retry/offline result, never successful
empty-cache presentation. A completed empty scan remains a legitimate no-networks
result. Diagnostics retain only fixed outcome, elapsed milliseconds, request count
and ready-adapter count, without interface/AP/address/credential data.

## Password and text

Dialog supports masked feedback through `--insecure --passwordbox`: the option
means asterisks, not plaintext. Synthetic native PTY tests verify masking, a separate
result pipe, no initial value/credential argv and no plaintext terminal transcript.
Existing protected request/storage paths remain. Unicode en/em dashes in prompts
were interpreted incorrectly by byte-locale terminal/dialog rendering; the native
C-locale test reproduces the mismatch. Updating locale files does not update an
already-running login shell's environment. The first retained launch has TERM=linux
and neither LANG nor LC_ALL; subsequent-boot slots have LANG=en_US.UTF-8. This
supports the first-login byte-locale mechanism. Exact physical terminal byte transcript
was not retained. Plain ASCII `12-128 printable characters` and
`8-63 printable ASCII characters` remove that dependency and pass real dialog tests
under both C and C.UTF-8. Region/Advanced separators are ASCII for the same reason.

## Main Menu network projection

`pcbm-info --json --network-only` uses the same Product collector and a one-second
total external-command budget, skipping unrelated hardware/service/SSID collection.
Menu only formats its versioned JSON: no connected interface, unavailable information,
Ethernet/Wi-Fi address, awaiting IP, multiple connected interfaces and concise overflow.
It prefers a usable non-link-local address and IPv4 when equivalent, supports IPv6
and names duplicate interface types. No assumed eth0/wlan0 names, credential output
or Menu network probes. Detailed addresses/MAC/interface information stays in the
existing information views. Native latency is measured; Pi responsiveness remains a
physical regression requirement.

Quiet boot, rainbow suppression, startup-message suppression and Project CBM boot
presentation remain [deferred](../design/boot-experience-backlog-2026-09-17.md).
Measured boot optimization is separate. No getty/PAM/TTY/session changes here.

References: [NetworkManager nmcli](https://networkmanager.pages.freedesktop.org/NetworkManager/NetworkManager/nmcli.html),
[Wireless LastScan](https://networkmanager.dev/docs/libnm/latest/NMDeviceWifi.html),
[dialog passwordbox](https://invisible-island.net/dialog/manpage/dialog.html).
