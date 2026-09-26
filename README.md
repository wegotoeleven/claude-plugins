# claude-plugins

A personal Claude Code plugin marketplace of skills for session management, repository documentation, and blog publishing.

## What is this?

This repository is a Claude Code plugin marketplace, registered at `.claude-plugin/marketplace.json`. It bundles three plugins, each a self-contained set of skills:

- **cc-plus** — quality-of-life enhancements for Claude Code itself: listing, deleting and migrating session history, and re-explaining a response in plain terms.
- **repo-kit** — skills for fleshing out and maintaining git repositories: generating `README.md` and `AGENTS.md` files, and tidying bash scripts to a house style.
- **blog-kit** — turns rough notes into a finished blog post and publishes it to a Hugo blog repo.

## Why does it exist?

To package a set of personal Claude Code workflows as installable plugins, rather than keeping them as one-off prompts or scattered scripts.

## How do I install it?

Prerequisites:

- [Claude Code](https://claude.ai/code) CLI installed and authenticated.
- Git to clone the marketplace; Python 3 for the session-management scripts (standard library only).

Clone the repository and start Claude Code:

```bash
git clone https://github.com/wegotoeleven/claude-plugins.git
cd claude-plugins
claude
```

Inside Claude Code, register the local marketplace and install the plugins you need:

```text
/plugin marketplace add .
/plugin install cc-plus@wegotoeleven-claude-plugins
/plugin install repo-kit@wegotoeleven-claude-plugins
/plugin install blog-kit@wegotoeleven-claude-plugins
/reload-plugins
```

Alternatively, register the remote marketplace with the following Claude Code command, then use the same install commands above:

```text
/plugin marketplace add https://github.com/wegotoeleven/claude-plugins.git
```

See the [Claude Code marketplace documentation](https://code.claude.com/docs/en/plugin-marketplaces) for installation details.

## How do I run it?

Start Claude Code in the project you want to work on, then invoke a skill from the examples below:

```bash
claude
```

There is no separate build step or service to start. Slash commands run inside Claude Code, not in your shell.

## How do I use it?

Each skill is invoked as a slash command scoped to its plugin, e.g. `/<plugin>:<skill>`.

### cc-plus

| Skill | Description |
|---|---|
| `delete-session` | Selectively delete Claude Code session history files from disk |
| `list-sessions` | List every Claude Code session on this machine with the full path to its transcript |
| `hol-up` | Re-explain the last response in plain terms, optionally tailored to a named audience |
| `migrate-session` | Copy a session's history into a different project directory so it shows up in `/resume` |

```text
/cc-plus:delete-session
/cc-plus:hol-up
/cc-plus:hol-up for my manager
/cc-plus:list-sessions
/cc-plus:migrate-session
```

Session scripts read data under `~/.claude/`. Deletion previews the affected files and asks for confirmation before permanently removing them. Migration copies history into the current project, preserves the source, and can overwrite matching destination files; do not migrate the live session running the skill.

### repo-kit

| Skill | Description |
|---|---|
| `agents-forge` | Generates an `AGENTS.md` with operational instructions for AI coding agents |
| `bash-tidy` | Refactors a bash script to conform to a house style guide based on the Google Shell Style Guide |
| `readme-forge` | Analyses a git repository and writes a `README.md` that conforms to common GitHub conventions |

```text
/repo-kit:agents-forge
/repo-kit:agents-forge path/to/repo
/repo-kit:bash-tidy path/to/script.sh
/repo-kit:readme-forge
/repo-kit:readme-forge path/to/repo
```

### blog-kit

| Skill | Description |
|---|---|
| `write-post` | Turns rough notes, a rant, or dictated input into a polished post in the user's voice and commits it to a Hugo blog repo |

```text
/blog-kit:write-post path/to/notes.txt
```

`write-post` targets the author's `wegotoeleven/blog` repository and requires Git access to it. It asks for approval before committing and pushing to `main`, which triggers deployment. Hugo is optional for local build verification.

## License

No license is specified.
