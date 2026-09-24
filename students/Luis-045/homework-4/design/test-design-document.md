# SecureBank Black Box Test Design Document

## Equivalence Partitioning

The automated Equivalence Partitioning suite contains 9 tests. The IDs below are aligned with the current test docstrings.

### Input 1: Transfer Amount

| Partition ID | Description | Type | Representative Value | Expected Result | Automated |
|---|---|---|---|---|---|
| EP1 | Valid transfer amount within account rules | Valid | $500 | Transfer succeeds | Yes |
| EP2 | Zero transfer amount | Invalid | $0 | Error: Amount must be positive | Yes |
| EP3 | Negative transfer amount | Invalid | -$100 | Error: Amount must be positive | Yes |
| EP4 | Amount exceeds daily transfer limit | Invalid | $5,000.01 for Checking | Error: Exceeds daily limit | Yes |
| EP5 | Amount exceeds available balance | Invalid | Balance + $1 | Error: Insufficient funds | Yes |

### Input 2: Account Type

| Partition ID | Description | Type | Representative Value | Expected Result | Automated |
|---|---|---|---|---|---|
| EP6 | Unsupported account type | Invalid | Business | Error: Invalid account type | Yes |
| EP10 | Supported Savings account | Valid | Savings | Account created using Savings rules | No |
| EP11 | Supported Checking account | Valid | Checking | Account created using Checking rules | No |
| EP12 | Supported Premium account | Valid | Premium | Account created using Premium rules | No |

### Input 3: Initial Balance

| Partition ID | Description | Type | Representative Value | Expected Result | Automated |
|---|---|---|---|---|---|
| EP7 | Negative initial balance | Invalid | -$1 | Error: Initial balance cannot be negative | Yes |
| EP13 | Zero initial balance | Valid | $0 | Account is created | No |
| EP14 | Positive initial balance | Valid | $2,000 | Account is created | No |

### Input 4: Deposit Amount

| Partition ID | Description | Type | Representative Value | Expected Result | Automated |
|---|---|---|---|---|---|
| EP8 | Zero deposit amount | Invalid | $0 | Error: Amount must be positive | Yes |
| EP15 | Positive deposit amount | Valid | $100 | Deposit succeeds | No |
| EP16 | Negative deposit amount | Invalid | -$100 | Error: Amount must be positive | No |

### Input 5: Payee

| Partition ID | Description | Type | Representative Value | Expected Result | Automated |
|---|---|---|---|---|---|
| EP9 | Non-string payee | Invalid | 12345 | Error: Invalid payee | Yes |
| EP17 | Valid string payee | Valid | Electricity | Bill payment may proceed to the remaining validations | No |
| EP18 | Empty payee | Invalid | Empty string | Error: Invalid payee | No |

---

## Boundary Value Analysis

The design covers five important boundaries. The IDs used by the six automated BVA tests match the current test docstrings; additional rows represent designed boundary cases that are not separately automated.

### Boundary 1: Minimum Transfer Amount ($0.01)

| Test ID | Boundary Position | Test Value | Expected Result | Automated |
|---|---|---:|---|---|
| BV7 | Below minimum | -$0.01 | Error: Amount must be positive | No |
| BV1 | Immediately below minimum | $0.00 | Error: Amount must be positive | Yes |
| BV2 | At minimum | $0.01 | Transfer succeeds | Yes |
| BV8 | Just above minimum | $0.02 | Transfer succeeds | No |

### Boundary 2: Checking Daily Transfer Limit ($5,000)

| Test ID | Boundary Position | Test Value | Expected Result | Automated |
|---|---|---:|---|---|
| BV3 | Just below limit | $4,999.99 | Transfer succeeds | Yes |
| BV4 | At limit | $5,000.00 | Transfer succeeds | Yes |
| BV5 | Just above limit | $5,000.01 | Error: Exceeds daily limit | Yes |
| BV9 | Far above limit | $6,000.00 | Error: Exceeds daily limit | No |

### Boundary 3: Savings Daily Transfer Limit ($2,000)

| Test ID | Boundary Position | Test Value | Expected Result | Automated |
|---|---|---:|---|---|
| BV10 | Just below limit | $1,999.99 | Transfer succeeds | No |
| BV11 | At limit | $2,000.00 | Transfer succeeds | No |
| BV6 | Just above limit | $2,000.01 | Error: Exceeds daily limit | Yes |
| BV12 | Far above limit | $3,000.00 | Error: Exceeds daily limit | No |

### Boundary 4: Savings Minimum Balance ($100)

| Test ID | Boundary Position | Balance After Transaction | Expected Result | Automated |
|---|---|---:|---|---|
| BV13 | Just below minimum | $99.99 | Account becomes Suspended | No |
| BV14 | At minimum | $100.00 | Account remains Active | No |
| BV15 | Just above minimum | $100.01 | Account remains Active | No |
| BV16 | Above minimum | $150.00 | Account remains Active | No |

### Boundary 5: Checking Fee Waiver Threshold ($5,000)

| Test ID | Boundary Position | Balance | Expected Result | Automated |
|---|---|---:|---|---|
| BV17 | Just below threshold | $4,999.99 | $10 fee charged | No |
| BV18 | At threshold | $5,000.00 | $10 fee charged | No |
| BV19 | Just above threshold | $5,000.01 | Fee waived | No |
| BV20 | Well above threshold | $6,000.00 | Fee waived | No |

---

## Decision Tables

The automated Decision Table suite contains 14 tests distributed across transfer validation, monthly fee processing, and bill payment validation.

### Decision Table 1: Transfer Validation

| Condition / Action | Rule 1 | Rule 2 | Rule 3 | Rule 4 |
|---|---|---|---|---|
| Account Active? | Y | N | Y | Y |
| Amount positive? | Y | Y | Y | Y |
| Within daily limit? | Y | Y | N | Y |
| Sufficient funds? | Y | Y | Y | N |
| **Transfer succeeds** | X | | | |
| **Error: Account is not active** | | X | | |
| **Error: Exceeds daily limit** | | | X | |
| **Error: Insufficient funds** | | | | X |

### Decision Table 2: Monthly Fee Processing

| Condition / Action | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 | Rule 6 |
|---|---|---|---|---|---|---|
| Account Closed? | N | N | N | N | N | Y |
| Account Type | Savings | Savings | Checking | Checking | Premium | Any |
| Balance above waiver threshold? | Y | N | Y | N | - | - |
| Fee causes balance below minimum? | - | N | - | - | - | - |
| **Charge $5 fee** | | X | | | | |
| **Charge $10 fee** | | | | X | | |
| **Waive fee** | X | | X | | X | |
| **Reject processing** | | | | | | X |

A Savings fee may also move the account to Suspended when the fee reduces the balance below the $100 minimum.

### Decision Table 3: Bill Payment Validation

| Condition / Action | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 |
|---|---|---|---|---|---|
| Account Active? | Y | N | Y | Y | Y |
| Valid payee? | Y | - | N | Y | Y |
| Amount positive? | Y | - | - | N | Y |
| Sufficient funds? | Y | - | - | - | N |
| **Payment succeeds** | X | | | | |
| **Error: Account is not active** | | X | | | |
| **Error: Invalid payee** | | | X | | |
| **Error: Amount must be positive** | | | | X | |
| **Error: Insufficient funds** | | | | | X |

### Automated Decision Table Test Cases

| Test ID | Area | Scenario | Expected Result |
|---|---|---|---|
| DT1 | Transfer | Active account, sufficient funds, within daily limit | Transfer succeeds |
| DT2 | Transfer | Frozen account attempts transfer | Error: Account is not active |
| DT3 | Transfer | Savings transfer exceeds daily limit | Error: Exceeds daily limit |
| DT4 | Monthly fee | Checking balance is above $5,000 | Fee waived |
| DT5 | Monthly fee | Savings balance is at $1,000 | $5 fee charged |
| DT6 | Bill payment | Empty payee | Error: Invalid payee |
| DT7 | Monthly fee | Closed account processes fee | Error: Account closed |
| DT8 | Monthly fee | Premium account processes fee | No fee charged |
| DT9 | Monthly fee | Savings balance at $100 is charged $5 | Balance becomes $95 and account becomes Suspended |
| DT10 | Bill payment | Frozen account attempts payment | Error: Account is not active |
| DT11 | Bill payment | Payment amount is $0 | Error: Amount must be positive |
| DT12 | Bill payment | Payment exceeds available balance | Error: Insufficient funds |
| DT13 | Bill payment | Valid payee, valid amount, sufficient funds | Payment succeeds and balance decreases |
| DT14 | Bill payment | Savings payment reduces balance below $100 | Payment succeeds and account becomes Suspended |

---

## State Transition Testing

The automated State Transition suite contains 11 tests.

### State Transition Diagram

```text
                          Freeze
                 +----------------------+
                 |                      v
             [ ACTIVE ] ------------> [ FROZEN ]
                 ^   |                    |   |
                 |   |                    |   | Deposit rejected
                 |   | Unfreeze invalid   |   v
                 |   +----> [ ACTIVE ]    | [ FROZEN ]
                 |                        |
                 |                        | Unfreeze
                 |                        v
                 |                    [ ACTIVE ]
                 |
                 | Deposit restores minimum
                 |
           [ SUSPENDED ]
              ^      |
              |      | Insufficient deposit
              |      v
              +-- [ SUSPENDED ]

ACTIVE ----- Close -----> CLOSED
CLOSED ---- Deposit ----> CLOSED
CLOSED ---- Freeze -----> CLOSED

ACTIVE -- Savings balance below minimum --> SUSPENDED
ACTIVE -- Valid deposit -----------------> ACTIVE
```

### State Transition Table

| Current State | Event | Next State | Expected Action / Output |
|---|---|---|---|
| Active | Savings balance drops below minimum after transfer | Suspended | Transfer succeeds and account is suspended |
| Suspended | Deposit restores minimum balance | Active | Deposit succeeds and normal access is restored |
| Active | Freeze request | Frozen | Account is frozen |
| Frozen | Unfreeze request | Active | Normal access is restored |
| Active | Close request | Closed | Account is permanently closed |
| Closed | Deposit attempted | Closed | Deposit rejected |
| Frozen | Deposit attempted | Frozen | Deposit rejected |
| Active | Valid deposit | Active | Deposit succeeds and state does not change |
| Suspended | Deposit does not restore minimum balance | Suspended | Deposit succeeds but account remains suspended |
| Closed | Freeze request | Closed | Freeze request rejected |
| Active | Unfreeze request | Active | Unfreeze request rejected |

### State Transition Test Cases

| Test ID | Start State | Event | Expected End State | Validation |
|---|---|---|---|---|
| ST1 | Active | Savings transfer reduces balance below $100 | Suspended | Transfer succeeds, balance is $90, state is Suspended |
| ST2 | Suspended | Deposit restores balance above minimum | Active | Deposit succeeds, balance is $110, state is Active |
| ST3 | Active | Freeze request | Frozen | `freeze()` returns True and state becomes Frozen |
| ST4 | Frozen | Unfreeze request | Active | `unfreeze()` returns True and state becomes Active |
| ST5 | Active | Close request | Closed | `close()` returns True and state becomes Closed |
| ST6 | Closed | Deposit attempted | Closed | Deposit fails and state remains Closed |
| ST7 | Frozen | Deposit attempted | Frozen | Deposit fails and state remains Frozen |
| ST8 | Active | Valid deposit | Active | Deposit succeeds and state remains Active |
| ST9 | Suspended | Deposit remains below Savings minimum | Suspended | Deposit succeeds and state remains Suspended |
| ST10 | Closed | Freeze request | Closed | `freeze()` returns False and state remains Closed |
| ST11 | Active | Unfreeze request | Active | `unfreeze()` returns False and state remains Active |

---

## Automated Test Traceability Summary

| Technique | Automated Tests |
|---|---:|
| Equivalence Partitioning | 9 |
| Boundary Value Analysis | 6 |
| Decision Table Testing | 14 |
| State Transition Testing | 11 |
| **Total** | **40** |

The identifiers in this document are aligned with the current automated test docstrings:

- `EP1` through `EP9`
- `BV1` through `BV6`
- `DT1` through `DT14`
- `ST1` through `ST11`

Additional Equivalence Partitioning and Boundary Value Analysis rows are included as designed cases to document the complete input classes and boundary sets required by the assignment, even when they are not implemented as separate automated tests.

## Test Design Summary

The SecureBank test design applies four black box testing techniques without relying on the internal implementation.

Equivalence Partitioning separates representative valid and invalid input classes. Boundary Value Analysis focuses on values immediately around critical numeric limits. Decision Table Testing evaluates combinations of banking business rules for transfers, fees, and bill payments. State Transition Testing validates behavior across Active, Suspended, Frozen, and Closed account states.

The final automated suite contains 40 tests: 9 Equivalence Partitioning tests, 6 Boundary Value Analysis tests, 14 Decision Table tests, and 11 State Transition tests.
