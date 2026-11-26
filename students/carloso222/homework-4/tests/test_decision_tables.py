from src.banking_system import BankAccount  # pylint: disable=import-error


class TestDecisionTables:
    def test_dt1_transfer_all_conditions_valid(self):
        """DT1: sufficient funds + within limit + active => success."""
        account = BankAccount("Checking", 1000)
        assert account.transfer(100)["success"] is True

    def test_dt2_transfer_insufficient_funds(self):
        """DT2: insufficient funds => reject transfer."""
        account = BankAccount("Checking", 100)
        result = account.transfer(200)
        assert result["success"] is False
        assert "Insufficient" in result["error"]

    def test_dt3_transfer_exceeds_limit(self):
        """DT3: sufficient funds but exceeds daily limit => reject."""
        account = BankAccount("Checking", 10000)
        result = account.transfer(5000.01)
        assert result["success"] is False
        assert "daily limit" in result["error"]

    def test_dt4_transfer_frozen_account(self):
        """DT4: frozen account => no transfer."""
        account = BankAccount("Checking", 1000)
        account.freeze()
        result = account.transfer(100)
        assert result["success"] is False
        assert "frozen" in result["error"].lower()

    def test_dt5_savings_fee_waived(self):
        """DT5: Savings balance above waiver threshold => no monthly fee."""
        account = BankAccount("Savings", 1500)
        assert account.process_monthly_fee()["fee_charged"] == 0

    def test_dt6_checking_fee_charged(self):
        """DT6: Checking balance not above threshold => $10 fee."""
        account = BankAccount("Checking", 5000)
        result = account.process_monthly_fee()
        assert result["fee_charged"] == 10

    def test_dt7_premium_never_charged_fee(self):
        """DT7: Premium account monthly fee is always $0."""
        account = BankAccount("Premium", 10000)
        assert account.process_monthly_fee()["fee_charged"] == 0

    def test_dt8_bill_valid_payee_positive_amount_and_funds(self):
        """DT8: all bill-payment conditions valid => payment succeeds."""
        account = BankAccount("Checking", 1000)
        result = account.pay_bill("Internet", 200)
        assert result["success"] is True
        assert account.balance == 800

    def test_dt9_bill_invalid_payee(self):
        """DT9: invalid payee => payment rejected."""
        account = BankAccount("Checking", 1000)
        assert account.pay_bill("FakePayee", 100)["success"] is False

    def test_dt10_bill_insufficient_funds(self):
        """DT10: valid payee and amount but insufficient funds => reject."""
        account = BankAccount("Checking", 50)
        result = account.pay_bill("Water", 100)
        assert result["success"] is False
        assert "Insufficient" in result["error"]
