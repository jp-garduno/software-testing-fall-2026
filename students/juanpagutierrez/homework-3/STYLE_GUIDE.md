# Team Python Style Guide (bonus)

This is a short, practical style guide based on what this homework's tooling
enforces. It's meant as a starting point for a small team, not an exhaustive
spec — the goal is that the tools do the enforcing, and this document
explains the *why* behind the defaults.

## Formatting

- **Line length**: 100 characters (configured in `.pylintrc` and passed to
  Black via `--line-length=100`). 79 is too cramped for modern wide-screen
  editors; 120 lets lines get hard to scan side by side in a diff.
- **Formatting is automatic**: run `black .` and `isort --profile=black .`
  before committing, or let the pre-commit hook do it. Never hand-format
  spacing, quotes, or import order — that's what causes noisy diffs and
  bikeshedding in code review.
- Imports are grouped: standard library, then third-party, then local —
  each group separated by a blank line, alphabetized within the group
  (isort does this automatically).

## Naming

- `snake_case` for functions, methods, and variables.
- `PascalCase` for classes.
- `UPPER_SNAKE_CASE` for module-level constants (e.g. `TASKS_FILE`).
- Avoid single-letter names except for short-lived loop counters (`i`, `j`)
  or trivial lambdas — prefer a descriptive name like `task` over `t`.

## Documentation

- Every module gets a one-line docstring describing its purpose.
- Every public function/method gets a one-line docstring describing what it
  does (not how) — if the function needs a paragraph to explain, it is
  probably doing too much.
- Skip docstrings only for tiny, obviously-named private helpers.

## Error handling

- Never use a bare `except:`. Catch the specific exception you expect
  (`json.JSONDecodeError`, `FileNotFoundError`, etc.) so unrelated bugs
  (like a typo causing a `NameError`) aren't silently swallowed.
- Always pass `encoding="utf-8"` to `open()` — relying on the platform
  default encoding causes hard-to-reproduce bugs across operating systems.

## Function design

- Never use a mutable object (`[]`, `{}`) as a default argument value.
  Use `None` and initialize inside the function body instead — Python
  evaluates default arguments once, at function definition time, so a
  mutable default is silently shared across every call that doesn't pass
  its own value.
- Prefer explicit imports (`from module import specific_name`) over
  wildcard imports (`from module import *`), which hide where a name
  actually comes from and can silently shadow other names.

## Commits

- Use [Conventional Commits](https://www.conventionalcommits.org/):
  `feat:`, `fix:`, `chore:`, `docs:`, `style:`, `refactor:`, `test:`.
- One logical change per commit; keep formatting-only changes in their own
  `style:` commit separate from behavior changes.

## Tooling summary

| Tool    | Purpose                          | When it runs           |
| ------- | --------------------------------- | ----------------------- |
| Black   | Code formatting                  | pre-commit, CI          |
| isort   | Import ordering                  | pre-commit, CI          |
| Pylint  | Style, bugs, complexity           | pre-commit, CI          |
| Bandit  | Security issues                  | pre-commit, CI          |

If a rule genuinely doesn't apply to a specific line, disable it locally with
a comment explaining why (e.g. `# pylint: disable=too-many-arguments`)
instead of disabling it project-wide.
