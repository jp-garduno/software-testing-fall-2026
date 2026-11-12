# Part 5: White Box Testing & Coverage Analysis Report

## 1. Coverage Metrics Achievement

To exceed the required thresholds of >85% statement coverage and >80% branch coverage, I followed a white box testing strategy driven by control-flow analysis. First, I wrote 15 isolated unit tests in `tests/test_task_unit.py` targeting every validation rule, state transition branch, overdue condition, and priority comparison in the `Task` model. Next, I implemented 12 integration and mocking tests in `tests/test_task_service_integration.py` using `pytest-cov` with `--cov-branch` enabled. Inspecting branch coverage early ensured that both `True` and `False` outcomes of every `if` statement in `Task` and `TaskService` were exercised, achieving 100% statement (126/126) and 100% branch (36/36) coverage.

## 2. Challenges in Reaching Coverage Goals

The primary challenge was covering implicit branches and error-handling paths rather than standard happy paths. For example, in `Task.is_overdue()`, short-circuit conditions for completed/archived tasks (`DONE`/`ARCHIVED`), missing `due_date` (`None`), and future vs. past timestamps create multiple decision branches. Similarly, in `TaskService.search_tasks()`, optional filter parameters (`status`, `priority`, `title_query`) each introduce two branches (filter applied vs. skipped). By designing targeted test cases that toggle each optional filter and test boundary states, all partial branches (`BrPart`) were eliminated without writing redundant tests.

## 3. Benefits of Mocking External Dependencies

Mocking `TaskRepository` and `NotificationService` with `unittest.mock.Mock(spec=...)` provided three decisive advantages:

1. **Execution Speed**: The entire 27-test suite executes in under 0.20 seconds because no real database connections or SMTP/SMS network requests are made.
2. **Deterministic Failure Simulation**: Using `side_effect`, I simulated database write failures and SMTP outages on demand to verify that `TaskService` aborts notifications when persistence fails, yet completes task creation gracefully when the email server fails.
3. **Behavioral Verification**: Assertions such as `assert_called_once_with` and `assert_not_called` verified exact component interactions at architectural boundaries.

## 4. Trade-offs Between Coverage and Test Quality

High code coverage is a useful diagnostic signal for finding untested branches, but coverage alone does not guarantee test quality; a test without meaningful assertions can execute lines of code without verifying correctness. While 100% coverage was achievable in this focused domain model, chasing 100% coverage in large production systems often yields diminishing returns when testing boilerplate or third-party adapters. Pairing structural branch coverage with strict behavioral assertions and interaction checks provided the right balance between metric completeness and fault detection.

## 5. Lessons Learned & Reflection

Working on TaskFlow highlighted how white box testing complements black box testing. While black box techniques (equivalence partitioning and boundary value analysis) helped design input validation tests for titles and due dates, white box control-flow inspection revealed internal branches—such as graceful notification fallback (`_notify_email`) and multi-filter combinations—that specification-only tests might miss. In future projects, I will enforce branch coverage thresholds in CI pipelines while prioritizing assertions on business invariants and boundary interactions.
