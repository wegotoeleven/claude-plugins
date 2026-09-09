---
name: agents-forge
description: Generate a well-structured AGENTS.md file for a Git repository by analysing its code, structure, and configuration. AGENTS.md is the cross-vendor convention for giving AI coding agents (Codex, Cursor, Copilot, and others) operational instructions. Use when the user asks to create, generate, or write an AGENTS.md for a project or repository.
argument-hint: "[repo-path]"
---

# agents-forge

Analyse the current repository (or the path provided in args) and produce an
`AGENTS.md` that follows the cross-vendor [agents.md](https://agents.md)
convention. Write the file to the root of the repository. If an `AGENTS.md`
already exists, show the user a diff of what would change and ask for
confirmation before overwriting.

`AGENTS.md` is read natively by Codex CLI, Cursor, GitHub Copilot, Devin,
Aider, Windsurf, Amp, Zed, Jules, VS Code, and other agentic tools. Claude
Code does not read it natively — it reads `CLAUDE.md` — so this skill also
wires up the documented bridge (see "The CLAUDE.md bridge" below) so Claude
Code picks up the same instructions.

**Guiding test**: an AI agent should be able to open the repository and
start working competently from `AGENTS.md` alone — how to set it up, build
it, test it, and submit a change correctly — without having to rediscover
those facts by trial and error first. Every section exists to serve that
test; if a piece of content wouldn't change how an agent acts in its first
few tool calls, it doesn't belong in AGENTS.md.

## How this differs from README.md

`AGENTS.md` is written for an AI agent about to work in this codebase, not
for a human evaluating the project. Skip anything a README would cover
(what the project is, why it exists, marketing framing) and skip anything
an agent can already discover by reading the code. Every line should be
something that saves an agent from getting a command, convention, or
guardrail wrong on its first attempt — the sort of thing you'd tell a new
teammate on their first day, not what you'd put in a pitch deck.

If a `readme-forge`-produced README already exists, don't restate its
content — reference it if useful, but keep AGENTS.md itself terse and
operational.

## Discovery phase

Gather the following before writing a single word. Only include a fact if
you can point to where you found it (a config file, script, or lockfile) —
never guess a command or convention.

1. **Repository root** — resolve from args or the current working directory.
2. **Monorepo check** — look for a workspace/package manager config
   (`pnpm-workspace.yaml`, `lerna.json`, `nx.json`, `go.work`, a Cargo
   workspace, multiple `pyproject.toml`/`package.json` under one root, etc.).
   If the repo is a genuine monorepo with independently buildable packages,
   plan for a root `AGENTS.md` plus one nested `AGENTS.md` per package
   (see "Monorepo handling" below) instead of a single flat file.
3. **Setup / build commands** — read `Makefile`, `package.json` scripts,
   `pyproject.toml`, `Cargo.toml`, `Dockerfile`, `docker-compose.yml`, and
   CI config (`.github/workflows/`, `.gitlab-ci.yml`) for the exact install,
   build, and dev-server commands. Prefer the commands CI actually runs over
   ones only mentioned in prose docs — CI is what's proven to work.
4. **Code style** — read linter/formatter configs (`.eslintrc*`,
   `.prettierrc*`, `ruff.toml`/`pyproject.toml` `[tool.ruff]`,
   `rustfmt.toml`, `.editorconfig`, `golangci.yml`) and any stated
   conventions in existing docs. Note naming/formatting rules only if
   they're enforced or explicitly documented, not inferred from a glance
   at a few files.
5. **Testing instructions** — the exact command(s) to run the full test
   suite, and, if discoverable, how to run a single test/file. Check
   `test/`, `tests/`, `spec/`, and manifest test scripts.
6. **PR / commit instructions** — existing `CONTRIBUTING.md`, PR templates,
   commit message conventions (e.g. Conventional Commits enforced by a
   commitlint config), branch naming rules, and required pre-merge checks
   (lint/test/build steps CI enforces).
7. **Dev environment tips** — required environment variables, local
   services the project depends on (databases, queues, mock servers via
   `docker-compose.yml`), default ports, and any non-obvious setup steps
   a fresh clone needs before commands in step 3 will work.
8. **Security / guardrails** — secrets handling (e.g. never commit
   `.env`), generated or vendored files agents shouldn't hand-edit
   (lockfiles, `dist/`, generated protobuf/GraphQL code, migrations),
   and any destructive commands or paths that need extra care. Only
   include what the repo's own structure or docs actually indicate —
   don't invent hypothetical risks.
9. **Existing `AGENTS.md`** — read it in full if present; this run should
   update it, not silently replace hard-won content.
10. **Existing `CLAUDE.md`** — read it if present, and check whether it
    already imports `AGENTS.md` (a first line of `@AGENTS.md`) or is a
    symlink to it.
11. **Existing README** — skim it for context (what the project is) so
    AGENTS.md doesn't need to re-derive that, but don't copy its content in.

Use parallel tool calls where reads are independent.

## AGENTS.md structure

`AGENTS.md` is plain Markdown with no enforced schema — agents just parse
the text. Even so, produce a consistent structure so the skill's output is
predictable. Omit any section with nothing genuine to say; never include
placeholder text or `TODO` markers.

```
# <Project Name> — Agent Instructions

<Optional one-line pointer to the README for what/why context, e.g.
"See README.md for what this project is and why it exists." Omit if
there's no README.>

## Setup Commands

The exact commands to install dependencies and get a working dev
environment, in fenced code blocks. Include prerequisite versions only
if the repo pins them (e.g. an `.nvmrc`, `engines` field, `rust-toolchain`).

## Dev Environment Tips

Environment variables, local services, ports, and any other state a fresh
clone needs before Setup Commands will fully work. Omit if Setup Commands
alone is sufficient.

## Code Style

Enforced conventions only — point at the linter/formatter config and
summarise what it enforces, rather than restating every rule the config
already encodes.

## Testing Instructions

The exact command to run the full suite, and how to run a single
test/file if that's discoverable. State what must pass before a change is
considered done.

## PR Instructions

Commit message format, branch naming, and the pre-merge checklist (the
checks CI will run, so an agent can run them locally first).

## Security Considerations    (omit if nothing genuine to say)

Secrets handling, files/paths agents must not hand-edit, and any
commands that need extra care.
```

### Monorepo handling

If discovery found a genuine monorepo, write a root `AGENTS.md` containing
only what's true repo-wide (shared setup, shared PR conventions, shared
security notes), and one `AGENTS.md` per package containing that package's
setup/test/style specifics. Say so explicitly in the root file, e.g. "See
`packages/<name>/AGENTS.md` for package-specific commands." Agents read the
nearest `AGENTS.md` in the directory tree, so the closest file to the code
being changed takes precedence — don't duplicate package-specific detail in
the root file.

## The CLAUDE.md bridge

Claude Code reads `CLAUDE.md`, not `AGENTS.md`. After writing `AGENTS.md`,
wire up the bridge so Claude Code reads the same content:

- **No `CLAUDE.md` exists yet**: create one whose first line is
  `@AGENTS.md` (an import — Claude Code expands it at session start). If
  the user has Claude-specific instructions to add, put them below the
  import, under their own heading.
- **`CLAUDE.md` exists and already imports `AGENTS.md`** (first line is
  `@AGENTS.md`, or it's a symlink to `AGENTS.md`): leave it alone.
- **`CLAUDE.md` exists with other content and no `AGENTS.md` import**:
  show the user a diff that prepends `@AGENTS.md` as the new first line
  ahead of the existing content, and ask for confirmation before writing —
  this is an existing file with content the user wrote, not scaffolding
  this skill owns. If the existing `CLAUDE.md` content substantially
  overlaps with what's now in `AGENTS.md`, point that out so the user can
  decide whether to trim it, but don't delete or rewrite their content
  yourself.

Default to the `@AGENTS.md` import over a symlink: it works cross-platform
(symlinks need Administrator/Developer Mode on Windows) and still allows
Claude-specific instructions underneath. Only use a symlink
(`ln -s AGENTS.md CLAUDE.md`) if the user asks for it explicitly and there's
no Claude-specific content to add.

## Writing rules

- Every instruction must be traceable to something discovered in the repo
  (a config file, script, CI step, or existing doc) — never invented.
- Prefer exact commands over descriptions ("Run `pnpm test --filter web`",
  not "run the web package's tests").
- Keep it short. Agents load this file into every session; padding it with
  restated code or obvious advice costs context for no benefit. If a
  section would just restate what a linter config already enforces, point
  at the config instead of repeating its rules.
- All commands in fenced code blocks with the correct language tag.
- No marketing language, no badges, no emoji.
- If something is unclear or contested (e.g. two conflicting lint configs),
  say so plainly rather than picking one silently.

## Process

1. Run the discovery phase in parallel where possible.
2. Decide single-file vs monorepo layout.
3. Synthesise findings into the structure above.
4. Write `AGENTS.md` (and any nested package `AGENTS.md` files). If one
   already exists, show a diff and get confirmation before overwriting.
5. Apply the CLAUDE.md bridge logic above.
6. Report a one-line summary of what was written (including any nested
   files and whether the CLAUDE.md bridge was created, already present, or
   needs the user's confirmation), and flag any sections omitted and why.
