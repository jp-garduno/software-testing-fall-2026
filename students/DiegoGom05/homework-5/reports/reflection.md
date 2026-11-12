# Reflection

## What was most challenging about achieving high coverage?

Reaching about 90% was straightforward, but the last few percent were the hardest. They were error-handling branches and optional filters that only run in unusual situations. I had to think about what could go wrong, like a database failing after a lookup, or an SMS gateway being down, and simulate it with mocks. I also had to decide how to handle requirements that were implied rather than written, such as notification failures not breaking the workflow.

## How does white box testing differ from black box testing?

In black box testing I design tests from the requirements without looking at the code: valid and invalid inputs, boundaries, expected outputs. In white box testing I read the implementation and design tests so that every statement, branch and exception path is executed. Black box finds missing or misunderstood requirements; white box finds untested logic and dead code. In this homework I used both: the requirements gave the scenarios, and the coverage report showed which ones I had forgotten.

## Will you use code coverage in your future projects?

Yes, but as a diagnostic tool, not as a goal. The HTML report is excellent for spotting scenarios I did not think of. I will set a reasonable minimum threshold (around 80-85%) in CI, review uncovered lines instead of chasing 100%, and make sure each test has meaningful assertions, because coverage alone cannot tell whether a test actually verifies anything.
