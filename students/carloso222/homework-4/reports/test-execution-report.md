# Test Execution Report

## Test Execution Summary

- **Date**: 2026-09-22
- **Test Framework**: pytest
- **Total Tests**: 43
- **Passed**: 43
- **Failed**: 0
- **Skipped**: 0
- **Duration**: 0.14s
- **Command**: `pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html`

## Coverage Summary

- **Line Coverage**: 88%
- **Statements**: 120
- **Missed Statements**: 15
- **HTML report**: `htmlcov/index.html`

## Results by Technique

### Equivalence Partitioning

All EP tests passed. The suite covers valid and invalid transfer amounts, supported and unsupported account types, valid/invalid payees, and invalid date-range partitions.

**Defects found:** None remaining in the final run.

### Boundary Value Analysis

All BVA tests passed. The suite checks the minimum transfer, Checking and Savings daily limits, Savings minimum balance, and the strict fee-waiver threshold around $1,000.

A particularly important edge case is the exact waiver threshold: the requirement states that the fee is waived when the balance is **greater than** the threshold. Therefore exactly $1,000 in Savings still incurs the $5 fee.

### Decision Tables

All decision-table tests passed. Rules exercise combinations of funds availability, daily limit, account state, payee validity, and monthly fee conditions.

### State Transitions

All state-transition tests passed. The suite validates Active, Suspended, Frozen, and Closed behavior, including the non-reopenable Closed state.

## Coverage Analysis

The test suite executes the principal black-box behaviors of account creation, transfers, monthly-fee processing, bill payment, deposits, freezing/unfreezing, closing, reopening rejection, and transaction filtering.

The strongest overlap occurs between BVA and decision-table testing around transfer limits and fee thresholds. This overlap is intentional: BVA validates exact edge values while decision tables validate combinations of business conditions. State-transition tests cover lifecycle behavior that plain input partitioning does not capture, especially the restrictions tied to Frozen, Suspended, and Closed states.

The remaining uncovered lines correspond mostly to branches such as future-dated bill scheduling, past-date rejection, reset of the accumulated daily transfer total, some invalid unfreeze paths, and valid transaction-history filtering. These are useful candidates for extra tests but are not required to meet the assignment minimum.

## Screenshots

Add screenshots generated on your own machine before submission:

1. `reports/screenshots/test-results.png` — terminal showing all 43 tests passing.
2. `reports/screenshots/coverage-report.png` — terminal coverage table or `htmlcov/index.html`.

> The text file `reports/pytest-output.txt` contains the verified run used for this report. Do not submit fabricated screenshots; capture the real local execution.
