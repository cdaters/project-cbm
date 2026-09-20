"""Small content policy for two native C64 applications; no plugin or downloader."""
from pathlib import Path
import stat
from .data import text

from .library import ROOT as CONTENT_ROOT
APP_FOLDERS = (('music', 'Creation', 'SID-Wizard'),
               )
NEW_APP_FOLDERS = (('music', 'c64', 'Creation', 'SID-Wizard'),
                   ('programs', 'c64', 'Communications', 'CCGMS'))


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
    if relative.parts[:3] not in APP_FOLDERS and relative.parts[:4] not in NEW_APP_FOLDERS:
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


def content_options(media, profile, root=CONTENT_ROOT, modem_path=Path('/etc/project-cbm/modem.json')):
    """Per-launch media options; never save emulator preferences or enable services."""
    path=Path(media)
    if path.is_symlink() or not path.is_file():
        raise ValueError('redirected_content')
    options=[]
    if path.suffix.lower()=='.g71':
        if profile not in ('x64','x64sc','x128','x128-80col'):
            raise ValueError('g71_requires_c64_c128')
        options += ['-drive8type','1571']
    try:relative=path.relative_to(Path(root).resolve())
    except ValueError:return options  # Existing direct launches outside the library.
    if path.resolve(strict=True)!=path:raise ValueError('redirected_content')
    if relative.parts[:4]==('programs','c64','Communications','CCGMS'):
        if profile!='x64sc':raise ValueError('ccgms_requires_c64')
        from .data import read_json
        from .modem import arguments
        settings=read_json(modem_path)
        arguments(settings)  # Same typed port/baud contract as the existing adapter.
        options += ['-acia1','-acia1mode','1','-acia1base','56832','-acia1irq','1',
                    '-myaciadev','0','-rsdev1','127.0.0.1:'+str(settings['port']),'-rsdev1ip232']
    return options
