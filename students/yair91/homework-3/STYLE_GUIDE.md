# Team style guide

A short guide so the tooling and the people agree. Everything here is enforced
by a tool; nothing is left to taste or to review comments.

## The rule behind the rules

**If a tool can decide it, a person should not.** Formatting, import order and
line length are settled by black, isort and pylint. Review time goes to naming,
boundaries and whether the code is correct.

## Formatting

| Setting | Value | Enforced by |
| --- | --- | --- |
| Line length | 120 | black, pylint, isort |
| Quotes | double | black |
| Import order | standard library, third party, local | isort (`--profile=black`) |
| End of file | one newline, no trailing whitespace | pre-commit hooks |
| Line endings | LF | `mixed-line-ending` hook |

120 rather than black's default 88: it is the number the course standard uses,
and at 88 the dictionary literals in this project wrap into something harder to
read than the long line.

## Naming

- Modules, functions and variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`, at module level
- Short names only where the meaning is obvious in context: `i`, `sku`, `qty`.
  They are listed in `.pylintrc` under `good-names`; anything else gets a word.

A name that needs a comment to be understood is the wrong name.

## Docstrings

Every module, class and public function has one. One line when one line is
enough. The docstring says *why* or *what for*, not what the code already
says:

```python
# Not useful
def total_value(self):
    """Return the total value."""

# Useful
def total_value(self):
    """Return the money tied up in the catalogue."""
```

## Error handling

- Never a bare `except`. Catch the exception you expect, by name.
- `is None`, never `== None`.
- No mutable default arguments. `None` as the default, build the list inside.

These three are not style. Each one was a real bug in the first version of this
project, documented in [REPORT.md](REPORT.md).

## Commits

Conventional Commits, enforced by a `commit-msg` hook:

```
<type>(<scope>): <description in the imperative, lowercase>
```

Types in use: `feat`, `fix`, `docs`, `style`, `refactor`, `chore`, `test`.
One logical change per commit. If the message needs an "and", it is two
commits.

## When each tool runs

| Moment | What runs |
| --- | --- |
| On save, in the editor | black, isort |
| On commit | every hook in `.pre-commit-config.yaml`, about two seconds |
| On push and pull request | the same checks over every file, plus `--fail-under=10` |

The budget for the commit hooks is a couple of seconds. Past that, people start
using `--no-verify`, and a hook that gets skipped protects nothing.

## Turning a rule off

`.pylintrc` disables nothing. If a rule has to be relaxed, it gets changed in
the file with a comment saying why, in the same commit. The one in place today:

```ini
[DESIGN]
# Product and Movement are value objects: they hold data and little else.
min-public-methods = 1
```

A rule turned off without a reason comes back later as a bug.
