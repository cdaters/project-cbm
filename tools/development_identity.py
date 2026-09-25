"""Explicit private 1.2 admission; no public-release identity or fallback."""
import re


def development_number(product):
    version = product.get('version', '')
    candidate = product.get('candidate', '')
    match = re.fullmatch(r'1\.2\.0-dev\.([1-9][0-9]*)', version)
    if match and candidate == 'private-engineering-1.2-dev' + match[1]:
        return match[1]
    if version.startswith('1.2') or candidate.startswith('private-engineering-1.2'):
        raise ValueError('1.2 requires matching explicit private development identity')
    return None


def development_packages(runtime, menu):
    if not re.fullmatch(r'1\.2\.0~dev[1-9][0-9]*-1', runtime):
        raise ValueError('private development Runtime package required')
    if not re.fullmatch(r'1\.2\.0~dev[1-9][0-9]*-1\+pcbm1', menu):
        raise ValueError('private development Menu package required')


def configuration_path(recipe, product):
    name = 'config-development.json' if development_number(product) else 'config.json'
    return recipe / 'build/pigen' / name


def export_path(recipe, product):
    name = 'EXPORT_IMAGE_DEVELOPMENT' if development_number(product) else 'EXPORT_IMAGE'
    return recipe / 'build/pigen/stage-cbm' / name


def valid_menu_tag(tag):
    return bool(re.fullmatch(r'v1\.1\.0(?:_(?:poc4\.[0-9]+|rc[0-9]+))?', tag)
                or re.fullmatch(r'v1\.2\.0_dev[1-9][0-9]*', tag))
