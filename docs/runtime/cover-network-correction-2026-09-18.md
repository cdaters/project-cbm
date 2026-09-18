# Controlling-terminal Cover admission and authoritative network information

This source correction follows the [attempt #4 card review](../qualification/poc4-attempt4-card-review-2026-09-17.md).
The owner reported a physically passing Pi 3B keyboard/VT lifecycle and missing Covers.
The literal `/dev/tty1` pathname guard rejected the supervisor's `/dev/tty` descriptor.
That is a confirmed source defect and a high-confidence explanation of the four
retained failures; no guard-rejection event existed to prove the exact physical branch.
Attempt #3's precise failure cause remains unproven.

## Cover admission

Menu queries Linux `TIOCGDEV` on stdin and its own controlling `/dev/tty`; both
must identify console tty1 (major 4, minor 1). It also requires `VT_GETSTATE` to
report active VT1 and the controlling terminal foreground process group to match
its existing group. Direct tty1 and the controlling alias therefore have the same
admission semantics. Root, non-Linux, non-terminal, other/foreign tty, inactive VT,
background group and unavailable ioctl cases produce fixed skip events and fail open.
No terminal/VT mode, process group, getty, PAM, device permission or privilege changes.

The existing Product supervisor, timeout/termination/reaping, pre-Cover capture,
restoration/readback before and after VICE, POC3 geometry, ALSA and F10/Quit are
unchanged. The wrapper logs `admitted`, `asset_ready`, or a fixed `skip_*` reason;
existing renderer initialization/video/renderer/presented/released events continue.
Product already retains these events in the private engineering launch `cover.json`.
Missing assets or failed admission still allow VICE to proceed. Seven artwork files
and registry mappings are unchanged. Successful native fixture rendering does not
establish physical Cover visibility or KMS/VT behavior.

Kernel authority: [Linux tty ioctl implementation](https://raw.githubusercontent.com/torvalds/linux/v6.12/drivers/tty/tty_io.c),
[VT API](https://github.com/torvalds/linux/blob/master/include/uapi/linux/vt.h), and
[allocated device numbers](https://cdn.kernel.org/doc/html/latest/admin-guide/devices.html).
`TIOCGDEV` returns the encoded real tty device, avoiding pathname alias assumptions.

## Network authority and presentation

Product `pcbm-info` adds optional `current_state.network_interfaces` to contract 1,
retaining `network_links` for older consumers. Each non-loopback interface reports
name, type, NetworkManager state, kernel link state, IPv4/IPv6 CIDRs, effective MAC
and nullable active Wi-Fi SSID. IP assignment and link state do not prove Internet
reachability. IPv6 link-local addresses require an interface zone when used.
Tentative, duplicate-address-failed, multicast, unspecified and loopback addresses
are omitted. Unknown/unavailable values remain explicit; an unavailable NetworkManager
query does not discard valid IP/MAC data.

The fixed read-only collectors use `ip -j address show`, selected NetworkManager
device fields and a cached `device wifi list --rescan no` only for connected Wi-Fi.
They never inspect saved connections/passwords, request secrets, scan, enable a
service or change network configuration. Commands inherit the existing one-second
bound and 64 KiB output contract. Parsers bound interfaces/addresses, reject malformed
or duplicate records, decode terse escaping and suppress unsafe SSIDs. Connection
names are not SSIDs. See the [nmcli command reference](https://networkmanager.pages.freedesktop.org/NetworkManager/NetworkManager/nmcli.html).

Existing System Information and CONTROL → Network's information entry consume the
same JSON authority. No Menu network probes or new top-level item. Runtime explicitly
depends on `iproute2`, already in the retained target closure.

## Validation and candidate boundary

Host: Product 162/163, only the known context-dependent macOS mktemp expectation;
Menu 76/76. Native Linux source suites: Product 163/163 and Menu 76/76. Focused cases
cover tty alias identity, inactive/background/foreign tty rejection, fixed skip events,
malformed/partial network data, CIDRs/MAC, escaped SSIDs and legacy UI compatibility.
Actual installed Linux command syntax and a synthetic namespace interface IP/MAC
collection pass; actual Wi-Fi association remains untested.

A disposable native test root uses an OverlayFS upper on guest ext4 over a verified
read-only (`ro,noload`, read-only loop) attempt #4 image. This avoids duplicating its
root filesystem without deleting prior state. It changes only staging isolation;
the approved factory still constructs a fresh ext4 image from a new frozen lock.
Staging credentials and journals are excluded from evidence export.

The next candidate is POC4 corrective attempt #5, retaining Product `1.1.0-poc.4`:
this continues POC4 runtime qualification, not a new milestone or public release.
Changed packages: Runtime `1.1.0~poc4.2-1`, Menu `1.1.0~poc4.3-1+pcbm1`
(tag `v1.1.0_poc4.3`). Unchanged components and rights gates remain exact frozen inputs.
Image/offline results will be recorded separately after construction. Quiet and fast
boot remain [backlog](../design/boot-experience-backlog-2026-09-17.md).
