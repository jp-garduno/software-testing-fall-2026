# Reflection

**What was most challenging about achieving high coverage?**

The hardest part was realising that mocks hide code from the coverage tool. After the
integration tests the project sat at 67% even though 61 tests passed, because the
repository and notification service were always replaced by mocks and never executed.
I had to write separate tests for those classes against a fake database and a fake
transport. The other difficult area was failure paths: exception handling and the retry
loop only run when a collaborator breaks, so each one needed a deliberately failing
double built with `side_effect`.

**How does white box testing differ from black box testing?**

Black box tests are written from the specification: given this input I expect that
output, without looking at the code. White box tests are written with the implementation
in front of me. I can read the branches, see that `update_task` has an arm for clearing
the due date, and deliberately build a test that takes it. The coverage report turns that
into a measurable feedback loop. The downside is coupling: tests that assert exact mock
calls can break when the internals are refactored, whereas black box tests survive that.
Both are needed, since coverage shows code ran, not that the requirement is correct.

**Will you use code coverage in your future projects?**

Yes, but as a diagnostic and not as a goal. I will enable branch coverage from the start,
look at the missing lines after each batch of tests, and use a threshold in CI as a floor
(around 80-90%) so regressions are noticed. I will not chase the last percent with
tests that assert nothing, and I will list what the number does not cover.
