# White Box Testing & Coverage Analysis Report

## Executive Summary

I built TaskFlow (task model, repository, notification gateway, service) and tested it to 100%
statement and branch coverage with 130 tests that run in about a tenth of a second. The number
matters less than what produced it: the biggest jump came from testing a layer I had mocked away
everywhere else, and the most useful check was one coverage cannot give, whether the tests fail
when the code is wrong.

## Coverage Metrics Achievement

I measured after every stage. The 43 unit tests took `task.py` to 100% immediately, because the
model is pure logic with an injectable clock. Adding integration tests brought the whole of `src/`
to only 88%, and the gap was concentrated: `notification_service.py` sat at 16%. Every service test
mocks the notification service, so its own branches never ran. The fix was to mock one level lower,
the email and SMS transport clients, and test the gateway directly. The hardest code to cover was
error handling, since it needs a collaborator to fail on demand.

## Challenges in Reaching Coverage Goals

Time was the first obstacle. My fixed test clock (October 1) was already in the past when I ran
the suite, so tests that built tasks with `datetime.now()` would have rejected "future" due dates.
Injecting a `clock` into `TaskService` and a `now` parameter into the model solved it and removed
real-time dependence everywhere. The second was `==` versus `!=` mutations that appeared to survive:
stale `.pyc` files, not weak tests. There were diminishing returns: closing the last 12% took 50
more tests (80 to 130), most of them for one small branch each.

## Benefits of Mocking External Dependencies

Mocks let me inject failures that are hard to produce for real: a database that dies mid-save, an
SMTP server that times out. They made it possible to assert behavior that matters, such as "no
notification is sent if the save failed" and "a failed email does not roll back a status change."
Without mocking the suite would need a database and mail server and would be slower and flaky.
The cost is that a mock only knows what I told it. Using `Mock(spec=...)` helped, since calling a
method the real class lacks raises an error, but a fake database can still disagree with a real one.

## Trade-offs Between Coverage and Test Quality

I do not think 100% is the goal. It is easy here because the code is small and has no I/O.
Some tests exist purely to reach a branch, for example the one that checks the real-clock default
for `touch()`, and they assert little. Coverage also hides a real defect: the duplicate-title check
is check-then-act, so two concurrent requests could both pass it, and no line or branch metric
shows that. To test quality rather than execution I mutated seven lines in a temporary copy; all
seven were caught. That is a small sample, but it tells me more than the percentage.

## Lessons Learned

What surprised me was how much the design drove testability: injecting the clock, repository and
notifier made the tests simple, and not injecting them would have made them painful. Next time I
would write tests alongside each class rather than measure after the fact, and run a proper
mutation tool such as `mutmut`. I will use coverage in future projects as a map of what was never
exercised, not as a score.
