# White Box Testing & Coverage Analysis Report

## Executive Summary

TaskFlow was built and tested in four layers: model, repository, notification
gateway and service. The final suite has 133 tests, runs in about 0.3 seconds
and reaches 100% statement, branch and function coverage of `src/`. Designing
for testability mattered more than any individual test.

## Coverage Metrics Achievement

I measured coverage after every suite instead of at the end. Unit tests alone
gave 57% overall but 100% of `task.py`, because boundary values were chosen
for every validation rule. Integration tests with a mocked repository and
notifier lifted the total to 87%. From there the HTML report became the guide:
it pointed to the `except` blocks that swallow notification failures and to
one partial branch (`if not self.phone_number`). The most effective strategy
was reading yellow "partial" lines: each one is a decision tested in only one
direction. Error handling was hardest to cover, since it only runs when a
collaborator fails.

## Challenges in Reaching Coverage Goals

Time was the first obstacle. The suggested model calls `datetime.now()`
directly, so overdue tests need workarounds like overwriting the due date
after creation. I added a `now` parameter to the model and
a `clock` to the service, and tests use a fixed date. Overdue tests became
deterministic and no longer bypass validation.

The second obstacle was a limit of the tool. coverage.py reports branches
between lines, so the compound condition in the repository filter showed 100%
after one call. I wrote one test per filter anyway. The last few percent did
have diminishing returns: closing 90% to 100% took 33 extra tests, but most of
them checked real rules, such as SMS truncation and invalid phone numbers.

## Benefits of Mocking External Dependencies

Mocking made the error paths reachable: a failing SMTP server or database is
one `side_effect` line. It also turned interactions
into assertions: the tests check that nothing is notified when saving fails,
that the save happens before the email, and that SMS is only sent for URGENT
tasks. Without mocks the suite would be slow and could not reproduce failures
on demand.

The cost is that a mock can drift from the real API. Using `Mock(spec=...)`
and `create_autospec` reduced that risk, because calls to methods or
signatures that do not exist fail. I also kept a `FakeDatabase` so that the
service, the real repository and the search logic run together at least once.

## Coverage vs Quality Trade-offs

100% was cheap here because the code is small and designed for testing; in a
larger system I would not chase it. I avoided tests that only execute lines:
every test asserts a result or an interaction, and the mocks verify arguments,
not just "was called". A suite can reach 100% and still be weak, because
coverage shows what ran, not what was checked. My balance rule is to use
coverage to find untested decisions and judge each test by whether it could
fail for a real bug.

## Lessons Learned

What surprised me most was how much testability depends on design. Code that
creates its own dependencies or reads the clock is hard to cover; code that
receives them is easy. Next time I would write
the service tests first with mocks, letting them define the repository
interface, instead of designing the interface up front. In future projects I
will add `--cov-branch` to CI and review the partial lines on every pull
request.

## Conclusion

White box testing works best as a feedback loop: write tests, read the report,
then decide whether a missed line is a missing test, dead code or an
acceptable gap. Coverage is a tool for finding untested decisions, not proof
of quality.
