# White Box Testing & Coverage Analysis Report

## Executive Summary

I built TaskFlow (a Task model, a TaskService, and two interfaces for persistence and notifications) and tested it
white box. The suite has 74 tests, reaches 100% statement and branch coverage, and runs in about half a second.

## Coverage Metrics Achievement

I worked from the code, not from the requirements list. For each `if` I wrote down both outcomes and made sure a test
forced each one. The unit tests on `Task` took it to full coverage quickly. Parametrization was the most effective tool:
one test body over every status pair covered all the transition branches at once. The hardest code to reach was the
`except` blocks around notifications, because normal runs never raise there; they only execute when a mock is configured
with `side_effect`. The compound filter in `search_tasks` (status, priority, date range, title) was second hardest, since
each `continue` is its own branch.

## Challenges in Reaching Coverage Goals

The main obstacle was time. `is_overdue` and due-date validation depend on `datetime.now()`, and the model rejects past
due dates at creation, so an overdue task cannot be built through the constructor. I solved it by assigning `due_date`
after construction in the test, which is a small white box shortcut that a black box test could not take. Reaching 100%
was easy here only because the system is small; the last few branches (empty filters, same-title update) each cost a test
that protects very little. Returns diminished well before 100%.

## Benefits of Mocking External Dependencies

Mocking made the suite fast, deterministic, and able to simulate failures (SMTP down, database error) that I could not
trigger otherwise. With `Mock(spec=...)` a typo in a method name fails the test instead of silently passing. Without
mocks I would need a database and an email provider just to run the suite, and every run would send notifications. It
also made some tests harder to write: you must understand exactly which calls the service makes, and a test can pass
while the real adapter is broken. The fake repository was a good middle ground: it checks behavior across several calls
without asserting individual interactions.

## Trade-offs Between Coverage and Test Quality

Coverage tells you which code ran, not whether anything checked the result. A test with no assertions would still raise
the number. I tried to keep every test asserting an outcome (state, raised error, or exact mock calls), including that
nothing was saved or sent on failure paths. A few tests, such as the one confirming the interfaces raise
`NotImplementedError`, exist mostly to cover trivial code and I treat them as low value. I think 100% is reasonable on a
small codebase like this, but on a real system I would aim for roughly 85-90% and spend the remaining effort on
boundary values and integration with real infrastructure.

## Lessons Learned

What surprised me is how much the design affects testability: passing the repository and notifier into `TaskService`
meant I never had to patch anything. A design decision I made while testing was catching notification errors in the
service, because the spec says a failed notification must not break the workflow. Next time I would write the failing
test first and check mutation testing, since mutation score would measure test quality in a way line coverage cannot.
I will use coverage as a way to find untested branches, not as a target to display.
