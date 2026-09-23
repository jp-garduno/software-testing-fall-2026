# Decision Tables

## Decision Table 1: Transfer Validation

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

## Decision Table 2: Monthly Fee Processing

| Condition                     | Rule 1  | Rule 2  | Rule 3   | Rule 4   | Rule 5  |
| ----------------------------- | ------- | ------- | -------- | -------- | ------- |
| Account type                  | Savings | Savings | Checking | Checking | Premium |
| Balance > waiver threshold?   | Y       | N       | Y        | N        | -       |
| **Action**                    |         |         |          |          |         |
| No fee charged (waived)       |         | X       |          | X        | X       |
| $5 fee charged                | X       |         |          |          |         |
| $10 fee charged               |         |         | X        |          |         |
| Check for insufficient funds  | X       |         | X        |          |         |

## Decision Table 3: Bill Payment Validation

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

## Decision Table 4: Account Creation Eligibility
 
| Condition                            | Rule 1       | Rule 2       | Rule 3 | Rule 4 |
| ------------------------------------ | ------------ | ------------ | ------ | ------ |
| Account type selected                | Save/Premium | Save/Premium | Check  | Check  |
| Initial deposit ≥ type minimum?      | Y            | N            | Y      | N      |
| **Action**                           |              |              |        |        |
| Account created (status Active)      | X            |              | X      | X      |
| Error: Initial deposit below minimum |              | X            |        |        |

### Coverage Summary

| Table                        | # Conditions | # Rules | Checked |
| ---------------------------- | ---------- - | ------- | ------- |
| Transfer Validation          | 3            | 8       | Yes     |
| Monthly Fee Processing       | 2            | 5       | Yes     |
| Bill Payment Validation      | 3            | 8       | Yes     |
| Account Creation Eligibility | 2            | 4       | Yes     |