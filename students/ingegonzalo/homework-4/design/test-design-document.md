# Test Design Document

## Equivalence Partitioning

### Input: Transfer Amount

| Partition ID | Description                | Type    | Representative Value | Expected Result                |
| ------------ | -------------------------- | ------- | -------------------- | ------------------------------ |
| EP1          | Valid amount within limits | Valid   | $500                 | Transfer succeeds              |
| EP2          | Zero amount                | Invalid | $0                   | Error: Amount must be positive |
| EP3          | Negative amount            | Invalid | -$100                | Error: Amount must be positive |
| EP4          | Amount exceeds daily limit | Invalid | $100,000             | Error: Exceeds daily limit     |
| EP5          | Amount exceeds balance     | Invalid | Balance + $1         | Error: Insufficient funds      |

### Input: Account Type

| Partition ID | Description     | Type     | Representative Value | Expected Result              |
| ------------ | --------------- | -------- | -------------------- | ---------------------------- |
| EP6          | Savings Account  | Valid   | Savings              | Applies the Savings Rules    |
| EP7          | Checking Account | Valid   | Checking             | Applies the Checking Rules   |
| EP8          | Premium Account  | Valid   | Premium              | Applies the Premium Rules    |
| EP9          | Undefined Type   | Invalid | Undefined            | Error: Invalid Account Type  |
| EP10         | Null             | Invalid | Null                 | Error: Account Type Required |

### Input: Account Balance

| Partition ID	| Description                | Type     | Representative Value | Expected Result                             |
| ------------- | -------------------------- | -------- | -------------------- | ------------------------------------------- |
| EP11          | Balance Above Minimum      | Valid    | $1,500               | Account remains Active                      |
| EP12          | Balance Exactly at Minimum | Valid    | $100                 | Account remains Active                      |
| EP13	        | Balance Below Minimum	     | Invalid  | $50                  | Account Status → Suspended                  |
| EP14	        | Negative Balance           | Invalid  | -$20                 | Error/Suspended: Balance cannot Be Negative |

### Input: Bill Payment

|Partition ID	|Description	                | Type	  | Representative Value | Expected Result                         |
| ------------- | ----------------------------- | ------  | -------------------- | --------------------------------------- |
| EP15	        | Valid registered payee        | Valid   |	City Electric Co.    | Payment proceeds                        |
| EP16	        | Empty payee name              | Invalid |	""	                 | Error: Payee required                   |
| EP17	        | Unregistered/unknown payee    | Invalid |	Random LLC           | Error: Payee not found                  |
| EP18	        | Payee name exceeds max length | Invalid |	300-char string	     |Error: Payee name too long               |
| EP19	        | Payee with invalid characters | Invalid |	"script"             | Error: Invalid characters in payee name |

### Input: Date Range Transaction History

| Partition ID | Description                           | Type    |	Representative Value     |	Expected Result              |
| ------------ | ------------------------------------- | ------- | ------------------------- | ----------------------------- |
| EP20	       | Valid past date range                 | Valid   | 2026-01-01 to 2026-06-01  | Returns matching transactions |
| EP21	       | Start date after end date             | Invalid | 2026-06-01 to 2026-01-01  | Error: Invalid date range     |
| EP22	       | Future date range                     | Valid   | 2027-01-01 to 2027-06-01  | Returns empty result set      |
| EP23         | Malformed date format                 | Invalid | 13/45/2026                | Error: Invalid date format    |
| EP24         | Range spanning entire account history | Valid   | account creation to today | Returns all transactions      |

## Boundary Value Analysis (BVA)

### Boundary 1: Transfer Amount — Savings Account ($2,000 daily limit)

| Test ID | Boundary           | Test Value | Expected Result                |
| ------- | ------------------ | ---------- | ------------------------------ |
| BVA1    | Below minimum      | $0         | Error: Amount must be positive |
| BVA2    | Minimum valid      | $0.01      | Transfer succeeds              |
| BVA3    | Just below limit   | $1,999.99  | Transfer succeeds              |
| BVA4    | At limit           | $2,000     | Transfer succeeds              |
| BVA5    | Just above limit   | $2,000.01  | Error: Exceeds daily limit     |
| BVA6    | Far above limit    | $5,000     | Error: Exceeds daily limit     |

### Boundary 2: Transfer Amount — Checking Account ($5,000 daily limit)

| Test ID | Boundary           | Test Value | Expected Result                |
| ------- | ------------------ | ---------- | ------------------------------ |
| BVA7    | Below minimum      | $0         | Error: Amount must be positive |
| BVA8    | Minimum valid      | $0.01      | Transfer succeeds              |
| BVA9    | Just below limit   | $4,999.99  | Transfer succeeds              |
| BVA10   | At limit           | $5,000     | Transfer succeeds              |
| BVA11   | Just above limit   | $5,000.01  | Error: Exceeds daily limit     |
| BVA12   | Far above limit    | $10,000    | Error: Exceeds daily limit     |

### Boundary 3: Transfer Amount — Premium Account ($50,000 daily limit)

| Test ID | Boundary         | Test Value | Expected Result            |
| ------- | ---------------- | ---------- | -------------------------- |
| BVA13   | Minimum valid    | $0.01      | Transfer succeeds          |
| BVA14   | Just below limit | $49,999.99 | Transfer succeeds          |
| BVA15   | At limit         | $50,000    | Transfer succeeds          |
| BVA16   | Just above limit | $50,000.01 | Error: Exceeds daily limit |

### Boundary 4: Account Balance vs Minimum — Savings Account ($100 minimum)

| Test ID | Boundary                     | Test Value | Expected Result                             |
| ------- | ---------------------------- | ---------- | ------------------------------------------- |
| BVA17   | Just below minimum           | $99.99     | Account status → Suspended                  |
| BVA18   | At minimum                   | $100       | Account remains Active                      |
| BVA19   | Just above minimum           | $100.01    | Account remains Active                      |
| BVA20   | Well above minimum           | $500       | Account remains Active                      |
| BVA21   | Zero balance                 | $0         | Account status → Suspended                  |
| BVA22   | Negative balance (edge case) | -$0.01     | Error/Suspended: balance cannot be negative |

### Boundary 5: Account Balance vs Fee Waiver Threshold — Savings Account ($1,000 waiver)

| Test ID | Boundary                    | Test Value | Expected Result                   |
| ------- | --------------------------- | ---------- | --------------------------------- |
| BVA23   | Just below waiver threshold | $999.99    | Monthly fee of $5 charged         |
| BVA24   | At waiver threshold         | $1,000     | Fee waived (rule says "> $1,000") |
| BVA25   | Just above waiver threshold | $1,000.01  | Fee waived                        |
| BVA26   | Far above threshold         | $5,000     | Fee waived                        |

### Boundary 6: Account Balance vs Fee Waiver Threshold — Checking Account ($5,000 waiver)

| Test ID | Boundary                    | Test Value | Expected Result                   |
| ------- | --------------------------- | ---------- | --------------------------------- |
| BVA27   | Just below waiver threshold | $4999.99   | Monthly fee of $10 charged        |
| BVA28   | At waiver threshold         | $5,000     | Fee waived (rule says "> $5,000") |
| BVA29   | Just above waiver threshold | $5,000.01  | Fee waived                        |
| BVA30   | Far above threshold         | $10,000    | Fee waived                        |

### Boundary 7: Account Balance vs Minimum — Premium Account ($10,000 minimum)

| Test ID | Boundary           | Test Value  | Expected Result             |
| ------- | ------------------ | ----------- | --------------------------- |
| BVA31   | Just below minimum | $9,999.99   | Account status -> Suspended |
| BVA32   | At minimum         | $10,000     | Account remains Active      |
| BVA33   | Just above minimum | $10,000.01  | Account remains Active      |
| BVA34   | Well above minimum | $50,000     | Account remains Active      |


### Coverage Summary

| Boundary                         | # Test Values | Limit Type               |
| -------------------------------- | ------------- | ------------------------ |
| Transfer Amount – Checking       | 6             | Daily Limit              |
| Transfer Amount – Savings        | 6             | Daily Limit              |
| Transfer Amount – Premium        | 4             | Daily Limit              |
| Balance vs Minimum – Savings     | 6             | Suspension Threshold     |
| Balance vs Fee Waiver – Savings  | 4             | Business Threshold (fee) |
| Balance vs Fee Waiver – Checking | 4             | Business Threshold (fee) |
| Balance vs Minimum – Premium     | 4             | Suspension Threshold     |

## Decision Tables

### Decision Table 1: Transfer Validation

| Condition                  | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 | Rule 6 | Rule 7 | Rule 8 |
| -------------------------- | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| Sufficient funds?          | Y      | Y      | Y      | Y      | N      | N      | N      | N      |
| Within daily limit?        | Y      | Y      | N      | N      | Y      | Y      | N      | N      |
| Account is Active?         | Y      | N      | Y      | N      | Y      | N      | Y      | N      |
| **Action**                 |        |        |        |        |        |        |        |        |
| Transfer succeeds          | X      |        |        |        |        |        |        |        |
| Error: Insufficient funds  |        |        |        |        | X      | X      | X      | X      |
| Error: Exceeds limit       |        |        | X      |        |        |        | X      |        |
| Error: Account not active  |        | X      |        | X      |        | X      |        | X      |

### Decision Table 2: Monthly Fee Processing

| Condition                     | Rule 1  | Rule 2  | Rule 3   | Rule 4   | Rule 5  |
| ----------------------------- | ------- | ------- | -------- | -------- | ------- |
| Account type                  | Savings | Savings | Checking | Checking | Premium |
| Balance > waiver threshold?   | Y       | N       | Y        | N        | -       |
| **Action**                    |         |         |          |          |         |
| No fee charged (waived)       |         | X       |          | X        | X       |
| $5 fee charged                | X       |         |          |          |         |
| $10 fee charged               |         |         | X        |          |         |
| Check for insufficient funds  | X       |         | X        |          |         |

### Decision Table 3: Bill Payment Validation

| Condition                       | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 | Rule 6 | Rule 7 | Rule 8 |
| ------------------------------- | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| Valid payee?                    | Y      | Y      | Y      | Y      | N      | N      | N      | N      |
| Amount > $0?                    | Y      | Y      | N      | N      | Y      | Y      | N      | N      |
| Sufficient funds?               | Y      | N      | Y      | N      | Y      | N      | Y      | N      |
| **Action**                      |        |        |        |        |        |        |        |        |
| Payment succeeds                | X      |        |        |        |        |        |        |        |
| Error: Insufficient funds       |        | X      |        | X      |        | X      |        | X      |
| Error: Amount must be positive  |        |        | X      |        |        |        | X      |        |
| Error: Invalid payee            |        |        |        |        | X      | X      | X      | X      |

### Decision Table 4: Account Creation Eligibility
 
| Condition                            | Rule 1       | Rule 2       | Rule 3 | Rule 4 |
| ------------------------------------ | ------------ | ------------ | ------ | ------ |
| Account type selected                | Save/Premium | Save/Premium | Check  | Check  |
| Initial deposit ≥ type minimum?      | Y            | N            | Y      | N      |
| **Action**                           |              |              |        |        |
| Account created (status Active)      | X            |              | X      | X      |
| Error: Initial deposit below minimum |              | X            |        |        |

#### Coverage Summary

| Table                        | # Conditions | # Rules | Checked |
| ---------------------------- | ---------- - | ------- | ------- |
| Transfer Validation          | 3            | 8       | Yes     |
| Monthly Fee Processing       | 2            | 5       | Yes     |
| Bill Payment Validation      | 3            | 8       | Yes     |
| Account Creation Eligibility | 2            | 4       | Yes     |

## State Transition Testing

### State Transition Diagram

                     ┌────────────────────────────────────────────┐
                     │                                            │
                     ▼                                            │
        (Balance restored above minimum)                          │
                     │                                            │
    ┌───────────►[Suspended]                                      │
    │                │    │                                       │
    │  (Balance <    │    │ (Close request)                       │
    │   minimum)     │    │                                       │
    │                │    ▼                                       │
[Active] ──────────► │  [Closed] ◄─────────────────────┐          │
    │  │             │    ▲                            │          │
    │  │             │    │ (Close request)            │          │
    │  │             │    │                            │          │
    │  │ (Freeze     │    │                            │          │
    │  │  request /  │    │                            │          │
    │  │  fraud)     │    │                            │          │
    │  ▼             │    │                            │          │
    │[Frozen]────────┘    │                            │          │
    │  │                  │                            │          │
    │  └─────────(Unfreeze approved)───────────────────┘          │
    │                                                             │
    └──(Close request)────────────────────────────────────────────┘

[Closed] --(Any event)--> [Closed]   (terminal state, no exit)

### State Transition Text

'Active' → 'Suspended': When balance under minimum
'Active' → 'Frozen': Client request or fraud
'Active' → 'Closed': Closing request
'Suspended' → 'Active': When deposit restores balance over minimum
'Suspended' → 'Closed': Closing request
'Frozen' → 'Active': Unfreeze approval
'Frozen' → 'Closed': Closing request
'Closed' → 'Closed': Any event in a closed account is invalid

### State Transition Table

| Current State  | Event                              | Next State   | Action/Output             |
| -------------- | ---------------------------------- | ------------ | ------------------------- |
| Active         | Balance drops below minimum        | Suspended    | Send warning notification |
| Active         | Freeze request (customer/fraud)    | Frozen       | Block all transactions    |
| Active         | Close request                      | Closed       | Final statement generated |
| Suspended      | Deposit restores balance           | Active       | Remove restrictions       |
| Suspended      | Close request                      | Closed       | Final statement generated |
| Frozen         | Unfreeze approved                  | Active       | Restore full access       |
| Frozen         | Close request                      | Closed       | Final statement generated |
| Closed         | Any event (transfer, freeze, etc.) | Closed       | Error: Account closed     |

### State Transition Test Cases

| Test ID | Start State | Event                                  | Expected End State | Validation                                   |
| ------- | ----------- | -------------------------------------- | ------------------ | -------------------------------------------- |
| ST1     | Active      | Transfer causes balance < minimum      | Suspended          | Warning shown, status = Suspended            |
| ST2     | Suspended   | Deposit restores balance above minimum | Active             | Status = Active, restrictions removed        |
| ST3     | Active      | Customer requests freeze               | Frozen             | All transactions blocked                     |
| ST4     | Frozen      | Customer requests unfreeze (approved)  | Active             | Full access restored                         |
| ST5     | Active      | Customer requests close                | Closed             | Final statement generated                    |
| ST6     | Suspended   | Customer requests close                | Closed             | Final statement generated                    |
| ST7     | Frozen      | Customer requests close                | Closed             | Final statement generated                    |
| ST8     | Closed      | Attempt to transfer funds              | Closed (no change) | Error: Account closed                        |
| ST9     | Closed      | Attempt to reopen account              | Closed (no change) | Error: Account closed, cannot be reopened    |
| ST10    | Frozen      | Attempt to transfer while frozen       | Frozen (no change) | Error: Account is frozen, transaction denied |

#### Coverage Summary

| Element                                          | Coverage                              |
| ------------------------------------------------ | ------------------------------------- |
| Status                                           | 4 (Active, Suspended, Frozen, Closed) |
| Valid Transition                                 | 7                                     |
| Invalid Transitions                              | 3 (ST8, ST9, ST10)                    |
| Testing cases                                    | 10                                    |