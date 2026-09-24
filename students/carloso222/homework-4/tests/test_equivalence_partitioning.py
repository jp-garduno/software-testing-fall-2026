from datetime import date

import pytest
from src.banking_system import BankAccount  # pylint: disable=import-error


class TestEquivalencePartitioning:
    def test_ep1_valid_transfer_amount(self):
        """EP1: valid transfer amount within balance and daily limit."""
        account = BankAccount("Checking", 2000)
        result = account.transfer(500)
        assert result["success"] is True
        assert account.view_balance() == 1500

    def test_ep2_zero_transfer_amount(self):
        """EP2: zero amount is an invalid partition."""
        account = BankAccount("Checking", 2000)
        result = account.transfer(0)
        assert result["success"] is False
        assert "positive" in result["error"]

    def test_ep3_negative_transfer_amount(self):
        """EP3: negative amount is an invalid partition."""
        account = BankAccount("Checking", 2000)
        result = account.transfer(-100)
        assert result["success"] is False
        assert "positive" in result["error"]

    def test_ep4_transfer_exceeds_daily_limit(self):
        """EP4: amount above the account daily limit is invalid."""
        account = BankAccount("Savings", 10000)
        result = account.transfer(2000.01)
        assert result["success"] is False
        assert "daily limit" in result["error"]

    def test_ep5_transfer_exceeds_balance(self):
        """EP5: amount within limit but above available balance is invalid."""
        account = BankAccount("Checking", 1000)
        result = account.transfer(1500)
        assert result["success"] is False
        assert "Insufficient funds" in result["error"]

    @pytest.mark.parametrize("account_type", ["Savings", "Checking", "Premium"])
    def test_ep6_valid_account_types(self, account_type):
        """EP6: every documented account type belongs to a valid partition."""
        initial = {"Savings": 100, "Checking": 0, "Premium": 10000}[account_type]
        account = BankAccount(account_type, initial)
        assert account.account_type == account_type

    def test_ep7_invalid_account_type(self):
        """EP7: unsupported account type is invalid."""
        with pytest.raises(ValueError, match="Invalid account type"):
            BankAccount("Student", 1000)

    def test_ep8_valid_payee(self):
        """EP8: known bill payee is valid."""
        account = BankAccount("Checking", 1000)
        result = account.pay_bill("Electricity", 100)
        assert result["success"] is True

    def test_ep9_invalid_payee(self):
        """EP9: unknown bill payee is invalid."""
        account = BankAccount("Checking", 1000)
        result = account.pay_bill("Unknown Merchant", 100)
        assert result["success"] is False
        assert "Invalid payee" in result["error"]

    def test_ep10_invalid_date_range(self):
        """EP10: start date after end date is an invalid date-range partition."""
        account = BankAccount("Checking", 1000)
        result = account.filter_transactions([], date(2026, 9, 10), date(2026, 9, 1))
        assert result["success"] is False
        assert "Invalid date range" in result["error"]
