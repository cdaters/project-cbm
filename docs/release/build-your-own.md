# Build Your Own Project CBM

[Documentation index](../README.md) · [Factory explanation](factory.md) · [Customization](customization.md)

Project CBM is assembled from Raspberry Pi OS Lite plus a small set of packages and
configuration. VICE emulates the computers. Project CBM Runtime connects system
information, preferences and privileged operations. Project CBM Menu presents the
keyboard interface. A build system called **pi-gen** puts those pieces into an SD-card image.

```text
Raspberry Pi OS Lite (64-bit, Debian 13 Trixie)
                    |
                  pi-gen
                    |
          Project CBM custom stage
                    +-- Runtime and Menu
                    +-- VICE and TCPser
                    +-- first-boot setup
                    +-- networking and optional services
                    +-- content library and appliance configuration
                    |
              bootable .img
                    |
             compressed .img.xz
```

## Choose your build route

**A published release:** use that release's Product/Menu sources and documented public
dependencies. This is the intended route for someone who wants to reproduce the product.
The [1.1.0 release](https://github.com/cdaters/project-cbm/releases/tag/v1.1.0) now
publishes Product/Menu refs, corresponding-source archives and inventories.
**Current limitation:** the complete initial-input acquisition/bootstrap route is
still unfinished. Public source availability alone does not provide an end-to-end
first image build or establish independent reproducibility. The
[dated public-build audit](../documentation/public-bootstrap.md) retains the original
findings; its publication-pending statements are historical.

**A customized image:** change your own source and build new packages/image. The
[worked customization examples](customization.md) explain what to change and test.
You can prepare the source changes now; assembling a complete image still needs the
build inputs and workflow described below.

**The project's official factory:** maintainers currently build from a complete preserved
input kit. It records exactly which source, packages and configuration are used, so later
builds do not silently download newer versions. That record is the **release lock**.
The [official walkthrough](../build/official-factory-walkthrough.md) documents the working
commands separately. You do not need that entire process to understand the appliance.

## What you need

Package and image assembly use **native arm64 Debian 13 Linux**. The image filesystem
needs Linux ownership, links, devices and mount behavior; an ordinary macOS folder is
not a substitute. Native arm64 Linux is the relevant environment, but a new host must
be tested against the project's capability checks. An x86 PC using emulation is not a
qualified Project CBM build route.

The qualified macOS route uses an Apple Silicon Mac and a Linux virtual machine managed
by Lima with Apple's Virtualization framework (VZ). Its current configuration allocates
8 CPUs, 10 GiB memory and a 256 GiB sparse disk on external storage. These are tested
factory allocations, not established minimum RAM/CPU requirements. The factory requires
more than 40 GiB free on its Linux ext4 workspace before construction; provisioning
checks require 256 GiB of free external storage. Keep extra room for sources and outputs.
See [Mac host setup](../build/lima-build-host.md) for the exact supported host workflow.

There is no reliable clean-from-download build-time estimate yet. A recent already
prepared/frozen image construction took about 193 seconds on the configured builder;
that excludes initial downloads, VICE/package builds, validation and compression checks.
Do not budget three minutes for a first build. Record your own host and stage timings.

## Get the sources

Run these on your source computer in a directory where you keep projects:

```sh
git clone https://github.com/cdaters/project-cbm.git
git clone https://github.com/cdaters/project-cbm-menu.git
export PROJECT_CBM_SRC="$PWD/project-cbm"
export PROJECT_CBM_MENU_SRC="$PWD/project-cbm-menu"
```

Product owns `runtime/`, `build/`, `tools/` and the product documentation. Menu owns
`scripts/`, `lib/`, `covers/` and its own `debian/` package recipe. Keep them as siblings
for cross-repository tests. Choose the exact refs listed with the intended release,
not an arbitrary newer branch. There is no public 1.1 final tag to substitute today.
When published, set these variables to its actual source refs:

```sh
git -C "$PROJECT_CBM_SRC" checkout "$PROJECT_CBM_REF"
git -C "$PROJECT_CBM_MENU_SRC" checkout "$PROJECT_CBM_MENU_REF"
```

**Stop here if those refs or the 1.1 recipes are unavailable.** Public main currently
must not be represented as containing the unpublished 1.1 implementation. The remaining
commands are the source-checked component procedure for readers who have the matching
source; they are not a claim that public bootstrap is already complete.

## Native Linux package walkthrough

Run in an arm64 Debian 13 development environment, not on the appliance SD card.
Set `PROJECT_CBM_SRC` and `PROJECT_CBM_MENU_SRC` to their Linux checkout paths.
Choose a new directory on mounted ext4 for generated files:

```sh
export PROJECT_CBM_WORK="/srv/project-cbm"
mkdir -p "$PROJECT_CBM_WORK/docs-example-packages"
cd "$PROJECT_CBM_WORK/docs-example-packages"
uname -m
findmnt -T "$PROJECT_CBM_WORK" -no FSTYPE
df -h "$PROJECT_CBM_WORK"
```

Expect `aarch64` and `ext4`. `/srv/project-cbm` must already be provisioned/writable
for your build user. Do not silently put a large build on another filesystem.
On a fresh disposable development host, install package-building tools and the exact
Build-Depends declared in each recipe. For the current recipes:

```sh
sudo apt-get update
sudo apt-get install build-essential debhelper python3 git ca-certificates curl \
  libsdl2-dev libdrm-dev libsdl2-image-dev libevdev-dev libasound2-dev \
  libpng-dev zlib1g-dev libcurl4-openssl-dev libreadline-dev libedit-dev \
  flex bison texinfo pkg-config dos2unix xa65
```

This installs today's repository versions for component development; it does not reproduce
an older release's exact toolchain. The official factory records versions and separates
this download phase from image construction. Additional image-host tools are declared in
`build/host/build-packages.list`; that list is not a substitute for package Build-Depends.

### Runtime and Menu

Export clean committed source into fresh directories. Run the following in the new
package workspace. These commands create binary packages only; they do not install them
on your computer or build an image.

```sh
mkdir runtime menu
git -C "$PROJECT_CBM_SRC" archive HEAD | tar -x -C runtime
cp -a "$PROJECT_CBM_SRC/build/packages/runtime/debian" runtime/debian
git -C "$PROJECT_CBM_MENU_SRC" archive HEAD | tar -x -C menu
(cd runtime && dpkg-checkbuilddeps && dpkg-buildpackage -b -us -uc)
(cd menu && dpkg-checkbuilddeps && dpkg-buildpackage -b -us -uc)
```

`dpkg-checkbuilddeps` reports missing dependencies. `dpkg-buildpackage` follows each
Debian recipe; resulting `.deb`, `.changes` and `.buildinfo` files appear in the parent
workspace. Runtime and Menu packages are architecture-independent. VICE and TCPser below
contain arm64 machine code. To distribute a build, also create/preserve the corresponding
source packages and licenses; binary-only development output is not the release process.

### VICE

Download VICE 3.10 using the pinned URL in `build/inputs-poc.json`; that file's historical
name does not mean its older Menu selection is the current one. Check the VICE source
hash before extracting. In the same workspace:

```sh
curl --fail --location --output vice-3.10.tar.gz   https://downloads.sourceforge.net/project/vice-emu/releases/vice-3.10.tar.gz
printf '%s  %s\n' 8e5bac18cbcb9f192380ad3ef881f8790f5b75c41d7b3da65d831985d864d6d1 vice-3.10.tar.gz | sha256sum -c -
tar -xf vice-3.10.tar.gz
cp -a "$PROJECT_CBM_SRC/build/packages/vice/debian" vice-3.10/debian
(cd vice-3.10 && dpkg-checkbuilddeps && dpkg-buildpackage -b -us -uc)
```

The Debian source workflow applies the two listed patches; do not apply them a second
time manually. [VICE integration](vice.md) explains the flags, SDL/ALSA dependencies,
profile mapping and performance choices. A source download failure or hash mismatch
must be resolved before building; don't update the expected hash merely to make it pass.

### TCPser

The modem component uses a specific upstream commit. This clone/checkout creates the
source directory; the Product recipe packages it without starting a modem service:

```sh
git clone https://github.com/go4retro/tcpser.git tcpser
(cd tcpser && git checkout fe7feff4862406b277e009d14c219f5d16cf1222)
cp -a "$PROJECT_CBM_SRC/build/packages/tcpser/debian" tcpser/debian
(cd tcpser && dpkg-checkbuilddeps && dpkg-buildpackage -b -us -uc)
sha256sum ./*.deb
```

Keep sources, package versions and checksums together. Changing source requires your
own new package version; don't distribute changed bytes under an existing release name.

## From packages to an SD image

Packages alone do not create the Raspberry Pi OS filesystem, accounts, first boot,
service policy or boot partitions. pi-gen and `build/pigen/stage-cbm` add those pieces.
The [factory guide](factory.md#the-project-cbm-recipe) shows the actual tree and how the
constructor calls pi-gen.

**The public walkthrough currently stops here.** The existing constructor requires a
release lock plus actual package/source/metadata objects; the current lock creator starts
from a previous private kit. It also restricts image identities to the implemented private
families. There is no supported public command that accepts just the four new `.deb`
files and builds the whole appliance. The missing step must supply the package inputs and Project CBM configuration before
pi-gen can assemble the appliance.

For maintainers with a complete verified kit, the ordered [official factory walkthrough](../build/official-factory-walkthrough.md)
continues through export, package validation, lock creation, stage integration, construction,
image checks and recovery. It is the demonstrated end-to-end image route, not an input a
new user is assumed to own. A public first-lock/acquisition wrapper and distributable
input set are explicit release work; they are not implemented in this documentation pass.

## macOS route

The final Pi filesystem must be assembled in Linux. On Apple Silicon, Project CBM uses
Lima/VZ to provide that Linux environment. Source may stay on the Mac; archives are copied
into the guest's ext4 storage. No shared Mac directory is used as a target root filesystem.

Use [the host setup recipe](../build/lima-build-host.md) in order: register/verify external
storage, obtain and verify the pinned Lima/guest bootstrap, render the configuration,
start the VM, then run its capability checks. The existing management commands are:

```sh
cd "$PROJECT_CBM_SRC"
python3 tools/build_host.py --workspace-config "$PROJECT_CBM_WORKSPACE_CONFIG" preflight
python3 tools/build_host.py --workspace-config "$PROJECT_CBM_WORKSPACE_CONFIG" lima start cbm
ssh -F "$PROJECT_CBM_SSH_CONFIG" lima-cbm
```

`PROJECT_CBM_WORKSPACE_CONFIG` is the JSON workspace registration created by that recipe;
`PROJECT_CBM_SSH_CONFIG` is the generated Lima SSH config in your registered bulk storage.
They are files you create/provision, not paths supplied by the developer's computer.
Inside the guest, use the Linux paths and package steps above. The same public-image
bootstrap gap applies; virtualization does not supply missing release inputs.

## What the complete factory does

1. Selects/downloads source and packages during a separate preparation phase.
2. Builds changed Project CBM packages, or verifies unchanged packages for reuse.
3. Records source versions, recipes, package bytes and build-host inputs in the release lock.
4. Runs pinned pi-gen stage0/1/2 to create Raspberry Pi OS Lite.
5. Runs stage-cbm to install the Project CBM packages, content layout and configuration.
6. Sets up the pcbm account, first boot, Menu session and optional service policies.
7. Writes the installed version/build record and removes build-only state.
8. Exports boot/root partitions to a raw `.img` and compresses it to `.img.xz`.
9. Verifies the image's contents and that decompressing XZ produces the same raw bytes.
10. Retains source/output records, then tests the image on physical hardware.

<a id="did-my-build-work"></a>

## Verify your build

For a personal build, first check the build exited successfully and locate the expected
files reported in its log. Do not flash a partial output after an error. Hash the files;
with Bash pipefail, verify compressed/raw agreement:

```sh
set -o pipefail
sha256sum "$PROJECT_CBM_IMAGE" "$PROJECT_CBM_XZ"
xz -dc "$PROJECT_CBM_XZ" | sha256sum
```

Set those variables to the actual output paths. The decompressed hash must match the raw
image hash. On a spare card, [flash and start](getting-started.md), finish setup, check
About/System Information, RUN C64, F10 → Quit, and POWER. On the Pi, these read-only commands
check the installed combination if you use a terminal:

```sh
cat /usr/share/project-cbm/identity.json
dpkg-query -W project-cbm-runtime project-cbm-menu project-cbm-vice project-cbm-tcpser
```

Project releases additionally check all installed packages, ELF/library dependencies,
filesystems, services/security, physical regressions and recoverability. Independent
build comparison is needed before claiming byte-for-byte reproducibility; a successful
build alone does not establish it. [Testing](../testing.md) describes those deeper checks.

## Builder troubleshooting

| Failure | First check / useful log |
| --- | --- |
| Missing recipe/ref | Confirm the intended source was actually published; public main is not a substitute for unpublished 1.1 |
| Missing dependency | Run `dpkg-checkbuilddeps` in the package source; inspect `debian/control` |
| Unsupported host | Check aarch64, Debian version, ext4 and capability results; don't bypass an architecture/mount gate |
| Lima will not start | Check the registered workspace, pinned guest image and VM log using the host recipe; don't delete the only copy of builder state |
| Insufficient space | Check both external host space and guest ext4 free space; sparse disk capacity is not free space |
| Package failure | Read that package's build output/log, beginning at the first error, not just its final exit code |
| Download/repository failure | Check URL/version/signature/checksum and network access during acquisition; frozen construction intentionally has no external downloads |
| chroot/loop/mount failure | Check Linux privileges, namespace/capability test, mount support and target environment; preserve partial work before cleanup |
| pi-gen/export failure | Read `build.log` in the generated pi-gen tree and captured constructor output; inspect the first failed stage |
| Checksum mismatch | Preserve both files and recheck transfer/decompression. Never relabel an unexpected file with the old checksum |
| Image boots without expected package | Compare installed identity/package list with your build output; confirm stage-cbm ran and you flashed the correct file |
| Image will not boot | Verify write/checksum, supported hardware and boot partition; preserve errors before a new build |

For the current official constructor, work/logs are under `builds/<candidate-directory>`,
raw output beneath its `work/export-image`, and compressed output under
`artifacts/<candidate-directory>`. The exact directory follows the supplied identity and
attempt argument; [factory details](factory.md#outputs-and-verification) explain this mapping.
