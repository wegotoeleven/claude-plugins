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

1. List every session on the machine as a ready-made Markdown table, using
   the script shared with `delete-session` and `migrate-session`:
   ```
   python3 "${CLAUDE_SKILL_DIR}/../../scripts/list_sessions.py" --all --table
   ```
   The script groups sessions by project, marks the current folder, shows
   each group's full transcript directory, and numbers rows continuously
   across groups. Formatting lives in the script so all three session skills
   display identical output.

2. Print the script's output exactly as-is. Do not reformat, reorder,
   re-number, or summarise it. If it prints `No sessions found.`, tell the
   user no sessions were found under `~/.claude/projects/` and stop.
