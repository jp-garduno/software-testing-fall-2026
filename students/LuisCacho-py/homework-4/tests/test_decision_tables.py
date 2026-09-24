"""
Decision Table Tests — SecureBank Online Banking System.

Tests based on the decision tables in:
  design/test-design-document.md — Section 1.3

Decision tables model combinations of conditions and their expected actions.

Technique: Decision Tables (DT)
  Table 1: Transfer Validation       (8 rules)
  Table 2: Monthly Fee Processing    (5 rules)
  Table 3: Bill Payment Validation   (4 rules)
"""

import pytest

from src.banking_system import AccountState, AccountType, BankAccount


class TestTransferValidationDecisionTable:
    """
    DT-1 — Transfer Validation (3 conditions × 8 rules).

    Conditions:
      C1: Sufficient funds?   (Y/N)
      C2: Within daily limit? (Y/N)
      C3: Account Active?     (Y/N — Frozen or Closed counts as N)

    Rule mapping:
      Rule 1 (Y,Y,Y) → Transfer succeeds
      Rule 2 (Y,Y,N) → Error: Account not Active
      Rule 3 (Y,N,Y) → Error: Exceeds daily limit
      Rule 4 (Y,N,N) → Error: Account not Active (first check)
      Rule 5 (N,Y,Y) → Error: Insufficient funds
      Rule 6 (N,Y,N) → Error: Account not Active
      Rule 7 (N,N,Y) → Error: Insufficient funds (or limit)
      Rule 8 (N,N,N) → Error: Account not Active
    """

    def test_dt01_rule1_sufficient_within_limit_active_succeeds(self, checking_account):
        """DT-1 Rule 1: Y,Y,Y → Transfer succeeds."""
        result = checking_account.transfer(200.00)
        assert result["success"] is True

    def test_dt02_rule2_sufficient_within_limit_frozen_rejected(self, frozen_account):
        """DT-1 Rule 2: Y,Y,N (Frozen) → Error: Account is Frozen."""
        result = frozen_account.transfer(100.00)
        assert result["success"] is False
        assert "frozen" in result["error"].lower()

    def test_dt03_rule3_sufficient_exceeds_limit_active_rejected(self, high_balance_checking):
        """DT-1 Rule 3: Y,N,Y → Error: Exceeds daily limit."""
        result = high_balance_checking.transfer(6_000.00)  # exceeds $5,000
        assert result["success"] is False
        assert "limit" in result["error"].lower()

    def test_dt04_rule4_sufficient_exceeds_limit_frozen_rejected(self):
        """DT-1 Rule 4: Y,N,N → Error: Account is Frozen (checked first)."""
        account = BankAccount(AccountType.CHECKING, 10_000.00)
        account.freeze()
        result = account.transfer(6_000.00)
        assert result["success"] is False
        assert "frozen" in result["error"].lower()

    def test_dt05_rule5_insufficient_within_limit_active_rejected(self, checking_account):
        """DT-1 Rule 5: N,Y,Y → Error: Insufficient funds."""
        result = checking_account.transfer(checking_account.balance + 500.00)
        assert result["success"] is False
        assert "insufficient" in result["error"].lower()

    def test_dt06_rule6_insufficient_within_limit_frozen_rejected(self):
        """DT-1 Rule 6: N,Y,N (Frozen) → Error: Account is Frozen."""
        account = BankAccount(AccountType.CHECKING, 10.00)
        account.freeze()
        result = account.transfer(50.00)
        assert result["success"] is False
        assert "frozen" in result["error"].lower()

    def test_dt07_rule7_insufficient_exceeds_limit_active_rejected(self):
        """DT-1 Rule 7: N,N,Y → Error: Insufficient funds (balance checked before limit)."""
        account = BankAccount(AccountType.CHECKING, 10.00)
        result = account.transfer(6_000.00)
        # Insufficient funds is checked before daily limit in our implementation
        assert result["success"] is False

    def test_dt08_rule8_insufficient_exceeds_limit_closed_rejected(self, closed_account):
        """DT-1 Rule 8: N,N,N → Error: Account is Closed."""
        result = closed_account.transfer(10_000.00)
        assert result["success"] is False
        assert "closed" in result["error"].lower()


class TestMonthlyFeeProcessingDecisionTable:
    """
    DT-2 — Monthly Fee Processing (2 conditions × 5 rules).

    Conditions:
      C1: Account type (Savings / Checking / Premium)
      C2: Balance > waiver threshold? (Y/N/— for Premium)

    Rules:
      Rule 1: Savings, Y → Fee waived
      Rule 2: Savings, N → $5.00 fee charged
      Rule 3: Checking, Y → Fee waived
      Rule 4: Checking, N → $10.00 fee charged
      Rule 5: Premium, — → No fee (always free)
    """

    def test_dt09_rule1_savings_above_threshold_fee_waived(self):
        """DT-2 Rule 1: Savings, balance > $1,000 → $5 fee waived."""
        account = BankAccount(AccountType.SAVINGS, 1_500.00)
        result = account.process_monthly_fee()
        assert result["waived"] is True
        assert result["fee_charged"] == 0

    def test_dt10_rule2_savings_below_threshold_fee_charged(self):
        """DT-2 Rule 2: Savings, balance ≤ $1,000 → $5.00 fee charged."""
        account = BankAccount(AccountType.SAVINGS, 200.00)
        result = account.process_monthly_fee()
        assert result["waived"] is False
        assert result["fee_charged"] == 5.00

    def test_dt11_rule3_checking_above_threshold_fee_waived(self):
        """DT-2 Rule 3: Checking, balance > $5,000 → $10 fee waived."""
        account = BankAccount(AccountType.CHECKING, 6_000.00)
        result = account.process_monthly_fee()
        assert result["waived"] is True
        assert result["fee_charged"] == 0

    def test_dt12_rule4_checking_below_threshold_fee_charged(self):
        """DT-2 Rule 4: Checking, balance ≤ $5,000 → $10.00 fee charged."""
        account = BankAccount(AccountType.CHECKING, 1_000.00)
        result = account.process_monthly_fee()
        assert result["waived"] is False
        assert result["fee_charged"] == 10.00

    def test_dt13_rule5_premium_no_fee_ever(self, premium_account):
        """DT-2 Rule 5: Premium → $0 fee (always waived regardless of balance)."""
        result = premium_account.process_monthly_fee()
        assert result["fee_charged"] == 0
        assert result["waived"] is True


class TestBillPaymentValidationDecisionTable:
    """
    DT-3 — Bill Payment Validation (3 conditions × 4 rules).

    Conditions:
      C1: Valid payee? (Y/N)
      C2: Amount > 0? (Y/N)
      C3: Sufficient funds? (Y/N)

    Rules:
      Rule 1: Y,Y,Y → Payment succeeds
      Rule 2: Y,Y,N → Error: Insufficient funds
      Rule 3: Y,N,— → Error: Amount must be positive
      Rule 4: N,—,— → Error: Payee required
    """

    def test_dt14_rule1_valid_payee_positive_amount_sufficient_funds(self, checking_account):
        """DT-3 Rule 1: Y,Y,Y → Bill payment succeeds."""
        result = checking_account.pay_bill("Internet Provider", 75.00)
        assert result["success"] is True
        assert checking_account.balance == pytest.approx(925.00, abs=0.01)

    def test_dt15_rule2_valid_payee_positive_amount_insufficient_funds(self):
        """DT-3 Rule 2: Y,Y,N → Error: Insufficient funds."""
        account = BankAccount(AccountType.CHECKING, 10.00)
        result = account.pay_bill("Gas Company", 500.00)
        assert result["success"] is False
        assert "insufficient" in result["error"].lower()

    def test_dt16_rule3_valid_payee_zero_amount_rejected(self, checking_account):
        """DT-3 Rule 3: Y,N,— → Error: Amount must be positive."""
        result = checking_account.pay_bill("Water Company", 0.00)
        assert result["success"] is False
        assert "positive" in result["error"].lower()

    def test_dt17_rule4_empty_payee_rejected(self, checking_account):
        """DT-3 Rule 4: N,—,— → Error: Payee name is required."""
        result = checking_account.pay_bill("", 100.00)
        assert result["success"] is False
        assert "payee" in result["error"].lower()
