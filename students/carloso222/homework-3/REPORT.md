# Static Testing Analysis Report

**Project**: Python Calculator (with input validation and operation history)
**Tools used**: Pylint, Black, isort, pre-commit

## 1. Issues Found

Running Pylint on the initial version of the `src/` code (`calculator.py`,
`validator.py`, `history.py`) found **6 issues** across two of the three
modules. `calculator.py` scored a clean 10.00/10 from the start, while
`validator.py` and `history.py` triggered warnings.

### Issue 1

- **Tool**: Pylint
- **Error**: `W0611`: Unused import `sys`
- **Location**: `validator.py:3`
- **Fix**: Removed the unused `import sys` statement.

### Issue 2

- **Tool**: Pylint
- **Error**: `W0611`: Unused import `math`
- **Location**: `validator.py:4`
- **Fix**: Removed the unused `import math` statement.

### Issue 3

- **Tool**: Pylint
- **Error**: `C0301`: Line too long (186/100 characters)
- **Location**: `validator.py:29`
- **Fix**: Rewrote the oversized inline docstring of `validate_operands` as a
  short summary line plus a wrapped extended description, and simplified the
  function body to return the tuple directly instead of using two throwaway
  variables.

### Issue 4

- **Tool**: Pylint
- **Error**: `W0611`: Unused import `os`
- **Location**: `history.py:5`
- **Fix**: Removed the unused `import os` statement (it had been added while
  planning a file-saving feature but was never actually used at that point).

### Issue 5

- **Tool**: Pylint
- **Error**: `W0702`: Bare `except` clause (`bare-except`)
- **Location**: `history.py:59`
- **Fix**: Replaced the bare `except:` in `save_to_file` with
  `except OSError as error`, so only expected file-system errors are caught
  and the error message is surfaced to the caller instead of being silently
  swallowed.

### Issue 6

- **Tool**: Pylint
- **Error**: `W1514`: `open()` used without explicit `encoding`
  (`unspecified-encoding`)
- **Location**: `history.py:57`
- **Fix**: Added `encoding="utf-8"` to the `open()` call to make file
  encoding explicit and avoid platform-dependent behavior.

**Categories**: all six issues fell into two categories — *code hygiene*
(unused imports, 3 of 6) and *robustness/error-handling* (bare except,
missing encoding, and an overly long/undocumented line, 3 of 6). No actual
logic bugs were introduced, but two of the issues (bare-except and missing
encoding) could have caused real problems in production: the bare except
would have hidden genuine bugs (e.g., a typo in a variable name) behind a
generic "Could not save history" message, and relying on the platform
default encoding can break on machines with a different locale.

After applying `black` and `isort` for formatting and import ordering, and
fixing the six issues above, the project scores **10.00/10** on Pylint.

## 2. Benefits Observed

Static testing caught things a quick manual read-through likely would have
missed. The unused imports are a good example: they don't affect program
behavior at all, so they're easy to skim past when reviewing code by eye,
but they add noise and can mislead future readers into thinking a module is
used somewhere. The bare `except` clause is the more interesting catch —
it's a pattern that "looks fine" and even feels defensive, but it's a real
anti-pattern that swallows unrelated errors. I doubt I would have flagged it
myself without the linter pointing it out explicitly.

Setup took about 30–40 minutes total: installing `pre-commit`, `pylint`,
`black`, and `isort`, writing the `.pre-commit-config.yaml`, generating and
tweaking `.pylintrc` (I raised `max-line-length` from 100 to a value that
matched the project's style), and then iterating on the actual fixes. That
is a small one-time cost compared to the time that could be lost later
debugging a silently-swallowed exception in production, or dealing with
merge conflicts caused by inconsistent formatting across contributors.

## 3. Integration

In a team workflow, I would run these tools at three different points:

- **In the IDE**: `black` and `pylint` as on-save/on-type integrations, so
  formatting and obvious issues are visible immediately while writing code,
  before a commit is even attempted.
- **Pre-commit hook**: the current `.pre-commit-config.yaml` setup, so no
  commit reaches the shared repository with trailing whitespace, malformed
  YAML/JSON, unsorted imports, or unformatted code. This keeps the "noise"
  out of code review so reviewers can focus on logic instead of style.
- **CI pipeline**: a full `pylint`, `black --check`, and `pytest --cov` run
  on every pull request, acting as a safety net in case someone bypasses
  local hooks (e.g., with `git commit --no-verify`) or has an outdated local
  environment.

## 4. Recommendations

`black` was the most immediately useful tool — it removes any debate about
formatting and just fixes it automatically, which meant I never had to
manually think about spacing or quote style. `pylint` was the most
educational, since it explained *why* something was a problem (not just
*that* it was), particularly with the bare-except warning.

One change I'd make going forward: I would enable a security-focused linter
like `bandit` from the start rather than as an afterthought, since a couple
of the issues found here (silent exception handling, implicit encoding)
sit right at the boundary between "style" and "security/reliability."

I would absolutely use this setup in future projects. The one-time cost of
configuring `pre-commit` and the linters is small, and it pays for itself
almost immediately by catching low-value review comments before a human
reviewer ever has to make them, leaving code review time for design and
logic discussions instead of formatting nitpicks.
