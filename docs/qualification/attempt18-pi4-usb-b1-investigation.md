# Attempt18 Pi 4 USB browsing defect — read-only investigation

**B1: FAIL**, reported by the owner on September 25, 2026. Normal FILES Midnight
Commander works; FILES → USB Drive → real partition → Mount Read-Only opens MC but
arrows echo escape characters, Tab/function keys fail, and Ctrl+C returns to Main
Menu. The [structured physical report](attempt18-pi4-usb-b1-failure-2026-09-25.json)
binds the observation to attempt18's exact artifact hashes. This supersedes the
earlier UNTESTED status for B1 only; it does not invalidate or relabel historical
offline passes. No image, runtime or USB modification has been made.

## Confirmed inspection

- Read-only SSH identifies Raspberry Pi 4 Model B Rev 1.4. Installed identity and
  build lock match attempt18. Runtime/Menu versions match; six relevant installed
  launch files hash identically to the inspected repositories.
- MC is `3:4.8.33-1+deb13u1`; sudo is `1.9.16p2-3+deb13u2`. Console session TERM is
  `linux`; that terminfo entry is installed. This does not yet compare MC's own
  environment in the two live states.
- `sudo -n -l` confirms `use_pty`. A privileged read-only /proc collector was refused
  because administrative authentication was not cached. No bypass was attempted.
  Unprivileged inspection succeeds but cannot inspect every root process descriptor.
- At the initial 23:43 UTC inspection and subsequent baseline checks, the Pi is at Main Menu, with no active MC/browse broker. The
  browse mount is absent and the exFAT USB partition has no mountpoint. This supports
  successful release following the reported Ctrl+C exit. The directory's continued
  existence is not a mounted filesystem. No agent unmount was needed/performed.
- Baseline tty1 while dialog is open is noncanonical/no-echo. That is a baseline,
  **not** the terminal state during broken USB MC. No stale-mode diagnosis can be
  made from it. The owner has been asked to leave ordinary MC open for comparison;
  both live MC snapshots remain pending.

## Launch-path difference and suspected cause

Normal Menu `scripts/pcbm-files:8` launches MC directly, inheriting the console.
USB `scripts/pcbm-usb-browse:18` starts the ingest bridge in the background with
stdin/stdout redirected to FIFOs and stderr to `/dev/null`. Product
`runtime/bin/pcbm-ingest-session` execs sudo and the fixed broker. The broker forks
and drops to UID/GID1000. `runtime/project_cbm/usb_browse.py:32` opens `/dev/tty` and
binds MC's three standard descriptors to it.

Therefore MC is not intentionally receiving the JSON pipes. The important question
is **which controlling terminal `/dev/tty` resolves to after sudo**. With `use_pty`,
the installed chain can add a sudo-owned session/PTY and terminal proxy. The direct
path and old native test do not have that boundary.

The matching upstream sudo source at
[exec_pty.c](https://github.com/sudo-project/sudo/blob/SUDO_1_9_16p2/src/exec_pty.c#L1208)
sets CD_EXEC_BG for FIFO standard streams and defers the initial raw-mode setup
(lines 1308–1312). It also controls forwarding based on foreground/raw state.
This supports a **suspected sudo/FIFO/terminal-ownership mismatch**: MC may configure
an inner PTY while the physical console remains cooked or input is not forwarded.
Debian patches and the exact live process states have not yet been compared.
The escape echo and Ctrl+C behavior fit this mechanism; they do not uniquely prove it.

The exact root cause must remain **UNCONFIRMED** until the normal and failing MC
snapshots identify their sessions, foreground groups, descriptors and termios.
No TERM-only fix, manual stty repair, sudo-policy change or live workaround is justified.

## Why the automated evidence did not cover this path

`tests/native/usb_browse.py` first uses `pty.fork()` and calls `usb_browse.browse`
directly. Its second section invokes `importer.perform` directly with synthetic
protocol pipes. Neither traverses the installed Menu → FIFO → ingest bridge →
sudo/use_pty chain. Both arrange their own controlling terminal. They send F10/Enter
and check output volume, return, cancellation and mount release; they do not assert
Up/Down selection changes or Tab panel changes. Unit tests mock Popen and terminal
opening. Thus the retained native PASS is narrower than complete physical B1.

Retained installed native logs were inspected, not rerun. The test gap is confirmed
even while the live failure mechanism remains under investigation.

## Conditional fix and required regression coverage

If the PTY mismatch is confirmed, the smallest fix that preserves the security
boundary is to put interactive MC ownership on the unprivileged caller side of
sudo, with direct attachment to the caller's existing terminal. Keep the fixed
broker responsible for the read-only mount lease and verified unmount result.
Preserve supervised child cleanup, cancellation and truthful safe-removal results.
This is a source-fix proposal, not an implementation or a finalized minimal diff.
Do not disable use_pty, broaden sudo or proxy MC keystrokes over the JSON channel.

Required tests must traverse the actual installed wrappers and sudo policy, with
TERM=linux and a real controlling PTY. Assert MC descriptor/foreground ownership,
outer terminal mode during navigation, Up/Down selection changes, Tab panel changes,
F10 return, Ctrl+C/HUP/client-disconnect cleanup, no remaining child, verified
read-only mount options and confirmed release. Include repeated browse, busy-unmount
failure without a false safe-removal claim, and ordinary MC regression. Physical
Pi 4 retesting remains required; successful synthetic PTY tests cannot replace it.

A source correction requires rebuilt affected packages and a **new distinct private
candidate/image** before qualification. Attempt18 must remain unchanged as evidence;
it cannot become a passing qualification artifact through an in-place patch.

## Next action and preservation

Owner opens ordinary MC and leaves it open. Capture read-only process/fd/environment/
termios state; then request owner-driven USB reproduction, capture the failure,
and observe Ctrl+C cleanup. Do not send navigation keys, mount media or modify the
live Pi through this investigation. Administrative access may be needed only if
the required descriptor snapshots are denied; never request the password itself.

Evidence: `qualification/attempt18-pi4-usb-browse-defect-2026-09-25` under configured
bulk storage. Initial read-only evidence is retained; follow-up captures must use
new filenames/checkpoints. This is an incomplete investigation, with no claimed
fix or successful reproduction by the agent. Earlier build/image artifacts, tags,
Menu source, unknown local work and all other physical results remain unchanged.
