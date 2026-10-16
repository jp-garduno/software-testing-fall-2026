# Coverage Analysis — TaskFlow

Measured with `pytest -v --cov=src --cov-branch --cov-report=term-missing --cov-report=html`
(pytest 8.4.2, coverage.py 7.10.7, Python 3.9.6). Raw output: `screenshots/test-execution.txt`
and `screenshots/coverage-summary.txt`.

## Coverage Summary

| Metric             | Threshold | Achieved | Status  |
| ------------------ | --------- | -------- | ------- |
| Statement Coverage | 80%       | 100% (234/234) | ✅ Pass |
| Branch Coverage    | 80%       | 100% (78/78)   | ✅ Pass |
| Function Coverage  | 80%       | 100%           | ✅ Pass |
| Line Coverage      | 80%       | 100%           | ✅ Pass |

coverage.py has no separate "function coverage" figure. Function coverage is 100% because every
statement in every function body executes (a function with zero executed statements would show
misses); the same applies to line coverage, which for this code base equals statement coverage.

## Coverage by File

| File                    | Statements | Branches | Functions | Lines |
| ----------------------- | ---------- | -------- | --------- | ----- |
| task.py                 | 100% (70)  | 100% (22) | 100%     | 100%  |
| task_service.py         | 100% (103) | 100% (32) | 100%     | 100%  |
| task_repository.py      | 100% (38)  | 100% (16) | 100%     | 100%  |
| notification_service.py | 100% (23)  | 100% (8)  | 100%     | 100%  |

## Test Suite

130 tests, 0 failed, 0 skipped, full run in about 0.1–0.3 s.

| File                              | Tests | Purpose                                                      |
| --------------------------------- | ----- | ------------------------------------------------------------ |
| `test_task_unit.py`               | 43    | Task model in isolation (validation, transitions, overdue, priority) |
| `test_task_service_integration.py`| 37    | TaskService + repository workflows, mocked notifications     |
| `test_mocking.py`                 | 24    | Mocks, stubs, fakes, failure injection, interaction order    |
| `test_coverage_edge_cases.py`     | 26    | Branches of the gateway/repository the service tests mock away |

## Untested Code Paths

**None at statement or branch level** — the report lists no missed lines and no partial branches.

That does not mean everything is verified. What the suite deliberately does *not* exercise:

### Real infrastructure behind the injected collaborators

**What**: `TaskRepository` talks to whatever `database` object it is given, and
`NotificationService` to whatever `email_client` / `sms_client` it is given. The suite only ever
supplies a hand-written `FakeDatabase` or `Mock` objects.

**Reason**: no real database or SMTP/SMS provider exists in this project; a real one would be
covered by system or contract tests, not unit/integration tests.

**Risk**: Medium for a real deployment (the fake can disagree with a real database about ids,
ordering, or transactions); none for the logic under test here.

### Concurrency

**What**: two simultaneous updates to the same task (lost update, duplicate-title race between
`find_by_title` and `save`).

**Reason**: the duplicate check is check-then-act and is not atomic; white box coverage metrics
cannot reveal this because every line and branch is executed single-threaded.

**Risk**: Medium in a multi-user system; a unique constraint in the real database would be needed.

## Coverage Improvement Strategy

Coverage was measured after each stage rather than only at the end:

| Stage                                   | Statements+branches (TOTAL) | Notes |
| --------------------------------------- | --------------------------- | ----- |
| Unit tests only (43 tests, `task.py`)   | 100% of `task.py`           | Service, repository and gateway not imported yet |
| + integration tests (80 tests, all `src/`) | 88%                      | `notification_service.py` 16%, `task_repository.py` 93%, `task_service.py` 96% |
| + mocking and edge-case tests (130 tests)  | 100%                     | Final result |

### What closed the gaps

1. **Gateway branches (16% → 100%)** — the service tests mock `NotificationService`, so none of its
   own logic ran. Tests with a mocked *transport client* cover unconfigured client, empty
   recipient/phone number, success, and delivery failure for both email and SMS.
2. **Repository error wrapping** — a parametrized test makes the database raise for every operation
   and checks each is converted to `RepositoryError` with the original exception chained.
3. **Search filter branches** — one test per filter (status, priority, `due_from`, `due_to`, title)
   including undated tasks, inclusive date bounds and the no-filter case.
4. **Service decision points** — same-task vs different-task title detection (by identity, by id
   when the repository returns a copy, and a different task whose id is unset), atomic failed
   updates, description truncation.

### Do the tests catch bugs, or only execute lines?

Coverage proves code ran, not that assertions would notice a defect. As a spot check I applied
seven one-line mutations to a temporary copy of `src/` and ran the suite: `<=`→`<` in the due-date
check, `>`→`>=` in overdue detection, the archive rule, the SMS-for-urgent condition, removing
`save` on a status change, an exclusive `due_to` bound, and inverting the purge guard. All seven
were detected by at least one failing test. (The first attempt reported two survivors; that was
stale bytecode in the copy — `==`/`!=` mutations keep the file size identical — and disappeared
after deleting `__pycache__`.) This is a hand-picked sample, not a full mutation-testing run.

## Evidence

Screenshots were not captured as images: the work was done in a non-interactive terminal with no
GUI. Equivalent evidence is checked in as text:

- `screenshots/test-execution.txt` — full `pytest -v` output with per-file coverage table
- `screenshots/coverage-summary.txt` — compact coverage summary

The HTML report is regenerated with `pytest --cov=src --cov-branch --cov-report=html` and opened
from `htmlcov/index.html`; it is excluded from git as a build artifact.
