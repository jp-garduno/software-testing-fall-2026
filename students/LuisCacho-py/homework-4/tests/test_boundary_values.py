"""
Boundary Value Analysis Tests — SecureBank Online Banking System.

Tests based on the boundaries identified in:
  design/test-design-document.md — Section 1.2

Each test references its boundary ID (BV-xx) and covers the values
just below, at, and just above each boundary.

Technique: Boundary Value Analysis (BVA)
  - Tests the minimum valid value, values just outside boundaries,
    values at each limit, and values just past each limit.
"""

import pytest

from src.banking_system import AccountState, AccountType, BankAccount


class TestTransferAmountBoundaryChecking:
    """BVA — Transfer Amount boundaries for Checking Account ($5,000 daily limit)."""

    def test_bv01_below_minimum_zero_rejected(self, high_balance_checking):
        """BV-01: Transfer $0.00 → Error (below minimum of $0.01)."""
        result = high_balance_checking.transfer(0.00)
        assert result["success"] is False
        assert "positive" in result["error"].lower()

    def test_bv02_minimum_valid_amount_succeeds(self, high_balance_checking):
        """BV-02: Transfer exactly $0.01 (minimum valid) → Transfer succeeds."""
        result = high_balance_checking.transfer(0.01)
        assert result["success"] is True
        assert high_balance_checking.balance == pytest.approx(9_999.99, abs=0.01)

    def test_bv03_just_below_daily_limit_succeeds(self, high_balance_checking):
        """BV-03: Transfer $4,999.99 (just below $5,000 limit) → Transfer succeeds."""
        result = high_balance_checking.transfer(4_999.99)
        assert result["success"] is True

    def test_bv04_at_daily_limit_succeeds(self, high_balance_checking):
        """BV-04: Transfer exactly $5,000.00 (at limit) → Transfer succeeds."""
        result = high_balance_checking.transfer(5_000.00)
        assert result["success"] is True
        assert high_balance_checking.daily_transfer_total == pytest.approx(5_000.00, abs=0.01)

    def test_bv05_just_above_daily_limit_rejected(self, high_balance_checking):
        """BV-05: Transfer $5,000.01 (just above limit) → Error: Exceeds daily limit."""
        result = high_balance_checking.transfer(5_000.01)
        assert result["success"] is False
        assert "limit" in result["error"].lower()

    def test_bv06_far_above_daily_limit_rejected(self, high_balance_checking):
        """BV-06: Transfer $10,000.00 (far above $5,000 limit) → Error: Exceeds daily limit."""
        result = high_balance_checking.transfer(10_000.00)
        assert result["success"] is False
        assert "limit" in result["error"].lower()


class TestTransferAmountBoundarySavings:
    """BVA — Transfer Amount boundaries for Savings Account ($2,000 daily limit)."""

    def test_bv07_at_savings_daily_limit_succeeds(self, high_balance_savings):
        """BV-07: Transfer exactly $2,000.00 (Savings limit) → Transfer succeeds."""
        result = high_balance_savings.transfer(2_000.00)
        assert result["success"] is True
        assert high_balance_savings.daily_transfer_total == pytest.approx(2_000.00, abs=0.01)

    def test_bv08_just_above_savings_limit_rejected(self, high_balance_savings):
        """BV-08: Transfer $2,000.01 (just above Savings limit) → Error: Exceeds daily limit."""
        result = high_balance_savings.transfer(2_000.01)
        assert result["success"] is False
        assert "limit" in result["error"].lower()


class TestMinimumBalanceBoundarySavings:
    """BVA — Account Balance vs. Minimum Balance boundary (Savings: $100 minimum)."""

    def test_bv09_balance_just_above_minimum_active(self):
        """BV-09: Balance $100.01 (just above $100 minimum) → State remains Active."""
        account = BankAccount(AccountType.SAVINGS, 100.01)
        assert account.state == AccountState.ACTIVE

    def test_bv10_balance_at_minimum_active(self):
        """BV-10: Balance exactly $100.00 (at minimum) → State is Active."""
        account = BankAccount(AccountType.SAVINGS, 100.00)
        assert account.state == AccountState.ACTIVE

    def test_bv11_balance_just_below_minimum_suspended(self):
        """BV-11: Balance $99.99 (just below $100 minimum) → State is Suspended."""
        account = BankAccount(AccountType.SAVINGS, 99.99)
        assert account.state == AccountState.SUSPENDED

    def test_bv12_balance_at_zero_savings_suspended(self):
        """BV-12: Balance $0.00 (Savings needs $100 min) → State is Suspended."""
        account = BankAccount(AccountType.SAVINGS, 0.00)
        assert account.state == AccountState.SUSPENDED


class TestFeeWaiverBoundaries:
    """BVA — Monthly Fee Waiver threshold boundaries."""

    def test_bv13_savings_balance_above_waiver_threshold_fee_waived(self):
        """BV-13: Savings balance $1,000.01 > $1,000 waiver → Fee is waived."""
        account = BankAccount(AccountType.SAVINGS, 1_000.01)
        result = account.process_monthly_fee()
        assert result["waived"] is True
        assert result["fee_charged"] == 0

    def test_bv14_savings_balance_at_waiver_threshold_fee_not_waived(self):
        """BV-14: Savings balance exactly $1,000.00 (not > threshold) → Fee IS charged."""
        account = BankAccount(AccountType.SAVINGS, 1_000.00)
        result = account.process_monthly_fee()
        # Balance is NOT > 1000, so fee applies
        assert result["fee_charged"] == 5.00

    def test_bv15_savings_balance_just_below_waiver_threshold_fee_charged(self):
        """BV-15: Savings balance $999.99 (just below $1,000) → Monthly fee charged."""
        account = BankAccount(AccountType.SAVINGS, 999.99)
        result = account.process_monthly_fee()
        assert result["fee_charged"] == 5.00


class TestDailyLimitCumulativeBoundary:
    """BVA — Cumulative daily transfers respecting the daily reset boundary."""

    def test_bv16_cumulative_transfers_at_limit_last_accepted(self, high_balance_checking):
        """BV-16: Two transfers totalling exactly $5,000 → Both succeed."""
        result1 = high_balance_checking.transfer(3_000.00)
        result2 = high_balance_checking.transfer(2_000.00)
        assert result1["success"] is True
        assert result2["success"] is True
        assert high_balance_checking.daily_transfer_total == pytest.approx(5_000.00, abs=0.01)

    def test_bv17_cumulative_transfers_exceed_limit_second_rejected(self, high_balance_checking):
        """BV-17: Two transfers that together exceed $5,000 → Second is rejected."""
        high_balance_checking.transfer(4_999.00)
        result = high_balance_checking.transfer(2.00)  # Would total 5001
        assert result["success"] is False
        assert "limit" in result["error"].lower()
