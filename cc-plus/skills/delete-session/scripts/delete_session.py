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


def find_other_copies(session_id, exclude_project_dir, projects_root):
    """Return other ~/.claude/projects/<slug> dirs that also have this session id.

    migrate-session copies a transcript into a new project dir without touching
    the original, so the same session id can legitimately live under several
    project dirs at once. Sidecar data (file-history, session-env, tasks) is
    keyed only by session id, not by project dir, so it's shared across every
    copy - deleting it because one copy is being removed would break the rest.
    """
    if not projects_root.exists():
        return []
    others = []
    for candidate in projects_root.iterdir():
        if not candidate.is_dir() or candidate == exclude_project_dir:
            continue
        if (candidate / f'{session_id}.jsonl').exists():
            others.append(str(candidate))
    return others


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
    projects_root = claude_home / 'projects'

    other_copies = find_other_copies(args.session_id, project_dir, projects_root)

    targets = [
        {'path': str(jsonl_file), 'type': 'file', 'exists': jsonl_file.exists()},
        {'path': str(session_dir), 'type': 'directory', 'exists': session_dir.exists()},
    ]

    # Sidecar data Claude Code keys by session id outside the project's own
    # ~/.claude/projects/<slug> directory, so it isn't reachable by session_dir above.
    # Skip it entirely if another project dir still has a copy of this session -
    # see find_other_copies for why.
    for sidecar_root in ('file-history', 'session-env', 'tasks'):
        sidecar_path = claude_home / sidecar_root / args.session_id
        target = {
            'path': str(sidecar_path),
            'type': 'directory' if sidecar_path.is_dir() else 'file',
            'exists': sidecar_path.exists(),
        }
        if other_copies:
            target['skipped_reason'] = (
                f'session id also present under: {", ".join(other_copies)}'
            )
        targets.append(target)

    history_entries = count_history_entries(jsonl_file) if jsonl_file.exists() else 0

    if args.dry_run:
        print(json.dumps({
            'dry_run': True,
            'session_id': args.session_id,
            'other_copies': other_copies,
            'targets': targets,
            'history_entries': history_entries,
        }, indent=2))
        return

    deleted = []
    skipped = []
    errors = []

    for target in targets:
        if not target['exists']:
            continue
        if target.get('skipped_reason'):
            skipped.append({'path': target['path'], 'reason': target['skipped_reason']})
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
        'skipped': skipped,
        'errors': errors,
    }, indent=2))


if __name__ == '__main__':
    main()
