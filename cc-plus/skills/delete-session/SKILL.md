---
name: delete-session
description: Selectively delete Claude Code session history files from disk. Use when the user asks to "delete a session", "delete a conversation", "clean up sessions", "remove old conversations", "remove a session", or wants to selectively remove Claude Code session histories, for the current project or across every project.
user-invocable: true
allowed-tools:
  - Bash(python3 *list_sessions.py*)
  - Bash(python3 *delete_session.py*)
  - AskUserQuestion
---

# Delete Session

## Steps

1. Ask the user which scope to work in, using AskUserQuestion:
   - "This folder" — sessions belonging to the current project only.
   - "All sessions" — every session across every project on this machine.

2. List sessions as a ready-made Markdown table, using the shared script (also used by `list-sessions` and `migrate-session`):
   - This folder:
     ```
     python3 "${CLAUDE_SKILL_DIR}/../../scripts/list_sessions.py" --table
     ```
   - All sessions:
     ```
     python3 "${CLAUDE_SKILL_DIR}/../../scripts/list_sessions.py" --all --table
     ```
   If it prints `No sessions found.`, tell the user and stop.

3. Print the script's output exactly as-is, so it matches `list-sessions`. Do not reformat, reorder, or re-number it. Each row's `session_id` is its `Transcript` file name without `.jsonl`, and its `project_dir` is the `Transcripts in:` path of the group it sits under; you need both to run the deletion script.

4. Ask the user which sessions to delete in plain text, e.g. "Which sessions should I delete? Give me the row numbers, comma-separated." Do NOT use AskUserQuestion for this: with more than a handful of sessions the list will exceed AskUserQuestion's 4-option limit. Accept multiple row numbers.

5. For each selected session, run a dry run to show what would be deleted, passing the `project_dir` recorded for that row:
   ```
   python3 "${CLAUDE_SKILL_DIR}/scripts/delete_session.py" "<session_id>" --project-dir "<project_dir>" --dry-run
   ```
   Collect the `targets` list from each (only entries where `exists` is true) and the `history_entries` count. `other_copies` lists any other project directories that also hold this same session id (from a prior `migrate-session` copy); when non-empty, the `file-history`/`session-env`/`tasks` sidecar targets carry a `skipped_reason` and will NOT be deleted, since that sidecar data is shared across every copy of the session id and removing it would break the copies you're keeping. Present the combined list to the user, grouped by session so it's clear what belongs to what, and call out any skipped sidecar data and why.

6. Ask the user to confirm using AskUserQuestion: "These are the files that will be deleted across N session(s). Proceed? This cannot be undone."

7. If confirmed, run the actual deletion for each selected session:
   ```
   python3 "${CLAUDE_SKILL_DIR}/scripts/delete_session.py" "<session_id>" --project-dir "<project_dir>"
   ```

8. Report what was deleted and what was skipped (with reasons), per session. If there were errors, report those too.
