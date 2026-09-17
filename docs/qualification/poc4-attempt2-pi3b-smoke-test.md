# Project CBM 1.1 POC4 attempt #2 — Pi 3B physical procedure

**Ready for owner review; physical qualification is UNTESTED.** Use only the exact
private engineering artifact below. This is not a beta, RC or public release.
Attempt #1 failed and produced no image. POC3 remains the previous physical baseline.

All artifact locators below are relative to configured bulk storage (currently
`/Volumes/TheBench/ProjectCBM-Work`). Do not use a similarly named earlier guest output.
Do not apply Raspberry Pi Imager OS customization: Project CBM owns first boot.

| Identity | Exact value |
| --- | --- |
| Product/candidate | `1.1.0-poc.4` / `private-engineering-poc4`, build attempt **2** |
| Integration | `93d264adf3bac6a397112ecd7349ab8105257852` |
| Release lock | `inputs/frozen-poc4-attempt2/release-lock.json` |
| Lock SHA-256 | `27f0e8ca522f745e240d088fc8fe8feab8f98c15eb165d72fad1a9ef18ee3fdf` |
| Raw image | `artifacts/private-poc4-attempt-2/2026-09-16-project-cbm-1.1.0-poc.4-lite-private-poc.img` |
| Raw bytes | 3087007744 |
| Raw SHA-256 | `e7c0b971ff3c12c09483477f760a09718a038143384774a7d43eca4a790aa217` |
| Compressed image | `artifacts/private-poc4-attempt-2/image_2026-09-16-project-cbm-1.1.0-poc.4-lite-private-poc.img.xz` |
| Compressed bytes | 597702372 |
| XZ SHA-256 | `0ced0321d84777a0e65ac4ebbf4bbae7c42f5680ceba37dc16a5820e5ec50bdf` |

Verify SHA-256 before flashing. Raw/XZ equivalence and read-only validation passed;
[build/validation report](../build/private-poc4-attempt2.md) gives limits and exact inputs.
The test writes normal first-boot/user state to the flashed card; retained master
image, lock and packages remain immutable. Never repair a failure to claim a pass.

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
