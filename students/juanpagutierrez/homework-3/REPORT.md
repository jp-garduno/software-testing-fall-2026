# Static Testing Analysis Report

**Project**: Task Manager CLI (Python)
**Tools used**: pre-commit, Black, isort, Pylint

## 1. Issues Found

Before any fixes, `pylint --rcfile=.pylintrc src/*.py` reported **26 issues**
across the three source files and rated the code **7.73/10**. `black --check`
flagged 2 of the 3 files as needing reformatting, and `isort --check-only`
flagged all 3 files for incorrectly ordered imports. In total, the linters
surfaced problems in four broad categories:

- **Style/convention (C-codes)**: 16 issues — missing docstrings, two
  functions and one method using camelCase instead of snake_case, a
  151-character line, a multi-statement line, and an `== True` singleton
  comparison.
- **Warnings (W-codes)**: 9 issues — a bare `except:`, two `open()` calls
  without an explicit encoding, an unused `sys` import in two files, a
  wildcard import (`from task_manager import *`) that also produced an
  "unused wildcard import" warning, and a mutable default argument
  (`tasks=[]`) on `TaskManager.__init__`.
- **Import ordering**: import statements were not alphabetized or grouped
  per PEP 8 / isort conventions in all three files.
- **Formatting**: inconsistent blank lines and an unwrapped dictionary
  literal that Black collapsed/expanded automatically.

The most common category by far was missing docstrings (9 occurrences),
followed by naming-convention violations. After fixing everything, Pylint
reports **0 issues and a 10.00/10 score**; `black` and `isort` report all
files as already formatted. The before/after Pylint output is committed as
`pylint-report-before.txt` and `pylint-report-after.txt` for reference.

## Appendix: Documented Fixes

### Issue 1

- **Tool**: Pylint
- **Error**: W0102: Dangerous default value `[]` as argument (`dangerous-default-value`)
- **Location**: `src/task_manager.py:9`
- **Fix**: Replaced the mutable default with `None` and initialized inside the method.
- **Before**: `def __init__(self, tasks=[]):`
- **After**: `def __init__(self, tasks=None):` with `self.tasks = tasks if tasks else load_tasks()`

### Issue 2

- **Tool**: Pylint
- **Error**: W0702: No exception type(s) specified (`bare-except`)
- **Location**: `src/storage.py:16`
- **Fix**: Caught the specific expected exception instead of a bare `except:`.
- **Before**: `except:\n        return []`
- **After**: `except json.JSONDecodeError:\n        return []`

### Issue 3

- **Tool**: Pylint
- **Error**: W0401 / W0614: Wildcard import / unused wildcard import
- **Location**: `src/cli.py:3`
- **Fix**: Imported only the names actually used.
- **Before**: `from task_manager import *`
- **After**: `from task_manager import TaskManager`

### Issue 4

- **Tool**: Pylint
- **Error**: C0103: Function name doesn't conform to snake_case naming style (`invalid-name`)
- **Location**: `src/storage.py:9,20,26`
- **Fix**: Renamed `loadTasks`, `saveTasks`, `deleteStorageFile` to snake_case.
- **Before**: `def loadTasks(path=TASKS_FILE):`
- **After**: `def load_tasks(path=TASKS_FILE):`

### Issue 5

- **Tool**: Pylint
- **Error**: C0301: Line too long (151/100) (`line-too-long`)
- **Location**: `src/storage.py:37`
- **Fix**: Dropped an unused dict key and let Black wrap the remaining literal across multiple lines.
- **Before**: `summary = {"total": total, "done": done, "pending": pending, "unused_field_that_is_not_needed...": None}`
- **After**: `return {"total": total, "done": done, "pending": pending}`

### Issue 6

- **Tool**: Pylint
- **Error**: C0121: Singleton comparison (`singleton-comparison`)
- **Location**: `src/storage.py:35`
- **Fix**: Used `is True` instead of `== True`.
- **Before**: `t.get("completed") == True`
- **After**: `t.get("completed") is True`

### Issue 7

- **Tool**: isort
- **Error**: Imports incorrectly sorted and/or formatted
- **Location**: `src/cli.py`, `src/storage.py`, `src/task_manager.py`
- **Fix**: Ran `isort --profile=black src/` to alphabetize and group standard-library vs. local imports.
- **Before**: `import sys\nimport argparse\nfrom task_manager import *\nfrom storage import get_storage_summary`
- **After**: `import argparse\n\nfrom storage import get_storage_summary\nfrom task_manager import TaskManager`

## 2. Benefits Observed

Static analysis caught real bugs that a quick manual read easily misses: the
mutable default argument (`tasks=[]`) is a classic Python pitfall that would
have caused every `TaskManager` instance without an explicit `tasks` argument
to silently share and mutate the same list — a bug that only shows up at
runtime, and only when two instances are created in the same process. The
bare `except:` was hiding exactly what kind of failure was being swallowed
(a real `json.JSONDecodeError` is very different from, say, a `KeyboardInterrupt`
or a `MemoryError`). The wildcard import would have made it easy to
accidentally shadow a name later without any warning. None of these would
reliably be caught by a quick manual review, especially under time pressure —
they require either deep familiarity with Python gotchas or, more
efficiently, a tool that already knows about them. Setup took about 20
minutes (installing the four tools, generating and trimming `.pylintrc`,
writing the `.pre-commit-config.yaml`), which is trivial compared to the time
a subtle shared-mutable-state bug could cost to debug in production.

## 3. Integration

In a team workflow I would run these tools at three points: (1) **in the
editor**, via the Pylint/Black/isort extensions, for instant feedback while
typing; (2) **at commit time**, via the pre-commit hooks configured here, so
nothing with an obvious issue ever reaches the shared history — this is the
cheapest point to fix something, before a reviewer ever sees it; and (3) **in
CI**, running the same `pre-commit run --all-files` command (or
`pylint --exit-zero` for scoring) on every pull request as a required check,
as a backstop for anyone who committed with `--no-verify` or an outdated
local environment. Formatting (Black/isort) should always auto-fix and
auto-commit where possible; correctness/style warnings from Pylint should
block the PR until addressed or explicitly justified with an inline
`# pylint: disable=` comment.

## 4. Recommendations

Black and isort were the most immediately useful tools because they require
zero decision-making — they just fix formatting and free up code review time
to focus on logic instead of spacing and import order. Pylint was the most
valuable for catching actual defects (the mutable default and bare except),
though its default rule set is noisy for small scripts; I'd keep it strict
for shared/production code but trim rules like `missing-module-docstring`
for short, self-explanatory scripts, as I did in `.pylintrc`. For future
projects I would add `bandit` for security-specific linting and wire all of
this into CI from day one rather than retrofitting it, since enforcing the
hooks from the very first commit is far easier than convincing a team to
adopt them after bad habits have already crept into the codebase.
