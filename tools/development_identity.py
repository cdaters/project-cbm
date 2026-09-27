"""Explicit 1.2 identities; private development and final release stay distinct."""
import re


def release_1_2(product):
    return product.get('version') == '1.2.0' and product.get('candidate') == 'release'


def content_1_2(product):
    return bool(development_number(product)) or release_1_2(product)


def release_packages(runtime, menu, capture):
    if (runtime, menu, capture) != ('1.2.0-1', '1.2.0-1+pcbm1', '1.0.0-1'):
        raise ValueError('final 1.2 requires final Runtime/Menu/capture packages')


def development_number(product):
    version = product.get('version', '')
    candidate = product.get('candidate', '')
    match = re.fullmatch(r'1\.2\.0-dev\.([1-9][0-9]*)', version)
    if match and candidate == 'private-engineering-1.2-dev' + match[1]:
        return match[1]
    if release_1_2(product):
        return None
    if version.startswith('1.2') or candidate.startswith('private-engineering-1.2'):
        raise ValueError('1.2 requires matching explicit private development identity')
    return None


def development_packages(runtime, menu):
    if not re.fullmatch(r'1\.2\.0~dev[1-9][0-9]*-1', runtime):
        raise ValueError('private development Runtime package required')
    if not re.fullmatch(r'1\.2\.0~dev[1-9][0-9]*-1\+pcbm1', menu):
        raise ValueError('private development Menu package required')


def configuration_path(recipe, product):
    name = ('config-1.2.json' if release_1_2(product) else
            'config-development.json' if development_number(product) else 'config.json')
    return recipe / 'build/pigen' / name


def export_path(recipe, product):
    name = 'EXPORT_IMAGE_DEVELOPMENT' if development_number(product) else 'EXPORT_IMAGE'
    return recipe / 'build/pigen/stage-cbm' / name


def valid_menu_tag(tag):
    return bool(re.fullmatch(r'v1\.1\.0(?:_(?:poc4\.[0-9]+|rc[0-9]+))?', tag)
                or re.fullmatch(r'v1\.2\.0(?:_dev[1-9][0-9]*)?', tag))
