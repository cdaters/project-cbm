"""Contract 1 for fixed appliance operations. No UI, shell, credentials in results."""
import re
from .data import loads

WIFI_UUID = '2b7787f5-f328-49a1-b5ab-53cf4726bd06'  # Managed connection ID, never a machine identity.

SERVICES = {'ssh': 'ssh.service', 'sharing': 'smbd.service', 'modem': 'tcpser.service', 'discovery': 'avahi-daemon.service'}
FIELDS = {'hostname': {'value'}, 'locale': {'value'}, 'timezone': {'value'}, 'keyboard': {'value'},
          'wifi-country': {'value'}, 'network': {'enabled'}, 'wifi-enroll': {'ssid', 'password'},
          'service': {'service', 'enabled'}, 'sharing-password': {'password'},
          'modem': {'port', 'baud'}, 'power': {'action'},
          'setup-region': {'locale','keyboard','timezone'}, 'setup-owner': {'password'},
          'setup-network': {'enabled'}, 'setup-finish': set(), 'wifi-rescan':set(), 'wifi-disconnect': set(), 'wifi-forget': set()}
for _op in ('wifi-country','wifi-rescan','wifi-enroll'):
    FIELDS['setup-'+_op]=FIELDS[_op]
RESULTS = {'saved_restart': 'Keyboard layout saved. It applies after reboot; current console input is unchanged.', 'credentials_required': 'Set a separate File Sharing password before enabling Samba.', 'ok': 'Setting applied.', 'invalid': 'The value is not supported. Check the setting and try again.',
           'pending': 'Complete local first-boot setup before changing this setting.',
           'unavailable': 'The required system facility is unavailable. Review System Information or Advanced guidance.',
           'failed': 'The operation could not be confirmed. Review current state before retrying; part of it may have applied.',
           'busy': 'Another configuration operation is running. Try again when it finishes.',
           'saved_pending': 'Settings saved; runtime integration is pending. The service was not enabled.'}


RESULTS.update(wifi_failed='Could not connect to Wi-Fi. Check the password, signal and router settings, then retry or choose another network. Authentication failure was not separately identified.',
               wifi_country_required='Set the Wi-Fi country where this Pi is used before connecting.')


def match(value, pattern):
    return isinstance(value, str) and len(value) <= 128 and re.fullmatch(pattern, value) is not None


def password(value, wifi=False):
    if not isinstance(value, str) or not value.isprintable(): return False
    if wifi: return 8 <= len(value) <= 63 and value.isascii()
    return 12 <= len(value) <= 128


def validate(request):
    if not isinstance(request, dict) or set(request) != {'schema_version','operation','values'} or type(request['schema_version']) is not int or request['schema_version'] != 1:
        raise ValueError('request')
    op=request['operation'];v=request['values']
    if not isinstance(op,str) or op not in FIELDS or not isinstance(v,dict) or set(v)!=FIELDS[op]:raise ValueError('operation')
    good=True
    if op=='hostname':good=match(v['value'],r'[a-z][a-z0-9-]{0,61}[a-z0-9]|[a-z]')
    elif op=='locale':good=match(v['value'],r'[a-z]{2,3}_[A-Z]{2}\.UTF-8')
    elif op=='timezone':good=match(v['value'],r'[A-Za-z_+-]+(?:/[A-Za-z0-9_+-]+){0,3}')
    elif op=='keyboard':good=match(v['value'],r'[a-z][a-z0-9_-]{0,31}')
    elif op=='wifi-country':good=match(v['value'],r'[A-Z]{2}')
    elif op in ('network','setup-network'):good=type(v['enabled']) is bool
    elif op=='wifi-enroll':good=isinstance(v['ssid'],str) and v['ssid'].isprintable() and 1<=len(v['ssid'].encode('utf-8'))<=32 and re.fullmatch(r'(?:[0-9]+;)+',v['ssid']) is None and password(v['password'],True)
    elif op in ('sharing-password','setup-owner'):good=password(v['password']) and ':' not in v['password']
    elif op=='service':good=isinstance(v['service'],str) and v['service'] in SERVICES and type(v['enabled']) is bool
    elif op=='modem':good=type(v['port']) is int and 1024<=v['port']<=65535 and type(v['baud']) is int and v['baud'] in (300,1200,2400,9600,19200,38400)
    elif op=='power':good=v['action'] in ('poweroff','reboot')
    if op=='setup-region':
        for setting in ('locale','keyboard','timezone'):
            validate({'schema_version':1,'operation':setting,'values':{'value':v[setting]}})
    if not good:raise ValueError('value')
    if op in ('setup-wifi-country','setup-wifi-rescan','setup-wifi-enroll'):
        validate({'schema_version':1,'operation':op.removeprefix('setup-'),'values':v})
    return request


def decode(raw):
    if len(raw)>4096:raise ValueError('request_size')
    return validate(loads(raw))


def result(code):
    return {'format':'project-cbm.config-result','schema_version':1,'status':code,'message':RESULTS[code]}


def keyfile(ssid, secret):
    """One CBM-owned WPA personal connection. No secrets in argv or logs."""
    def escape(s):return s.replace('\\','\\\\').replace(' ','\\s')
    return ('[connection]\nid=Project CBM Wi-Fi\nuuid='+WIFI_UUID+'\ntype=wifi\nautoconnect=true\n'
            '[wifi]\nmode=infrastructure\nssid='+escape(ssid)+'\n'
            '[wifi-security]\nkey-mgmt=wpa-psk\npsk='+escape(secret)+'\n'
            '[ipv4]\nmethod=auto\n[ipv6]\nmethod=auto\n')
