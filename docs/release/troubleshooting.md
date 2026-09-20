# Troubleshooting Project CBM

[Documentation index](../README.md) · [User Manual](user-guide.md) · [Backup/recovery](recovery.md)

Start with the screen's message and the simplest check. Avoid changing several emulator,
network and system settings together. If you are qualifying a release image, record the
failure before repairing or reflashing it. Builder problems have a
[separate section](build-your-own.md#builder-troubleshooting).

## Startup, keyboard and display

| Problem | First things to try |
| --- | --- |
| No display | Check power supply, HDMI cable/input, and a display known to work with the Pi. Verify the downloaded image and that flashing completed. Allow video establishment time |
| Never reaches Menu | Note whether artwork, setup or an error appeared. Keep a photo of the error; try console/SSH if available. Protect content before reflash |
| First boot takes longer | Storage preparation and Wi-Fi can take time. Follow working-state messages; do not interrupt card writes merely because another Pi was faster |
| Setup appears again | A paused/failed setup resumes by design. If a fully completed setup repeats, record the last successful screen and report it |
| Keyboard does not respond | Check connection/battery, try a simple wired USB keyboard, and check Tab/button focus. A media-key keyboard may need Fn for F10 |
| Wrong typed characters | Verify the layout under CONTROL → Language, Keyboard and Region and reboot. Passwords entered before that reboot used the previously active layout |
| Artwork missing | A missing Cover should not stop emulation. Record machine and display behavior; use the correct unmodified image before experimenting with artwork or video settings |

Do not promise recovery by pulling power during writes. If normal shutdown is impossible,
keep the failing card and obtain help with recovery rather than repeatedly power-cycling.
[Verbose startup](boot.md#verbose-recovery) is an advanced option.

## Network and services

| Problem | First things to try |
| --- | --- |
| Wi-Fi list empty | Set the correct Wi-Fi country, wait for the scan to finish, then rescan if the radio/network genuinely changed. Check router distance/band availability; continue offline if necessary |
| Wi-Fi password rejected | Confirm exact SSID, current keyboard layout and WPA personal password. Enterprise/open networks need Advanced configuration |
| Ethernet has no IP | Check cable/router port, enable normal networking, and inspect Network/System Information. An offline setting disconnects Ethernet too |
| `.local` fails | Turn on Network Discovery; try the current numeric IP. Guest Wi-Fi or router filtering can prevent local-name discovery |
| SSH connection refused | Check Remote Access reports On and use the displayed address. Username is pcbm, password is the administrator password |
| Sharing missing in Finder/Explorer | Use the direct SMB address from How to connect. Browsing can fail while direct sharing works |
| Sharing password rejected | Use the separate File Sharing password and username pcbm. Clear a stale saved client credential, then reconnect |
| Service remains Pending/Failed | Refresh status, check networking/setup completion, then preserve the message. Do not assume an enabled preference means the service is ready |

[Networking](networking.md) has the full Mac/Windows paths and enable/disable steps.

## Content and USB

| Problem | First things to try |
| --- | --- |
| Drive not listed | Insert before opening IMPORT, reopen the screen, and confirm FAT/exFAT/ext4. Already mounted drives and the system disk are excluded |
| Copy incomplete | Read the error and release status. Check free space and supported file types. Earlier files may have copied; same-name destinations are preserved on retry |
| Cannot safely remove drive | If unmount/release was not confirmed, leave it inserted and shut down safely before unplugging |
| Imported files not visible | Check `category/machine/Imported` and source subfolders; SID files always go to `music/c64/Imported` |
| File copied to home but absent from CONTENT | Move it into the `content` library's proper category/machine folder using FILES or SFTP |
| File browses but will not launch | ROM/BIN/REU resources require VICE configuration; SID playback is not integrated. Other media must match the selected machine/drive/RAM |
| G71 imported but not listed | Current CONTENT omits `.g71`; open it through compatible VICE media controls. This source mismatch is recorded for release review |
| A hidden media file is in FILES but not CONTENT | Import and CONTENT have separate filtering. Inspect in FILES and use a normal visible filename if appropriate; do not assume copy failed |
| Updated same-name game was not copied | USB import preserves existing names. Keep both versions under distinct names or replace deliberately in FILES after backup |

Do not clean a source drive merely to make counts match. The [narrow metadata policy](content.md#host-metadata-and-counts)
excludes known housekeeping entries, not all possible hidden retro content.

## VICE, sound and return

| Problem | First things to try |
| --- | --- |
| Emulation/music runs slowly | Use Pi 4-class supported hardware, normal Commodore 64 profile, a suitable supply and cooling. Check whether you changed expensive emulator settings; compare after backing up preferences. One workload's success does not prove all workloads |
| No sound | Check display speakers/volume, CONTROL → Picture, Sound and Controllers → Audio output and test, then test the connected HDMI output. Check VICE sound is enabled |
| Game controls fail | Commodore joystick port/key mappings are in VICE's F10 settings. The keyboard working in Project CBM does not select the game's required joystick port |
| Disk does not start | Confirm the machine family and software instructions. Attach the correct drive type/memory expansion where needed; multi-disk software may need manual disk changes |
| F10 does not open VICE menu | Try Fn+F10, check keyboard function-key mode. Record the profile and any changed VICE menu-key setting |
| Ctrl+Alt+F2 fails in VICE | Known limitation: quit with F10 → Quit first, then switch from Project CBM |
| Quit does not return cleanly | Stop repeated launches, preserve what is visible and the relevant launch diagnostics if accessible, then report the exact version/machine |
| POWER/REBOOT fails | Wait for the operation/error message. Use Advanced or SSH for orderly Linux shutdown only if you understand the operation; preserve evidence of the failed normal action |

## Reporting a problem

Include the Project CBM version, Pi model, what you selected, expected result and actual
result. System Information and About supply useful facts. Share a relevant screenshot
with passwords and private network details removed. Do not upload account databases,
Wi-Fi connection files, private SSH keys or entire unreviewed journals. Personal content
may also have redistribution restrictions. The [layout reference](accounts-and-layout.md)
helps an experienced user locate a specific diagnostic without exposing unrelated data.
