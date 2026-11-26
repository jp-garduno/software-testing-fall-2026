# Black Box Testing Analysis Report — SecureBank

## Executive Summary

Applying all four black box techniques to SecureBank surfaced a small set of
genuinely dangerous edge cases — a strict `>` waiver threshold, a
balance-dependent `unfreeze()` outcome, and state-checks that must run before
amount/funds checks — none of which would have been obvious from reading the
business rules alone. Boundary Value Analysis and State Transition Testing
were the two techniques that pulled their weight the most; Equivalence
Partitioning was the fastest to write but the least likely to catch a subtle
bug on its own.

## Technique Effectiveness

### Equivalence Partitioning

EP was effective at scaffolding the test suite quickly — once the classes
(valid amount, zero, negative, over-limit, over-balance) were identified, the
tests wrote themselves. Its main weakness showed up immediately: my first EP4
test picked $100,000 as "an amount exceeding the daily limit" without
checking that the fixture's balance ($10,000) was also exceeded, so the test
passed for the *wrong reason* — the funds check fired first, not the limit
check. EP tells you *which* classes exist, but not which other condition
might mask the one you're trying to isolate; you still have to think about
condition ordering by hand.

### Boundary Value Analysis

BVA was the most consistently valuable technique here, because SecureBank's
rules are almost entirely boundary-defined (minimums, limits, thresholds).
The waiver-threshold boundary (BV16) is the standout example: the spec says
"waived if balance > threshold," and testing the value exactly *at* the
threshold is the only way to pin down whether that comparison is `>` or `>=`
— a one-character bug that changes who gets charged a fee every month.

### Decision Tables

Decision tables were most useful for making an *implicit* precedence rule
explicit: SecureBank checks account state before checking amount or funds,
so a frozen account with a perfectly valid transfer amount still gets
rejected for being frozen, not for any funds-related reason. Writing the
table forced me to decide and document that ordering before writing a single
test; without the table, I likely would have written a transfer-validation
test suite that never independently confirmed *why* a given input failed.

### State Transition Testing

This was the only technique that caught anything a stateless test could not:
`unfreeze()` must inspect the *current balance*, not just "was frozen,"
to decide whether the account lands on Active or Suspended. Every other
technique tests a single call against a freshly constructed account; state
transition testing is what forces a sequence (`freeze()` then `unfreeze()`)
and is the only place a bug in *how state persists* between calls could hide.

## Coverage Comparison

| Technique | What it covers | Overlap with others |
| --------- | --------------- | --------------------- |
| EP | Which class of input triggers which category of outcome | Baseline that BVA refines |
| BVA | The exact operator (`>`, `>=`) at each numeric boundary | Re-executes EP's branches, adds precision EP can't provide |
| Decision Tables | Interaction/precedence between multiple simultaneous conditions | Overlaps with EP for single-condition rules, adds multi-condition cases |
| State Transitions | Correctness across a *sequence* of calls, not one call | No real overlap — the only technique that tests history-dependent behavior |

The line-coverage tool reported 100% coverage, but that number is misleading
on its own: EP alone could reach high line coverage while still missing the
`>` vs. `>=` bug BVA is designed to catch, since both branches of a boundary
condition can execute "some line" without ever executing the *boundary*
value itself. The real gap no technique here caught is concurrency — two
simultaneous transfers against the same account racing on
`daily_transfer_total` — which needs a different testing approach entirely.

## Real-World Application

In a real banking project, I would prioritize State Transition Testing and
Decision Tables first, because they encode the business rules that are most
likely to be mis-implemented as ambiguous precedence rather than simple
off-by-one errors, and those bugs are the hardest to find by code review.
BVA would run continuously alongside them for every numeric threshold, since
new boundaries are cheap to add and consistently high-value. EP would be the
first pass on any brand-new input field, mostly as a way to make sure invalid
classes are enumerated before deeper design starts.

## Recommendations

Next time, I would design the decision tables *before* the EP/BVA tables
rather than after, since the precedence rules the decision tables surfaced
(state-before-amount, amount-before-funds, funds-before-limit) would have
made several of the EP/BVA test cases easier to write correctly the first
time, instead of discovering the ordering by a failing assertion. I would
also add a small property-based/fuzz layer on top of this suite in a real
project — generating random (balance, amount, account_type) tuples and
checking invariants like "balance never goes negative" — as a complement to,
not a replacement for, these four hand-designed techniques.
