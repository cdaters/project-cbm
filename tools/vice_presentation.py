"""Product initial VICE settings; no per-launch preference overwrite."""
import os
from pathlib import Path

CHIPS = {
    'C64': ('VICII',), 'C64SC': ('VICII',), 'SCPU64': ('VICII',),
    'C64DTV': ('VICII',), 'C128': ('VICII', 'VDC'),
    'CBM-II': ('Crtc',), 'CBM-II-5x0': ('VICII',),
    'VIC20': ('VIC',), 'PLUS4': ('TED',), 'PET': ('Crtc',),
}


def defaults():
    lines = ['[Version]', 'ConfigVersion=3.10', '']
    for section, chips in CHIPS.items():
        lines.append('[' + section + ']')
        for chip in chips:
            lines += [chip+'AspectMode=2', chip+'Fullscreen=1', chip+'FullscreenMode=0']
        lines.append('')
    return '\n'.join(lines).encode()


def seed(path):
    """Create initial user-owned configuration only if absent, including symlinks.

    Used solely in image construction before sealing. Runtime does not call this.
    Preserve existing config bytes; exclusive create also refuses symlink targets.
    """
    path = Path(path)
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    except FileExistsError:
        return False
    with os.fdopen(fd, 'wb') as stream:
        stream.write(defaults())
        stream.flush()
        os.fsync(stream.fileno())
    return True
