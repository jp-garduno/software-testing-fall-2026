"""Decision Table tests for SecureBank."""

from src.banking_system import BankAccount


class TestDecisionTables:
    """Tests derived from SecureBank decision tables."""

    def test_transfer_valid_conditions(self):
        """DT1: Sufficient funds + within limit + active = success."""
        account = BankAccount("Checking", 10000)

        result = account.transfer(1000)

        assert result["success"] is True
        assert account.balance == 9000

    def test_transfer_frozen_account(self):
        """DT2: Transfer from frozen account must fail."""
        account = BankAccount("Checking", 10000)
        account.freeze()

        result = account.transfer(1000)

        assert result["success"] is False
        assert "not active" in result["error"]

    def test_transfer_over_daily_limit(self):
        """DT3: Transfer over daily limit must fail."""
        account = BankAccount("Savings", 10000)

        result = account.transfer(2000.01)

        assert result["success"] is False
        assert "daily limit" in result["error"]

    def test_checking_fee_waived(self):
        """DT4: Checking fee is waived above $5,000."""
        account = BankAccount("Checking", 5000.01)

        result = account.process_monthly_fee()

        assert result["success"] is True
        assert result["fee_charged"] == 0
        assert account.balance == 5000.01

    def test_savings_fee_charged(self):
        """DT5: Savings fee is charged when waiver condition is not met."""
        account = BankAccount("Savings", 1000)

        result = account.process_monthly_fee()

        assert result["success"] is True
        assert result["fee_charged"] == 5
        assert account.balance == 995

    def test_bill_payment_invalid_payee(self):
        """DT6: Bill payment with invalid payee must fail."""
        account = BankAccount("Checking", 3000)

        result = account.pay_bill("", 100)

        assert result["success"] is False
        assert "Invalid payee" in result["error"]