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

## Discovery phase

Gather the following before writing a single word:

1. **Repository root** — resolve from args or the current working directory.
2. **Project name** — use the directory name; cross-check against
   `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, or equivalent.
3. **Language and toolchain** — infer from file extensions, lock files, and
   manifest files present in the tree.
4. **Purpose** — read the entry-point files (e.g. `main.*`, `index.*`,
   `app.*`, `src/`), top-level source files, and any existing docs folder.
5. **Install / build / run commands** — read `Makefile`, `package.json`
   scripts, `pyproject.toml`, `Cargo.toml`, `Dockerfile`, `docker-compose.yml`,
   CI config (`.github/workflows/`, `.gitlab-ci.yml`), and shell scripts in
   the repo root.
6. **Configuration** — look for `.env.example`, `config/`, environment
   variable usage in source files, and any sample config files.
7. **Tests** — check for a `test/`, `tests/`, `spec/` directory or test
   scripts defined in manifests.
8. **License** — read `LICENSE`, `LICENSE.md`, or the license field in
   manifests.
9. **Existing docs** — read any `docs/` folder, inline `USAGE`, `CONTRIBUTING`,
   or `CHANGELOG` files that should be cross-referenced.
10. **Recent git history** — run `git log --oneline -20` to understand what
    the project does if source alone is ambiguous.

Use parallel tool calls where reads are independent.

## README structure

Produce the README in this exact section order. Omit a section entirely if
there is genuinely nothing to say (e.g. no configuration needed). Never
include placeholder text or `TODO` markers.

```
# <Project Name>

<One-sentence tagline — what it does and for whom.>

<Optional: 2–4 sentence expanded description. Include the core problem solved,
the main approach, and any notable constraints or non-goals.>

## Features          (omit if the project is a single-purpose tool)

- Bullet list of meaningful capabilities — not boilerplate

## Prerequisites

List runtime and build-time dependencies with version requirements where known.

## Installation

Step-by-step shell commands in a fenced code block. Cover clone → install →
any post-install setup. Use the actual commands discovered in the repo.

## Usage

Concrete examples — the golden path first, then the most common variations.
Use fenced code blocks for every command. If the tool has a CLI, show `--help`
output style. If it is a library, show a short import + call example.

## Configuration      (omit if none)

Explain every required and optional environment variable or config key.
Reference the `.env.example` or config file if one exists.

## Running Tests      (omit if no tests found)

The exact command(s) to run the test suite.

## Contributing       (omit if the repo is clearly personal/private)

One short paragraph: branch conventions, PR expectations, where to file issues.

## License

State the licence name and link to the LICENSE file. Example:
`Distributed under the MIT License. See [LICENSE](LICENSE) for details.`
```

## Writing rules

- Use title case for section headings.
- All shell commands in fenced code blocks with the correct language tag
  (`bash`, `sh`, `powershell`, etc.).
- No badges unless the repo already has a CI config — in that case add a
  build-status badge for the primary CI workflow only.
- No "Table of Contents" section for READMEs shorter than six sections.
- No emoji.
- Active voice, present tense ("Run `make build`", not "You can run…").
- Do not invent features, commands, or config keys that do not exist in the
  code. If something is unclear, leave that section out rather than guess.
- Keep the tone neutral and technical — avoid marketing language.

## Process

1. Run the discovery phase in parallel where possible.
2. Synthesise findings into the README structure above.
3. Write `README.md` to the repository root.
4. Report a one-line summary of what was written and flag any sections that
   were omitted and why.
