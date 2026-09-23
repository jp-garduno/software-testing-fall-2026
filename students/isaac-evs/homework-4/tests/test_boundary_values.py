"""Boundary Value Analysis tests — see design/test-design-document.md, Section 2."""

from datetime import date, timedelta

from src.banking_system import BankAccount


class TestCheckingTransferLimitBoundaries:
    def test_bv1_below_minimum_amount(self, checking_account, today):
        """BV1: $0.00 is below the minimum transfer amount and fails."""
        result = checking_account.transfer(0.00, today=today)
        assert result["success"] is False
        assert "must be positive" in result["error"]

    def test_bv2_minimum_valid_amount(self, checking_account, today):
        """BV2: $0.01 is the minimum valid transfer amount and succeeds."""
        result = checking_account.transfer(0.01, today=today)
        assert result["success"] is True
        assert checking_account.balance == 9999.99

    def test_bv3_just_below_daily_limit(self, checking_account, today):
        """BV3: $4,999.99 is just below the $5,000 Checking daily limit and succeeds."""
        result = checking_account.transfer(4999.99, today=today)
        assert result["success"] is True

    def test_bv4_at_daily_limit(self, checking_account, today):
        """BV4: $5,000.00 is exactly at the Checking daily limit and succeeds."""
        result = checking_account.transfer(5000.00, today=today)
        assert result["success"] is True
        assert checking_account.daily_transfer_total == 5000.00

    def test_bv5_just_above_daily_limit(self, checking_account, today):
        """BV5: $5,000.01 is just above the Checking daily limit and fails."""
        result = checking_account.transfer(5000.01, today=today)
        assert result["success"] is False
        assert "daily limit" in result["error"]

    def test_bv6_far_above_daily_limit(self, checking_account, today):
        """BV6: $10,000.00 is far above the Checking daily limit and fails."""
        result = checking_account.transfer(10000.00, today=today)
        assert result["success"] is False
        assert "daily limit" in result["error"]

    def test_daily_limit_resets_on_a_new_day(self, checking_account, today):
        """The daily transfer total resets to $0 once a new calendar day begins."""
        checking_account.transfer(5000, today=today)
        assert checking_account.daily_transfer_total == 5000
        result = checking_account.transfer(5000, today=today + timedelta(days=1))
        assert result["success"] is True
        assert checking_account.daily_transfer_total == 5000


class TestSavingsTransferLimitBoundaries:
    def test_bv7_just_below_savings_limit(self, today):
        """BV7: $1,999.99 is just below the $2,000 Savings daily limit and succeeds."""
        account = BankAccount("Savings", 5000, today=today)
        result = account.transfer(1999.99, today=today)
        assert result["success"] is True

    def test_bv8_at_savings_limit(self, today):
        """BV8: $2,000.00 is exactly at the Savings daily limit and succeeds."""
        account = BankAccount("Savings", 5000, today=today)
        result = account.transfer(2000.00, today=today)
        assert result["success"] is True

    def test_bv9_just_above_savings_limit(self, today):
        """BV9: $2,000.01 is just above the Savings daily limit and fails."""
        account = BankAccount("Savings", 5000, today=today)
        result = account.transfer(2000.01, today=today)
        assert result["success"] is False
        assert "daily limit" in result["error"]


class TestSavingsMinimumBalanceBoundaries:
    def test_bv10_just_below_minimum_suspends(self, today):
        """BV10: Ending balance $99.99 (just below Savings' $100 minimum) suspends the account."""
        account = BankAccount("Savings", 150, today=today)
        account.transfer(50.01, today=today)  # balance -> 99.99
        assert account.balance == 99.99
        assert account.state == "Suspended"

    def test_bv11_at_minimum_stays_active(self, today):
        """BV11: Ending balance exactly $100.00 keeps the account Active."""
        account = BankAccount("Savings", 150, today=today)
        account.transfer(50, today=today)  # balance -> 100.00
        assert account.balance == 100.00
        assert account.state == "Active"

    def test_bv12_just_above_minimum_stays_active(self, today):
        """BV12: Ending balance $100.01 (just above the minimum) keeps the account Active."""
        account = BankAccount("Savings", 150, today=today)
        account.transfer(49.99, today=today)  # balance -> 100.01
        assert account.balance == 100.01
        assert account.state == "Active"


class TestPremiumMinimumBalanceBoundaries:
    def test_bv13_just_below_minimum_suspends(self, today):
        """BV13: Ending balance $9,999.99 (just below Premium's $10,000 minimum) suspends the account."""
        account = BankAccount("Premium", 10100, today=today)
        account.transfer(100.01, today=today)  # balance -> 9999.99
        assert account.balance == 9999.99
        assert account.state == "Suspended"

    def test_bv14_at_minimum_stays_active(self, today):
        """BV14: Ending balance exactly $10,000.00 keeps the account Active."""
        account = BankAccount("Premium", 10100, today=today)
        account.transfer(100, today=today)  # balance -> 10000.00
        assert account.balance == 10000.00
        assert account.state == "Active"

    def test_bv15_just_above_minimum_stays_active(self, today):
        """BV15: Ending balance $10,000.01 (just above the minimum) keeps the account Active."""
        account = BankAccount("Premium", 10100, today=today)
        account.transfer(99.99, today=today)  # balance -> 10000.01
        assert account.balance == 10000.01
        assert account.state == "Active"


class TestMonthlyFeeWaiverBoundary:
    def test_bv16_balance_at_threshold_fee_charged(self):
        """BV16: Balance exactly at the $1,000 waiver threshold still gets charged (waiver is strictly '>')."""
        account = BankAccount("Savings", 1000)
        result = account.apply_monthly_fee()
        assert result["success"] is True
        assert result["charged"] == 5
        assert account.balance == 995

    def test_bv17_balance_just_above_threshold_fee_waived(self):
        """BV17: Balance just above the waiver threshold ($1,000.01) gets the fee waived."""
        account = BankAccount("Savings", 1000.01)
        result = account.apply_monthly_fee()
        assert result["success"] is True
        assert result["charged"] == 0.0
        assert account.balance == 1000.01

    def test_bv18_balance_just_below_threshold_fee_charged(self):
        """BV18: Balance just below the waiver threshold ($999.99) gets charged the fee."""
        account = BankAccount("Savings", 999.99)
        result = account.apply_monthly_fee()
        assert result["success"] is True
        assert result["charged"] == 5


class TestInsufficientFundsForFeeBoundary:
    def test_bv19_balance_just_below_fee_amount_suspends(self):
        """BV19: Balance just below the $10 Checking fee amount fails to pay it and suspends."""
        account = BankAccount("Checking", 9.99)
        result = account.apply_monthly_fee()
        assert result["success"] is False
        assert account.state == "Suspended"

    def test_bv20_balance_exactly_at_fee_amount_succeeds(self):
        """BV20: Balance exactly at the $10 Checking fee amount pays it, leaving $0.00."""
        account = BankAccount("Checking", 10.00)
        result = account.apply_monthly_fee()
        assert result["success"] is True
        assert account.balance == 0.00
