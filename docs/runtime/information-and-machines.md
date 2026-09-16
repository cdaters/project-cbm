# System Information and choosing a machine

Source implementation, 2026-09-16. These changes are **not installed in POC1–3**.
A future versioned package/image must include the matching product runtime and Menu.

## System Information

Choose **CONTROL → INFO — System Information**. The view groups build/component
versions, hardware, OS/storage/display and current configuration. Use Up/Down or
Page Up/Page Down to scroll. Enter on Back or Escape returns to CONTROL. Reopen the
view to refresh it; collection happens once per visit and does not need networking.

Missing facts appear as **Unavailable**, not errors or invented hardware details.
Built versions and currently installed package versions are distinct. A configured
boot mode does not establish the active boot behavior. The normal view does not
include raw diagnostics, credits or lengthy licenses. **SYSTEM → SHOW — About Project
CBM** remains the existing location for credits pending a separate cleanup; its legacy
version/network probes are not the information authority.

The view wraps long build IDs instead of discarding their ends. It supports 80×24
and larger consoles, and a scrolling layout down to 40×12. Smaller terminals get a
short explanation; use `pcbm-info` or enlarge the terminal. Fixture tests exercise
wrapping down to 20 columns, but the interactive minimum is 40. Resizing within an
open dialog is not qualified; reopen the view to measure the new dimensions.

For support, run `pcbm-info` or `pcbm-info --json` from a shell. Review hostname and
interface names before sharing. The UI itself sends nothing anywhere.

## Choose the default Commodore machine

1. Choose **MACHINES**. The current default is marked with `*`.
2. Choose **DEFAULT — Set the machine used by RUN**.
3. Select a machine. Saving returns to Main Menu, whose default label confirms it.
4. Choose **RUN** to launch that machine.

Selecting a machine directly from the first MACHINES screen launches it immediately
without changing your default. Back/Escape from the default selector leaves the
selection unchanged. F10 opens the VICE menu; Quit returns to Project CBM.
The default is also used by the existing content launcher. It does **not** select
a boot mode or change VICE's own saved video/audio preferences.

No sudo or administrator password is needed. Preferences belong to your normal user
in `~/.config/project-cbm/preferences.json` (or your absolute XDG_CONFIG_HOME).
On first use, an existing recognized legacy default is imported if the new file is
missing. The legacy file is retained; later legacy edits do not replace your choice.
Without either file, the recommended profile is Commodore 64 (`x64sc`).

If saved preferences are malformed, the screen explains that a safe fallback is in
use. Saving then asks whether to retain a private copy of malformed data and recover
preferences. **No** leaves the file unchanged. Recovery resets other invalid values
to defaults. Unsafe permissions, symlinks, oversized files or another active writer
can still prevent saving; check [recovery instructions](preferences.md), not sudoers.
