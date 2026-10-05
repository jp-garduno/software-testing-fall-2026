# Test Design Document — SecureBank Black Box Testing Suite

**Student**: Kaito0110
**Assignment**: Homework 4 — Black Box Testing
**System Under Test**: SecureBank Online Banking

---

## 1. Equivalence Partitioning (EP)

### Input: Transfer Amount

| Partition ID | Description                | Type    | Representative Value | Expected Result                |
| ------------ | -------------------------- | ------- | -------------------- | ------------------------------ |
| EP1          | Valid amount within limits | Valid   | \$500                | Transfer succeeds              |
| EP2          | Zero amount                | Invalid | \$0.00               | Error: Amount must be positive |
| EP3          | Negative amount            | Invalid | -\$100               | Error: Amount must be positive |
| EP4          | Amount exceeds daily limit | Invalid | \$100,000            | Error: Exceeds daily limit     |
| EP5          | Amount exceeds balance     | Invalid | Balance + \$1        | Error: Insufficient funds      |

### Input: Account Type

| Partition ID | Description      | Type  | Representative Value | Expected Result        |
| ------------ | ---------------- | ----- | -------------------- | ---------------------- |
| EP6          | Savings account  | Valid | SAVINGS              | Account created active |
| EP7          | Checking account | Valid | CHECKING             | Account created active |
| EP8          | Premium account  | Valid | PREMIUM              | Account created active |

### Input: Account Balance at Creation

| Partition ID | Description                          | Type    | Representative Value | Expected Result  |
| ------------ | ------------------------------------ | ------- | -------------------- | ---------------- |
| EP9          | Balance above minimum (savings)      | Valid   | \$500                | State: Active    |
| EP10         | Balance below minimum (savings)      | Invalid | \$50                 | State: Suspended |
| EP11         | Zero balance (checking — no minimum) | Valid   | \$0                  | State: Active    |

### Input: Payee for Bill Payment

| Partition ID | Description           | Type    | Representative Value | Expected Result       |
| ------------ | --------------------- | ------- | -------------------- | --------------------- |
| EP12         | Known valid payee     | Valid   | "electric_company"   | Bill payment succeeds |
| EP13         | Unknown/invalid payee | Invalid | "random_payee"       | Error: Invalid payee  |

### Input: Date Range for Transaction History

| Partition ID | Description                 | Type    | Representative Value | Expected Result                     |
| ------------ | --------------------------- | ------- | -------------------- | ----------------------------------- |
| EP14         | Valid range (start <= end)  | Valid   | Today-30d to today   | Returns filtered transactions       |
| EP15         | Invalid range (start > end) | Invalid | Today to yesterday   | Error: Start date must be before... |
| EP16         | No filter (None, None)      | Valid   | None, None           | Returns all transactions            |

---

## 2. Boundary Value Analysis (BVA)

### Boundary: Transfer Amount — Checking Account (\$5,000 daily limit)

| Test ID | Boundary         | Test Value  | Expected Result                |
| ------- | ---------------- | ----------- | ------------------------------ |
| BV1     | Below minimum    | \$0.00      | Error: Amount must be positive |
| BV2     | Minimum valid    | \$0.01      | Transfer succeeds              |
| BV3     | Just below limit | \$4,999.99  | Transfer succeeds              |
| BV4     | At limit         | \$5,000.00  | Transfer succeeds              |
| BV5     | Just above limit | \$5,000.01  | Error: Exceeds daily limit     |
| BV6     | Far above limit  | \$10,000.00 | Error: Exceeds daily limit     |

### Boundary: Transfer Amount — Savings Account (\$2,000 daily limit)

| Test ID | Boundary         | Test Value | Expected Result            |
| ------- | ---------------- | ---------- | -------------------------- |
| BV7     | Just below limit | \$1,999.99 | Transfer succeeds          |
| BV8     | At limit         | \$2,000.00 | Transfer succeeds          |
| BV9     | Just above limit | \$2,000.01 | Error: Exceeds daily limit |

### Boundary: Account Balance vs Minimum — Savings (\$100 minimum)

| Test ID | Boundary           | Test Value | Expected Result  |
| ------- | ------------------ | ---------- | ---------------- |
| BV10    | At minimum         | \$100.00   | State: Active    |
| BV11    | Just below minimum | \$99.99    | State: Suspended |
| BV12    | Just above minimum | \$100.01   | State: Active    |

### Boundary: Fee Waiver Threshold — Savings (\$1,000 threshold)

| Test ID | Boundary             | Test Value | Expected Result |
| ------- | -------------------- | ---------- | --------------- |
| BV13    | Just above threshold | \$1,000.01 | Fee waived      |
| BV14    | At threshold         | \$1,000.00 | Fee waived      |
| BV15    | Just below threshold | \$999.99   | \$5 fee charged |

### Boundary: Premium Account Minimum (\$10,000)

| Test ID | Boundary           | Test Value  | Expected Result  |
| ------- | ------------------ | ----------- | ---------------- |
| BV16    | At minimum         | \$10,000.00 | State: Active    |
| BV17    | Just below minimum | \$9,999.99  | State: Suspended |

### Boundary: Bill Payment Amount

| Test ID | Boundary         | Test Value | Expected Result                |
| ------- | ---------------- | ---------- | ------------------------------ |
| BV18    | Zero amount      | \$0.00     | Error: Amount must be positive |
| BV19    | Minimum positive | \$0.01     | Payment succeeds               |

---

## 3. Decision Tables

### Decision Table 1: Transfer Validation

| Condition             | R1  | R2  | R3  | R4  | R5  | R6  | R7  | R8  |
| --------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
| Sufficient funds?     | Y   | Y   | Y   | Y   | N   | N   | N   | N   |
| Within daily limit?   | Y   | Y   | N   | N   | Y   | Y   | N   | N   |
| Account is Active?    | Y   | N   | Y   | N   | Y   | N   | Y   | N   |
| **Action**            |     |     |     |     |     |     |     |     |
| Transfer succeeds     | X   |     |     |     |     |     |     |     |
| Error: Insufficient   |     |     |     |     | X   |     | X   |     |
| Error: Exceeds limit  |     |     | X   |     |     |     |     |     |
| Error: Account frozen |     | X   |     | X   |     | X   |     | X   |

### Decision Table 2: Monthly Fee Processing

| Condition                   | R1      | R2      | R3       | R4       | R5      |
| --------------------------- | ------- | ------- | -------- | -------- | ------- |
| Account type                | Savings | Savings | Checking | Checking | Premium |
| Balance ≥ waiver threshold? | Y       | N       | Y        | N        | —       |
| **Action**                  |         |         |          |          |         |
| Fee waived                  | X       |         | X        |          | X       |
| \$5 fee charged             |         | X       |          |          |         |
| \$10 fee charged            |         |         |          | X        |         |

### Decision Table 3: Bill Payment Validation

| Condition        | R1  | R2  | R3  | R4  |
| ---------------- | --- | --- | --- | --- |
| Valid payee?     | Y   | Y   | Y   | N   |
| Amount > 0?      | Y   | Y   | N   | Y   |
| Account active?  | Y   | N   | Y   | Y   |
| **Action**       |     |     |     |     |
| Payment succeeds | X   |     |     |     |
| Error: Frozen    |     | X   |     |     |
| Error: Amount    |     |     | X   |     |
| Error: Payee     |     |     |     | X   |

---

## 4. State Transition Testing

### State Transition Diagram

```
                    +--[Balance < Min]-->  [Suspended]
                    |                          |
  [Active] --[Freeze]--> [Frozen]    [Deposit restores]
      |               |         \         /
      |           [Unfreeze]     \       /
      |               |          v     v
  [Close]         [Close]       [Active]
      |               |
      v               v
  [Closed] <------[Close]----  [Suspended]
      |
  (No further transitions)
```

### State Transition Table

| Current State | Event                       | Next State | Action/Output             |
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

| Test ID | Start State | Event                             | Expected End State | Validation                    |
| ------- | ----------- | --------------------------------- | ------------------ | ----------------------------- |
| ST1     | Active      | Transfer causes balance < \$100   | Suspended          | state == Suspended            |
| ST2     | Suspended   | Deposit \$500                     | Active             | state == Active               |
| ST3     | Active      | Freeze request                    | Frozen             | state == Frozen, success=True |
| ST4     | Frozen      | Unfreeze approved                 | Active             | state == Active, success=True |
| ST5     | Active      | Close request                     | Closed             | state == Closed, success=True |
| ST6     | Suspended   | Close request                     | Closed             | state == Closed, success=True |
| ST7     | Frozen      | Close request                     | Closed             | state == Closed, success=True |
| ST8     | Closed      | Transfer attempt                  | Closed             | success=False, "closed"       |
| ST9     | Closed      | Deposit attempt                   | Closed             | success=False, "closed"       |
| ST10    | Closed      | Close again                       | Closed             | success=False, "closed"       |
| ST11    | Suspended   | Transfer attempt                  | Suspended          | success=False, "suspended"    |
| ST12    | Active      | Apply fee with insufficient funds | Suspended          | state == Suspended            |
