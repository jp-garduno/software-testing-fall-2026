# SecureBank Black Box Test Design Document

## Equivalence Partitioning

### Input 1: Transfer Amount

| Partition ID | Description | Type | Representative Value | Expected Result |
|---|---|---|---|---|
| EP1 | Valid amount within account limits | Valid | $500 | Transfer succeeds |
| EP2 | Zero amount | Invalid | $0 | Error: Amount must be positive |
| EP3 | Negative amount | Invalid | -$100 | Error: Amount must be positive |
| EP4 | Amount exceeds daily limit | Invalid | $5,000.01 for Checking | Error: Exceeds daily limit |
| EP5 | Amount exceeds available balance | Invalid | Balance + $1 | Error: Insufficient funds |

### Input 2: Account Type

| Partition ID | Description | Type | Representative Value | Expected Result |
|---|---|---|---|---|
| EP6 | Savings account | Valid | Savings | Account created with Savings rules |
| EP7 | Checking account | Valid | Checking | Account created with Checking rules |
| EP8 | Premium account | Valid | Premium | Account created with Premium rules |
| EP9 | Unsupported account type | Invalid | Business | Error: Invalid account type |
| EP10 | Empty account type | Invalid | Empty string | Error: Invalid account type |

### Input 3: Account Balance

| Partition ID | Description | Type | Representative Value | Expected Result |
|---|---|---|---|---|
| EP11 | Positive balance | Valid | $2,000 | Account operates normally |
| EP12 | Zero balance for Checking | Valid | $0 | Account can be created |
| EP13 | Negative initial balance | Invalid | -$100 | Error: Initial balance cannot be negative |
| EP14 | Savings balance below minimum after transaction | Valid state transition | $99 | Account becomes Suspended |
| EP15 | Premium balance above minimum | Valid | $20,000 | Account remains Active |

### Input 4: Payee Information

| Partition ID | Description | Type | Representative Value | Expected Result |
|---|---|---|---|---|
| EP16 | Valid payee name | Valid | Electricity Company | Bill payment allowed |
| EP17 | Empty payee | Invalid | Empty string | Error: Invalid payee |
| EP18 | Non-string payee | Invalid | 12345 | Error: Invalid payee |
| EP19 | Valid payee with sufficient funds | Valid | Credit Card | Payment succeeds |
| EP20 | Valid payee but insufficient funds | Invalid transaction | Water Company | Error: Insufficient funds |

### Input 5: Transaction History Date Range

| Partition ID | Description | Type | Representative Value | Expected Result |
|---|---|---|---|---|
| EP21 | Valid start and end dates | Valid | Sep 1 - Sep 30 | Transactions in range displayed |
| EP22 | Same start and end date | Valid | Sep 15 - Sep 15 | Transactions for that day displayed |
| EP23 | Start date after end date | Invalid | Sep 30 - Sep 1 | Error: Invalid date range |
| EP24 | Missing start date | Invalid | No start date | Error: Start date required |
| EP25 | Invalid date format | Invalid | abc | Error: Invalid date |

---

## Boundary Value Analysis

### Boundary 1: Minimum Transfer Amount ($0.01)

| Test ID | Boundary | Test Value | Expected Result |
|---|---|---:|---|
| BV1 | Below minimum | -$0.01 | Error: Amount must be positive |
| BV2 | Immediately below minimum | $0.00 | Error: Amount must be positive |
| BV3 | At minimum | $0.01 | Transfer succeeds |
| BV4 | Just above minimum | $0.02 | Transfer succeeds |

### Boundary 2: Checking Daily Transfer Limit ($5,000)

| Test ID | Boundary | Test Value | Expected Result |
|---|---|---:|---|
| BV5 | Just below limit | $4,999.99 | Transfer succeeds |
| BV6 | At limit | $5,000.00 | Transfer succeeds |
| BV7 | Just above limit | $5,000.01 | Error: Exceeds daily limit |
| BV8 | Far above limit | $6,000.00 | Error: Exceeds daily limit |

### Boundary 3: Savings Daily Transfer Limit ($2,000)

| Test ID | Boundary | Test Value | Expected Result |
|---|---|---:|---|
| BV9 | Just below limit | $1,999.99 | Transfer succeeds |
| BV10 | At limit | $2,000.00 | Transfer succeeds |
| BV11 | Just above limit | $2,000.01 | Error: Exceeds daily limit |
| BV12 | Far above limit | $3,000.00 | Error: Exceeds daily limit |

### Boundary 4: Savings Minimum Balance ($100)

| Test ID | Boundary | Balance After Transaction | Expected Result |
|---|---|---:|---|
| BV13 | Just below minimum | $99.99 | Account becomes Suspended |
| BV14 | At minimum | $100.00 | Account remains Active |
| BV15 | Just above minimum | $100.01 | Account remains Active |
| BV16 | Above minimum | $150.00 | Account remains Active |

### Boundary 5: Checking Fee Waiver Threshold ($5,000)

| Test ID | Boundary | Balance | Expected Result |
|---|---|---:|---|
| BV17 | Just below threshold | $4,999.99 | $10 fee charged |
| BV18 | At threshold | $5,000.00 | $10 fee charged |
| BV19 | Just above threshold | $5,000.01 | Fee waived |
| BV20 | Well above threshold | $6,000.00 | Fee waived |

---

## Decision Tables

### Decision Table 1: Transfer Validation

| Condition / Action | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 | Rule 6 | Rule 7 | Rule 8 |
|---|---|---|---|---|---|---|---|---|
| Sufficient funds? | Y | Y | Y | Y | N | N | N | N |
| Within daily limit? | Y | Y | N | N | Y | Y | N | N |
| Account Active? | Y | N | Y | N | Y | N | Y | N |
| **Transfer succeeds** | X | | | | | | | |
| **Error: Account not active** | | X | | X | | X | | X |
| **Error: Exceeds daily limit** | | | X | | | | X | |
| **Error: Insufficient funds** | | | | | X | | X | |

Rule 1 represents the successful transfer scenario. The other rules verify that a transfer is rejected when one or more required conditions are not satisfied.

### Decision Table 2: Monthly Fee Processing

| Condition / Action | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 |
|---|---|---|---|---|---|
| Account Type | Savings | Savings | Checking | Checking | Premium |
| Balance above waiver threshold? | Y | N | Y | N | - |
| **Charge $5 fee** | | X | | | |
| **Charge $10 fee** | | | | X | |
| **Waive fee** | X | | X | | X |

Savings accounts are charged $5 unless their balance is above $1,000. Checking accounts are charged $10 unless their balance is above $5,000. Premium accounts have no monthly fee.

### Decision Table 3: Bill Payment Validation

| Condition / Action | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 | Rule 6 | Rule 7 | Rule 8 |
|---|---|---|---|---|---|---|---|---|
| Valid payee? | Y | Y | Y | Y | N | N | N | N |
| Amount > $0? | Y | Y | N | N | Y | Y | N | N |
| Sufficient funds? | Y | N | Y | N | Y | N | Y | N |
| **Payment succeeds** | X | | | | | | | |
| **Error: Insufficient funds** | | X | | X | | | | |
| **Error: Amount must be positive** | | | X | X | | | X | X |
| **Error: Invalid payee** | | | | | X | X | X | X |

---

## State Transition Testing

### State Transition Diagram

```text
                    Freeze Request
              +------------------------+
              |                        v
          [ ACTIVE ] --------------> [ FROZEN ]
              |                          |
              |                          | Unfreeze
              |                          |
 Balance < Minimum                      v
              |                     [ ACTIVE ]
              v
        [ SUSPENDED ]
              |
              | Deposit restores
              | minimum balance
              v
          [ ACTIVE ]

ACTIVE -------- Close Request --------> CLOSED
SUSPENDED ----- Close Request --------> CLOSED
FROZEN -------- Close Request --------> CLOSED

CLOSED -------- Any Event ------------> CLOSED
```

### State Transition Table

| Current State | Event | Next State | Action / Output |
|---|---|---|---|
| Active | Balance drops below minimum | Suspended | Transactions restricted |
| Active | Freeze request | Frozen | Transactions blocked |
| Active | Close request | Closed | Account terminated |
| Suspended | Deposit restores minimum balance | Active | Normal access restored |
| Suspended | Close request | Closed | Account terminated |
| Frozen | Unfreeze request | Active | Normal access restored |
| Frozen | Close request | Closed | Account terminated |
| Closed | Any transaction request | Closed | Error: Account closed |

### State Transition Test Cases

| Test ID | Start State | Event | Expected End State | Validation |
|---|---|---|---|---|
| ST1 | Active | Savings transfer causes balance to fall below $100 | Suspended | State equals Suspended |
| ST2 | Suspended | Deposit restores balance above $100 | Active | State equals Active |
| ST3 | Active | Freeze request | Frozen | State equals Frozen |
| ST4 | Frozen | Unfreeze request | Active | State equals Active |
| ST5 | Active | Close request | Closed | State equals Closed |
| ST6 | Closed | Deposit attempted | Closed | Transaction rejected and state remains Closed |
| ST7 | Suspended | Close request | Closed | Account remains permanently Closed |
| ST8 | Frozen | Close request | Closed | Account remains permanently Closed |

---

## Test Design Summary

The SecureBank test design applies four black box testing techniques to validate the most important business rules without relying on the internal implementation.

Equivalence Partitioning divides major inputs into representative valid and invalid groups. Boundary Value Analysis focuses on values immediately around important limits such as minimum transfers, daily limits, minimum balances, and fee thresholds.

Decision Tables evaluate combinations of conditions for transfers, monthly fees, and bill payments. State Transition Testing validates the behavior of accounts as they move between Active, Suspended, Frozen, and Closed states.

Together, these techniques provide systematic coverage of normal behavior, invalid inputs, edge cases, business-rule combinations, and account lifecycle behavior.