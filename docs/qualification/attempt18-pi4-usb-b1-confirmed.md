# Attempt18 Pi 4 B1: confirmed terminal ownership defect

September 25, 2026 (Phoenix; cleanup capture September 26 UTC). This supplements
the [initial investigation](attempt18-pi4-usb-b1-investigation.md), whose pending
statements describe the earlier checkpoint. **B1 remains FAIL.** No repair was
performed on the qualification Pi or USB. Artifact binding remains the
[original owner report](attempt18-pi4-usb-b1-failure-2026-09-25.json).

## Live comparison

The owner opened normal MC, then the failing USB MC, then pressed Ctrl+C. Read-only
SSH collected process/session/group, standard descriptors, allowlisted environment,
termios and mount state. The three retained snapshots are `normal-mc.json`,
`usb-mc.json` and `after-ctrl-c.json` in
`qualification/attempt18-pi4-usb-browse-live-2026-09-25` under bulk storage.

| Observation | Normal MC, 23:56:04 UTC | USB MC, 23:58:30 UTC |
| --- | --- | --- |
| MC PID | 3330 | 3442 |
| Controlling terminal | tty1 | pts/0, created through sudo |
| SID / PGID / foreground TPGID | 2058 / 2058 / 2058 | 3426 / 3427 / 3426 |
| Standard descriptors 0/1/2 | /dev/tty1 | /dev/tty, resolving in the inner session |
| Physical tty1 canonical / echo | off / off | on / on |
| Physical tty1 interrupt key | Ctrl+G | Ctrl+C |
| TERM | linux | linux |

The sudo monitor owns the inner PTY foreground group; MC is in another group.
The physical console remains cooked, echoing control sequences instead of providing
MC's expected immediate keyboard input. This is the concrete root cause of the
arrow/Tab/function-key failure. Ctrl+C is handled through the outer console workflow
and aborts it. The precise inner-PTY termios and root-process descriptors were denied
to the unprivileged collector; they are not claimed as measured.

Normal FILES launches `/usr/bin/mc` directly from Menu `scripts/pcbm-files:8`.
USB Menu `scripts/pcbm-usb-browse:18` starts a background FIFO protocol bridge;
Product `runtime/bin/pcbm-ingest-session` execs sudo with `use_pty`; the broker forks
an unprivileged worker; `runtime/project_cbm/usb_browse.py:32` opens `/dev/tty` there.
That terminal is sudo's inner PTY, not the original console. MC's standard streams
are attached to a real terminal, **not the JSON FIFOs**. The unwanted sudo terminal
proxy and changed foreground/session ownership are the defect.

The retained matching upstream sudo `exec_pty.c` explains why FIFO stdin/stdout
select background execution and defer initial raw mode. The live installed result
establishes the behavior independently of any unexamined downstream patch details.
The same installed MC and TERM/terminfo work in the direct path. USB MC's restricted
PATH, C.UTF-8 locale, HOME and dropped supplementary groups differ from normal MC,
but do not explain the observed foreground/cooked-terminal mismatch.

## Cleanup and safe removal

At 00:01:52 UTC after the owner's Ctrl+C, the browse mount was absent, the USB
partition was unmounted, MC and its broker were gone, and no accessible process
held the browse path. The owner confirmed return to Main Menu. tty1 was again
noncanonical/no-echo for dialog. This observed browse lease was successfully released;
the USB was safe to remove from this workflow at that snapshot. This does not claim
a complete privileged audit of unrelated raw-device descriptors or promise safety
after a later remount.

## Fix scope and regression gap

The smallest safe source correction is to keep MC on the unprivileged **caller side
of sudo**, attached directly to that caller's controlling terminal and foreground
group. Keep the fixed privileged broker responsible for the read-only mount lease,
bounded worker supervision and verified release. The bridge/protocol must explicitly
hand off browse-ready and hold/release ownership without sending terminal bytes
through protocol FIFOs. Preserve cancellation, parent-death cleanup and truthful
busy-unmount errors. This is a proposed correction, not an implemented minimal diff.
Disabling `use_pty`, broadening sudo, manual stty repair or weakening mounts is not
needed to correct this ownership error.

`tests/native/usb_browse.py` calls the browser and `importer.perform` directly in
synthetic PTYs, bypassing the installed Menu/FIFO/sudo boundary. It checks screen
output, F10/Enter and cleanup, not behavioral arrow/Tab navigation. Unit tests mock
terminal opening and Popen. Those retained passes remain valid for their narrower
scope, but did not exercise the failed path.

Required regression coverage:

- Traverse the real installed Menu → FIFO bridge → sudo policy → broker path under
  a controlling PTY with TERM=linux; verify MC foreground group and terminal fds.
- Verify physical/caller terminal canonical/echo state while MC is interactive;
  assert Up/Down selection, Tab panel change, function-key action and F10 return.
- Exercise Ctrl+C, HUP, bridge disconnect and worker crash; no orphan MC, leaked
  lease or false safe-removal claim. Check read-only/nosuid/nodev/noexec throughout.
- Repeat browsing, exercise busy-unmount failure, and regress ordinary FILES MC.
- Requalify the exact new candidate on physical Pi 4; synthetic passes cannot
  replace B1 and cleanup observations on hardware.

Affected packages must be rebuilt into a **new distinct PRIVATE NON-RELEASE image**.
Attempt18 stays failed evidence. No source fix, package, image or stable 1.1.0 tag
was changed by this investigation. Local documentation and private evidence only.
