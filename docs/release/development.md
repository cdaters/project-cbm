# Develop and contribute to Project CBM

[Documentation index](../README.md) · [Build Your Own](build-your-own.md) · [Customization](customization.md)

Start by using the appliance and reading the [User Manual](user-guide.md). A contributor
should know what a user sees before changing its implementation. Product and Menu are
separate repositories so presentation and system integration can evolve independently.

## Where a change belongs

| Concern | Source to start with | Responsibility |
| --- | --- | --- |
| Main Menu/CONTROL/CONTENT/IMPORT/FILES wording | Menu `scripts/` and `lib/` | Presentation and navigation |
| Network/system/service information | Product `runtime/project_cbm/info.py`, `network_info.py`, `service_info.py` | Read-only structured facts; Menu formats them |
| Machine selection | Product `runtime/data/profiles.json`, `profiles.py`, `preferences.py` | Validated registry and saved user choice |
| Content layout/import | Product `library.py`, `importer.py`; Menu content/import clients | One library policy, safe copies and truthful result display |
| Setup/configuration | Product `setup.py`, `configuration.py`, `config_backend.py`; Menu first-run/setup UI | Validate/apply fixed operations; protect secrets |
| Emulator launch | Menu `pcbm-run-vice`; Product `build/pigen/stage-cbm/files/engineering.py` | One unprivileged Cover/VICE/terminal-return path |
| Boot session/presentation | Product stage files `pcbm-console-session`, `boot_session.py`, getty/profile files | Existing Linux session ownership and ready-screen handoff |
| Packages/image integration | Product `build/packages`, `tools/install_poc_stage.py`; Menu `debian` | Component installation, first boot and assembled image |
| Practical documentation | Product `docs/release` | Current user/build/customization authority; Menu public-docs mirror is historical |

`pcbm-info` JSON is the information authority. Avoid duplicating shell probes in Menu.
A preference says what the user wants; observed service/listener state says what is
actually available. A configuration request passes through validated fixed helpers,
not an arbitrary root shell. Account role names such as owner are API concepts; the
normal Unix username is pcbm. See [accounts/layout](accounts-and-layout.md).

## Set up a checkout

Use sibling Product/Menu repositories as described in Build Your Own. Read both
AGENTS.md files for contribution rules and CURRENT-STATE.md for active work before editing;
inspect `git status` so you do not overwrite someone else's unfinished changes. Work on
a branch. No production Pi, installer, old release-prep script or documentation-sync
script should be used as a static test.

On your development host, create a Python environment for contract tests:

```sh
cd "$PROJECT_CBM_SRC"
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements-contracts.txt
```

Use the version requirements in the repository. A public checkout currently lacks the
unpublished 1.1 refs; [bootstrap status](../documentation/public-bootstrap.md) applies
to contributors too. Reading public 1.0 code is not testing the 1.1 implementation.

## Testing

With Product's Python environment active, run host tests from each repository:

```sh
cd "$PROJECT_CBM_SRC"
python3 -m unittest discover -s tests
cd "$PROJECT_CBM_MENU_SRC"
python3 -m unittest discover -s tests
```

For a narrow change, use its focused test module first. Check each changed Bash script
with `bash -n`, Python syntax/JSON schemas, diff whitespace, links, file sizes and secret
patterns. Documentation has a dedicated check:

```sh
cd "$PROJECT_CBM_SRC"
python3 tools/check_release_docs.py
```

Native Linux tests in `tests/native` exercise actual packages, accounts, services,
filesystems and pseudo-terminal behavior in guarded disposable environments. Read their
README first; never run them against your real appliance root or unisolated build host.
Physical tests are still needed for Pi keyboard, HDMI/KMS, audio, networking, USB and
speed. A dummy graphics/audio backend cannot establish those behaviors.

The [testing contract](../testing.md) explains what each layer proves. Use original test
media or separately permitted reference content. Do not redistribute a game/demo simply
because it was used to find a defect.

## Package and interface changes

Runtime and Menu have independent versions. Runtime exposes the API package dependency
used by Menu. A registry change can require Runtime only; UI code requires Menu; VICE
source/flags require its own package; installer-only changes require new image integration.
Rebuild changed components and verify unchanged package bytes when reusing them.

The Runtime recipe also installs `docs/release/*.md`. Documentation source changes do
not alter an already-built Runtime package or an existing image. Decide separately how
to distribute refreshed manuals or include them in a later authorized package release.
Do not pretend a repository documentation edit updates the Pi's installed manual.

For configuration work, read [configuration](../runtime/configuration-contract.md) and
[security](../security.md). For launch changes, read [Covers](../runtime/covers.md) and
[VICE](vice.md). Preserve saved preferences, user control, F10/Quit, complete aspect-correct
canvas and verified terminal restoration on both success and failure. Do not solve a
status/permission problem by widening passwordless sudo.

## Release and recovery

A release lock records exactly which source and packages built an image. It is useful
because otherwise an upstream update might silently change the next build. The factory
retains the corresponding bytes and build environment, checks the finished image, and
prepares a physical procedure that names that exact image hash. [Build and release](../build-and-release.md)
and [official walkthrough](../build/official-factory-walkthrough.md) give the full process.

Git bundles and external manifests preserve the source/inputs beyond one computer or
remote host. Recovery tests clone the bundles offline and compare refs, tags, files and
fsck results. An independent backup matters: another folder on the same disk is not
independent custody. [Engineering recovery](../recovery.md) is the technical authority.
Bit-for-bit reproducibility requires independent builds and comparison, not just a saved lock.

Make coherent commits with a verified author identity, update CURRENT-STATE and relevant
contracts, and leave exact tests/limitations for the next contributor. Do not amend
historical evidence to turn an earlier failure into a success. Publishing branches,
packages, images or third-party assets is a separate authorized release action.

## Design goals

Project CBM boots into a Commodore-focused appliance rather than a desktop. The Menu
covers ordinary tasks; Linux remains available for owners who want it. VICE provides
mature emulation, and portable content folders keep user data understandable. Local
setup/services avoid a cloud-account dependency. Fresh-image upgrades keep components
in a known combination while user backup/restore protects personal work. Explainable
builds and measured physical behavior matter more than adding general desktop features.

After time away, use CURRENT-STATE to locate the current source, candidate, pending
physical tests and recovery record. Check the actual checkout before trusting a dated
status paragraph. Then follow the user-facing task through the table above; there is
no need to reconstruct the project's conversation history.
