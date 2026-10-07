"""Boundary value analysis tests.

Every boundary in ``design/test-design-document.md`` is exercised on both
sides plus the value itself, because an off-by-one is invisible from the
middle of a partition. Ids match the BVA tables in that document.
"""

from src.banking_system import BankAccount


class TestCheckingTransferLimitBoundary:
    """Boundary 1: transfer amount against the $5,000 Checking daily limit."""

    def test_below_minimum_transfer(self, checking_account):
        """BV1: $0.00 is below the $0.01 minimum."""
        result = checking_account.transfer(0.00)
        assert result["success"] is False
        assert result["error"] == "Amount must be positive"

    def test_at_minimum_transfer(self, checking_account):
        """BV2: $0.01 is the smallest accepted transfer."""
        result = checking_account.transfer(0.01)
        assert result["success"] is True
        assert checking_account.balance == 9999.99

    def test_just_below_daily_limit(self, checking_account):
        """BV3: one cent under the limit still goes through."""
        result = checking_account.transfer(4999.99)
        assert result["success"] is True
        assert checking_account.daily_transfer_total == 4999.99

    def test_at_daily_limit(self, checking_account):
        """BV4: the limit itself is allowed, the rule is 'exceeds'."""
        result = checking_account.transfer(5000.00)
        assert result["success"] is True
        assert checking_account.daily_transfer_total == 5000.00

    def test_just_above_daily_limit(self, checking_account):
        """BV5: one cent over the limit is refused."""
        result = checking_account.transfer(5000.01)
        assert result["success"] is False
        assert result["error"] == "Exceeds daily limit"

    def test_far_above_daily_limit(self, checking_account):
        """BV6: well past the limit fails for the same reason, not another."""
        result = checking_account.transfer(10000.00)
        assert result["success"] is False
        assert result["error"] == "Exceeds daily limit"


class TestSavingsTransferLimitBoundary:
    """Boundary 2: transfer amount against the $2,000 Savings daily limit."""

    def test_below_minimum_transfer(self):
        """BV7: $0.00 on a Savings account is below the minimum."""
        account = BankAccount("Savings", 5000.0)
        result = account.transfer(0.00)
        assert result["success"] is False
        assert result["error"] == "Amount must be positive"

    def test_at_minimum_transfer(self):
        """BV8: $0.01 is accepted, the minimum does not depend on the type."""
        account = BankAccount("Savings", 5000.0)
        assert account.transfer(0.01)["success"] is True

    def test_just_below_daily_limit(self):
        """BV9: $1,999.99 on a Savings account is accepted."""
        account = BankAccount("Savings", 5000.0)
        assert account.transfer(1999.99)["success"] is True

    def test_at_daily_limit(self):
        """BV10: exactly $2,000.00 is accepted."""
        account = BankAccount("Savings", 5000.0)
        result = account.transfer(2000.00)
        assert result["success"] is True
        assert account.daily_transfer_total == 2000.00

    def test_just_above_daily_limit(self):
        """BV11: $2,000.01 is refused even though the balance covers it."""
        account = BankAccount("Savings", 5000.0)
        result = account.transfer(2000.01)
        assert result["success"] is False
        assert result["error"] == "Exceeds daily limit"


class TestSavingsMinimumBalanceBoundary:
    """Boundary 3: resulting balance against the $100 Savings minimum."""

    def test_leaves_one_cent_above_minimum(self):
        """BV12: ending at $100.01 keeps the account Active."""
        account = BankAccount("Savings", 200.0)
        account.transfer(99.99)
        assert account.balance == 100.01
        assert account.state == "Active"

    def test_leaves_exactly_the_minimum(self):
        """BV13: ending exactly at $100.00 is still Active, the rule is 'below'."""
        account = BankAccount("Savings", 200.0)
        account.transfer(100.00)
        assert account.balance == 100.00
        assert account.state == "Active"

    def test_leaves_one_cent_below_minimum(self):
        """BV14: ending at $99.99 suspends the account."""
        account = BankAccount("Savings", 200.0)
        result = account.transfer(100.01)
        assert account.balance == 99.99
        assert account.state == "Suspended"
        assert result["warning"] == "Balance below minimum"

    def test_leaves_the_account_empty(self):
        """BV15: draining the account to $0.00 suspends it, it does not fail."""
        account = BankAccount("Savings", 200.0)
        result = account.transfer(200.00)
        assert result["success"] is True
        assert account.balance == 0.00
        assert account.state == "Suspended"


class TestPremiumMinimumBalanceBoundary:
    """Boundary 4: resulting balance against the $10,000 Premium minimum."""

    def test_leaves_one_cent_above_minimum(self):
        """BV16: $10,000.01 keeps a Premium account Active."""
        account = BankAccount("Premium", 12000.0)
        account.transfer(1999.99)
        assert account.balance == 10000.01
        assert account.state == "Active"

    def test_leaves_exactly_the_minimum(self):
        """BV17: $10,000.00 exactly keeps Premium Active."""
        account = BankAccount("Premium", 12000.0)
        account.transfer(2000.00)
        assert account.balance == 10000.00
        assert account.state == "Active"

    def test_leaves_one_cent_below_minimum(self):
        """BV18: $9,999.99 suspends a Premium account."""
        account = BankAccount("Premium", 12000.0)
        account.transfer(2000.01)
        assert account.balance == 9999.99
        assert account.state == "Suspended"

    def test_leaves_the_balance_far_below_minimum(self):
        """BV19: a Premium account well under its minimum is still only Suspended."""
        account = BankAccount("Premium", 12000.0)
        account.transfer(11000.00)
        assert account.balance == 1000.00
        assert account.state == "Suspended"


class TestCumulativeDailyLimitBoundary:
    """Boundary 5: the daily limit applies to the running total, not one transfer."""

    def test_two_transfers_just_below_the_limit(self, checking_account):
        """BV20: $3,000 + $1,999.99 stays one cent under the limit."""
        checking_account.transfer(3000.00)
        result = checking_account.transfer(1999.99)
        assert result["success"] is True
        assert checking_account.remaining_daily_limit() == 0.01

    def test_two_transfers_reaching_the_limit_exactly(self, checking_account):
        """BV21: $3,000 + $2,000 lands on the limit and is accepted."""
        checking_account.transfer(3000.00)
        result = checking_account.transfer(2000.00)
        assert result["success"] is True
        assert checking_account.remaining_daily_limit() == 0.00

    def test_second_transfer_crossing_the_limit(self, checking_account):
        """BV22: $3,000 + $2,000.01 crosses the limit and is refused."""
        checking_account.transfer(3000.00)
        result = checking_account.transfer(2000.01)
        assert result["success"] is False
        assert result["error"] == "Exceeds daily limit"

    def test_limit_resets_at_midnight(self, checking_account):
        """BV23: after the reset the full limit is available again."""
        checking_account.transfer(5000.00)
        checking_account.reset_daily_limit()
        assert checking_account.remaining_daily_limit() == 5000.00
        assert checking_account.transfer(1.00)["success"] is True
