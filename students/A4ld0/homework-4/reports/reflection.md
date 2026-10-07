# Homework 4 reflection

Draft based on the completed implementation and measured results; review and
personalize before submitting.

The most challenging part of this assignment was translating informal banking
rules into precise expectations. Statements such as restoring a balance
"above the minimum" leave an important question at exact equality. Fee waivers
and suspended-account permissions also needed explicit interpretations. Writing
those assumptions first made it possible to use the same expectations in both
languages without allowing implementation details to define the requirements.

The exercise showed how black box techniques complement one another.
Equivalence partitioning organized valid and invalid inputs. Boundary analysis
focused attention on the smallest meaningful differences in money and dates.
Decision tables exposed combinations that isolated tests could overlook, while
state transitions demonstrated how one operation changes what is allowed next.
The midnight reset and scheduled-payment examples were particularly useful
because their correctness depends on a sequence of events.

The final evidence gives me confidence in the documented classroom simulation:
both implementations pass the same 172 scenarios and exceed the required
coverage threshold. Exact result comparisons and unchanged-state assertions
provide stronger evidence than simply checking that methods return successfully.
However, neither the passing count nor high coverage proves that every possible
behavior is correct. Both suites share expected results, so an incorrect
expectation could survive in both languages.

Before treating this as a real banking application, I would want independently
reviewed requirements and tests for authentication, concurrent transactions,
persistent storage, and external settlement. The main takeaway is to connect
test design, implementation, and evidence through clear identifiers and honest
limits on what the tests demonstrate.
