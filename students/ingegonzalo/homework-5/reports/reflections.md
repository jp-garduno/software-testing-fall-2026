# Reflection

## What was most challenging about achieving high coverage?

Reaching 100% was not the hard part; making sure the tests were meaningful was. The assignment's own example for overdue detection creates a task with a past due date, which the constructor rejects, so I had to create the task first and set the date afterward. Later, a fixture used a two-character title and broke a test because of the very validation I was testing. Branch coverage in the search filters was also demanding, since each condition needed its own case. Parametrizing the status transitions covered many paths with little code, while the error paths required mocks with `side_effect` to simulate database and notification failures. I also wrote a few tests mainly to cover the `NotImplementedError` interfaces, which raise coverage but verify very little.

## How does white box testing differ from black box testing?

Black box testing checks behavior against the specification without looking at the code. White box testing uses the internal structure: I read the code to find every `if/else`, exception path and state transition, and wrote tests for each one. The coverage report then showed exactly what my tests had not executed. The limitation is that white box tests can become tied to implementation details, and coverage cannot tell whether the specification itself is correct.

## Will you use code coverage in your future projects?

Yes, but as a guide rather than a goal. I will use branch coverage to find untested logic and set a reasonable threshold in CI, while relying on strong assertions and black box tests to judge quality. 100% coverage shows that the code ran, not that it is correct.