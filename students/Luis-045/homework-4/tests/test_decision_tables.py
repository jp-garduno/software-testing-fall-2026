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

    def test_monthly_fee_closed_account(self):
        """Closed account cannot process monthly fee."""
        account = BankAccount("Checking", 5000)
        account.close()

        result = account.process_monthly_fee()

        assert result["success"] is False
        assert "closed" in result["error"].lower()

    def test_premium_monthly_fee_waived(self):
        """Premium account never pays a monthly fee."""
        account = BankAccount("Premium", 20000)

        result = account.process_monthly_fee()

        assert result["success"] is True
        assert result["fee_charged"] == 0

    def test_monthly_fee_suspends_savings_account(self):
        """Fee can place Savings account below its minimum balance."""
        account = BankAccount("Savings", 100)

        result = account.process_monthly_fee()

        assert result["success"] is True
        assert result["fee_charged"] == 5
        assert account.balance == 95
        assert account.state == "Suspended"

    def test_bill_payment_from_frozen_account(self):
        """Frozen account cannot pay bills."""
        account = BankAccount("Checking", 1000)
        account.freeze()

        result = account.pay_bill("Electricity", 100)

        assert result["success"] is False
        assert "not active" in result["error"]

    def test_bill_payment_zero_amount(self):
        """Bill payment amount must be positive."""
        account = BankAccount("Checking", 1000)

        result = account.pay_bill("Electricity", 0)

        assert result["success"] is False
        assert "positive" in result["error"]

    def test_bill_payment_insufficient_funds(self):
        """Bill payment above balance must fail."""
        account = BankAccount("Checking", 1000)

        result = account.pay_bill("Electricity", 1001)

        assert result["success"] is False
        assert "Insufficient funds" in result["error"]

    def test_successful_bill_payment(self):
        """Valid bill payment should reduce account balance."""
        account = BankAccount("Checking", 1000)

        result = account.pay_bill("Electricity", 200)

        assert result["success"] is True
        assert account.balance == 800
        assert account.state == "Active"

    def test_bill_payment_can_suspend_savings_account(self):
        """Bill payment below Savings minimum causes suspension."""
        account = BankAccount("Savings", 150)

        result = account.pay_bill("Electricity", 60)

        assert result["success"] is True
        assert account.balance == 90
        assert account.state == "Suspended"