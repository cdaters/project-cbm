# POC4 attempt #3 — Pi 3B procedure DRAFT

**NOT READY TO FLASH. NO ATTEMPT #3 IMAGE EXISTS.** Construction was blocked by automatic
approval. This is a prepared test plan, not authorization to substitute attempt #2.
Finalize only after the single frozen build and complete offline validation succeed.
Do not perform physical testing now. No other Pi model or additional candidate.

| Identity | Binding |
| --- | --- |
| Product | 1.1.0-poc.4 / private-engineering-poc4, attempt 3 |
| Integration | `b362c70215cef0e2c6c6a845635c47fd39b3ebbf` |
| Menu | v1.1.0_poc4.1 / 407ced58b711209631cdfb4db6dcd741a555f408 |
| Lock | `inputs/frozen-poc4-attempt3/release-lock.json` |
| Lock SHA-256 | `435c6e0d7a5a45eaff3f45af6d384fca5b602139fa9fb640950e2f5e7b4f39a9` |
| Raw path/size/SHA-256 | NOT PRODUCED — required before use |
| XZ path/size/SHA-256 | NOT PRODUCED — required before use |
| Raw/XZ agreement | NOT RUN — required before use |

[Owner report](../build/poc4-attempt3-owner-review.md) explains status/evidence limits.
Bulk root: `/Volumes/TheBench/ProjectCBM-Work` for this deployment. Once finalized,
verify exact raw/XZ hashes before flashing. Do not apply Imager OS customization:
Project CBM owns initialization. Keep master image/lock/packages immutable. The
flashed test card is expected to receive supported setup/user writes.

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

## Required Covers, file manager and mixer checks

1. Default C64: Menu → RUN → correct C64 Cover → x64sc. Brief approximately 0.75 s,
   proportional artwork, complete C64 canvas with correct geometry/pillarboxing.
2. Explicit MACHINES launch of one additional profile (for example VIC-20): its correct
   Cover → corresponding VICE executable; input, F10/menu/Quit, clean CBM return.
3. With a different default selected through supported UI, launch C64 content with
   its independently selected/forced profile. Cover must match actual C64, not default.
4. No stale display, broken keyboard/VT or persistent graphics ownership. Switch
   tty1↔tty2, quit and launch again. Record display/connector/mode and diagnostic data.
   These actions qualify only the exercised profiles/video standard/display.
5. FILES → Midnight Commander: verify normal appliance UID, browse/copy an owner-created
   test file within content, F10 exit → Menu. No sudo mc. Do not change system files.
6. Picture, Sound and Controllers → Advanced Mixer: keyboard controls/card selection
   where available, Escape return; subsequent VICE audio still works. Digital devices
   with no mixer controls are NOT APPLICABLE, not automatically failure. No manual sudo
   alsactl store; record actual persistence only.

## Required Wi-Fi without Ethernet scenario

Use a suitable owner-controlled WPA-personal AP. Begin with **no Ethernet cable**.
Test first boot's Configure Wi-Fi choice on its own properly recorded fresh-flash run,
while also retaining a separate Stay Offline result. Do not improvise first-boot state
resets. Network path: country/radio → scan → select SSID → password → connect.
From an already completed Stay Offline run, explicitly Enable networking first.

Check status and pcbm-info, reboot, automatic reconnection, disconnect/forget and
supported offline return. Credentials must not appear in info/diagnostics/logs or
photographs. No shell/raspi-config workaround. This scenario is required before
claiming this candidate's network UX qualified; unavailable AP/radio environment means
UNTESTED with reason, not an invented pass or automatic software failure.

## Optional additional network/service tests

Keep offline core qualification independent of these tests. Enable only the feature
under test through pcbm-config; record initial/final states and disable afterward.

| Area | Bounded test |
| --- | --- |
| Ethernet | Explicit network enable, link/DHCP/status and offline return |
| Wi-Fi | Required no-Ethernet scenario above; additional AP/security conditions only if supported |
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
Useful screens: first boot, System Information, C64/second Covers, C64 geometry,
SID-Wizard, StrikeTerm and Midnight Commander. Do not use the accidental staging-copy
directories identified in the owner report for photographic or qualification evidence.
Record original filename, SHA-256, caption, result represented and evidence limits.
A photo can show a screen/geometry/state; audible tones, movement, physical input,
network connectivity and persistence are operator observations unless separately
captured. Keep full monitor/bezel in geometry photos; redact unrelated personal data.

Read-only extraction of logs from rootfs uses Linux `ro,noload`. Do not repair or
modify the candidate to obtain a pass. No other Pi model or subsequent candidate
is automatically authorized by this procedure.
