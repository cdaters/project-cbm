"""Explicit build-process environments; never copy the operator environment."""
import re

PATH = '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'


def environment(source_date_epoch=None, *, target=False):
    result = {'PATH': PATH, 'HOME': '/root', 'USER': 'root', 'LOGNAME': 'root',
              'LANG': 'C.UTF-8', 'LC_ALL': 'C.UTF-8', 'TMPDIR': '/tmp',
              'TMP': '/tmp', 'TEMP': '/tmp', 'PYTHONDONTWRITEBYTECODE': '1'}
    if source_date_epoch is not None:
        value = str(source_date_epoch)
        if not re.fullmatch(r'[0-9]{1,12}', value):
            raise ValueError('invalid declared SOURCE_DATE_EPOCH')
        result['SOURCE_DATE_EPOCH'] = value
    if target:
        result['DEBIAN_FRONTEND'] = 'noninteractive'
    return result
