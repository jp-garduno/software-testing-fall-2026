from decimal import Decimal

from src.banking_system import BankAccount  # pylint: disable=import-error


class TestBoundaryValues:
    def test_bv1_transfer_zero(self):
        """BV1: $0.00 is immediately below the minimum valid transfer."""
        account = BankAccount("Checking", 1000)
        assert account.transfer(0)["success"] is False

    def test_bv2_transfer_minimum_valid(self):
        """BV2: $0.01 is the minimum valid transfer."""
        account = BankAccount("Checking", 1000)
        assert account.transfer(0.01)["success"] is True
        assert account.balance == Decimal("999.99")

    def test_bv3_checking_just_below_daily_limit(self):
        """BV3: $4,999.99 is just below the Checking daily limit."""
        account = BankAccount("Checking", 10000)
        assert account.transfer(4999.99)["success"] is True

    def test_bv4_checking_at_daily_limit(self):
        """BV4: $5,000.00 is exactly the Checking daily limit."""
        account = BankAccount("Checking", 10000)
        assert account.transfer(5000)["success"] is True

    def test_bv5_checking_just_above_daily_limit(self):
        """BV5: $5,000.01 is just above the Checking daily limit."""
        account = BankAccount("Checking", 10000)
        result = account.transfer(5000.01)
        assert result["success"] is False
        assert "daily limit" in result["error"]

    def test_bv6_savings_just_below_daily_limit(self):
        """BV6: $1,999.99 is just below the Savings daily limit."""
        account = BankAccount("Savings", 10000)
        assert account.transfer(1999.99)["success"] is True

    def test_bv7_savings_at_daily_limit(self):
        """BV7: $2,000.00 is exactly the Savings daily limit."""
        account = BankAccount("Savings", 10000)
        assert account.transfer(2000)["success"] is True

    def test_bv8_savings_just_above_daily_limit(self):
        """BV8: $2,000.01 is just above the Savings daily limit."""
        account = BankAccount("Savings", 10000)
        assert account.transfer(2000.01)["success"] is False

    def test_bv9_savings_balance_below_minimum(self):
        """BV9: Savings $99.99 is below the $100 minimum balance."""
        account = BankAccount("Savings", 99.99)
        assert account.state == "Suspended"

    def test_bv10_savings_balance_at_minimum(self):
        """BV10: Savings $100.00 is exactly the minimum balance."""
        account = BankAccount("Savings", 100)
        assert account.state == "Active"

    def test_bv11_savings_fee_threshold_at_1000_is_not_waived(self):
        """BV11: assignment says waived if balance > $1,000, so exactly $1,000 pays fee."""
        account = BankAccount("Savings", 1000)
        result = account.process_monthly_fee()
        assert result["fee_charged"] == 5
        assert account.balance == 995

    def test_bv12_savings_fee_threshold_just_above_is_waived(self):
        """BV12: $1,000.01 is just above the Savings waiver threshold."""
        account = BankAccount("Savings", 1000.01)
        result = account.process_monthly_fee()
        assert result["fee_charged"] == 0
        assert account.balance == Decimal("1000.01")
