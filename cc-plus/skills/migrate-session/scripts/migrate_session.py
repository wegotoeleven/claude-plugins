#!/usr/bin/env python3
"""Copy a Claude Code session's history into a different project's directory
so it shows up in /resume from the new location.

Copies rather than moves: the source transcript is left untouched, so this
is safe to re-run and the migration can't destroy the original.
"""

import json
import re
import shutil
import sys
from pathlib import Path


def path_to_project_dir(project_path):
    return re.sub(r'[^a-zA-Z0-9]', '-', project_path)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    flags = [a for a in sys.argv[1:] if a.startswith('--')]

    if len(args) != 3:
        print(json.dumps({
            'error': 'Usage: migrate_session.py <old_project_path> <new_project_path> <session_id> [--dry-run]',
        }))
        sys.exit(1)

    old_project_path, new_project_path, session_id = args
    dry_run = '--dry-run' in flags

    old_dir = Path.home() / '.claude' / 'projects' / path_to_project_dir(old_project_path)
    new_dir = Path.home() / '.claude' / 'projects' / path_to_project_dir(new_project_path)

    old_jsonl = old_dir / f'{session_id}.jsonl'
    old_session_dir = old_dir / session_id
    new_jsonl = new_dir / f'{session_id}.jsonl'
    new_session_dir = new_dir / session_id

    if not old_jsonl.exists():
        print(json.dumps({'error': f'Source transcript not found: {old_jsonl}'}))
        sys.exit(1)

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

    if dry_run:
        print(json.dumps({
            'dry_run': True,
            'session_id': session_id,
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
        'session_id': session_id,
        'copied': copied,
        'errors': errors,
        'source_untouched': str(old_jsonl),
        'resume_with': f'cd {new_project_path} && claude',
    }, indent=2))


if __name__ == '__main__':
    main()
