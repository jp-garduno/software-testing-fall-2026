# Coverage Analysis

Measured from `homework-5/` with:

```bash
pytest -v --cov=src --cov-branch --cov-report=term-missing --cov-report=html
```

**119 tests, all passing, full suite runs in about 0.4 s.**

## Coverage Summary

| Metric             | Threshold | Achieved | Status  |
| ------------------ | --------- | -------- | ------- |
| Statement Coverage | 80%       | 100%     | ✅ Pass |
| Branch Coverage    | 80%       | 100%     | ✅ Pass |
| Function Coverage  | 80%       | 100%     | ✅ Pass |
| Line Coverage      | 80%       | 100%     | ✅ Pass |

Raw numbers: 234 statements / 0 missed, 74 branches / 0 partial, 33 functions / 33 executed.
(coverage.py does not print a function percentage in the terminal; it was computed from
`coverage json`, which lists each function with its own summary.)

## Coverage by File

| File                    | Statements | Branches | Functions | Lines |
| ----------------------- | ---------- | -------- | --------- | ----- |
| task.py                 | 100% (66)  | 100% (22) | 100% (9)  | 100%  |
| task_service.py         | 100% (82)  | 100% (26) | 100% (12) | 100%  |
| task_repository.py      | 100% (58)  | 100% (18) | 100% (8)  | 100%  |
| notification_service.py | 100% (28)  | 100% (8)  | 100% (4)  | 100%  |

The Task model reaches 100% statement and branch coverage from the **unit tests alone**
(`pytest tests/test_task_unit.py --cov=src --cov-branch`), so the Part 1 requirement does
not depend on the integration tests.

## Untested Code Paths

None. No `# pragma: no cover` markers and no `omit` rules are used, so the number above
is not hiding anything.

Being honest about what 100% does **not** tell us:

- **The notification transport is a stub.** `NotificationService._deliver` is fully
  exercised, but only against a mocked `transport` callable. Nothing verifies that a real
  SMTP/SMS provider accepts the payload. That belongs in a contract or end-to-end test
  with a sandbox account. **Risk: medium**, because it is the only real external boundary.
- **The repository is only tested against an in-memory `dict`.** Its error wrapping is
  verified with doubles that raise `OSError`, but real database behaviour (transactions,
  concurrent writers, id generation) is out of scope. `_next_id` is not thread-safe.
  **Risk: medium** for production, none for this assignment.
- **Time is real.** Tests use `datetime.now()` with generous offsets (hours or days), so
  they cannot flake, but a frozen clock would let us test exact boundaries such as
  `due_date == now`. **Risk: low.**

## Coverage Improvement Strategy

The suite was built incrementally and coverage was measured after each stage:

| Stage (commit)                                  | Tests | Statement | task.py | task_service.py | task_repository.py | notification_service.py |
| ----------------------------------------------- | ----- | --------- | ------- | --------------- | ------------------ | ----------------------- |
| 1. Model + unit tests                           | 37    | 100% (only `task.py` existed) | 100% | n/a | n/a | n/a |
| 2. Service/repo/notifier added + integration tests | 61 | **67%**   | 100%    | 88%             | 20%                | 25%                     |
| 3. Mocking/error scenarios + edge cases         | 119   | **100%**  | 100%    | 100%            | 100%               | 100%                    |

### What the 67% run revealed

Reading `--cov-report=term-missing` after the integration tests showed exactly where the gaps were:

1. **`task_repository.py` (20%)**: the workflow tests mock the repository, so none of its
   own logic ran. Added `TestTaskRepository` and `TestRepositorySearch` against a real
   dict-backed repository, covering save/id assignment, exact title lookup, delete,
   every search filter and their combination.
2. **`notification_service.py` (25%)**: added tests for email/SMS delivery, address and
   phone validation, the missing-transport error, retry-then-succeed and give-up-after-
   `max_retries`.
3. **`task_service.py` (88%)**: the missing lines were the SMS channel
   (`create_task_with_sms`), the `except` blocks in `_notify_email`/`_notify_sms`, and one
   branch in `update_task` (`due_date=None`, which clears the due date). Covered with
   notification-failure tests and an explicit "clear due date" test.
4. **Error paths in the repository**: database failures are wrapped in `RepositoryError`;
   tested by injecting doubles whose `__setitem__`, `__contains__`, `get` and `values`
   raise `OSError`.

### Judgement calls

- Branch coverage was the real driver. Statement coverage reached 88% in the service
  while one `if` arm (`due_date is not None`) was still unvisited.
- I did not write tests that only call a function without asserting something about the
  result. Each added test checks a returned value, a state change or a mock interaction.

## Evidence

- `screenshots/coverage-summary.png`: terminal output with the table above.
- `screenshots/coverage-html-report.png`: the generated `htmlcov/index.html`
  (not committed; regenerate it with the command at the top).
- `screenshots/test-execution.png`: `pytest -v` run showing all tests passing.
