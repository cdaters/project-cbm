# Build-host and target environment

POC4 attempt #1 failed before CBM integration. The invocation exported a builder-only
TMPDIR; pinned pi-gen `on_chroot` passed it through `capsh --chroot`. AppArmor 4.1.0-1's
postinst calls `mktemp` while generating its home-directory tunable. The retained log
and a disposable native reproduction establish this cause. No AppArmor policy change
or package-check bypass is necessary.

## Explicit boundaries

`tools/build_environment.py` defines a new environment rather than copying ambient
operator state. The factory clears inherited variables before probes and starts
pi-gen/the frozen transport with that environment. The declared epoch comes from the
lock. pi-gen loads its own exported stage/configuration variables from generated
`config`; these remain available to host stage scripts and CBM integration.

The retained `target-environment.patch` adds two boundaries to pinned pi-gen:

- debootstrap gets fixed root identity, system PATH, C.UTF-8, `/tmp`, noninteractive
  debconf and declared epoch, plus ONLY the explicitly configured frozen HTTP proxy;
- `on_chroot` gets the same fixed base without any proxy, CBM paths or host exports.
  Its target `/tmp` is mode 1777. Target APT uses the generated proxy configuration.

CBM's direct chroot calls use the same target environment. The pinned stage scripts
were inspected: target values are inserted by host-expanded here-documents; the
quoted APT here-document computes its architecture inside the target. None requires
ambient operator or CBM build paths. debootstrap may create its own internal variables;
those are upstream-controlled bootstrap state, not inherited operator configuration.

| Variable family | Policy |
| --- | --- |
| TMPDIR / TMP / TEMP | `/tmp` inside the Linux guest or target, respectively |
| HOME / USER / LOGNAME | `/root` / `root` / `root` for image-construction processes |
| PATH | Fixed standard Linux executable directories |
| LANG / LC_ALL / other locale overrides | C.UTF-8; other ambient overrides absent |
| XDG_* | Absent |
| proxies | Absent except declared bootstrap HTTP proxy; target APT config is explicit |
| Python | No PYTHONPATH/HOME/startup injection; bytecode generation disabled |
| Git | No ambient Git config/path overrides |
| CBM_* / pi-gen stage paths | Generated host config only; not target package environment |
| BASH_ENV / ENV / exported functions / LD_* / SUDO_* | Ambient values discarded |
| SOURCE_DATE_EPOCH | Validated declared epoch, never ambient |
| DEBIAN_FRONTEND | Target/bootstrap noninteractive; package errors remain fatal |

This is process reproducibility/isolation, not a security sandbox for untrusted code.
Invoke the factory with an explicit interpreter and a clean `env -i`; a Python script
cannot retroactively sanitize its interpreter's startup. Do not record raw environment
dumps. The guest's `/tmp` resides on TheBench-backed ext4; it is not macOS `/private/tmp`.
macOS/Lima acquisition still uses the guarded external temp/cache paths.

## Reproduce and retry

Ordinary regression: `python -m unittest discover -s tests -p test_build_environment.py`.
The opt-in [native regression](../../tests/native/build_environment.sh) requires a NEW
disposable copy of the failed root and patched `scripts/common`, runs in private mount/
PID/network namespaces, reproduces both mktemp and actual AppArmor configuration failure,
then verifies hostile-variable exclusion, `/tmp`, dpkg/AppArmor configuration and APT.
Never run it against the preserved failed tree.

`freeze_poc4_retry.py` preserves attempt #1 and freezes `inputs/frozen-poc4-attempt2`.
Component packages and their source mappings are reused byte-for-byte. Integration
source, chroot sealing recipe and declared pi-gen patch change, so complete inputs and
installed identity are **not identical**. `construct_poc.py --attempt 2` uses separate
`builds/private-poc4-attempt-2` and `artifacts/private-poc4-attempt-2`; existing workspace
creation fails rather than overwriting evidence. The host guard runs before construction
and after pi-gen, including failure. A new integrity failure stops the attempt.
