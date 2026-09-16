# Private Project CBM 1.1 POC2 — completed build checkpoint

Completed 2026-09-15 America/Phoenix (image date 2026-09-16 UTC).
**STOP for owner review. POC2 is built and offline/static validation passed.**
No physical test, POC3, SSH enablement, public release or push was performed.
The Linux VM is stopped. This is a controlled build, not reproducibility proven.

## What changed and why

[POC1's immutable Pi 3B record](../qualification/poc1-pi3b-2026-09-15.json) retains
boot/Menu/input PASS, x64sc display/console recovery FAIL and later tests UNTESTED.
[Evidence-ranked analysis](../qualification/poc1-pi3b-analysis.md) remains unconfirmed.
POC2 addresses graphics closure and session ownership; it does not claim a Pi fix.

- VICE **3.10-1+pcbm2** explicitly requires GL/GLX/EGL/GLES/GBM/Mesa runtime libraries.
  Five additional runtime packages, zero existing base upgrades: libgl1/libglx0
  1.7.0-1+b2, libglx-mesa0 26.2.2-1~bpo13+0~rpt1, libxcb-glx0 1.17.0-2+b1,
  libxxf86vm1 1:1.1.4-1+b4. No desktop or development stack in the appliance.
- Standard getty/login/PAM owns tty1; a tty1-only profile starts the unprivileged
  Menu loop. pi now has /bin/bash, with password still locked. A separate tty2
  local non-root autologin exists only for this private engineering candidate.
- Both RUN and CONTENT use the shared unprivileged launcher. F10 opens VICE's menu;
  choose Quit to exit. Observer restores saved terminal keyboard/text/termios state
  and Menu resumes; actual Pi return behavior awaits testing.
- Four bounded launch directories retain 128 KiB stdout/stderr tails, identity,
  allowlisted environment, audio/spawn timing, PIDs, exit/signal and three snapshots.
  `pcbm-diagnostics` assembles the latest launch/current state. No root shell,
  network, arbitrary environment dump, process argv, passwords or private keys.
  Root-only kernel journal data may be unavailable; that denial is not bypassed.
- Exact no-argument poweroff/reboot are the only new sudo grants. SSH/Samba/TCPser/
  Avahi/NetworkManager remain masked. Unsupported setup screens now explain the
  engineering restriction. Full offline-first settings and narrow configuration
  helpers remain required later 1.1 work, described in the [setup review](../qualification/setup-ux-review.md).
- New original MIT qualification media is an explicit schema-2 input, installed
  through normal Programs/Music/Demos paths before freezing. Public inclusion is
  deferred. POC1 schema 1 remains readable and untouched.

The [design/build guide](poc2-design.md) explains implementation choices and the
newly reproduced VICE stdout/color logging crash. `+logcolorize -logfile -` avoids
that crash without a VICE patch; it does not establish POC1's physical cause.
No renderer/device index or historical display geometry is forced in the appliance.

## Exact inputs

| Input | Identity |
| --- | --- |
| Candidate | 1.1.0-poc.2 / private-engineering-poc2 |
| Frozen lock SHA-256 | `bc1c6e16c32d6285973933b8d50371899bc18e5407dd654c9a14d1187eb194ac` |
| Integration commit | `2b894ad187f0b603d2e0c9965aba242073e2cb90` |
| pi-gen arm64 | `6fcca44892d5d4b36f826d2b8fb16d716369fada` |
| Base | Same Trixie 13.7 / kernel 6.18.50 / Mesa 26.2.2 as POC1 |
| Menu tag | v1.1.0_poc2, object 4ff0f9c5d94f16064e2c43c960a429ecb275372b |
| Menu peeled source | 897cee7c792b11bfed80168a576f263340f5f57d |
| Menu source tar SHA-256 | c60eb7b43e266931668535cd656e9ec356b237e90d8f4a7644aaf23d260f4a3f |
| VICE source tar SHA-256 | 8e5bac18cbcb9f192380ad3ef881f8790f5b75c41d7b3da65d831985d864d6d1 |
| TCPser source | fe7feff4862406b277e009d14c219f5d16cf1222; accepted POC1 package reused |

| Package | Version | SHA-256 |
| --- | --- | --- |
| menu | 1.1.0~poc2-1+pcbm1 | `e29bc3598f3be0869f79184250f88a03f4c59f1304a20a428223bac58c97bd11` |
| tcpser | 1.1.6~beta-1+pcbm1 | `8b8f8a4f3ec98dddf5bdb347320dad05e1bbe5230e0ee2727248c247a5af584f` |
| vice | 3.10-1+pcbm2 | `ea941c6d7e2e7c61366bd8b6b45bbf9a1dc538c013e336f6c96ae94265535ab0` |

The generic build script also rebuilt TCPser and produced the same .deb hash; the
lock deliberately reuses its accepted POC1 component record. This one matching
package is not evidence of image reproducibility. Corresponding source, .buildinfo,
.changes, build logs, acquisition metadata and exact host supplement are retained.

## Qualification-media provenance and results

Author: Project CBM contributors. License: explicit MIT grant in
[qualification/media/LICENSE](../../qualification/media/LICENSE). Authoritative
source is this repository's [media directory](../../qualification/media/README.md),
commit `14e4ade77ec83e0429d194a6b5ecfa5ef7655e75`. Python standard-library build; deterministic
archive SHA-256 `61673c45058ba31d2e28c699c631e99173c4e44b8b49c82c83735c2c5614d0af`.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| pcbm-sid-check.prg | 527 | `f3433a637606898f9d5d6e1988027e08a28537476b8275ed698f902a6e64d12d` |
| pcbm-smoke.prg | 192 | `e5607be032ddf5ecbe9e14eceaace640d9eff86845204227d69012ebdb499989` |
| pcbm-video-input.prg | 607 | `ab4c892a62265435d875f7868dedcffecdba6760ea882691743aa4ae330dc75c` |
| pcbm-check.d64 | 174848 | `84bfb28bf97fd7073131e7b672ee6bb012f0da82bdf1ef4da87f6bc01440cc5f` |

Total content payload: 176174 bytes. The frozen
manifest records source files, destinations, expected behavior and the initially
pending reference qualification; these later results are external attestations,
not a reason to rewrite that frozen input.

Independent builder reference: newly built VICE, SDL dummy video/software renderer,
source-tree system resources, no Pi KMS/ALSA/session. Smoke and D64 showed the expected
PASS screen; SID reached DONE; graphics showed colors/star and neutral joystick.
Non-warp WAV output contains 428,288 mono 16-bit samples at 48 kHz, range -3472 to
3097. These establish loading/execution and generated samples, not heard audio or
interactive keyboard/joystick correctness. No blanket known-good hardware claim.
Initial dummy/warp recording limitations and the logging crash/backtrace are retained.

## Image outputs and footprint

Relative to configured bulk root (currently /Volumes/TheBench/ProjectCBM-Work):

| Output | Bytes | SHA-256 |
| --- | ---: | --- |
| `artifacts/private-poc2/2026-09-16-project-cbm-1.1.0-poc.2-lite-private-poc.img` | 3095396352 | `ef221dc09ea65d3976f88e65cde8f153a9c32989be09c6b35d545b111ccb7467` |
| `artifacts/private-poc2/image_2026-09-16-project-cbm-1.1.0-poc.2-lite-private-poc.img.xz` | 596406680 | `757aca812835c676d75eaad651b6739fc79461c25c8aa7426524f6692a6b3d9f` |

XZ decompression agrees exactly with the raw image digest. DOS layout: 512 MiB FAT
boot partition and 2,550,136,832-byte root partition. Before first-boot expansion:
root filesystem capacity 2439266304 bytes, used
1652502528, free 786763776,
available to non-root 642482176.
Runtime package Installed-Size totals 1597286400
bytes; component package sizes and individual partition measurements are in the
[machine-readable result](private-poc2.json). First-boot user capacity and safe
maintenance margin remain unmeasured. No nominal minimum SD size is claimed.

## Validation and limits

- 34 host tests pass on macOS and native Linux. Shared Bash launcher tests cover
  RUN/content arguments, paths with spaces, nonzero status and invalid profiles.
- All **79 offline image checks PASS**: packages/payloads, graphics libraries,
  getty/PAM setup, unprivileged account/launcher, bounded diagnostics, power-only
  sudo, disabled SSH/services, media hashes, fresh identity, absent builder residue.
- Read-only ext4/FAT checks, systemd unit verification and **112 ELF objects** pass;
  no missing dependency in the inspected executable/SDL/GL/EGL/vc4 closure.
- All 2,738 frozen objects rehashed after export. All 2,731 POC1 baseline files,
  including its qualification record, remain unchanged. Historical 1,677-entry
  preservation manifest and every pre-existing tag remain unchanged.
- Build wall time 2:36.63, CPU 225%, maximum measured process RSS 506,244 KiB. This
  is not total VM peak memory. Kernel/renderer/session/ALSA/controller behavior,
  interrupted first boot, cloned identity and physical return remain UNTESTED.
- GDB installation added/updated 12 host binaries for reference debugging; exact
  binaries/sources/metadata are in the lock's host supplement. It happened after
  component compilation. No debugging tooling was installed into the image.
- Nonfatal frozen apt-listchanges changelog warnings are retained. No missing
  binary/source input was replaced with an arbitrary newer package.
- No independent clean image rebuild. UUIDs/partition IDs, filesystem metadata,
  build timestamps and compression/environment effects remain nondeterminism to
  measure; minimal identity binds the frozen input lock, not a reproducibility claim.

## Retention, recovery and next step

- `inputs/frozen-poc2`: authoritative lock and content-addressed retained inputs.
- `inputs/qualification-media-0.1.0`: media output/provenance/license/source revision.
- `packages/poc2`: package/source/build records; source trees/caches remain disposable.
- `artifacts/private-poc2`: raw/XZ, package inventory and offline/closure validation.
- `qualification/poc2`: preservation baseline/verification, reference screenshots/
  logs/WAV, construction/acquisition logs and result summary.
- `archive/milestone1-private-poc2-2026-09-15`: additive final Git checkpoint/bundles
  and offline restore evidence. Existing sealed checkpoints are not replaced.

The VM is stopped, not destroyed. All bulk data remains on TheBench; an additional
folder on that device is not an independent encrypted backup. Independent custody,
public service/setup policy, full privilege UX, physical budgets and subsequent
reproducibility work remain open.

**Exact next step:** owner reviews this checkpoint and follows the
[hash-bound Pi 3B smoke test](../qualification/poc2-pi3b-smoke-test.md).
No automatic physical testing, POC3, SSH enablement or publication.
