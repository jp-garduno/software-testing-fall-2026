"""Decision table tests (design section 3).

One test per rule of the four decision tables: transfer validation (DT1), monthly fee processing
(DT2), bill payment validation (DT3) and account creation (DT4).
"""

from datetime import date, timedelta

import pytest

from src.banking_system import (
    ERR_AMOUNT_POSITIVE,
    ERR_CLOSED,
    ERR_DAILY_LIMIT,
    ERR_FROZEN,
    ERR_INACTIVE_PAYEE,
    ERR_INSUFFICIENT,
    ERR_INVALID_AMOUNT,
    ERR_INVALID_TYPE,
    ERR_OPENING_DEPOSIT,
    ERR_PAST_DATE,
    ERR_UNKNOWN_PAYEE,
)


class TestTransferValidationTable:
    """DT1: state, amount validity, daily limit and funds, in that precedence order."""

    def test_rule_1_active_account_with_valid_transfer(self, account_factory):
        """DT1 R1: Active + valid amount + within limit + funded -> transfer succeeds."""
        account = account_factory("Checking", 1000.00)
        result = account.transfer(200.00)
        assert result["success"] is True
        assert account.balance == 800.00

    def test_rule_2_suspended_account_can_still_transfer(self, account_factory):
        """DT1 R2: Suspended blocks nothing; it only carries a warning."""
        account = account_factory("Savings", 90.00, state="Suspended")
        result = account.transfer(10.00)
        assert result["success"] is True
        assert account.balance == 80.00

    def test_rule_3_frozen_account_is_blocked(self, account_factory):
        """DT1 R3: Frozen is view-only."""
        account = account_factory("Checking", 1000.00, state="Frozen")
        result = account.transfer(100.00)
        assert result["success"] is False
        assert result["error"] == ERR_FROZEN

    def test_rule_4_closed_account_is_blocked(self, account_factory):
        """DT1 R4: Closed reports its own error, distinct from Frozen."""
        account = account_factory("Checking", 1000.00, state="Closed")
        result = account.transfer(100.00)
        assert result["success"] is False
        assert result["error"] == ERR_CLOSED

    def test_rule_5_non_positive_amount(self, account_factory):
        """DT1 R5: Active + non-positive amount -> amount error."""
        account = account_factory("Checking", 1000.00)
        result = account.transfer(-5.00)
        assert result["error"] == ERR_AMOUNT_POSITIVE

    def test_rule_6_non_numeric_amount(self, account_factory):
        """DT1 R6: Active + non-numeric amount -> numeric error."""
        account = account_factory("Checking", 1000.00)
        result = account.transfer(None)
        assert result["error"] == ERR_INVALID_AMOUNT

    def test_rule_7_amount_over_daily_limit(self, account_factory):
        """DT1 R7: the limit is checked before the balance."""
        account = account_factory("Checking", 20000.00)
        result = account.transfer(6000.00)
        assert result["error"] == ERR_DAILY_LIMIT

    def test_rule_8_amount_over_balance(self, account_factory):
        """DT1 R8: within the limit but unfunded -> insufficient funds."""
        account = account_factory("Checking", 1000.00)
        result = account.transfer(1200.00)
        assert result["error"] == ERR_INSUFFICIENT

    def test_rule_9_state_check_wins_over_invalid_amount(self, account_factory):
        """DT1 R9: a Frozen account reports the state error, never the amount error."""
        account = account_factory("Checking", 1000.00, state="Frozen")
        result = account.transfer(-1.00)
        assert result["error"] == ERR_FROZEN

    def test_rule_10_suspended_account_still_needs_funds(self, account_factory):
        """DT1 R10: Suspended follows exactly the same funds rule as Active."""
        account = account_factory("Savings", 50.00, state="Suspended")
        result = account.transfer(60.00)
        assert result["error"] == ERR_INSUFFICIENT
        assert account.balance == 50.00


class TestMonthlyFeeTable:
    """DT2: account type, waiver threshold and fee affordability."""

    def test_rule_1_premium_never_pays_a_fee(self, premium_account):
        """DT2 R1: the Premium fee is $0 regardless of balance."""
        result = premium_account.apply_monthly_fee()
        assert result["waived"] is True
        assert premium_account.balance == 100000.00

    def test_rule_2_savings_above_threshold_is_waived(self, account_factory):
        """DT2 R2: Savings over $1,000 pays nothing."""
        account = account_factory("Savings", 2500.00)
        result = account.apply_monthly_fee()
        assert result["waived"] is True
        assert account.balance == 2500.00

    def test_rule_3_savings_below_threshold_is_charged(self, account_factory):
        """DT2 R3: Savings under $1,000 pays the $5 fee."""
        account = account_factory("Savings", 800.00)
        result = account.apply_monthly_fee()
        assert result["charged"] == 5.00
        assert account.balance == 795.00

    def test_rule_4_checking_above_threshold_is_waived(self, account_factory):
        """DT2 R4: Checking over $5,000 pays nothing."""
        account = account_factory("Checking", 6000.00)
        result = account.apply_monthly_fee()
        assert result["waived"] is True
        assert account.balance == 6000.00

    def test_rule_5_checking_below_threshold_is_charged(self, account_factory):
        """DT2 R5: Checking under $5,000 pays the $10 fee."""
        account = account_factory("Checking", 4000.00)
        result = account.apply_monthly_fee()
        assert result["charged"] == 10.00
        assert account.balance == 3990.00

    def test_rule_6_unaffordable_fee_suspends_the_account(self, account_factory):
        """DT2 R6: a fee the balance cannot cover suspends the account and charges nothing."""
        account = account_factory("Savings", 3.00, state="Suspended")
        result = account.apply_monthly_fee()
        assert result["success"] is False
        assert result["error"] == ERR_INSUFFICIENT
        assert account.balance == 3.00
        assert account.state == "Suspended"

    def test_fee_that_crosses_the_minimum_also_suspends(self, account_factory):
        """DT2 R3 + A4: a charged fee that lands under the minimum suspends the account too."""
        account = account_factory("Savings", 102.00)
        result = account.apply_monthly_fee()
        assert result["charged"] == 5.00
        assert account.balance == 97.00
        assert account.state == "Suspended"


class TestBillPaymentTable:
    """DT3: state, payee, amount, date and funds."""

    def test_rule_1_valid_immediate_payment(self, account_with_payees):
        """DT3 R1: every condition satisfied -> paid immediately."""
        result = account_with_payees.pay_bill("CFE", 250.00)
        assert result["success"] is True
        assert result["scheduled"] is False
        assert account_with_payees.balance == 750.00

    def test_rule_2_payment_above_balance(self, account_with_payees):
        """DT3 R2: a valid payee cannot be paid without funds."""
        result = account_with_payees.pay_bill("CFE", 5000.00)
        assert result["error"] == ERR_INSUFFICIENT

    def test_rule_3_unknown_payee(self, account_with_payees):
        """DT3 R3: unregistered payee."""
        assert account_with_payees.pay_bill("NOPE", 10.00)["error"] == ERR_UNKNOWN_PAYEE

    def test_rule_4_inactive_payee(self, account_with_payees):
        """DT3 R4: registered but deactivated payee."""
        assert account_with_payees.pay_bill("OLD-GYM", 10.00)["error"] == ERR_INACTIVE_PAYEE

    def test_rule_5_non_positive_amount(self, account_with_payees):
        """DT3 R5: the payee is checked before the amount."""
        assert account_with_payees.pay_bill("CFE", 0.00)["error"] == ERR_AMOUNT_POSITIVE

    def test_rule_6_past_scheduled_date(self, account_with_payees):
        """DT3 R6: a payment cannot be scheduled into the past."""
        today = date(2026, 3, 10)
        result = account_with_payees.pay_bill("CFE", 10.00, scheduled_date=today - timedelta(days=2), today=today)
        assert result["error"] == ERR_PAST_DATE

    def test_rule_7_frozen_account_cannot_pay_bills(self, account_with_payees):
        """DT3 R7: the state check precedes every payment condition."""
        account_with_payees.freeze()
        assert account_with_payees.pay_bill("NOPE", -1.00)["error"] == ERR_FROZEN

    def test_rule_8_future_payment_is_scheduled(self, account_with_payees):
        """DT3 R8: a future date schedules the payment without debiting the balance."""
        today = date(2026, 3, 10)
        result = account_with_payees.pay_bill("CFE", 300.00, scheduled_date=today + timedelta(days=5), today=today)
        assert result["scheduled"] is True
        assert account_with_payees.balance == 1000.00


class TestAccountCreationTable:
    """DT4: supported type and opening deposit."""

    def test_rule_1_valid_creation(self, opener):
        """DT4 R1: supported type with a deposit above the minimum."""
        result = opener("Savings", 250.00)
        assert result["success"] is True
        assert result["balance"] == 250.00

    def test_rule_2_deposit_below_minimum(self, opener):
        """DT4 R2: a deposit under the type minimum is rejected."""
        assert opener("Premium", 500.00)["error"] == ERR_OPENING_DEPOSIT

    def test_rule_3_negative_deposit(self, opener):
        """DT4 R3: a negative deposit is rejected before the minimum is considered."""
        assert opener("Checking", -1.00)["error"] == ERR_AMOUNT_POSITIVE

    @pytest.mark.parametrize("account_type", ["Crypto", "savings", ""], ids=["unknown", "wrong-case", "empty"])
    def test_rule_4_unsupported_type(self, opener, account_type):
        """DT4 R4: the type check precedes every deposit condition."""
        assert opener(account_type, 50000.00)["error"] == ERR_INVALID_TYPE
