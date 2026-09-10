#!/usr/bin/env python3
"""Copy a Claude Code session's history into a different project's directory
so it shows up in /resume from the new location.

Copies rather than moves: the source transcript is left untouched, so this
is safe to re-run and the migration can't destroy the original.
"""

import argparse
import json
import os
import re
import shutil
from pathlib import Path


def path_to_project_dir(project_path):
    return re.sub(r'[^a-zA-Z0-9]', '-', project_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('session_id')
    parser.add_argument('--old-project-dir', required=True,
                         help='absolute path to the source ~/.claude/projects/<slug> directory, '
                              'as reported by list_sessions.py\'s "project_dir" field')
    parser.add_argument('--new-project-path', default=os.getcwd(),
                         help='working directory to migrate into (default: cwd)')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    old_dir = Path(args.old_project_dir)
    new_dir = Path.home() / '.claude' / 'projects' / path_to_project_dir(args.new_project_path)

    old_jsonl = old_dir / f'{args.session_id}.jsonl'
    old_session_dir = old_dir / args.session_id
    new_jsonl = new_dir / f'{args.session_id}.jsonl'
    new_session_dir = new_dir / args.session_id

    if not old_jsonl.exists():
        print(json.dumps({'error': f'Source transcript not found: {old_jsonl}'}))
        raise SystemExit(1)

    targets = [
        {
            'source': str(old_jsonl),
            'dest': str(new_jsonl),
            'type': 'file',
            'dest_exists': new_jsonl.exists(),
            'size_kb': round(old_jsonl.stat().st_size / 1024, 1),
        },
        {
            'source': str(old_session_dir),
            'dest': str(new_session_dir),
            'type': 'directory',
            'source_exists': old_session_dir.exists(),
            'dest_exists': new_session_dir.exists(),
        },
    ]

    if args.dry_run:
        print(json.dumps({
            'dry_run': True,
            'session_id': args.session_id,
            'targets': targets,
        }, indent=2))
        return

    new_dir.mkdir(parents=True, exist_ok=True)

    copied = []
    errors = []

    try:
        shutil.copy2(old_jsonl, new_jsonl)
        copied.append(str(new_jsonl))
    except Exception as e:
        errors.append({'path': str(new_jsonl), 'error': str(e)})

    if old_session_dir.exists():
        try:
            shutil.copytree(old_session_dir, new_session_dir, dirs_exist_ok=True)
            copied.append(str(new_session_dir))
        except Exception as e:
            errors.append({'path': str(new_session_dir), 'error': str(e)})

    print(json.dumps({
        'session_id': args.session_id,
        'copied': copied,
        'errors': errors,
        'source_untouched': str(old_jsonl),
        'resume_with': f'cd {args.new_project_path} && claude',
    }, indent=2))


if __name__ == '__main__':
    main()
