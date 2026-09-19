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
VICE binary, Cover mapping, data requirements and tests. The current C64 default retains x64sc with portable optimization and reSID
interpolation, subject to minimum-hardware performance qualification. A derivative
changing that choice must document its measured compatibility/fidelity tradeoff. VICE owns its
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

## Worked source changes

Use a branch in your own repositories, a new package version for changed components,
and a new image identity. Never edit a finished image and keep calling it the old build.
The paths below are relative to Product unless prefixed with `../project-cbm-menu`.
Run the relevant source tests, package tests, actual-image validation and physical
checks after each kind of change. The [build guide](build-your-own.md) explains which
parts of the public bootstrap remain to be supplied; a private predecessor kit is not
an assumed public prerequisite for reading or changing these recipes.

### Replace a C64 Cover and change branding

Put artwork you have rights to at
`../project-cbm-menu/covers/pcbmcover-c64.jpg`. Keep the `c64` Cover identity in
`runtime/data/profiles.json`; the other C64-family profiles intentionally share it.
The installed file is `/usr/share/project-cbm-menu/covers/pcbmcover-c64.jpg`.
Update that file's `size_bytes` and `sha256` in Menu's `docs/cover-artwork.json` and
record your actual provenance/license. This small read-only command obtains the values:

```sh
python3 - <<'PY'
import hashlib
from pathlib import Path
p=Path('../project-cbm-menu/covers/pcbmcover-c64.jpg')
print(p.stat().st_size, hashlib.sha256(p.read_bytes()).hexdigest())
PY
```

Changing a JSON hash does not grant artwork rights. Update the asset/admission records
in your new lock and corresponding source, rebuild Menu, and inspect the image's Cover
bytes plus physical aspect/presentation. Test failure/timeout cleanup as well as the
happy path. Do not change terminal or display modes to accommodate your replacement.

The Main Menu title is in Menu `scripts/pcbm-menu`; the Cover renderer window title is
in `lib/pcbm_cover_view.py`. Image naming is in Product `build/pigen/config.json`.
Change those sources, update your product identity/documentation, rebuild Menu where
changed and freeze new integration. Cosmetic branding still needs screen-fit checks on
small terminals and the Pi. Keep upstream notices and third-party attribution.

### Change the Computer Name or default machine

On a running appliance use CONTROL → Network → Computer Name. This safely validates
and writes the setting; no image rebuild is needed. For a derivative whose fresh default
is `mycbm`, change the `/etc/hostname` and `127.0.1.1` values in
`tools/install_poc_stage.py`. Use lowercase letters/digits/hyphens, no leading/trailing
hyphen, and stay within the backend's length limit. Do not bake a `.local` suffix into
`/etc/hostname`; discovery adds that addressing convention. Adjust your expected-default
validation/tests and build new integration. Check name resolution, SSH/SMB examples and
reboot persistence on the resulting system.

For your own current console user, the supported preference commands are:

```sh
pcbm-preferences show
pcbm-preferences set default_machine xvic
pcbm-preferences set boot_preference menu
```

Run these in the appliance user's context; an administrator's separate home is not the
console's preference store. Normally MACHINES/CONTROL handle that context for you.
To ship VIC-20 as a derivative default, change `default_machine` in
`build/pigen/defaults.json`, seed `xvic` in `/etc/pcbm/default-machine.conf` from
`tools/install_poc_stage.py`, and make the `xvic` registry entry the sole recommended
profile if that is your intended fallback too. Runtime's validator requires exactly one
recommended profile. Rebuild Runtime for registry changes, freeze integration, and test
fresh initialization, saved user choice, missing/invalid preference recovery and RUN.
Existing valid saved preferences should continue to win over a changed factory default.

### Add or alter a machine profile

Here is the existing C128 80-column pattern, showing all required fields:

```json
{
  "id": "x128-80col",
  "name": "Commodore 128 (80-column)",
  "executable": "x128",
  "description": "C128 with the VDC 80-column display",
  "video_chips": ["VICII", "VDC"],
  "recommended": false,
  "launch_options": ["-80col"],
  "cover_asset": "c128"
}
```

Do not insert a duplicate of that profile into the current registry. For a new profile
such as a deliberate `x64ntsc` alias, add its entry to `runtime/data/profiles.json` and
extend the explicit ID→executable/options validation in `runtime/project_cbm/data.py`
to admit only `x64ntsc`→`x64sc` with `['-ntsc']`. Add that option list to
`schemas/machine-profiles.schema.json`. The existing validator otherwise requires the
ID to match the executable, except for the C128 pattern; changing only the JSON will
correctly fail. Review Menu's profile consumption and add a focused test showing the
exact argument array and rejection of shell strings/unknown options. Keep the shared
launcher and Cover mapping. Rebuild Runtime and any actually changed Menu code, verify
the installed executable/resources, then qualify timing, keyboard, display and return.
This is an advanced source extension, not an unrestricted command-line profile feature.

### Change VICE defaults

For a personal change, use F10 and save resources in VICE. For fresh-image defaults,
edit `tools/vice_presentation.py`, which generates both the system template and the
initial user configuration. For example, selecting `SidResidSampling=2` for C64/C64SC
restores the more expensive resampling method; the current floor-oriented seed uses
interpolation value 1. Keep user configuration creation exclusive so an existing saved
file is never overwritten. Update `tests/test_poc3.py` and performance expectations,
freeze new integration, and repeat the minimum-hardware workload checks. A resource
change does not require recompiling VICE, but a change to its patches/build flags does.
Changing the SID engine, true-drive emulation or core has broader compatibility costs
than changing a display preference; document and test those costs.

### Add content or another application

Ordinary personal content needs no package change: import or transfer it to the right
`/home/pi/pcbm` category. For distributable content in a derivative, establish its rights,
retain exact payload/source/license bytes and use a manifest rather than a download
script that fetches unpinned files during boot.

SID-Wizard demonstrates the application pattern: inspect `build/optional/sid-wizard.json`,
its Product installation/verification tools and `runtime/project_cbm/applications.py`.
The immutable application template/manifests live under `/usr/share/project-cbm/applications`;
the user works on a copy. For another C64 disk application, add an explicit admitted
application identity, disk/source/license hashes and a working-copy path, route launch
through the existing VICE profile, and test missing/changed template and writable-copy
behavior. Add a Menu entry only if needed; do not execute an arbitrary package-supplied
shell string as root. Rebuild the changed Runtime/Menu package and freeze the application
inputs. StrikeTerm's private admission cannot be reused as a public rights grant.

### Add a Debian package

For a simple command-line utility such as `tree`, add its deliberate installation to
`tools/install_poc_stage.py`'s target `apt-get install --no-install-recommends` list, or
to the relevant component's Debian Depends if that component actually requires it.
Acquire its exact binary, corresponding source and dependency closure through the
retention process before freezing. The current image constructor is offline and must
reject a new package missing from the kit. If you expose it in Menu, add a bounded
unprivileged action and rebuild Menu too. Verify the resulting installed package/version/
architecture in the generated manifest, ELF closure where applicable, image footprint
and actual utility return. Do not run `apt install` against a sealed image to bypass the
new-input identity or record a today's-mirror package as an old pin.

### First-boot and service defaults

Bootstrap locale/timezone/keyboard values are in `build/pigen/config.json`; the choices
and first-boot orchestration are in Menu `lib/pcbm-setup-ui.sh` and
`scripts/pcbm-first-run`. Product `runtime/project_cbm/setup.py` owns accepted setup
steps and readiness, while `configuration.py` validates values and `config_backend.py`
performs fixed operations. For example, change a derivative's initial timezone from
UTC to `Europe/London` in the pi-gen config, then test the wizard's chosen/default value
and the installed `/etc/localtime`; changing only a label would not change the system.
Do not pre-complete password setup or store a chosen password in the image.

Service defaults are coordinated: `build/pigen/defaults.json` declares intent;
`tools/install_poc_stage.py` installs unit presets, policy and initial network state;
`runtime/project_cbm/service_info.py` reports observed readiness. If a derivative changes
a service default, update those together and test actual listener state before and after
first boot/reboot. For example, changing Avahi discovery to start after completed setup
requires a deliberate setup/backend action in addition to a manifest Boolean. Retain
explicit Remote Access/File Sharing opt-in and credential gates unless your derivative
consciously adopts and documents a different exposure model. Never make a status label
say On merely because you changed a default.

### Modify stage-cbm and produce the image

Add a numbered stage action only when the existing installer is not the appropriate
owner. `stage-cbm/prerun.sh` copies the previous filesystem; `00-cbm/00-run.sh` calls
`install_poc_stage.py` with the frozen lock and target. Use `ROOTFS_DIR` for target paths,
sanitized target-local `/tmp`, and retained package inputs. A command running on the
builder is not automatically running inside the target. Do not accidentally change the
builder's `/etc`, accounts or services.

After your edits, run source/focused/native checks, commit clean sources, rebuild only
changed components, retain exact inputs and create a distinct lock. The image factory
then constructs a fresh filesystem and exports raw/XZ artifacts. Verify installed
identity, package manifest, filesystems, ELF closure, accounts/services and raw/XZ hash
equivalence; create recovery and perform physical qualification. The [build walkthrough](build-your-own.md)
provides the actual existing commands and its current public-bootstrap limits.
