---
name: bash-tidy
description: Refactor a bash script to conform to the house style guide. Use when the user asks to tidy, clean up, or style-check a bash or shell script.
argument-hint: "[file-path]"
---

# bash-tidy

Refactor a bash script to conform to the house style guide. If a file
path is provided in the args, use that. Otherwise ask the user which
file to tidy.

## Style rules

### Header and safety
The file header must follow this exact structure (per Google Shell Style
Guide §File Header):

```bash
#!/usr/bin/env bash
#
# Brief description of what this script does.
```

- Line 1: `#!/usr/bin/env bash`
- Line 2: `#` (empty comment — no trailing space)
- Line 3+: description inferred from reading the script; one sentence is
  usually enough, more only if the purpose isn't obvious from the name
- No copyright, author, or filename lines unless already present
- `set -euo pipefail` follows the header block, separated by a blank line

### Formatting
- Follow the Google Shell Style Guide as the baseline
- 79-character line limit (PEP 8 equivalent for bash)
- 4-space indentation — no tabs
- Blank lines between logical sections; no `# ---` divider lines
- One blank line between function definitions

### Naming
- Functions: `snake_case`
- Local variables: `snake_case`, declared with `local` at top of function
- Script-level constants: `UPPER_SNAKE_CASE`, declared with `readonly`
- Global mutable state: `UPPER_SNAKE_CASE`
- No single-letter variable names except loop counters

### Functions
- No `function` keyword — use `name() {` form
- Declare all variables `local` inside functions
- Use `local __var` + `printf -v` for indirect (return-by-name) variables

### Standard utility functions
- Error-and-exit function must be named `fatal()`:
  ```bash
  fatal() {
      echo "Fatal: ${*}" >&2
      exit 1
  }
  ```
- Progress/info function must be named `info()`:
  ```bash
  info() {
      echo "==> ${*}"
  }
  ```
- All other error messages go to stderr with `>&2`

### Conditionals and syntax
- Use `[[ ]]` not `[ ]`
- Use `$(command)` not backticks
- Quote all variable expansions: `"${var}"` not `$var`
- Use `|| fatal "..."` for inline error handling where appropriate

### Comments
- Only comment where logic is not self-evident
- Function-level comments describe args and return values if non-obvious
- No end-of-line comments that just restate the code

### `main()` pattern
- All top-level logic lives in a `main()` function
- Script ends with `main "$@"`

## Process

1. Read the target file in full
2. Identify all deviations from the style rules above
3. Apply all fixes in a single edit pass — do not make multiple small edits
4. Summarise what was changed and why
