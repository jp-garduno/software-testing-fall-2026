# Exercise 5: Bank Account Kata

**Module**: 6 - Test Driven Development  
**Difficulty**: Intermediate  
**Time**: 75 minutes

---

## 🎯 Objectives

Practice TDD with stateful objects, date handling, and business logic.

By completing this exercise, you will:

- Test stateful objects with TDD
- Handle temporal data (dates/times)
- Design class interfaces through tests
- Practice mocking and dependency injection
- Build complex business logic incrementally

---

## Problem Description

Create a `BankAccount` class that manages deposits, withdrawals, and provides an account statement.

### Requirements

**Basic Operations**:

- `deposit(amount)` - Add money to account
- `withdraw(amount)` - Remove money from account
- `get_balance()` - Return current balance

**Transaction History**:

- `statement()` - Print account statement with all transactions

**Business Rules**:

- Account starts with balance of 0
- Cannot withdraw more than current balance (overdraft protection)
- All transactions are recorded with date and time
- Statement shows date, transaction type, amount, and running balance

### Statement Format

```
Date       | Amount  | Balance
---------------------------------
2026-08-04 | +500.00 | 500.00
2026-08-03 | -100.00 | 0.00
2026-08-02 | +100.00 | 100.00
```

Note: Most recent transactions appear first (reverse chronological order).

---

## Why Bank Account?

This kata is valuable because:

- **Stateful**: Tests must manage object state over time
- **Real-world**: Banking is familiar domain
- **Temporal data**: Must handle dates correctly
- **Testability**: Forces good design decisions
- **Separation of concerns**: Display logic vs business logic
- **Dependency injection**: Learn to inject date/time

Created by Sandro Mancuso, this kata teaches testing of stateful systems.

---

## Design Considerations

### Challenge: Testing with Dates

Dates are challenging to test because they change! Consider these approaches:

**Approach 1: Inject Date**

```python
def deposit(self, amount, date=None):
    if date is None:
        date = datetime.now()
    # Use date
```

**Approach 2: Clock Abstraction**

```python
class Clock:
    def now(self):
        return datetime.now()

class BankAccount:
    def __init__(self, clock=None):
        self.clock = clock or Clock()

    def deposit(self, amount):
        date = self.clock.now()
```

**Approach 3: Mock datetime** (not recommended)

```python
# Using unittest.mock - harder to maintain
```

For this kata, use **Approach 1** (inject date) for simplicity.

---

## Step-by-Step TDD Guide

### Step 1: Initial Balance is Zero

**Test First**:

```python
def test_new_account_has_zero_balance():
    account = BankAccount()
    assert account.get_balance() == 0
```

```javascript
test("new account has zero balance", () => {
  const account = new BankAccount();
  expect(account.getBalance()).toBe(0);
});
```

**Implementation**:

```python
class BankAccount:
    def __init__(self):
        self.balance = 0

    def get_balance(self):
        return self.balance
```

```javascript
class BankAccount {
  constructor() {
    this.balance = 0;
  }

  getBalance() {
    return this.balance;
  }
}
```

---

### Step 2: Deposit Increases Balance

**Test First**:

```python
def test_deposit_increases_balance():
    account = BankAccount()
    account.deposit(100)
    assert account.get_balance() == 100
```

**Implementation**:

```python
def deposit(self, amount):
    self.balance += amount
```

```javascript
deposit(amount) {
  this.balance += amount;
}
```

---

### Step 3: Multiple Deposits

**Test First**:

```python
def test_multiple_deposits():
    account = BankAccount()
    account.deposit(100)
    account.deposit(50)
    assert account.get_balance() == 150
```

**Run test**: Should PASS with existing implementation.

---

### Step 4: Withdrawal Decreases Balance

**Test First**:

```python
def test_withdrawal_decreases_balance():
    account = BankAccount()
    account.deposit(100)
    account.withdraw(30)
    assert account.get_balance() == 70
```

**Implementation**:

```python
def withdraw(self, amount):
    self.balance -= amount
```

---

### Step 5: Cannot Overdraw

**Test First**:

```python
def test_cannot_withdraw_more_than_balance():
    account = BankAccount()
    account.deposit(50)

    with pytest.raises(InsufficientFundsError):
        account.withdraw(100)

    assert account.get_balance() == 50  # Balance unchanged
```

```javascript
test("cannot withdraw more than balance", () => {
  const account = new BankAccount();
  account.deposit(50);

  expect(() => account.withdraw(100)).toThrow("Insufficient funds");
  expect(account.getBalance()).toBe(50); // Balance unchanged
});
```

**Implementation**:

```python
class InsufficientFundsError(Exception):
    pass

def withdraw(self, amount):
    if amount > self.balance:
        raise InsufficientFundsError("Insufficient funds")
    self.balance -= amount
```

```javascript
withdraw(amount) {
  if (amount > this.balance) {
    throw new Error("Insufficient funds");
  }
  this.balance -= amount;
}
```

---

### Step 6: Record Transactions

**Test First**:

```python
from datetime import date

def test_records_deposit_transaction():
    account = BankAccount()
    account.deposit(100, date(2026, 8, 2))

    transactions = account.get_transactions()
    assert len(transactions) == 1
    assert transactions[0].amount == 100
    assert transactions[0].date == date(2026, 8, 2)
```

**Implementation** (Refactor to track transactions):

```python
from dataclasses import dataclass
from datetime import date, datetime
from typing import List

@dataclass
class Transaction:
    date: date
    amount: float
    balance_after: float

class BankAccount:
    def __init__(self):
        self.balance = 0
        self.transactions: List[Transaction] = []

    def deposit(self, amount, transaction_date=None):
        if transaction_date is None:
            transaction_date = datetime.now().date()

        self.balance += amount
        self.transactions.append(
            Transaction(transaction_date, amount, self.balance)
        )

    def withdraw(self, amount, transaction_date=None):
        if transaction_date is None:
            transaction_date = datetime.now().date()

        if amount > self.balance:
            raise InsufficientFundsError("Insufficient funds")

        self.balance -= amount
        self.transactions.append(
            Transaction(transaction_date, -amount, self.balance)
        )

    def get_balance(self):
        return self.balance

    def get_transactions(self):
        return self.transactions
```

---

### Step 7: Generate Statement

**Test First**:

```python
def test_statement_shows_transactions():
    account = BankAccount()
    account.deposit(100, date(2026, 8, 2))
    account.withdraw(50, date(2026, 8, 3))
    account.deposit(200, date(2026, 8, 4))

    statement = account.statement()

    expected = """Date       | Amount   | Balance
--------------------------------------
2026-08-04 | +200.00  | 250.00
2026-08-03 | -50.00   | 50.00
2026-08-02 | +100.00  | 100.00"""

    assert statement == expected
```

```javascript
test("statement shows transactions", () => {
  const account = new BankAccount();
  account.deposit(100, new Date(2026, 7, 2)); // Month is 0-indexed
  account.withdraw(50, new Date(2026, 7, 3));
  account.deposit(200, new Date(2026, 7, 4));

  const statement = account.statement();

  const expected = `Date       | Amount   | Balance
--------------------------------------
2026-08-04 | +200.00  | 250.00
2026-08-03 | -50.00   | 50.00
2026-08-02 | +100.00  | 100.00`;

  expect(statement).toBe(expected);
});
```

**Implementation**:

```python
def statement(self):
    """Generate account statement."""
    lines = ["Date       | Amount   | Balance"]
    lines.append("-" * 38)

    # Reverse chronological order
    for trans in reversed(self.transactions):
        amount_str = f"{trans.amount:+.2f}"
        balance_str = f"{trans.balance_after:.2f}"
        date_str = trans.date.strftime("%Y-%m-%d")

        lines.append(f"{date_str} | {amount_str:8} | {balance_str}")

    return "\n".join(lines)
```

```javascript
statement() {
  const lines = ["Date       | Amount   | Balance"];
  lines.push("-".repeat(38));

  // Reverse chronological order
  const reversed = [...this.transactions].reverse();

  for (const trans of reversed) {
    const amountStr = (trans.amount >= 0 ? "+" : "") +
                      trans.amount.toFixed(2);
    const balanceStr = trans.balanceAfter.toFixed(2);
    const dateStr = trans.date.toISOString().split('T')[0];

    lines.push(
      `${dateStr} | ${amountStr.padStart(8)} | ${balanceStr}`
    );
  }

  return lines.join("\n");
}
```

---

### Step 8: Empty Statement

**Test First**:

```python
def test_empty_statement():
    account = BankAccount()
    statement = account.statement()

    expected = """Date       | Amount   | Balance
--------------------------------------"""

    assert statement == expected
```

**Run test**: Should PASS with existing implementation.

---

## Complete Solution

### Python (pytest)

```python
from dataclasses import dataclass
from datetime import date, datetime
from typing import List


class InsufficientFundsError(Exception):
    """Raised when withdrawal exceeds balance."""
    pass


@dataclass
class Transaction:
    """Record of a single transaction."""
    date: date
    amount: float
    balance_after: float


class BankAccount:
    """
    Bank account with deposit, withdrawal, and statement features.

    Usage:
        account = BankAccount()
        account.deposit(100)
        account.withdraw(30)
        print(account.statement())
    """

    def __init__(self):
        """Initialize account with zero balance."""
        self.balance = 0.0
        self.transactions: List[Transaction] = []

    def deposit(self, amount: float, transaction_date: date = None) -> None:
        """
        Deposit money into account.

        Args:
            amount: Amount to deposit (must be positive)
            transaction_date: Date of transaction (default: today)

        Raises:
            ValueError: If amount is not positive
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")

        if transaction_date is None:
            transaction_date = datetime.now().date()

        self.balance += amount
        self.transactions.append(
            Transaction(transaction_date, amount, self.balance)
        )

    def withdraw(self, amount: float, transaction_date: date = None) -> None:
        """
        Withdraw money from account.

        Args:
            amount: Amount to withdraw (must be positive)
            transaction_date: Date of transaction (default: today)

        Raises:
            ValueError: If amount is not positive
            InsufficientFundsError: If amount exceeds balance
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")

        if amount > self.balance:
            raise InsufficientFundsError(
                f"Insufficient funds: balance is {self.balance:.2f}, "
                f"attempted to withdraw {amount:.2f}"
            )

        if transaction_date is None:
            transaction_date = datetime.now().date()

        self.balance -= amount
        self.transactions.append(
            Transaction(transaction_date, -amount, self.balance)
        )

    def get_balance(self) -> float:
        """Return current balance."""
        return self.balance

    def get_transactions(self) -> List[Transaction]:
        """Return list of all transactions."""
        return self.transactions.copy()

    def statement(self) -> str:
        """
        Generate account statement.

        Returns:
            Formatted statement string with all transactions
            in reverse chronological order.
        """
        lines = ["Date       | Amount   | Balance"]
        lines.append("-" * 38)

        # Reverse chronological order
        for trans in reversed(self.transactions):
            amount_str = f"{trans.amount:+.2f}"
            balance_str = f"{trans.balance_after:.2f}"
            date_str = trans.date.strftime("%Y-%m-%d")

            lines.append(f"{date_str} | {amount_str:>8} | {balance_str}")

        return "\n".join(lines)


# Tests
import pytest


class TestBankAccount:
    def test_new_account_has_zero_balance(self):
        account = BankAccount()
        assert account.get_balance() == 0

    def test_deposit_increases_balance(self):
        account = BankAccount()
        account.deposit(100)
        assert account.get_balance() == 100

    def test_multiple_deposits(self):
        account = BankAccount()
        account.deposit(100)
        account.deposit(50)
        account.deposit(25)
        assert account.get_balance() == 175

    def test_withdrawal_decreases_balance(self):
        account = BankAccount()
        account.deposit(100)
        account.withdraw(30)
        assert account.get_balance() == 70

    def test_multiple_withdrawals(self):
        account = BankAccount()
        account.deposit(100)
        account.withdraw(20)
        account.withdraw(30)
        assert account.get_balance() == 50

    def test_cannot_withdraw_more_than_balance(self):
        account = BankAccount()
        account.deposit(50)

        with pytest.raises(InsufficientFundsError):
            account.withdraw(100)

        assert account.get_balance() == 50  # Balance unchanged

    def test_cannot_withdraw_from_empty_account(self):
        account = BankAccount()

        with pytest.raises(InsufficientFundsError):
            account.withdraw(10)

    def test_deposit_must_be_positive(self):
        account = BankAccount()

        with pytest.raises(ValueError):
            account.deposit(-50)

        with pytest.raises(ValueError):
            account.deposit(0)

    def test_withdrawal_must_be_positive(self):
        account = BankAccount()
        account.deposit(100)

        with pytest.raises(ValueError):
            account.withdraw(-20)

        with pytest.raises(ValueError):
            account.withdraw(0)

    def test_records_deposit_transaction(self):
        account = BankAccount()
        account.deposit(100, date(2026, 8, 2))

        transactions = account.get_transactions()
        assert len(transactions) == 1
        assert transactions[0].amount == 100
        assert transactions[0].date == date(2026, 8, 2)
        assert transactions[0].balance_after == 100

    def test_records_withdrawal_transaction(self):
        account = BankAccount()
        account.deposit(100, date(2026, 8, 2))
        account.withdraw(30, date(2026, 8, 3))

        transactions = account.get_transactions()
        assert len(transactions) == 2
        assert transactions[1].amount == -30
        assert transactions[1].balance_after == 70

    def test_empty_statement(self):
        account = BankAccount()
        statement = account.statement()

        expected = """Date       | Amount   | Balance
--------------------------------------"""

        assert statement == expected

    def test_statement_with_single_deposit(self):
        account = BankAccount()
        account.deposit(100, date(2026, 8, 2))

        statement = account.statement()

        assert "2026-08-02" in statement
        assert "+100.00" in statement
        assert "100.00" in statement

    def test_statement_shows_transactions_in_reverse_order(self):
        account = BankAccount()
        account.deposit(100, date(2026, 8, 2))
        account.withdraw(50, date(2026, 8, 3))
        account.deposit(200, date(2026, 8, 4))

        statement = account.statement()

        # Most recent first
        lines = statement.split("\n")
        assert "2026-08-04" in lines[2]  # After header
        assert "2026-08-03" in lines[3]
        assert "2026-08-02" in lines[4]

    def test_complete_statement(self):
        account = BankAccount()
        account.deposit(1000, date(2026, 8, 1))
        account.withdraw(100, date(2026, 8, 2))
        account.deposit(500, date(2026, 8, 3))
        account.withdraw(200, date(2026, 8, 4))

        statement = account.statement()

        expected = """Date       | Amount   | Balance
--------------------------------------
2026-08-04 | -200.00  | 1200.00
2026-08-03 | +500.00  | 1400.00
2026-08-02 | -100.00  | 900.00
2026-08-01 | +1000.00 | 1000.00"""

        assert statement == expected

    def test_statement_format_with_various_amounts(self):
        account = BankAccount()
        account.deposit(1, date(2026, 8, 1))
        account.deposit(10.50, date(2026, 8, 2))
        account.withdraw(5.25, date(2026, 8, 3))

        statement = account.statement()

        assert "+1.00" in statement
        assert "+10.50" in statement
        assert "-5.25" in statement
```

### JavaScript (Jest)

```javascript
class InsufficientFundsError extends Error {
  constructor(message) {
    super(message);
    this.name = "InsufficientFundsError";
  }
}

class Transaction {
  constructor(date, amount, balanceAfter) {
    this.date = date;
    this.amount = amount;
    this.balanceAfter = balanceAfter;
  }
}

class BankAccount {
  constructor() {
    this.balance = 0;
    this.transactions = [];
  }

  deposit(amount, transactionDate = null) {
    if (amount <= 0) {
      throw new Error("Deposit amount must be positive");
    }

    if (transactionDate === null) {
      transactionDate = new Date();
    }

    this.balance += amount;
    this.transactions.push(
      new Transaction(transactionDate, amount, this.balance),
    );
  }

  withdraw(amount, transactionDate = null) {
    if (amount <= 0) {
      throw new Error("Withdrawal amount must be positive");
    }

    if (amount > this.balance) {
      throw new InsufficientFundsError(
        `Insufficient funds: balance is ${this.balance.toFixed(2)}, ` +
          `attempted to withdraw ${amount.toFixed(2)}`,
      );
    }

    if (transactionDate === null) {
      transactionDate = new Date();
    }

    this.balance -= amount;
    this.transactions.push(
      new Transaction(transactionDate, -amount, this.balance),
    );
  }

  getBalance() {
    return this.balance;
  }

  getTransactions() {
    return [...this.transactions];
  }

  statement() {
    const lines = ["Date       | Amount   | Balance"];
    lines.push("-".repeat(38));

    // Reverse chronological order
    const reversed = [...this.transactions].reverse();

    for (const trans of reversed) {
      const amountStr =
        (trans.amount >= 0 ? "+" : "") + trans.amount.toFixed(2);
      const balanceStr = trans.balanceAfter.toFixed(2);
      const dateStr = trans.date.toISOString().split("T")[0];

      lines.push(`${dateStr} | ${amountStr.padStart(8)} | ${balanceStr}`);
    }

    return lines.join("\n");
  }
}

describe("BankAccount", () => {
  test("new account has zero balance", () => {
    const account = new BankAccount();
    expect(account.getBalance()).toBe(0);
  });

  test("deposit increases balance", () => {
    const account = new BankAccount();
    account.deposit(100);
    expect(account.getBalance()).toBe(100);
  });

  test("multiple deposits", () => {
    const account = new BankAccount();
    account.deposit(100);
    account.deposit(50);
    account.deposit(25);
    expect(account.getBalance()).toBe(175);
  });

  test("withdrawal decreases balance", () => {
    const account = new BankAccount();
    account.deposit(100);
    account.withdraw(30);
    expect(account.getBalance()).toBe(70);
  });

  test("cannot withdraw more than balance", () => {
    const account = new BankAccount();
    account.deposit(50);

    expect(() => account.withdraw(100)).toThrow(InsufficientFundsError);
    expect(account.getBalance()).toBe(50);
  });

  test("deposit must be positive", () => {
    const account = new BankAccount();
    expect(() => account.deposit(-50)).toThrow();
    expect(() => account.deposit(0)).toThrow();
  });

  test("records transactions", () => {
    const account = new BankAccount();
    const testDate = new Date(2026, 7, 2);
    account.deposit(100, testDate);

    const transactions = account.getTransactions();
    expect(transactions).toHaveLength(1);
    expect(transactions[0].amount).toBe(100);
  });

  test("statement shows transactions in reverse order", () => {
    const account = new BankAccount();
    account.deposit(100, new Date(2026, 7, 2));
    account.withdraw(50, new Date(2026, 7, 3));
    account.deposit(200, new Date(2026, 7, 4));

    const statement = account.statement();
    const lines = statement.split("\n");

    expect(lines[2]).toContain("2026-08-04");
    expect(lines[3]).toContain("2026-08-03");
    expect(lines[4]).toContain("2026-08-02");
  });

  test("complete statement", () => {
    const account = new BankAccount();
    account.deposit(1000, new Date(2026, 7, 1));
    account.withdraw(100, new Date(2026, 7, 2));
    account.deposit(500, new Date(2026, 7, 3));
    account.withdraw(200, new Date(2026, 7, 4));

    const statement = account.statement();

    expect(statement).toContain("+1000.00");
    expect(statement).toContain("-100.00");
    expect(statement).toContain("+500.00");
    expect(statement).toContain("-200.00");
  });
});

module.exports = { BankAccount, InsufficientFundsError };
```

---

## Evaluation Criteria

| Criteria                 | Points | Description                                 |
| ------------------------ | ------ | ------------------------------------------- |
| **TDD Process**          | 20     | Tests written first, small steps            |
| **State Management**     | 25     | Correct balance tracking                    |
| **Transaction History**  | 20     | Properly records all transactions           |
| **Statement Generation** | 20     | Correct format, reverse chronological order |
| **Error Handling**       | 15     | Validates input, prevents overdraft         |

**Total**: 100 points

---

## Common Mistakes

❌ **Not injecting dates**  
✅ Pass date as parameter for testability

❌ **Storing balance only**  
✅ Calculate from transactions OR store both

❌ **Wrong statement order**  
✅ Most recent first (reverse chronological)

❌ **Poor formatting**  
✅ Aligned columns, consistent decimal places

❌ **Allowing negative deposits**  
✅ Validate all inputs

---

## Tips for Success

1. **Test State Changes**: Each test should verify state after operations
2. **Inject Dates**: Makes tests deterministic
3. **Small Steps**: Start with balance, add transactions later
4. **Helper Methods**: Format currency, format dates
5. **Edge Cases**: Empty account, exact balance withdrawal
6. **Separation of Concerns**: Business logic vs presentation
7. **Immutability**: Return copies of transaction list

---

## Bonus Challenges

### Challenge 1: Interest Calculation

Add interest:

```python
def apply_interest(self, rate: float, transaction_date: date = None):
    """Apply interest at given rate (e.g., 0.05 for 5%)"""
    interest = self.balance * rate
    self.deposit(interest, transaction_date)
```

### Challenge 2: Transaction Categories

Add categories:

```python
def deposit(self, amount, category="deposit", transaction_date=None):
    # Track category
    pass

def statement_by_category(self):
    # Group by category
    pass
```

### Challenge 3: Account Limits

Add daily limits:

```python
def set_daily_withdrawal_limit(self, limit):
    pass

def get_daily_withdrawals(self, date):
    pass
```

---

## Deliverables

1. **Complete BankAccount class** with all tests passing
2. **Transaction history** properly recorded
3. **Statement generation** with correct formatting
4. **Error handling** for edge cases
5. **Git history** showing TDD progression
6. **Reflection** (1 page) on testing stateful objects

---

## Resources

- [Bank Account Kata](https://kata-log.rocks/banking-kata) - Original by Sandro Mancuso
- [Testing Stateful Systems](https://martinfowler.com/articles/testing-strategies.html)
- [Dependency Injection](https://en.wikipedia.org/wiki/Dependency_injection)

---

## Next Steps

1. Review [Theory: Testing Stateful Objects](../theory/06-stateful-testing.md)
2. Complete [Homework: Custom Kata](../homework/homework-6.md)
3. Watch Sandro Mancuso's demonstration
4. Try adding bonus features with TDD

---

**Bank Account teaches you how to test and design stateful systems with TDD!**
