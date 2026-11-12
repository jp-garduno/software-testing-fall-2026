# Static Testing Report

**Student**: Emmanuel Arias (`yair91`)
**Project**: Inventory — stock control for a small warehouse
**Language**: Python

## 1. Issues Found

The first pylint run over `src/` reported **48 findings across 19 distinct
codes**, for a score of **6.10/10**. The full output is in
[`reports/pylint-before.txt`](reports/pylint-before.txt).

| Category | Findings | What they were |
| --- | --- | --- |
| Convention (C) | 35 | Missing docstrings, `.format()` where an f-string belongs, `addProduct` instead of `add_product`, two statements on one line, a 226-character line |
| Refactor (R) | 7 | `else` after `return`, iterating a dict by key instead of `.items()`, a constructor with six arguments, a class with no public methods |
| Warning (W) | 6 | Unused import, unused variable, bare `except`, `open()` without an encoding |

The most common finding was the missing docstring, 22 of the 48. That number
is loud but cheap: it says nothing about whether the code works.

**The three that were actual bugs**, not style:

**`tags=[]` as a default argument** (W0102). A list written as a default is
created once, when the function is defined, and then shared by every `Product`
built without tags. Tagging one product would have tagged all of them. This is
the kind of thing that survives code review because it looks completely
ordinary.

**A bare `except`** (W0702) in `Inventory.remove`. It was meant to catch a
missing key, and it also catches `KeyboardInterrupt`, `MemoryError` and any
typo inside the `try`. The method would have reported "product not found" for
problems that had nothing to do with the product.

**`sku == None`** (C0121), four times. It calls `__eq__`, so an object with a
permissive `__eq__` compares equal to nothing in particular. `is None` asks the
question that was meant.

## 2. Benefits Observed

**The formatters barely moved the needle.** Running black and isort took the
score from 6.10 to **6.26**. They fixed spacing and the two-statements-per-line
cases and nothing else. Everything that mattered — the shared list, the bare
except, the unused import — needed a human decision. That is a useful thing to
learn early: auto-formatting is not static analysis, it only makes the code
look consistent.

**Would review have caught these?** The naming, the long line and the missing
docstrings, yes, immediately. The mutable default argument, honestly, no. I
have read that code several times and it reads fine. A linter does not get
bored, and that is its real advantage over a reviewer on their fourth file of
the afternoon.

**Setup time against time saved.** The configuration took about forty minutes,
most of it on the problems in section 3. Each later run is under two seconds,
and it caught three real bugs on the first one.

**Security linting**, added as bonus, found nothing: bandit reports 0 issues
over 122 lines. A clean result is also information.

## 3. Integration

The three tools belong at three different moments, and the mistake is running
all of them everywhere:

- **Editor**: black and isort on save. Formatting should never be something a
  person thinks about or argues about in a review.
- **Pre-commit**: the fast checks — whitespace, end of file, valid YAML and
  JSON, no private keys, no large files — plus pylint and bandit scoped to
  `src/`. The whole hook set runs in about two seconds, which is the budget
  before people start using `--no-verify`.
- **CI**: the same checks over every file, not only the changed ones.
  Pre-commit can be skipped with `--no-verify`; CI cannot. That is what
  `ci/static-analysis.yml` is for.

**Three configuration problems I only found by running it.** The first version
of the hooks looked correct and was not:

1. `black` reformatted to 88 columns instead of 120. Pre-commit runs from the
   git root, so black never saw the `pyproject.toml` in this folder. Fixed by
   passing `--line-length=120` in the hook arguments.
2. The pylint and bandit hooks silently skipped everything. Their filter was
   `^src/.*\.py$`, anchored at the repo root, and this project lives in a
   subdirectory. Fixed with `(^|/)src/.*\.py$`. A hook that skips reports
   "Passed", which is worse than failing.
3. Running `pre-commit run --all-files` from the root of the course repository
   reformatted 642 files belonging to other people. Nothing was committed, but
   the lesson stands: pre-commit's scope is the repository, not the folder you
   are standing in.

## 4. Recommendations

**Most useful tool: pylint**, by a distance. Black is pleasant and saves
arguments, but it cannot tell you that a default argument is shared.

**What I would change in the configuration.** Nothing is disabled in
`.pylintrc`, and I would keep it that way. The one setting I did relax,
`min-public-methods = 1`, is written down with its reason: `Product` and
`Movement` hold data, and forcing a second method on them would push logic
into the wrong class. A rule turned off without a reason comes back later as a
bug.

**Would I use this again?** It is already in my homework 4 and 7 submissions,
where the same configuration keeps both at 10.00/10. What transfers is not the
tool but the habit of running it before the commit instead of after the
review.
