"""Bounded data parsing; never execute configuration or include raw errors."""
import json
import re
from pathlib import Path

LIMIT = 65536


def loads(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('duplicate_key')
            result[key] = value
        return result

    def invalid(_):
        raise ValueError('invalid_number')

    if len(raw) > LIMIT:
        raise ValueError('too_large')
    try:
        return json.loads(raw, object_pairs_hook=pairs, parse_constant=invalid)
    except (UnicodeError, RecursionError) as exc:
        raise ValueError('invalid_json') from exc


def read_json(path):
    with Path(path).open('rb') as stream:
        return loads(stream.read(LIMIT + 1))


def text(value, limit=256):
    if not isinstance(value, str) or not value or len(value) > limit:
        raise ValueError('invalid_text')
    if not all(c.isprintable() for c in value):
        raise ValueError('control_character')
    return value


def token(value, pattern=r'[A-Za-z0-9][A-Za-z0-9._+~:-]*'):
    text(value)
    if not re.fullmatch(pattern, value):
        raise ValueError('invalid_token')
    return value


def registry(path=None):
    path = path or Path(__file__).resolve().parents[1] / 'data/profiles.json'
    data = read_json(path)
    if not isinstance(data, dict) or set(data) != {'schema_version', 'profiles'} or type(data['schema_version']) is not int or data['schema_version'] != 1:
        raise ValueError('registry_schema')
    profiles = data['profiles']
    if not isinstance(profiles, list) or not 1 <= len(profiles) <= 32:
        raise ValueError('registry_size')
    seen = set()
    for p in profiles:
        if not isinstance(p, dict) or set(p) != {'id', 'name', 'executable', 'description', 'video_chips', 'recommended', 'launch_options'}:
            raise ValueError('registry_fields')
        token(p['id'], r'x[a-z0-9]+(?:-80col)?')
        token(p['executable'], r'x[a-z0-9]+')
        text(p['name']); text(p['description'])
        if p['id'] in seen or type(p['recommended']) is not bool:
            raise ValueError('registry_duplicate')
        expected = ['-80col'] if p['id'] == 'x128-80col' else []
        if p['launch_options'] != expected or p['executable'] != ('x128' if p['id'] == 'x128-80col' else p['id']):
            raise ValueError('registry_launch_contract')
        seen.add(p['id'])
        if not isinstance(p['video_chips'], list) or not p['video_chips'] or len(set(p['video_chips'])) != len(p['video_chips']):
            raise ValueError('registry_chips')
        if not set(p['video_chips']) <= {'VICII', 'VDC', 'VIC', 'TED', 'CRTC'}:
            raise ValueError('registry_chips')
    if sum(p['recommended'] for p in profiles) != 1:
        raise ValueError('registry_default')
    return profiles
