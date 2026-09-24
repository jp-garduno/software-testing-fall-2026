"""Equivalence partitioning tests (design: design/test-design-document.md, section 1)."""

from datetime import date

import pytest

from banking_system import BankAccount


class TestTransferAmountPartitions:
    """Input: transfer amount (EP1-EP7)."""

    def test_ep1_valid_amount_within_limits_succeeds(self, checking):
        """EP1: $500 from a $10,000 Checking account succeeds."""
        result = checking.transfer(500)
        assert result["success"] is True
        assert checking.balance == 9500

    def test_ep2_zero_amount_is_rejected(self, checking):
        """EP2: $0 is not a positive amount."""
        result = checking.transfer(0)
        assert result["success"] is False
        assert result["error"] == "Amount must be positive"
        assert checking.balance == 10000

    def test_ep3_negative_amount_is_rejected(self, checking):
        """EP3: -$100 is not a positive amount."""
        result = checking.transfer(-100)
        assert result["success"] is False
        assert result["error"] == "Amount must be positive"
        assert checking.balance == 10000

    def test_ep4_amount_over_daily_limit_is_rejected(self, checking):
        """EP4: $100,000 exceeds the $5,000 Checking daily limit."""
        result = checking.transfer(100000)
        assert result["success"] is False
        assert "Exceeds daily limit" in result["errors"]
        assert checking.daily_transfer_total == 0

    def test_ep5_amount_over_balance_is_rejected(self, make_account):
        """EP5: balance + $1 cannot be transferred."""
        account = make_account("Checking", 300)
        result = account.transfer(301)
        assert result["success"] is False
        assert result["error"] == "Insufficient funds"
        assert account.balance == 300

    @pytest.mark.parametrize("bad_amount", ["abc", None, True, [500], float("nan"), float("inf")])
    def test_ep6_non_numeric_amount_is_rejected(self, checking, bad_amount):
        """EP6: amounts that are not finite numbers are rejected."""
        result = checking.transfer(bad_amount)
        assert result["success"] is False
        assert result["error"] == "Amount must be a number"
        assert checking.balance == 10000

    def test_ep7_more_than_two_decimals_is_rejected(self, checking):
        """EP7: $10.005 cannot be represented in cents."""
        result = checking.transfer(10.005)
        assert result["success"] is False
        assert "2 decimal places" in result["error"]


class TestAccountTypePartitions:
    """Input: account type (EP8-EP11)."""

    @pytest.mark.parametrize(
        "account_type, expected_limit",
        [("Savings", 2000), ("Checking", 5000), ("Premium", 50000)],
    )
    def test_ep8_to_ep10_each_type_has_its_daily_limit(self, make_account, account_type, expected_limit):
        """EP8/EP9/EP10: Savings $2,000, Checking $5,000, Premium $50,000."""
        balance = 10000 if account_type != "Premium" else 100000
        account = make_account(account_type, balance)
        assert account.get_daily_limit() == expected_limit
        assert account.transfer(expected_limit)["success"] is True
        assert account.transfer(1)["success"] is False

    def test_ep11_unknown_account_type_is_rejected(self):
        """EP11: 'Gold' is not an account type."""
        with pytest.raises(ValueError, match="Invalid account type"):
            BankAccount("Gold", 1000)


class TestInitialBalancePartitions:
    """Input: initial balance when creating an account (EP12-EP15)."""

    def test_ep12_negative_balance_is_rejected(self):
        """EP12: a negative opening balance is invalid."""
        with pytest.raises(ValueError, match="cannot be negative"):
            BankAccount("Checking", -1)

    def test_ep13_balance_below_type_minimum_is_rejected(self):
        """EP13: $50 is positive but below the Savings minimum of $100."""
        with pytest.raises(ValueError, match="below the Savings minimum"):
            BankAccount("Savings", 50)

    def test_ep14_balance_above_minimum_creates_active_account(self):
        """EP14: $500 Savings account is created Active."""
        account = BankAccount("Savings", 500)
        assert account.state == "Active"
        assert account.balance == 500

    def test_ep15_non_numeric_balance_is_rejected(self):
        """EP15: a text balance is invalid."""
        with pytest.raises(ValueError, match="must be a number"):
            BankAccount("Checking", "lots")


class TestAccountStatePartitions:
    """Input: account state when transferring (EP16-EP19)."""

    def test_ep16_active_account_can_transfer(self, checking):
        """EP16: Active accounts operate normally, no warning."""
        result = checking.transfer(100)
        assert result["success"] is True
        assert result["warning"] is None

    def test_ep17_suspended_account_can_transfer_with_warning(self, make_account):
        """EP17: Suspended accounts may still transfer and show a warning."""
        account = make_account("Savings", 150)
        account.transfer(60)
        assert account.state == "Suspended"
        result = account.transfer(10)
        assert result["success"] is True
        assert account.balance == 80

    def test_ep18_frozen_account_cannot_transfer(self, checking):
        """EP18: Frozen accounts are view-only."""
        checking.freeze()
        result = checking.transfer(100)
        assert result["success"] is False
        assert result["error"] == "Account is frozen"
        assert checking.get_balance() == 10000

    def test_ep19_closed_account_cannot_transfer(self, checking):
        """EP19: Closed accounts reject transfers."""
        checking.close()
        result = checking.transfer(100)
        assert result["success"] is False
        assert result["error"] == "Account is closed"


class TestPayeePartitions:
    """Input: payee information for bill payment (EP20-EP23)."""

    def test_ep20_registered_payee_is_paid(self, checking, today):
        """EP20: a registered utility is paid and debited."""
        result = checking.pay_bill("CFE Electricity", 250, on_date=today)
        assert result["success"] is True
        assert checking.balance == 9750

    def test_ep21_unregistered_payee_is_rejected(self, checking, today):
        """EP21: an unknown payee is invalid."""
        result = checking.pay_bill("Random Store", 250, on_date=today)
        assert result["success"] is False
        assert result["error"] == "Invalid payee"
        assert checking.balance == 10000

    @pytest.mark.parametrize("blank", ["", "   "])
    def test_ep22_blank_payee_is_rejected(self, checking, today, blank):
        """EP22: empty or whitespace-only payee names are missing information."""
        result = checking.pay_bill(blank, 250, on_date=today)
        assert result["success"] is False
        assert result["error"] == "Payee is required"

    def test_ep23_non_string_payee_is_rejected(self, checking, today):
        """EP23: a payee that is not text is missing information."""
        result = checking.pay_bill(None, 250, on_date=today)
        assert result["success"] is False
        assert result["error"] == "Payee is required"


class TestPaymentDatePartitions:
    """Input: bill payment date (EP24-EP27)."""

    def test_ep24_no_date_pays_immediately(self, checking, today):
        """EP24: without a date the payment is immediate."""
        result = checking.pay_bill("Telmex Internet", 100, on_date=today)
        assert result["scheduled"] is False
        assert checking.balance == 9900

    def test_ep25_future_date_schedules_without_debit(self, checking, today):
        """EP25: a future date only schedules the payment."""
        result = checking.pay_bill("Telmex Internet", 100, payment_date="2026-10-01", on_date=today)
        assert result["scheduled"] is True
        assert checking.balance == 10000
        assert checking.scheduled_payments[0]["date"] == date(2026, 10, 1)

    def test_ep26_past_date_is_rejected(self, checking, today):
        """EP26: payments cannot be dated in the past."""
        result = checking.pay_bill("Telmex Internet", 100, payment_date="2026-09-01", on_date=today)
        assert result["success"] is False
        assert result["error"] == "Payment date cannot be in the past"

    def test_ep27_malformed_date_is_rejected(self, checking, today):
        """EP27: '15/09/2026' is not an ISO date."""
        result = checking.pay_bill("Telmex Internet", 100, payment_date="15/09/2026", on_date=today)
        assert result["success"] is False
        assert result["error"] == "Invalid payment date"


class TestHistoryDateRangePartitions:
    """Input: date range for transaction history (EP28-EP34)."""

    @pytest.fixture
    def history_account(self, make_account):
        """Account with deposits on Sep 1, Sep 10 and Sep 20."""
        account = make_account("Checking", 1000)
        for day in ("2026-09-01", "2026-09-10", "2026-09-20"):
            account.deposit(100, on_date=day)
        return account

    def test_ep28_range_containing_transactions(self, history_account):
        """EP28: Sep 5 - Sep 15 contains only the Sep 10 deposit."""
        rows = history_account.get_history("2026-09-05", "2026-09-15")
        assert [row["date"] for row in rows] == [date(2026, 9, 10)]

    def test_ep29_range_without_transactions_is_empty(self, history_account):
        """EP29: a valid range with no activity returns an empty list."""
        assert history_account.get_history("2026-08-01", "2026-08-31") == []

    def test_ep30_only_start_date(self, history_account):
        """EP30: open-ended range starting Sep 10."""
        assert len(history_account.get_history(start="2026-09-10")) == 2

    def test_ep31_only_end_date(self, history_account):
        """EP31: open-ended range ending Sep 10."""
        assert len(history_account.get_history(end="2026-09-10")) == 2

    def test_ep32_start_after_end_is_rejected(self, history_account):
        """EP32: an inverted range is invalid."""
        with pytest.raises(ValueError, match="must not be after"):
            history_account.get_history("2026-09-20", "2026-09-01")

    def test_ep33_malformed_date_is_rejected(self, history_account):
        """EP33: 'yesterday' is not a date."""
        with pytest.raises(ValueError, match="Invalid date"):
            history_account.get_history("yesterday", "2026-09-01")

    def test_ep34_no_filter_returns_everything(self, history_account):
        """EP34: no range returns the whole history."""
        assert len(history_account.get_history()) == 3


class TestDepositAndDatePartitions:
    """Supporting partitions for deposits (EP35-EP36) and date inputs (EP37)."""

    @pytest.mark.parametrize("bad_amount", [0, -5, "ten", 1.234])
    def test_ep35_invalid_deposit_amounts_are_rejected(self, checking, bad_amount):
        """EP35: deposits follow the same amount rules as transfers."""
        assert checking.deposit(bad_amount)["success"] is False
        assert checking.balance == 10000

    def test_ep36_valid_deposit_increases_balance(self, checking):
        """EP36: a $250.50 deposit is credited."""
        assert checking.deposit(250.50)["success"] is True
        assert checking.balance == 10250.50

    def test_ep37_date_inputs_accept_dates_datetimes_and_iso_strings(self, checking):
        """EP37: date, datetime and 'YYYY-MM-DD' all identify the same day; other types do not."""
        from datetime import datetime  # pylint: disable=import-outside-toplevel

        checking.deposit(1, on_date=date(2026, 9, 1))
        checking.deposit(1, on_date=datetime(2026, 9, 1, 23, 59))
        checking.deposit(1, on_date="2026-09-01")
        assert len(checking.get_history("2026-09-01", "2026-09-01")) == 3
        assert checking.process_monthly_fee(12345)["error"] == "Invalid date"
