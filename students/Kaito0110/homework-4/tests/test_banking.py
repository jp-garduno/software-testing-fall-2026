"""
Comprehensive black-box test suite for SecureBank Online Banking System.

Techniques applied:
- Equivalence Partitioning (EP)
- Boundary Value Analysis (BVA)
- Decision Tables (DT)
- State Transition Testing (ST)
"""

from datetime import date, timedelta

import pytest
from src.banking import AccountState, AccountType, BankAccount, BillPaymentService

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def savings_account():
    """Active savings account with $500 balance."""
    return BankAccount(
        "SA001", AccountType.SAVINGS, initial_balance=500.0, owner_name="Alice"
    )


@pytest.fixture
def checking_account():
    """Active checking account with $3000 balance."""
    return BankAccount(
        "CA001", AccountType.CHECKING, initial_balance=3000.0, owner_name="Bob"
    )


@pytest.fixture
def premium_account():
    """Active premium account with $15000 balance."""
    return BankAccount(
        "PA001", AccountType.PREMIUM, initial_balance=15000.0, owner_name="Carol"
    )


@pytest.fixture
def bill_service():
    """Bill payment service instance."""
    return BillPaymentService()


# ===========================================================================
# PART 1 — EQUIVALENCE PARTITIONING (EP)
# ===========================================================================


class TestEquivalencePartitioning:
    """Tests derived from Equivalence Partitioning analysis."""

    # --- EP: Transfer Amount ---

    def test_ep1_valid_transfer_amount(self, savings_account):
        """EP1: Valid amount within limits → transfer succeeds."""
        result = savings_account.transfer(500.00)
        assert result["success"] is True

    def test_ep2_zero_transfer_amount(self, savings_account):
        """EP2: Zero amount → Error: Amount must be positive."""
        result = savings_account.transfer(0.0)
        assert result["success"] is False
        assert "positive" in result["message"].lower()

    def test_ep3_negative_transfer_amount(self, savings_account):
        """EP3: Negative amount → Error: Amount must be positive."""
        result = savings_account.transfer(-100.0)
        assert result["success"] is False
        assert "positive" in result["message"].lower()

    def test_ep4_transfer_exceeds_daily_limit(self):
        """EP4: Amount exceeds daily limit → Error: Exceeds daily limit."""
        # Use an account with large balance so funds are not the limiting factor
        acc = BankAccount("EP4", AccountType.SAVINGS, initial_balance=200_000.0)
        result = acc.transfer(100_000.0)
        assert result["success"] is False
        assert "limit" in result["message"].lower()

    def test_ep5_transfer_exceeds_balance(self, savings_account):
        """EP5: Amount exceeds balance → Error: Insufficient funds."""
        result = savings_account.transfer(savings_account.balance + 1.0)
        assert result["success"] is False
        assert "insufficient" in result["message"].lower()

    # --- EP: Account Type ---

    def test_ep6_savings_account_valid_type(self):
        """EP6: SAVINGS is a valid account type."""
        acc = BankAccount("T1", AccountType.SAVINGS, initial_balance=500.0)
        assert acc.account_type == AccountType.SAVINGS

    def test_ep7_checking_account_valid_type(self):
        """EP7: CHECKING is a valid account type."""
        acc = BankAccount("T2", AccountType.CHECKING, initial_balance=100.0)
        assert acc.account_type == AccountType.CHECKING

    def test_ep8_premium_account_valid_type(self):
        """EP8: PREMIUM is a valid account type."""
        acc = BankAccount("T3", AccountType.PREMIUM, initial_balance=15000.0)
        assert acc.account_type == AccountType.PREMIUM

    # --- EP: Account Balance ---

    def test_ep9_balance_above_minimum_active(self):
        """EP9: Balance above minimum → account is Active."""
        acc = BankAccount("T4", AccountType.SAVINGS, initial_balance=500.0)
        assert acc.state == AccountState.ACTIVE

    def test_ep10_balance_below_minimum_suspended(self):
        """EP10: Balance below minimum → account is Suspended."""
        acc = BankAccount("T5", AccountType.SAVINGS, initial_balance=50.0)
        assert acc.state == AccountState.SUSPENDED

    def test_ep11_checking_zero_balance_active(self):
        """EP11: Checking with $0 balance → Active (no minimum)."""
        acc = BankAccount("T6", AccountType.CHECKING, initial_balance=0.0)
        assert acc.state == AccountState.ACTIVE

    # --- EP: Payee Information for Bill Payment ---

    def test_ep12_valid_payee(self, savings_account, bill_service):
        """EP12: Valid payee → bill payment succeeds."""
        result = bill_service.pay_bill(savings_account, "electric_company", 50.0)
        assert result["success"] is True

    def test_ep13_invalid_payee(self, savings_account, bill_service):
        """EP13: Invalid/unknown payee → Error: Invalid payee."""
        result = bill_service.pay_bill(savings_account, "random_payee", 50.0)
        assert result["success"] is False
        assert "invalid payee" in result["message"].lower()

    # --- EP: Date Range for Transaction History ---

    def test_ep14_valid_date_range(self, savings_account):
        """EP14: Valid date range (start <= end) → returns history."""
        savings_account.deposit(100.0)
        result = savings_account.get_transaction_history(
            start_date=date.today() - timedelta(days=30),
            end_date=date.today(),
        )
        assert result["success"] is True

    def test_ep15_invalid_date_range(self, savings_account):
        """EP15: Start date after end date → Error."""
        result = savings_account.get_transaction_history(
            start_date=date.today(),
            end_date=date.today() - timedelta(days=1),
        )
        assert result["success"] is False
        assert "start date" in result["message"].lower()

    def test_ep16_no_date_filter(self, savings_account):
        """EP16: No date filter → returns all transactions."""
        savings_account.deposit(10.0)
        result = savings_account.get_transaction_history()
        assert result["success"] is True
        assert len(result["data"]) >= 1


# ===========================================================================
# PART 2 — BOUNDARY VALUE ANALYSIS (BVA)
# ===========================================================================


class TestBoundaryValueAnalysis:
    """Tests derived from Boundary Value Analysis."""

    # --- BVA: Transfer Amount — Checking Account ($5,000 limit) ---

    def test_bv1_transfer_below_minimum(self, checking_account):
        """BV1: $0.00 → Error: Amount must be positive."""
        result = checking_account.transfer(0.00)
        assert result["success"] is False

    def test_bv2_transfer_at_minimum(self, checking_account):
        """BV2: $0.01 → Transfer succeeds."""
        result = checking_account.transfer(0.01)
        assert result["success"] is True

    def test_bv3_transfer_just_below_limit(self):
        """BV3: $4,999.99 → Transfer succeeds."""
        acc = BankAccount("BV3", AccountType.CHECKING, initial_balance=10000.0)
        result = acc.transfer(4999.99)
        assert result["success"] is True

    def test_bv4_transfer_at_limit(self):
        """BV4: $5,000.00 → Transfer succeeds."""
        acc = BankAccount("C2", AccountType.CHECKING, initial_balance=10000.0)
        result = acc.transfer(5000.00)
        assert result["success"] is True

    def test_bv5_transfer_just_above_limit(self):
        """BV5: $5,000.01 → Error: Exceeds daily limit."""
        acc = BankAccount("C3", AccountType.CHECKING, initial_balance=10000.0)
        result = acc.transfer(5000.01)
        assert result["success"] is False
        assert "limit" in result["message"].lower()

    def test_bv6_transfer_far_above_limit(self):
        """BV6: $10,000.00 → Error: Exceeds daily limit."""
        acc = BankAccount("C4", AccountType.CHECKING, initial_balance=20000.0)
        result = acc.transfer(10000.00)
        assert result["success"] is False
        assert "limit" in result["message"].lower()

    # --- BVA: Transfer Amount — Savings Account ($2,000 limit) ---

    def test_bv7_savings_transfer_just_below_limit(self):
        """BV7: $1,999.99 → Transfer succeeds (savings)."""
        acc = BankAccount("S2", AccountType.SAVINGS, initial_balance=5000.0)
        result = acc.transfer(1999.99)
        assert result["success"] is True

    def test_bv8_savings_transfer_at_limit(self):
        """BV8: $2,000.00 → Transfer succeeds (savings)."""
        acc = BankAccount("S3", AccountType.SAVINGS, initial_balance=5000.0)
        result = acc.transfer(2000.00)
        assert result["success"] is True

    def test_bv9_savings_transfer_just_above_limit(self):
        """BV9: $2,000.01 → Error: Exceeds daily limit (savings)."""
        acc = BankAccount("S4", AccountType.SAVINGS, initial_balance=5000.0)
        result = acc.transfer(2000.01)
        assert result["success"] is False
        assert "limit" in result["message"].lower()

    # --- BVA: Account Balance vs Minimum — Savings ($100 minimum) ---

    def test_bv10_balance_at_minimum(self):
        """BV10: Balance exactly $100 → Active state (savings)."""
        acc = BankAccount("S5", AccountType.SAVINGS, initial_balance=100.0)
        assert acc.state == AccountState.ACTIVE

    def test_bv11_balance_just_below_minimum(self):
        """BV11: Balance $99.99 → Suspended state (savings)."""
        acc = BankAccount("S6", AccountType.SAVINGS, initial_balance=99.99)
        assert acc.state == AccountState.SUSPENDED

    def test_bv12_balance_just_above_minimum(self):
        """BV12: Balance $100.01 → Active state (savings)."""
        acc = BankAccount("S7", AccountType.SAVINGS, initial_balance=100.01)
        assert acc.state == AccountState.ACTIVE

    # --- BVA: Fee Waiver — Savings ($1,000 threshold) ---

    def test_bv13_fee_waiver_above_threshold(self):
        """BV13: Balance $1,000.01 → fee waived (savings)."""
        acc = BankAccount("S8", AccountType.SAVINGS, initial_balance=1000.01)
        result = acc.apply_monthly_fee()
        assert result["success"] is True
        assert "waived" in result["message"].lower()

    def test_bv14_fee_waiver_at_threshold(self):
        """BV14: Balance exactly $1,000 → fee waived (savings)."""
        acc = BankAccount("S9", AccountType.SAVINGS, initial_balance=1000.0)
        result = acc.apply_monthly_fee()
        assert result["success"] is True
        assert "waived" in result["message"].lower()

    def test_bv15_fee_charged_below_threshold(self):
        """BV15: Balance $999.99 → fee charged (savings)."""
        acc = BankAccount("S10", AccountType.SAVINGS, initial_balance=999.99)
        result = acc.apply_monthly_fee()
        assert result["success"] is True
        assert "fee" in result["message"].lower()

    # --- BVA: Premium Account Minimum ($10,000) ---

    def test_bv16_premium_at_minimum(self):
        """BV16: Premium balance exactly $10,000 → Active."""
        acc = BankAccount("P1", AccountType.PREMIUM, initial_balance=10000.0)
        assert acc.state == AccountState.ACTIVE

    def test_bv17_premium_below_minimum(self):
        """BV17: Premium balance $9,999.99 → Suspended."""
        acc = BankAccount("P2", AccountType.PREMIUM, initial_balance=9999.99)
        assert acc.state == AccountState.SUSPENDED

    # --- BVA: Bill Payment Amount ---

    def test_bv18_bill_payment_zero_amount(self, savings_account, bill_service):
        """BV18: Bill payment with $0 → Error."""
        result = bill_service.pay_bill(savings_account, "electric_company", 0.0)
        assert result["success"] is False

    def test_bv19_bill_payment_positive_amount(self, savings_account, bill_service):
        """BV19: Bill payment with $0.01 → succeeds."""
        result = bill_service.pay_bill(savings_account, "electric_company", 0.01)
        assert result["success"] is True


# ===========================================================================
# PART 3 — DECISION TABLE TESTING (DT)
# ===========================================================================


class TestDecisionTables:
    """Tests derived from Decision Table analysis."""

    # Decision Table 1: Transfer Validation
    # Conditions: Sufficient Funds | Within Daily Limit | Account Active
    # -----------------------------------------------------------------------
    # Rule 1: Y | Y | Y  → Transfer succeeds
    # Rule 2: Y | Y | N  → Error: Account frozen/suspended
    # Rule 3: Y | N | Y  → Error: Exceeds limit
    # Rule 4: Y | N | N  → Error: Account frozen (takes priority)
    # Rule 5: N | Y | Y  → Error: Insufficient funds
    # Rule 6: N | Y | N  → Error: Account frozen
    # Rule 7: N | N | Y  → Error: Exceeds limit (checked after state)
    # Rule 8: N | N | N  → Error: Account frozen

    def test_dt1_rule1_all_conditions_met(self):
        """DT Rule 1: Funds OK + within limit + active → succeeds."""
        acc = BankAccount("DT1", AccountType.CHECKING, initial_balance=1000.0)
        result = acc.transfer(100.0)
        assert result["success"] is True

    def test_dt1_rule2_account_frozen(self):
        """DT Rule 2: Funds OK + within limit + frozen → account frozen error."""
        acc = BankAccount("DT2", AccountType.CHECKING, initial_balance=1000.0)
        acc.freeze()
        result = acc.transfer(100.0)
        assert result["success"] is False
        assert "frozen" in result["message"].lower()

    def test_dt1_rule3_exceeds_limit_active(self):
        """DT Rule 3: Funds OK + exceeds limit + active → limit error."""
        acc = BankAccount("DT3", AccountType.CHECKING, initial_balance=10000.0)
        result = acc.transfer(5001.0)
        assert result["success"] is False
        assert "limit" in result["message"].lower()

    def test_dt1_rule4_exceeds_limit_frozen(self):
        """DT Rule 4: Funds OK + exceeds limit + frozen → frozen error."""
        acc = BankAccount("DT4", AccountType.CHECKING, initial_balance=10000.0)
        acc.freeze()
        result = acc.transfer(5001.0)
        assert result["success"] is False
        assert "frozen" in result["message"].lower()

    def test_dt1_rule5_insufficient_funds_active(self):
        """DT Rule 5: Insufficient funds + within limit + active → insufficient error."""
        acc = BankAccount("DT5", AccountType.CHECKING, initial_balance=50.0)
        result = acc.transfer(100.0)
        assert result["success"] is False
        assert "insufficient" in result["message"].lower()

    def test_dt1_rule6_insufficient_funds_frozen(self):
        """DT Rule 6: Insufficient funds + within limit + frozen → frozen error."""
        acc = BankAccount("DT6", AccountType.CHECKING, initial_balance=50.0)
        acc.freeze()
        result = acc.transfer(30.0)
        assert result["success"] is False
        assert "frozen" in result["message"].lower()

    def test_dt1_rule7_insufficient_and_over_limit_active(self):
        """DT Rule 7: Insufficient + exceeds limit + active → state error first."""
        acc = BankAccount("DT7", AccountType.CHECKING, initial_balance=0.0)
        result = acc.transfer(6000.0)
        assert result["success"] is False

    def test_dt1_rule8_all_bad_frozen(self):
        """DT Rule 8: Insufficient + exceeds limit + frozen → frozen error."""
        acc = BankAccount("DT8", AccountType.CHECKING, initial_balance=0.0)
        acc.freeze()
        result = acc.transfer(6000.0)
        assert result["success"] is False
        assert "frozen" in result["message"].lower()

    # Decision Table 2: Monthly Fee Processing
    # Conditions: Account Type | Balance > Waiver Threshold
    # -----------------------------------------------------------------------
    # Rule 1: Savings | Y  → No fee charged
    # Rule 2: Savings | N  → $5 fee charged
    # Rule 3: Checking | Y → No fee charged
    # Rule 4: Checking | N → $10 fee charged
    # Rule 5: Premium  | - → No fee (always free)

    def test_dt2_rule1_savings_above_threshold(self):
        """DT2 Rule 1: Savings + balance > $1000 → fee waived."""
        acc = BankAccount("DT9", AccountType.SAVINGS, initial_balance=1500.0)
        result = acc.apply_monthly_fee()
        assert result["success"] is True
        assert "waived" in result["message"].lower()

    def test_dt2_rule2_savings_below_threshold(self):
        """DT2 Rule 2: Savings + balance < $1000 → $5 fee charged."""
        acc = BankAccount("DT10", AccountType.SAVINGS, initial_balance=500.0)
        balance_before = acc.balance
        result = acc.apply_monthly_fee()
        assert result["success"] is True
        assert acc.balance == balance_before - 5.0

    def test_dt2_rule3_checking_above_threshold(self):
        """DT2 Rule 3: Checking + balance > $5000 → fee waived."""
        acc = BankAccount("DT11", AccountType.CHECKING, initial_balance=6000.0)
        result = acc.apply_monthly_fee()
        assert result["success"] is True
        assert "waived" in result["message"].lower()

    def test_dt2_rule4_checking_below_threshold(self):
        """DT2 Rule 4: Checking + balance < $5000 → $10 fee charged."""
        acc = BankAccount("DT12", AccountType.CHECKING, initial_balance=3000.0)
        balance_before = acc.balance
        result = acc.apply_monthly_fee()
        assert result["success"] is True
        assert acc.balance == balance_before - 10.0

    def test_dt2_rule5_premium_no_fee(self):
        """DT2 Rule 5: Premium → no fee regardless of balance."""
        acc = BankAccount("DT13", AccountType.PREMIUM, initial_balance=15000.0)
        balance_before = acc.balance
        result = acc.apply_monthly_fee()
        assert result["success"] is True
        assert acc.balance == balance_before  # No deduction

    # Decision Table 3: Bill Payment Validation
    # Conditions: Valid Payee | Amount > 0 | Account Active | Sufficient Funds
    # -----------------------------------------------------------------------
    # Rule 1: Y | Y | Y | Y → Bill payment succeeds
    # Rule 2: Y | Y | N | Y → Error: Account frozen
    # Rule 3: Y | N | Y | - → Error: Amount must be positive
    # Rule 4: N | Y | Y | Y → Error: Invalid payee

    def test_dt3_rule1_valid_bill_payment(self, savings_account, bill_service):
        """DT3 Rule 1: Valid payee + amount > 0 + active + funds → succeeds."""
        result = bill_service.pay_bill(savings_account, "water_company", 75.0)
        assert result["success"] is True

    def test_dt3_rule2_frozen_account_bill(self, savings_account, bill_service):
        """DT3 Rule 2: Valid payee + amount > 0 + frozen → frozen error."""
        savings_account.freeze()
        result = bill_service.pay_bill(savings_account, "water_company", 75.0)
        assert result["success"] is False
        assert "frozen" in result["message"].lower()

    def test_dt3_rule3_zero_amount_bill(self, savings_account, bill_service):
        """DT3 Rule 3: Valid payee + amount = 0 + active → amount error."""
        result = bill_service.pay_bill(savings_account, "electric_company", 0.0)
        assert result["success"] is False
        assert "positive" in result["message"].lower()

    def test_dt3_rule4_invalid_payee_bill(self, savings_account, bill_service):
        """DT3 Rule 4: Invalid payee + amount > 0 + active → payee error."""
        result = bill_service.pay_bill(savings_account, "unknown_vendor", 50.0)
        assert result["success"] is False
        assert "invalid payee" in result["message"].lower()


# ===========================================================================
# PART 4 — STATE TRANSITION TESTING (ST)
# ===========================================================================


class TestStateTransitions:
    """Tests derived from State Transition analysis."""

    # State Diagram:
    # Active ---(balance < min)---> Suspended
    # Active ---(freeze request)---> Frozen
    # Active ---(close request)----> Closed
    # Suspended ---(deposit restores)---> Active
    # Suspended ---(close request)----> Closed
    # Frozen ---(unfreeze)-----------> Active
    # Frozen ---(close request)-------> Closed
    # Closed ---(any event)-----------  Error: Account closed

    def test_st1_active_to_suspended_on_low_balance(self):
        """ST1: Active + transfer causes balance < $100 → Suspended."""
        acc = BankAccount("ST1", AccountType.SAVINGS, initial_balance=150.0)
        assert acc.state == AccountState.ACTIVE
        acc.transfer(75.0)  # balance drops to $75 < $100 minimum
        assert acc.state == AccountState.SUSPENDED

    def test_st2_suspended_to_active_on_deposit(self):
        """ST2: Suspended + deposit restores balance → Active."""
        acc = BankAccount("ST2", AccountType.SAVINGS, initial_balance=50.0)
        assert acc.state == AccountState.SUSPENDED
        acc.deposit(500.0)
        assert acc.state == AccountState.ACTIVE

    def test_st3_active_to_frozen_on_freeze_request(self):
        """ST3: Active + freeze request → Frozen."""
        acc = BankAccount("ST3", AccountType.CHECKING, initial_balance=1000.0)
        assert acc.state == AccountState.ACTIVE
        result = acc.freeze()
        assert result["success"] is True
        assert acc.state == AccountState.FROZEN

    def test_st4_frozen_to_active_on_unfreeze(self):
        """ST4: Frozen + unfreeze approved → Active."""
        acc = BankAccount("ST4", AccountType.CHECKING, initial_balance=1000.0)
        acc.freeze()
        assert acc.state == AccountState.FROZEN
        result = acc.unfreeze()
        assert result["success"] is True
        assert acc.state == AccountState.ACTIVE

    def test_st5_active_to_closed(self):
        """ST5: Active + close request → Closed."""
        acc = BankAccount("ST5", AccountType.CHECKING, initial_balance=500.0)
        assert acc.state == AccountState.ACTIVE
        result = acc.close()
        assert result["success"] is True
        assert acc.state == AccountState.CLOSED

    def test_st6_suspended_to_closed(self):
        """ST6: Suspended + close request → Closed."""
        acc = BankAccount("ST6", AccountType.SAVINGS, initial_balance=50.0)
        assert acc.state == AccountState.SUSPENDED
        result = acc.close()
        assert result["success"] is True
        assert acc.state == AccountState.CLOSED

    def test_st7_frozen_to_closed(self):
        """ST7: Frozen + close request → Closed."""
        acc = BankAccount("ST7", AccountType.CHECKING, initial_balance=1000.0)
        acc.freeze()
        result = acc.close()
        assert result["success"] is True
        assert acc.state == AccountState.CLOSED

    def test_st8_closed_transfer_rejected(self):
        """ST8: Closed + transfer attempt → Error: Account closed."""
        acc = BankAccount("ST8", AccountType.CHECKING, initial_balance=500.0)
        acc.close()
        result = acc.transfer(100.0)
        assert result["success"] is False
        assert "closed" in result["message"].lower()

    def test_st9_closed_deposit_rejected(self):
        """ST9: Closed + deposit attempt → Error: Account closed."""
        acc = BankAccount("ST9", AccountType.CHECKING, initial_balance=500.0)
        acc.close()
        result = acc.deposit(100.0)
        assert result["success"] is False
        assert "closed" in result["message"].lower()

    def test_st10_closed_cannot_be_reopened(self):
        """ST10: Closed + close again → Error: Account already closed."""
        acc = BankAccount("ST10", AccountType.CHECKING, initial_balance=500.0)
        acc.close()
        result = acc.close()
        assert result["success"] is False
        assert "closed" in result["message"].lower()

    def test_st11_suspended_cannot_transfer(self):
        """ST11: Suspended + transfer attempt → Error: Account suspended."""
        acc = BankAccount("ST11", AccountType.SAVINGS, initial_balance=50.0)
        assert acc.state == AccountState.SUSPENDED
        result = acc.transfer(10.0)
        assert result["success"] is False
        assert "suspended" in result["message"].lower()

    def test_st12_fee_causes_suspension(self):
        """ST12: Active + fee with insufficient funds → Suspended."""
        acc = BankAccount("ST12", AccountType.SAVINGS, initial_balance=3.0)
        # Balance $3 < fee $5, so applying fee should suspend
        result = acc.apply_monthly_fee()
        assert result["success"] is False
        assert acc.state == AccountState.SUSPENDED

    # --- Additional scenario tests ---

    def test_scheduled_bill_payment_future_date(self, savings_account, bill_service):
        """Bill payment scheduled for future date → scheduled successfully."""
        future = date.today() + timedelta(days=5)
        result = bill_service.pay_bill(
            savings_account, "gas_company", 30.0, scheduled_date=future
        )
        assert result["success"] is True
        assert "scheduled" in result["message"].lower()

    def test_scheduled_bill_payment_past_date(self, savings_account, bill_service):
        """Bill payment with past scheduled date → Error."""
        past = date.today() - timedelta(days=1)
        result = bill_service.pay_bill(
            savings_account, "gas_company", 30.0, scheduled_date=past
        )
        assert result["success"] is False
        assert "past" in result["message"].lower()

    def test_daily_limit_cumulative(self):
        """Cumulative transfers respecting daily limit (checking $5,000)."""
        acc = BankAccount("CUM1", AccountType.CHECKING, initial_balance=10000.0)
        acc.transfer(3000.0)  # $3,000 used
        result = acc.transfer(2000.0)  # $5,000 total — at limit
        assert result["success"] is True
        result2 = acc.transfer(0.01)  # Exceeds limit
        assert result2["success"] is False
        assert "limit" in result2["message"].lower()

    def test_premium_large_transfer(self):
        """Premium account can transfer up to $50,000 per day."""
        acc = BankAccount("PR1", AccountType.PREMIUM, initial_balance=100000.0)
        result = acc.transfer(50000.0)
        assert result["success"] is True

    def test_unfreeze_non_frozen_account_error(self):
        """Attempt to unfreeze a non-frozen account → Error."""
        acc = BankAccount("UNF1", AccountType.CHECKING, initial_balance=1000.0)
        result = acc.unfreeze()
        assert result["success"] is False
        assert "not frozen" in result["message"].lower()
