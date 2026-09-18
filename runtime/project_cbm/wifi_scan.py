"""Wait for NetworkManager readiness and an actually completed scan, not acceptance.

Only fixed state fields are read. AP names, addresses and credentials never enter
the diagnostic result. The caller owns authorization and its compound deadline.
"""
import re
import time

NM = '/usr/bin/nmcli'
SERVICE = 'org.freedesktop.NetworkManager'
WIFI = SERVICE + '.Device.Wireless'


def devices(raw):
    rows = []
    row = {}
    for line in raw.splitlines() + ['']:
        if not line or line.startswith('GENERAL.DEVICE:'):
            if row.get('GENERAL.TYPE') == 'wifi':
                name = row.get('GENERAL.DEVICE', '')
                path = row.get('GENERAL.DBUS-PATH', '')
                state = row.get('GENERAL.STATE', '').split(' ', 1)[0]
                if (re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,14}', name)
                        and re.fullmatch(r'/org/freedesktop/NetworkManager/Devices/[0-9]+', path)
                        and state.isdecimal() and 30 <= int(state) <= 100):
                    rows.append((name, path))
            row = {}
        if line:
            key, sep, value = line.partition(':')
            if sep: row[key] = value
    return rows[:8]


def completed_scan(query, path):
    raw = query(['/usr/bin/busctl', '--system', '--timeout=1', 'get-property',
                 SERVICE, path, WIFI, 'LastScan'])
    if raw is None or not re.fullmatch(r'x -?[0-9]+\s*', raw):
        return None
    return int(raw.split()[1])


def scan(query, request, deadline, clock=time.monotonic, pause=time.sleep):
    start = clock()
    end = min(deadline, start + 25)
    ready_end = min(end, start + 10)
    rounds = 0
    outcome = 'readiness_timeout'
    while clock() < ready_end:
        raw = query([NM, '--terse', '--escape', 'no', '--fields',
                     'GENERAL.DEVICE,GENERAL.TYPE,GENERAL.STATE,GENERAL.DBUS-PATH', 'device', 'show'])
        available = devices(raw or '')
        if available:
            break
        pause(min(.25, max(0, ready_end-clock())))
    else:
        available = []
    if available:
        before = {path: completed_scan(query, path) for _, path in available}
        if any(value is None for value in before.values()):
            outcome = 'scan_state_unavailable'
        else:
            outcome = 'scan_timeout'
            pending = dict(before)
            next_request = clock()
            while pending and clock() < end:
                if rounds < 2 and clock() >= next_request:
                    rounds += 1
                    for name, path in available:
                        if path in pending:
                            # Request acceptance does not mean scan completion. An
                            # automatic scan already running may reject this request.
                            request([NM, '--wait', '2', 'device', 'wifi', 'rescan', 'ifname', name])
                    next_request = clock() + 5
                for path, old in list(pending.items()):
                    current = completed_scan(query, path)
                    if current is not None and current >= 0 and current > old:
                        del pending[path]
                if not pending:
                    outcome = 'complete'
                    break
                pause(min(.25, max(0, end-clock())))
    return {'schema_version': 1, 'result': outcome, 'request_rounds': rounds,
            'ready_interfaces': len(available), 'elapsed_ms': int((clock()-start)*1000)}
