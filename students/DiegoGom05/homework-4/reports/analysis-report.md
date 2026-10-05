# Black Box Testing Analysis Report

## Executive Summary

This analysis evaluates four structural black-box testing techniques—Equivalence Partitioning, Boundary Value Analysis, Decision Tables, and State Transition Testing—applied to the `bankingSystem.js` module. The execution achieved 100% line and branch coverage across 25 unit tests using Jest. The findings demonstrate how combining input-domain partitioning with structural state and rule modeling ensures robust software quality in domain-critical financial applications.

---

## Technique Effectiveness

### Equivalence Partitioning

Equivalence Partitioning (EP) was the easiest technique to apply and proved essential for establishing baseline test cases. By partitioning inputs into valid (positive amounts, supported account types) and invalid domains (negative amounts, zero value, unsupported account types), EP quickly validated basic parameter handling and error paths. During execution, EP highlighted a critical validation order issue where an insufficient balance check was bypassed by a daily limit check. However, EP alone lacks precision for testing exact business thresholds.

### Boundary Value Analysis

Boundary Value Analysis (BVA) provided the highest confidence regarding arithmetic correctness and boundary logic. Applying BVA around critical thresholds—such as $0.01 (minimum transfer), $5,000.00 (daily limit for checking accounts), and $25,000.00 (premium limit)—ensured that strict inequality operators (`>`, `<`, `>=`, `<=`) were correctly implemented without off-by-one bugs or floating-point precision drifts.

### Decision Tables

Decision Tables were the hardest technique to structure initially due to the combinatorics of compound conditions, but they proved to be the most effective for identifying logic gaps. Modeling interactions between account tiers (`Savings`, `Checking`, `Premium`), account balances, and fee waivers ensured that multi-variable business rules were systematically covered. This technique eliminated ambiguity surrounding complex fee structures and conditional bill payment failures.

### State Transition Testing

State Transition Testing was crucial for verifying the system's lifecycle behavior. Financial systems rely heavily on state integrity (`Active`, `Suspended`, `Frozen`, `Closed`), and this technique ensured that restricted accounts successfully blocked outbound transactions while allowing valid recovery triggers (e.g., restoring a `Suspended` account to `Active` upon receiving a qualifying deposit).

---

## Coverage Comparison

Each technique targeted distinct architectural dimensions of the application. While EP and BVA focused on input parameter boundaries, Decision Tables and State Transitions targeted multi-variable conditional logic and system states.

| Technique                    | Focus Area                      | Code Coverage Contribution        | Primary Strengths                                                    |
| :--------------------------- | :------------------------------ | :-------------------------------- | :------------------------------------------------------------------- |
| **Equivalence Partitioning** | Input Domains & Parameter Types | ~30% (Main validation lines)      | Rapid identification of missing input checks and basic error routes. |
| **Boundary Value Analysis**  | Exact Numeric Thresholds        | ~25% (Conditional branches)       | High precision for boundary checks and edge-case prevention.         |
| **Decision Tables**          | Multi-variable Rules & Fees     | ~25% (Compound `if`/`else` logic) | Systematic coverage of rule combinations and complex logic paths.    |
| **State Transitions**        | Account Lifecycle & Guards      | ~20% (State guard clauses)        | Guarantees system integrity across valid and invalid state changes.  |

### Overlaps and Gaps

- **Overlaps**: Significant overlap occurred between EP and BVA on valid/invalid transfer amounts, as both exercise basic input paths. Similarly, Decision Tables overlapped with State Transitions when evaluating fee behaviors on suspended or restricted accounts.
- **Gaps**: Black-box techniques inherent to single-unit testing missed concurrency issues (e.g., simultaneous transfers race conditions) and persistence failures, which require integration and non-functional testing.

---

## Real-World Application

In a professional setting, testing high-risk financial software requires a layered, prioritized testing strategy:

1. **Prioritization**: I would prioritize **Decision Tables** and **State Transition Testing** during the initial architectural design phase, as core business rules and state machines carry the highest financial and compliance risk.
2. **Technique Synergy**: The combination of **EP + BVA** works best for fast input validation at the unit level, while **Decision Tables + State Transitions** form the backbone of integration and system test plans.
3. **Banking Domain Insights**: In financial software, an undetected off-by-one boundary error or an improper state bypass can lead to direct monetary loss or regulatory non-compliance, making BVA and State Transition testing indispensable.

---

## Recommendations

For future test design and system iterations, I recommend the following improvements:

1. **Validation Re-ordering**: Refactor input checking to evaluate state guards first, followed by structural input validation, account balance checks, and finally daily transaction limits.
2. **Property-Based Testing**: Introduce property-based testing (e.g., using `fast-check` in JavaScript) to complement BVA by generating thousands of random boundary values and floating-point combinations.
3. **Integration & Concurrency Testing**: Expand testing beyond unit-level black-box techniques to include multi-threaded asynchronous stress tests and mock API integration tests for external payee services.

---

## Lessons Learned

The most important insight from this implementation is that high test coverage (100%) does not guarantee logical correctness if assertion quality or evaluation order is flawed. Structuring test suites using formal black-box design techniques ensures that tests actively search for edge cases rather than merely hitting lines of code.
