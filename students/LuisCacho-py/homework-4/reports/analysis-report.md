# Black Box Testing Analysis Report

**Student:** Luis Cacho (`LuisCacho-py`)
**Module:** 4 — Black Box Testing
**System:** SecureBank Online Banking Platform
**Word count:** ~620

---

## Executive Summary

This report analyzes the application of four black box testing techniques —
Equivalence Partitioning (EP), Boundary Value Analysis (BVA), Decision Tables
(DT), and State Transition Testing (ST) — to the SecureBank Online Banking
System. The suite achieved 83% code coverage with 71 passing tests, revealing
implementation details and edge cases not obvious from casual inspection.

---

## Technique Effectiveness

### Equivalence Partitioning

EP proved to be the best foundation technique for this project. By grouping
inputs into valid and invalid classes, it provided immediate broad coverage
without requiring knowledge of exact boundary values. The 18 EP tests covered
all five major input domains (transfer amount, account type, account balance,
payee, and date ranges) and caught the invalid-type rejection (`ValueError`)
and the whitespace-only payee case in a single pass.

The main challenge with EP was determining partition boundaries — especially
for account balance, where "below minimum" and "above minimum" feel intuitive
but the exact threshold varies per account type. EP requires discipline to
avoid over-testing valid partitions while under-testing invalid ones.

**Finding:** EP-04 revealed that the implementation checks the account balance
*before* the daily limit. This is a significant detail because a test with
$100,000 transfer and $10,000 balance returns "Insufficient funds" rather than
"Exceeds daily limit" — both correct, but the error priority matters for UX.

### Boundary Value Analysis

BVA was the highest-yield technique for finding subtle behavioral edge cases.
The discovery of the fee waiver boundary (BV-14) is a representative example:
a balance of exactly $1,000.00 in a Savings account triggers the $5.00 monthly
fee because the waiver condition is strict inequality (`balance > threshold`),
not `>=`. This single test case directly verifies a contractual business rule
that could cause customer complaints if implemented incorrectly.

BVA was the hardest technique to apply thoroughly, because boundary selection
requires understanding of every numeric threshold in the specification. With
five independent boundary groups covering transfer minimums, daily limits for
two account types, balance thresholds, and fee waivers, the risk of missing a
boundary is real. Systematic table-driven design (as documented in Section 1.2)
was essential to ensure completeness.

BVA gave the highest confidence in correctness for numerical rules because
off-by-one errors in monetary systems can have large real-world consequences.

### Decision Tables

Decision tables were most effective at ensuring that *combinations* of
conditions were tested. The transfer validation table (8 rules) forced testing
of scenarios such as "frozen account with insufficient funds attempting a
transfer above the daily limit" — a combination that would be easy to miss
with EP or BVA alone.

The technique was straightforward to apply once the conditions were identified.
The main challenge was ensuring that conditions were truly independent; in the
fee processing table, the account type determines both the fee amount and the
threshold, so they cannot be treated as fully orthogonal.

**Finding:** DT revealed validation priority in the transfer function: the
account state (Frozen/Closed) is checked first, then balance, then daily
limit. This prioritization is implicit in the code and not stated in the spec.

### State Transition Testing

State testing was the most distinctive technique. Without it, the complex
interactions between account state and other operations would remain largely
untested. ST-07 was particularly important: it confirmed that Suspended accounts
are *not* rejected at the state level — only Frozen and Closed accounts are.
This is a subtle distinction with real user impact.

ST also excels at finding defects in multi-step scenarios (ST-17, ST-18),
where a freeze-then-unfreeze cycle or a low-balance-then-deposit sequence could
leave the system in an inconsistent state.

---

## Coverage Comparison

| Technique | Tests | Strengths                          | Weaknesses                        | Overlap |
|-----------|-------|------------------------------------|-----------------------------------|---------|
| EP        | 18    | Broad, quick structural coverage   | Misses off-by-one errors          | High    |
| BVA       | 17    | Precise numerical edge cases       | Time-consuming boundary selection | Medium  |
| DT        | 17    | Condition combinations             | Can explode in size               | Medium  |
| ST        | 19    | Lifecycle and sequential behavior  | Only models documented states     | Low     |

The overlap between EP and DT is high because many decision table rules
correspond directly to equivalence partitions. The unique contribution of BVA
is numerical precision; the unique contribution of ST is temporal (multi-step)
coverage.

No black box technique covered the CSV export utility or the system-level
`process_all_monthly_fees()` sweep — these were outside the scope of the
business-rule-focused test design.

---

## Real-World Application

In a professional banking system, I would apply these techniques in the
following priority order:

1. **Decision Tables first** — for complex business rules involving multiple
   conditions. Banking systems are rule-dense; tables make rules explicit and
   reviewable by non-technical stakeholders (compliance, legal).
2. **BVA second** — for every monetary threshold. Off-by-one errors in fee
   waivers, transfer limits, or minimum balances have direct financial and
   regulatory consequences.
3. **ST third** — for account lifecycle. Regulatory audits often focus on
   whether closed accounts can be re-opened or what happens at account
   suspension — states are critical.
4. **EP last** — as a completeness check to ensure all input classes are
   covered.

The combination of DT + BVA is particularly powerful for financial systems
because DT handles qualitative rules (who can do what) while BVA handles
quantitative limits (how much).

---

## Recommendations

1. **Add mutation testing** to verify that the test suite actually catches bugs.
   All 71 tests passed against the correct implementation; mutation testing
   would confirm they would fail against incorrect implementations.

2. **Increase coverage of utility paths**: the CSV export and system-wide fee
   sweep (uncovered 17%) are integration points that should be tested with
   additional integration tests.

3. **Parameterize BVA tests** using `pytest.mark.parametrize` to reduce
   duplication and make it easier to add new boundary values (e.g., Premium
   account balance boundaries).

4. **Add property-based tests** (e.g., with Hypothesis) to complement black
   box testing with automated boundary discovery. This is especially valuable
   for the transfer amount domain where floating-point rounding may introduce
   unexpected behaviors.

---

## Lessons Learned

The most important insight from this assignment was that **no single black box
technique is sufficient**. EP gave coverage breadth but missed the `$1,000.00
vs $1,000.01` fee waiver issue that BVA caught. DT revealed validation
priorities that EP and BVA did not expose. ST caught the Suspended-vs-Frozen
distinction that all three other techniques missed. Black box testing is most
effective as a portfolio of complementary techniques applied systematically.
