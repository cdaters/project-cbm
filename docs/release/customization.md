# Customize your Project CBM image

You own your Raspberry Pi. These levels explain the consequences of a change, not
restrictions on your ability to administer Linux. Start with user preferences when
possible; image changes use the [build workflow](build-your-own.md) and a new identity.

## Intended everyday customization

- **Default machine and startup:** MACHINES saves the RUN default. CONTROL → Machine
  and Startup selects Menu or emulator boot. Preferences are validated, atomic and
  user-owned; valid new state wins over one-time legacy import.
- **Computer Name:** CONTROL → Network changes projectcbm using validated syntax.
- **Content:** import or share files into `/home/pi/pcbm`; bring your own lawful library.
  Do not add games, demos, ROMs or music merely because a reference archive contains them.
- **Covers and branding in a derivative:** Menu owns seven mapped artwork files. Replace
  artwork you have rights to in your own source, preserve registry mapping/filenames or
  update both deliberately, recalculate `docs/cover-artwork.json` and the corresponding
  rights/source records, version/package Menu, and freeze a new candidate. The current
  private helper intentionally rejects changed artwork against the existing manifest.
  Update that manifest/admission explicitly; never overwrite a frozen Cover object.
  UI titles live in Menu scripts; image name/defaults live in Product pi-gen configuration.

## Advanced image customization

Machine definitions are in Product `runtime/data/profiles.json`; Menu consumes the
validated registry through the runtime interface. Add a profile only with the correct
VICE binary, Cover mapping, data requirements and tests. Keep x64sc as the accurate
C64 default unless your derivative deliberately makes another choice. VICE owns its
emulation geometry and user preferences; ordinary preference changes should use VICE,
not framebuffer/resolution workarounds in the launcher.

For first-boot or service defaults, inspect `runtime/project_cbm/setup.py`, the fixed
configuration backend/policy and `tools/install_poc_stage.py`. The default Computer Name
is seeded by that stage; runtime changes remain user-owned. Do not place a factory
password, private Wi-Fi profile or developer SSH key in source. Complete setup gates
and explicit opt-in services must remain coherent with your selected defaults.

Add optional applications through the [application contract](../runtime/optional-applications-contract.md):
retain source, license, payload/recipe hashes, registry/launcher integration and rights
classification. SID-Wizard already has established admission. StrikeTerm remains private
engineering with a public-release rights gate. Owner-supplied SID/demo references do not
become redistributable by being included in a development workspace.

Adding a Debian package changes the authenticated binary/source closure and often
footprint/ELF dependencies. Acquire and retain exact inputs before frozen assembly;
update `build/pigen/stage-cbm` and its install recipe as appropriate. Never install into
a finished image and claim the old lock. Version only changed components, freeze clean
source and re-run actual-image and relevant physical tests. See [factory](factory.md).

## Core components deserve extra care

Console getty/login/PAM owns the session; the shared launcher supervises Covers,
restores terminal state and launches VICE unprivileged. Changes can leave input or
Menu return broken even when a headless test passes. Preserve F10, bounded child cleanup,
full aspect-correct canvas and terminal restoration across failures and repeated launches.

The privileged backend accepts a fixed typed request contract. Broad sudo commands,
shell interpolation or credential argv/logging expand the trust boundary. The information
service is read-only and structured; adding duplicate Menu probes creates conflicting
state. Release locks, immutable attempts and recovery manifests make results attributable;
weakening them makes later diagnosis and rebuilds unreliable. These areas require focused
Linux tests and a new physical qualification, not just a successful package install.

## Derivative appliance pattern

A derivative can reuse the design: minimal supported base, local first boot, separately
versioned UI/runtime, structured configuration authority, constrained operations,
explicit content/application integration, frozen factory inputs, offline validation,
recovery and model-specific physical qualification. Project CBM demonstrates that pattern;
it is not a generic appliance framework or a license grant for every bundled component.
Keep your derivative identity, rights and qualification honest, and retain user control.
