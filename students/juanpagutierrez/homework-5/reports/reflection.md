# Reflection - Homework 5

## What was most challenging about achieving high coverage?

The statements were easy; the branches were not. After the integration and
mocking suites, statement coverage looked fine, but coverage.py still reported
eleven partial branches: filter conditions that were only ever true, and error
handlers that no normal input could reach. Covering them meant thinking about
inputs I would not naturally try, such as a task with no due date inside a date
range, or an SMS of exactly 160 characters, and using mocks with `side_effect`
to force database and provider failures. Time was the other challenge: overdue
logic depends on the current time, so I had to make the clock injectable before
the tests became deterministic.

## How does white box testing differ from black box testing?

Black box testing designs cases from the specification: given these inputs,
the documented output should appear. It cannot know whether a test reached
every path in the implementation. White box testing designs cases from the code
itself: each `if`, loop and `except` becomes something to reach. In practice
the two complement each other. The specification told me *what* TaskFlow should
do, and the coverage report told me *which parts of my implementation* had
never been exercised. Neither alone would have found the inclusive date-range
boundary.

## Will you use code coverage in future projects?

Yes, but as a diagnostic tool rather than a goal. I will run branch coverage
in CI and read the missing and partial lines to find untested logic, without
chasing 100%. This assignment also showed me that a covered line can still be
wrong, as the duplicate-title race condition shows, so coverage will sit
alongside code review and contract tests, not replace them.
