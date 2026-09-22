"""Equivalence Partitioning tests for SecureBank."""

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