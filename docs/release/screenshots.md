# Take screenshots from SSH

Enable **Remote Access (SSH)** in CONTROL → Services. From another computer, connect
as `pcbm` using your configured hostname, then capture the screen currently visible
on the Pi's HDMI display:

```sh
ssh pcbm@projectcbm.local 'pcbm-screenshot'
```

The command prints the exact saved PNG path. Images live in
`/home/pcbm/content/screenshots/`, with UTC names such as
`pcbm-20260927T044557Z.png`. Captures in the same second get `-01`, `-02`, and so on.
Existing files are never overwritten. An optional name must be a plain filename
ending in `.png`, for example `pcbm-screenshot my-test.png`; do not supply a path.

Open the `screenshots` folder in your authenticated **Project CBM** file share, or
copy the printed file with SFTP. The command works without a desktop or DISPLAY
setting. It captures Menu, Midnight Commander, guided Import and supported VICE
screens, including gameplay. A Cover can be captured during its normal short display
interval; it is not held on screen for a screenshot.

Capture is on demand only: no upload, background recording or video. Screenshots may
include personal filenames or anything else visible on the display. Review them
before sharing. The screenshot directory and files are private to the `pcbm` account;
file sharing uses that same authenticated account.

If no usable display is active or the picture changes to an unsupported display
configuration, the command reports that capture is unavailable and does not leave a
partial PNG. Multiple displays are not qualified. Moving-frame captures are not a
promise of perfectly tear-free video. No Menu Screenshot action or generic
`screenshot` command is provided.

[Networking and SSH](networking.md) · [User Manual](user-guide.md)
