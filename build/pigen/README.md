# Private POC image integration

This is the first engineering implementation, not a release or Pi qualification.
Source selection: ../inputs-poc.json. Full input lock is generated externally only
after all packages, authenticated APT bytes and source/host closures are retained.

## Input resolution versus construction

`resolve-inputs.sh` runs pinned upstream stage0/1/2 with `SKIP_IMAGES` on every
stage. This disposable rootfs resolves package versions, dependencies and source
requirements; it is never exported as a candidate. The local retention transport
fetches only approved Debian/Raspberry Pi HTTPS origins. APT/debootstrap perform
normal repository authentication. Exact bytes and URLs are catalogued. Successful
component packages and their runtime dependencies are resolved before the catalog
is frozen. Missing package versions stop closure acceptance; Debian snapshots may
supply the exact versions with explicitly recorded acquisition/trust evidence.

Final construction must start with fresh stage directories and a frozen input lock.
The transport switches to frozen mode and refuses absent URLs instead of fetching
new inputs. All descriptor bytes, nested closure entries and actual Debian package
control identities are verified before construction. No fixture may drive assembly.
The integration stage verifies the same lock and installs its generated identity.
Image hashes, validation results and publication metadata remain external outputs.

## Bounded POC runtime policy

The private candidate boots to Bash/dialog Menu as local pi, with locked pi/root
passwords and no reusable builder credentials. The unit provides a local user shell
after Menu exit. Shared Menu launch/return behavior is preserved, with necessary
/usr/bin relocation. The stage installs VICE and TCPser binaries, standard runtime
libraries and Samba, but SSH/Samba/TCPser/Avahi/NetworkManager are disabled/masked.
No default network listener or baked credential is inferred from historical v1.0.
Network configuration and privileged controls remain intentionally incomplete for
this first POC; enabling them needs subsequent product/security work. No broad sudo
policy is copied. Cover art is absent pending rights review; its helper safely skips.

## Single first-boot owner

The inspected `raspberrypi-sys-mods 1:20260914` contains initramfs `resize_early` and
`set_partuuid` hooks gated by the kernel `resize` argument. `rpi-resize.service`
requests systemd-growfs-root; userconfig and SSH-key regeneration are separate
vendor services. The CBM stage removes `resize`, masks the competing growth/user/
SSH services, and removes cloud-init. It never stacks PiShrink/cloud-init/vendor
partition growth with its own coordinator.

`pcbm-first-boot.service` is the sole POC coordinator. Systemd supplies a fresh
machine-id from the sealed `uninitialized` marker. The coordinator locks its state,
checks actual mounted ext4 root/parent and the declared two-partition DOS layout,
retains pre-growth geometry, calls Debian growpart/resize2fs, and checks kernel and
disk geometry agree before proceeding. It refuses overlap, movement, shrink,
non-final root, unsupported mapper/GPT/sector layouts, stale kernel geometry or
ambiguous devices. SD/USB/NVMe names are discovered rather than hard-coded.

[Debian growpart](https://manpages.debian.org/trixie/cloud-guest-utils/growpart.1.en.html)
defines status 1 as no available growth; errors stop initialization. Its 10 MiB
fudge is a partition-growth threshold, not an SD-card requirement. Journal/state
writes are atomically replaced and fsynced; postconditions are checked again after
interruption. A stale kernel partition view requires reboot/inspection before retry.
User directories are seeded without replacing user files. Network listeners remain
off; no SSH host keys are needed by this POC. Completion gates the console service.
The base-release identity is read-only input, never first-boot progress state.

Pure geometry rejection tests run on the host. Interrupted first boot, power loss,
real-device growth, persistence and actual service ordering remain unqualified until
physical tests. Do not claim research/static tests prove safe power interruption.

## Sealing and footprint

The stage explicitly purges compiler/development payload found in upstream Lite,
checks important runtime component versions remain installed, removes temporary .debs,
source/build caches, reusable machine/SSH/cloud state and builder history. The final
upstream exporter also clears logs/its APT proxy; offline validation must verify that
composition. Retain exact package inventory and owned-path manifest externally;
measure raw/XZ bytes, partition/filesystem size/free space and installed package sizes.
No fixed 8 GB minimum or measured maintenance margin is asserted.

Known nondeterminism to inspect in a later clean rebuild: filesystem/disk identifiers,
file/archive timestamps, package maintainer script state, initramfs generation,
random seeds, compression/tool versions and build execution timing. SOURCE_DATE_EPOCH
and pinned inputs reduce variability; one image is not proof of reproducibility.

## Source retention findings

The initial discovery root included upstream rpi-connect-lite 2.12.2, a cloud remote
access client not required by CBM. No matching source entry was available in the
resolved APT Sources. The candidate excludes it with the retained one-line
exclude-connect.patch before stage execution; its unused .deb is omitted from the
frozen URL map, and its unsuccessful source lookup is retained as an explicitly
out-of-scope discovery result. This is not a claim that missing sources were recovered.
The stage/offline audit must confirm it is absent. Future input-resolution runs apply
the same patch up front. Other stage inputs keep their source retention requirements.

libftdi1 source 1.5-10 collided with an older binary name in APT lookup; --only-source
selects its authenticated Sources entry correctly. Original failed results remain;
an additive source-name reconciliation records the successful exact acquisition.
Old bootstrap binaries/sources were recovered through Debian's official snapshot API,
verified against snapshot file identities and assigned retained SHA-256 hashes. This
is HTTPS/API acquisition evidence, not an independently verified historical Release
signature claim; current APT repository authentication remains enabled and unchanged.

## Frozen export adaptation

`frozen-export.patch` adapts three upstream export scripts: CBM account initialization
replaces upstream user rename; export clears APT state without another update/upgrade;
final sealing removes the temporary policy-rc.d. Stage installation still uses normally
authenticated retained APT metadata. Construction runs in a network namespace with
loopback only, so missing frozen requests fail rather than change inputs. This patch
is an explicit hashed lock input, not an unrecorded edit to upstream history.
