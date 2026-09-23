# Static Testing Analysis Report

## Fixed Issues (Part 4)

### Issue 1

- **Tool**: Pylint
- **Error**: W0102 Dangerous default value `[]` as argument (dangerous-default-value)
- **Location**: `src/models.py:33` (`ExpenseBook.__init__`)
- **Fix**: Use `None` as the default and build a new list inside the function.
- **Before**: `def __init__(self, expenses=[]):`
- **After**: `def __init__(self, expenses=None): self.expenses = expenses if expenses is not None else []`

### Issue 2

- **Tool**: Pylint
- **Error**: W0702 No exception type(s) specified (bare-except)
- **Location**: `src/models.py:40` (`ExpenseBook.add`)
- **Fix**: Remove the try/except entirely — `is_valid()` never raises, so the
  bare `except: pass` was only hiding unrelated bugs.
- **Before**: `try:\n    if expense.is_valid():\n        self.expenses.append(expense)\nexcept:\n    pass`
- **After**: `if expense.is_valid():\n    self.expenses.append(expense)`

### Issue 3

- **Tool**: Pylint
- **Error**: C0103 Method name `ToDict`/`totalByCategory` doesn't conform to snake_case (invalid-name)
- **Location**: `src/models.py:23` and `src/models.py:49`
- **Fix**: Rename to `to_dict` and `total_by_category`, and update the call
  sites in `src/storage.py` and `src/reports.py`.
- **Before**: `def ToDict(self): ...` / `def totalByCategory(self, category): ...`
- **After**: `def to_dict(self): ...` / `def total_by_category(self, category): ...`

### Issue 4

- **Tool**: Pylint
- **Error**: W1514 / R1732 Using `open` without an explicit encoding, and
  without a `with` block (unspecified-encoding, consider-using-with)
- **Location**: `src/storage.py:9-12` (`save_to_json`) and similar spots in
  `load_from_json`
- **Fix**: Use `with open(path, "w", encoding="utf-8") as f:` instead of a
  manual `open()`/`close()` pair.
- **Before**: `f = open(path, "w")\njson.dump(data, f)\nf.close()`
- **After**: `with open(path, "w", encoding="utf-8") as f:\n    json.dump(data, f)`

### Issue 5

- **Tool**: Pylint
- **Error**: C0209 Formatting a regular string which could be an f-string (consider-using-f-string)
- **Location**: `src/reports.py:54-56` (`ReportBuilder.build`)
- **Fix**: Replace `%`-style formatting with f-strings.
- **Before**: `lines.append("total: %s" % self.book.total())`
- **After**: `lines.append(f"total: {self.book.total()}")`

### Issue 6

- **Tool**: Black / Pylint
- **Error**: C0410 Multiple imports on one line, plus two unused imports
  (multiple-imports, unused-import)
- **Location**: `src/models.py:1`
- **Fix**: Split the combined import and drop the unused `os` and `sys`
  imports (only `datetime` was actually used).
- **Before**: `import datetime, os, sys`
- **After**: `import datetime`

## 1. Issues Found

Running Pylint against the initial `src/` code (`pylint-report-before.txt`)
reported **46 issues** across the three modules, and rated the code
**6.13/10**. Grouped by category:

- **Documentation (23 issues)**: `missing-function-docstring` (16),
  `missing-class-docstring` (3), plus related naming hints.
- **Style/convention (13 issues)**: `invalid-name` (camelCase method names
  like `ToDict`/`totalByCategory`), `singleton-comparison`
  (`== None` instead of `is None`), `consider-using-f-string`,
  `multiple-imports`, `multiple-statements`, `wrong-import-order`,
  `line-too-long`, `no-else-return`, `simplifiable-if-statement`.
- **Correctness/robustness (7 issues)**: `dangerous-default-value` (a
  mutable list as a default argument), `bare-except` (swallowing *all*
  exceptions, including real bugs), `unspecified-encoding` and
  `consider-using-with` (file handles opened without a context manager or
  explicit encoding), `unused-import`/`unused-wildcard-import`,
  `wildcard-import`.

The single most common issue was missing docstrings, but the most
*important* issues were the small group of correctness bugs: the shared
mutable default (`expenses=[]`) meant every `ExpenseBook` created without
an explicit list would silently share the same underlying list, and the
bare `except:` in `ExpenseBook.add()` would hide programming errors (e.g.
a typo attribute access) as if the expense were simply invalid.

## 2. Benefits Observed

Static analysis caught real bugs that a quick manual read easily misses.
The mutable-default-argument bug in particular is a classic Python trap —
it doesn't look wrong at a glance, and it only manifests once two
`ExpenseBook` instances are used together and start polluting each
other's data. I doubt I would have caught it without running Pylint.
The bare `except` is similarly dangerous: it "worked" in testing because
no exception happened to occur, but it would have silently hidden future
bugs.

Setup took about 40 minutes total (installing pre-commit, black, isort,
and pylint; writing and tuning the `.pylintrc`; wiring the config into
`.pre-commit-config.yaml`; and matching the pinned pylint version between
the local venv and the pre-commit hook environment). Fixing the 46
reported issues took roughly another hour, most of which was manual
(renaming methods, rewriting the mutable-default and bare-except code,
adding docstrings) since Black and isort only auto-fixed formatting,
import order, and quote style. Given how quickly this setup would have
found the mutable-default bug in a larger, longer-lived project, the
time invested is small compared to the debugging time it would save.

## 3. Integration

For a team, I'd run these tools at three points:

- **IDE**: Black and isort configured as format-on-save, so nobody has to
  think about style.
- **Pre-commit**: the current hook set (whitespace/EOF/YAML/JSON checks
  plus Black, isort, and Pylint) runs on every commit, catching issues
  before they even reach a PR.
- **CI**: the same `pre-commit run --all-files` command re-run on every
  push/PR as a required check, since pre-commit hooks are opt-in locally
  and someone could always skip them with `--no-verify`.

## 4. Recommendations

Pylint was the most useful tool here because it caught actual logic
issues (the mutable default, the bare except), not just style. Black and
isort were valuable for removing bikeshedding around formatting entirely
— they auto-fixed a third of the reported issues with zero manual effort.

If I were configuring this for a longer-lived project, I would tune
`.pylintrc` further: raise `docstring-min-length` so tiny one-line
helpers don't need docstrings, and keep `too-few-public-methods` disabled
for small, intentionally single-purpose classes like `ReportBuilder`
rather than treating every such warning as something to fix. I would
absolutely use this setup (pre-commit + Black + isort + Pylint) in future
projects — the cost is low, it runs automatically, and it consistently
surfaces the kind of subtle bug that's easy to miss in review.
