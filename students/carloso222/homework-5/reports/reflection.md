# Reflection — Homework 5

## What was most challenging about achieving high coverage?

The error paths. Happy paths are covered almost automatically by the first
integration tests, but the `except` blocks that handle a failed email, SMS or
database call only run when a collaborator breaks. I needed mocks with
`side_effect` to reach them, plus a clear rule for each failure: a failed save
stops the operation and sends nothing, while a failed notification is logged
and the task change is kept. Time was the other challenge. Until I injected a
clock, overdue tests depended on the real date.

## How does white box testing differ from black box testing?

In black box testing (homework 4) I designed cases only from the
specification, using equivalence classes, boundaries, decision tables and
state diagrams, without looking at the code. In white box testing the code
itself is the input: I read the branches, ran coverage and added tests for
decisions that had only been exercised one way. The two complement each other.
Black box testing finds missing behaviour that coverage cannot show, while
white box testing finds untested paths that the specification never mentions,
such as wrapping database errors or truncating a long SMS.

## Will you use code coverage in your future projects?

Yes, but as a guide, not a target. I will run tests with `--cov-branch` in CI,
review the partial and missed lines in the HTML report on each change, and set
a reasonable threshold, around 85%, rather than demanding 100%. More
importantly, I will design code with injected dependencies from the start,
because that is what made high coverage cheap in this project.
