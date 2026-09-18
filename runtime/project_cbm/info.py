"""Read-only, bounded information collectors and stable JSON/text presentation."""
import argparse
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys

from .data import LIMIT, loads, registry, text, token
from . import preferences, network_info

PACKAGES = {'menu': 'project-cbm-menu', 'vice': 'project-cbm-vice', 'tcpser': 'project-cbm-tcpser'}
SERVICES = {'ssh': 'ssh.service', 'samba': 'smbd.service', 'tcpser': 'tcpser.service', 'avahi': 'avahi-daemon.service', 'network_manager': 'NetworkManager.service', 'first_boot': 'pcbm-first-boot.service'}


class Local:
    """Injectable OS boundary; no shell, inherited credentials or network requests."""
    def read(self, path):
        with open(path, 'rb') as stream:
            raw = stream.read(LIMIT + 1)
        if len(raw) > LIMIT:
            raise ValueError('too_large')
        return raw.decode('utf-8')

    def paths(self, pattern):
        import glob
        return sorted(glob.glob(pattern))[:64]

    def exists(self, path):
        return Path(path).is_file()

    def uname(self):
        u = os.uname()
        return {'architecture': u.machine, 'kernel': u.release, 'hostname': u.nodename, 'system': u.sysname}

    def storage(self):
        s = os.statvfs('/')
        return {'total_bytes': s.f_blocks * s.f_frsize, 'available_bytes': s.f_bavail * s.f_frsize, 'free_bytes': s.f_bfree * s.f_frsize}

    def command(self, args):
        result = subprocess.run(args, capture_output=True, text=True, timeout=1,
                                env={'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'SYSTEMD_COLORS': '0', 'SYSTEMD_PAGER': 'cat'})
        if len(result.stdout) > LIMIT:
            raise ValueError('too_large')
        return result.returncode, result.stdout


def os_release(raw):
    allowed = {'ID', 'NAME', 'PRETTY_NAME', 'VERSION_ID', 'VERSION_CODENAME'}
    data = {}
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        key, sep, value = line.partition('=')
        if not sep or key not in allowed:
            continue
        if key.lower() in data:
            raise ValueError('duplicate_os_key')
        # shlex performs quoting only; no variable expansion or execution.
        parts = shlex.split(value, comments=False, posix=True)
        if len(parts) != 1:
            raise ValueError('invalid_os_value')
        data[key.lower()] = text(parts[0])
    if not data:
        raise ValueError('missing_os_identity')
    return {k.lower(): data.get(k.lower()) for k in sorted(allowed)}


def identity(raw):
    """Validate the supported identity projection, never pass through extra fields."""
    d = loads(raw)
    if not isinstance(d, dict) or d.get('format') != 'project-cbm.image-identity' or type(d.get('schema_version')) is not int or d['schema_version'] != 1:
        raise ValueError('unsupported_identity')
    if type(d.get('fixture')) is not bool or type(d.get('configuration_schema_version')) is not int or d['configuration_schema_version'] < 1:
        raise ValueError('invalid_identity')
    if not isinstance(d.get('components'), dict):
        raise ValueError('invalid_components')
    result = {'fixture': d['fixture'], 'product_version': token(d['product']['version']), 'candidate': token(d['product']['candidate']),
              'build_id': token(d['build_id'], r'[a-f0-9]{64}'), 'release_lock_sha256': token(d['release_lock_sha256'], r'[a-f0-9]{64}'),
              'integration_commit': token(d['integration_commit'], r'[a-f0-9]{40}'), 'architecture': token(d['architecture']),
              'configuration_schema_version': d['configuration_schema_version'],
              'base': {k: text(d['base'][k]) for k in ('distribution', 'suite', 'release_identity')},
              'components': {}}
    for key in PACKAGES:
        component = d['components'].get(key)
        result['components'][key] = None if component is None else {k: token(component[k]) for k in ('version', 'package_version')}
    return result


def packages(raw):
    output = {key: {'installed': False, 'version': None} for key in PACKAGES}
    for line in raw.splitlines():
        fields = line.split('\t')
        if len(fields) != 3:
            raise ValueError('package_format')
        name, version, state = fields
        for key, package in PACKAGES.items():
            if name.split(':')[0] == package:
                if output[key]['version'] is not None:
                    raise ValueError('duplicate_package')
                output[key] = {'installed': state == 'installed', 'version': token(version) if state == 'installed' else None}
    return output


def service_states(raw):
    output = {key: None for key in SERVICES}
    for block in raw.strip().split('\n\n'):
        fields = dict(line.split('=', 1) for line in block.splitlines() if '=' in line)
        for name, unit in SERVICES.items():
            if fields.get('Id') == unit:
                output[name] = {key: token(fields[key]) if fields.get(key) else None for key in ('LoadState', 'ActiveState', 'SubState', 'UnitFileState')}
    return output


def drm_modes(raw):
    data = loads(raw)
    rows = data['connectors']
    if not isinstance(rows, list) or len(rows) > 256:
        raise ValueError('drm_size')
    modes = {}
    for row in rows:
        card, connector = row['card'], row['connector_id']
        if type(card) is not int or not 0 <= card < 16 or type(connector) is not int or connector < 0:
            raise ValueError('drm_id')
        key = (card, connector)
        if key in modes:
            raise ValueError('duplicate_drm_id')
        active = row['active']
        modes[key] = None
        if active is not None:
            width, height, refresh = (active[k] for k in ('width', 'height', 'refresh_hz'))
            if not all(type(v) is int for v in (width, height, refresh)) or not (0 < width <= 32768 and 0 < height <= 32768 and 0 <= refresh <= 1000):
                raise ValueError('drm_mode')
            modes[key] = {'width': width, 'height': height, 'refresh_hz': refresh or None}
    return modes


def collect(source=None, preference_path=None, profiles=None):
    source = Local() if source is None else source
    issues = []

    def attempt(name, fn, fallback=None):
        try:
            return fn()
        except (OSError, ValueError, KeyError, TypeError, UnicodeError, subprocess.SubprocessError):
            issues.append({'collector': name, 'code': 'unavailable_or_invalid'})
            return fallback

    profiles = attempt('profiles', registry, []) if profiles is None else profiles
    built = attempt('identity', lambda: identity(source.read('/usr/share/project-cbm/identity.json')))
    uname = attempt('platform', source.uname, {})
    running = {k: uname.get(k) for k in ('architecture', 'kernel')}
    current = {'hostname': attempt('hostname', lambda: text(uname['hostname']))}
    running['model'] = attempt('model', lambda: text(source.read('/proc/device-tree/model').rstrip('\0\n')))
    def soc():
        values = source.read('/proc/device-tree/compatible').strip('\0\n').split('\0')
        return next((text(v) for v in values if v.startswith('brcm,')), None)
    running['soc'] = attempt('soc', soc)
    def cpu():
        for line in source.read('/proc/cpuinfo').splitlines():
            key, _, value = line.partition(':')
            if key.strip() == 'model name':
                return text(value.strip())
        return None
    running['cpu_model'] = attempt('cpu', cpu)
    def read_os():
        try:
            raw = source.read('/etc/os-release')
        except FileNotFoundError:
            raw = source.read('/usr/lib/os-release')
        return os_release(raw)
    running['os'] = attempt('os', read_os)
    running['debian_version'] = attempt('debian', lambda: text(source.read('/etc/debian_version').strip()))
    def memory():
        fields = {}
        for line in source.read('/proc/meminfo').splitlines():
            m = re.fullmatch(r'(MemTotal|MemAvailable):\s+(\d+) kB', line)
            if m:
                fields[m[1]] = int(m[2]) * 1024
        total = fields['MemTotal']
        available = fields.get('MemAvailable')
        if total <= 0 or available is not None and not 0 <= available <= total:
            raise ValueError('memory_range')
        return {'usable_total_bytes': total, 'available_bytes': available}
    running['memory'] = attempt('memory', memory)
    running['root_storage'] = attempt('storage', source.storage)
    def displays():
        result = []
        modes = {}
        helper = '/usr/libexec/project-cbm-vice/drm-state'
        if source.exists(helper) and source.exists('/etc/pcbm/engineering-poc'):
            def query_modes():
                code, raw = source.command([helper])
                if code != 0:
                    raise ValueError('drm_query_failed')
                return drm_modes(raw)
            modes = attempt('active_drm', query_modes, {})
        paths = source.paths('/sys/class/drm/card*-*/status')
        if not paths:
            raise ValueError('no_drm_interface')
        for path in paths:
            status = source.read(path).strip()
            if status != 'connected':
                continue
            parent = str(Path(path).parent)
            enabled = attempt('display_enabled', lambda: source.read(parent + '/enabled').strip())
            name = text(Path(parent).name)
            active = None
            if modes:
                def match_mode():
                    match = re.match(r'card([0-9]+)-', name)
                    if match is None:
                        raise ValueError('unrecognized_card_name')
                    card = int(match.group(1))
                    connector = int(source.read(parent + '/connector_id').strip())
                    return modes.get((card, connector))
                active = attempt('display_match', match_mode)
            result.append({'connector': name, 'enabled': enabled == 'enabled' if enabled in ('enabled', 'disabled') else None, 'active_mode': active})
        # modes lists advertised modes, NOT the active CRTC mode. Do not guess.
        if any(v['active_mode'] is None for v in result):
            issues.append({'collector': 'display_mode', 'code': 'not_exposed_by_collector'})
        return result
    running['displays'] = attempt('display', displays) if uname.get('system') == 'Linux' else None
    def installed():
        code, raw = source.command(['/usr/bin/dpkg-query', '-W', '-f=${binary:Package}\t${Version}\t${db:Status-Status}\n', *PACKAGES.values()])
        if code not in (0, 1):
            raise ValueError('package_query_failed')
        if code == 1 and not raw:
            # Query failure and all-absent cannot safely be distinguished here.
            raise ValueError('package_query_empty')
        return packages(raw)
    current['packages'] = attempt('packages', installed)
    def services():
        code, raw = source.command(['/usr/bin/systemctl', '--system', '--no-pager', 'show', '--property=Id,LoadState,ActiveState,SubState,UnitFileState', *SERVICES.values()])
        if code != 0:
            raise ValueError('service_query_failed')
        return service_states(raw)
    current['services'] = attempt('services', services)
    def network():
        result = []
        for path in source.paths('/sys/class/net/*/operstate'):
            name = Path(path).parent.name
            if name != 'lo':
                result.append({'interface': token(name), 'operstate': token(source.read(path).strip())})
        return result
    current['network_links'] = attempt('network', network) if uname.get('system') == 'Linux' else None
    current['network_interfaces'] = network_info.collect(source, attempt) if uname.get('system') == 'Linux' else None
    def legacy(path, allowed):
        value = source.read(path).strip()
        if value not in allowed:
            raise ValueError('invalid_legacy_setting')
        return value
    current['preferences'] = preferences.read(preference_path, profiles) if profiles else None
    legacy_raw = ''
    if current['preferences'] is not None and current['preferences']['status'] != 'ok':
        legacy_raw = attempt('legacy_default', lambda: source.read('/etc/pcbm/default-machine.conf'), '')
    selected = attempt('default_machine', lambda: preferences.selection(preference_path, profiles,
        legacy_raw=legacy_raw, snapshot=current['preferences'])) if profiles else None
    current['default_machine'] = {key: selected[key] if selected else None for key in ('id', 'name', 'source')}
    current['boot_mode'] = {'configured': attempt('boot_mode', lambda: legacy('/etc/pcbm/boot-mode.conf', {'menu', 'machine', 'MENU', 'MACHINE', 'Menu', 'Machine'})), 'effective': None}
    issues.append({'collector': 'effective_boot_mode', 'code': 'not_exposed_by_collector'})
    if current['preferences'] is not None and current['preferences']['status'] == 'invalid':
        issues.append({'collector': 'preferences', 'code': 'unavailable_or_invalid'})
    return {'format': 'project-cbm.info', 'schema_version': 1, 'built_as': built, 'running_on': running, 'current_state': current, 'issues': issues}


def human(data):
    b = data['built_as'] or {}
    r = data['running_on']; c = data['current_state']
    def size(value):
        return 'unknown' if value is None else f'{value / (1024 ** 3):.2f} GiB'
    def component(key):
        expected = ((b.get('components') or {}).get(key) or {}).get('version')
        installed = ((c['packages'] or {}).get(key) or {}).get('version')
        return f'{expected or "unknown"} (current package: {installed or "unavailable/not installed"})'
    os_data = r['os'] or {}; mem = r['memory'] or {}; disk = r['root_storage'] or {}
    displays = r['displays']
    display = 'unknown' if displays is None else ', '.join(x['connector'] + ((' ' + str(x['active_mode']['width']) + 'x' + str(x['active_mode']['height']) + (' @ ' + str(x['active_mode']['refresh_hz']) + ' Hz' if x['active_mode']['refresh_hz'] else '')) if x['active_mode'] else ' (mode unavailable)') for x in displays) or 'none connected'
    rows = [('Project CBM', b.get('product_version')), ('Candidate', b.get('candidate')), ('Build', b.get('build_id')),
            ('Menu', component('menu')), ('VICE', component('vice')), ('TCPser', component('tcpser')),
            ('Hardware', r['model']), ('Architecture', r['architecture']), ('Memory (usable)', size(mem.get('usable_total_bytes'))),
            ('OS', os_data.get('pretty_name')), ('Kernel', r['kernel']), ('Display', display),
            ('Root storage', size(disk.get('total_bytes')) + ' total; ' + size(disk.get('available_bytes')) + ' available'),
            ('Hostname', c['hostname']), ('Default machine', c['default_machine']['name']),
            ('Boot mode', 'unknown (configured: ' + (c['boot_mode']['configured'] or 'unknown') + ')')]
    lines = ['Project CBM System Information']
    if b.get('fixture'):
        lines.append('SYNTHETIC FIXTURE — not a release or hardware result')
    lines += [f'{key:18} {value if value is not None else "unknown"}' for key, value in rows]
    links = c['network_links']
    lines.append('Network links      ' + ('unknown' if links is None else ', '.join(v['interface'] + ': ' + v['operstate'] for v in links) or 'none observed'))
    for row in c.get('network_interfaces') or []:
        lines.append(f"  {row['interface']} ({row['type']}): {row['state']}; link {row['operstate']}")
        lines.append('    MAC: ' + (row['mac'] or 'unavailable'))
        for family in ('ipv4', 'ipv6'):
            lines.append('    ' + family.upper() + ': ' + (', '.join(row[family]) or 'none assigned'))
        if row['ssid'] is not None: lines.append('    SSID: ' + row['ssid'])
    if c['services'] is not None:
        labels = {'ssh': 'SSH', 'samba': 'Samba', 'tcpser': 'Modem/BBS', 'avahi': 'mDNS', 'network_manager': 'Network', 'first_boot': 'First boot'}
        def state(value):
            if value is None:
                return 'unknown'
            if value['LoadState'] == 'not-found':
                return 'not installed'
            if value['UnitFileState'] == 'masked' or value['LoadState'] == 'masked':
                return 'unavailable (masked)'
            return {'active': 'running', 'inactive': 'stopped', 'failed': 'failed'}.get(value['ActiveState'], 'unknown')
        lines.append('Services           ' + ', '.join(labels[key] + ': ' + state(v) for key, v in c['services'].items()))
    lines.append('User preferences   ' + (c['preferences'] or {}).get('source', 'unavailable') + ' (default machine applied; boot preference not applied)')
    if data['issues']:
        lines.append('Some information is unavailable; --json includes collection status.')
    return '\n'.join(lines) + '\n'


def main(argv=None):
    parser = argparse.ArgumentParser(description='Read-only Project CBM system information')
    parser.add_argument('--json', action='store_true', help='versioned structured information for tools')
    args = parser.parse_args(argv)
    try:
        data = collect()
    except (ValueError, OSError, TypeError):
        print('Project CBM profile data is unavailable or invalid; check the runtime installation.', file=sys.stderr)
        return 2
    print(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=True) if args.json else human(data), end='\n' if args.json else '')
    return 0
