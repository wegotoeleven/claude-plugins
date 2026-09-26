---
name: list-sessions
description: List every Claude Code session on this machine, across all projects, with the full path to each session's transcript on disk. Use when the user asks to "list sessions", "show my sessions", "what sessions do I have", "where are my sessions stored", or wants to find a session's transcript file. Read-only.
user-invocable: true
allowed-tools:
  - Bash(python3 *list_sessions.py*)
---

# List Sessions

Read-only: this skill never modifies, copies, or deletes anything. Point the
user at `migrate-session` or `delete-session` if they want to act on what
they see.

## Steps

1. List every session on the machine, using the script shared with
   `delete-session` and `migrate-session`:
   ```
   python3 "${CLAUDE_SKILL_DIR}/../../scripts/list_sessions.py" --all
   ```
   The output is JSON: an array of session objects with `session_id`,
   `display` (name), `created`, `last_edited`, `folder_size` (total size of
   the sessions in that project's folder), `folder` (the project's
   working-directory path), `project_dir` (the actual
   `~/.claude/projects/<slug>` path on disk), `transcript_path` (the full
   path to the session's `.jsonl` transcript), and `is_current_folder`.
   Sessions are sorted by `created` ascending (oldest first).

2. If the array is empty, tell the user no sessions were found under
   `~/.claude/projects/` and stop.

3. Group the sessions by `project_dir`, ordering groups by their oldest
   session. For each group, print a short header:
   - The project's `folder` path, marked "(current folder)" when
     `is_current_folder` is true.
   - `Stored in:` followed by the full `project_dir` path.
   - The group's `folder_size` and session count.

   Under each header, print a table with columns `#`, `Created`,
   `Last Edited`, `Name`, `Transcript`, oldest first. `Transcript` is the
   full `transcript_path`, shown verbatim in backticks, never shortened
   with `~` or truncated. Number rows continuously across all groups.

4. End with a one-line total: number of sessions and number of projects.
