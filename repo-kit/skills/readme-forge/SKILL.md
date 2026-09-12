---
name: readme-forge
description: Generate a well-structured README.md for a Git repository by analysing its code, structure, and git history. Use when the user asks to create, generate, or write a README for a project or repository.
argument-hint: "[repo-path]"
---

# readme-forge

Analyse the current repository (or the path provided in args) and produce a
`README.md` that meets common GitHub open-source conventions. Write the file
to the root of the repository. If a `README.md` already exists, show the user
a diff of what would change and ask for confirmation before overwriting.

**Guiding test**: a human developer should be able to clone the repository
and start understanding it from the README alone — what it is, why it
exists, and how to get it running — without having to read source first.
Every section exists to serve that test; if a piece of content wouldn't
help a newly-cloned reader get oriented, it doesn't belong in the README.

## Discovery phase

Gather the following before writing a single word:

1. **Repository root** — resolve from args or the current working directory.
2. **Project name** — use the directory name; cross-check against
   `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, or equivalent.
3. **Language and toolchain** — infer from file extensions, lock files, and
   manifest files present in the tree.
4. **What it is** — read the entry-point files (e.g. `main.*`, `index.*`,
   `app.*`, `src/`), top-level source files, and any existing docs folder, to
   describe what the project does and its notable capabilities.
5. **Why it exists** — infer the problem being solved from the README/docs
   (if present), issue templates, commit messages, and code comments. Look
   for stated motivation, non-goals, or a "why not X" rationale. If nothing
   in the repo speaks to motivation, keep this section short and factual
   rather than inventing a narrative.
6. **Prerequisites and install steps** — read `Makefile`, `package.json`
   scripts, `pyproject.toml`, `Cargo.toml`, `Dockerfile`, `docker-compose.yml`,
   CI config (`.github/workflows/`, `.gitlab-ci.yml`), and shell scripts in
   the repo root for dependency versions and setup commands.
7. **Run and configuration** — the exact command(s) that start/build the
   project, plus `.env.example`, `config/`, environment variable usage in
   source files, and any sample config files needed to run it.
8. **Usage and tests** — concrete usage examples (CLI invocation, library
   import, API call) and any `test/`, `tests/`, `spec/` directory or test
   scripts defined in manifests.
9. **Contributing** — existing `CONTRIBUTING` file, branch conventions,
   PR templates, or issue templates, and whether the repo otherwise reads as
   personal/private (e.g. no stated intent for others to use or fork it)
   versus intended for outside use.
10. **License** — read `LICENSE`, `LICENSE.md`, or the license field in
    manifests.
11. **Existing docs** — read any `docs/` folder, inline `USAGE`, or
    `CHANGELOG` files that should be cross-referenced.
12. **Recent git history** — run `git log --oneline -20` to understand what
    the project does if source alone is ambiguous.

Use parallel tool calls where reads are independent.

## README structure

Produce the README in this exact section order, with literal question-style
headings as shown. Never include placeholder text or `TODO` markers.

```
# <Project Name>

<One-sentence tagline — what it does and for whom.>

## What is this?

2–4 sentences: what the project does, its main approach, and notable
capabilities (fold in what would otherwise be a "Features" list — as prose
or a short bullet list if there are more than a couple of items).

## Why does it exist?

The problem it solves and, where genuinely known from the repo, the
reasoning behind the approach or any notable constraints/non-goals. Keep
this short and factual — do not invent motivation the repo doesn't state.
Use `###` subheadings only if the reasoning is genuinely multi-part (e.g.
several independent design decisions that each need their own line) —
don't add them for a single paragraph of motivation.

## How do I install it?

Prerequisites (runtime/build-time dependencies with versions, where known),
then step-by-step shell commands in a fenced code block covering clone →
install → any post-install setup. Use the actual commands discovered in
the repo.

## How do I run it?

The exact command(s) to start/build the project, and any required or
optional environment variables / config keys needed to do so. Reference
the `.env.example` or config file if one exists. Omit the configuration
part if the project needs none. Use `###` subheadings only if there's
enough distinct material to need them (e.g. separate start/stop/logs
commands plus a non-trivial config explanation) — a couple of commands
and a short note don't need subheadings.

## How do I use it?

Concrete usage examples — the golden path first, then the most common
variations. Use fenced code blocks for every command. If the tool has a
CLI, show `--help` output style. If it is a library, show a short import +
call example. If the repo has tests, include the command(s) to run the
test suite as part of this section. This is also where any material that
doesn't fit the other sections belongs — e.g. a service/API reference
table, persistent data paths, operational notes, or known limitations.
Use `###` subheadings only if there's enough of this kind of material to
need them; for a simple tool, usage examples alone with no subheadings
is normal and preferred.

## How do I contribute?    (omit if the repo is clearly personal/private)

One short paragraph: branch conventions, PR expectations, where to file
issues.

## License

Always include this section, regardless of whether the repo is
personal/private. State the licence name and link to the LICENSE file, e.g.
`Distributed under the MIT License. See [LICENSE](LICENSE) for details.` If
no license file or field exists anywhere in the repo, say so plainly (e.g.
"No license is specified.") rather than guessing one.
```

## Writing rules

- Use the literal question-style headings shown above, verbatim, including
  sentence case — do not reword them into conventional headings like
  "Overview" or "Installation", and do not title-case them.
- `###` subheadings are permitted only under "Why does it exist?", "How do
  I run it?", and "How do I use it?", and only when the content genuinely
  needs them to stay readable — not by default. Every other section stays
  flat.
- All shell commands in fenced code blocks with the correct language tag
  (`bash`, `sh`, `powershell`, etc.).
- No badges unless the repo already has a CI config — in that case add a
  build-status badge for the primary CI workflow only.
- No "Table of Contents" section — the README is a fixed, short set of
  sections and doesn't need one.
- No emoji.
- Active voice, present tense ("Run `make build`", not "You can run…").
- Do not invent features, commands, config keys, or motivation that do not
  exist in the repo. If something is unclear, keep that section brief and
  factual rather than guess — the License section is the one exception: it
  is never omitted and must always state something explicit, even if that's
  "no license specified".
- Keep the tone neutral and technical — avoid marketing language.

## Process

1. Run the discovery phase in parallel where possible.
2. Synthesise findings into the README structure above.
3. Write `README.md` to the repository root.
4. Report a one-line summary of what was written and flag any sections that
   were omitted and why.
