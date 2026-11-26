# Reflection — Homework 4: Black Box Testing Suite

**Student**: Isaac Vazquez (isaac-evs)

## What was most challenging?

The hardest part wasn't writing individual tests — it was resolving the
ambiguities in the business rules *before* writing them. The spec says fees
are "waived if balance > threshold" and daily limits reset "at midnight," but
neither statement says what happens at the exact boundary, or how a test can
deterministically simulate "midnight" without depending on the real clock. I
had to make the transfer's daily-limit check accept an explicit `today`
parameter so tests could control the date directly, rather than relying on
`date.today()` and getting flaky, order-dependent results.

## What did I learn about black box testing?

That the four techniques aren't redundant with each other — each one catches
a different category of bug. Equivalence Partitioning found the missing
error-message coverage fastest, Boundary Value Analysis was the only thing
that could catch a `>` vs. `>=` typo on the fee waiver, Decision Tables were
what made me *decide* that account-state checks must run before amount
checks (an ordering the prose spec never states outright), and State
Transition Testing was the only technique that caught a bug involving two
calls in sequence (`freeze()` then `unfreeze()`) instead of one call in
isolation. Line coverage alone (100% here) would not have told me any of
that on its own.

## How confident am I in the quality of the banking system?

Fairly confident for the rules this suite actually covers — every documented
business rule has at least one test pinned to its exact boundary or
precedence decision. I would not yet trust it under concurrent access (two
transfers racing against the same account), since none of the four
techniques here are designed to catch that class of bug.
