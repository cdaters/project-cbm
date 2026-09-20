"""Registry and effective default interface for unprivileged Menu/launcher consumers."""
import argparse
import json
import sys
from .data import registry
from . import preferences, library
from .applications import application_profile


def main(argv=None):
    parser = argparse.ArgumentParser(description='Validated Project CBM machine profiles')
    sub = parser.add_subparsers(dest='action', required=True)
    sub.add_parser('list')  # JSON contract 1; canonical validated registry projection.
    sub.add_parser('menu')  # Bounded tab-separated contract 1 for Bash, not pretty output.
    default = sub.add_parser('default'); default.add_argument('--id-only', action='store_true')
    sub.add_parser('initialize')
    sub.add_parser('content-families')
    content = sub.add_parser('content-profile'); content.add_argument('media')
    resolve = sub.add_parser('resolve'); resolve.add_argument('profile')
    output = resolve.add_mutually_exclusive_group()
    output.add_argument('--launch-fields', action='store_true')
    output.add_argument('--cover', action='store_true')
    args = parser.parse_args(argv)
    try:
        profiles = registry()
        if args.action == 'content-families':
            for name, (label, _) in library.FAMILIES.items():
                print(name+'\t'+label)
            return 0
        if args.action == 'content-profile':
            selected = application_profile(args.media, profiles)
            if selected is None:
                selected = library.content_profile(args.media, profiles, preferences.selection(profiles=profiles)['id'])
            print(selected)
            return 0
        if args.action == 'list':
            result = {'schema_version': 1, 'profiles': profiles}
        elif args.action == 'resolve':
            result = next((p for p in profiles if p['id'] == args.profile), None)
            if result is None:
                raise ValueError('unknown_profile')
            if args.cover:
                print(result['cover_asset'])
                return 0
            if args.launch_fields:
                print('\n'.join([result['executable'], *result['launch_options']]))
                return 0
        else:
            state = preferences.initialize(profiles=profiles) if args.action == 'initialize' else preferences.selection(profiles=profiles)
            if args.action == 'default':
                print(state['id'] if args.id_only else '\t'.join(state[k] for k in ('id', 'name', 'preference_status')))
                return 0
            if args.action == 'menu':
                print('\t'.join(['state', state['id'], state['name'], state['preference_status']]))
                for p in profiles:
                    print('\t'.join(['profile', p['id'], p['name'], p['description']]))
                return 0
            result = state
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (ValueError, TypeError, OSError, StopIteration):
        print('Machine selection unavailable. Check the Project CBM runtime and user preference permissions.', file=sys.stderr)
        return 2
