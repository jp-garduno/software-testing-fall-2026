# Black Box Testing Analysis Report

**Student**: Pablo Portillo · **Module 4** · SecureBank Online Banking

## Executive Summary

Designing 116 test cases for SecureBank with four black box techniques produced two clear results.
First, the techniques are complementary rather than overlapping: individually they cover between
60% and 74% of the implementation, and only together do they reach 100% line and branch coverage.
Second, the technique with the *lowest* coverage, Boundary Value Analysis, is the one that found
the most genuine defects — which is a warning about ranking test techniques by coverage numbers.

## Technique Effectiveness

**Boundary Value Analysis found the most issues.** Two specification ambiguities only surfaced when
I wrote values one cent apart. The fee rule says "waived if balance > $1,000", so a balance of
exactly $1,000.00 is still charged (BV21); and an account is suspended below the minimum, so
$100.00 stays Active while $99.99 does not (BV17/BV18). Every equivalence partition test passes
under either reading of both rules. BVA also exposed an implementation defect rather than a
specification one: with plain floating point, transferring $0.01 from $20,000 gives
$19,999.989999999998, so both implementations now hold money as integer cents.

**Decision tables were the hardest to apply and the most valuable for structure.** The example
table in the brief marks two actions for a single rule — a frozen account with insufficient funds —
which is impossible for an API returning one error. Building the table forced me to fix an explicit
precedence (state → amount → limit → funds) and to test it: rule R9 asserts that a frozen account
with a negative amount reports the state error. Without the table that ordering would have been an
accident of whichever `if` I typed first.

**Equivalence Partitioning was the easiest and the widest.** It reaches every validation branch for
the least effort, and produced two input classes the brief never mentions: a deactivated payee is
not the same class as an unknown payee, and an empty date-range result is valid, not an error.

**State transition testing gave me the most confidence**, because it tests sequences rather than
single calls. Its unique find was ST6: freeze an account whose balance is below the minimum, then
unfreeze it, and it must land in Suspended, not Active — otherwise freezing becomes a way to escape
the minimum-balance rule. No single-call technique could have produced that case.

## Coverage Comparison

| Technique | Tests | Line coverage | Branch coverage | Unique contribution |
| --------- | ----- | ------------- | --------------- | ------------------- |
| Equivalence Partitioning | 36 | 71% | 44/76 | Validation errors on every operation |
| Boundary Value Analysis  | 33 | 60% | 32/76 | Correctness of each comparison operator |
| Decision Tables          | 31 | 74% | 49/76 | Precedence between guards |
| State Transitions        | 16 | 72% | 46/76 | Multi-step sequences, Closed-account guards |
| **Combined**             | **116** | **100%** | **76/76** | — |

The overlap is real but shallow. EP and BVA touch the same lines and ask different questions: EP
asks whether the rule exists, BVA asks whether its operator is `>` or `>=`. Decision tables reuse
EP's inputs but assert which error wins. The gap all four leave is temporal: nothing proves the
daily limit truly resets at midnight, because the tests call a `reset_daily_limit()` hook directly.
That needs integration testing with a controllable clock, and concurrent transfers against one
daily limit are equally invisible at this level.

## Real-World Application

I would apply them in the order EP → BVA → decision tables → state transitions, because each
narrows the next: EP maps the input domain cheaply, BVA attacks the few numeric edges EP found,
decision tables handle any rule with three or more conditions, and state transitions cover anything
with a lifecycle. For a payments system I would prioritise BVA — an off-by-one cent in a limit
check is both the most likely defect and the most expensive one.

The pairing that worked best was decision tables plus state transitions: the table says what should
happen on one call, and the state model says what should happen across several. The pairing that
misled me was EP alone — 36 passing partition tests gave a false sense of completeness until the
first boundary test contradicted the specification.

## Recommendations

Next time I would measure coverage earlier. The first run came in at 95%, and the gaps were all the
same mistake: I had written the amount partitions against `transfer` only, as if they belonged to
that method rather than to the input domain. Re-applying them to `deposit`, `pay_bill` and
`create_account` (EP28–EP35) and adding the invalid-event case ST13 closed the rest.

The design could be improved with pairwise combinations of account type and state, which I covered
only where a rule demanded it, and by asserting the CSV export against a fixed string instead of a
line count. Beyond black box work I would add property-based testing for the money arithmetic — "no
operation changes the total across two accounts" is stronger than any single boundary case — and
integration tests with a controllable clock for the midnight reset and the fee job.

*Word count: 680 words of prose (excluding tables and headings).*
