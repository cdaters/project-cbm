# Startup artwork and recovery display

[Documentation index](../README.md) · [Getting Started](getting-started.md)

Project CBM displays its own startup artwork while preparing the appliance. On a fresh
image it hands over to First Boot Setup, then Main Menu. On later boots it proceeds to
Main Menu, or the selected default emulator if you changed Boot preference.

The artwork is intended to remain visible until the next meaningful screen is ready,
with about three seconds minimum once displayed. Setup should not be followed by another
startup splash. Machine Covers are separate and appear when launching an emulator.
Some early black-screen time while video starts is normal. Monitor-generated HDMI/input
popups belong to the display, not Project CBM.

Routine successful filesystem/login output is suppressed. Actual filesystem checks
still run, and errors can remain visible. Final physical presentation/timing is being
qualified; no instant-on or fixed boot-time claim is made. SD card, model and peripherals
can affect time to the first usable screen.

## Verbose recovery

Start with [user troubleshooting](troubleshooting.md). For advanced investigation,
Ctrl+Alt+F2 from Project CBM reaches the console and Ctrl+Alt+F1 returns. Quit VICE first.
SSH works when Remote Access was enabled. Numeric startup traces live under
`/home/pcbm/.local/state/project-cbm/boot`; renderer diagnostics are in
`/home/pcbm/.local/state/project-cbm/diagnostics/primary-presentation.json` when available.

If you need more visible startup detail on your own system, back up
`/boot/firmware/cmdline.txt`, then remove `quiet`, `loglevel=4` and
`systemd.show_status=auto` from its **single line**. Preserve root/console and other
parameters. This restores the verbose path; do not split the file into multiple lines.
You can edit that firmware-partition file on another computer after safe shutdown if
the Pi cannot reach a shell. Restore the saved file to return to normal presentation.
During release testing, preserve the failure evidence before altering the test card.

For developers, compare power-on-to-interactive-Menu observation with boot phase traces;
`dialog_dispatch` is a software boundary and `first_input` records the first completed
interaction, not the moment the display became usable. Do not add concurrent systemd
unit durations. The [developer guide](development.md) links the lifecycle contracts.
