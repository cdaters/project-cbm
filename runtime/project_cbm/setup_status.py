"""Read only the public, bounded first-boot progress projection."""
import json
import sys
from .setup import STATUS, initial, read_state
from .config_backend import trusted
from .data import read_json


def main():
    try:
        class Reader:
            def setup_read(self):
                if not STATUS.exists(): return initial()
                return read_json(trusted(STATUS))
        state = read_state(Reader())
        if len(sys.argv) == 1:
            print(json.dumps(state, sort_keys=True)); return 0
        if len(sys.argv) == 2 and sys.argv[1] in ('region','owner','network','complete'):
            done = state['complete'] if sys.argv[1] == 'complete' else sys.argv[1] in state['completed']
            return 0 if done else 1
        return 2
    except (OSError, ValueError, TypeError):
        print('First-boot progress is unavailable; use diagnostics before retrying.', file=sys.stderr)
        return 2
