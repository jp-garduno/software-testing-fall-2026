# TaskFlow Coverage Analysis

## Coverage Summary

Coverage was measured with `coverage.py` 7.16.2 using branch tracing and all
64 tests. The required 80% thresholds are exceeded.

| Metric             | Threshold |       Achieved | Status |
| ------------------ | --------: | -------------: | ------ |
| Statement coverage |       80% | 100% (227/227) | Pass   |
| Branch coverage    |       80% |   100% (92/92) | Pass   |
| Function coverage  |       80% |   100% (27/27) | Pass   |
| Line coverage      |       80% |           100% | Pass   |

Function coverage counts each non-empty production function reported in the
coverage JSON and verifies that the function executed at least one statement.

## Coverage by File

| File                          |   Statements |     Branches |    Functions |
| ----------------------------- | -----------: | -----------: | -----------: |
| `src/task.py`                 | 100% (80/80) | 100% (40/40) |   100% (7/7) |
| `src/task_repository.py`      | 100% (44/44) | 100% (22/22) |   100% (7/7) |
| `src/task_service.py`         | 100% (97/97) | 100% (30/30) | 100% (11/11) |
| `src/notification_service.py` |   100% (6/6) |   100% (0/0) |   100% (2/2) |

## Untested Code Paths

No production statements or branches were untested in the measured run. The
real database and notification-provider integrations are deliberately outside
this exercise: the repository uses in-memory storage, and notification
delivery is represented by a boundary that reports an unconfigured provider.
Tests verify those boundaries and simulate repository and notification
failures with `unittest.mock`; no network, database, or filesystem service is
needed.

## Coverage Improvement Strategy

The first measured run reached 93.8% statement coverage and 92.4% branch
coverage. The remaining gaps exposed unvisited timezone mismatch checks,
validation paths in field updates, and SMS failure handling. Focused tests
were added for each condition, including both aware/naive datetime mismatch
directions, valid and invalid updates, and notification failure behavior.
The final run covered all 227 statements and all 92 branch destinations.

## Evidence

- [Coverage summary screenshot](./screenshots/coverage-summary.png)
- [HTML source report screenshot](./screenshots/coverage-html-report.png)
- [Test execution screenshot](./screenshots/test-execution.png)

The generated interactive HTML report is available at `htmlcov/index.html`
after running the coverage commands in the project README. The generated
`htmlcov/` directory and `.coverage` data file are intentionally not committed.
