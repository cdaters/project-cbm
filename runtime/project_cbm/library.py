"""Product-owned content layout, independent of the administrator's home."""
from pathlib import Path

ROOT = Path('/home/pi/pcbm')
# Registry IDs, never executable paths. The chosen ID is checked against the registry.
FAMILIES = {
    'c64': ('Commodore 64', ('x64sc', 'x64', 'xscpu64', 'x64dtv')),
    'c128': ('Commodore 128', ('x128', 'x128-80col')),
    'vic20': ('Commodore VIC-20', ('xvic',)),
    'plus4': ('Commodore Plus/4', ('xplus4',)),
    'pet': ('Commodore PET', ('xpet',)),
    'cbm2': ('Commodore CBM-II', ('xcbm2',)),
    'cbm5x0': ('Commodore CBM-II 5x0', ('xcbm5x0',)),
    'shared': ('Shared / choose using RUN default', ()),
}
CATEGORIES = ('games', 'demos', 'programs', 'music', 'roms')
MUSIC_FAMILIES = ('c64', 'c128', 'vic20', 'plus4', 'shared')


def directories():
    """Fresh-image directories only; existing user trees are never rearranged."""
    for category in CATEGORIES:
        families = MUSIC_FAMILIES if category == 'music' else FAMILIES
        for family in families:
            if category == 'roms' and family == 'shared':
                continue
            yield Path(category) / family
    yield Path('screenshots')
    yield Path('saves')


def content_profile(path, profiles, default, root=ROOT):
    """Machine-tagged folders select a compatible profile without saving a default."""
    path, root = Path(path), Path(root).resolve(strict=True)
    if not path.is_absolute() or '..' in path.parts or not path.is_file():
        raise ValueError('invalid_content')
    relative = path.relative_to(root)
    if path.resolve(strict=True) != path:
        raise ValueError('redirected_content')
    parts = relative.parts
    if not parts or parts[0] not in CATEGORIES:
        raise ValueError('outside_content_categories')
    if parts[0] == 'roms' or path.suffix.lower() in ('.rom', '.bin', '.reu'):
        raise ValueError('resource_requires_vice_settings')
    if len(parts) < 3 or parts[1] not in FAMILIES or parts[1] == 'shared':
        return default  # Legacy unclassified files remain accessible; no guessing.
    choices = FAMILIES[parts[1]][1]
    if parts[1:3] == ('c128', '80col'):
        selected = 'x128-80col'
    else:
        selected = default if default in choices else choices[0]
    if not any(p['id'] == selected for p in profiles):
        raise ValueError('content_profile_unavailable')
    return selected


def import_destination(category, extension, family=None):
    if category not in ('games', 'demos', 'programs', 'music'):
        raise ValueError('import_category')
    if family is not None and family not in FAMILIES:
        raise ValueError('import_family')
    # Legacy clients retain their old destination; the current UI always chooses a family.
    if family is None:
        return ('music' if extension == '.sid' else category, 'Imported')
    if extension == '.sid':
        return ('music', 'c64', 'Imported')
    return (category, family, 'Imported')
