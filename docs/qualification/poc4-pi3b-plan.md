# Runtime-activation Pi 3B qualification outline — NOT READY TO RUN

The [POC4 attempt stopped before producing an image](../build/poc4-blocked.md).
There are **no raw/XZ hashes to flash**. This outline is preparation only. A future
approved, offline-validated artifact must supply exact candidate, lock, raw/XZ hashes
and filenames before this becomes an executable qualification procedure. Do not use
a similarly named guest output or customize an image through Raspberry Pi Imager.

Record every row as PASS, FAIL, UNTESTED or NOT APPLICABLE, with the observation and
reason. An absent joystick/AP/network/BBS service is not automatically a CBM failure.
First failure: preserve diagnostics and STOP; do not repair the running qualification
system. Supported settings changes explicitly requested by the procedure are tests;
manual configuration/package repairs to make a failure pass are not.

## Required core tests

1. Record exact hashes, Pi3B, storage, power supply, display/cable/resolution, audio and
   keyboard/controller equipment. Photograph the whole display for geometry evidence.
2. Boot: root expands once using the actual root device; no reusable machine ID or
   host keys. Record available storage via System Information after initialization.
3. First boot: region/UTF-8 locale, keyboard, timezone; unique `owner` password; obvious
   **Stay Offline** choice; successful completion and automatic Menu. Keyboard changes
   apply after reboot, so password entry uses the current layout. Never report passwords.
4. Reboot: no unexpected setup replay; region/keyboard/timezone remain; Menu returns.
   Record interrupted-setup recovery separately on explicitly authorized disposable
   media; do not improvise power cuts during the main qualification run.
5. Menu/rendering/keyboard and tty1→tty2→tty1. On tty2, `pcbm-diagnostics` and
   `pcbm-info --json` must remain available without root. Preserve bounded launch logs
   before rotation removes the primary failure evidence.
6. RUN→x64sc: complete C64 canvas, native geometry with expected unused side area,
   keyboard and joystick where available. F10→VICE menu→Quit→responsive CBM Menu.
7. CONTENT: original `pcbm-smoke.prg`, `pcbm-sid-check.prg` (all three expected voices),
   `pcbm-video-input.prg` (colors/movement/keyboard/joystick), `pcbm-check.d64`.
   Record SID-generated audio only; this does not prove PSID/RSID, stereo or fidelity.
8. CONTROL/pcbm-config: Machine and Startup; Picture, Sound and Controllers; Language,
   Keyboard and Region; Network; Services; Content and Storage; System Information;
   About; Advanced. Confirm consistent Back/Escape and understandable failures.
9. Change default profile and save/reboot; RUN uses it. Restore the original through
   the supported UI. Test direct-machine boot once, Quit→Menu and a safe Menu recovery
   route. Do not infer other emulator/video-standard qualification from these actions.
10. System Information/pcbm-info: build/Menu/VICE/TCPser identity, Pi model, architecture,
    memory, OS/Debian/kernel, storage, display, hostname, network/services, selected
    machine and boot mode. Distinguish built identity from detected runtime state.
11. Advanced→Terminal: authenticate as owner, ordinary shell, authenticated sudo,
    then `exit` returns naturally. Advanced→raspi-config: authenticate, open and leave
    without unrelated changes, return cleanly. Cancel/wrong password must not break UI.
12. Safe USB: select known removable test media; import only owned diagnostics; correct
    category/ownership, no overwrites, clean unmount, CONTENT discovery and launch.
13. Final normal reboot→Menu. Record actual persistence tested, not a blanket guarantee.

## Optional network/service tests

Keep offline core qualification independent of these tests. Enable only the feature
under test through pcbm-config; record initial/final states and disable afterward.

| Area | Bounded test |
| --- | --- |
| Ethernet | Explicit network enable, link/DHCP/status and offline return |
| Wi-Fi | Country, availability/discovery, WPA-personal enrollment, status, disconnect/forget; no credential in info/logs/diagnostics |
| Hostname | Supported update, local resolution and status |
| File Sharing | Separate Samba credential, deliberate enable, intended content share only, access from trusted client, disable |
| Remote Shell | Explicit SSH enable generates fresh host keys; owner login, authenticated sudo, disable; no root login |
| BBS/Modem | Typed port/baud, deliberate enable/disable; actual outgoing BBS interaction only with an available authorized endpoint |
| mDNS | Deliberate enable/disable and hostname discovery on a suitable LAN |

No external network/BBS environment: mark its dependent tests UNTESTED/NOT APPLICABLE,
not failed. Do not expose a public inbound listener or manually change firewall/auth
settings to bypass a failure. Never put credential screenshots in retained evidence.

## Third-party application tests

- **SID-Wizard:** CONTENT→Music→Creation→SID-Wizard. Launch, geometry, keyboard,
  bounded SID audio. Save a small owner-created work to the working disk; exit and
  relaunch to verify persistence. The root template must remain unchanged. F10/Quit
  returns to CBM. Do not claim general composition/fidelity qualification.
- **StrikeTerm**, only if the new lock retains the reviewed private admission:
  CONTENT→Programs→Communications→StrikeTerm. Discovery/launch/geometry/keyboard,
  F10/Quit/return. BBS connectivity is the separate service test. Physical success
  **does not establish public redistribution rights**.
- Optional owner-supplied SID/dual-SID/Wonderland XIV remain separate reference tests,
  never required for the core gate. Current `.sid` generic autostart should refuse
  clearly; do not report PSID/RSID playback as implemented. No automatic downloading.

## Evidence

Future photographs go to a new external qualification evidence directory, not Git.
Record original filename, SHA-256, caption, result represented and evidence limits.
A photo can show a screen/geometry/state; audible tones, movement, physical input,
network connectivity and persistence are operator observations unless separately
captured. Keep full monitor/bezel in geometry photos; redact unrelated personal data.

Read-only extraction of logs from rootfs uses Linux `ro,noload`. Do not repair or
modify the candidate to obtain a pass. No other Pi model or subsequent candidate
is automatically authorized by this procedure.
