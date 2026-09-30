# Test Execution Report - SecureBank

## 1. Test Execution Summary

| | Python (pytest) | JavaScript (Jest) |
|---|---|---|
| **Date** | 2026-09-23 | 2026-09-23 |
| **Framework** | pytest 8.4.2 / pytest-cov 7.1.0 (Python 3.9.6) | Jest 29 (Node 24) |
| **Total tests** | 183 | 184 |
| **Passed** | 183 | 184 |
| **Failed / Skipped** | 0 / 0 | 0 / 0 |
| **Duration** | 0.24 s | 0.31 s |
| **Line (statement) coverage** | 100% (234/234) | 100% |
| **Branch coverage** | 100% (108/108 branches) | 98.9% |
| **Function coverage** | 100% | 100% |
| **pylint (course rc) / eslint** | 10.00/10 | 0 findings |

Commands: `pytest -v --cov=src --cov-branch --cov-report=term --cov-report=html` and `npm test -- --coverage --verbose`.
(Test counts include parametrized cases; the number of test *functions* is lower.)

## 2. Results by Technique (Python)

### Equivalence Partitioning - 46 tests, all passing (`tests/test_equivalence_partitioning.py`)
- ✅ EP1 valid transfer, EP2 zero, EP3 negative, EP4 over limit, EP5 over balance, EP6 non-numeric (6 values), EP7 >2 decimals
- ✅ EP8-EP10 limits per account type, EP11 invalid type
- ✅ EP12-EP15 opening balance partitions
- ✅ EP16-EP19 account state partitions
- ✅ EP20-EP23 payee partitions, EP24-EP27 payment date partitions
- ✅ EP28-EP34 history date range partitions, EP35-EP37 deposit and date-type partitions

**Defects found**: none in the implementation. Writing the partitions did expose 11 specification ambiguities
(design document, section 0) such as whether Suspended accounts may transact and whether the daily limit is cumulative.

### Boundary Value Analysis - 59 tests, all passing (`tests/test_boundary_values.py`)
- ✅ BV1-BV6 Checking limit $5,000, BV7-BV11 Savings limit $2,000, BV12-BV16 amount vs balance
- ✅ BV17-BV22 balance vs minimum (Savings, Premium), BV23-BV27 cumulative limit and midnight reset
- ✅ BV28-BV34 fee waiver thresholds, BV35-BV37 fee affordability, BV38-BV42 fee day of month
- ✅ BV43-BV48 opening balance, BV49-BV52 decimal precision, BV53-BV56 history dates, BV57-BV59 payment dates

**Defects found**: none in the final code. Two items found *while building* the oracle: (1) `$0.001` / `$10.005` must be
rejected as sub-cent amounts, which is why amounts are validated with `Decimal` and not float arithmetic; (2) `1000 - 0.01`
style balances need cent-rounding (`round(..., 2)`) or `balance == 999.99` comparisons break.

### Decision Tables - 44 tests, all passing (`tests/test_decision_tables.py`)
- ✅ DT1 R1-R8 (parametrized truth table) + R9-R13 (closed, bad destination, own-account move, self transfer, suspended destination)
- ✅ DT2 R1-R11 monthly fee (waived / charged / suspended / unpaid / premium / wrong day / frozen / invalid date / suspended)
- ✅ DT3 R1-R10 bill payment (including multi-error reporting)
- ✅ DT4 R1-R6 account creation and information update

**Defects found**: one **test-suite gap** (not a code bug): the mutation check (section 5) showed that my first version
of the suite did not detect a mutant that stopped Suspended accounts from receiving transfers / paying fees.
Rules DT1-R13 and DT2-R11 were added and the mutant is now killed.

### State Transitions - 34 tests, all passing (`tests/test_state_transitions.py`)
- ✅ ST1-ST13 valid transitions (Active->Suspended via transfer, bill payment and fee; Suspended->Active; freeze / unfreeze; close from 3 states)
- ✅ ST14-ST21 invalid transitions and the Closed absorbing state (9 events), lifecycle path
- ✅ ST22-ST25 history, CSV export (+ quoting), closed-account visibility, update while frozen

**Defects found**: none.

The JavaScript suite mirrors these files one-to-one (47 / 59 / 44 / 34 tests, all passing).

## 3. Screenshots

| | |
|---|---|
| Python test results (`pytest -v`) | ![pytest](screenshots/test-results.png) |
| Python coverage, terminal | ![cov term](screenshots/coverage-summary-terminal.png) |
| Python coverage, HTML report | ![cov html](screenshots/coverage-report.png) |
| Per-file HTML coverage | ![cov file](screenshots/coverage-report-banking-system.png) |
| Jest results and coverage | ![jest](screenshots/test-results-js.png) |
| Mutation check | ![mutation](screenshots/mutation-check.png) |
| Lint (pylint / eslint) | ![lint](screenshots/lint.png) |

The terminal images are the real captured output of the commands, rendered to PNG with headless Chromium; the HTML
coverage images are direct screenshots of `htmlcov/`. No test failed during the final run, so there are no failure
screenshots. Failures did occur once while developing: running a single Jest file trips the global coverage threshold (section 4), and the
first mutation run left one survivor (section 5).

## 4. Coverage Analysis

**Covered**: every statement and function of `banking_system.py` / `bankingSystem.js`; all 108 branches (Python) and 98.9% of branches in JavaScript.

**Not covered**: nothing in Python. In JavaScript two defensive branches remain (default arguments `extra = {}` in `ok()` and `{ owner, email } = {}` in `updateInfo` that are never used without an argument). None is business logic. (An earlier run left one Python branch, `update_info` with only `owner`, uncovered; DT4-R6 was added for it.)

**Coverage by technique** (each file run alone, Python, statements / branches):

| Technique alone | Statement cover |
|---|---|
| EP | 73% |
| BVA | 67% |
| Decision tables | 84% |
| State transitions | 79% |
| **All four** | **100%** (100% branches) |

No single technique reaches full coverage: EP and BVA concentrate on `transfer`, `validate_amount` and date handling,
decision tables reach fees, bill payments and creation, state tests reach lifecycle and history. The union reaches 100%,
which is the argument for combining them. Note that 100% coverage is a by-product here, not the goal: the mutation check
(16 injected defects, 16 killed) is a stronger signal of suite quality than the coverage number.
(Running a Jest file alone trips the 80% coverage threshold in `package.json`; that only matters for the per-file runs used in this table, not `npm test`.)

## 5. Mutation Check

`python tools/mutation_check.py` - 16 mutants (off-by-one on limits, minimums, thresholds, day-of-month, inclusive date
bounds, wrong limit constant, missing state guards). Result: **16 killed, 0 survived**. BVA detected 13 of the 16; the state-guard mutants M11 and M16 were detected *only* by the state transition tests, and M15 *only* by the decision tables.
See `screenshots/mutation-check.png`.
