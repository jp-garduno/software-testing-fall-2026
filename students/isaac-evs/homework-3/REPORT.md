# Static Testing Analysis Report

## 1. Issues Found

Running `pylint` against the original, unformatted `src/` directory (see `pylint-report-before.txt`) surfaced **36 issues** and rated the code at **6.51/10**. The issues fell into a handful of clear categories:

- **Missing docstrings** (`C0114`, `C0115`, `C0116`) — every module, class, and function was missing a docstring. This was by far the most common category, accounting for roughly 20 of the 36 findings.
- **Unused imports** (`W0611`) — `calculator.py` imported `os`, `math`, and `typing.List` without ever using them, a classic copy-paste leftover.
- **Real correctness/style risks**, not just cosmetic noise:
  - A bare `except:` clause in `divide()` (`W0702`) that would silently swallow *any* exception, not just `ZeroDivisionError`.
  - A mutable default argument `numbers=[]` in `average()` (`W0102`) — a well-known Python footgun where the default list is shared across calls and can accumulate state unexpectedly.
  - Singleton comparisons like `t.done == False` and `t.done == True` (`C0121`) in `task_manager.py`, which are non-idiomatic and slightly slower than `not t.done` / `t.done`.
  - An unused parameter on `calculate_percentage()` that existed purely to test line-length rules and had no real purpose (`W0613`).
  - A line exceeding the configured 100-character limit (`C0301`).

Running `black` and `isort` separately (before touching any logic) reformatted all three source files — mostly normalizing quote style, wrapping long argument lists across multiple lines, and adding blank-line spacing between functions, none of which pylint flags directly but which materially improved readability.

## 2. Benefits Observed

Static testing caught several things a quick manual read-through likely would have missed. The bare `except:` clause, for instance, looks harmless on a fast read of `divide()` — it "just handles errors" — but pylint immediately flagged it as a code smell because it would also mask bugs like a `TypeError` from passing a string instead of a number, making debugging much harder later. Similarly, the mutable default argument in `average()` is a subtle bug pattern that doesn't fail any of my existing tests today, but would silently misbehave the moment someone called `average()` without an argument multiple times expecting an empty list each time. A manual review focused on "does this look right" would very plausibly pass both of these without a second thought, since the code runs and produces correct output under normal test inputs.

Setup itself took under 30 minutes total: generating `.pylintrc`, writing `.pre-commit-config.yaml`, and running `black`/`isort`/`pylint` for the first pass. Fixing the flagged issues (adding docstrings, replacing the bare except, fixing the default argument, removing unused imports, and fixing the singleton comparisons) took another 20–30 minutes. Given that even one of these bugs (the mutable default, or the swallowed exception) could cause a genuinely confusing production incident and hours of debugging down the line, the time investment is clearly worth it — especially since it's a one-time setup cost that pays off on every future commit automatically.

## 3. Integration

For a team project, I would integrate these tools at three levels:

- **IDE**: Configure `black` and `pylint` as on-save/on-type integrations (e.g., VS Code's Python extension) so developers see issues immediately while writing code, before they even attempt to commit.
- **Pre-commit hook**: Exactly as configured here — `pre-commit install` on every developer's machine ensures formatting and linting issues are caught locally before a commit is even created, keeping the shared history clean and preventing "fix formatting" commits from cluttering the log.
- **CI pipeline**: Run `pylint`, `black --check`, and `isort --check` (non-mutating checks) as a required GitHub Actions job on every pull request, as a safety net in case someone bypasses their local hooks (e.g., with `--no-verify`) or has an outdated local environment. CI should fail the build if these checks don't pass, not just warn.

## 4. Recommendations

`black` was the most immediately useful tool — it requires zero configuration decisions (it is deliberately opinionated) and eliminates entire categories of bikeshedding arguments about formatting in code review. `pylint` was the most valuable for catching actual latent bugs (the bare except and mutable default), not just style. `isort` was useful but lower-impact on a project this small.

If I were to change the configuration, I would relax a few of pylint's stricter default conventions for a team setting — for example, `missing-function-docstring` on every single test function is arguably excessive, since well-named test functions are often self-documenting, and I would consider disabling that specific check for `test_*.py` files via a per-file override rather than a global one.

I would absolutely use this setup in future projects. The combination of automatic formatting (no manual style debates), automatic import sorting, and static analysis catching real bugs before they ship is a very high return for a relatively small, one-time setup cost — and pre-commit hooks mean the whole team benefits without needing to remember to run these tools manually.
