# Exercise 4 Coverage Reflection

I wrote 67 test cases, including parameterized cases, to cover the order
processor's main behavior and edge conditions. The most challenging paths were
the short-circuit validation rules, the ZIP+4 format checks, and the defensive
branch that caps a discount at the subtotal. That last path cannot be reached
through the default discount configuration, so I tested it by adding a custom
discount percentage to the processor instance. This verified the safeguard
without changing production behavior.

High coverage is not the same as good testing. A test can execute a line
without checking whether the result is correct. For that reason, these tests
assert exact validation messages, boundary values, state transitions, cost
breakdowns, normalized codes, and delivery dates. Parameterization keeps
similar boundary checks independent while avoiding repetitive test code.

For production code, I think 80–90% coverage is often a reasonable baseline,
but the appropriate target depends on risk. Payment calculations, security
rules, and safety-critical decisions deserve much higher branch coverage than
simple presentation code. There are also diminishing returns: forcing every
defensive or unreachable line to execute can make tests tightly coupled to
implementation details. Coverage is best used as a map that reveals untested
areas, while meaningful assertions, realistic scenarios, mutation testing,
and code review provide stronger evidence that the software behaves correctly.
