# Comparative Analysis: Black Box Testing Techniques

**Student**: Kaito0110
**Assignment**: Homework 4 — Black Box Testing
**Word Count**: ~620 words

---

## Introduction

This analysis compares the four black-box testing techniques applied to the SecureBank Online Banking System: Equivalence Partitioning (EP), Boundary Value Analysis (BVA), Decision Tables (DT), and State Transition Testing (ST). Each technique targets a different category of defects and offers unique strengths and limitations. Understanding their complementary nature is essential for designing efficient, high-quality test suites.

---

## Equivalence Partitioning (EP)

Equivalence Partitioning reduced the test design effort by grouping inputs into classes whose members are assumed to behave identically. For SecureBank, this meant identifying five distinct partitions for the transfer amount (valid, zero, negative, exceeds limit, exceeds balance) and separate classes for account type, balance, payee, and date range. This yielded 16 test cases that collectively cover a broad behavioral surface.

**Effectiveness**: EP was highly efficient for covering normal and invalid input categories with minimal redundancy. It uncovered logical branches that would otherwise require exhaustive testing. The main limitation is that EP alone gives no information about where within a valid partition failures may lurk—particularly at the edges of the partition boundaries.

**Defects found during design**: While designing EP partitions, I noticed that the "amount exceeds daily limit" and "amount exceeds balance" partitions were not independent—when balance is low, the system raises the balance error first. This ordering insight came directly from the partitioning exercise and improved the implementation.

---

## Boundary Value Analysis (BVA)

BVA extends EP by focusing test cases on the exact boundary values and their immediate neighbors ($\pm$1 unit). For the checking account's $5,000 daily limit, six boundary tests were designed: $0.00, $0.01, $4,999.99, $5,000.00, $5,000.01, and $10,000.00. The same pattern was applied to savings limits, minimum balance thresholds, and fee waiver thresholds.

**Effectiveness**: BVA proved to be the most defect-sensitive technique in this assignment. During implementation, two tests initially failed because fixture accounts had insufficient balances for near-limit transfers—a subtle interaction between two boundaries (the daily limit and the balance). This kind of off-by-one or fixture-setup defect is exactly what BVA is designed to expose. BVA produced 19 test cases and achieved the highest density of real behavior coverage per test.

**Limitation**: BVA requires a precise numerical specification. For boolean or categorical inputs (like account type), it provides no added value over EP.

---

## Decision Tables (DT)

Decision Tables systematically enumerate combinations of conditions and their corresponding actions. For the transfer validation table, three conditions (sufficient funds, within daily limit, account active) produced 8 logical rules. Two additional tables covered monthly fee processing and bill payment validation.

**Effectiveness**: DT was uniquely valuable for multi-condition logic. It revealed priority ordering among error conditions—for example, that the frozen-account check must fire before the limit check. This ordering is easy to overlook in EP or BVA tests because those techniques examine one variable at a time. DT also helped identify a potential gap: Rule 7 (insufficient funds + exceeds limit + active) needed a clear specification of which error to report first.

**Limitation**: DT scales poorly for systems with many conditions. With $n$ boolean conditions, $2^n$ rules are generated; pruning equivalent rules requires domain knowledge.

---

## State Transition Testing (ST)

State Transition Testing modeled the four account states (Active, Frozen, Suspended, Closed) and seven transitions. Test cases validated every valid transition, confirmed that invalid transitions are rejected, and checked that closed accounts reject all subsequent operations.

**Effectiveness**: ST was indispensable for discovering lifecycle-related defects that the other techniques cannot see. For instance, the "fee causes suspension" scenario (ST12) and "cumulative daily limit" scenario were only naturally expressed as sequences of events leading through multiple states. No other technique would have prompted these multi-step test scenarios.

**Limitation**: ST requires a well-defined state model. In systems without explicit states, this technique demands extra upfront analysis.

---

## Summary Comparison

| Criterion            | EP              | BVA           | DT                     | ST                  |
| -------------------- | --------------- | ------------- | ---------------------- | ------------------- |
| Best for             | Input classes   | Numeric edges | Multi-condition logic  | Sequences/lifecycle |
| Test cases generated | 16              | 19            | 17                     | 17                  |
| Defect type targeted | Invalid classes | Off-by-one    | Condition combinations | State bugs          |
| Design effort        | Low             | Medium        | Medium–High            | High                |
| Scalability          | High            | High          | Low (exponential)      | Medium              |

## Conclusion

No single technique is sufficient on its own. EP provides broad input coverage, BVA pinpoints numeric defects at boundaries, DT handles complex multi-condition logic systematically, and ST captures behavioral sequences across time. The 69-test suite in this homework demonstrates that combining all four techniques achieves 93% code coverage—well above the 80% minimum—and validates the correctness of SecureBank's core banking rules across a wide variety of scenarios.
