#!/usr/bin/env python3
"""List Claude Code sessions for a given project path."""

import json
import os
import sys
from pathlib import Path
from datetime import datetime, timezone


def path_to_project_dir(project_path):
    return project_path.replace('/', '-')


def get_session_info(jsonl_path):
    custom_title = None
    slug = None
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

    return custom_title, slug, first_timestamp, last_timestamp, first_user_message


def format_timestamp(ts):
    if not ts:
        return 'unknown'
    try:
        dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M')
    except Exception:
        return ts[:16]


def main():
    project_path = sys.argv[1] if len(sys.argv) >= 2 else os.getcwd()
    project_dir = Path.home() / '.claude' / 'projects' / path_to_project_dir(project_path)

    if not project_dir.exists():
        print(json.dumps([]))
        return

    sessions = []
    for jsonl_file in project_dir.glob('*.jsonl'):
        session_id = jsonl_file.stem
        size_kb = round(jsonl_file.stat().st_size / 1024, 1)
        custom_title, slug, first_ts, last_ts, first_msg = get_session_info(jsonl_file)

        sessions.append({
            'session_id': session_id,
            'display': custom_title or slug or first_msg or session_id,
            'timestamp': first_ts,
            'last_active': last_ts,
            'size_kb': size_kb,
        })

    sessions.sort(key=lambda s: s['last_active'] or '', reverse=True)
    print(json.dumps(sessions, indent=2))


if __name__ == '__main__':
    main()
