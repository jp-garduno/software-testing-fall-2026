# Test Execution Report — SecureBank Black Box Test Suite

## Test Execution Summary

- **Date**: 2026-09-23
- **Test Framework**: pytest 8.4.2 (with pytest-cov)
- **Total Tests**: 75
- **Passed**: 75
- **Failed**: 0
- **Skipped**: 0
- **Duration**: ~0.1s

## Coverage Summary

- **Line Coverage**: 100% (103/103 statements in `src/banking_system.py`)
- **Function Coverage**: 100% (every public method and helper function is exercised)
- **Branch note**: `pytest-cov`'s default report here is statement (line) coverage,
  not a separate branch-coverage number; see "Coverage Analysis" below for how
  branch-level coverage was verified by hand for the highest-risk conditionals.

---

## Results by Technique

### Equivalence Partitioning (23 tests)

File: `tests/test_equivalence_partitioning.py`

- ✅ `test_ep1_valid_amount_within_limits`
- ✅ `test_ep2_zero_amount`
- ✅ `test_ep3_negative_amount`
- ✅ `test_ep4_amount_exceeds_daily_limit`
- ✅ `test_ep5_amount_exceeds_balance`
- ✅ `test_ep6_valid_type_savings`
- ✅ `test_ep7_valid_type_checking`
- ✅ `test_ep8_valid_type_premium`
- ✅ `test_ep9_invalid_type`
- ✅ `test_ep10_blank_type`
- ✅ `test_ep9b_invalid_type_raises_on_account_creation`
- ✅ `test_ep2b_deposit_non_positive_amount_rejected`
- ✅ `test_ep11_balance_above_minimum_is_active`
- ✅ `test_ep12_balance_below_minimum_is_suspended`
- ✅ `test_ep13_balance_at_minimum_is_active`
- ✅ `test_ep14_valid_payee`
- ✅ `test_ep15_empty_payee`
- ✅ `test_ep16_whitespace_payee`
- ✅ `test_ep17_none_payee`
- ✅ `test_ep18_valid_range_start_before_end`
- ✅ `test_ep19_valid_range_single_day`
- ✅ `test_ep20_invalid_range_start_after_end`
- ✅ `test_ep21_valid_range_no_matches`

**Defects found**: One test-design bug caught during implementation, not a
production defect: `test_ep4` originally reused the `checking_account` fixture
(balance $10,000) to test an amount exceeding the $5,000 daily limit, but
$100,000 also exceeds that balance — the *funds* check fires first in the
implementation, so the test was asserting the wrong error message. Fixed by
isolating the daily-limit partition with a dedicated high-balance account so
only one condition varies at a time — exactly the "one assertion, one cause"
principle Part 1 documents.

### Boundary Value Analysis (21 tests)

File: `tests/test_boundary_values.py`

- ✅ `test_bv1_below_minimum_amount` … `test_bv6_far_above_daily_limit` (Checking limit)
- ✅ `test_daily_limit_resets_on_a_new_day`
- ✅ `test_bv7_just_below_savings_limit` … `test_bv9_just_above_savings_limit` (Savings limit)
- ✅ `test_bv10_just_below_minimum_suspends` … `test_bv12_just_above_minimum_stays_active` (Savings minimum balance)
- ✅ `test_bv13_just_below_minimum_suspends` … `test_bv15_just_above_minimum_stays_active` (Premium minimum balance)
- ✅ `test_bv16_balance_at_threshold_fee_charged` … `test_bv18_balance_just_below_threshold_fee_charged` (fee waiver threshold)
- ✅ `test_bv19_balance_just_below_fee_amount_suspends`, `test_bv20_balance_exactly_at_fee_amount_succeeds` (insufficient funds for fee)

**Defects found**: None in the implementation. BV16 is worth calling out
specifically: the design document flags that the waiver threshold is
implemented as strictly `> threshold`, so a balance sitting *exactly* on the
threshold ($1,000.00 for Savings) still gets charged. A naive `>=`
implementation would have silently waived that account's fee — BV16 is the
one test in the whole suite that would fail if someone "fixed" the comparison
operator without re-reading the spec.

### Decision Tables (16 tests)

File: `tests/test_decision_tables.py`

- ✅ 6 tests for Decision Table 1 (Transfer Validation): success, exceeds-limit,
  insufficient-funds, non-positive-amount, frozen, closed
- ✅ 5 tests for Decision Table 2 (Monthly Fee Processing): Savings waived,
  Savings charged, Checking waived, Checking insufficient (suspends), Premium
  (always $0)
- ✅ 5 tests for Decision Table 3 (Bill Payment Validation): success, frozen,
  invalid payee, non-positive amount, insufficient funds

**Defects found**: None. These tests specifically pin the *precedence* decision
documented in the design (account state is checked before amount/funds), by
verifying that a frozen account is rejected with the frozen-specific message
rather than an unrelated funds/limit error.

### State Transitions (15 tests)

File: `tests/test_state_transitions.py`

- ✅ ST1–ST7: all valid transitions (Active→Suspended, Suspended→Active,
  Active→Frozen, Frozen→Active, Frozen→Suspended, Active→Closed, Suspended→Closed)
- ✅ ST8–ST10: invalid transitions from/around Closed and Frozen
- ✅ ST11–ST15: additional invalid-transition and edge cases (deposit/freeze/fee
  on a Closed account, unfreezing a non-Frozen account, a fee charge that
  itself triggers suspension)

**Defects found**: None, but ST4 vs. ST5 (`unfreeze()` landing on Active vs.
Suspended depending on current balance) is the highest-value pair in this
group — an implementation that always unfreezes straight to `Active` without
re-checking the balance would pass every other test in the suite and fail
only here.

---

## Screenshots

This assignment was completed in a non-interactive terminal environment
without a GUI, so raw terminal output was captured as text instead of image
screenshots:

- `reports/screenshots/test-results.txt` — full `pytest -v` verbose output (all 75 tests, PASSED)
- `reports/screenshots/coverage-report.txt` — `pytest --cov=src --cov-report=term-missing` output (100% coverage)
- `htmlcov/index.html` (generated locally by `pytest --cov-report=html`, excluded from the
  repository via `.gitignore` since it's a regeneratable build artifact — run the command
  in the README to reproduce it)

---

## Coverage Analysis

- **What's covered**: Every statement in `src/banking_system.py` is executed —
  all four `BankAccount` state-changing methods (`transfer`, `deposit`,
  `freeze`, `unfreeze`, `close`, `apply_monthly_fee`), every account-type rule
  branch (Savings/Checking/Premium), the module-level validation helpers
  (`validate_account_type`, `validate_bill_payment`,
  `filter_transactions_by_date`), and the `ValueError` raised for an
  unrecognized account type at construction time.
- **Branch coverage, verified manually**: line coverage alone can hide an
  untested branch of an `if/else` that both still execute *some* line in the
  function. The two branches most worth checking by hand were:
  - `unfreeze()`'s `"Active" if balance >= min else "Suspended"` — both arms
    are exercised (ST4 and ST5 respectively).
  - `apply_monthly_fee()`'s three-way branch (waived / charged / insufficient)
    — all three arms are exercised (BV17 waived, BV16/BV18 charged, BV19
    insufficient).
- **How coverage differs by technique**: EP and Decision Table tests mostly
  cover *which branch* is taken (the `if`/`elif` conditions themselves); BVA
  tests re-execute the *same* branches EP already covers, but their value
  isn't new line coverage — it's confirming the comparison operator at each
  branch boundary is the correct one (`>`, `>=`, `<`, `<=`), which line
  coverage cannot detect on its own. State Transition tests are the only
  technique that specifically exercises *sequences* of calls (freeze then
  unfreeze; suspend then deposit then check Active again) rather than a
  single call in isolation, so they are what would catch a bug in how state
  persists across the account's lifecycle rather than within one method.
- **Nothing is currently uncovered.** If the system were extended, the
  weakest area for a next iteration would be concurrent/simultaneous
  transfers against the same account (a race on `daily_transfer_total`),
  which no black box technique here targets since it requires a concurrency
  (not input-based) testing approach.
