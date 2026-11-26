from banking_system import BankAccount


class TestBoundary1TransferAmountSavings:
    """Boundary 1: Transfer Amount - Savings Account ($2,000 daily limit)."""

    def test_bva1_below_minimum(self):
        """BVA1: $0 transfer should fail."""
        account = BankAccount("Savings", 1500)
        result = account.transfer(0)
        assert result["success"] is False
        assert "must be positive" in result["error"]

    def test_bva2_minimum_valid(self):
        """BVA2: $0.01 transfer should succeed."""
        account = BankAccount("Savings", 1500)
        result = account.transfer(0.01)
        assert result["success"] is True

    def test_bva4_at_limit(self):
        """BVA4: Transfer exactly at the $2,000 Savings limit should succeed."""
        account = BankAccount("Savings", 3000)
        result = account.transfer(2000)
        assert result["success"] is True

    def test_bva5_just_above_limit(self):
        """BVA5: Transfer of $2,000.01 should fail (exceeds daily limit)."""
        account = BankAccount("Savings", 3000)
        result = account.transfer(2000.01)
        assert result["success"] is False
        assert "daily limit" in result["error"]


class TestBoundary2TransferAmountChecking:
    """Boundary 2: Transfer Amount - Checking Account ($5,000 daily limit)."""

    def test_bva7_below_minimum(self, checking_account):
        """BVA7: $0 transfer should fail."""
        result = checking_account.transfer(0)
        assert result["success"] is False
        assert "must be positive" in result["error"]

    def test_bva8_minimum_valid(self, checking_account):
        """BVA8: $0.01 transfer should succeed."""
        result = checking_account.transfer(0.01)
        assert result["success"] is True

    def test_bva10_at_limit(self):
        """BVA10: Transfer exactly at the $5,000 Checking limit should succeed."""
        account = BankAccount("Checking", 10000)
        result = account.transfer(5000)
        assert result["success"] is True

    def test_bva11_just_above_limit(self):
        """BVA11: Transfer of $5,000.01 should fail (exceeds daily limit)."""
        account = BankAccount("Checking", 10000)
        result = account.transfer(5000.01)
        assert result["success"] is False
        assert "daily limit" in result["error"]


class TestBoundary3TransferAmountPremium:
    """Boundary 3: Transfer Amount - Premium Account ($50,000 daily limit)."""

    def test_bva13_minimum_valid(self, premium_account):
        """BVA13: $0.01 transfer should succeed."""
        result = premium_account.transfer(0.01)
        assert result["success"] is True

    def test_bva15_at_limit(self):
        """BVA15: Transfer exactly at the $50,000 Premium limit should succeed."""
        account = BankAccount("Premium", 60000)
        result = account.transfer(50000)
        assert result["success"] is True

    def test_bva16_just_above_limit(self):
        """BVA16: Transfer of $50,000.01 should fail (exceeds daily limit)."""
        account = BankAccount("Premium", 60000)
        result = account.transfer(50000.01)
        assert result["success"] is False
        assert "daily limit" in result["error"]


class TestBoundary4BalanceVsMinimumSavings:
    """Boundary 4: Account Balance vs Minimum - Savings Account ($100 minimum)."""

    def test_bva17_just_below_minimum_suspends(self):
        """BVA17: Balance dropping to $99.99 should suspend the account."""
        account = BankAccount("Savings", 200)
        account.transfer(100.01)  # 200 - 100.01 = 99.99
        assert account.state == "Suspended"

    def test_bva18_at_minimum_stays_active(self):
        """BVA18: Balance exactly at $100 minimum should remain Active."""
        account = BankAccount("Savings", 200)
        account.transfer(100)  # 200 - 100 = 100
        assert account.state == "Active"

    def test_bva19_just_above_minimum_stays_active(self):
        """BVA19: Balance at $100.01 should remain Active."""
        account = BankAccount("Savings", 200)
        account.transfer(99.99)  # 200 - 99.99 = 100.01
        assert account.state == "Active"


class TestBoundary5FeeWaiverSavings:
    """Boundary 5: Account Balance vs Fee Waiver Threshold - Savings Account ($1,000)."""

    def test_bva23_below_waiver_fee_charged(self):
        """BVA23: Balance just below $1,000 should incur the $5 monthly fee."""
        account = BankAccount("Savings", 999.99)
        result = account.apply_monthly_fee()
        assert result["fee_charged"] == 5

    def test_bva24_at_waiver_threshold_fee_still_charged(self):
        """
        BVA24: Balance exactly at $1,000. The business rule says the fee is
        waived only when balance is STRICTLY greater than the threshold
        ("waived if balance > $1,000"), so at exactly $1,000 the fee is
        still charged. This boundary is where BVA exposes the classic
        '>' vs '>=' ambiguity - see analysis-report.md for discussion.
        """
        account = BankAccount("Savings", 1000)
        result = account.apply_monthly_fee()
        assert result["fee_charged"] == 5

    def test_bva25_just_above_waiver_fee_waived(self):
        """BVA25: Balance at $1,000.01 should waive the fee."""
        account = BankAccount("Savings", 1000.01)
        result = account.apply_monthly_fee()
        assert result["fee_charged"] == 0


class TestBoundary6FeeWaiverChecking:
    """Boundary 6: Account Balance vs Fee Waiver Threshold - Checking Account ($5,000)."""

    def test_bva27_below_waiver_fee_charged(self):
        """BVA27: Balance just below $5,000 should incur the $10 monthly fee."""
        account = BankAccount("Checking", 4999.99)
        result = account.apply_monthly_fee()
        assert result["fee_charged"] == 10

    def test_bva28_at_waiver_threshold_fee_still_charged(self):
        """
        BVA28: Balance exactly at $5,000. Same '>' vs '>=' boundary issue
        as BVA24: the fee is still charged at exactly the threshold.
        """
        account = BankAccount("Checking", 5000)
        result = account.apply_monthly_fee()
        assert result["fee_charged"] == 10

    def test_bva29_just_above_waiver_fee_waived(self):
        """BVA29: Balance at $5,000.01 should waive the fee."""
        account = BankAccount("Checking", 5000.01)
        result = account.apply_monthly_fee()
        assert result["fee_charged"] == 0


class TestBoundary7BalanceVsMinimumPremium:
    """Boundary 7: Account Balance vs Minimum - Premium Account ($10,000 minimum)."""

    def test_bva31_just_below_minimum_suspends(self):
        """BVA31: Balance dropping to $9,999.99 should suspend the account."""
        account = BankAccount("Premium", 20000)
        account.transfer(10000.01)  # 20000 - 10000.01 = 9999.99
        assert account.state == "Suspended"

    def test_bva32_at_minimum_stays_active(self):
        """BVA32: Balance exactly at $10,000 minimum should remain Active."""
        account = BankAccount("Premium", 20000)
        account.transfer(10000)  # 20000 - 10000 = 10000
        assert account.state == "Active"

    def test_bva33_just_above_minimum_stays_active(self):
        """BVA33: Balance at $10,000.01 should remain Active."""
        account = BankAccount("Premium", 20000)
        account.transfer(9999.99)  # 20000 - 9999.99 = 10000.01
        assert account.state == "Active"