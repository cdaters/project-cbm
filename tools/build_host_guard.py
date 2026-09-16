"""Refuse image construction on a package-drifted or auto-updating Linux host."""
import subprocess

UPDATE_UNITS = ('apt-daily.timer', 'apt-daily-upgrade.timer', 'apt-daily.service',
                'apt-daily-upgrade.service', 'unattended-upgrades.service')


def inventory(text):
    result = {}
    for line in text.splitlines():
        fields = line.split('\t')
        if len(fields) < 2 or not all(fields[:2]) or fields[0] in result:
            raise ValueError('invalid/duplicate host package inventory')
        result[fields[0]] = fields[1]
    if not result:
        raise ValueError('empty host package inventory')
    return result


def compare(expected, actual):
    if inventory(expected) != inventory(actual):
        raise ValueError('host package drift: retain exact inputs and freeze a new lock before building')


def verify(lock, kit):
    for unit in UPDATE_UNITS:
        state = subprocess.run(['systemctl', 'is-enabled', unit], capture_output=True, text=True)
        if state.stdout.strip() != 'masked':
            raise ValueError('automatic host updates must be masked during controlled construction: '+unit)
    actual = subprocess.check_output(['dpkg-query', '-W', '-f=${binary:Package}\t${Version}\t${source:Package}\t${source:Version}\n'], text=True)
    compare((kit/lock['build']['toolchain']['path']).read_text(), actual)
