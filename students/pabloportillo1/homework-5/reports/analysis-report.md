# White Box Testing & Coverage Analysis Report

## Coverage Metrics Achievement

The final suite has 169 tests and reaches 100% statement and 100% branch coverage of `src/` in under
half a second. I built it in four measured steps: unit tests for the `Task` model (60%), integration
tests running `TaskService` on the real repository over an in-memory fake database (89%), mocking
tests for failure paths (98%), and boundary tests (100%). The integration step was the most
effective, because each workflow test crosses three layers. The hardest code to cover was failure
handling: a fake database never fails, so the `DatabaseError` translation and the notification retry
loop only ran once I replaced their dependencies with mocks that raise on demand.

## Challenges in Reaching Coverage Goals

Time was the first obstacle. Overdue detection and "due date must be in the future" depend on
`datetime.now()`, so a test written today could fail tomorrow. Patching `task.datetime` with a small
`FrozenClock` fixture fixed that, and it let tests move time forward instead of forcing a past due
date onto a task. The second was a misleading number: unit tests that never call the service already
showed 62% statement coverage, because 108 of the 273 statements run at import time. Branch coverage
has no such inflation, so I learned to read it as the honest metric. And yes, there were diminishing
returns: the last 2.3 points took 64 tests.

## Benefits of Mocking External Dependencies

Mocks made error scenarios cheap. A database outage, an SMTP failure or a provider that fails once
and then succeeds is one `side_effect` line, and the whole suite runs in 0.4 seconds. They also
improved the design: to mock the database and the gateways I had to inject them, which gave the code
clear boundaries. I used `create_autospec` everywhere, so a mock rejects a call with the wrong
arguments instead of silently accepting it. The cost is that a mock only checks what I told it to
expect, which is why the integration tests use a fake database with real behaviour and mock only the
notification service.

## Trade-offs Between Coverage and Test Quality

I do not think 100% is a goal in itself, and this project showed why. I ran a small mutation check:
twelve one-character bugs, such as `<=` turned into `<`. The suite at 98% coverage caught only two of
them, and six of the survivors were in `task.py`, which had been at 100% since the first step. Most
of the 64 edge case tests add little or no coverage; their value is pinning each rule at its exact
boundary. I did not write tests just to turn a line green, but coverage alone could not have told me
whether I had.

## Lessons Learned About White Box Testing

What surprised me most is how different "executed" and "verified" are. Coverage is excellent at
pointing to code nobody ran, like the four red lines left after step 3, and weak at saying whether
the tests would notice a wrong comparison. Next time I would start from boundary values, as in black
box testing, and use coverage afterwards to find what I missed rather than as the target. In future
projects I will keep branch coverage in CI with a threshold, inject clocks and external services from
the start, and run a quick mutation check on the rules that matter most.
