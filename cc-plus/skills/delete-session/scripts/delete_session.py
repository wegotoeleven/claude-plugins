#!/usr/bin/env python3
"""Delete a Claude Code session and its associated files."""

import json
import os
import shutil
import sys
from pathlib import Path


def path_to_project_dir(project_path):
    return project_path.replace('/', '-')


def count_history_entries(jsonl_path):
    try:
        count = sum(1 for line in open(jsonl_path) if line.strip())
        return count
    except Exception:
        return 0


def main():
    if len(sys.argv) < 3:
        print(json.dumps({'error': 'Usage: delete_session.py <project_path> <session_id> [--dry-run]'}))
        sys.exit(1)

    project_path = sys.argv[1]
    session_id = sys.argv[2]
    dry_run = '--dry-run' in sys.argv

    project_dir = Path.home() / '.claude' / 'projects' / path_to_project_dir(project_path)
    jsonl_file = project_dir / f'{session_id}.jsonl'
    session_dir = project_dir / session_id

    targets = [
        {'path': str(jsonl_file), 'type': 'file', 'exists': jsonl_file.exists()},
        {'path': str(session_dir), 'type': 'directory', 'exists': session_dir.exists()},
    ]

    history_entries = count_history_entries(jsonl_file) if jsonl_file.exists() else 0

    if dry_run:
        print(json.dumps({
            'dry_run': True,
            'session_id': session_id,
            'targets': targets,
            'history_entries': history_entries,
        }, indent=2))
        return

    deleted = []
    errors = []

    for target in targets:
        if not target['exists']:
            continue
        try:
            if target['type'] == 'file':
                os.remove(target['path'])
            else:
                shutil.rmtree(target['path'])
            deleted.append(target['path'])
        except Exception as e:
            errors.append({'path': target['path'], 'error': str(e)})

    print(json.dumps({
        'session_id': session_id,
        'deleted': deleted,
        'errors': errors,
    }, indent=2))


if __name__ == '__main__':
    main()
