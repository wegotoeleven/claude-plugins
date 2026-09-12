# claude-plugins — Agent Instructions

See README.md for what this project is and why it exists.

## Repository Structure

Each top-level directory (`cc-plus`, `repo-kit`, `blog-kit`) is a plugin containing:

- `.claude-plugin/plugin.json` — `name`, `version`, `description`, `author`, `keywords`.
- `skills/<skill-name>/SKILL.md` — one subdirectory per skill, with YAML frontmatter (`name`, `description`, and optionally `user-invocable`, `argument-hint`, `allowed-tools`) followed by the skill's instructions. Some skills also ship a `scripts/` subdirectory (e.g. `cc-plus/skills/delete-session/scripts/`).

There is no build step, package manager, or compiled output — the repo is plain Markdown and JSON, loaded directly by Claude Code.

## Conventions

- Bump the owning plugin's `version` in its `.claude-plugin/plugin.json` whenever a skill is added or its behavior changes: minor for a new skill or a new/changed capability within an existing skill, patch for a smaller behavior tweak or clarification. Every skill-adding commit in this repo's history pairs with a version bump (e.g. `fb13c48` added `migrate-session` and bumped `cc-plus` 1.0.0 → 1.1.0).
- Adding a skill to an *existing* plugin needs no marketplace change — skills are auto-discovered from the plugin's `skills/` directory. Adding a brand-new *plugin* requires a new entry in `.claude-plugin/marketplace.json` at the repo root.
- `SKILL.md` frontmatter conventions observed across this repo: the `name` field matches the skill's directory name; `description` states what the skill does plus the phrases that should trigger it; `user-invocable: true` marks skills meant to be run directly as `/plugin:skill`; `argument-hint` documents expected CLI-style args; `allowed-tools` scopes which tools a skill's steps may call (see `cc-plus/skills/delete-session/SKILL.md` for an example restricting `Bash` to specific scripts).

## Testing Instructions

No automated tests or CI. Validate a new or changed skill by installing the plugin locally and invoking its slash command to confirm it behaves as documented:

```bash
/plugin add .
/reload-plugins
```

## PR Instructions

No `CONTRIBUTING.md` or enforced commit format. Recent commit messages are short, imperative, present-tense summaries of the change (e.g. "Added migrate-session skill", "Increment version").
