"""Fresh-image quiet console settings; no video/session ownership changes."""
OPTIONS = ('quiet', 'loglevel=4', 'logo.nologo', 'systemd.show_status=auto')


def cmdline(raw):
    # The partition identity, console, rootwait and filesystem options are retained.
    names = {option.split('=')[0] for option in OPTIONS}
    words = [word for word in raw.split() if word != 'resize' and word.split('=')[0] not in names]
    if not any(word.startswith('root=') for word in words):
        raise ValueError('missing root device')
    return ' '.join([*words, *OPTIONS])+'\n'


def firmware(raw):
    # [all] prevents the option accidentally inheriting an upstream model filter.
    marker = '# Project CBM boot presentation'
    if marker in raw:
        raise ValueError('presentation already installed')
    return raw.rstrip()+'\n\n[all]\n'+marker+'\ndisable_splash=1\n'


ISSUE = '\n  PROJECT CBM\n  Your Commodore computer is starting.\n\n'
