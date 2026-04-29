---
name: delete-session
description: Selectively delete Claude Code session history files from disk. Use when the user asks to "delete a session", "delete a conversation", "clean up sessions", "remove old conversations", "remove a session", or wants to selectively remove Claude Code session histories for the current project.
user-invocable: true
allowed-tools:
  - Bash(python3 *list_sessions.py*)
  - Bash(python3 *delete_session.py*)
  - AskUserQuestion
---

# Delete Session

## Steps

1. List sessions for the current project by running:
   ```
   python3 "${CLAUDE_SKILL_DIR}/scripts/list_sessions.py"
   ```
   The output is JSON: an array of objects with `session_id`, `display` (slug or first user message), `timestamp`, `last_active`, and `size_kb`. Sessions are sorted by `last_active` descending (most recently active first).

2. Present the sessions to the user as a numbered table with columns: #, Last Active, Display, Size. Use the `last_active` field for the date column and the `display` field as the session identifier.

3. Ask the user which session to delete in plain text — do NOT use AskUserQuestion here.

4. For the selected session, run a dry run to show what would be deleted:
   ```
   python3 "${CLAUDE_SKILL_DIR}/scripts/delete_session.py" "<session_id>" --dry-run
   ```
   Present the `targets` list to the user, showing only items where `exists` is true. Also show the `history_entries` count.

5. Ask the user to confirm using AskUserQuestion: "These are the files that will be deleted. Proceed? This cannot be undone."

6. Run the actual deletion:
   ```
   python3 "${CLAUDE_SKILL_DIR}/scripts/delete_session.py" "<session_id>"
   ```

7. Report what was deleted. If there were errors, report those too.
