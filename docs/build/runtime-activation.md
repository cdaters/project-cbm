# First-boot/runtime activation engineering work

In progress, 2026-09-16. Owner authorization covers one new private engineering
candidate, following the accepted configuration and optional-content source work.
No public release, push, physical test, other Pi model or boot cosmetic optimization.
POC1–3 remain immutable; POC3 is the previous physically demonstrated Pi 3B baseline.

## Implementation boundaries

- Keep the POC3 getty/login/PAM session and VICE geometry/return behavior.
- Keep the existing root-expansion service as the only growth mechanism.
- Local setup records region, owner credentials and a network choice independently.
  Offline is a valid completed choice. Completion requires verified growth, a valid
  machine ID, a usable owner credential and valid sudoers. A crash between the final
  marker and readiness publication is repaired by a repeated finish request.
- The image will contain a locked `owner` account, UID 1001, in Debian's ordinary
  `sudo` group. The appliance account remains `pi`, UID 1000. There is no preset owner
  password. Local setup uses PAM through `chpasswd` stdin; finished setup is not a
  password-reset interface. Later password changes belong to authenticated owner
  administration. No password goes into argv, logs, metadata or test evidence.
- Normal operations use the fixed no-argument configuration helper. USB import has
  a separate constrained helper; neither accepts arbitrary commands/paths/units.
- TCPser's typed adapter binds IP232 to `127.0.0.1:<selected port>` and its inbound
  listener to `127.0.0.1:0`. Port zero means an ephemeral local listener, **not disabled
  listening**. This supports outgoing modem use; public incoming BBS hosting is not
  exposed by the normal settings API. No serial/IP tracing is enabled.
- `.sid` import remains supported, but generic VICE autostart is refused. A dedicated
  validated PSID/RSID player remains the next bounded media gate.

These are source implementation decisions, not claims of completed runtime activation.
Package integration, service tests, the complete candidate lock/image and physical
procedure remain pending until the completed build record says otherwise.

## Native staging evidence so far

The Linux builder runs Debian 13, aarch64, kernel `6.12.107+deb13-cloud-arm64`.
Automatic builder APT update units remain masked. No new host package was installed.

The guest path `artifacts/private-poc3` contains the **previously rejected** POC3
host-drift attempt, SHA-256
`3c2fcc470305632eda6600ef7fefbb507583364a78ad3d17895d9b7cb9c4a538`,
596,976,676 bytes. It exactly matches the external
`artifacts/poc3-unaccepted-host-drift` copy. The staging checksum preflight rejected
it before extraction. No candidate was constructed from it. Guest build-output paths
are not an artifact authority.

The authoritative external accepted POC3 XZ still verifies as
`e7d9657bfbb1124b38c2f1f3479698e24a34be7234db80d766f189da946ace3c`.
It was copied to guest `staging-inputs/poc3-accepted.img.xz`, decompressed and verified
against the recorded raw hash. A read-only `ro,noload` loop mount supplied a separate
copy at `/srv/project-cbm/staging/runtime-activation/root`; originals were untouched.

- Actual native account creation, locking, PAM password initialization through stdin,
  rejection of an incorrect password and authenticated sudo to UID 0 passed in that
  disposable chroot. Generated test passwords existed only in memory/the disposable
  credential store and were invalidated immediately; none was reported or retained.
- Actual native root expansion passed on an independent 4 GiB loop-image copy; the
  second invocation retained the start sector and safely reported no further growth.
- An earlier growth harness stopped at the machine-ID prerequisite. A plain chroot
  has no booted PID 1 to process `uninitialized`. The corrected **test-only** harness
  used systemd's offline initializer. This is not a change to image sealing and does
  not establish real boot ordering or physical interruption safety.

Upstream references checked 2026-09-16:
[machine-ID setup](https://manpages.debian.org/trixie/systemd/systemd-machine-id-setup.1.en.html),
[first-boot identity semantics](https://manpages.debian.org/trixie/systemd/machine-id.5.en.html),
[PAM password input](https://manpages.debian.org/trixie/passwd/chpasswd.8.en.html).

## Optional inputs

SID-Wizard's previously accepted exact 1.97 native core subset remains the authority;
no licensing re-review or additional music/instrument/manual/host content is intended.

StrikeTerm 2014 Final was acquired from the author's endorsed CSDb source:
`https://csdb.dk/getinternalfile.php/129890/st2014final.d64`.
The D64 is 174,848 bytes, SHA-256
`72b803c54c7892857c0ddb5674dabc841d59a496285975546bef689308940595`.
It matches the previously recorded Combian copy exactly. Its directory starts with
the `STRIKETERM 2014` PRG. This comparison establishes artifact identity, not rights
or physical compatibility. Retained acquisition: configured bulk storage
`inputs/runtime1-striketerm-review/`.

Owner classification: **PRIVATE-ENGINEERING-ADMITTED;
PUBLIC-RELEASE-RIGHTS-GATE-PENDING**. Comprehensive public redistribution permission
remains unresolved. No reference SID/demo payload is admitted or downloaded.

## Remaining gates

Complete native staging, matching versioned packages/interfaces, frozen inputs,
one controlled image, offline checks, footprint measurements, hash-bound owner Pi 3B
procedure and verified recovery bundles. No image or new hardware qualification has
been produced by this work yet. Do not interpret intermediate fixture passes as a
completed milestone or a physical pass.

## Native staging gate (completed before candidate freezing)

The two `1.1.0~poc4-0~staging1` packages installed into an independent accepted-POC3
root copy; `dpkg --audit` reported no unresolved package/dependency state. These
preliminary packages are not final candidate artifacts. Source corrections below
were tested in the disposable copy and must be included in the final packages.

Existing `unshare`/systemd utilities supplied private mount, PID, network, UTS, IPC
and cgroup namespaces; no container platform was installed. A temporary delegated
`pcbm-native-staging` unit limited memory to 2 GiB and devices to basic character
interfaces, with one explicitly admitted synthetic loop device for import testing.
The namespace had loopback only, no external route, private service bus and hidden
hardware sysfs. Its root/getty/hardware units were inhibited **only in staging**.
The namespace's expected EEPROM/remount failures do not constitute a Pi boot test.
The builder hostname/network, account databases and package inventory were unchanged.
See the opt-in [native harnesses](../../tests/native/README.md). Upstream
[systemd namespace requirements](https://systemd.io/CONTAINER_INTERFACE/) and
[util-linux unshare](https://man7.org/linux/man-pages/man1/unshare.1.html) were consulted
on 2026-09-16. This is test isolation, not a new runtime/build foundation.

**Passed in native Linux staging:**

- Matching package installation and installed `pcbm-info --json`.
- Exact no-argument helper sudoers parses; `pi` can invoke approved requests;
  arbitrary root `id`, helper arguments and unknown operations are rejected.
- Real locale generation, next-boot keyboard compilation and timezone application.
- Real local owner password initialization, incorrect-password rejection,
  authenticated sudo to UID 0 and refusal of password reset after setup completion.
- First-boot state transitions with an offline choice; completion prerequisites.
  Its growth marker was injected from the separately verified loop-growth contract,
  not misrepresented as expansion of the namespace root.
- Actual Advanced Terminal authentication failure/success and return, using a
  pseudo-terminal; no password echoed. Authenticated raspi-config noninteractive
  invocation. Full interactive raspi-config and physical keymaps remain Pi tests.
- Hostname update and user-readable local resolution without changing the builder.
- Samba's separate credential enrollment/readiness and service start/stop.
- SSH key absence before explicit generation, fresh generation, config syntax,
  deliberate service start/stop. No external SSH login was attempted.
- TCPser actual start/stop and loopback-only IP232 plus ephemeral inbound listener.
  The first readiness assertion raced process startup; bounded observation confirmed
  both loopback listeners. This is not BBS connectivity qualification.
- mDNS daemon/socket start/stop. No physical LAN name-resolution claim.
- NetworkManager offline selection; real private keyfile parsing and exact synthetic
  password round trip (including punctuation/backslash); missing-radio activation
  fails. Only redacted result flags were emitted; the test connection was deleted.
- Synthetic read-only ext4 mount/copy/unmount: two files copied as UID 1000, a symlink
  and root-only directory skipped, SID classified under music; retry copied nothing
  and preserved destinations; the source image SHA-256 remained unchanged.
  Test discovery was explicitly substituted; production cannot request loop devices.

**Corrections from review/staging:** Wi-Fi rescan now dispatches rescan rather than
forget; hostname changes keep `/etc/hosts` readable and locally consistent; ext4
import uses `noload` to prevent journal replay and skips inaccessible directories
without elevating the copying process. The terminal harness initially failed to
recognize ANSI-colored prompts; authentication itself was working.

Product tests: **138 pass**. Menu tests: **50 pass**, plus its shared-launcher checker.
AST, JSON, per-file changed-shell syntax and diff whitespace checks pass. Fixtures
cover interruption before every setup marker, prerequisites, no false completion,
no completed-setup password reset, secret exclusion and operation/path/unit rejection.
These tests do not simulate power interruption during filesystem resize/PAM writes.
Physical power-loss recovery, Pi hardware, Wi-Fi/Ethernet, external Samba/SSH/mDNS,
BBS connectivity and application/media execution remain physical qualification gates.

Staging credentials were generated in memory and invalidated. Do not preserve the
staging root, shadow backups, Samba databases or journals as build/recovery evidence.
Preserve source harnesses and sanitized results; the candidate is constructed afresh
from the frozen package closure, never by cleaning this staging root.
