# White Box Testing & Coverage Analysis Report

## Coverage Metrics Achievement

TaskFlow reached its coverage goals through a control-flow-first test strategy. I started with the `Task` model because it contains the rules that every higher-level workflow depends on: title and due-date validation, priority ordering, overdue detection, and state transitions. Rather than checking only a happy path, the unit suite exercises both sides of each meaningful decision: short and oversized titles, past and future dates, valid and invalid transitions, active and terminal overdue states, and higher, lower, and equal priorities. This gives the model high statement and branch coverage while keeping every test independent.

The service layer then uses strict mocks for its repository and notification dependencies. That made it practical to test duplicate titles, missing records, database-save errors, notification-provider errors, soft deletion, status updates, overdue scans, and combined search filters. Tests verify both output and interaction: a duplicate task must not be saved or notified, while a successful creation must be persisted before notifications are attempted. This was the most effective strategy because otherwise these paths would require database records and external credentials.

## Challenges in Reaching Coverage Goals

The challenging areas were the defensive branches that happen only after a specific sequence of state changes. For example, an archived task must first be archived and then tested for an attempted update; similarly, a task must be placed in `DONE` before the invalid backward transition can be verified. Search also needs tasks with different statuses, priorities, dates, and titles so that each optional filter can be tested independently and in combination. Parametrization helped reduce repeated setup without hiding intent.

There are diminishing returns near complete coverage. Reaching every line can encourage tests that merely execute code without asserting useful behavior. I avoided that by naming each test after the business rule it proves and by checking effects such as persisted tasks, blocked side effects, changed timestamps, and notification contents.

## Benefits of Mocking External Dependencies

Mocking made the tests fast, deterministic, and safe. A real database or messaging service would introduce latency, credentials, network failures, and possible accidental emails or SMS messages. With `Mock(spec=...)`, a test can simulate a duplicate lookup, a repository outage, or an SMTP failure in one line and assert the service's response. The `spec` also prevents tests from silently calling methods that the interface does not provide.

Mocks do add responsibility: tests should not mirror private implementation details. The suite therefore verifies public outcomes and boundary interactions, not internal helper calls. In a production system I would complement these tests with a small number of integration tests against controlled infrastructure.

## Coverage Versus Test Quality and Lessons Learned

One hundred percent coverage is not automatically worth pursuing. It can be useful for a small, critical algorithm, but a percentage cannot prove that requirements are complete or that assertions are meaningful. A practical target is high coverage for business rules and error paths, paired with readable tests and risk-based scenarios. The main lesson is that white-box coverage is a diagnostic tool: it exposes unvisited decisions, while thoughtful assertions determine whether the tested behavior is actually correct.
