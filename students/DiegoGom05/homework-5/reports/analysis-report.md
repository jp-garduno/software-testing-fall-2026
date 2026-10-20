# White Box Testing & Coverage Analysis Report

## Coverage Metrics Achievement

I reached 100% statement and branch coverage (176 statements, 54 branches) with 119 tests. The most effective strategy was designing tests directly from the code's decision points: I listed every `if` in `Task` and `TaskService` and wrote at least one test for each outcome. Parametrized tests were very efficient for status transitions and priority comparisons. The hardest code to cover was `search_tasks`, where every filter has its own branches (filter absent, filter present, task without due date), and the exception handlers in the notification helpers, which only run when a dependency fails and therefore need `side_effect` mocks.

## Challenges in Reaching Coverage Goals

The first obstacle was the interface stubs: every `raise NotImplementedError` counted as an uncovered line until I wrote tests asserting that behavior. A second one was a requirement gap: one required test says a notification failure must not break the workflow, while the sample service did not catch exceptions, so I had to design a `try/except` wrapper and log the failure. I also lost time with a broken pip launcher in my Windows virtual environment, solved by using `python -m pip`. Diminishing returns were clear: roughly the first 90% came from the unit and integration tests, while the last 10% required many small tests that mostly confirmed behavior that was already obvious.

## Benefits of Mocking External Dependencies

Mocking made the suite fast and deterministic, with no database or SMTP server needed. Isolation means a failing test points to one component. The biggest benefit was error injection: simulating "Database connection failed" or "SMTP server unavailable" takes one line with `side_effect`, while reproducing it against real services would be almost impossible. Using `Mock(spec=...)` also caught typos in method names. Without mocking, the repository and notification classes would need real implementations just to run a test. Mocks did add maintenance cost, since they must stay aligned with the real interface, so I complemented them with a fake in-memory repository that checks the full workflow with real behavior instead of scripted return values.

## Trade-offs Between Coverage and Test Quality

100% coverage does not prove the code is correct: a test with no assertions still counts. Some of my tests, like the ones verifying `NotImplementedError`, exist mainly to cover lines; they document the interface contract but would not find real bugs. To keep quality high, I asserted on state and interactions (call arguments, call order, "no notification if save fails") rather than only executing code. For a small core of business logic like this, 100% is reasonable. As a general target, I would prefer around 85-90% plus other signals such as mutation testing.

## Lessons Learned About White Box Testing

What surprised me was how much branch coverage reveals beyond statement coverage: a line can run while one of its outcomes never does. Designing the code with dependency injection made mocking trivial, which taught me that testability is a design property. Next time I would apply TDD more strictly, writing the test before each method, and enable `--cov-branch` from the first run. In future projects I will use coverage reports to find forgotten scenarios, not as a score to maximize.
