"""
Equivalence Partitioning Tests — SecureBank Online Banking System.

Tests based on the equivalence classes identified in:
  design/test-design-document.md — Section 1.1

Each test references its partition ID (EP-xx) to link implementation
back to the design document.

Technique: Equivalence Partitioning (EP)
  - Valid partitions: representative values that should succeed.
  - Invalid partitions: representative values that should be rejected.
"""

import pytest

from src.banking_system import AccountState, AccountType, BankAccount, BankingSystem


class TestTransferAmountPartitions:
    """EP — Input: Transfer Amount (5 partitions)."""

    def test_ep01_valid_amount_within_limits(self, checking_account):
        """EP-01: Valid amount within daily limit and balance → Transfer succeeds."""
        result = checking_account.transfer(500.00)
        assert result["success"] is True
        assert result["error"] is None
        assert checking_account.balance == pytest.approx(500.00, abs=0.01)

    def test_ep02_zero_amount_rejected(self, checking_account):
        """EP-02: Zero amount → Error: Amount must be positive (min $0.01)."""
        result = checking_account.transfer(0.00)
        assert result["success"] is False
        assert "positive" in result["error"].lower()

    def test_ep03_negative_amount_rejected(self, checking_account):
        """EP-03: Negative amount → Error: Amount must be positive."""
        result = checking_account.transfer(-100.00)
        assert result["success"] is False
        assert "positive" in result["error"].lower()

    def test_ep04_amount_exceeds_daily_limit(self):
        """EP-04: Amount > daily limit ($5,000 for Checking) → Error: Exceeds daily limit."""
        # Use a very large balance so insufficient-funds is never triggered first
        rich_account = BankAccount(AccountType.CHECKING, 200_000.00)
        result = rich_account.transfer(100_000.00)
        assert result["success"] is False
        assert "daily" in result["error"].lower() or "limit" in result["error"].lower()

    def test_ep05_amount_exceeds_balance(self, checking_account):
        """EP-05: Amount > current balance → Error: Insufficient funds."""
        result = checking_account.transfer(checking_account.balance + 1.00)
        assert result["success"] is False
        assert "insufficient" in result["error"].lower()


class TestAccountTypePartitions:
    """EP — Input: Account Type (4 partitions)."""

    def test_ep06_savings_account_type_valid(self):
        """EP-06: Valid account type 'Savings' → Account created successfully."""
        account = BankAccount(AccountType.SAVINGS, 500.00)
        assert account.account_type == AccountType.SAVINGS
        assert account.get_daily_limit() == 2_000.00

    def test_ep07_checking_account_type_valid(self):
        """EP-07: Valid account type 'Checking' → Account created successfully."""
        account = BankAccount(AccountType.CHECKING, 500.00)
        assert account.account_type == AccountType.CHECKING
        assert account.get_daily_limit() == 5_000.00

    def test_ep08_premium_account_type_valid(self):
        """EP-08: Valid account type 'Premium' → Account created successfully."""
        account = BankAccount(AccountType.PREMIUM, 10_000.00)
        assert account.account_type == AccountType.PREMIUM
        assert account.get_daily_limit() == 50_000.00

    def test_ep09_invalid_account_type_rejected(self):
        """EP-09: Invalid account type → ValueError raised."""
        with pytest.raises(ValueError, match="Unknown account type"):
            BankAccount("Gold", 500.00)


class TestAccountBalancePartitions:
    """EP — Input: Account Balance (3 partitions relative to minimum)."""

    def test_ep10_balance_above_minimum_active(self):
        """EP-10: Balance well above minimum → Account state is Active."""
        account = BankAccount(AccountType.SAVINGS, 500.00)
        assert account.state == AccountState.ACTIVE

    def test_ep11_balance_below_minimum_suspended(self):
        """EP-11: Initial balance below $100 minimum (Savings) → Account is Suspended."""
        account = BankAccount(AccountType.SAVINGS, 50.00)
        assert account.state == AccountState.SUSPENDED

    def test_ep12_zero_balance_checking_allowed(self):
        """EP-12: Checking has $0 minimum; zero initial balance → Active state."""
        account = BankAccount(AccountType.CHECKING, 0.00)
        assert account.state == AccountState.ACTIVE


class TestPayeePartitions:
    """EP — Input: Payee (bill payment) — 3 partitions."""

    def test_ep13_valid_payee_bill_payment_succeeds(self, checking_account):
        """EP-13: Valid non-empty payee string → Bill payment succeeds."""
        result = checking_account.pay_bill("Electric Company", 50.00)
        assert result["success"] is True

    def test_ep14_empty_payee_rejected(self, checking_account):
        """EP-14: Empty payee string → Error: Payee name is required."""
        result = checking_account.pay_bill("", 50.00)
        assert result["success"] is False
        assert "payee" in result["error"].lower()

    def test_ep15_whitespace_payee_rejected(self, checking_account):
        """EP-15: Whitespace-only payee → Error: Payee name is required."""
        result = checking_account.pay_bill("   ", 50.00)
        assert result["success"] is False
        assert "payee" in result["error"].lower()


class TestDateRangePartitions:
    """EP — Input: Date range for transaction history — 3 partitions."""

    def test_ep16_no_date_filter_returns_all(self, checking_account):
        """EP-16: No date filter → All transactions returned successfully."""
        checking_account.transfer(50.00)
        result = checking_account.get_transaction_history()
        assert result["success"] is True
        assert len(result["transactions"]) >= 1

    def test_ep17_valid_date_range_returns_filtered(self, checking_account):
        """EP-17: Valid start ≤ end date range → Filtered transactions returned."""
        from datetime import date
        checking_account.deposit(100.00)
        today = date.today()
        result = checking_account.get_transaction_history(
            start_date=today, end_date=today
        )
        assert result["success"] is True

    def test_ep18_invalid_date_range_rejected(self, checking_account):
        """EP-18: Start date after end date → Error returned."""
        from datetime import date, timedelta
        today = date.today()
        result = checking_account.get_transaction_history(
            start_date=today,
            end_date=today - timedelta(days=1),
        )
        assert result["success"] is False
        assert "date" in result["error"].lower()
