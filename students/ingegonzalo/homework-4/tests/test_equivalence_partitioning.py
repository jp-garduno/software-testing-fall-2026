import pytest
from banking_system import BankAccount


class TestEquivalencePartitioning:

    def test_ep1_valid_transfer_amount(self, checking_account):
        """EP1: Valid amount within limits should succeed."""
        result = checking_account.transfer(500)
        assert result["success"] is True
        assert checking_account.balance == 9500

    def test_ep3_negative_transfer_amount(self, checking_account):
        """EP3: Negative amount should be rejected."""
        result = checking_account.transfer(-100)
        assert result["success"] is False
        assert "must be positive" in result["error"]

    def test_ep7_checking_account_type(self):
        """EP7: Checking account applies Checking rules."""
        account = BankAccount("Checking", 500)
        assert account.get_minimum_balance() == 0
        assert account.get_daily_limit() == 5000

    def test_ep9_undefined_account_type(self):
        """EP9: Undefined/unrecognized account type should raise an error."""
        with pytest.raises(ValueError, match="Invalid account type"):
            BankAccount("Undefined", 500)

    def test_ep13_balance_below_minimum_suspends_account(self, savings_account):
        """EP13: A transfer that drops balance below minimum suspends the account."""
        savings_account.transfer(1450)  # 1500 - 1450 = 50, below $100 minimum
        assert savings_account.state == "Suspended"

    def test_ep16_empty_payee_name(self, checking_account):
        """EP16: Empty payee name should be rejected."""
        result = checking_account.pay_bill("", 100)
        assert result["success"] is False
        assert "Invalid payee" in result["error"]