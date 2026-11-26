# Test Execution Report — SecureBank Black Box Suite

**Student**: Pablo Portillo
**Date**: 2026-09-23
**Commit under test**: branch `feat/pabloportillo1/homework-4`

---

## 1. Test Execution Summary

| Item             | Python                        | JavaScript                     |
| ---------------- | ----------------------------- | ------------------------------ |
| Framework        | pytest 9.1.1 (Python 3.11.9)  | Jest 29.7 (Node 22)            |
| Command          | `pytest -v --cov=src --cov-branch` | `npx jest --coverage --verbose` |
| Total tests      | 116                           | 116                            |
| Passed           | 116                           | 116                            |
| Failed           | 0                             | 0                              |
| Skipped          | 0                             | 0                              |
| Duration         | 0.13 s                        | 0.42 s                         |

### Coverage Summary

| Metric            | Python (`src/banking_system.py`) | JavaScript (`js/src/bankingSystem.js`) |
| ----------------- | -------------------------------- | -------------------------------------- |
| Statement/line coverage | 100% (213/213 statements)   | 100%                                    |
| Branch coverage   | 100% (76/76 branches)            | 99.15%                                  |
| Function coverage | 100%                             | 100%                                    |

The single uncovered JavaScript branch is the `active = true` default parameter of the `Payee`
constructor (`js/src/bankingSystem.js:106`): the Jest suite always passes the flag explicitly, once
as `true` and once as `false`, so the default is never taken. Python has no equivalent gap because
`coverage.py` does not treat a default argument as a branch. This is a measurement difference
between the two tools, not a hole in the test design.

Raw console logs live in `reports/logs/`. The HTML and XML coverage reports are generated on demand
(see the README for the commands) and are not committed, since CI regenerates and uploads them on
every run.

---

## 2. Results by Technique

Every test name carries its design ID, so each line below maps back to a row of
`design/test-design-document.md`.

### Equivalence Partitioning — 36 automated tests (EP1–EP35)

- ✅ Transfer amount partitions (EP1–EP7): valid, zero, negative, over limit, over balance,
  non-numeric, sub-cent, plus one test asserting that **no** invalid partition moves money.
- ✅ Account type partitions (EP8–EP12): the three supported types, an unknown type, an empty name.
- ✅ Opening balance partitions (EP13–EP16).
- ✅ Payee partitions (EP17–EP19): active, unknown, deactivated.
- ✅ Scheduled date partitions (EP20–EP22): immediate, future, past.
- ✅ History date range partitions (EP23–EP27): partial range, no range, empty result, inverted
  range, wrong bound type.
- ✅ Amount partitions re-applied to `deposit`, `pay_bill` and `create_account` (EP28–EP35).

**Findings**: EP exposed the two partitions the brief never mentions — a *deactivated* payee is not
the same input class as an *unknown* payee, and an empty result set for a date range is a valid
outcome rather than an error. Both were added to the design before implementation.

### Boundary Value Analysis — 33 automated tests (BV1–BV31)

- ✅ Checking daily limit $5,000 (BV1–BV6).
- ✅ Savings daily limit $2,000 (BV7–BV10).
- ✅ Cumulative daily limit and midnight reset, Premium $50,000 (BV11–BV14).
- ✅ Balance against the $100 Savings minimum (BV15–BV19).
- ✅ Fee waiver threshold $1,000 (BV20–BV23).
- ✅ Fee affordability against the $10 Checking fee (BV24–BV27).
- ✅ Inclusive ends of the history date range (BV28–BV31).

**Findings**: two ambiguities in the specification only became visible at the boundary.
(1) "Fee waived if balance > $1,000" means a balance of exactly $1,000.00 is **still charged** —
BV21 is the test that pins that reading down. (2) Suspension starts at $99.99, not at $100.00, so
BV17 and BV18 sit one cent apart and disagree on the resulting state. A naive implementation using
`<=` in either place passes every EP test and fails only these two.

A third finding is implementation-level: with plain floating point, `0.1 + 0.2`-style drift makes
BV2 (`$0.01`) and BV3 (`$4,999.99`) flaky. Both implementations therefore store money as integer
cents, and BV2 asserts the exact resulting balance (`19999.99`) rather than an approximation.

### Decision Tables — 31 automated tests (DT1 R1–R10, DT2 R1–R6, DT3 R1–R8, DT4 R1–R4)

- ✅ Transfer validation, including the two precedence rules: R9 (a Frozen account reports the state
  error, not the amount error) and R10 (a Suspended account obeys exactly the same funds rule as an
  Active one).
- ✅ Monthly fee processing, including the interaction case where a *successfully charged* fee pushes
  a Savings account below its minimum and suspends it.
- ✅ Bill payment validation, including the scheduled-payment rule that leaves the balance untouched.
- ✅ Account creation.

**Findings**: the example decision table in the assignment brief marks two actions for the same rule
(a frozen account with insufficient funds). Building the table properly forced an explicit
precedence — state → amount → limit → funds — which is now assumption A2 and is asserted by R9.
Without the table this ordering would have been an accident of the `if` sequence.

### State Transitions — 16 automated tests (ST1–ST13)

- ✅ Active → Suspended (transfer, ST1; unpayable monthly fee, ST9).
- ✅ Suspended → Active (ST2) and Suspended → Suspended (ST3, ST10).
- ✅ Active → Frozen (ST4) and Frozen → Active / Suspended (ST5, ST6).
- ✅ → Closed from Active and Frozen (ST7, ST11), with the CSV final statement.
- ✅ Closed rejects transfer, deposit, close, freeze, unfreeze and fee processing (ST8 + extra).
- ✅ Boundary transition: landing exactly on the minimum stays Active (ST12).
- ✅ Invalid event: `unfreeze` on an Active account is refused (ST13).

**Findings**: ST6 is the case no other technique produced. Freezing an account whose balance is
below the minimum and then unfreezing it must land in **Suspended**, not Active — otherwise
freezing becomes a way to erase the minimum-balance rule. ST12 is the overlap point with BVA: the
same boundary value is checked here for its *state* effect rather than its arithmetic.

---

## 3. Screenshots

| Evidence | File |
| -------- | ---- |
| pytest verbose run, 116 passed | `reports/screenshots/test-results-pytest.png` |
| Python coverage report (100% line, 100% branch) | `reports/screenshots/coverage-report-python.png` |
| Jest verbose run with coverage, 116 passed | `reports/screenshots/test-results-jest.png` |
| pylint 10.00/10, eslint clean, prettier clean | `reports/screenshots/quality-checks.png` |

The PNGs are terminal captures rendered from the console logs recorded in `reports/logs/` during
the run described above; the logs themselves are committed next to them so any number in this
report can be checked against the raw output.

No test failed at any point in the final run. Failures that occurred *while building* the suite are
described in section 4 below, because they are the useful part.

---

## 4. Coverage Analysis

### Which code paths are covered

All of them, in Python: 213 statements and 76 branches, 100% of each, with `--cov-branch` enabled.
That includes every error return of `transfer`, `pay_bill`, `deposit`, `apply_monthly_fee`,
`freeze`, `unfreeze`, `close`, `get_transactions` and `create_account`, plus both sides of every
state check.

### Which paths were not covered, and why

Reaching 100% took two deliberate additions after the first run, which measured **95% line / 94%
branch**. The uncovered paths were:

| Uncovered path | Why the first design missed it |
| -------------- | ------------------------------ |
| Invalid amounts in `deposit`, `pay_bill` and `create_account` | The amount partitions had been written against `transfer` only, as if they belonged to that one method rather than to the input domain. |
| `BankAccount()` constructed directly with an unknown type | `create_account` guards the type first, so the constructor's own guard was unreachable through the front door. |
| Non-finite and scientific-notation amounts | `inf` and `1e-07` are legal numeric literals that no dollar-shaped representative value would ever produce. |
| `unfreeze` on an account that is not Frozen | The state design listed valid transitions and forgot that refusing an *invalid* event is also behaviour worth asserting. |

These became EP28–EP35 and ST13, and the design document was updated before the tests were written.
That is the honest lesson of the coverage run: black box design covers *rules*, and coverage
measurement is what reveals the rules you only wrote down for one entry point.

### How coverage differs by technique

Coverage was measured per technique by running each file on its own against a clean coverage
database.

| Technique | Tests | Line coverage | Branch coverage | What it uniquely reached |
| --------- | ----- | ------------- | --------------- | ------------------------ |
| Equivalence Partitioning | 36 | 71% (161/213) | 44/76 | Every validation error branch, across all four money operations |
| Boundary Value Analysis  | 33 | 60% (141/213) | 32/76 | The comparison operators themselves (`>` vs `>=`) — few new lines, but the only tests that prove the operator is right |
| Decision Tables          | 31 | 74% (164/213) | 49/76 | Rule precedence: which guard runs first |
| State Transitions        | 16 | 72% (162/213) | 46/76 | `close`, the CSV final statement, and the Closed-account guards |
| **All four together**    | **116** | **100% (213/213)** | **76/76** | — |

Each technique on its own lands between 60% and 74%, and no single one gets close to the combined
100% — the four are genuinely complementary rather than redundant. The most useful number in the
table is the lowest one: BVA has the weakest coverage of the four (60% of lines, 32 of 76 branches)
and is still the technique that found the most real defects, because its value is in *which value*
crosses a comparison, not in how many lines it touches. A team that ranked its techniques by
coverage percentage would drop exactly the wrong one.
