# Part 1: Test Design Document

## 1.1 Equivalence Partitioning

### Input: Transfer Amount

| Partition ID | Description                                 | Type    | Representative Value        | Expected Result                |
| :----------- | :------------------------------------------ | :------ | :-------------------------- | :----------------------------- |
| EP1_TA       | Valid amount within daily limit and balance | Valid   | $500.00                     | Transfer succeeds              |
| EP2_TA       | Zero amount                                 | Invalid | $0.00                       | Error: Amount must be positive |
| EP3_TA       | Negative amount                             | Invalid | -$100.00                    | Error: Amount must be positive |
| EP4_TA       | Amount exceeds daily limit                  | Invalid | $10,001.00                  | Error: Exceeds daily limit     |
| EP5_TA       | Amount exceeds balance                      | Invalid | $6,000.00 (Balance: $5,000) | Error: Insufficient funds      |

### Input: Account Type

| Partition ID | Description                      | Type    | Representative Value | Expected Result                                    |
| :----------- | :------------------------------- | :------ | :------------------- | :------------------------------------------------- |
| EP1_AT       | Valid Checking Account           | Valid   | "Checking"           | Account accepted, apply checking limits            |
| EP2_AT       | Valid Savings Account            | Valid   | "Savings"            | Account accepted, apply savings limits             |
| EP3_AT       | Valid Investment/Premium Account | Valid   | "Investment"         | Account accepted, apply premium features           |
| EP4_AT       | Invalid/Unsupported Account Type | Invalid | "Credit Card"        | Error: Unsupported account type for this operation |
| EP5_AT       | Blank / Unselected Account Type  | Invalid | Null / Empty         | Error: Account type is required                    |

### Input: Account Balance

| Partition ID | Description                                 | Type    | Representative Value | Expected Result                                          |
| :----------- | :------------------------------------------ | :------ | :------------------- | :------------------------------------------------------- |
| EP1_AB       | Balance above required minimum threshold    | Valid   | $1,500.00            | Account in good standing; full features active           |
| EP2_AB       | Balance between minimum threshold and $0.00 | Valid   | $50.00 (Min: $100)   | Account active; low balance warning triggered            |
| EP3_AB       | Zero balance                                | Valid   | $0.00                | Transactions blocked; status changed to inactive/warning |
| EP4_AB       | Negative balance (Overdraft)                | Invalid | -$50.00              | Overdraft fee applied; debit transactions blocked        |

### Input: Payee Information for Bill Payment

| Partition ID | Description                              | Type    | Representative Value       | Expected Result                      |
| :----------- | :--------------------------------------- | :------ | :------------------------- | :----------------------------------- |
| EP1_PI       | Registered payee with active status      | Valid   | "CFE Electric" (ID: 99482) | Payee loaded successfully            |
| EP2_PI       | Non-existent or unregistered Payee ID    | Invalid | "999999"                   | Error: Payee not found               |
| EP3_PI       | Inactive or blocked Payee                | Invalid | "Old Merchant" (ID: 10023) | Error: Payee unavailable for payment |
| EP4_PI       | Payee account number with invalid format | Invalid | "CFE-1234-XYZ!!!"          | Error: Invalid payee account format  |

### Input: Date Range for Transaction History

| Partition ID | Description                                           | Type    | Representative Value     | Expected Result                           |
| :----------- | :---------------------------------------------------- | :------ | :----------------------- | :---------------------------------------- |
| EP1_DR       | Valid historical range (Start <= End <= Today)        | Valid   | 2026-01-01 to 2026-03-01 | Display transactions for selected range   |
| EP2_DR       | Future date in Start or End Date                      | Invalid | 2026-10-01 to 2026-10-15 | Error: Dates cannot be in the future      |
| EP3_DR       | Start Date is strictly after End Date                 | Invalid | 2026-05-10 to 2026-05-01 | Error: Start Date must be before End Date |
| EP4_DR       | Date range exceeds maximum allowed limit (> 365 days) | Invalid | 2024-01-01 to 2026-01-01 | Error: Date range cannot exceed 12 months |
| EP5_DR       | Invalid date format                                   | Invalid | "31/02/2026" / "ABC"     | Error: Invalid date format                |

---

## 1.2 Boundary Value Analysis

### Boundary: Transfer Amount (Checking Account - $5,000.00 Daily Limit)

| Test ID | Boundary                      | Test Value | Expected Result                |
| :------ | :---------------------------- | :--------- | :----------------------------- |
| BV1_TA1 | Below minimum allowed         | $0.00      | Error: Amount must be positive |
| BV2_TA1 | Minimum valid transfer amount | $0.01      | Transfer succeeds              |
| BV3_TA1 | Just below daily limit        | $4,999.99  | Transfer succeeds              |
| BV4_TA1 | Exactly at daily limit        | $5,000.00  | Transfer succeeds              |
| BV5_TA1 | Just above daily limit        | $5,000.01  | Error: Exceeds daily limit     |
| BV6_TA1 | Far above daily limit         | $10,000.00 | Error: Exceeds daily limit     |

### Boundary: Transfer Amount (Premium Account - $25,000.00 Daily Limit)

| Test ID | Boundary                      | Test Value | Expected Result                |
| :------ | :---------------------------- | :--------- | :----------------------------- |
| BV1_TA2 | Below minimum allowed         | -$0.01     | Error: Amount must be positive |
| BV2_TA2 | Minimum valid transfer amount | $0.01      | Transfer succeeds              |
| BV3_TA2 | Just below daily limit        | $24,999.99 | Transfer succeeds              |
| BV4_TA2 | Exactly at daily limit        | $25,000.00 | Transfer succeeds              |
| BV5_TA2 | Just above daily limit        | $25,000.01 | Error: Exceeds daily limit     |
| BV6_TA2 | Far above daily limit         | $50,000.00 | Error: Exceeds daily limit     |

### Boundary: Account Balance vs Minimum (Savings Account - $100.00 Minimum)

| Test ID | Boundary                             | Test Value | Expected Result                                    |
| :------ | :----------------------------------- | :--------- | :------------------------------------------------- |
| BV1_AB  | Balance well below minimum           | $0.00      | Account Restricted / Fee Charged                   |
| BV2_AB  | Balance just below minimum           | $99.99     | Low balance warning triggered; monthly fee applies |
| BV3_AB  | Balance exactly at minimum threshold | $100.00    | Account in good standing; no fee                   |
| BV4_AB  | Balance just above minimum threshold | $100.01    | Account in good standing; no fee                   |
| BV5_AB  | High healthy balance                 | $500.00    | Account in good standing; no fee                   |

### Boundary: Daily Cumulative Transfer Count Limit (Max 5 transactions/day)

| Test ID | Boundary                             | Test Value   | Expected Result                              |
| :------ | :----------------------------------- | :----------- | :------------------------------------------- |
| BV1_TC  | Zero transactions performed          | 0 transfers  | Transfer allowed                             |
| BV2_TC  | Just below maximum transaction count | 4 transfers  | Transfer allowed                             |
| BV3_TC  | Exactly at maximum transaction count | 5 transfers  | Transfer allowed (5th transaction succeeds)  |
| BV4_TC  | Just above maximum transaction count | 6 transfers  | Error: Daily transaction count limit reached |
| BV5_TC  | Well above transaction count         | 10 transfers | Error: Daily transaction count limit reached |

### Boundary: Transaction History Date Search Range (Max 365 Days)

| Test ID | Boundary                        | Test Value | Expected Result                          |
| :------ | :------------------------------ | :--------- | :--------------------------------------- |
| BV1_DS  | Minimum range                   | 1 day      | Search succeeds                          |
| BV2_DS  | Just below maximum allowed days | 364 days   | Search succeeds                          |
| BV3_DS  | Exactly at maximum allowed days | 365 days   | Search succeeds                          |
| BV4_DS  | Just above maximum allowed days | 366 days   | Error: Date range cannot exceed 365 days |
| BV5_DS  | Far above maximum allowed days  | 730 days   | Error: Date range cannot exceed 365 days |

---

## 1.3 Decision Tables

### Decision Table 1: Transfer Validation

| Condition                 | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 | Rule 6 | Rule 7 | Rule 8 |
| ------------------------- | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :----: |
| Sufficient funds?         |   Y    |   Y    |   Y    |   Y    |   N    |   N    |   N    |   N    |
| Within daily limit?       |   Y    |   Y    |   N    |   N    |   Y    |   Y    |   N    |   N    |
| Account is Active?        |   Y    |   N    |   Y    |   N    |   Y    |   N    |   Y    |   N    |
| **Action**                |        |        |        |        |        |        |        |        |
| Transfer succeeds         |   X    |        |        |        |        |        |        |        |
| Error: Insufficient funds |        |        |        |        |   X    |   X    |   X    |   X    |
| Error: Exceeds limit      |        |        |   X    |        |        |        |   X    |        |
| Error: Account frozen     |        |   X    |        |   X    |        |   X    |        |   X    |

### Decision Table 2: Monthly Fee Processing

| Condition                         |  Rule 1   |   Rule 2   |   Rule 3    |    Rule 4    | Rule 5  |
| --------------------------------- | :-------: | :--------: | :---------: | :----------: | :-----: |
| Account type                      |  Savings  |  Savings   |  Checking   |   Checking   | Premium |
| Balance > waiver threshold?       | Y (>$100) | N (<=$100) | Y (>$1,000) | N (<=$1,000) |    -    |
| **Action**                        |           |            |             |              |         |
| Apply $0 Monthly Fee              |     X     |            |      X      |              |    X    |
| Charge Standard Monthly Fee ($12) |           |     X      |             |      X       |         |

### Decision Table 3: Bill Payment Validation

| Condition                      | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 |
| ------------------------------ | :----: | :----: | :----: | :----: | :----: |
| Payee Service Available?       |   Y    |   Y    |   Y    |   N    |   N    |
| Valid Payee Account ID?        |   Y    |   Y    |   N    |   Y    |   N    |
| Amount <= Available Balance?   |   Y    |   N    |   -    |   -    |   -    |
| **Action**                     |        |        |        |        |        |
| Payment Processed Successfully |   X    |        |        |        |        |
| Error: Insufficient balance    |        |   X    |        |        |        |
| Error: Invalid Payee Account   |        |        |   X    |        |   X    |
| Error: Service unavailable     |        |        |        |   X    |        |

---

## 1.4 State Transition Testing

### State Transition Diagram

                         +------------------------------------------+
                         |                                          |
                         v                                          |
                    +---------+       (Balance < Min)       +-----------+
                    | Active  | --------------------------> | Suspended |
                    +---------+                             +-----------+
                     |   |  ^                                  |       |
                     |   |  | (Deposit restores)               |       |
                     |   |  +----------------------------------+       |
                     |                                                |
                     | (Freeze)                            (Close Request)
                     |                                                |
                     v                                                v
                 +---------+       (Close Request)       +--------------+
                 | Frozen  | --------------------------> |    Closed    |
                 +---------+                              +--------------+
                     |                                         ^
                     |                                         |
                     +-----------------------------------------+
                              (Close Request)

```

### State Transition Table

| Current State | Event                       | Next State | Action / Output           |
| ------------- | --------------------------- | ---------- | ------------------------- |
| Active        | Balance drops below minimum | Suspended  | Send warning notification |
| Active        | Freeze request              | Frozen     | Block all transactions    |
| Active        | Close request               | Closed     | Final statement generated |
| Suspended     | Deposit restores balance    | Active     | Remove restrictions       |
| Suspended     | Close request               | Closed     | Final statement generated |
| Frozen        | Unfreeze approved           | Active     | Restore full access       |
| Frozen        | Close request               | Closed     | Final statement generated |
| Closed        | Any event                   | Closed     | Error: Account closed     |

### State Transition Test Cases

| Test ID | Start State | Event                          | Expected End State | Validation                                 |
| ------- | ----------- | ------------------------------ | ------------------ | ------------------------------------------ |
| ST1     | Active      | Transfer causes balance < $100 | Suspended          | Warning shown, status = Suspended          |
| ST2     | Suspended   | Deposit $500                   | Active             | Status = Active, full access restored      |
| ST3     | Active      | Freeze request                 | Frozen             | Block all transactions, status = Frozen    |
| ST4     | Frozen      | Unfreeze approved              | Active             | Access restored, status = Active           |
| ST5     | Active      | Close request                  | Closed             | Final statement generated, status = Closed |
| ST6     | Suspended   | Close request                  | Closed             | Final statement generated, status = Closed |
| ST7     | Frozen      | Attempt outbound transfer      | Frozen             | Error: Account frozen                      |
| ST8     | Closed      | Any event                      | Closed             | Error: Account closed                      |
```
