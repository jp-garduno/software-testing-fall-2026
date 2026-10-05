"""Decision table tests.

One test per rule of the three tables in
``design/test-design-document.md``. Rule ids are written as DT<table>-R<rule>.
"""

from src.banking_system import BankAccount


class TestTransferValidationTable:
    """DT1: transfer validation.

    Conditions, in the order the system evaluates them: account allows
    transactions, amount within the daily limit, sufficient funds. The order
    matters because it decides which error a caller sees when more than one
    condition fails.
    """

    def test_rule_1_all_conditions_met(self):
        """DT1-R1: funds Y, limit Y, active Y -> transfer succeeds."""
        account = BankAccount("Checking", 10000.0)
        result = account.transfer(1000)
        assert result["success"] is True
        assert account.balance == 9000.00

    def test_rule_2_frozen_account(self):
        """DT1-R2: funds Y, limit Y, active N -> account frozen."""
        account = BankAccount("Checking", 10000.0, state="Frozen")
        result = account.transfer(1000)
        assert result["success"] is False
        assert result["error"] == "Account is frozen"

    def test_rule_3_above_daily_limit(self):
        """DT1-R3: funds Y, limit N, active Y -> exceeds daily limit."""
        account = BankAccount("Checking", 10000.0)
        result = account.transfer(6000)
        assert result["success"] is False
        assert result["error"] == "Exceeds daily limit"

    def test_rule_4_above_limit_and_frozen(self):
        """DT1-R4: funds Y, limit N, active N -> state wins over the limit."""
        account = BankAccount("Checking", 10000.0, state="Frozen")
        result = account.transfer(6000)
        assert result["success"] is False
        assert result["error"] == "Account is frozen"

    def test_rule_5_insufficient_funds(self):
        """DT1-R5: funds N, limit Y, active Y -> insufficient funds."""
        account = BankAccount("Checking", 500.0)
        result = account.transfer(1000)
        assert result["success"] is False
        assert result["error"] == "Insufficient funds"

    def test_rule_6_insufficient_and_frozen(self):
        """DT1-R6: funds N, limit Y, active N -> state wins over the funds."""
        account = BankAccount("Checking", 500.0, state="Frozen")
        result = account.transfer(1000)
        assert result["success"] is False
        assert result["error"] == "Account is frozen"

    def test_rule_7_insufficient_and_above_limit(self):
        """DT1-R7: funds N, limit N, active Y -> the limit is reported first."""
        account = BankAccount("Checking", 500.0)
        result = account.transfer(6000)
        assert result["success"] is False
        assert result["error"] == "Exceeds daily limit"

    def test_rule_8_all_conditions_failed(self):
        """DT1-R8: funds N, limit N, active N -> state still wins."""
        account = BankAccount("Checking", 500.0, state="Frozen")
        result = account.transfer(6000)
        assert result["success"] is False
        assert result["error"] == "Account is frozen"


class TestMonthlyFeeTable:
    """DT2: monthly fee processing on the 1st of the month."""

    def test_rule_1_savings_above_waiver(self):
        """DT2-R1: Savings above $1,000 -> fee waived."""
        account = BankAccount("Savings", 1500.0)
        result = account.apply_monthly_fee()
        assert result["waived"] is True
        assert account.balance == 1500.00

    def test_rule_2_savings_below_waiver(self):
        """DT2-R2: Savings at or below $1,000 -> $5 charged."""
        account = BankAccount("Savings", 500.0)
        result = account.apply_monthly_fee()
        assert result["charged"] == 5.0
        assert account.balance == 495.00

    def test_rule_3_savings_cannot_cover_the_fee(self):
        """DT2-R3: balance under the fee -> not charged, account suspended."""
        account = BankAccount("Savings", 3.0)
        result = account.apply_monthly_fee()
        assert result["success"] is False
        assert result["error"] == "Insufficient funds for fee"
        assert account.state == "Suspended"
        assert account.balance == 3.00

    def test_rule_4_checking_above_waiver(self):
        """DT2-R4: Checking above $5,000 -> fee waived."""
        account = BankAccount("Checking", 6000.0)
        assert account.apply_monthly_fee()["waived"] is True

    def test_rule_5_checking_below_waiver(self):
        """DT2-R5: Checking at or below $5,000 -> $10 charged."""
        account = BankAccount("Checking", 5000.0)
        result = account.apply_monthly_fee()
        assert result["charged"] == 10.0
        assert account.balance == 4990.00

    def test_rule_6_premium_never_pays(self):
        """DT2-R6: Premium has no monthly fee regardless of balance."""
        account = BankAccount("Premium", 10000.0)
        result = account.apply_monthly_fee()
        assert result["waived"] is True
        assert account.balance == 10000.00


class TestBillPaymentTable:
    """DT3: bill payment validation."""

    def test_rule_1_valid_immediate_payment(self):
        """DT3-R1: payee Y, amount Y, funds Y, immediate -> paid now."""
        account = BankAccount("Checking", 1000.0)
        result = account.pay_bill("Electric Co", 250)
        assert result["success"] is True
        assert result["scheduled"] is False
        assert account.balance == 750.00

    def test_rule_2_invalid_payee(self):
        """DT3-R2: payee N -> rejected before anything else is checked."""
        account = BankAccount("Checking", 1000.0)
        result = account.pay_bill("", 250)
        assert result["success"] is False
        assert result["error"] == "Invalid payee"

    def test_rule_3_non_positive_amount(self):
        """DT3-R3: payee Y, amount N -> amount must be positive."""
        account = BankAccount("Checking", 1000.0)
        result = account.pay_bill("Electric Co", 0)
        assert result["success"] is False
        assert result["error"] == "Amount must be positive"

    def test_rule_4_insufficient_funds(self):
        """DT3-R4: payee Y, amount Y, funds N -> insufficient funds."""
        account = BankAccount("Checking", 100.0)
        result = account.pay_bill("Electric Co", 250)
        assert result["success"] is False
        assert result["error"] == "Insufficient funds"

    def test_rule_5_future_dated_payment_is_scheduled(self, tomorrow):
        """DT3-R5: a future date schedules the payment without moving money."""
        account = BankAccount("Checking", 1000.0)
        result = account.pay_bill("Electric Co", 250, scheduled_date=tomorrow)
        assert result["success"] is True
        assert result["scheduled"] is True
        assert account.balance == 1000.00

    def test_rule_6_past_dated_payment_is_rejected(self, yesterday):
        """DT3-R6: a date already gone cannot be scheduled."""
        account = BankAccount("Checking", 1000.0)
        result = account.pay_bill("Electric Co", 250, scheduled_date=yesterday)
        assert result["success"] is False
        assert result["error"] == "Scheduled date is in the past"


class TestBillPaymentGuardRules:
    """DT3 continued: the guards that run before the payee is even read."""

    def test_rule_7_frozen_account(self):
        """DT3-R7: a frozen account pays no bills."""
        account = BankAccount("Checking", 1000.0, state="Frozen")
        result = account.pay_bill("Electric Co", 250)
        assert result["success"] is False
        assert result["error"] == "Account is frozen"

    def test_rule_8_non_numeric_amount(self):
        """DT3-R8: an amount that is not a number."""
        account = BankAccount("Checking", 1000.0)
        result = account.pay_bill("Electric Co", "two hundred")
        assert result["success"] is False
        assert result["error"] == "Amount must be a number"


class TestMonthlyFeeOnNonActiveAccounts:
    """DT2 continued: the fee run meets accounts that are not Active."""

    def test_closed_account_is_not_charged(self):
        """DT2-R7: a closed account is out of the fee run."""
        account = BankAccount("Checking", 1000.0)
        account.close()
        result = account.apply_monthly_fee()
        assert result["success"] is False
        assert result["error"] == "Account is closed"

    def test_frozen_account_is_still_charged_and_stays_frozen(self):
        """DT2-R8: freezing stops the customer, not the bank's own fee."""
        account = BankAccount("Savings", 500.0, state="Frozen")
        result = account.apply_monthly_fee()
        assert result["charged"] == 5.0
        assert account.balance == 495.00
        assert account.state == "Frozen"
