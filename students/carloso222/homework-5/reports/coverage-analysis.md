# Coverage Analysis — TaskFlow

Command used (same flags as the grading system):

```bash
pytest -v --cov=src --cov-branch --cov-report=html --cov-report=term-missing
```

Tool: coverage.py 7.x through pytest-cov. Python 3.11+.

## Coverage Summary

| Metric             | Threshold | Achieved         | Status  |
| ------------------ | --------- | ---------------- | ------- |
| Statement Coverage | 80%       | 100% (247 / 247) | ✅ Pass |
| Branch Coverage    | 80%       | 100% (70 / 70)   | ✅ Pass |
| Function Coverage  | 80%       | 100% (38 / 38)   | ✅ Pass |
| Line Coverage      | 80%       | 100%             | ✅ Pass |

Function coverage was read from coverage.py's JSON report (`files[*].functions`):
every function and method in `src/` executes at least once.

## Coverage by File

| File                    | Statements | Branches  | Functions | Lines |
| ----------------------- | ---------- | --------- | --------- | ----- |
| task.py                 | 100% (98)  | 100% (34) | 100% (13) | 100%  |
| task_service.py         | 100% (78)  | 100% (20) | 100% (12) | 100%  |
| task_repository.py      | 100% (34)  | 100% (8)  | 100% (10) | 100%  |
| notification_service.py | 100% (29)  | 100% (8)  | 100% (3)  | 100%  |
| errors.py               | 100% (8)   | —         | —         | 100%  |

## Untested Code Paths

There are no uncovered statements or branches, and nothing is excluded with
`# pragma: no cover`. Two limits of the metric are still worth documenting,
because "100%" does not mean "every path":

### task_repository.py — `_matches()` (compound boolean conditions)

```python
return (
    (status is None or task.status == status)
    and (priority is None or task.priority == priority)
    and _in_date_range(task.due_date, due_from, due_to)
    and (not title_contains or title_contains.lower() in task.title.lower())
)
```

**Reason**: coverage.py measures branches between _lines_, not the
short-circuit outcomes inside one `and`/`or` expression. This function would
show 100% after a single call. It is not a measured gap, but it is a real one,
so each sub-condition has its own test in `TestRepositorySearch` (status only,
priority only, `due_from` only, `due_to` only, both dates, partial title, all
combined, no match). That is condition coverage done by hand.

**Risk**: Low — every condition is exercised in both directions.

### Real infrastructure (`TaskRepository` database, SMTP/SMS clients)

**Reason**: the production database client and the email/SMS providers are
not part of `src/`; they are injected. Their real behaviour (network timeouts,
retries, provider limits) belongs to system / end-to-end tests with real
infrastructure. Here their failures are simulated with `side_effect`
(`TimeoutError`, `ConnectionError`, `OSError`) and the wrapping into
`RepositoryError` / `NotificationError` is verified.

**Risk**: Medium for production, out of scope for unit/integration tests.

## Screenshots

| File                                         | Shows                                                                                                                                   |
| -------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `screenshots/coverage-summary.png`           | Terminal output: statement + branch coverage per file                                                                                   |
| `screenshots/coverage-html-report.png`       | HTML report index (100% statements and branches)                                                                                        |
| `screenshots/coverage-html-task-service.png` | HTML view of `task_service.py`, all lines covered                                                                                       |
| `screenshots/coverage-gaps-before.png`       | HTML view of `task_service.py` **before** the mocking tests: red (missed) and yellow (partial) lines in the notification error handlers |
| `screenshots/test-execution.png`             | `pytest -v` — 133 tests passing in ≈ 0.3 s                                                                                              |

## How Coverage Goals Were Achieved

The suites were written in order and coverage was measured after each one.
These are the real numbers from those runs (statement + branch, `--cov-branch`):

| Run | Test files included   | Tests | Total coverage | task_service | task_repository | notification_service |
| --- | --------------------- | ----- | -------------- | ------------ | --------------- | -------------------- |
| 1   | unit                  | 56    | 57%            | 19%          | 29%             | 24%                  |
| 2   | + integration         | 85    | 87%            | 92%          | 90%             | 24%                  |
| 3   | + mocking             | 100   | 90%            | 100%         | 90%             | 24%                  |
| 4   | + coverage edge cases | 133   | **100%**       | 100%         | 100%            | 100%                 |

### Initial coverage: 57%

Unit tests alone covered `task.py` at 100% (statements and all 34 branches)
but almost nothing else, which is expected: they test the model in isolation.

### Strategy applied

1. **Boundary values for every validation rule** (titles of 2/3/100/101
   characters, whitespace-only titles, descriptions of 500/501, due date equal
   to "now"). This took the model to 100% branch coverage in run 1.
2. **Integration tests with mocked repository and notifier** for every use
   case and business rule (duplicates, invalid transitions, archive rules,
   overdue) → `task_service.py` from 19% to 92%.
3. **Error-path tests with `side_effect`** (run 3). The report from run 2
   (`coverage-gaps-before.png`) showed lines 114-116 and 124-126 — the
   `except` blocks that swallow notification failures — and the partial
   branch `if not self.phone_number` never taking its `True` side. Tests for
   SMTP/SMS failures and for a service without a phone number closed them →
   `task_service.py` 100%.
4. **Repository and notifier internals** (run 4). The run-3 report still
   showed `_in_date_range` lines 74/76 (no date filter / task without due
   date) and the whole `NotificationService` untested, since the service
   always used a mock of it. `test_coverage_edge_cases.py` added a fake
   database with four representative tasks, one test per filter, database
   failures for every CRUD operation, and validation tests for email
   addresses, phone numbers and SMS truncation at exactly 160 characters.

### Final coverage: 100%

Total 133 tests; 48 were added after run 2 specifically to target branches
the report marked as missed or partial.
