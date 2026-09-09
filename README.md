# claude-plugins

A personal Claude Code plugin marketplace of skills for session management, repository documentation, and blog publishing.

## What is this?

This repository is a Claude Code plugin marketplace, registered at `.claude-plugin/marketplace.json`. It bundles three plugins, each a self-contained set of skills:

- **cc-plus** — quality-of-life enhancements for Claude Code itself: deleting and migrating session history, and re-explaining a response in plain terms.
- **repo-kit** — skills for fleshing out and maintaining git repositories: generating `README.md` and `AGENTS.md` files, and tidying bash scripts to a house style.
- **blog-kit** — turns rough notes into a finished blog post and publishes it to a Hugo blog repo.

## Why does it exist?

To package a set of personal Claude Code workflows as installable plugins, rather than keeping them as one-off prompts or scattered scripts.

## How do I install it?

Prerequisites:

- [Claude Code](https://claude.ai/code) CLI installed and authenticated.

```bash
/plugin add https://github.com/wegotoeleven/claude-plugins.git
/reload-plugins
```

## How do I run it?

Install individual plugins from the marketplace as needed:

```
/plugin install cc-plus
/plugin install repo-kit
/plugin install blog-kit
```

## How do I use it?

Each skill is invoked as a slash command scoped to its plugin, e.g. `/<plugin>:<skill>`.

### cc-plus

| Skill | Description |
|---|---|
| `delete-session` | Selectively delete Claude Code session history files from disk |
| `hol-up` | Re-explain the last response in plain terms, optionally tailored to a named audience |
| `migrate-session` | Copy a session's history into a different project directory so it shows up in `/resume` |

```
/cc-plus:delete-session
/cc-plus:hol-up
/cc-plus:hol-up for my manager
/cc-plus:migrate-session
```

### repo-kit

| Skill | Description |
|---|---|
| `agents-forge` | Generates an `AGENTS.md` with operational instructions for AI coding agents |
| `bash-tidy` | Refactors a bash script to conform to a house style guide based on the Google Shell Style Guide |
| `readme-forge` | Analyses a git repository and writes a `README.md` that conforms to common GitHub conventions |

```
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

```
/blog-kit:write-post path/to/notes.txt
```

## License

No license is specified.
