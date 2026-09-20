# Customize Project CBM

[Documentation index](../README.md) · [Build Your Own](build-your-own.md) · [Developer guide](development.md)

Start with settings on your Pi when they do what you need. You can change RUN's default,
Computer Name, Wi-Fi, services, audio and saved VICE settings without making an image.
You own the computer, including Linux. Source-based customization is for changing what
**a new image** installs or choosing different software/artwork.

The examples below are instructions for your own future derivative, not changes made
to the reviewed release candidate. Use source you are entitled to modify, a new branch
and your own versions. The current public image bootstrap is incomplete; the
[build guide](build-your-own.md) explains the exact boundary. These examples do not
pretend that editing a file alone produces an image.

## Before editing

Keep Product and Menu as sibling checkouts and set `PROJECT_CBM_SRC` and
`PROJECT_CBM_MENU_SRC` as in Build Your Own. All unprefixed source paths below are
relative to Product. `../project-cbm-menu/` means its sibling Menu checkout. Commit
or back up your work, then create a branch:

```sh
cd "$PROJECT_CBM_SRC"
git switch -c customize-my-cbm
```

Create a corresponding branch in Menu only if it changes. Run focused tests from the
[development guide](development.md#testing), rebuild the affected packages using the
[package walkthrough](build-your-own.md#native-linux-package-walkthrough), and assemble
an image through a supported build route when its required inputs are available.
The official route requires a new lock/output identity. Never overwrite an existing
release image/package with different bytes under the same name.

## Change the default Computer Name

**On your Pi:** CONTROL → Network → Computer Name → enter `mycbm`. No rebuild. Check
Network, SSH/sharing connection help and persistence after reboot. Enter only the base
name, not `mycbm.local`.

**For a fresh derivative:** edit `tools/install_poc_stage.py`. Its current lines write
`projectcbm` to `/etc/hostname` and replace/create the `127.0.1.1` entry in `/etc/hosts`.
Change all three hostname literals in that small block to `mycbm`, retaining the newline
and regular-expression behavior. Do not rename account `pcbm`; that is a different thing.

For example, the hostname write becomes:

```python
owned_put('/etc/hostname', 'mycbm\n')
```

The hosts replacement/fallback must likewise say `127.0.1.1\tmycbm`. Names start with a
lowercase letter, contain lowercase letters/digits/hyphens, end alphanumerically and fit
63 characters. Update derivative expected-default assertions. This changes image
integration, not Runtime/Menu binaries by itself; build a fresh image, then test both
hostname files, `.local` discovery, current-IP fallback and a user rename through CONTROL.

## Replace a machine Cover

Replace `../project-cbm-menu/covers/pcbmcover-c64.jpg` with your own licensed artwork.
The C64-family profiles share Cover ID `c64` in `runtime/data/profiles.json`; preserve
that mapping for a drop-in replacement. The installed file is
`/usr/share/project-cbm-menu/covers/pcbmcover-c64.jpg`.

The renderer accepts JPG/PNG, at most 2 MiB per image and dimensions no larger than 4096
pixels in either direction. It preserves proportions and centers artwork within its
available area; use the existing image's proportions as a starting point. Keeping the
JPG filename avoids changing mapping/packaging code. Do not rename PNG bytes to `.jpg`.

Read the new byte count/hash from Product's directory:

```sh
python3 - <<'PY2'
import hashlib
from pathlib import Path
p = Path('../project-cbm-menu/covers/pcbmcover-c64.jpg')
print(p.stat().st_size, hashlib.sha256(p.read_bytes()).hexdigest())
PY2
```

Update that entry in Menu `docs/cover-artwork.json`, including honest origin/license
information, and the derivative's image asset/input record. A new hash is not a rights
grant. Bump/rebuild **Menu**. Test `fit()`/renderer limits in Menu tests, missing-image
fallback, actual installed asset bytes and repeated physical Cover → VICE → Quit.
The seven mappings and primary artwork are listed in the [layout](accounts-and-layout.md)
and Menu artwork manifests. Craig Daters authorizes the supplied artwork with Project CBM 1.1.0; this is not a general MIT license for separate or modified artwork. Use your own licensed art for a derivative.

## Change the default machine

**On your Pi:** MACHINES → DEFAULT → Commodore VIC-20. The equivalent ordinary-user
commands are:

```sh
pcbm-preferences show
pcbm-preferences set default_machine xvic
pcbm-preferences set boot_preference menu
```

These preserve the distinction between RUN default and boot destination. No rebuild.

**For a fresh derivative:** set `default_machine` to `xvic` in
`build/pigen/defaults.json`; change the `/etc/pcbm/default-machine.conf` seed in
`tools/install_poc_stage.py` to `xvic`; and make `xvic` the sole `recommended: true`
profile in `runtime/data/profiles.json` (set x64sc false). Runtime's missing/invalid-state
fallback uses the recommended profile, while initial setup can import the legacy seed.
Changing only the JSON declaration would leave those other defaults inconsistent.
Rebuild **Runtime** for registry changes, plus new image integration. Test fresh setup,
RUN, valid saved C64 preferences still winning, and explicit malformed-preference recovery.

## Change a VICE default

**On your Pi:** use F10 → VICE settings and save the choice. Make a backup first.
Project CBM does not overwrite saved emulator settings at every launch.

**For a fresh derivative:** `tools/vice_presentation.py` generates the initial template.
For example, to start in a window-sized canvas rather than the current fullscreen
resource, change the generated `chip+'Fullscreen=1'` value to `chip+'Fullscreen=0'`.
Console SDL/KMS may still own the whole physical display; this is an emulator resource,
not a desktop window manager. Validate your actual intended display effect on hardware.

For a sound example, the existing C64/C64SC `SidResidSampling=1` selects interpolation.
Changing it to another VICE-supported method needs the corresponding VICE 3.10 resource
reference and a real-time/audio comparison; do not guess enum values. The generator's
output is `/usr/share/project-cbm/vice-defaults.ini`, seeded to absent user settings only.
Integration must be rebuilt into a new image; VICE binaries need no rebuild unless their
source/options change. Test new-user seeding and existing preferences remaining unchanged.
Use `tests/test_first_boot_geometry.py` and the performance/lifecycle checks in the
[VICE guide](vice.md), adapting expected defaults deliberately for your derivative.

## Add an application

**Personal C64 application:** place a legally obtained standard disk at
`/home/pcbm/content/programs/c64/MyEditor/MyEditor.d64`. CONTENT → PROGRAMS lists it,
selects C64 and uses normal VICE autostart. No new Menu entry, root permission or package
is necessary. Save work on your own writable disk and use F10 → Quit. Test load/save
and a second launch, not merely that the emulator opens.

**Application included in an image:** SID-Wizard demonstrates the current mechanism:
`build/optional/sid-wizard.json` records source/payload/license hashes and destination;
`tools/optional_software.py` constructs/installs/verifies the working disk; Runtime's
`applications.py` recognizes its folder and enforces a standard C64 D64 launch. A second
non-generic application is **not** added by inventing a JSON entry: the current validator,
lock schema/installer and application routing explicitly recognize particular inputs.
Add the new contract, source/license/template and tests together before using that route.
There is no general application plugin installer today.

For a normal disk whose generic C64 routing suffices, don't add special runtime logic.
For a host Linux utility, package it with normal permissions and add an unprivileged Menu
action only if useful. Follow the existing FILES/MC call-and-return pattern. Changes to
Runtime require its package; a new Menu action requires Menu; new content/installer input
requires a new image. Validate writable working copies, missing input, launch/return,
source/license availability and user ownership. The approved CCGMS-only disk is a concrete
example; its BSD notice and source are retained. A private admission of other software
is not a reusable redistribution permission for your derivative.

## Add a Debian package

To include `tree` as an example command-line utility, edit `tools/install_poc_stage.py`'s
explicit target `apt-get install -y --no-install-recommends` argument list and add `'tree'`
alongside its existing deliberate extras. This is the actual stage-cbm package location;
there is no separate stage-cbm package-list file to edit. If a component needs it at
runtime, add a Debian Depends in that component instead of an unrelated image extra.

An official offline build also needs tree's exact package/source and dependencies in its
input set before construction. Without them, the build must fail rather than download
something unexpected. A Menu entry is optional: an Advanced terminal can run `tree`
without one. No Runtime/Menu rebuild is needed for an installer-only extra; any changed
component dependency/action does require that package rebuild. Validate `dpkg-query -W tree`
on the resulting image, the package manifest, footprint, and command return. Do not install
it into a finished release image and continue calling the changed image the old release.

## Change first-boot defaults

To initialize a derivative timezone to `Europe/London`, change `timezone` in
`build/pigen/config.json` from `UTC`. This is the system's build-time default, not a
promise that every wizard choice is preselected the same way. Check Menu
`lib/pcbm-setup-ui.sh` for offered choices and `scripts/pcbm-first-run` for navigation.
The wizard's explicit user selection must still apply through Product `setup.py` and
`configuration.py`.

Build new integration; rebuild Menu if its offered choices/presentation changed, or
Runtime if accepted values/operations changed. Test a fresh card through setup, timezone
result, Back/Escape/resume, password masking, Wi-Fi and a subsequent boot. Never bake a
shared password, private Wi-Fi credentials or a setup-completed marker to skip the user.

## Change a service default

For your **own configured Pi**, CONTROL → Services changes and saves it; no image rebuild.
For a derivative, prefer optional services remaining off until the user requests them.
`build/pigen/defaults.json` describes intent, but changing its Boolean alone does not
activate anything. Installer presets/policy and Runtime setup/backend actions determine
when a service can actually run.

For example, discovery after setup needs coordinated changes in the installer and
`runtime/project_cbm/setup.py`/`config_backend.py`, with actual service-state checks through
`service_info.py`. Keep SSH/File Sharing credential setup coherent. This is an advanced
product change, not a one-line documented switch. Rebuild affected Runtime/integration,
test before setup, after setup, reboot persistence, listener state and Turn Off behavior.

## Change branding

Primary boot artwork is Menu `covers/pcbmcover1.jpg`, recorded by `docs/primary-artwork.json`.
Machine Covers use `covers/pcbmcover-*.jpg` and their separate manifest. Replace licensed
art using the Cover process above. Main Menu wording/title is in Menu `scripts/pcbm-menu`;
shared dialogs/status text also live in `scripts/` and `lib/`. Use your own product name
without removing required upstream attribution.

Image name/date live in Product `build/pigen/config.json`; the export suffix is in
`build/pigen/stage-cbm/EXPORT_IMAGE`. Installed product metadata comes from the build
record, not a hand-edited finished `/usr/share/project-cbm/identity.json`. The current
private constructor restricts candidate families, so a general derivative identity needs
an explicit tooling change after the public bootstrap gap is addressed. Do not claim
that changing only a filename changes the installed identity.

Rebuild Menu for art/UI changes and any changed Runtime documentation/payload. Create
new integration/input records and an image through the supported route. Check screen fit,
Covers/boot handoff, About/version/filenames and rights as well as appearance.

## Adding machine profiles and modifying the stage

The existing C128 VDC profile illustrates the registry fields: ID `x128-80col`, executable
`x128`, chips VICII/VDC, option `-80col` and Cover `c128`. It is already present. You cannot
add arbitrary IDs/options simply by duplicating that JSON: `runtime/project_cbm/data.py`
and the profile schema constrain executables and flags. A genuinely new profile needs
matching validator, content-family routing, Menu consumption and tests; Runtime must be
rebuilt. Reuse the shared launcher and existing machine Cover mapping where appropriate.

`build/pigen/stage-cbm/00-cbm/00-run.sh` invokes the target installer after `prerun.sh`
copies the previous filesystem. Most deliberate package/default changes belong in that
installer. New numbered steps must distinguish the builder from `ROOTFS_DIR`; use the
sanitized target environment. The [factory guide](factory.md) shows where your change runs.

## What deserves extra care

Content, normal preferences and original artwork are the easiest changes to understand.
Package composition, profiles and first boot need fresh-image validation. Tty/getty/PAM,
privileged helpers, the shared VICE lifecycle and release/recovery records affect whether
you retain input, return safely, protect passwords and know what you built. Test those
changes more deeply; they are not forbidden, but their consequences extend beyond one screen.

Another retro appliance could reuse this pattern: small Linux base, local setup, separate
UI/runtime, understandable content, limited privileged operations, explainable builds and
physical tests. Project CBM remains the worked example, not a generic framework dependency.
