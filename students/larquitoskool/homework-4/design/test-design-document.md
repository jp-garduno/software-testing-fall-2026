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

| Partition ID | Description | Type | Representative Value | Expected Result |
| ------------ | ----------- | ---- | -------------------- | --------------- |

...

## Boundary Value Analysis

### Boundary: Transfer Amount (Checking Account - $5,000 limit)

| Test ID | Boundary         | Test Value | Expected Result                |
| ------- | ---------------- | ---------- | ------------------------------ |
| BV1     | Below minimum    | $0.00      | Error: Amount must be positive |
| BV2     | Minimum valid    | $0.01      | Transfer succeeds              |
| BV3     | Just below limit | $4,999.99  | Transfer succeeds              |
| BV4     | At limit         | $5,000.00  | Transfer succeeds              |
| BV5     | Just above limit | $5,000.01  | Error: Exceeds daily limit     |
| BV6     | Far above limit  | $10,000.00 | Error: Exceeds daily limit     |

### Boundary: Account Balance vs Minimum (Savings - $100 minimum)

| Test ID | Boundary | Test Value | Expected Result |
| ------- | -------- | ---------- | --------------- |

...

## Decision Tables

### Decision Table 1: Transfer Validation

| Condition                 | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 | Rule 6 | Rule 7 | Rule 8 |
| ------------------------- | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| Sufficient funds?         | Y      | Y      | Y      | Y      | N      | N      | N      | N      |
| Within daily limit?       | Y      | Y      | N      | N      | Y      | Y      | N      | N      |
| Account is Active?        | Y      | N      | Y      | N      | Y      | N      | Y      | N      |
| **Action**                |
| Transfer succeeds         | X      |        |        |        |        |        |        |        |
| Error: Insufficient funds |        |        |        |        | X      | X      | X      | X      |
| Error: Exceeds limit      |        |        | X      |        |        |        | X      |        |
| Error: Account frozen     |        | X      |        | X      |        | X      |        | X      |

### Decision Table 2: Monthly Fee Processing

| Condition                   | Rule 1  | Rule 2  | Rule 3   | Rule 4  |
| --------------------------- | ------- | ------- | -------- | ------- |
| Account type                | Savings | Savings | Checking | Premium |
| Balance > waiver threshold? | Y       | N       | Y        | -       |
| **Action**                  |

...

## State Transition Testing

### State Transition Diagram


### State Transition Table

| Current State | Event | Next State | Action/Output |
|---------------|-------|------------|---------------|
| Active | Balance drops below minimum | Suspended | Send warning notification |
| Active | Freeze request | Frozen | Block all transactions |
| Active | Close request | Closed | Final statement generated |
| Suspended | Deposit restores balance | Active | Remove restrictions |
| Suspended | Close request | Closed | Final statement generated |
| Frozen | Unfreeze approved | Active | Restore full access |
| Frozen | Close request | Closed | Final statement generated |
| Closed | Any event | Closed | Error: Account closed |

### State Transition Test Cases

| Test ID | Start State | Event | Expected End State | Validation |
|---------|-------------|-------|-------------------|------------|
| ST1 | Active | Transfer causes balance < $100 | Suspended | Warning shown, status = Suspended |
| ST2 | Suspended | Deposit $500 | Active | Status = Active, full access restored |
...