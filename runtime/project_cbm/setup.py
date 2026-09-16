"""Local first-boot state machine. Called only by the serialized root backend.

The image contains a locked, ordinary sudo-capable owner account. No password is
stored here: chpasswd consumes it through stdin and PAM owns the credential store.
"""
import json
from pathlib import Path
import re
from .configuration import result

STATE = Path('/var/lib/project-cbm/setup/state.json')
STATUS = Path('/var/lib/project-cbm/setup/status.json')
STEPS = ('region', 'owner', 'network')


def initial():
    return {'schema_version': 1, 'completed': [], 'complete': False}


def read_state(system):
    state = system.setup_read()
    if (not isinstance(state, dict) or set(state) != {'schema_version', 'completed', 'complete'}
            or type(state['schema_version']) is not int or state['schema_version'] != 1
            or type(state['complete']) is not bool or not isinstance(state['completed'], list)
            or any(x not in STEPS for x in state['completed'])
            or len(set(state['completed'])) != len(state['completed'])
            or (state['complete'] and set(state['completed']) != set(STEPS))):
        raise ValueError('setup_state')
    return state


def apply(request, policy, system, configure):
    state = read_state(system)
    op, values = request['operation'], request['values']
    # Finished setup is not a password-reset API. Owner administration owns later
    # password changes. A crash after the final marker can safely republish readiness.
    if state['complete']:
        if op == 'setup-finish':
            if not system.owner_ready(policy['owner_user']): return result('failed')
            system.setup_activate(policy)
            return result('ok')
        return result('invalid')
    step = op.removeprefix('setup-')
    if step in state['completed']: return result('ok')
    required={'owner':{'region'},'network':{'region','owner'}}.get(step,set())
    if not required<=set(state['completed']):return result('invalid')
    if op == 'setup-region':
        for setting in ('locale', 'keyboard', 'timezone'):
            answer = configure({'schema_version': 1, 'operation': setting,
                                'values': {'value': values[setting]}},
                               {**policy, 'system_ready': True}, system)
            if answer['status'] not in ('ok', 'saved_restart'): return answer
    elif op == 'setup-owner':
        if not system.owner_expected(policy['owner_user']): return result('failed')
        if not system.run(['/usr/sbin/chpasswd'], stdin=policy['owner_user'] + ':' + values['password'] + '\n'):
            return result('failed')
        if not system.owner_ready(policy['owner_user']): return result('failed')
    elif op == 'setup-network':
        # Enrolment is optional and separate. Offline is a fully completed choice.
        answer = configure({'schema_version': 1, 'operation': 'network',
                            'values': {'enabled': values['enabled']}},
                           {**policy, 'system_ready': True}, system)
        if answer['status'] != 'ok': return answer
    elif op == 'setup-finish':
        if set(state['completed']) != set(STEPS): return result('invalid')
        if not system.setup_prerequisites() or not system.owner_ready(policy['owner_user']):
            return result('failed')
        state['complete'] = True
        system.setup_save(state)
        system.setup_activate(policy)
        return result('ok')
    else:
        return result('invalid')
    state['completed'].append(step)
    system.setup_save(state)
    return result('ok')
