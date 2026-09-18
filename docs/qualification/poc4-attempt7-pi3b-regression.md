# POC4 attempt #7 — release-readiness Pi 3B procedure

**READY FOR OWNER PHYSICAL TEST: YES. READY TO FLASH: YES.**
All behavior on this new image starts UNTESTED. Codex performs no physical testing.
This procedure supersedes earlier candidate procedures only for the new hash-bound image.

| Identity | Exact binding |
| --- | --- |
| Product | 1.1.0-poc.4 / private-engineering-poc4, attempt 7 |
| Integration | `33347bb9c11e87e70069da5d160e03ec197efe31` |
| Menu | v1.1.0_poc4.5 / `4c88fa38ce28c63b6342adfb5d7a084a21248684` |
| Lock | `inputs/frozen-poc4-attempt7/release-lock.json` |
| Lock SHA-256 | `1c25d7f7850c63c41e2730bdaef2deef9cd6d0ccf1321c9b23fd4d9228926b3d` |
| Raw | `artifacts/private-poc4-attempt-7/2026-09-18-project-cbm-1.1.0-poc.4-lite-private-poc.img`; 3087007744 bytes |
| Raw SHA-256 | `cbab8327981eaf0d1d632d6637d3117fd2c2d68ac6d529c434b52fed995b60ba` |
| XZ | `artifacts/private-poc4-attempt-7/image_2026-09-18-project-cbm-1.1.0-poc.4-lite-private-poc.img.xz`; 598188816 bytes |
| XZ SHA-256 | `b8119c4f3bb1c9361cd4d0c047eaa454447884e36dad9d345b50673ba9e7b687` |

Paths are relative to `/Volumes/TheBench/ProjectCBM-Work`. Raw/XZ equivalence passes.
[Build report](../build/private-poc4-attempt7.md) / [exact results](../build/private-poc4-attempt7.json).
Recovery checkpoint: `archive/poc4-attempt7-2026-09-18`; verify its external manifest.


Use a fresh disposable card; preserve attempt #6 and its evidence. Verify the complete
SHA-256 of the chosen raw/XZ file before writing it. Leave Imager OS customization off.
Record Pi **3B**, card, power supply, keyboard, display/cable/scaling, audio/controller
and client OS versions. Use only the exact named image; safely eject before insertion.

Record each item PASS / FAIL / UNTESTED, plus a short observation. Test outcomes apply
only to that hardware/image/function. Do not photograph passwords or post private
network/account data. Retain original photographs externally with filenames, captions,
byte counts and SHA-256; do not commit large photographs. Network addresses in photos
remain private evidence. Optional tests need not precede reporting a critical regression.

## Priority core regression

1. Boot; note visible rainbow/startup text (unchanged, deferred polish).
2. Complete first boot: language, keyboard, timezone, owner password and Wi-Fi country.
   Confirm masked typing and plain ASCII ranges; owner username guidance must be clear.
3. Confirm the first Wi-Fi scan produces available networks or a truthful bounded error;
   connect, then reach Menu. Continuing offline is valid for the core lifecycle test.
4. Check Menu keyboard, default machine and compact status. Compare displayed IP(s) with
   Network Information. No connected interface must not show a stale address.
5. Ctrl+Alt+F2 to tty2; verify input, run `pcbm-diagnostics`; Ctrl+Alt+F1 back to Menu.
6. RUN: correct visible Cover, sane proportions, complete VICE canvas and keyboard.
7. Try Ctrl+Alt+F2 while VICE is active. **Known accepted limitation:** the pinned SDL
   console backend does not activate another VT from this shortcut. Record the outcome;
   this expected limitation alone is not a new core regression. Do not use a workaround.
   If it does switch, Ctrl+Alt+F1 must return to the same running VICE session.
8. F10 → Quit; verify immediate responsive Menu input, then both VT directions again.
9. Repeat the complete Cover/VICE/F10/Quit/Menu/VT lifecycle for three cycles. Preserve
   diagnostics before further launches if anything fails; launch evidence slots rotate.
10. Launch another machine/profile and verify its matching Cover. Change the RUN default,
    return to Main Menu and verify the displayed default and next RUN behavior.
11. Reboot safely: Wi-Fi/default preference persist, wizard does not rerun, status is current.

**On a new core regression, stop unrelated tests and collect evidence first.** Do not
repair the qualification card with reset/stty/chvt, service restarts, file edits or new
packages. Preserve fixed `pcbm-diagnostics`/engineering records before another launch.
Use the [read-only card collection policy](poc4-regression-collect-evidence.md) after
safe shutdown/removal; verify card identity before interpreting it. A still image does
not establish input responsiveness, audio or timing.

## Network identity and status

12. Confirm default Computer Name `projectcbm`. Change it under Network to a unique valid
    name, verify displayed name and local resolution, then keep that name for the tests.
    Invalid punctuation, `.local`, leading/trailing hyphens and overlong names must be rejected.
13. Check Network and System Information: current type, SSID where applicable, IP and
    detailed interface/MAC information agree. Unplug/disconnect/reconnect and refresh.
14. Where available, test Ethernet, Wi-Fi and both together; device names need not be
    eth0/wlan0. Check concise Main Menu versus detailed submenu presentation.
15. With Network Discovery on, test chosen-name.local resolution from another computer;
    if it fails, record the client/network and test the displayed IP fallback.
16. After reboot verify Computer Name, addresses and the intended service choices persist.

## Remote Access (SSH)

17. Open Services → Remote Access. Off offers Turn On; it should not also offer Turn Off.
18. Turn On. Confirm actual On after completion, and updated Main Menu/Services status.
    Pending/Failed/Unavailable must not be mislabeled On.
19. Verify Computer Name/IP, **owner** username, first-boot password guidance and generated
    SSH command are clear. The password itself must never appear.
20. From another computer, use the displayed command and first-boot owner password.
    Confirm an owner shell; verify authenticated administration where desired, then exit.
21. Reboot, check On and make a new client connection using the documented workflow.
22. Turn Off. Verify Off, the inverse action and disappearance from active Main Menu status.
23. Make a **new** connection from the client and verify it is refused/unavailable.
    Existing sessions do not establish whether new connections are allowed.

## File Sharing

24. Open File Sharing. Confirm username owner and explicit **separate password** guidance.
    Set it with visible masking; mismatch/cancel must not claim success.
25. Turn On and confirm the notice that Network Discovery also turns on. Verify actual
    On and Password: Set, without exposing the password.
26. Read How to connect: actual Computer Name/IP, username, share **Project CBM**, Mac
    URL and Windows path. No hard-coded old pcbm/raspberrypi name should remain.
27. macOS: Finder → Go → Connect to Server, using the displayed smb URL. Authenticate as
    owner with the sharing password, not an assumed Unix password.
28. Verify Finder discovery where supported. If absent, retain the failure separately
    from direct SMB success; test chosen-name.local and direct IP.
29. Windows if available: use the displayed File Explorer path, test authentication and
    direct access. Record browsing/discovery independently; automatic Network browsing
    is not guaranteed in this build (no WS-Discovery daemon).
30. Copy a small lawful test file into the share; verify it in CONTENT/FILES, read it
    back and compare. Confirm access is to content only, not the owner home or root.
31. Reboot; verify persisted On, credentials and access/content as intended.
32. Turn Off and verify actual Off plus refused new SMB access. Discovery is independently
    controlled and may remain On; it must not keep advertising a running SMB share.
33. Change the sharing password and verify the documented credential distinction. Never
    include either old/new secret in the test report.

## Remaining utilities and preferences

34. Toggle Network Discovery independently; verify actual status and name/discovery effects.
35. Midnight Commander: browse normal user content, F10 exit and responsive Menu return.
36. SID-Wizard: launch admitted disk, keyboard/audio behavior as available, F10/Quit return.
37. StrikeTerm: launch admitted private application. BBS connectivity is a separate test.
38. USB import: select device/category, import lawful small files, verify destination/count,
    repeat without overwriting existing content, wait for safe unmount before removal.
39. BBS / Modem where release-supported: turn on, verify local endpoint/settings and use
    an authorized BBS from the intended application; turn off and verify actual state.
40. Check relevant user/VICE preferences across another launch and reboot; report exactly
    which preferences were tested. Unreported audio/controllers/functions remain UNTESTED.
41. POWER shutdown; safely remove power/card. Retain the exact outcome and private evidence.

## After the report

A passing result can support the next dedicated **quiet boot + measured fast boot + RC
polish** milestone. It does not authorize publication, another model's qualification or
third-party redistribution. Record failures honestly; expected SDL-active VT limitation
and inconsistent platform browsing stay distinct from new regressions.
