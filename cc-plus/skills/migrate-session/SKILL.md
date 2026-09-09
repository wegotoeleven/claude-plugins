---
name: migrate-session
description: Copy a Claude Code session's history into a different project directory so it shows up in /resume from the new location. Use when the user asks to "migrate a session", "move a session", "move a conversation to a new folder", says a session isn't showing in /resume after moving/renaming a project directory, or wants to carry session history across a folder move.
user-invocable: true
allowed-tools:
  - Bash(python3 *list_sessions.py*)
  - Bash(python3 *migrate_session.py*)
  - AskUserQuestion
---

# Migrate Session

Claude Code keys session history off the *filesystem path* a session was
started in (`~/.claude/projects/<mangled-path>/`), not off the repository
itself. Moving, renaming, or relocating a project directory (e.g. onto a
different volume) leaves old sessions invisible to `/resume` from the new
path, even though the transcripts still exist under the old one. This skill
copies a session's transcript (and its associated file directory, if any)
from the old project path's directory into the new one's.

Copies, never moves: the source is left untouched, so this is safe to
re-run and can't destroy the original transcript.

**The session being migrated must not be the live session running this
skill.** The transcript file is written continuously while a session is
open, so copying it mid-session captures a snapshot and misses everything
written after the copy — including, ironically, the copy command itself.
If the session the user wants to migrate is the one currently running,
tell them to end it (exit or close the terminal/tab) and run this skill
again from a different session afterward, rather than copying now.

## Steps

1. Determine the **old project path** — the directory the session was
   originally started in. Ask the user for it in plain text if it isn't
   already clear from the conversation.

2. List sessions for that path by running:
   ```
   python3 "${CLAUDE_SKILL_DIR}/scripts/list_sessions.py" "<old_project_path>"
   ```
   The output is JSON: an array of objects with `session_id`, `display`
   (slug or first user message), `timestamp`, `last_active`, and
   `size_kb`, sorted by `last_active` descending.

3. Present the sessions as a numbered table with columns: #, Last Active,
   Display, Size. Ask the user which session to migrate in plain text — do
   NOT use AskUserQuestion here, since the option set is dynamic. If the
   selected session's ID matches the session currently running this skill,
   stop and tell the user to end this session first and re-run the skill
   from another one — see the warning above.

4. Determine the **new project path** — the directory the user now works
   from (and will run `claude` from). Default to the current working
   directory if the skill is being run from there, but confirm it with the
   user rather than assuming, since a wrong path just makes the session
   invisible under a different name.

5. Run a dry run to preview what would be copied:
   ```
   python3 "${CLAUDE_SKILL_DIR}/scripts/migrate_session.py" "<old_project_path>" "<new_project_path>" "<session_id>" --dry-run
   ```
   Show the user the source and destination paths and the transcript size.
   If any `dest_exists` is `true`, flag it clearly — the copy will
   overwrite a same-named file already at the destination.

6. Confirm with AskUserQuestion: "This will copy the session to the new
   project directory. Proceed?"

7. Run the actual copy:
   ```
   python3 "${CLAUDE_SKILL_DIR}/scripts/migrate_session.py" "<old_project_path>" "<new_project_path>" "<session_id>"
   ```

8. Report what was copied and that the original is untouched at its
   original path. Tell the user how to pick it up:
   ```
   cd <new_project_path> && claude
   ```
   then `/resume` and select the session. If they want the old copy
   removed afterward, point them at the `delete-session` skill rather than
   deleting it here — that keeps destructive deletion in one place with
   its own confirmation flow.
