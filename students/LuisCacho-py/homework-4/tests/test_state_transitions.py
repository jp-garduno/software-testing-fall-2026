"""
State Transition Tests — SecureBank Online Banking System.

Tests based on the state transition diagram and table in:
  design/test-design-document.md — Section 1.4

States: Active, Frozen, Suspended, Closed
Valid transitions are tested as well as invalid/impossible transitions.

Technique: State Transition Testing (ST)
  Each test references its ST ID (ST-xx).
"""

import pytest

from src.banking_system import AccountState, AccountType, BankAccount


class TestActiveStateTransitions:
    """ST — Transitions OUT of Active state."""

    def test_st01_active_to_suspended_via_low_balance(self, savings_account):
        """ST-01: Active → Suspended when transfer causes balance to drop below $100."""
        # savings_account starts at $500
        result = savings_account.transfer(450.00)  # leaves $50 (below $100 min)
        assert result["success"] is True
        assert savings_account.state == AccountState.SUSPENDED

    def test_st02_active_to_frozen_via_freeze_request(self, checking_account):
        """ST-02: Active → Frozen via freeze() call (customer/fraud request)."""
        result = checking_account.freeze()
        assert result["success"] is True
        assert checking_account.state == AccountState.FROZEN

    def test_st03_active_to_closed_via_close_request(self, checking_account):
        """ST-03: Active → Closed via close() call."""
        result = checking_account.close()
        assert result["success"] is True
        assert checking_account.state == AccountState.CLOSED

    def test_st04_active_remains_active_after_normal_transfer(self, savings_account):
        """ST-04: Active stays Active when balance remains above minimum after transfer."""
        result = savings_account.transfer(100.00)  # $500 - $100 = $400 (still ≥ $100)
        assert result["success"] is True
        assert savings_account.state == AccountState.ACTIVE


class TestSuspendedStateTransitions:
    """ST — Transitions OUT of Suspended state."""

    def test_st05_suspended_to_active_via_deposit(self, suspended_savings):
        """ST-05: Suspended → Active when deposit restores balance above $100."""
        assert suspended_savings.state == AccountState.SUSPENDED
        result = suspended_savings.deposit(100.00)  # $50 + $100 = $150 ≥ $100
        assert result["success"] is True
        assert suspended_savings.state == AccountState.ACTIVE

    def test_st06_suspended_to_closed_via_close_request(self, suspended_savings):
        """ST-06: Suspended → Closed via close() (any state can be closed)."""
        result = suspended_savings.close()
        assert result["success"] is True
        assert suspended_savings.state == AccountState.CLOSED

    def test_st07_suspended_blocks_transfers(self, suspended_savings):
        """ST-07: Suspended account allows transfers (state != Frozen/Closed), but
        insufficient funds still blocks (no balance to transfer)."""
        # Suspended accounts can attempt transfers but balance is too low
        result = suspended_savings.transfer(100.00)
        # Either blocked by state or by insufficient funds — system must reject
        assert result["success"] is False

    def test_st08_suspended_stays_suspended_if_deposit_insufficient(self, suspended_savings):
        """ST-08: Suspended stays Suspended when deposit is positive but still < $100."""
        suspended_savings.deposit(10.00)  # now $60 — still below $100
        assert suspended_savings.state == AccountState.SUSPENDED


class TestFrozenStateTransitions:
    """ST — Transitions OUT of Frozen state."""

    def test_st09_frozen_to_active_via_unfreeze(self, frozen_account):
        """ST-09: Frozen → Active via unfreeze() when balance meets minimum."""
        result = frozen_account.unfreeze()
        assert result["success"] is True
        assert frozen_account.state == AccountState.ACTIVE

    def test_st10_frozen_to_closed_via_close_request(self, frozen_account):
        """ST-10: Frozen → Closed via close()."""
        result = frozen_account.close()
        assert result["success"] is True
        assert frozen_account.state == AccountState.CLOSED

    def test_st11_frozen_blocks_all_transfers(self, frozen_account):
        """ST-11: Frozen account rejects all transfer attempts."""
        result = frozen_account.transfer(50.00)
        assert result["success"] is False
        assert "frozen" in result["error"].lower()

    def test_st12_frozen_blocks_bill_payment(self, frozen_account):
        """ST-12: Frozen account rejects bill payment attempts."""
        result = frozen_account.pay_bill("Utility Co", 50.00)
        assert result["success"] is False
        assert "frozen" in result["error"].lower()


class TestClosedStateTransitions:
    """ST — Closed state is terminal (no transitions out)."""

    def test_st13_closed_rejects_transfer(self, closed_account):
        """ST-13: Closed account rejects transfer — Closed is terminal."""
        result = closed_account.transfer(10.00)
        assert result["success"] is False
        assert "closed" in result["error"].lower()

    def test_st14_closed_rejects_deposit(self, closed_account):
        """ST-14: Closed account rejects deposit — Closed is terminal."""
        result = closed_account.deposit(100.00)
        assert result["success"] is False
        assert "closed" in result["error"].lower()

    def test_st15_closed_cannot_be_closed_again(self, closed_account):
        """ST-15: Closing an already-Closed account returns an error."""
        result = closed_account.close()
        assert result["success"] is False
        assert "already" in result["error"].lower()

    def test_st16_closed_cannot_be_frozen(self, closed_account):
        """ST-16: Freezing a Closed account is not allowed."""
        result = closed_account.freeze()
        assert result["success"] is False


class TestComplexStateSequences:
    """ST — Multi-step state transition sequences."""

    def test_st17_active_freeze_unfreeze_back_to_active(self, checking_account):
        """ST-17: Active → Frozen → Active (full freeze/unfreeze cycle)."""
        checking_account.freeze()
        assert checking_account.state == AccountState.FROZEN

        checking_account.unfreeze()
        assert checking_account.state == AccountState.ACTIVE

        # Should be fully operational again
        result = checking_account.transfer(100.00)
        assert result["success"] is True

    def test_st18_active_suspended_active_sequence(self, savings_account):
        """ST-18: Active → Suspended (transfer) → Active (deposit) full cycle."""
        savings_account.transfer(450.00)  # drops to $50 → Suspended
        assert savings_account.state == AccountState.SUSPENDED

        savings_account.deposit(200.00)  # $50 + $200 = $250 → Active
        assert savings_account.state == AccountState.ACTIVE

    def test_st19_fee_insufficient_causes_suspension(self):
        """ST-19: Fee processing on low-balance account → Account suspended."""
        # $8 balance, $10 Checking fee
        account = BankAccount(AccountType.CHECKING, 8.00)
        result = account.process_monthly_fee()
        assert result.get("suspended") is True
        assert account.state == AccountState.SUSPENDED
