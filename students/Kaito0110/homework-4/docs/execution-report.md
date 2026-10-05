# Test Execution Report — SecureBank Black Box Testing Suite

**Student**: Kaito0110
**Assignment**: Homework 4 — Black Box Testing
**Execution Date**: 2026-09-23
**Environment**: Python 3.10.8, pytest 9.1.1, pytest-cov 7.1.0, Windows

---

## Summary

| Metric          | Value        |
| --------------- | ------------ |
| Total Tests     | 69           |
| Passed          | 69 ✅        |
| Failed          | 0            |
| Errors          | 0            |
| Skipped         | 0            |
| Coverage (src/) | **93%**      |
| Execution Time  | 0.86 seconds |

---

## Test Execution Command

```bash
pytest students/Kaito0110/homework-4/tests/test_banking.py -v \
  --cov=students/Kaito0110/homework-4/src \
  --cov-report=term-missing
```

---

## Results by Technique

### Equivalence Partitioning (16 tests)

| Test ID | Test Name                                 | Result  |
| ------- | ----------------------------------------- | ------- |
| EP1     | test_ep1_valid_transfer_amount            | ✅ PASS |
| EP2     | test_ep2_zero_transfer_amount             | ✅ PASS |
| EP3     | test_ep3_negative_transfer_amount         | ✅ PASS |
| EP4     | test_ep4_transfer_exceeds_daily_limit     | ✅ PASS |
| EP5     | test_ep5_transfer_exceeds_balance         | ✅ PASS |
| EP6     | test_ep6_savings_account_valid_type       | ✅ PASS |
| EP7     | test_ep7_checking_account_valid_type      | ✅ PASS |
| EP8     | test_ep8_premium_account_valid_type       | ✅ PASS |
| EP9     | test_ep9_balance_above_minimum_active     | ✅ PASS |
| EP10    | test_ep10_balance_below_minimum_suspended | ✅ PASS |
| EP11    | test_ep11_checking_zero_balance_active    | ✅ PASS |
| EP12    | test_ep12_valid_payee                     | ✅ PASS |
| EP13    | test_ep13_invalid_payee                   | ✅ PASS |
| EP14    | test_ep14_valid_date_range                | ✅ PASS |
| EP15    | test_ep15_invalid_date_range              | ✅ PASS |
| EP16    | test_ep16_no_date_filter                  | ✅ PASS |

**EP Subtotal: 16/16 ✅**

---

### Boundary Value Analysis (19 tests)

| Test ID | Test Name                                  | Result  |
| ------- | ------------------------------------------ | ------- |
| BV1     | test_bv1_transfer_below_minimum            | ✅ PASS |
| BV2     | test_bv2_transfer_at_minimum               | ✅ PASS |
| BV3     | test_bv3_transfer_just_below_limit         | ✅ PASS |
| BV4     | test_bv4_transfer_at_limit                 | ✅ PASS |
| BV5     | test_bv5_transfer_just_above_limit         | ✅ PASS |
| BV6     | test_bv6_transfer_far_above_limit          | ✅ PASS |
| BV7     | test_bv7_savings_transfer_just_below_limit | ✅ PASS |
| BV8     | test_bv8_savings_transfer_at_limit         | ✅ PASS |
| BV9     | test_bv9_savings_transfer_just_above_limit | ✅ PASS |
| BV10    | test_bv10_balance_at_minimum               | ✅ PASS |
| BV11    | test_bv11_balance_just_below_minimum       | ✅ PASS |
| BV12    | test_bv12_balance_just_above_minimum       | ✅ PASS |
| BV13    | test_bv13_fee_waiver_above_threshold       | ✅ PASS |
| BV14    | test_bv14_fee_waiver_at_threshold          | ✅ PASS |
| BV15    | test_bv15_fee_charged_below_threshold      | ✅ PASS |
| BV16    | test_bv16_premium_at_minimum               | ✅ PASS |
| BV17    | test_bv17_premium_below_minimum            | ✅ PASS |
| BV18    | test_bv18_bill_payment_zero_amount         | ✅ PASS |
| BV19    | test_bv19_bill_payment_positive_amount     | ✅ PASS |

**BVA Subtotal: 19/19 ✅**

---

### Decision Tables (13 tests)

| Test ID | Test Name                                         | Result  |
| ------- | ------------------------------------------------- | ------- |
| DT1-R1  | test_dt1_rule1_all_conditions_met                 | ✅ PASS |
| DT1-R2  | test_dt1_rule2_account_frozen                     | ✅ PASS |
| DT1-R3  | test_dt1_rule3_exceeds_limit_active               | ✅ PASS |
| DT1-R4  | test_dt1_rule4_exceeds_limit_frozen               | ✅ PASS |
| DT1-R5  | test_dt1_rule5_insufficient_funds_active          | ✅ PASS |
| DT1-R6  | test_dt1_rule6_insufficient_funds_frozen          | ✅ PASS |
| DT1-R7  | test_dt1_rule7_insufficient_and_over_limit_active | ✅ PASS |
| DT1-R8  | test_dt1_rule8_all_bad_frozen                     | ✅ PASS |
| DT2-R1  | test_dt2_rule1_savings_above_threshold            | ✅ PASS |
| DT2-R2  | test_dt2_rule2_savings_below_threshold            | ✅ PASS |
| DT2-R3  | test_dt2_rule3_checking_above_threshold           | ✅ PASS |
| DT2-R4  | test_dt2_rule4_checking_below_threshold           | ✅ PASS |
| DT2-R5  | test_dt2_rule5_premium_no_fee                     | ✅ PASS |
| DT3-R1  | test_dt3_rule1_valid_bill_payment                 | ✅ PASS |
| DT3-R2  | test_dt3_rule2_frozen_account_bill                | ✅ PASS |
| DT3-R3  | test_dt3_rule3_zero_amount_bill                   | ✅ PASS |
| DT3-R4  | test_dt3_rule4_invalid_payee_bill                 | ✅ PASS |

**DT Subtotal: 17/17 ✅** _(includes 4 additional DT3 tests)_

---

### State Transition Testing (17 tests)

| Test ID | Test Name                                   | Result  |
| ------- | ------------------------------------------- | ------- |
| ST1     | test_st1_active_to_suspended_on_low_balance | ✅ PASS |
| ST2     | test_st2_suspended_to_active_on_deposit     | ✅ PASS |
| ST3     | test_st3_active_to_frozen_on_freeze_request | ✅ PASS |
| ST4     | test_st4_frozen_to_active_on_unfreeze       | ✅ PASS |
| ST5     | test_st5_active_to_closed                   | ✅ PASS |
| ST6     | test_st6_suspended_to_closed                | ✅ PASS |
| ST7     | test_st7_frozen_to_closed                   | ✅ PASS |
| ST8     | test_st8_closed_transfer_rejected           | ✅ PASS |
| ST9     | test_st9_closed_deposit_rejected            | ✅ PASS |
| ST10    | test_st10_closed_cannot_be_reopened         | ✅ PASS |
| ST11    | test_st11_suspended_cannot_transfer         | ✅ PASS |
| ST12    | test_st12_fee_causes_suspension             | ✅ PASS |
| ST+     | test_scheduled_bill_payment_future_date     | ✅ PASS |
| ST+     | test_scheduled_bill_payment_past_date       | ✅ PASS |
| ST+     | test_daily_limit_cumulative                 | ✅ PASS |
| ST+     | test_premium_large_transfer                 | ✅ PASS |
| ST+     | test_unfreeze_non_frozen_account_error      | ✅ PASS |

**ST Subtotal: 17/17 ✅**

---

## Coverage Report

```
Name                                            Stmts   Miss  Cover   Missing
-----------------------------------------------------------------------------
students\Kaito0110\homework-4\src\__init__.py       0      0   100%
students\Kaito0110\homework-4\src\banking.py      137      9    93%   133, 155, 157, 178, 207, 221, 223, 249, 275
-----------------------------------------------------------------------------
TOTAL                                             137      9    93%
```

**Coverage: 93%** — exceeds the required 80% threshold ✅

The uncovered lines (9 total) correspond to edge-case branches within the `get_transaction_history` date filtering logic and the `export to CSV` stub, which are not fully exercised by the black-box test set but represent internal implementation details not required by the specification.

---

## Notes

- Initial run revealed 2 failures caused by fixture setup (insufficient account balance for boundary tests). Both were corrected by creating dedicated accounts with adequate funds.
- All 69 tests pass after corrections.
- Tests are fully independent — each creates its own account instances to avoid state pollution between tests.
