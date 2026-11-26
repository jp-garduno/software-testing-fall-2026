# Coverage Analysis

Command: `pytest -v --cov=src --cov-branch --cov-report=term-missing --cov-report=html` (coverage.py 7.10, Python 3.9).

## Coverage Summary

| Metric             | Threshold | Achieved | Status  |
| ------------------ | --------- | -------- | ------- |
| Statement Coverage | 80%       | 100%     | ✅ Pass |
| Branch Coverage    | 80%       | 100%     | ✅ Pass |
| Function Coverage  | 80%       | 100%     | ✅ Pass |
| Line Coverage      | 80%       | 100%     | ✅ Pass |

## Coverage by File

| File                    | Statements | Branches | Functions | Lines |
| ----------------------- | ---------- | -------- | --------- | ----- |
| task.py                 | 100% (58)  | 100% (20) | 100%     | 100%  |
| task_service.py         | 100% (96)  | 100% (38) | 100%     | 100%  |
| task_repository.py      | 100% (13)  | n/a      | 100%      | 100%  |
| notification_service.py | 100% (5)   | n/a      | 100%      | 100%  |
| **Total**               | 100% (172) | 100% (58) | 100%     | 100%  |

## Untested Code Paths

None: every statement and every branch in `src/` is executed. Coverage.py reports 0 missed statements and 0 partial
branches. Two caveats worth stating honestly:

- **`TaskRepository` and `NotificationService` are interfaces.** Their methods only raise `NotImplementedError`, and
  `test_real_interfaces_must_be_mocked` just checks that. 100% on those two files says nothing about a real database or
  email/SMS provider, which would need their own integration tests against real infrastructure.
- **Covered is not the same as verified.** Time-dependent code (`datetime.now()`) is exercised with offsets of days, so
  the exact boundary (`due_date == now`) is not deterministic and is not asserted.

## Screenshots

- `screenshots/test-execution.png`: verbose test run (rendered from the captured terminal output)
- `screenshots/coverage-summary.png`: terminal coverage table (rendered from the captured terminal output)
- `screenshots/coverage-html-report.png`: capture of the generated `htmlcov/index.html`

## How Coverage Goals Were Achieved

### Initial coverage

I wrote the tests together with the code, branch by branch, so there was no separate low-coverage baseline to report.
The first full run with `--cov-branch` already showed 100%; the extra tests in `test_coverage_edge_cases.py` were
added afterwards to pin down boundaries and filters rather than to close gaps.

### Strategy applied

1. **Unit tests per branch of `Task`**: title boundaries (2/3/100/101 characters, empty, `None`), past/future due date,
   every transition pair via parametrization (including all four targets out of ARCHIVED), and each short-circuit in
   `is_overdue`.
2. **Integration tests per service rule**: duplicate title, not-found, invalid transition, archived-is-frozen, search
   filters one by one and combined, date range with open ends, tasks without a due date.
3. **Mock `side_effect` for failure branches**: repository errors propagate (no notification sent); email and SMS
   errors are logged and swallowed.
4. **`test_coverage_edge_cases.py`** for boundary and filter edge cases.

### Final coverage

100% statements / 100% branches with 74 tests, running in about 0.4 seconds.
