# Backups, upgrades and user recovery

[Documentation index](../README.md) · [Troubleshooting](troubleshooting.md)

Keep a copy of your work before reflashing, replacing a card or experimenting. A copy
on the same SD card does not protect against card failure. Use another computer or
independent storage and check that you can open files from the backup.

## Back up your files

The main thing to preserve is **/home/pcbm/content**: games, demos, programs, music,
resources, saves and any writable application disks you edited. Through File Sharing,
copy the whole **Project CBM** share to a dated folder on your other computer. Wait for
the copy to finish, check several files, then disconnect the share. USB IMPORT brings
files into the Pi; it is not a backup/export feature.

Preferences are outside the share. If you want them too, use an SFTP client with Remote
Access enabled. Save these folders/files privately:

| Location | Why preserve it? |
| --- | --- |
| `/home/pcbm/.config/project-cbm` | RUN default and appliance preferences |
| `/home/pcbm/.config/vice` | Saved emulator settings |
| `/home/pcbm/.local/share/vice` | Personal VICE data/keymaps if used |
| `/home/pcbm/.config/pcbm` | Audio and other legacy UI preferences if present |
| `/home/pcbm/.asoundrc` | Your selected ALSA output if present; review before restoring to different hardware |
| Other personal files/application data you created | Work saved outside the normal library |

You do not need to copy system programs to preserve your collection; the image supplies
them. Configuration/application files can include private paths or login details. Keep
personal backups private, preferably encrypted. Do not publish a used-card image.

### An rsync example for experienced users

Run this on a Mac/Linux computer with rsync installed and Remote Access enabled on the
Pi. It copies the library to a new dated backup folder; it does not delete remote files.

```sh
PROJECT_CBM_BACKUP="$HOME/ProjectCBM-backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$PROJECT_CBM_BACKUP/content"
rsync -rt --ignore-existing -- pcbm@projectcbm.local:/home/pcbm/content/ "$PROJECT_CBM_BACKUP/content/"
```

Use a new backup directory for each snapshot. `--ignore-existing` preserves names
already in that backup, so it is not a command for refreshing changed same-name saves.
SFTP or Finder/Explorer is simpler for many users.

## Upgrade or reflash

Project CBM is an appliance image: the OS, emulator and Menu are tested together.
There is no supported Menu-driven in-place OS release upgrade. `apt full-upgrade`
is not the documented way to turn one Project CBM release into another.

1. Back up content and wanted preferences. Keep the old card until restoration works.
2. Download/check the new image and [flash](getting-started.md#flash-the-card) a card.
3. Complete first boot again with your chosen password and network settings.
4. Restore content to its matching folders through File Sharing or SFTP. USB import
   is useful for selected media, but adds Imported directories and is not a full-tree restore.
5. Check the library and a few launches. Restore settings selectively; reselect audio
   if the Pi/display changed. A saved VICE configuration may restore older emulator defaults.
6. Enable only the services you need and verify their connection information.

Do not copy an old whole `/etc`, account database, host keys, Samba password database
or setup-completed marker over a fresh system. Set the File Sharing password again.
Normal SSH host-key changes after your deliberate reflash should be verified, not
confused with an unrelated machine answering at the same address.

## Recover a setting or Menu problem

If Menu still works, undo the last setting through CONTROL. If saved machine preferences
are malformed, MACHINES can offer explicit recovery that preserves a private copy and
resets invalid values. Do not approve a reset casually if you still need that data.

CONTROL → Advanced → Terminal opens your pcbm shell. Ctrl+Alt+F2 from Menu also reaches
the local console; Ctrl+Alt+F1 returns. Type `exit` to leave a shell opened from Advanced.
SSH is another route if previously enabled. General administrative commands use `sudo`
and your first-boot password. Owners retain control of Linux; low-level display/session
changes can affect Menu return, so keep backups and change one thing at a time.

If the system cannot start, protect the card and recover personal content from a backup
or a safely handled card before reflashing. There is no universal recovery password.
An owner with physical access can use normal Linux offline recovery or reflash after
preserving data. See [verbose boot](boot.md#verbose-recovery) for a display/debug route.

Engineering recovery is a separate subject: rebuilding source, packages and images
from preserved inputs. Contributors can follow [engineering recovery](../recovery.md);
ordinary users do not need Git bundles to back up games.
