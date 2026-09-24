"""Equivalence Partitioning tests for SecureBank."""

import pytest

from src.banking_system import BankAccount


class TestEquivalencePartitioning:
    """Tests based on representative equivalence classes."""

    def test_valid_transfer_amount(self):
        """EP1: Valid transfer amount should succeed."""
        account = BankAccount("Checking", 2000)

        result = account.transfer(500)

        assert result["success"] is True
        assert account.balance == 1500

    def test_zero_transfer_amount(self):
        """EP2: Zero transfer amount should fail."""
        account = BankAccount("Checking", 2000)

        result = account.transfer(0)

        assert result["success"] is False
        assert "positive" in result["error"]

    def test_negative_transfer_amount(self):
        """EP3: Negative transfer amount should fail."""
        account = BankAccount("Checking", 2000)

        result = account.transfer(-100)

        assert result["success"] is False
        assert "positive" in result["error"]

    def test_transfer_exceeds_daily_limit(self):
        """EP4: Transfer above daily limit should fail."""
        account = BankAccount("Checking", 10000)

        result = account.transfer(5000.01)

        assert result["success"] is False
        assert "daily limit" in result["error"]

    def test_transfer_exceeds_balance(self):
        """EP5: Transfer above available balance should fail."""
        account = BankAccount("Checking", 1000)

        result = account.transfer(1001)

        assert result["success"] is False
        assert "Insufficient funds" in result["error"]

    def test_invalid_account_type(self):
        """EP6: Invalid account type should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid account type"):
            BankAccount("Business", 1000)

    def test_negative_initial_balance(self):
        """EP7: Negative initial balance should raise ValueError."""
        with pytest.raises(
            ValueError, match="Initial balance cannot be negative"
        ):
            BankAccount("Checking", -1)

    def test_zero_deposit_amount(self):
        """EP8: Zero deposit amount should be rejected."""
        account = BankAccount("Checking", 1000)

        result = account.deposit(0)

        assert result["success"] is False
        assert "positive" in result["error"]

    def test_non_string_payee(self):
        """EP9: Non-string payee should be rejected."""
        account = BankAccount("Checking", 1000)

        result = account.pay_bill(12345, 100)

        assert result["success"] is False
        assert "Invalid payee" in result["error"]