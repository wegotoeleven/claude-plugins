# claude-plugins

A personal Claude Code plugin marketplace.

Each plugin lives in its own subdirectory. The marketplace is registered at `.claude-plugin/marketplace.json`.

## Plugins

### repo-kit

| Skill | Description |
|---|---|
| `bash-tidy` | Refactors a bash script to conform to a house style guide based on the Google Shell Style Guide |
| `readme-forge` | Analyses a git repository and writes a `README.md` that conforms to common GitHub conventions |

## Prerequisites

- [Claude Code](https://claude.ai/code) CLI installed and authenticated.

## Installation

```bash
/plugin add https://github.com/wegotoeleven/claude-plugins.git
/reload-plugins
```

## Usage

### bash-tidy

Invoke with a file path, or let the skill prompt for one:

```
/repo-kit:bash-tidy path/to/script.sh
```

### readme-forge

Run from the repository root to document, or pass a path:

```
/repo-kit:readme-forge
/repo-kit:readme-forge path/to/repo
```
