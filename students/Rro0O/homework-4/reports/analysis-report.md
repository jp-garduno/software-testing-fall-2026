# Black Box Testing Analysis Report

## Executive Summary

I designed 37 equivalence partitions, 59 boundary values, four decision tables and 25 state transition cases for SecureBank,
and automated them as 183 pytest tests (plus an equivalent 184-test Jest port). All pass with 100% statement and branch
coverage. The most useful result was not a bug in the code but a measurement of the tests themselves: a 16-mutant check
initially left one defect undetected, which exposed a gap that no design table had listed.

## Technique Effectiveness

### Equivalence Partitioning
EP was the fastest way to get broad, readable coverage and the easiest to apply: every input gets valid and invalid classes
and each class gets one test. Its real value was forcing me to enumerate inputs I would otherwise skip (payee, payment date,
date ranges) and to notice eleven specification ambiguities, for example whether Suspended accounts may transact. Alone it
reached only 73% of statements and detected 6 of 16 mutants, because representative values sit in the middle of a class.

### Boundary Value Analysis
BVA was the most effective at finding potential defects. It detected 13 of the 16 injected mutants, including every
comparison operator swap (`>` vs `>=`) on limits, minimums, fee thresholds and inclusive date ranges. The most valuable
boundary was the fee waiver: "balance > $1,000" means exactly $1,000 still pays. Cumulative limits (BV23-BV27) were the
hardest, because a boundary can be reached by a sequence rather than a single value.

### Decision Tables
Decision tables were the hardest to build and keep complete, but gave the clearest picture of combined rules. The transfer
table forced me to decide what happens when several checks fail at once (report all, unless the account is frozen), and
the fee table crossed account type, date, state and balance. They were the only technique that killed mutant M15, where
Suspended accounts stopped receiving transfers and paying fees.

### State Transition Testing
State testing was the only technique that covered *invalid* transitions: freezing a Suspended account, unfreezing an
Active one, and nine events against a Closed account. Two mutants (M11, M16) that allowed illegal transitions were
detected only by state tests. It gave me the most confidence in the lifecycle, including the fact that three different
events (transfer, bill payment, fee) lead to Suspended.

## Coverage Comparison

| Technique | Tests | Statements covered alone | Mutants detected (of 16) |
|---|---|---|---|
| EP | 46 | 73% | 6 |
| BVA | 59 | 67% | 13 |
| Decision tables | 44 | 84% | 4 |
| State transitions | 34 | 79% | 4 |

Overlap is large: BVA and EP both hit the transfer and date logic, and eight mutants were detected by more than one
technique. Gaps do exist between techniques, however: without the decision tables the suite missed the Suspended-account
behaviour, and without state tests it missed illegal transitions. What no technique caught, because none of them targets it,
is anything outside the specification: concurrency, rounding across many operations, and real clock behaviour around
midnight (my tests inject dates instead of using the clock).

## Real-World Application

In a real project I would start with EP to map the input space, then apply BVA to every numeric or date partition, since
BVA gave the most defect detection per test. Decision tables suit rules with three or more interacting conditions, and
state testing any entity with a lifecycle, which in banking is every account. EP+BVA is the best pair for validation code;
decision tables+state testing for business workflows.

## Recommendations

Next time I would write the mutation check earlier, since it found a gap that reviewing the tables did not. I would add
property-based tests (random sequences of operations checking that the balance never goes negative and that Closed is
absorbing), pairwise testing for the type-by-state-by-amount combinations, and real time-dependent tests around midnight.
Security (authorization on freeze/close), concurrency and performance testing would also be needed before trusting a real system.

## Lessons Learned

Coverage of 100% says the code ran, not that the tests would notice a defect; the mutation check said much more.
