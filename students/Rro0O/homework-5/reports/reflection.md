# Reflection

**What was most challenging about achieving high coverage?** The code that only runs when something goes wrong: the
`except` blocks around notifications and the guards that depend on the current time. Those branches never execute in a
normal run, so I had to configure mocks with `side_effect` and set fields after construction to build states (such as an
overdue task) that the constructor deliberately refuses. The last few percent also felt the most mechanical, with each
extra test protecting very little.

**How does white box testing differ from black box testing?** In black box testing I derive cases from the
specification (equivalence classes, boundaries) without looking at the implementation. In white box testing I read the
implementation and choose inputs to make each statement and branch execute. That finds paths the spec never mentions,
such as a defensive branch, but it can miss requirements that the code simply forgot to implement, since coverage only
measures code that exists. The two approaches complement each other.

**Will you use code coverage in your future projects?** Yes, as a diagnostic tool rather than a goal. I will run it in
CI with a reasonable threshold and use the branch report to spot untested decisions. I will not treat a high number as
proof of quality, and I will pair it with meaningful assertions and, where possible, mutation testing.
