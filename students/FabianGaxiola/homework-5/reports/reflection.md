# Brief Reflection

The most challenging part of reaching high coverage was identifying conditions
that look similar but take different branches. Timezone-aware and naive
datetimes, title uniqueness on update, and notification failures each required
their own scenarios. The branch report helped point to specific gaps, and
injecting a reference time made overdue tests deterministic.

White-box testing uses knowledge of internal control flow to choose tests for
statements, conditions, and branches. Black-box testing focuses on inputs and
observable outputs without relying on implementation details. Both are useful:
the TaskFlow tests use business requirements to assert outcomes, then use
coverage feedback to check whether important paths were exercised.

I expect to use coverage in future projects as a diagnostic tool, not as a
standalone quality score. A 100% result for these files confirms that every
tracked statement and branch ran in the test suite, but it cannot prove that
the requirements are complete or that every assertion is meaningful. Mocks
also made it practical to test database and notification failures without
third-party testing packages, network calls, or persistent test state. The
main lesson is to pair coverage measurements with isolated tests and explicit
behavioral assertions. The in-memory repository gives workflows realistic
component interactions while still keeping the suite fast and repeatable.
