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
