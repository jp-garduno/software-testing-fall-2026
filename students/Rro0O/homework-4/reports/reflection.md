# Reflection

**What was most challenging?** The statement is short, so the hardest part was deciding what the correct behaviour is
before testing it. Can a Suspended account transfer? Is the daily limit per transfer or cumulative? Does a fee of $10
apply to exactly $5,000? I documented eleven such decisions in the design document so that every expected result in the
tests has a stated source. Building the decision tables was the second challenge: keeping the rules complete while
collapsing impossible combinations takes patience.

**What did I learn about black box testing?** Each technique sees a different kind of defect. EP maps the inputs, BVA
catches off-by-one mistakes, decision tables expose rule interactions and state tests are the only ones that check
illegal transitions. I also learned that coverage is a weak measure of test quality: my suite had full coverage while a
mutation check still found a defect no test noticed (Suspended accounts losing the ability to receive transfers and pay
fees). Adding two decision table rules fixed it.

**How confident am I in the quality of the system?** Fairly confident about the specified business rules: 183 Python and
184 JavaScript tests pass, coverage is 100% and all 16 injected defects are detected. I am less confident about anything
the specification does not describe, such as concurrent transfers, real-clock behaviour at midnight, authentication and
performance. Those need other kinds of testing, and my system under test is also a model I wrote myself, not a real bank.
