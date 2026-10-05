# Test Execution Report

## Test Execution Summary

- **Date**: 2026-09-23
- **Test Framework**: pytest 9.1.1
- **Platform**: win32, Python 3.14.2
- **Total Tests**: 39
- **Passed**: 39
- **Failed**: 0
- **Skipped**: 0
- **Duration**: 0.32s

## Coverage Summary

- **Line Coverage**: 78% (71 of 91 statements covered)
- **Statements Missed**: 20
- **Branch/Function Coverage**: Not measured separately (pytest-cov run without `--cov-branch`); all public methods are exercised at least once except `reset_daily_limit()` and `get_transaction_history()` date filtering, which are unused in the current design.

## Results by Technique

### Equivalence Partitioning (6 tests)

- ✅ test_ep1_valid_transfer_amount
- ✅ test_ep3_negative_transfer_amount
- ✅ test_ep7_checking_account_type
- ✅ test_ep9_undefined_account_type
- ✅ test_ep13_balance_below_minimum_suspends_account
- ✅ test_ep16_empty_payee_name

**Defects Found**: None. All 6 partitions behaved as expected per the design document.

### Boundary Value Analysis (21 tests)

- ✅ test_bva1_below_minimum
- ✅ test_bva2_minimum_valid
- ✅ test_bva4_at_limit
- ✅ test_bva5_just_above_limit
- ✅ test_bva7_below_minimum
- ✅ test_bva8_minimum_valid
- ✅ test_bva10_at_limit
- ✅ test_bva11_just_above_limit
- ✅ test_bva13_minimum_valid
- ✅ test_bva15_at_limit
- ✅ test_bva16_just_above_limit
- ✅ test_bva17_just_below_minimum_suspends
- ✅ test_bva18_at_minimum_stays_active
- ✅ test_bva19_just_above_minimum_stays_active
- ✅ test_bva23_below_waiver_fee_charged
- ✅ test_bva24_at_waiver_threshold_fee_still_charged
- ✅ test_bva25_just_above_waiver_fee_waived
- ✅ test_bva27_below_waiver_fee_charged
- ✅ test_bva28_at_waiver_threshold_fee_still_charged
- ✅ test_bva29_just_above_waiver_fee_waived
- ✅ test_bva31_just_below_minimum_suspends
- ✅ test_bva32_at_minimum_stays_active
- ✅ test_bva33_just_above_minimum_stays_active

**Defects Found**: BVA24 and BVA28 expose a specification ambiguity. The business rule states the fee is "waived if balance **>** threshold" (strictly greater than), so at the exact threshold ($1,000 for Savings, $5,000 for Checking) the fee is still charged, not waived. The implementation follows the literal rule; the original design document's "Expected Result" column for these two rows says "Fee waived," which contradicts the stated rule. This was documented as a design-vs-specification discrepancy rather than a code defect.

### Decision Tables (5 tests)

- ✅ test_rule1_funds_within_limit_active_succeeds
- ✅ test_rule2_funds_within_limit_not_active_fails
- ✅ test_rule3_funds_exceeds_limit_active_fails
- ✅ test_rule5_insufficient_funds_within_limit_active_fails
- ✅ test_rule5_invalid_payee_dominates_other_conditions

**Defects Found**: None in the tested rules. Note: Decision Table 2 (Monthly Fee Processing) was redesigned independently and its X-mark mapping was not implemented as automated tests; it should be reviewed against the business rule ("fee waived if balance > threshold") before final submission, since the current markup in the table appears to have the "waived" and "charged" columns reversed relative to that rule.

### State Transitions (5 tests)

- ✅ test_st1_active_to_suspended_on_low_balance
- ✅ test_st2_suspended_to_active_on_deposit
- ✅ test_st3_active_to_frozen_on_freeze_request
- ✅ test_st5_active_to_closed_on_close_request
- ✅ test_st8_closed_account_rejects_transfer

**Defects Found**: None. All 5 tested transitions (2 valid chains, 1 valid single transition pair, 1 valid close, 1 invalid-transition rejection) matched the state transition table exactly.

## Coverage Analysis

### Which code paths are covered?
All core validation logic used by the four testing techniques is covered: `transfer()`'s full validation chain (positive amount → sufficient funds → account active → daily limit), `pay_bill()`'s validation chain (payee → amount → funds), `_check_suspension()`, `apply_monthly_fee()`'s fee/waiver logic for Savings and Checking, and the `freeze()` / `close()` state transitions from Active.

### Which are not covered and why?
The missing 20 statements (78% → not 100%) fall into a few clear groups, confirmed via `pytest --cov-report=term-missing`:

- **`reset_daily_limit()` (lines 141-144)**: Never called by any test. This method exists to model the "daily limit resets at midnight" business rule, but no test simulates the passage of a day, since none of the four design techniques (EP, BVA, decision tables, state transitions) directly target time-based resets.
- **`get_transaction_history()` date filtering (line 161)**: The method currently returns the full history unfiltered; the `start_date`/`end_date` parameters are accepted but unused, so there's no branch to cover. This corresponds to EP20-EP24 (Date Range partitions) in the design document, which were never implemented as tests — flagged in an earlier review of `test_equivalence_partitioning.py`.
- **`unfreeze()` and `close()` error branches (lines 136, 148)**: The "account is not frozen" and "account already closed" guard clauses aren't exercised because ST4, ST6, ST7, ST9, and ST10 were cut when the state transition suite was trimmed down to 5 tests.
- **`deposit()`'s error branches (lines 86, 88)**: "Account is closed" and "Amount must be positive" guards inside `deposit()` aren't hit by any current test, since only the success path (ST2) is tested.
- **Invalid amount format check in `transfer()` (line 65)** and **account-type/initial-balance validation in `__init__` (line 25)**: these guard clauses (non-numeric transfer amount, initial deposit below minimum) aren't triggered by the current 39 tests.
- **Rules 4, 6, 7 of the Transfer Validation decision table and Rules 1-4, 6-8 of Bill Payment Validation (lines 105-113)**: only Rules 1, 2, 3, 5 (Transfer) and Rule 5 (Bill Payment) were kept when the decision table suite was trimmed to 5 tests, so the remaining rule combinations don't execute.

### How does coverage differ by technique?
Boundary Value Analysis drives the most coverage by volume (21 of 39 tests) because it exercises every numeric branch condition (`<=`, `>`, `>=`) across three account types. Equivalence Partitioning, Decision Tables, and State Transitions were each deliberately trimmed to 5-6 tests per the assignment's minimum requirements, so they cover their "happy path" and one or two dominant error cases each, but not every rule/branch in their own design tables (e.g., only 4 of 8 rules in Decision Table 1 are tested; only 1 of 8 rules in Decision Table 3 is tested). This is an intentional trade-off for a lean submission, not an oversight — but it does mean coverage would rise noticeably (likely into the low 90s%) if every designed test case were implemented instead of a representative subset.