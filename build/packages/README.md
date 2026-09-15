# Private POC packages

Standard debhelper/dpkg-buildpackage recipes. VICE source 3.10 and TCPser upstream
fe7feff4862406b277e009d14c219f5d16cf1222 are retained externally; Menu packaging
belongs in the companion feature/1.1-debian-package branch. These recipes do not
install into the release rootfs while compiling. Build only in the approved Linux
host, with exact source hashes, generic arm64 flags and retained dependency versions.

VICE explicitly disables native-CPU optimization (`--disable-arch`) and builds SDL2,
ALSA and SDL sound, including x64. TCPser uses generic arm64 Debian flags. No service
or sudo defaults are installed by these packages. Actual shared-library dependencies
come from dpkg-shlibdeps. Retain .dsc, orig/debian source, .buildinfo, .changes, .deb,
debug packages and build logs. POC builds use fresh source directories in the dedicated
Debian guest; stronger per-package sbuild isolation is future factory hardening.
The guest's complete dependency inventory must be frozen/retained before image assembly.

VICE's upstream ROM/data licensing is distinct from code licensing; retain upstream
source/notices, do not import historical private ROMs/media, and do not publish this
private engineering payload without distribution review. No public release is authorized.

## First successful candidates (2026-09-15)

VICE 3.10-1+pcbm1 (arm64), TCPser 1.1.6~beta-1+pcbm1 (arm64), Menu
1.1.0~poc1-1+pcbm1 (all) built successfully. See CURRENT-STATE.md for hashes.
VICE success used an out-of-tree build, disabled unnecessary autoreconf of the
release tarball, and declared configure-required dos2unix/xa65/SDL2-image/evdev.
No upstream code patch was needed. VICE build wall time 74.68 s, GNU time maximum
RSS 482,988 KiB; this is not total VM peak RAM or a Pi runtime benchmark. Installed
sizes: VICE 40,787 KiB, Menu 103 KiB, TCPser 78 KiB, excluding dependencies.
Build dependencies remain exclusively in the disposable builder. Initial failed
configure/source-packaging attempts and successful logs remain externally retained.
