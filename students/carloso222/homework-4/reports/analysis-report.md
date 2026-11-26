# Black Box Testing Analysis Report

## Executive Summary

The SecureBank exercise showed that no single black-box technique is sufficient for a system with numeric limits, business rules, and account states. Equivalence Partitioning reduced the input space, Boundary Value Analysis concentrated on high-risk edges, Decision Tables organized combinations of conditions, and State Transition Testing validated behavior that depends on prior events. Used together, the four techniques produced a more convincing suite than any one of them alone.

## Technique Effectiveness

### Equivalence Partitioning

Equivalence Partitioning was the easiest technique to begin with because the banking inputs naturally separate into meaningful valid and invalid groups. Transfer amounts, account types, payees, balances, and date ranges all have obvious partitions. Its main advantage was efficiency: instead of testing every possible transfer amount, I could choose representative values for positive amounts, zero, negative amounts, amounts above the balance, and amounts above the daily limit. The limitation is that EP does not focus strongly enough on exact thresholds, so it can miss defects that only appear at a boundary.

### Boundary Value Analysis

Boundary Value Analysis was the most useful technique for numeric rules. Banking software contains many exact thresholds where an off-by-one-cent error can create incorrect behavior. The most valuable cases were $0.00/$0.01, $4,999.99/$5,000/$5,000.01 for Checking transfers, and $999.99/$1,000/$1,000.01 for the Savings fee waiver. The wording of the requirement matters here: the fee is waived when the balance is greater than the threshold, not greater than or equal to it. Testing exactly at the threshold provides confidence that the implementation follows that rule.

### Decision Tables

Decision Tables were the hardest technique to design because several conditions interact at the same time. A transfer may have sufficient funds but still fail because the account is Frozen or because the daily limit has already been exceeded. Writing these combinations as rules made hidden interactions visible and reduced the risk of testing only the happy path. They were especially effective for transfer validation, monthly fees, and bill payment. Their main cost is that the number of combinations can grow quickly, so irrelevant or impossible combinations must be simplified carefully.

### State Transition Testing

State Transition Testing provided the most confidence in lifecycle behavior. The same operation can be allowed or rejected depending on whether an account is Active, Suspended, Frozen, or Closed. This technique caught scenarios that input-focused testing alone would not express clearly, such as a Suspended Savings account returning to Active after a deposit, or a Closed account rejecting reopening. It also forced the tests to verify not only an output but the resulting state.

## Coverage Comparison

| Technique         | Main strength                   | Typical overlap                 | Main gap              |
| ----------------- | ------------------------------- | ------------------------------- | --------------------- |
| EP                | Broad input-class coverage      | BVA on numeric partitions       | Exact edges           |
| BVA               | Threshold and off-by-one errors | EP and fee rules                | Multi-condition logic |
| Decision Tables   | Business-rule combinations      | EP/BVA representative values    | Long state history    |
| State Transitions | Lifecycle and restrictions      | Decision conditions using state | Large numeric spaces  |

There is useful overlap rather than unnecessary duplication. For example, transfer limits appear in EP, BVA, and decision-table tests, but each technique asks a different question. EP checks the class of input, BVA checks the exact edge, and a decision table checks how the limit interacts with funds and account state. A remaining gap is non-functional testing: this suite does not measure performance, security, usability, concurrency, or resilience.

## Real-World Application

In a real banking project I would start with EP to map the domain, then apply BVA to every financial threshold. I would use Decision Tables for regulatory and business rules with multiple conditions, and State Transition Testing for account lifecycle, fraud controls, authentication locks, and payment workflows. For financial operations, BVA and Decision Tables are especially strong together because they combine exact monetary limits with rule interactions.

## Recommendations

Next time I would add requirement-to-test traceability in a dedicated matrix and include accumulated daily transfers rather than only single-transfer limits. I would also add tests for midnight resets, scheduled payment dates, CSV export, repeated transactions, and invalid data types. Beyond black-box functional testing, I would recommend security testing, concurrency testing, performance testing, and property-based testing for monetary invariants. The main lesson is to combine complementary techniques and link automated cases to documented rules.
