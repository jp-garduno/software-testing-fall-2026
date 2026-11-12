# White Box Testing & Coverage Analysis Report

## Executive Summary

This report reflects on testing TaskFlow using a white box approach. The final suite contains 83 tests, runs in under one second, and achieves 100% statement and branch coverage (172 statements and 60 branches). The main lesson is that coverage shows which code was executed, but does not guarantee test quality.

## Coverage Metrics Achievement

I started with unit tests for the `Task` model and then moved to the service layer. Parametrized tests and mocks with `side_effect` were the most effective strategies. Testing status transitions covered valid, invalid, and ARCHIVED cases efficiently. Boundary tests for titles (2, 3, 100, and 101 characters) verified validation limits. The most challenging areas were `search_tasks`, where each filtering condition required specific scenarios, and notification error handling, which required mocked exceptions to simulate dependency failures.

## Challenges in Reaching Coverage Goals

One obstacle was the assignment's overdue test, which created a task with a past due date even though the constructor rejected it. I solved this by creating the task first and assigning the date afterward. Another fixture used an invalid two-character title. I also accidentally duplicated integration tests in the edge case file, inflating the test count and hiding failures until they appeared twice.

Diminishing returns became evident when the remaining uncovered code consisted mainly of interface methods that raise `NotImplementedError`. Testing these methods increased coverage but provided little practical value.

## Benefits of Mocking External Dependencies

Mocking the repository and notification service made tests fast, isolated, and deterministic. It also allowed me to simulate database failures and SMTP outages without requiring real external services. This reduced execution time and made failures easier to diagnose.

I used mocks to verify behavior, stubs to provide data, and an in-memory fake repository to test complete workflows. To verify that saving occurred before notification, I recorded events through `side_effect`, since checking individual mock calls did not clearly establish execution order.

## Trade-offs Between Coverage and Test Quality

I do not consider 100% coverage a necessary goal. Some tests primarily increased coverage, especially those testing `NotImplementedError` interfaces, without verifying meaningful behavior. Coverage proves that code executed, not that it works correctly.

I prioritized business rules such as valid transitions, duplicate titles, and soft deletion before using coverage reports to identify gaps. Every test should fail when the behavior it protects breaks. Therefore, I consider 85–90% coverage with strong assertions potentially more valuable than 100% coverage with weak tests.

## Lessons Learned About White Box Testing

Many problems originated in the test code itself, including invalid fixtures, duplicated tests, and unrealistic examples. In future projects, I will create valid fixtures, run coverage after each test file, and identify duplicates earlier. I will also use branch coverage, establish reasonable CI thresholds, and combine white box testing with black box testing to evaluate actual behavior rather than executed lines alone.