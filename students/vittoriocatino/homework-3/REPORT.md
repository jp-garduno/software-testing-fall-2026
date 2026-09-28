# Static Testing Analysis Report

## Issues Found

I used a small in-memory task tracker because it has enough behavior to test
without hiding static-analysis results behind a framework. Before applying the
project configuration, I ran Pylint over the three source modules and the test
module. The first run reported **35 findings** and scored **7.52/10**. The
findings were intentionally concentrated in maintainability categories: four
missing module docstrings, four missing class docstrings, twenty-three missing
function or method docstrings, three lines over the configured 88-character
limit, and one redundant empty-list comparison. After adding the missing
documentation, Pylint exposed one follow-up warning for an unnecessary `pass`
statement in the documented exception class. Removing it produced a final
Pylint score of **10.00/10**.

The following fixes document more than the required five issues:

1. **Pylint C0114, `src/service.py:1`** — I added a module docstring that
   defines the service layer's responsibility.
2. **Pylint C0115, `src/models.py:11`** — I documented the `Task` data model
   so its state and purpose are clear to callers.
3. **Pylint C0116, `src/service.py:23`** — I added a docstring to
   `create_task` describing validation, storage, and the returned task.
4. **Pylint C0301, `src/service.py:10`** — I split the long `create_task`
   signature across lines using Black-compatible formatting.
5. **Pylint C0301, `test_task_service.py:5`** — I expanded the validation
   import into a parenthesized, sorted import block.
6. **Pylint C1803, `test_task_service.py:101`** — I replaced
   `normalise_tags(None) == []` with the clearer `not normalise_tags(None)`.
7. **Pylint W0107, `src/validation.py:7`** — After documenting the custom
   exception, I removed its now-unnecessary `pass` statement.

Black and isort then confirmed that formatting and imports were stable, while
Bandit found no security issues in `src/`. The fourteen automated tests pass
and exercise every executable source statement, yielding 100% measured source
coverage.

## Benefits Observed

Static testing caught problems that would not change the visible behavior of a
task being created or completed, but would make the project harder to maintain.
For example, missing documentation and very long lines do not fail unit tests;
they increase the time needed for another developer to understand a method.
The redundant comparison was also logically correct, yet the linter suggested a
more idiomatic and readable expression. A manual review could find these
issues, but a reviewer might reasonably focus on business logic and miss the
same repetitive documentation warnings across several modules.

The initial setup took longer than a single manual code read because it required
choosing tool versions, defining scope, and resolving the baseline warnings.
That cost is paid once. On later changes, the hooks provide feedback before the
code leaves the developer's machine, which is cheaper than discovering style,
import, or security problems during review or after merging. The automated
formatters are particularly useful because they remove subjective formatting
discussion from a pull request.

## Integration

I would use three layers in a team workflow. The IDE runs Black, isort, and
Pylint while code is being written so a developer receives immediate feedback.
The pre-commit hook repeats the essential formatting, linting, file hygiene,
and Bandit checks on changed files, preventing an accidental bad commit. The
included GitHub Actions workflow repeats the checks on pull requests so the
team does not depend on every contributor's local setup. Unit tests and
coverage run there as well, which keeps correctness feedback alongside static
analysis results.

## Recommendations

Pylint was most useful for explanatory warnings, Black and isort for making
the codebase mechanically consistent, and Bandit for adding a focused security
review. I would keep the current focused configuration rather than disable
large groups of warnings: only the `too-few-public-methods` rule is disabled
because a custom exception and an enum are intentionally small. In a larger
project, I would gradually add type checking and a documented complexity budget
after the team agrees on their value. I would use this workflow in future
projects because it makes the expected quality standard executable, repeatable,
and visible before code review begins.
