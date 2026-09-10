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

2. List sessions, using the shared script (also used by `migrate-session`):
   - This folder:
     ```
     python3 "${CLAUDE_SKILL_DIR}/../../scripts/list_sessions.py"
     ```
   - All sessions:
     ```
     python3 "${CLAUDE_SKILL_DIR}/../../scripts/list_sessions.py" --all
     ```
   The output is JSON: an array of session objects with `session_id`, `display` (name), `created`, `last_edited`, `folder_size` (total size of the sessions in that project's folder), `folder` (the project's working-directory path), `project_dir` (the actual `~/.claude/projects/<slug>` path on disk, needed for deletion), and `is_current_folder`. Sessions are sorted by `created` ascending (oldest first).

3. Present the sessions to the user as a single numbered table, oldest first:
   - This folder: columns `#`, `Created`, `Last Edited`, `Name`, `Folder Size`.
   - All sessions: same columns plus `Folder` (use the `folder` field, i.e. the real project path, not `project_dir`).
   Keep `session_id` and `project_dir` out of the printed table but keep them mapped to each row number internally, since you need both to run the deletion scripts.

4. Ask the user which sessions to delete in plain text, e.g. "Which sessions should I delete? Give me the row numbers, comma-separated." Do NOT use AskUserQuestion for this: with more than a handful of sessions the list will exceed AskUserQuestion's 4-option limit. Accept multiple row numbers.

5. For each selected session, run a dry run to show what would be deleted, passing the `project_dir` recorded for that row:
   ```
   python3 "${CLAUDE_SKILL_DIR}/scripts/delete_session.py" "<session_id>" --project-dir "<project_dir>" --dry-run
   ```
   Collect the `targets` list from each (only entries where `exists` is true) and the `history_entries` count. Present the combined list to the user, grouped by session so it's clear what belongs to what.

6. Ask the user to confirm using AskUserQuestion: "These are the files that will be deleted across N session(s). Proceed? This cannot be undone."

7. If confirmed, run the actual deletion for each selected session:
   ```
   python3 "${CLAUDE_SKILL_DIR}/scripts/delete_session.py" "<session_id>" --project-dir "<project_dir>"
   ```

8. Report what was deleted, per session. If there were errors, report those too.
