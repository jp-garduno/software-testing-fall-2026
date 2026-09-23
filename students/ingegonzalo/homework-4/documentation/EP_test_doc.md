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