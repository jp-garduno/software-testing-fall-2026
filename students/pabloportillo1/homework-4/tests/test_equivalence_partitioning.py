"""Equivalence Partitioning tests (design IDs EP1-EP27).

Each test covers one partition from section 1 of design/test-design-document.md using that
partition's representative value.
"""

from datetime import date, timedelta

import pytest

from src.banking_system import (
    ERR_AMOUNT_POSITIVE,
    ERR_AMOUNT_PRECISION,
    ERR_DAILY_LIMIT,
    ERR_DATE_ORDER,
    ERR_DATE_TYPE,
    ERR_INACTIVE_PAYEE,
    ERR_INSUFFICIENT,
    ERR_INVALID_AMOUNT,
    ERR_INVALID_TYPE,
    ERR_OPENING_DEPOSIT,
    ERR_PAST_DATE,
    ERR_UNKNOWN_PAYEE,
    BankAccount,
)


class TestTransferAmountPartitions:
    """Input: transfer amount on a Checking account with $1,000 and a $5,000 daily limit."""

    def test_valid_amount_within_funds_and_limit_succeeds(self, checking_account):
        """EP1: a $500 transfer is inside every rule and must succeed."""
        result = checking_account.transfer(500.00)
        assert result["success"] is True
        assert checking_account.balance == 500.00

    def test_zero_amount_is_rejected(self, checking_account):
        """EP2: $0.00 is not a positive amount."""
        result = checking_account.transfer(0.00)
        assert result["success"] is False
        assert result["error"] == ERR_AMOUNT_POSITIVE

    def test_negative_amount_is_rejected(self, checking_account):
        """EP3: -$100 is not a positive amount."""
        result = checking_account.transfer(-100.00)
        assert result["success"] is False
        assert result["error"] == ERR_AMOUNT_POSITIVE

    def test_amount_above_daily_limit_is_rejected(self, checking_account):
        """EP4: $100,000 is far above the $5,000 Checking limit."""
        result = checking_account.transfer(100000.00)
        assert result["success"] is False
        assert result["error"] == ERR_DAILY_LIMIT

    def test_amount_above_balance_but_within_limit_is_rejected(self, checking_account):
        """EP5: $1,500 fits the daily limit but not the $1,000 balance."""
        result = checking_account.transfer(1500.00)
        assert result["success"] is False
        assert result["error"] == ERR_INSUFFICIENT

    def test_non_numeric_amount_is_rejected(self, checking_account):
        """EP6: a text amount is not a number."""
        result = checking_account.transfer("five hundred")
        assert result["success"] is False
        assert result["error"] == ERR_INVALID_AMOUNT

    def test_sub_cent_amount_is_rejected(self, checking_account):
        """EP7: $0.001 carries sub-cent precision and must not be rounded silently."""
        result = checking_account.transfer(0.001)
        assert result["success"] is False
        assert result["error"] == ERR_AMOUNT_PRECISION

    def test_rejected_transfer_leaves_balance_untouched(self, checking_account):
        """EP2-EP7: no invalid partition may move money."""
        for amount in (0.00, -100.00, 100000.00, 1500.00, "five hundred", 0.001):
            checking_account.transfer(amount)
        assert checking_account.balance == 1000.00
        assert checking_account.daily_transfer_total == 0.00


class TestAccountTypePartitions:
    """Input: account type at creation."""

    @pytest.mark.parametrize(
        "account_type,expected_limit,expected_minimum,opening_balance",
        [
            ("Savings", 2000.00, 100.00, 500.00),
            ("Checking", 5000.00, 0.00, 500.00),
            ("Premium", 50000.00, 10000.00, 20000.00),
        ],
        ids=["EP8-savings", "EP9-checking", "EP10-premium"],
    )
    def test_supported_account_types_are_created(
        self, opener, account_type, expected_limit, expected_minimum, opening_balance
    ):
        """EP8-EP10: each supported type is created with its own limit and minimum."""
        result = opener(account_type, opening_balance)
        assert result["success"] is True
        assert result["account"].get_daily_limit() == expected_limit
        assert result["account"].get_minimum_balance() == expected_minimum

    def test_unsupported_account_type_is_rejected(self, opener):
        """EP11: a type outside the catalogue cannot be opened."""
        result = opener("Crypto", 500.00)
        assert result["success"] is False
        assert result["error"] == ERR_INVALID_TYPE

    def test_empty_account_type_is_rejected(self, opener):
        """EP12: an empty type name is as invalid as an unknown one."""
        result = opener("", 500.00)
        assert result["success"] is False
        assert result["error"] == ERR_INVALID_TYPE


class TestOpeningBalancePartitions:
    """Input: opening balance, checked against the account-type minimum."""

    def test_opening_deposit_above_minimum_succeeds(self, opener):
        """EP13: $500 clears the $100 Savings minimum."""
        result = opener("Savings", 500.00)
        assert result["success"] is True
        assert result["state"] == "Active"

    def test_opening_deposit_below_minimum_is_rejected(self, opener):
        """EP14: $50 is under the $100 Savings minimum."""
        result = opener("Savings", 50.00)
        assert result["success"] is False
        assert result["error"] == ERR_OPENING_DEPOSIT

    def test_negative_opening_deposit_is_rejected(self, opener):
        """EP15: a negative opening deposit is not a deposit at all."""
        result = opener("Savings", -10.00)
        assert result["success"] is False
        assert result["error"] == ERR_AMOUNT_POSITIVE

    def test_premium_opened_below_its_minimum_is_rejected(self, opener):
        """EP16: $9,000 is under the $10,000 Premium minimum."""
        result = opener("Premium", 9000.00)
        assert result["success"] is False
        assert result["error"] == ERR_OPENING_DEPOSIT


class TestPayeePartitions:
    """Input: payee reference used by bill payment."""

    def test_registered_active_payee_is_paid(self, account_with_payees):
        """EP17: a registered, active payee receives the payment."""
        result = account_with_payees.pay_bill("CFE", 120.00)
        assert result["success"] is True
        assert account_with_payees.balance == 880.00

    def test_unknown_payee_is_rejected(self, account_with_payees):
        """EP18: a payee that was never registered cannot be paid."""
        result = account_with_payees.pay_bill("UNKNOWN-99", 120.00)
        assert result["success"] is False
        assert result["error"] == ERR_UNKNOWN_PAYEE

    def test_deactivated_payee_is_rejected(self, account_with_payees):
        """EP19: a deactivated payee is a distinct partition from an unknown one."""
        result = account_with_payees.pay_bill("OLD-GYM", 120.00)
        assert result["success"] is False
        assert result["error"] == ERR_INACTIVE_PAYEE


class TestScheduledDatePartitions:
    """Input: scheduled date of a bill payment."""

    def test_immediate_payment_debits_now(self, account_with_payees):
        """EP20: without a date the payment is immediate."""
        result = account_with_payees.pay_bill("CFE", 100.00)
        assert result["scheduled"] is False
        assert account_with_payees.balance == 900.00

    def test_future_payment_is_scheduled_without_debit(self, account_with_payees):
        """EP21: a future date schedules the payment and leaves the balance alone."""
        today = date(2026, 3, 1)
        result = account_with_payees.pay_bill("CFE", 100.00, scheduled_date=today + timedelta(days=15), today=today)
        assert result["success"] is True
        assert result["scheduled"] is True
        assert account_with_payees.balance == 1000.00

    def test_past_payment_date_is_rejected(self, account_with_payees):
        """EP22: a date before today cannot be scheduled."""
        today = date(2026, 3, 1)
        result = account_with_payees.pay_bill("CFE", 100.00, scheduled_date=today - timedelta(days=1), today=today)
        assert result["success"] is False
        assert result["error"] == ERR_PAST_DATE


class TestHistoryDateRangePartitions:
    """Input: date range used to filter the transaction history."""

    def test_range_covering_some_entries_filters_history(self, account_with_history):
        """EP23: only the entries inside the range are returned."""
        result = account_with_history.get_transactions(date(2026, 3, 1), date(2026, 3, 20))
        assert result["success"] is True
        assert result["count"] == 2

    def test_missing_range_returns_full_history(self, account_with_history):
        """EP24: no range means the whole statement."""
        result = account_with_history.get_transactions()
        assert result["count"] == 3

    def test_range_without_entries_returns_empty_history(self, account_with_history):
        """EP25: an empty result is a valid outcome, not an error."""
        result = account_with_history.get_transactions(date(2030, 1, 1), date(2030, 1, 31))
        assert result["success"] is True
        assert result["count"] == 0

    def test_inverted_range_is_rejected(self, account_with_history):
        """EP26: the start date cannot be after the end date."""
        result = account_with_history.get_transactions(date(2026, 3, 31), date(2026, 3, 1))
        assert result["success"] is False
        assert result["error"] == ERR_DATE_ORDER

    def test_wrong_bound_type_is_rejected(self, account_with_history):
        """EP27: a string is not a date object."""
        result = account_with_history.get_transactions("2026-03-01", date(2026, 3, 31))
        assert result["success"] is False
        assert result["error"] == ERR_DATE_TYPE


class TestAmountPartitionsAcrossOperations:
    """The amount partitions of section 1.1 applied to every operation that accepts money."""

    def test_deposit_rejects_sub_cent_amount(self, checking_account):
        """EP28: deposit must apply the same precision rule as transfer."""
        result = checking_account.deposit(0.001)
        assert result["error"] == ERR_AMOUNT_PRECISION
        assert checking_account.balance == 1000.00

    def test_deposit_rejects_non_positive_amount(self, checking_account):
        """EP29: a deposit of $0 moves no money."""
        assert checking_account.deposit(0.00)["error"] == ERR_AMOUNT_POSITIVE

    def test_bill_payment_rejects_non_numeric_amount(self, account_with_payees):
        """EP30: bill payment must reject a text amount just like transfer does."""
        assert account_with_payees.pay_bill("CFE", "one hundred")["error"] == ERR_INVALID_AMOUNT

    def test_account_creation_rejects_non_numeric_deposit(self, opener):
        """EP31: the opening deposit is an amount and follows the amount partitions."""
        assert opener("Checking", "one thousand")["error"] == ERR_INVALID_AMOUNT

    def test_infinite_amount_is_rejected(self, checking_account):
        """EP32: infinity is numeric but not a finite amount of money."""
        assert checking_account.transfer(float("inf"))["error"] == ERR_INVALID_AMOUNT

    def test_constructor_rejects_unknown_account_type(self):
        """EP33: the account type partition holds at the constructor, not only at create_account."""
        with pytest.raises(ValueError):
            BankAccount("Crypto", 500.00)

    def test_structured_value_is_not_an_amount(self, checking_account):
        """EP34: a dict is neither a number nor a numeric string."""
        assert checking_account.transfer({"amount": 100})["error"] == ERR_INVALID_AMOUNT

    def test_scientific_notation_below_one_cent_is_rejected(self, checking_account):
        """EP35: 1e-07 is a legal literal but still a sub-cent amount."""
        assert checking_account.transfer(1e-07)["error"] == ERR_AMOUNT_PRECISION
