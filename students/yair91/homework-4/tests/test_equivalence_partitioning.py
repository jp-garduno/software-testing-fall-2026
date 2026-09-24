"""Equivalence partitioning tests.

Each test names the partition it represents in
``design/test-design-document.md`` (EP1, EP2, ...). One representative value
per partition: if the partition is right, any other value in it behaves the
same way.
"""

from datetime import date, timedelta

import pytest

from src.banking_system import BankAccount


class TestTransferAmountPartitions:
    """Input: transfer amount."""

    def test_valid_amount_within_limits(self, checking_account):
        """EP1: a valid amount inside the balance and the daily limit."""
        result = checking_account.transfer(500)
        assert result["success"] is True
        assert checking_account.balance == 9500.00

    def test_zero_amount_is_rejected(self, checking_account):
        """EP2: zero is not a positive amount."""
        result = checking_account.transfer(0)
        assert result["success"] is False
        assert result["error"] == "Amount must be positive"

    def test_negative_amount_is_rejected(self, checking_account):
        """EP3: a negative amount is not a withdrawal in reverse."""
        result = checking_account.transfer(-100)
        assert result["success"] is False
        assert result["error"] == "Amount must be positive"

    def test_amount_above_daily_limit_is_rejected(self, checking_account):
        """EP4: above the daily limit, even with the funds available."""
        result = checking_account.transfer(100000)
        assert result["success"] is False
        assert result["error"] == "Exceeds daily limit"

    def test_amount_above_balance_is_rejected(self, savings_account):
        """EP5: inside the daily limit but more than the account holds."""
        result = savings_account.transfer(savings_account.balance + 1)
        assert result["success"] is False
        assert result["error"] == "Insufficient funds"

    def test_non_numeric_amount_is_rejected(self, checking_account):
        """EP6: a value that is not a number at all."""
        result = checking_account.transfer("five hundred")
        assert result["success"] is False
        assert result["error"] == "Amount must be a number"


class TestAccountTypePartitions:
    """Input: account type. Each type is its own partition."""

    def test_savings_daily_limit(self, savings_account):
        """EP7: Savings accounts are limited to $2,000 per day."""
        assert savings_account.get_daily_limit() == 2000

    def test_checking_daily_limit(self, checking_account):
        """EP8: Checking accounts are limited to $5,000 per day."""
        assert checking_account.get_daily_limit() == 5000

    def test_premium_daily_limit(self, premium_account):
        """EP9: Premium accounts are limited to $50,000 per day."""
        assert premium_account.get_daily_limit() == 50000

    def test_unknown_account_type_is_rejected(self):
        """EP10: a type outside the three supported ones."""
        with pytest.raises(ValueError):
            BankAccount("Platinum", 1000)


class TestAccountBalancePartitions:
    """Input: account balance, read against the type minimum."""

    def test_balance_at_or_above_minimum_keeps_account_active(self):
        """EP11: a balance that meets the minimum leaves the account Active."""
        account = BankAccount("Savings", 50.0)
        account.deposit(100)
        assert account.balance == 150.00
        assert account.state == "Active"

    def test_balance_below_minimum_suspends_account(self, savings_account):
        """EP12: a balance under the minimum moves the account to Suspended."""
        savings_account.transfer(1450)
        assert savings_account.balance == 50.00
        assert savings_account.state == "Suspended"


class TestPayeePartitions:
    """Input: payee for a bill payment."""

    def test_valid_payee_is_accepted(self, checking_account):
        """EP13: a named payee."""
        result = checking_account.pay_bill("City Water", 120)
        assert result["success"] is True
        assert checking_account.balance == 9880.00

    def test_empty_payee_is_rejected(self, checking_account):
        """EP14: an empty or blank payee is not a payee."""
        result = checking_account.pay_bill("   ", 120)
        assert result["success"] is False
        assert result["error"] == "Invalid payee"


class TestDateRangePartitions:
    """Input: date range for the transaction history."""

    def test_range_containing_transactions_returns_them(self, checking_account):
        """EP15: a well-formed range that covers today's activity."""
        checking_account.transfer(100)
        checking_account.pay_bill("Gas Co", 50)
        history = checking_account.get_transaction_history(
            date.today() - timedelta(days=1), date.today() + timedelta(days=1)
        )
        assert len(history) == 2

    def test_inverted_range_is_rejected(self, checking_account):
        """EP16: a range whose start is after its end is not a range."""
        with pytest.raises(ValueError):
            checking_account.get_transaction_history(date.today(), date.today() - timedelta(days=5))


class TestAccountStatePartitions:
    """Input: the state an account is constructed in."""

    def test_known_state_is_accepted(self):
        """EP17: one of the four documented states."""
        account = BankAccount("Checking", 1000.0, state="Frozen")
        assert account.state == "Frozen"

    def test_unknown_state_is_rejected(self):
        """EP18: a state outside the four is refused at construction."""
        with pytest.raises(ValueError):
            BankAccount("Checking", 1000.0, state="Dormant")


class TestDepositAmountPartitions:
    """Input: deposit amount."""

    def test_valid_deposit(self, savings_account):
        """EP19: a positive deposit increases the balance."""
        result = savings_account.deposit(250)
        assert result["success"] is True
        assert savings_account.balance == 1750.00

    def test_zero_deposit_is_rejected(self, savings_account):
        """EP20: zero is not a deposit."""
        result = savings_account.deposit(0)
        assert result["success"] is False
        assert result["error"] == "Amount must be positive"

    def test_deposit_into_closed_account_is_rejected(self, savings_account):
        """EP21: a closed account takes no money in."""
        savings_account.close()
        result = savings_account.deposit(250)
        assert result["success"] is False
        assert result["error"] == "Account is closed"


class TestHistoryExport:
    """Output: CSV export of the filtered history."""

    def test_export_includes_header_and_rows(self, checking_account):
        """EP22: the export carries a header plus one row per transaction."""
        checking_account.transfer(100)
        checking_account.pay_bill("Gas Co", 50)
        csv_text = checking_account.export_history_csv()
        lines = csv_text.splitlines()
        assert lines[0] == "date,type,amount,payee"
        assert len(lines) == 3
        assert "Gas Co" in lines[2]

    def test_export_of_an_empty_history(self, checking_account):
        """EP23: with no transactions the export is just the header."""
        assert checking_account.export_history_csv() == "date,type,amount,payee"
