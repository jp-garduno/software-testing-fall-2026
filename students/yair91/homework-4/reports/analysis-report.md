# Black Box Testing Analysis Report

**Homework 4 · Module 4**
**Author**: Emmanuel Arias (`yair91`)

## Executive Summary

Four techniques produced 87 tests against SecureBank, all passing, with 100%
statement coverage and a clean pylint run. The interesting result was not the
green suite but what each technique found on its own: the technique with the
lowest coverage number turned out to be the one protecting the rules most
likely to break.

## Technique Effectiveness

**Boundary value analysis found the most real risk.** Every genuine defect I
could imagine in this system lives on an edge: a `<=` where `<` belongs turns
"suspended below $100" into "suspended at $100", and nothing else in the suite
would notice. BV13 and BV17 — the balances landing exactly on the minimum — and
BV4 and BV10 — the transfers landing exactly on the daily limit — exist only to
catch that. It was also the easiest technique to apply, because once the
boundary is identified the values write themselves.

**Decision tables were the hardest, and the most useful for thinking.** Filling
DT1 forced a question the brief never answers: when an account is frozen _and_
short of funds _and_ over the limit, which error does the customer see? Any of
the three is defensible, but the system has to pick one and stick to it. Four of
the eight rules in DT1 exist purely to pin that precedence down. Without the
table I would have implemented whatever order felt natural and never noticed
there was a decision being made.

**State transition testing gave me the most confidence.** It is the only
technique here that tests what the system remembers. ST9 is the case I would
have missed: unfreezing an account whose balance is under the minimum should
land in Suspended, not Active, and the obvious implementation of `unfreeze`
sets the state to Active unconditionally. That is a plausible bug that no
amount of input partitioning would reach.

**Equivalence partitioning was the cheapest.** Mostly bookkeeping, but it is
what makes the others affordable: once the input space is cut into classes, BVA
knows which edges to probe and the tables know which conditions matter.

## Coverage Comparison

Running each file on its own against `src/` gave:

| Technique                | Tests | Coverage alone |
| ------------------------ | ----- | -------------- |
| Equivalence partitioning | 23    | 76%            |
| Boundary value analysis  | 23    | 47%            |
| Decision tables          | 24    | 70%            |
| State transitions        | 17    | 65%            |
| All four                 | 87    | 100%           |

The overlap is heavy — all four together add only 24 points over the best
single technique — but the ranking is upside down relative to value. BVA scores
lowest with the same test count as EP, because it hits three or four lines from
six angles instead of visiting many lines once. Coverage measures breadth and is
blind to depth, so the technique guarding the riskiest rules looks weakest.

The gap no technique closed is time: nothing tests the midnight reset firing on
its own, the fee job running on the 1st, or a scheduled payment settling when
its date arrives.

## Real-World Application

I would prioritise decision tables first, before any code, because they surface
the questions the specification never answered, and those are cheaper to settle
in a conversation than in production. Then BVA on whatever thresholds the tables
expose. State transition testing belongs wherever an entity has a lifecycle:
accounts, orders, tickets, subscriptions.

The pairing that worked best was EP then BVA on the same input: EP says where
the classes are, BVA says exactly where they end.

## Recommendations

I would do two things differently. First, write the decision tables before the
implementation rather than alongside it — I settled the validation precedence
after the code already had an order, which is backwards. Second, stop treating
100% coverage as the finish line and measure something that rewards depth;
mutation testing would have told me whether BV13 actually detects the `<=`
defect it was written for, and coverage never will.

For further testing: integration tests around the scheduler and the fee job,
property-based tests on the money arithmetic to attack the float rounding, and a
concurrency test for two transfers racing the same daily limit.
