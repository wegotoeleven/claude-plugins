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
copies one or more sessions' transcripts (and their associated file
directories, if any) from wherever they currently live into the **current**
project directory.

Copies, never moves: sources are left untouched, so this is safe to re-run
and can't destroy an original transcript.

**A session being migrated must not be the live session running this
skill.** The transcript file is written continuously while a session is
open, so copying it mid-session captures a snapshot and misses everything
written after the copy — including, ironically, the copy command itself.
If the user selects the session currently running this skill, drop it from
the batch and tell them to migrate it separately after ending this session
(exit or close the terminal/tab), running this skill again from another
session afterward.

## Steps

1. List every session on the machine using the script shared with
   `delete-session`:
   ```
   python3 "${CLAUDE_SKILL_DIR}/../../scripts/list_sessions.py" --all
   ```
   The output is JSON: an array of session objects with `session_id`,
   `display` (name), `created`, `last_edited`, `folder_size` (total size of
   the sessions in that project's folder), `folder` (the project's
   working-directory path), `project_dir` (the actual
   `~/.claude/projects/<slug>` path on disk), and `is_current_folder`
   (true when the session already belongs to the directory this skill is
   running from). Sessions are sorted by `created` ascending (oldest
   first).

2. Present the sessions to the user as a single numbered table, oldest
   first, with columns `#`, `Created`, `Last Edited`, `Name`, `Location`,
   `Folder Size`. For `Location`, use "current folder" (or similar wording)
   when `is_current_folder` is true, otherwise show the `folder` path. Keep
   `session_id` and `project_dir` out of the printed table but keep them
   mapped to each row number internally, since you need both to run the
   migration script.

3. Ask the user which sessions to migrate in plain text, e.g. "Which
   sessions should I migrate here? Give me the row numbers,
   comma-separated." Do NOT use AskUserQuestion for this: with more than a
   handful of sessions the list will exceed AskUserQuestion's 4-option
   limit. Accept multiple row numbers.

4. Validate the selection before doing anything:
   - Drop any row already marked `is_current_folder: true` and tell the
     user it's already here, nothing to do.
   - If any selected row's `session_id` matches the session currently
     running this skill, drop it from the batch and warn the user per the
     note above.
   - If nothing is left to migrate after these checks, stop here.

5. For each remaining selected session, run a dry run to preview what
   would be copied, passing that row's `project_dir` as the source:
   ```
   python3 "${CLAUDE_SKILL_DIR}/scripts/migrate_session.py" "<session_id>" --old-project-dir "<project_dir>" --dry-run
   ```
   `--new-project-path` defaults to the current working directory; only
   pass it explicitly if the user wants to migrate somewhere other than
   where this skill is running. Show the user the source and destination
   paths and the transcript size for each. If any `dest_exists` is `true`,
   flag it clearly — the copy will overwrite a same-named file already at
   the destination.

6. Confirm with AskUserQuestion: "This will copy N session(s) into the
   current project directory. Proceed?"

7. Run the actual copy for each confirmed session:
   ```
   python3 "${CLAUDE_SKILL_DIR}/scripts/migrate_session.py" "<session_id>" --old-project-dir "<project_dir>"
   ```

8. Report what was copied, per session, and that every original is
   untouched at its original path. Tell the user how to pick them up:
   `/resume` from this directory, then select the session. If they want an
   old copy removed afterward, point them at the `delete-session` skill
   rather than deleting it here — that keeps destructive deletion in one
   place with its own confirmation flow.
