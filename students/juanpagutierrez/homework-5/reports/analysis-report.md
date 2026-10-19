# White Box Testing & Coverage Analysis Report

## Executive Summary

TaskFlow's 142-test suite reaches 100% statement and branch coverage in about
0.3 seconds, mostly thanks to design decisions made before any test.

## Coverage Metrics Achievement

I measured after each suite. Unit tests alone gave 50%: the `Task` model was
fully covered, but the other three modules were barely touched. Integration
tests with a mocked repository took the total to 76%, and the mocking suite
took it to 90%. The last 10% came from reading the `BrPart` (partial branch)
column rather than the overall percentage. It pointed to specific conditions,
such as date-range filters, that had only ever been evaluated one way.

The most effective strategies were boundary values (titles of 2, 3, 100 and
101 characters; a due date exactly equal to "now") and a parametrized table
of status transitions. The hardest code to cover was the `except` blocks
around the database and the email/SMS providers, because no happy-path test
can ever reach them.

## Challenges in Reaching Coverage Goals

The first obstacle was time. `is_overdue` depends on `datetime.now()`, so any
test near a boundary could flake. I added an optional `now` argument to `Task`
and a `clock` to `TaskService`, and pinned every test to a fixed instant.

The second obstacle was the `NotImplementedError` stubs from the example
repository. Code that only raises cannot be meaningfully covered. I gave
`TaskRepository` real logic on top of a `database` client, so the repository
itself is tested and only the client is mocked.

Returns diminished: the last 10% took 46 tests, a third of the suite, for
21 statements and 11 partial branches.

## Benefits of Mocking External Dependencies

Mocks let me produce failures on demand. A single `side_effect` simulates a
database outage or an SMTP timeout, and I could prove two rules that are
hard to show any other way. First, a failed save sends no notification.
Second, a failed notification never undoes a save. Asserting call order with
`attach_mock` showed that the save happens before the email.

Without mocks, the suite would need a database and a mail server, run in
seconds, and could not reliably reproduce outages.
Mocking also cost something. A mock only encodes my assumption about an
interface. `Mock(spec=...)` helped by rejecting methods that do not exist, and
the fake repository caught state bugs that per-call stubs could not, such as
a rename freeing the old title.

## Trade-offs Between Coverage and Test Quality

100% was cheap here because the codebase is small and designed for testing.
On a larger system I would not chase it. Every test asserts an outcome, but a
few edge-case tests, such as checking that `repr` contains the title, are
closer to coverage-driven than risk-driven. Meanwhile, the duplicate-title
race condition is fully "covered" and still broken under concurrency.
Coverage shows which code ran, not whether the behavior is right. I balanced
this by requiring every test to assert something a user would notice.

## Lessons Learned About White Box Testing

What surprised me was how much testing influenced the design: dependency
injection, an injectable clock and one error type per layer exist mainly
because they made branches reachable. Next time I would add the clock from
the first line of code instead of retrofitting it. In future projects I will
use branch coverage, specifically the partial-branch list, as a map of what is
untested rather than as a target, and I will pair it with contract tests for
anything I mock.

## Conclusion

Coverage showed precisely what was unexercised; the remaining risks (real
drivers, concurrency, timezones) appear in no percentage.
