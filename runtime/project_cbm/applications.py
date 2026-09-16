"""Small content policy for two native C64 applications; no plugin or downloader."""
from pathlib import Path
import stat
from .data import text

CONTENT_ROOT = Path('/home/pi/pcbm')
APP_FOLDERS = (('music', 'Creation', 'SID-Wizard'),
               ('programs', 'Communications', 'StrikeTerm'))


def application_profile(media, profiles, root=CONTENT_ROOT):
    """Return a registry ID for admitted app folders, or None for ordinary content.

    An owner-supplied disk is not authenticated software. Structural checks only
    establish supported media, never copyright permission or safe C64 behavior.
    """
    value = text(str(media), 1024)
    path = Path(value)
    if not path.is_absolute() or '..' in path.parts or not path.is_file():
        raise ValueError('invalid_content')
    root = Path(root).resolve(strict=True)
    relative = path.relative_to(root)
    if not stat.S_ISREG(path.stat().st_mode) or path.resolve(strict=True) != path:
        raise ValueError('redirected_content')
    if relative.parts[:3] not in APP_FOLDERS:
        return None
    if path.suffix.lower() != '.d64' or path.stat().st_size != 174848:
        raise ValueError('application_requires_standard_d64')
    with path.open('rb') as stream:
        stream.seek(357*256)  # track 18 sector 0, BAM/directory start
        bam = stream.read(256)
        directory = stream.read(256)
    if bam[:3] != bytes([18, 1, 65]) or (directory[2] & 7) != 2:
        raise ValueError('application_disk_missing_first_prg')
    if not any(p['id'] == 'x64sc' and p['executable'] == 'x64sc' for p in profiles):
        raise ValueError('c64_profile_unavailable')
    return 'x64sc'
