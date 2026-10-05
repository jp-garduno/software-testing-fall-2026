# Reflection: Code Coverage and Testing Metrics

## 1. How many tests did you write to achieve >95% coverage?
A total of **63 tests** were written across the suite for `OrderProcessor` and `Order`. These tests systematically evaluate happy paths, input validation constraints, address verification, edge cases for shipping calculation tiers, discount application and capping, order processing state changes, and delivery date estimations.

## 2. Were there any paths that were difficult or impossible to test? Why?
Yes. Specifically, the branch `elif len(zip_code) == 10:` at line 121 has an unreachable `False` branch. This occurs because the enclosing `if` block at line 114 already enforces `not (len(zip_code) == 5 or len(zip_code) == 10)`. Consequently, inside this block, if `len(zip_code) != 5`, it is mathematically guaranteed to be `10`. Therefore, the `elif` condition will always evaluate to `True` when evaluated, making the `False` branch of that `elif` structurally unreachable without changing the production code. This is an excellent example of how defensive programming can produce unreachable branches in coverage tools.

## 3. Is high coverage the same as good testing?
No. Code coverage is a quantitative metric, not a qualitative one. High coverage merely indicates that statements or branch decisions were executed during test runs. It does not guarantee that the assertions are verifying the correct business logic, that semantic edge cases are handled, or that boundary conditions produce correct outputs. Good testing focuses on behavioral correctness, specification compliance, meaningful assertions, and fault injection.

## 4. What percentage of coverage do you think is reasonable for production code?
In most production systems, 80% to 90% is a pragmatic and healthy target. Critical financial, medical, or security components often justify 95% to 100% statement and branch coverage. Requiring 100% across an entire large codebase often produces diminishing returns, where developers write artificial tests just to trigger boilerplate, logging statements, or defensive branches rather than testing meaningful business rules.

## 5. Can you have high coverage but poor tests? How?
Yes, absolutely. A test suite can achieve 100% coverage simply by executing every function without containing any `assert` statements, or by asserting trivial truths like `assert True`. Furthermore, tests can have high coverage while missing fundamental edge cases, race conditions, floating-point inaccuracies, or boundary transitions that only emerge with specific data combinations.
