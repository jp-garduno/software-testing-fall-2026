# White Box Testing & Coverage Analysis Report

## Executive Summary

TaskFlow was implemented as a compact task-management system with a validated
model, an in-memory repository, a notification boundary, and a service that
coordinates business workflows. The final suite contains 64 tests implemented
with Python's standard library. Coverage.py reports 100% statement coverage
(227 of 227 statements), 100% branch coverage (92 of 92 branches), and 100%
function coverage (27 of 27 non-empty functions).

## Coverage Metrics Achievement

I began with model-level tests for title and description boundaries, valid and
invalid due dates, status transitions, overdue checks, and priority comparison.
I then covered service operations using both a real in-memory repository and
mocked boundaries. Branch coverage required treating each boolean outcome as a
separate test target, including timezone-awareness mismatches, invalid update
types, duplicate titles, archived-task restrictions, and failed notifications.
The remaining paths after the first measured run were identified from the
coverage report and addressed with focused cases rather than broad, redundant
tests. The most useful strategy was to inject the current time into overdue
checks and to use `side_effect` for failure scenarios.

## Challenges in Reaching Coverage Goals

The hardest cases were not the happy paths; they were boundary conditions that
look similar but follow different branches. A timezone-aware due date compared
with a naive clock must be rejected, as must the inverse. Similarly, updating a
title has distinct paths when the title is unchanged, unused, or already owned
by another task. Reading the branch report made these gaps measurable. Another
challenge was keeping the submission independent of third-party test
frameworks while still producing branch and HTML reports. The solution was to
run `unittest` and use coverage.py only as a reporting utility.

## Benefits of Mocking External Dependencies

Mocks kept tests deterministic and fast. A repository mock can fail on demand,
so the service's rule that a failed save prevents notification can be verified
without creating a database. A notification mock makes email and SMS calls,
arguments, counts, and order observable without contacting an external
provider. The in-memory repository remains real in workflow tests, which
provides meaningful component interaction without making every test depend on
the same mock behavior. Without these doubles, network and storage state would
make results slower and less repeatable.

## Coverage vs. Test Quality Trade-offs

One hundred percent coverage is evidence that the tracked statements and
branches ran; it does not prove the requirements are complete or the assertions
are correct. Here the final target is defensible because each added case checks
a business rule or error contract, not merely execution. The test suite asserts
observable results, repository contents, notification attempts, and expected
exceptions. More tests that only execute lines without checking outcomes would
inflate confidence without adding value. The reports therefore pair numerical
coverage with examples of the behaviors each group exercises.

## Lessons Learned

White-box testing showed where control flow still lacked a representative
scenario, while the business rules determined whether that scenario mattered.
The branch report was especially helpful for finding the less obvious
date/time and partial-update paths. I would continue to separate pure model
tests from service workflow tests and mock only at external boundaries. In a
larger system, I would add integration tests against a real database and
notification provider in a separate environment; those infrastructure checks
are intentionally not simulated as production integrations here. Coverage is
most useful as feedback for test design, combined with clear assertions,
isolation, and a review of the requirements.
