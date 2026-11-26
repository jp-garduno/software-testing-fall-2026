"""Boundary value analysis tests (design: design/test-design-document.md, section 2)."""

from datetime import date, timedelta

import pytest

from banking_system import BankAccount


class TestTransferAmountCheckingLimit:
    """Boundary 1: transfer amount, Checking account, $5,000 daily limit (BV1-BV6)."""

    def test_bv1_zero_is_below_minimum(self, checking):
        """BV1: $0.00 -> Error: Amount must be positive."""
        result = checking.transfer(0.00)
        assert result["success"] is False
        assert "must be positive" in result["error"]

    def test_bv2_minimum_valid_amount(self, make_account):
        """BV2: exactly $0.01 succeeds."""
        account = make_account("Checking", 1000)
        result = account.transfer(0.01)
        assert result["success"] is True
        assert account.balance == 999.99

    def test_bv3_just_below_limit(self, checking):
        """BV3: $4,999.99 succeeds."""
        assert checking.transfer(4999.99)["success"] is True
        assert checking.daily_transfer_total == 4999.99

    def test_bv4_exactly_at_limit(self, checking):
        """BV4: $5,000.00 succeeds."""
        result = checking.transfer(5000)
        assert result["success"] is True
        assert checking.daily_transfer_total == 5000

    def test_bv5_just_above_limit(self, checking):
        """BV5: $5,000.01 -> Error: Exceeds daily limit."""
        result = checking.transfer(5000.01)
        assert result["success"] is False
        assert result["error"] == "Exceeds daily limit"
        assert checking.balance == 10000

    def test_bv6_far_above_limit(self, checking):
        """BV6: $10,000.00 -> Error: Exceeds daily limit."""
        result = checking.transfer(10000)
        assert result["success"] is False
        assert result["error"] == "Exceeds daily limit"


class TestTransferAmountSavingsLimit:
    """Boundary 2: transfer amount, Savings account, $2,000 daily limit (BV7-BV11)."""

    @pytest.mark.parametrize(
        "amount, should_succeed",
        [
            (0.01, True),  # BV7 minimum valid
            (1999.99, True),  # BV8 just below limit
            (2000.00, True),  # BV9 at limit
            (2000.01, False),  # BV10 just above limit
            (4000.00, False),  # BV11 far above limit
        ],
    )
    def test_bv7_to_bv11_savings_limit_boundary(self, savings, amount, should_succeed):
        """BV7-BV11: values around the $2,000 Savings limit."""
        assert savings.transfer(amount)["success"] is should_succeed


class TestTransferAmountVersusBalance:
    """Boundary 3: transfer amount against a $1,000 balance (BV12-BV16)."""

    @pytest.mark.parametrize(
        "amount, should_succeed, expected_balance",
        [
            (1.00, True, 999.00),  # BV12 small amount
            (999.99, True, 0.01),  # BV13 one cent below balance
            (1000.00, True, 0.00),  # BV14 whole balance
            (1000.01, False, 1000.00),  # BV15 one cent above balance
            (1500.00, False, 1000.00),  # BV16 far above balance
        ],
    )
    def test_bv12_to_bv16_amount_versus_balance(self, make_account, amount, should_succeed, expected_balance):
        """BV12-BV16: a transfer may use the whole balance but not a cent more."""
        account = make_account("Checking", 1000)
        result = account.transfer(amount)
        assert result["success"] is should_succeed
        assert account.balance == expected_balance
        if not should_succeed:
            assert result["error"] == "Insufficient funds"


class TestBalanceVersusMinimum:
    """Boundary 4: resulting balance against the Savings minimum of $100 (BV17-BV21)."""

    @pytest.mark.parametrize(
        "transfer_amount, resulting_balance, expected_state",
        [
            (99.99, 100.01, "Active"),  # BV17 just above minimum
            (100.00, 100.00, "Active"),  # BV18 exactly the minimum
            (100.01, 99.99, "Suspended"),  # BV19 just below minimum
            (199.99, 0.01, "Suspended"),  # BV20 almost empty
            (200.00, 0.00, "Suspended"),  # BV21 empty
        ],
    )
    def test_bv17_to_bv21_savings_minimum_balance(
        self, make_account, transfer_amount, resulting_balance, expected_state
    ):
        """BV17-BV21: balance == minimum stays Active, one cent less suspends."""
        account = make_account("Savings", 200)
        result = account.transfer(transfer_amount)
        assert result["success"] is True
        assert account.balance == resulting_balance
        assert account.state == expected_state

    def test_bv22_premium_minimum_boundary(self, make_account):
        """BV22: Premium at $10,000.00 is Active, at $9,999.99 it is Suspended."""
        at_minimum = make_account("Premium", 10001)
        below_minimum = make_account("Premium", 10001)
        at_minimum.transfer(1)
        below_minimum.transfer(1.01)
        assert at_minimum.state == "Active"
        assert below_minimum.state == "Suspended"


class TestCumulativeDailyLimit:
    """Boundary 5: the daily limit accumulates and resets at midnight (BV23-BV27)."""

    def test_bv23_two_transfers_adding_up_to_limit(self, checking, today):
        """BV23: $4,999.99 + $0.01 = $5,000.00 is allowed."""
        assert checking.transfer(4999.99, on_date=today)["success"] is True
        assert checking.transfer(0.01, on_date=today)["success"] is True
        assert checking.daily_transfer_total == 5000

    def test_bv24_one_cent_over_accumulated_limit(self, checking, today):
        """BV24: after reaching $5,000, one more cent is rejected."""
        checking.transfer(5000, on_date=today)
        result = checking.transfer(0.01, on_date=today)
        assert result["success"] is False
        assert result["error"] == "Exceeds daily limit"

    def test_bv25_rejected_transfer_does_not_count(self, checking, today):
        """BV25: a rejected $5,000.01 transfer leaves the whole $5,000 available."""
        checking.transfer(5000.01, on_date=today)
        assert checking.daily_transfer_total == 0
        assert checking.transfer(5000, on_date=today)["success"] is True

    def test_bv26_limit_resets_on_next_day(self, checking, today):
        """BV26: the day after hitting the limit, $5,000 is available again."""
        checking.transfer(5000, on_date=today)
        result = checking.transfer(5000, on_date=today + timedelta(days=1))
        assert result["success"] is True
        assert checking.daily_transfer_total == 5000

    def test_bv27_limit_does_not_reset_within_same_day(self, checking):
        """BV27: 23:59 and 00:00 are different days; two transfers on the same day are not."""
        checking.transfer(5000, on_date=date(2026, 9, 15))
        assert checking.transfer(1, on_date=date(2026, 9, 15))["success"] is False
        assert checking.transfer(1, on_date=date(2026, 9, 16))["success"] is True


class TestFeeWaiverThreshold:
    """Boundary 6: monthly fee waiver thresholds (BV28-BV35). Fees are charged on the 1st."""

    @pytest.mark.parametrize(
        "balance, expected_fee",
        [
            (999.99, 5.0),  # BV28 just below threshold
            (1000.00, 5.0),  # BV29 exactly at threshold: "> $1,000" is NOT met
            (1000.01, 0.0),  # BV30 just above threshold: waived
            (1001.00, 0.0),  # BV31 above threshold
        ],
    )
    def test_bv28_to_bv31_savings_fee_waiver(self, make_account, balance, expected_fee):
        """BV28-BV31: Savings pays $5 unless the balance is strictly above $1,000."""
        account = make_account("Savings", balance)
        result = account.process_monthly_fee("2026-10-01")
        assert result["fee_charged"] == expected_fee
        assert result["waived"] is (expected_fee == 0.0)

    @pytest.mark.parametrize(
        "balance, expected_fee",
        [
            (4999.99, 10.0),  # BV32 just below threshold
            (5000.00, 10.0),  # BV33 exactly at threshold
            (5000.01, 0.0),  # BV34 just above threshold
        ],
    )
    def test_bv32_to_bv34_checking_fee_waiver(self, make_account, balance, expected_fee):
        """BV32-BV34: Checking pays $10 unless the balance is strictly above $5,000."""
        account = make_account("Checking", balance)
        assert account.process_monthly_fee("2026-10-01")["fee_charged"] == expected_fee


class TestFeeAffordability:
    """Boundary 7: balance against the $10 Checking fee (BV35-BV37)."""

    def test_bv35_balance_one_cent_below_fee_suspends(self, make_account):
        """BV35: $9.99 cannot pay $10 -> account Suspended, nothing charged."""
        account = make_account("Checking", 9.99)
        result = account.process_monthly_fee("2026-10-01")
        assert result["suspended"] is True
        assert account.state == "Suspended"
        assert account.balance == 9.99
        assert account.unpaid_fees == 10

    def test_bv36_balance_equal_to_fee_is_charged(self, make_account):
        """BV36: $10.00 pays the fee exactly; Checking minimum is $0 so it stays Active."""
        account = make_account("Checking", 10)
        result = account.process_monthly_fee("2026-10-01")
        assert result["fee_charged"] == 10
        assert account.balance == 0
        assert account.state == "Active"

    def test_bv37_balance_one_cent_above_fee_is_charged(self, make_account):
        """BV37: $10.01 pays the fee and keeps one cent."""
        account = make_account("Checking", 10.01)
        account.process_monthly_fee("2026-10-01")
        assert account.balance == 0.01
        assert account.state == "Active"


class TestFeeProcessingDay:
    """Boundary 8: fees are charged only on the 1st of the month (BV38-BV42)."""

    @pytest.mark.parametrize(
        "day, charged",
        [
            ("2026-09-30", False),  # BV38 last day of previous month
            ("2026-10-01", True),  # BV39 first of the month
            ("2026-10-02", False),  # BV40 day after
            ("2026-02-28", False),  # BV41 last day of February
            ("2026-03-01", True),  # BV42 first day after February
        ],
    )
    def test_bv38_to_bv42_fee_only_on_first_of_month(self, make_account, day, charged):
        """BV38-BV42: only the 1st of a month triggers fee processing."""
        account = make_account("Checking", 1000)
        assert account.process_monthly_fee(day)["success"] is charged
        assert (account.balance == 990) is charged


class TestAccountCreationMinimums:
    """Boundary 9: opening balance against the type minimum (BV43-BV48)."""

    @pytest.mark.parametrize(
        "account_type, balance, valid",
        [
            ("Savings", 99.99, False),  # BV43
            ("Savings", 100.00, True),  # BV44
            ("Savings", 100.01, True),  # BV45
            ("Premium", 9999.99, False),  # BV46
            ("Premium", 10000.00, True),  # BV47
            ("Premium", 10000.01, True),  # BV48
        ],
    )
    def test_bv43_to_bv48_opening_balance_minimum(self, account_type, balance, valid):
        """BV43-BV48: the minimum balance itself is the smallest valid opening balance."""
        if valid:
            assert BankAccount(account_type, balance).state == "Active"
        else:
            with pytest.raises(ValueError):
                BankAccount(account_type, balance)


class TestAmountPrecision:
    """Boundary 10: decimal precision of amounts (BV49-BV52)."""

    @pytest.mark.parametrize(
        "amount, valid",
        [
            (0.001, False),  # BV49 below one cent
            (0.01, True),  # BV50 one cent
            (0.011, False),  # BV51 fractions of a cent
            (0.10, True),  # BV52 ten cents
        ],
    )
    def test_bv49_to_bv52_amount_precision(self, checking, amount, valid):
        """BV49-BV52: amounts must be whole cents."""
        assert checking.transfer(amount)["success"] is valid


class TestHistoryDateBoundaries:
    """Boundary 11: inclusive limits of a history date range (BV53-BV56)."""

    @pytest.fixture
    def account_with_deposits(self, make_account):
        """Deposits on Sep 9, 10, 20 and 21 (one day either side of the range)."""
        account = make_account("Checking", 1000)
        for day in ("2026-09-09", "2026-09-10", "2026-09-20", "2026-09-21"):
            account.deposit(1, on_date=day)
        return account

    def test_bv53_day_before_start_is_excluded(self, account_with_deposits):
        """BV53: Sep 9 is outside Sep 10 - Sep 20."""
        days = [tx["date"] for tx in account_with_deposits.get_history("2026-09-10", "2026-09-20")]
        assert date(2026, 9, 9) not in days

    def test_bv54_start_day_is_included(self, account_with_deposits):
        """BV54: Sep 10 is inside the range."""
        days = [tx["date"] for tx in account_with_deposits.get_history("2026-09-10", "2026-09-20")]
        assert date(2026, 9, 10) in days

    def test_bv55_end_day_is_included(self, account_with_deposits):
        """BV55: Sep 20 is inside the range."""
        days = [tx["date"] for tx in account_with_deposits.get_history("2026-09-10", "2026-09-20")]
        assert date(2026, 9, 20) in days

    def test_bv56_day_after_end_is_excluded_and_single_day_range_works(self, account_with_deposits):
        """BV56: Sep 21 is outside; a range with start == end returns that single day."""
        rows = account_with_deposits.get_history("2026-09-10", "2026-09-20")
        assert date(2026, 9, 21) not in [tx["date"] for tx in rows]
        assert len(account_with_deposits.get_history("2026-09-20", "2026-09-20")) == 1


class TestPaymentDateBoundaries:
    """Boundary 12: bill payment date around 'today' (BV57-BV59)."""

    @pytest.mark.parametrize(
        "payment_date, outcome",
        [
            ("2026-09-14", "rejected"),  # BV57 yesterday
            ("2026-09-15", "paid"),  # BV58 today
            ("2026-09-16", "scheduled"),  # BV59 tomorrow
        ],
    )
    def test_bv57_to_bv59_payment_date_around_today(self, checking, today, payment_date, outcome):
        """BV57-BV59: yesterday is rejected, today is immediate, tomorrow is scheduled."""
        result = checking.pay_bill("Visa Credit Card", 100, payment_date=payment_date, on_date=today)
        if outcome == "rejected":
            assert result["success"] is False
        else:
            assert result["success"] is True
            assert result["scheduled"] is (outcome == "scheduled")
            assert checking.balance == (10000 if outcome == "scheduled" else 9900)
