"""Decision Table tests — see design/test-design-document.md, Section 3."""

from src.banking_system import BankAccount, validate_bill_payment


class TestTransferValidationDecisionTable:
    def test_dt_r1_active_positive_sufficient_within_limit_succeeds(
        self, checking_account, today
    ):
        """DT1-R1: Active, positive amount, sufficient funds, within limit -> succeeds."""
        result = checking_account.transfer(500, today=today)
        assert result["success"] is True

    def test_dt_r2_active_positive_sufficient_exceeds_limit_fails(
        self, checking_account, today
    ):
        """DT1-R2: Active, positive amount, sufficient funds, exceeds daily limit -> rejected."""
        result = checking_account.transfer(5000.01, today=today)
        assert result["success"] is False
        assert "daily limit" in result["error"]

    def test_dt_r3_active_positive_insufficient_funds_fails(self, today):
        """DT1-R3: Active, positive amount, insufficient funds -> rejected."""
        account = BankAccount("Checking", 100, today=today)
        result = account.transfer(200, today=today)
        assert result["success"] is False
        assert "Insufficient funds" in result["error"]

    def test_dt_r4_active_non_positive_amount_fails(self, checking_account, today):
        """DT1-R4: Active, non-positive amount -> rejected regardless of funds/limit."""
        result = checking_account.transfer(-50, today=today)
        assert result["success"] is False
        assert "must be positive" in result["error"]

    def test_dt_r5_frozen_account_fails_before_other_checks(
        self, checking_account, today
    ):
        """DT1-R5: Frozen account rejects transfer even with valid amount/funds."""
        checking_account.freeze()
        result = checking_account.transfer(10, today=today)
        assert result["success"] is False
        assert "frozen" in result["error"]

    def test_dt_closed_account_fails(self, checking_account, today):
        """DT1 (Closed variant): Closed account rejects transfer just like Frozen."""
        checking_account.close()
        result = checking_account.transfer(10, today=today)
        assert result["success"] is False
        assert "closed" in result["error"]


class TestMonthlyFeeDecisionTable:
    def test_dt2_r1_savings_above_waiver_fee_waived(self):
        """DT2-R1: Savings, balance above waiver threshold -> fee waived."""
        account = BankAccount("Savings", 1500)
        result = account.apply_monthly_fee()
        assert result["success"] is True
        assert result["charged"] == 0.0

    def test_dt2_r2_savings_below_waiver_sufficient_fee_charged(self):
        """DT2-R2: Savings, balance below waiver but enough to cover fee -> fee charged."""
        account = BankAccount("Savings", 500)
        result = account.apply_monthly_fee()
        assert result["success"] is True
        assert result["charged"] == 5
        assert account.balance == 495

    def test_dt2_r3_checking_above_waiver_fee_waived(self):
        """DT2-R3: Checking, balance above waiver threshold -> fee waived."""
        account = BankAccount("Checking", 6000)
        result = account.apply_monthly_fee()
        assert result["success"] is True
        assert result["charged"] == 0.0

    def test_dt2_r4_checking_below_waiver_insufficient_suspends(self):
        """DT2-R4: Checking, balance below waiver and below fee amount -> fails, suspends."""
        account = BankAccount("Checking", 5)
        result = account.apply_monthly_fee()
        assert result["success"] is False
        assert account.state == "Suspended"

    def test_dt2_r5_premium_never_charged(self):
        """DT2-R5: Premium account has a $0 monthly fee regardless of balance."""
        account = BankAccount("Premium", 10000)
        result = account.apply_monthly_fee()
        assert result["success"] is True
        assert result["charged"] == 0.0
        assert account.balance == 10000


class TestBillPaymentValidationDecisionTable:
    def test_dt3_r1_active_valid_payee_positive_sufficient_succeeds(
        self, checking_account
    ):
        """DT3-R1: Active account, valid payee, positive amount, sufficient funds -> succeeds."""
        result = validate_bill_payment(checking_account, "Electric Co", 100)
        assert result["success"] is True

    def test_dt3_r2_frozen_account_fails(self, checking_account):
        """DT3-R2: Frozen account rejects the payment regardless of other conditions."""
        checking_account.freeze()
        result = validate_bill_payment(checking_account, "Electric Co", 100)
        assert result["success"] is False
        assert "frozen" in result["error"]

    def test_dt3_r3_invalid_payee_fails(self, checking_account):
        """DT3-R3: Active account with an empty payee is rejected."""
        result = validate_bill_payment(checking_account, "", 100)
        assert result["success"] is False
        assert "Invalid payee" in result["error"]

    def test_dt3_r4_non_positive_amount_fails(self, checking_account):
        """DT3-R4: Active account, valid payee, non-positive amount is rejected."""
        result = validate_bill_payment(checking_account, "Electric Co", 0)
        assert result["success"] is False
        assert "must be positive" in result["error"]

    def test_dt3_r5_insufficient_funds_fails(self, today):
        """DT3-R5: Active account, valid payee, positive amount exceeding balance is rejected."""
        account = BankAccount("Checking", 50, today=today)
        result = validate_bill_payment(account, "Electric Co", 100)
        assert result["success"] is False
        assert "Insufficient funds" in result["error"]
