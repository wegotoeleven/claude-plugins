# claude-plugins — Agent Instructions

See README.md for what this project is and why it exists.

## Setup Commands

Nothing to install and no build step: the plugins are Markdown and JSON, and the Python helpers run on `python3` using only the standard library (no version is pinned). To work on a plugin, start Claude Code from the repository root:

```bash
claude
```

Then register this checkout as a marketplace and install the plugin being changed (example: `cc-plus`):

```text
/plugin marketplace add .
/plugin install cc-plus@wegotoeleven-claude-plugins
/reload-plugins
```

## Dev Environment Tips

Each top-level directory (`cc-plus`, `repo-kit`, `blog-kit`) is a plugin containing:

- `.claude-plugin/plugin.json` — `name`, `version`, `description`, `author`, `keywords`.
- `skills/<skill-name>/SKILL.md` — one directory per skill: YAML frontmatter followed by the skill's instructions. Some skills also ship a `scripts/` directory (e.g. `cc-plus/skills/delete-session/scripts/`).

`cc-plus/scripts/list_sessions.py` is shared by all three session-management skills (`list-sessions`, `delete-session`, `migrate-session`). Keep shared helpers inside their owning plugin so they stay available once installed.

## Code Style

No linter or formatter configuration is present. Follow the existing Markdown, JSON, and Python style.

- Bump the owning plugin's `version` in its `.claude-plugin/plugin.json` whenever a skill is added or its behavior changes: minor for a new skill or a new/changed capability within an existing skill, patch for a smaller behavior tweak or clarification. Every skill-adding commit in this repo's history pairs with a version bump (e.g. `fb13c48` added `migrate-session` and bumped `cc-plus` 1.0.0 → 1.1.0).
- Adding a skill to an *existing* plugin needs no marketplace change — skills are auto-discovered from the plugin's `skills/` directory. Adding a brand-new *plugin* requires a new entry in `.claude-plugin/marketplace.json` at the repo root.
- `SKILL.md` frontmatter conventions: `name` matches the skill's directory name; `description` states what the skill does plus the phrases that should trigger it; `user-invocable: true` marks skills meant to be run directly as `/plugin:skill`; `argument-hint` documents expected CLI-style args; `allowed-tools` scopes which tools a skill's steps may call (see `cc-plus/skills/delete-session/SKILL.md` for an example restricting `Bash` to specific scripts).

## Testing Instructions

No automated tests or CI. Reload after edits and invoke the changed skill to confirm its documented behavior before considering a skill change complete. For example, after changing `hol-up`, give Claude a prompt to answer, then run:

```text
/reload-plugins
/cc-plus:hol-up
```

Preview session-script changes with each script's `--dry-run` flag before any real deletion or migration. Check all three callers when changing `list_sessions.py`. Report any interactive check that could not be run.

## PR Instructions

No `CONTRIBUTING.md` or enforced commit format. Recent commits use short summaries (e.g. "Added migrate-session skill", "Increment version"). Preserve the plugin version and marketplace conventions above.

## Security Considerations

- Keep `.env` files out of commits; `.gitignore` excludes them.
- Session scripts operate on real data under `~/.claude/`. Preserve deletion previews and confirmation, including protection of shared sidecar data when another copy of a session exists.
- Migration preserves sources but can overwrite destination files. Preserve overwrite warnings and the exclusion of the live session running the skill.
- `blog-kit` writes to a separate blog repository (`github.com/wegotoeleven/blog`) and pushes to `main` to deploy. Preserve its clean-working-tree check and approval before committing and pushing.
