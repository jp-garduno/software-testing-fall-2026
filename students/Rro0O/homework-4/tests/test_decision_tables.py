"""Decision table tests (design: design/test-design-document.md, section 3)."""

import pytest

from banking_system import BankAccount


def _account_for_transfer(make_account, funds_ok, limit_ok, operable):
    """Build an account and amount that produce the requested condition combination.

    Checking account with $1,000: amount $500 fits the balance and the $5,000 limit.
    Amount $6,000 exceeds the limit and the balance; $2,000 exceeds only the balance.
    """
    account = make_account("Checking", 1000)
    if funds_ok and limit_ok:
        amount = 500
    elif funds_ok and not limit_ok:
        account = make_account("Checking", 20000)
        amount = 6000
    elif not funds_ok and limit_ok:
        amount = 2000
    else:
        amount = 6000
    if not operable:
        account.freeze()
    return account, amount


class TestTransferValidationTable:
    """Decision table 1: transfer validation (DT1-R1 ... DT1-R8)."""

    @pytest.mark.parametrize(
        "rule, funds_ok, limit_ok, operable, expected_errors",
        [
            ("R1", True, True, True, []),
            ("R2", True, True, False, ["Account is frozen"]),
            ("R3", True, False, True, ["Exceeds daily limit"]),
            ("R4", True, False, False, ["Account is frozen"]),
            ("R5", False, True, True, ["Insufficient funds"]),
            ("R6", False, True, False, ["Account is frozen"]),
            ("R7", False, False, True, ["Exceeds daily limit", "Insufficient funds"]),
            ("R8", False, False, False, ["Account is frozen"]),
        ],
    )
    def test_dt1_transfer_validation_rules(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self, make_account, rule, funds_ok, limit_ok, operable, expected_errors
    ):
        """DT1-R1..R8: every combination of funds / limit / account state gives the tabulated actions."""
        account, amount = _account_for_transfer(make_account, funds_ok, limit_ok, operable)
        balance_before = account.balance
        result = account.transfer(amount)
        assert result["errors"] == expected_errors, rule
        assert result["success"] is (not expected_errors)
        if expected_errors:
            assert account.balance == balance_before
        else:
            assert account.balance == balance_before - amount

    def test_dt1_r9_closed_account_behaves_like_frozen(self, checking):
        """DT1-R9: a Closed account is also 'not operable' but reports a different message."""
        checking.close()
        assert checking.transfer(100)["errors"] == ["Account is closed"]

    def test_dt1_r10_destination_that_cannot_receive_blocks_the_transfer(self, make_account):
        """DT1-R10: transferring to a Closed own account fails and nothing is debited."""
        source = make_account("Checking", 1000)
        target = make_account("Savings", 500)
        target.close()
        result = source.transfer(100, destination=target)
        assert result["errors"] == ["Destination account cannot receive funds"]
        assert source.balance == 1000

    def test_dt1_r11_transfer_between_own_accounts_moves_money(self, make_account):
        """DT1-R11: own-account transfer debits the source and credits the destination."""
        source = make_account("Checking", 1000)
        target = make_account("Savings", 500)
        result = source.transfer(250, destination=target)
        assert result["success"] is True
        assert (source.balance, target.balance) == (750, 750)

    def test_dt1_r13_suspended_destination_can_receive_and_is_reactivated(self, make_account):
        """DT1-R13: a Suspended own account may receive money; reaching the minimum reactivates it."""
        source = make_account("Checking", 1000)
        target = make_account("Savings", 150)
        target.transfer(60)
        assert target.state == "Suspended"
        assert source.transfer(50, destination=target)["success"] is True
        assert (target.balance, target.state) == (140, "Active")

    def test_dt1_r12_transfer_to_same_account_is_rejected(self, checking):
        """DT1-R12: an account cannot transfer to itself."""
        assert checking.transfer(10, destination=checking)["error"] == "Cannot transfer to the same account"


class TestMonthlyFeeTable:
    """Decision table 2: monthly fee processing (DT2-R1 ... DT2-R9). Date is the 1st unless noted."""

    FEE_DAY = "2026-10-01"

    def test_dt2_r1_savings_above_threshold_is_waived(self, make_account):
        """DT2-R1: Savings $1,500 -> fee waived."""
        account = make_account("Savings", 1500)
        result = account.process_monthly_fee(self.FEE_DAY)
        assert (result["waived"], result["fee_charged"], account.balance) == (True, 0.0, 1500)

    def test_dt2_r2_savings_below_threshold_is_charged(self, make_account):
        """DT2-R2: Savings $500 -> $5 charged, stays Active."""
        account = make_account("Savings", 500)
        result = account.process_monthly_fee(self.FEE_DAY)
        assert (result["fee_charged"], account.balance, account.state) == (5, 495, "Active")

    def test_dt2_r3_savings_fee_pushes_balance_below_minimum(self, make_account):
        """DT2-R3: Savings $102 - $5 = $97 < $100 minimum -> charged and Suspended."""
        account = make_account("Savings", 102)
        result = account.process_monthly_fee(self.FEE_DAY)
        assert result["fee_charged"] == 5
        assert account.balance == 97
        assert account.state == "Suspended"

    def test_dt2_r4_checking_above_threshold_is_waived(self, make_account):
        """DT2-R4: Checking $8,000 -> fee waived."""
        account = make_account("Checking", 8000)
        assert account.process_monthly_fee(self.FEE_DAY)["waived"] is True
        assert account.balance == 8000

    def test_dt2_r5_checking_below_threshold_is_charged(self, make_account):
        """DT2_R5: Checking $2,000 -> $10 charged."""
        account = make_account("Checking", 2000)
        account.process_monthly_fee(self.FEE_DAY)
        assert account.balance == 1990

    def test_dt2_r6_checking_cannot_afford_fee_is_suspended(self, make_account):
        """DT2-R6: Checking $5 cannot pay $10 -> Suspended, fee recorded as unpaid."""
        account = make_account("Checking", 5)
        result = account.process_monthly_fee(self.FEE_DAY)
        assert result["suspended"] is True
        assert (account.state, account.balance, account.unpaid_fees) == ("Suspended", 5, 10)

    @pytest.mark.parametrize("balance", [10000, 250000])
    def test_dt2_r7_premium_never_pays_a_fee(self, make_account, balance):
        """DT2-R7: Premium monthly fee is $0 at any balance."""
        account = make_account("Premium", balance)
        result = account.process_monthly_fee(self.FEE_DAY)
        assert (result["fee_charged"], account.balance) == (0.0, balance)

    def test_dt2_r8_not_first_of_month_nothing_happens(self, make_account):
        """DT2-R8: on the 15th no fee is processed."""
        account = make_account("Checking", 100)
        result = account.process_monthly_fee("2026-10-15")
        assert result["success"] is False
        assert account.balance == 100

    @pytest.mark.parametrize("closer", ["freeze", "close"])
    def test_dt2_r9_frozen_or_closed_accounts_are_skipped(self, make_account, closer):
        """DT2-R9: fees are not processed for Frozen / Closed accounts."""
        account = make_account("Checking", 100)
        getattr(account, closer)()
        result = account.process_monthly_fee(self.FEE_DAY)
        assert result["success"] is False
        assert account.balance == 100

    def test_dt2_r11_suspended_account_still_pays_the_fee(self, make_account):
        """DT2-R11: fees are processed for Suspended accounts too ($90 - $5 = $85, still Suspended)."""
        account = make_account("Savings", 150)
        account.transfer(60)
        result = account.process_monthly_fee(self.FEE_DAY)
        assert result["fee_charged"] == 5
        assert (account.balance, account.state) == (85, "Suspended")

    def test_dt2_r10_invalid_date_is_rejected(self, checking):
        """DT2-R10: an unparsable date cannot trigger fees."""
        assert checking.process_monthly_fee("first of october")["error"] == "Invalid date"


class TestBillPaymentTable:
    """Decision table 3: bill payment validation (DT3-R1 ... DT3-R8)."""

    def test_dt3_r1_all_valid_immediate_payment(self, checking, today):
        """DT3-R1: valid payee, amount, funds, date today -> paid now."""
        result = checking.pay_bill("SIAPA Water", 300, on_date=today)
        assert (result["success"], result["scheduled"], checking.balance) == (True, False, 9700)
        assert checking.transactions[-1]["type"] == "bill payment"

    def test_dt3_r2_all_valid_future_payment_is_scheduled(self, checking, today):
        """DT3-R2: valid, future date -> scheduled, balance untouched."""
        result = checking.pay_bill("SIAPA Water", 300, payment_date="2026-12-31", on_date=today)
        assert (result["scheduled"], checking.balance, len(checking.scheduled_payments)) == (True, 10000, 1)

    def test_dt3_r3_invalid_payee(self, checking, today):
        """DT3-R3: unknown payee -> Invalid payee."""
        assert checking.pay_bill("Nobody", 300, on_date=today)["errors"] == ["Invalid payee"]

    def test_dt3_r4_amount_not_positive(self, checking, today):
        """DT3-R4: amount <= 0 -> Amount must be positive."""
        assert checking.pay_bill("SIAPA Water", 0, on_date=today)["errors"] == ["Amount must be positive"]

    def test_dt3_r5_insufficient_funds(self, make_account, today):
        """DT3-R5: amount above balance -> Insufficient funds, nothing debited."""
        account = make_account("Checking", 100)
        assert account.pay_bill("SIAPA Water", 300, on_date=today)["errors"] == ["Insufficient funds"]
        assert account.balance == 100

    def test_dt3_r6_past_date(self, checking, today):
        """DT3-R6: past date -> error."""
        result = checking.pay_bill("SIAPA Water", 300, payment_date="2026-01-01", on_date=today)
        assert result["errors"] == ["Payment date cannot be in the past"]

    def test_dt3_r7_frozen_account_blocks_everything(self, checking, today):
        """DT3-R7: Frozen account -> only the state error, whatever else is wrong."""
        checking.freeze()
        result = checking.pay_bill("Nobody", -5, on_date=today)
        assert result["errors"] == ["Account is frozen"]

    def test_dt3_r8_multiple_failures_are_all_reported(self, checking, today):
        """DT3-R8: bad payee + bad amount + past date are all reported together."""
        result = checking.pay_bill("Nobody", -5, payment_date="2020-01-01", on_date=today)
        assert result["errors"] == ["Invalid payee", "Amount must be positive", "Payment date cannot be in the past"]

    def test_dt3_r10_invalid_amount_type_and_date_are_reported(self, checking, today):
        """DT3-R10: a text amount and an unparsable date are both reported."""
        result = checking.pay_bill("SIAPA Water", "lots", payment_date="someday", on_date=today)
        assert result["errors"] == ["Amount must be a number", "Invalid payment date"]

    def test_dt3_r9_payment_that_drops_below_minimum_suspends(self, make_account, today):
        """DT3-R9: a Savings bill payment leaving $90 (< $100) succeeds with a suspension warning."""
        account = make_account("Savings", 150)
        result = account.pay_bill("Telmex Internet", 60, on_date=today)
        assert result["success"] is True
        assert account.state == "Suspended"
        assert "suspended" in result["warning"]


class TestAccountCreationTable:
    """Decision table 4: account creation (DT4-R1 ... DT4-R5)."""

    def test_dt4_r1_all_conditions_true_creates_account(self):
        """DT4-R1: valid type, balance >= minimum, owner given -> Active account."""
        account = BankAccount("Premium", 12000, owner="  Ana Perez ")
        assert (account.state, account.owner, account.get_minimum_balance()) == ("Active", "Ana Perez", 10000)

    def test_dt4_r2_invalid_type(self):
        """DT4-R2: invalid type -> rejected."""
        with pytest.raises(ValueError, match="Invalid account type"):
            BankAccount("Platinum", 50000)

    def test_dt4_r3_balance_below_minimum(self):
        """DT4-R3: Premium with $9,000 -> rejected."""
        with pytest.raises(ValueError, match="below the Premium minimum"):
            BankAccount("Premium", 9000)

    @pytest.mark.parametrize("owner", ["", "   ", None])
    def test_dt4_r4_missing_owner(self, owner):
        """DT4-R4: blank owner -> rejected."""
        with pytest.raises(ValueError, match="Owner name is required"):
            BankAccount("Checking", 100, owner=owner)

    def test_dt4_r5_update_info_rules(self, checking):
        """DT4-R5: account information can be updated when valid and is validated otherwise."""
        assert checking.update_info(owner="New Name", email="a@b.com")["success"] is True
        assert (checking.owner, checking.email) == ("New Name", "a@b.com")
        result = checking.update_info(owner=" ", email="not-an-email")
        assert result["errors"] == ["Owner name is required", "Invalid e-mail address"]

    def test_dt4_r6_partial_update_changes_only_the_given_field(self, checking):
        """DT4-R6: updating only the owner keeps the e-mail and vice versa."""
        checking.update_info(email="a@b.com")
        checking.update_info(owner="Only Name")
        assert (checking.owner, checking.email) == ("Only Name", "a@b.com")
