# White Box Testing & Coverage Analysis Report

## Coverage Metrics Achievement

I built TaskFlow in layers and measured coverage after each one. Unit tests on the Task model reached 100% statement and branch coverage for `task.py` on their own. After adding the service and its mocked integration tests, overall coverage was only 67%, which was misleading: the repository and notification classes had never really run, because mocks replaced them. The `term-missing` report pointed straight at the gaps, and a third batch of tests brought everything to 100% statements, 100% branches and 33/33 functions. Reading the missing line numbers was the most effective strategy. The hardest code to cover was exception handling: the repository's `RepositoryError` wrapping and the notification retry loop both need a collaborator that fails on demand.

## Challenges in Reaching Coverage Goals

The main obstacle was that mocking a dependency hides it from coverage. A mocked repository proves the service calls it correctly, not that the repository works, so each real class needed its own tests against a fake database. Failure injection was the second challenge, solved with `side_effect`, including lists such as "fails once, then succeeds" for retries. Diminishing returns appeared quickly: going from 67% to about 95% took a few well-aimed tests, while the last branches (clearing a due date, SMS failure) each needed a dedicated scenario for a tiny gain.

## Benefits of Mocking External Dependencies

Mocking made the suite fast (119 tests in about 0.4 s) and deterministic. No test needs a network, mail server or database, and a failure points to one component. It also made otherwise hard scenarios easy, such as an SMTP outage in the middle of a status change. Without mocks I would have needed a running provider and would likely have tested only happy paths. Mocks have a cost: `Mock(spec=...)` was necessary so typos do not pass silently, and tests that assert exact call arguments are coupled to the implementation. For the full lifecycle test I used a hand-written fake repository, because asserting final state is more robust than asserting call sequences.

## Trade-offs Between Coverage and Test Quality

Reaching 100% was feasible because the codebase is small, but I do not think the number should be the goal. Coverage shows which lines ran, not whether assertions are meaningful. The `repr` test is the weakest in the suite: it exists mostly to cover a line. Every other test is tied to a behaviour, such as a return value, a state change, or an interaction that must not happen (no notification when saving fails). The coverage report also lists what 100% does not prove: the real notification provider, real database behaviour and exact time boundaries. I would set a floor around 80-90% and spend remaining effort on edge cases and failure modes, not the last few lines.

## Lessons Learned

What surprised me most was the gap between line and branch coverage: the service looked nearly done at 88%, yet one `if` arm was still unvisited, so I trust branch coverage more. Making notification failures non-fatal was also a design decision the tests forced me to state explicitly. Next time I would inject a clock so overdue logic can be tested at exact boundaries, and write tests alongside each class instead of in batches. In future projects I will enable branch coverage early and use it to find untested behaviour, not to prove the suite is finished.
