#!/usr/bin/env python3
"""List Claude Code sessions, either for one project or across all projects."""

import argparse
import json
import os
import re
from pathlib import Path
from datetime import datetime


def path_to_project_dir(project_path):
    return re.sub(r'[^a-zA-Z0-9]', '-', project_path)


def human_size(num_bytes):
    size = float(num_bytes)
    for unit in ('B', 'KB', 'MB', 'GB'):
        if size < 1024 or unit == 'GB':
            return f'{size:.1f} {unit}'
        size /= 1024


def format_timestamp(ts):
    if not ts:
        return 'unknown'
    try:
        dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M')
    except Exception:
        return ts[:16]


def get_session_info(jsonl_path):
    custom_title = None
    slug = None
    cwd = None
    first_timestamp = None
    last_timestamp = None
    first_user_message = None

    try:
        with open(jsonl_path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                obj = json.loads(line)

                ts = obj.get('timestamp')
                if ts:
                    if first_timestamp is None:
                        first_timestamp = ts
                    last_timestamp = ts

                if not cwd and obj.get('cwd'):
                    cwd = obj['cwd']

                if obj.get('type') == 'custom-title' and obj.get('customTitle'):
                    custom_title = obj['customTitle']

                if not slug and obj.get('slug'):
                    slug = obj['slug']

                if (first_user_message is None
                        and obj.get('type') == 'user'
                        and not obj.get('toolUseResult')):
                    content = obj.get('message', {}).get('content', '')
                    if isinstance(content, str) and content.strip():
                        first_user_message = content.strip()[:100]
                    elif isinstance(content, list):
                        for block in content:
                            if (isinstance(block, dict)
                                    and block.get('type') == 'text'
                                    and block['text'].strip()):
                                first_user_message = block['text'].strip()[:100]
                                break
    except Exception:
        pass

    return {
        'custom_title': custom_title,
        'slug': slug,
        'cwd': cwd,
        'first_timestamp': first_timestamp,
        'last_timestamp': last_timestamp,
        'first_user_message': first_user_message,
    }


def scan_project_dir(project_dir):
    """Return (sessions, folder_size_bytes) for one ~/.claude/projects/<slug> dir."""
    jsonl_files = sorted(project_dir.glob('*.jsonl'))
    folder_size_bytes = sum(f.stat().st_size for f in jsonl_files)

    sessions = []
    for jsonl_file in jsonl_files:
        info = get_session_info(jsonl_file)
        sessions.append({
            'session_id': jsonl_file.stem,
            'display': info['custom_title'] or info['slug'] or info['first_user_message'] or jsonl_file.stem,
            'created': format_timestamp(info['first_timestamp']),
            'last_edited': format_timestamp(info['last_timestamp']),
            'created_raw': info['first_timestamp'] or '',
            'folder': info['cwd'] or str(project_dir),
            'project_dir': str(project_dir),
        })
    return sessions, folder_size_bytes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('project_path', nargs='?', default=os.getcwd())
    parser.add_argument('--all', action='store_true', help='scan every project directory')
    args = parser.parse_args()

    projects_root = Path.home() / '.claude' / 'projects'
    current_project_dir = str(projects_root / path_to_project_dir(os.getcwd()))

    if args.all:
        project_dirs = [d for d in projects_root.iterdir() if d.is_dir()] if projects_root.exists() else []
    else:
        candidate = projects_root / path_to_project_dir(args.project_path)
        project_dirs = [candidate] if candidate.exists() else []

    all_sessions = []
    for project_dir in project_dirs:
        sessions, folder_size_bytes = scan_project_dir(project_dir)
        if not sessions:
            continue
        folder_size = human_size(folder_size_bytes)
        for s in sessions:
            s['folder_size'] = folder_size
            s['is_current_folder'] = s['project_dir'] == current_project_dir
            all_sessions.append(s)

    all_sessions.sort(key=lambda s: s['created_raw'])
    for s in all_sessions:
        del s['created_raw']

    print(json.dumps(all_sessions, indent=2))


if __name__ == '__main__':
    main()
