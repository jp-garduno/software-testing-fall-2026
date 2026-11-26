# Static Analysis Report — NEWS2 Early-Warning Scorer

**Student**: Pablo Portillo
**Project**: Kadu Care NEWS2 Early-Warning Scorer (Python)
**Baseline**: Pylint 6.71/10 · **After fixes**: Pylint 10.00/10 · 28 tests passing

---

## 1. Issues Found

The first Pylint run over `src/` reported **46 findings across three files**, plus one
configuration error in my own `.pylintrc` (`E0015: Unrecognized option found: suggestion-mode`) —
a useful reminder that the linter also lints the linter's setup. Black wanted to reformat 3 of the
7 files and isort disagreed with the import order in 2 of them.

Grouped by category, the distribution was:

| Category | Count | Representative codes |
| --- | --- | --- |
| Documentation | 19 | `C0114`, `C0115`, `C0116` missing module/class/function docstrings |
| Style & convention | 13 | `C0301` line too long, `C0103` invalid name, `C0411` import order |
| Correctness risk | 6 | `W0102` mutable default, `W0702` bare except, `W1514` no encoding |
| Simplification | 6 | `R1705`/`R1720` else-after-return, `R1716`, `C0206` |
| Dead code | 4 | `W0611` unused imports, `W0612` unused variable |

The single most common message was `C0116` (missing function docstring, 14 occurrences), followed
by `C0121` (`== None` instead of `is None`, 6 occurrences). That ranking is telling: the bulk of
what a linter finds is not bugs, it is *consistency debt* — the kind of thing a reviewer gets
bored of pointing out by the third file.

## 2. Benefits Observed

One finding was a genuine defect rather than a style complaint. `W0102: Dangerous default value []
as argument` flagged `PatientRecord.__init__(self, patient_id, name, history=[])`. Python evaluates
that default **once**, at function definition, so every patient record created without an explicit
history would have shared the *same* list object — one patient's vital signs appearing in another
patient's chart. In the clinical domain this module models, that is a patient-safety bug, not a
nit. I fixed it (`history=None` plus `list(history) if history else []`) and added a regression
test, `test_records_do_not_share_history`, which fails against the original code and passes now.

Would manual review have caught it? Possibly — but it is exactly the kind of defect that hides in
a plausible-looking signature, and my own test suite did not cover it until the linter told me
where to look. `W0702: bare except` was similarly valuable: the original `except:` around
`float(value)` would have swallowed `KeyboardInterrupt`, masking a problem instead of reporting it.

On time: configuring pre-commit, Pylint, Black, isort and Bandit took me roughly 50 minutes,
including reading documentation. Applying the fixes took about 40 more. Against that, Black and
isort now resolve every formatting argument automatically and permanently, and the hooks run in
under ten seconds per commit. On a team of five, a single avoided round-trip of "please fix the
import order" per pull request pays the setup back within the first week.

## 3. Integration

I would run each tool at the stage where feedback is cheapest:

- **IDE (on save)** — Black and isort as format-on-save. The developer never sees a formatting
  diff, because the file is already correct before it is staged.
- **Pre-commit (on commit)** — file hygiene, Black, isort, Pylint and Bandit on *changed files
  only*, plus `conventional-pre-commit` validating the commit message. Fast, local, and it keeps
  broken style out of history rather than fixing it later.
- **CI (on pull request)** — the same hooks with `--all-files`, so a contributor who skipped the
  local install cannot bypass the gate. CI is the enforcement point; pre-commit is the convenience
  point. This is the workflow I added in the accompanying GitHub Actions job.

The rule I would put in the team style guide is that **CI must run exactly what pre-commit runs**.
If they drift, developers stop trusting the local hooks and start using `--no-verify`.

## 4. Recommendations

The most useful tool was Pylint, by a wide margin — it was the only one that found an actual
defect. Black was the most *valuable per minute spent*: zero configuration, zero debate, done.
Bandit found nothing in this codebase, which is the correct result for a module with no I/O beyond
one JSON read, but it costs nothing to keep in place for when that changes.

The configuration change I would make is on scope. I disabled only `too-few-public-methods` and
`duplicate-code`, and I would keep that discipline: disabling rules in bulk turns a 10.00/10 score
into a number that means nothing. If a rule genuinely does not fit, I would rather disable it
inline at the single site with a comment explaining why, so the exception stays visible.

Yes, I will use this in future projects, and I intend to add it to my team project this semester.
The strongest argument is not the tidy formatting — it is that a two-character default argument
would otherwise have shipped, and no amount of manual review discipline scales the way a hook
running on every commit does.

---

## Appendix — Issues Fixed (Part 4)

### Issue 1

- **Tool**: Pylint
- **Error**: `W0102: Dangerous default value [] as argument (dangerous-default-value)`
- **Location**: `src/patient_record.py:7`
- **Fix**: Use `None` as the sentinel and build a fresh list per instance, so records cannot share
  one history object. Covered by `test_records_do_not_share_history`.
- **Before**:

  ```python
  def __init__(self, patient_id, name, history = []):
      self.history = history
  ```

- **After**:

  ```python
  def __init__(self, patient_id, name, history=None):
      """Create a record, optionally seeded with an existing history."""
      self.history = list(history) if history else []
  ```

### Issue 2

- **Tool**: Pylint
- **Error**: `W0702: No exception type(s) specified (bare-except)`
- **Location**: `src/vitals.py:29`
- **Fix**: Catch only the conversion errors `float()` can raise, so `KeyboardInterrupt` and
  `SystemExit` are no longer swallowed.
- **Before**:

  ```python
  try:
      value = float(value)
  except:
      errors.append("non numeric value for field: " + field)
  ```

- **After**:

  ```python
  try:
      value = float(value)
  except (TypeError, ValueError):
      errors.append("non numeric value for field: " + field)
  ```

### Issue 3

- **Tool**: Pylint
- **Error**: `C0121: Comparison 'value == None' should be 'value is None' (singleton-comparison)`
  — 6 occurrences across `vitals.py` and `patient_record.py`
- **Location**: `src/vitals.py:24`, `src/patient_record.py:14,42,52`
- **Fix**: Compare singletons by identity. `==` invokes `__eq__`, which a custom object can
  override to return `True` against `None`; `is` cannot be fooled.
- **Before**:

  ```python
  if value == None:
  ```

- **After**:

  ```python
  if value is None:
  ```

### Issue 4

- **Tool**: Pylint
- **Error**: `C0301: Line too long (206/120) (line-too-long)` — 3 occurrences
- **Location**: `src/patient_record.py:54`, `src/patient_record.py:18`, `src/vitals.py:34`
- **Fix**: Replace string concatenation with f-strings split over multiple lines. Shorter *and*
  readable, rather than merely shorter.
- **Before**:

  ```python
  return "Patient " + self.name + " (" + self.patient_id + ") scored " + str(last["score"]) + " on NEWS2, risk " + last["risk"] + ", trend " + self.trend() + ", monitoring " + last["monitoring"] + "."
  ```

- **After**:

  ```python
  who = f"Patient {self.name} ({self.patient_id})"
  return (
      f"{who} scored {last['score']} on NEWS2, risk {last['risk']}, "
      f"trend {self.trend()}, monitoring {last['monitoring']}."
  )
  ```

### Issue 5

- **Tool**: Pylint
- **Error**: `W0611: Unused import sys` / `Unused Dict imported from typing` / `Unused import math`,
  and `W0612: Unused variable 'unused'`
- **Location**: `src/news2.py:2`, `src/vitals.py:3-4`, `src/vitals.py:42`
- **Fix**: Delete the dead imports and the leftover `os.getcwd()` call. Removing `sys` also cleared
  `C0411: wrong-import-order` for free.
- **Before**:

  ```python
  import json
  import os
  from typing import Dict
  import math
  ...
      unused = os.getcwd()
  ```

- **After**:

  ```python
  import json
  ```

### Issue 6

- **Tool**: Pylint
- **Error**: `C0103: Variable name "Total" doesn't conform to snake_case naming style
  (invalid-name)` and `C0206: Consider iterating with .items()`
- **Location**: `src/news2.py:35,44-45`
- **Fix**: Rename to `total` and replace the manual accumulation loop with `sum()`.
- **Before**:

  ```python
  Total = 0
  for k in breakdown:
      Total = Total + breakdown[k]
  return Total, breakdown
  ```

- **After**:

  ```python
  total = sum(breakdown.values())
  return total, breakdown
  ```

### Issue 7

- **Tool**: Pylint
- **Error**: `W1514: Using open without explicitly specifying an encoding (unspecified-encoding)`
- **Location**: `src/vitals.py:54`
- **Fix**: Pin UTF-8 so the module reads the same file identically on every platform, instead of
  inheriting the machine's locale.
- **Before**:

  ```python
  with open(path) as f:
  ```

- **After**:

  ```python
  with open(path, encoding="utf-8") as f:
  ```

### Issue 8

- **Tool**: Black and isort
- **Error**: `would reformat` (3 files) and out-of-order imports (2 files)
- **Location**: `src/news2.py`, `src/patient_record.py`, `test_news2.py`
- **Fix**: Ran `isort --profile=black --line-length=120` then `black --line-length=120`. No manual
  edits — this is the category of issue that should never consume a human reviewer's attention.
