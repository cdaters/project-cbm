# Project CBM 1.2.0

Find more Commodore software, bring your own files onto the Pi, and capture the
moments you want to share. Project CBM 1.2 adds Assembly64 Online Library, a more
selective USB importer, safe USB browsing and screenshots from SSH.

These notes describe 1.2.0. Check [release availability](../../README.md#current-release)
for the verified image and checksums before flashing.

## Highlights

- Assembly64 Online Library: search, filter, inspect and save software.
- Guided USB Import: scan a folder and choose what to copy.
- Read-only USB browsing with Midnight Commander and Safe Unmount.
- `pcbm-screenshot` for Menu, MC, Covers and supported VICE/gameplay screens.
- Direct startup into your RUN machine, with reliable return to Menu.
- Clearer file sizes, friendly names and improved Back/Parent navigation.

## Assembly64 Online Library

Open **CONTENT → Online Library** to search Assembly64. Use the supported filters,
read a result's details and choose downloadable files before saving them to your
local library. **Already Present** avoids copying identical files; **Keep Both**
preserves different versions. Saved content works offline through Browse Library.
**Server Information** stays readable until you leave it; **About & Support**
provides the official website and optional donation links.

**Powered by Assembly64** — [assembly64.hackerswithstyle.se](https://assembly64.hackerswithstyle.se).
Assembly64 is an independent project/team; Project CBM provides an API integration,
not ownership or wider affiliation. Optional support: [PayPal](https://www.paypal.com/donate/?hosted_button_id=8D6YK9LXULYPE)
or [Ko-fi](https://ko-fi.com/assembly64). No hosted collection is bundled. Search
and downloads need Internet access; automatic FTP/server fallback is not provided.

## USB improvements

**CONTENT → Import from USB** lets you choose a partition/folder, scan, select
supported files, choose category and machine, review, then import. Scanning never
copies files. Unsupported files are explained, and Parent/Back make it easier to
change the source. Read the completion and USB-release result before unplugging.

**FILES → USB Drive** is for manual browsing/copying. Mount Read-Only, use Midnight
Commander, press F10, then Safe Unmount. MC uses its own overwrite prompts; guided
Import offers reviewed selection and duplicate handling. Both protect the USB source.

Raw BIN/ROM resources are not general importable content. Copying a ROM file through
FILES does not configure it in VICE. Dedicated ROM management remains future work.

## Screenshots

From SSH, run `pcbm-screenshot`. It prints the PNG path under
`/home/pcbm/content/screenshots/`, named with a UTC timestamp. Retrieve it through
file sharing or SFTP. An optional basename ending in `.png` is accepted; existing
files are never overwritten. Capture is local and on demand, with no upload or video.
Normal Covers are brief: capture during their existing interval without extending it.

## Startup improvements

Choose **CONTROL → Machine and Startup → Boot preference**: Menu or Default emulator.
Direct startup finishes the boot artwork, shows the selected machine Cover and
opens visible VICE. F10 → Quit returns to a responsive Menu without an auto-launch
loop. Normal Menu/RUN behavior remains available.

## Other improvements

Improved USB keyboard handling, clearer scan/result messages, readable sizes,
retained filter choices and persistent Server Information. Existing CCGMS 2021,
SID-Wizard and VICE profiles remain included. Multi-display capture, one-step
Save & Run, selectable public servers and extra hardware qualification are deferred.

## Upgrade note

There is no supported in-place Project CBM release upgrade. Back up your entire
content library and wanted personal settings to another computer, keep the old card,
flash the new verified image to separate media, complete first boot, then restore
content with file sharing or SFTP. Restore preferences selectively rather than
copying system/account files. See [backup and recovery](recovery.md#upgrade-or-reflash).

[User Manual](user-guide.md) · [Assembly64](online-library.md) · [Content/USB](content.md)
· [Screenshots](screenshots.md) · [Startup](boot.md)
