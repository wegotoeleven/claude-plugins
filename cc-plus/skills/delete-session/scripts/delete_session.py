#!/usr/bin/env python3
"""Delete a Claude Code session and its associated files."""

import argparse
import json
import os
import re
import shutil
from pathlib import Path


def path_to_project_dir(project_path):
    return re.sub(r'[^a-zA-Z0-9]', '-', project_path)


def count_history_entries(jsonl_path):
    try:
        return sum(1 for line in open(jsonl_path) if line.strip())
    except Exception:
        return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('session_id')
    parser.add_argument('--project-dir', help='absolute path to the ~/.claude/projects/<slug> directory')
    parser.add_argument('--project-path', help='project working directory to derive the slug from (default: cwd)')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    if args.project_dir:
        project_dir = Path(args.project_dir)
    else:
        project_path = args.project_path or os.getcwd()
        project_dir = Path.home() / '.claude' / 'projects' / path_to_project_dir(project_path)

    jsonl_file = project_dir / f'{args.session_id}.jsonl'
    session_dir = project_dir / args.session_id
    claude_home = Path.home() / '.claude'

    targets = [
        {'path': str(jsonl_file), 'type': 'file', 'exists': jsonl_file.exists()},
        {'path': str(session_dir), 'type': 'directory', 'exists': session_dir.exists()},
    ]

    # Sidecar data Claude Code keys by session id outside the project's own
    # ~/.claude/projects/<slug> directory, so it isn't reachable by session_dir above.
    for sidecar_root in ('file-history', 'session-env', 'tasks'):
        sidecar_path = claude_home / sidecar_root / args.session_id
        targets.append({
            'path': str(sidecar_path),
            'type': 'directory' if sidecar_path.is_dir() else 'file',
            'exists': sidecar_path.exists(),
        })

    history_entries = count_history_entries(jsonl_file) if jsonl_file.exists() else 0

    if args.dry_run:
        print(json.dumps({
            'dry_run': True,
            'session_id': args.session_id,
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
        'session_id': args.session_id,
        'deleted': deleted,
        'errors': errors,
    }, indent=2))


if __name__ == '__main__':
    main()
