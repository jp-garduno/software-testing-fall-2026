"""Boundary Value Analysis tests for SecureBank."""

from src.banking_system import BankAccount


class TestBoundaryValues:
    """Tests focused on transfer amount boundaries."""

    def test_transfer_zero_amount(self):
        """BV1: $0.00 is immediately below the minimum valid amount."""
        account = BankAccount("Checking", 10000)

        result = account.transfer(0.00)

        assert result["success"] is False
        assert "positive" in result["error"]

    def test_transfer_minimum_valid_amount(self):
        """BV2: $0.01 is the minimum valid transfer."""
        account = BankAccount("Checking", 10000)

        result = account.transfer(0.01)

        assert result["success"] is True
        assert account.balance == 9999.99

    def test_transfer_just_below_checking_limit(self):
        """BV3: $4,999.99 is just below the Checking daily limit."""
        account = BankAccount("Checking", 10000)

        result = account.transfer(4999.99)

        assert result["success"] is True
        assert account.daily_transfer_total == 4999.99

    def test_transfer_at_checking_limit(self):
        """BV4: $5,000 is exactly the Checking daily limit."""
        account = BankAccount("Checking", 10000)

        result = account.transfer(5000)

        assert result["success"] is True
        assert account.daily_transfer_total == 5000

    def test_transfer_above_checking_limit(self):
        """BV5: $5,000.01 is immediately above the Checking limit."""
        account = BankAccount("Checking", 10000)

        result = account.transfer(5000.01)

        assert result["success"] is False
        assert "daily limit" in result["error"]

    def test_transfer_above_savings_limit(self):
        """BV6: $2,000.01 is immediately above the Savings limit."""
        account = BankAccount("Savings", 10000)

        result = account.transfer(2000.01)

        assert result["success"] is False
        assert "daily limit" in result["error"]