# Configuration maturation checkpoint — 2026-09-16

**Source pass complete; stop for owner review.** This is the last concentrated
Menu/configuration architecture pass. Retain Bash/dialog and move forward with product
runtime integration. No new Menu framework study is recommended.

Read [the user guide](pcbm-config.md) and [implementation/activation contract](configuration-contract.md).

## What changed

CONTROL now opens one task-oriented pcbm-config. The nine areas cover Machine and
Startup; Picture, Sound and Controllers; Language, Keyboard and Region; Network;
Services; Content and Storage; System Information; About; Advanced. Info/About use
the existing JSON authority, not new Linux/version probes. User machine preferences
and registry-based RUN remain intact.

Concrete before → after improvements:

- Separate old SYSTEM/NETWORK/BBS scripts and stale status logic → thin compatibility
  routes into one configuration controller and one information authority.
- QUIT followed by an unexpected session restart → Advanced Terminal; `exit` returns
  to the waiting UI. POWER/REBOOT remain familiar Main Menu shortcuts, not duplicates.
- Broad or unsupported passwordless commands → typed, validated fixed operations,
  explicit runtime readiness, and a separate authenticated owner path.
- Sourced audio shell configuration → data-only bounded parsing and atomic user save.
- Generic mount/ROM helpers → clear pending safe import with a complete constrained
  storage contract; authenticated owner file administration remains available.
- Extra save acknowledgments → concise result in the next menu; uncertain operations
  say to inspect current state rather than falsely claiming success.

No new resident service, UI framework, network stack, mouse requirement or dependency
stack. Ordinary operations use user preferences where possible. Advanced owners retain
normal Debian/PAM/sudo administration; there is no universal password or root shortcut.

## Implemented versus pending

Implemented and fixture-tested: UI navigation/results; information/About formatting;
user machine and boot-intent saves; audio data handling; JSON schemas/client/backend;
fixed hostname, locale, next-boot keyboard, timezone, Wi-Fi country/enrollment, service,
Samba credential and power adapters; typed modem intent; returning terminal and
separately authenticated owner/raspi-config dispatch.

**PENDING RUNTIME ACTIVATION:** matching versioned product/Menu package installation,
root-owned policy/helper/sudoers validation, first-boot account and authentication setup,
network and individual service readiness, native Linux operations and real console UI.
No readiness policy or sudoers rule is installed by this pass. Saved boot intent needs
its single session consumer; modem intent needs its fixed TCPser argv/listener adapter;
safe automatic USB import needs the constrained storage broker. These are concrete
product integration/implementation gates, not disguised completed runtime functionality.
First-boot, broker, modem and service requirements are detailed in the contract.

The existing POC3 tty/getty/PAM/session, launcher, VICE geometry, qualification media,
service masks and image inputs remain unchanged. New source is not covered by POC3's
Pi 3B pass. Independent clean-rebuild reproducibility and other hardware qualification
remain unproven. No build, physical testing, service activation, optional software,
boot optimization, push or publication occurred.

## Validation and cost

[Machine-readable validation](configuration-validation.json),
[configuration timings](configuration-performance.json),
[info/registry/preference timings](configuration-consumers-performance.json).

108 product tests and 43 Menu tests pass, plus the included shared-launcher checker.
The suites cover injection/unknown operations/units/paths; readiness; secret redaction;
Samba/Unix separation; locale/keyboard/catalog checks; atomic writes; malformed state;
Cancel/Back/Escape; typed saved versus applied results; Info/About missing values and
width; existing preference/machine/launcher and POC3 source regressions.

Mac ARM64/Python 3.14.5 medians: configuration open/Back 13.17 ms; region open/Back
28.69 ms; About 58.54 ms; fixture hostname submission 90.12 ms. Cold validation CLI
35.15 ms, observed peak 20.05 MiB. Info CLI 40.90 ms; registry validation 0.075 ms;
preference read 0.028 ms/write 0.211 ms. Fake dialogs/adapters do not measure real
rendering or Linux mutations. Maxima are retained (including cold-process outliers).
Pi 3 performance and Pi 3A+ memory budgets still require actual measurement.

Syntax/schema/link/size/private-pattern/ref checks and sudoers syntax validation pass.
ShellCheck is unavailable. No real dialog, native Linux install or physical test was
performed. Fixtures are synthetic, not credentials or retained appliance extracts.

## Recovery and exact continuation

Source branches: product `feature/1.1-build-foundation`, Menu
`feature/1.1-debian-package`. Input commits were product
`dbffa305cb70559444999d73bbbeb80f81e95897` and Menu
`4feda57c2ff1f5d0807a6873c0b88b5d84435bd8`.
Menu output commit: `87a16af19e7329b7cf8dbc16ee9420613f35245f`.
The Git commit containing this checkpoint is the exact product source output; its
external manifest records that hash and the exact Menu output without a self-reference.

Configured bulk storage: `archive/configuration-maturation-2026-09-16/` contains
both all-ref Git bundles, ref inventories, offline restored mirrors, fsck/restore
reports and SHA-256 manifest. Adjacent qualification evidence:
`qualification/configuration-maturation-2026-09-16/`. Preservation rechecked 5,503
POC1/2 baseline entries, 2,789 POC3 frozen input objects and exact POC3 lock/raw/XZ
hashes. Earlier checkpoint bundles, tags, historical records and artifact bytes remain
unchanged. No image/photo duplication. Same-device recovery is **not** independent
backup; custody/signing and independent rebuild remain open.

**Exact next product milestone:** owner-authorized first-boot/owner-account and runtime
activation integration. Install new versioned source into a disposable Linux staging
target; verify authentication, helper trust/privilege rules, region/hostname, explicit
offline/network choice and per-service credential/readiness behavior. Integrate/test
single boot-preference consumption and the required TCPser/storage adapters before
claiming their features usable. Only a later explicitly authorized frozen candidate
may carry these changes for Pi 3B regression/activation qualification. Do not build
POC4 or activate POC3 in this checkpoint. Defer additional Pi models, boot optimization,
StrikeTerm/SID-Wizard and broad feature work until their own product gates.
