"""Boundary Value Analysis tests (design IDs BV1-BV31).

Each boundary from section 2 of design/test-design-document.md is exercised below, on and above
its edge.
"""

from datetime import date

import pytest

from src.banking_system import (
    ERR_AMOUNT_POSITIVE,
    ERR_DAILY_LIMIT,
    ERR_INSUFFICIENT,
    WARN_BELOW_MINIMUM,
)


class TestCheckingDailyLimitBoundary:
    """Boundary: transfer amount against the $5,000 Checking daily limit."""

    @pytest.mark.parametrize(
        "amount,expected_error",
        [(0.00, ERR_AMOUNT_POSITIVE), (5000.01, ERR_DAILY_LIMIT), (10000.00, ERR_DAILY_LIMIT)],
        ids=["BV1-zero", "BV5-one-cent-over", "BV6-far-over"],
    )
    def test_amounts_outside_the_limit_are_rejected(self, funded_checking_account, amount, expected_error):
        """BV1, BV5, BV6: below the minimum transfer and above the daily limit both fail."""
        result = funded_checking_account.transfer(amount)
        assert result["success"] is False
        assert result["error"] == expected_error

    @pytest.mark.parametrize(
        "amount", [0.01, 4999.99, 5000.00], ids=["BV2-minimum", "BV3-just-below-limit", "BV4-at-limit"]
    )
    def test_amounts_inside_the_limit_succeed(self, funded_checking_account, amount):
        """BV2, BV3, BV4: the smallest valid amount and the limit itself are accepted."""
        result = funded_checking_account.transfer(amount)
        assert result["success"] is True
        assert funded_checking_account.daily_transfer_total == amount

    def test_transfer_at_minimum_valid_amount_debits_one_cent(self, funded_checking_account):
        """BV2: $0.01 must debit exactly one cent, with no floating point drift."""
        funded_checking_account.transfer(0.01)
        assert funded_checking_account.balance == 19999.99


class TestSavingsDailyLimitBoundary:
    """Boundary: transfer amount against the $2,000 Savings daily limit."""

    @pytest.mark.parametrize(
        "amount,expected_success",
        [(0.01, True), (1999.99, True), (2000.00, True), (2000.01, False)],
        ids=["BV7-minimum", "BV8-just-below-limit", "BV9-at-limit", "BV10-one-cent-over"],
    )
    def test_savings_limit_edges(self, account_factory, amount, expected_success):
        """BV7-BV10: the Savings limit sits at $2,000, one cent lower than a passing $2,000.00."""
        account = account_factory("Savings", 5000.00)
        result = account.transfer(amount)
        assert result["success"] is expected_success
        if not expected_success:
            assert result["error"] == ERR_DAILY_LIMIT


class TestCumulativeDailyLimitBoundary:
    """Boundary: cumulative daily total against the $50,000 Premium limit."""

    @pytest.mark.parametrize(
        "second_amount,expected_success,expected_total",
        [(0.99, True, 49999.99), (1.00, True, 50000.00), (1.01, False, 49999.00)],
        ids=["BV11-just-below", "BV12-at-limit", "BV13-one-cent-over"],
    )
    def test_second_transfer_of_the_day_is_measured_cumulatively(
        self, premium_account, second_amount, expected_success, expected_total
    ):
        """BV11-BV13: the limit applies to the running daily total, not to a single transfer."""
        premium_account.transfer(49999.00)
        result = premium_account.transfer(second_amount)
        assert result["success"] is expected_success
        assert premium_account.daily_transfer_total == expected_total

    def test_limit_resets_at_midnight(self, premium_account):
        """BV14: the same amount that was rejected before midnight is accepted after the reset."""
        premium_account.transfer(49999.00)
        assert premium_account.transfer(1.01)["success"] is False
        premium_account.reset_daily_limit()
        result = premium_account.transfer(1.01)
        assert result["success"] is True
        assert premium_account.daily_transfer_total == 1.01


class TestMinimumBalanceBoundary:
    """Boundary: resulting balance against the $100 Savings minimum."""

    @pytest.mark.parametrize(
        "amount,expected_balance,expected_state",
        [
            (50.00, 150.00, "Active"),
            (99.99, 100.01, "Active"),
            (100.00, 100.00, "Active"),
            (100.01, 99.99, "Suspended"),
            (200.00, 0.00, "Suspended"),
        ],
        ids=["BV15-above", "BV16-one-cent-above", "BV17-at-minimum", "BV18-one-cent-below", "BV19-empty"],
    )
    def test_state_after_transfer_follows_the_minimum_balance(
        self, account_factory, amount, expected_balance, expected_state
    ):
        """BV15-BV19: suspension starts one cent under the minimum, not at it."""
        account = account_factory("Savings", 200.00)
        result = account.transfer(amount)
        assert result["success"] is True
        assert account.balance == expected_balance
        assert account.state == expected_state

    def test_dropping_below_minimum_raises_a_warning(self, account_factory):
        """BV18: crossing the boundary must warn the customer, not fail silently."""
        account = account_factory("Savings", 200.00)
        result = account.transfer(100.01)
        assert WARN_BELOW_MINIMUM in result["warnings"]
        assert WARN_BELOW_MINIMUM in account.notifications


class TestFeeWaiverBoundary:
    """Boundary: balance against the $1,000 Savings fee waiver threshold."""

    @pytest.mark.parametrize(
        "balance,expected_waived,expected_balance",
        [
            (999.99, False, 994.99),
            (1000.00, False, 995.00),
            (1000.01, True, 1000.01),
            (5000.00, True, 5000.00),
        ],
        ids=["BV20-just-below", "BV21-at-threshold", "BV22-one-cent-above", "BV23-far-above"],
    )
    def test_fee_waiver_is_strictly_above_the_threshold(
        self, account_factory, balance, expected_waived, expected_balance
    ):
        """BV20-BV23: 'waived if balance > $1,000' means $1,000.00 exactly is still charged."""
        account = account_factory("Savings", balance)
        result = account.apply_monthly_fee()
        assert result["success"] is True
        assert result["waived"] is expected_waived
        assert account.balance == expected_balance


class TestFeeAffordabilityBoundary:
    """Boundary: balance against the $10 Checking monthly fee."""

    @pytest.mark.parametrize(
        "balance,expected_balance",
        [(10.01, 0.01), (10.00, 0.00)],
        ids=["BV24-one-cent-spare", "BV25-exactly-affordable"],
    )
    def test_affordable_fee_is_charged(self, account_factory, balance, expected_balance):
        """BV24, BV25: a fee equal to the balance is still payable."""
        account = account_factory("Checking", balance)
        result = account.apply_monthly_fee()
        assert result["success"] is True
        assert account.balance == expected_balance
        assert account.state == "Active"

    @pytest.mark.parametrize("balance", [9.99, 0.00], ids=["BV26-one-cent-short", "BV27-empty"])
    def test_unaffordable_fee_suspends_the_account(self, account_factory, balance):
        """BV26, BV27: one cent short of the fee suspends the account and charges nothing."""
        account = account_factory("Checking", balance)
        result = account.apply_monthly_fee()
        assert result["success"] is False
        assert result["error"] == ERR_INSUFFICIENT
        assert account.balance == balance
        assert account.state == "Suspended"


class TestHistoryRangeBoundary:
    """Boundary: inclusive ends of the transaction history date range."""

    @pytest.mark.parametrize(
        "start,end,expected_count",
        [
            (date(2026, 2, 1), date(2026, 3, 1), 1),
            (date(2026, 3, 2), date(2026, 3, 31), 2),
            (date(2026, 3, 1), date(2026, 3, 31), 3),
            (date(2026, 3, 15), date(2026, 3, 15), 1),
        ],
        ids=["BV28-ends-on-first", "BV29-starts-one-day-late", "BV30-full-range", "BV31-single-day"],
    )
    def test_range_ends_are_inclusive(self, account_with_history, start, end, expected_count):
        """BV28-BV31: both ends of the range belong to the range."""
        result = account_with_history.get_transactions(start, end)
        assert result["success"] is True
        assert result["count"] == expected_count
