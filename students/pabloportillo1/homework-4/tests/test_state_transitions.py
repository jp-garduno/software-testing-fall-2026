"""State transition tests (design IDs ST1-ST12).

Covers every valid transition of section 4 plus the invalid transitions out of Closed.
"""

import pytest

from src.banking_system import ERR_CLOSED, ERR_FROZEN, ERR_INSUFFICIENT, WARN_BELOW_MINIMUM


class TestStateTransitions:
    """One test per row of the state transition test case table."""

    def test_st1_transfer_below_minimum_suspends_active_account(self, account_factory):
        """ST1: Active -> Suspended when a transfer leaves the balance under the minimum."""
        account = account_factory("Savings", 200.00)
        result = account.transfer(100.01)
        assert account.state == "Suspended"
        assert result["warnings"] == [WARN_BELOW_MINIMUM]
        assert account.balance == 99.99

    def test_st2_deposit_restores_suspended_account(self, account_factory):
        """ST2: Suspended -> Active when a deposit brings the balance back to the minimum."""
        account = account_factory("Savings", 50.00, state="Suspended")
        result = account.deposit(500.00)
        assert account.state == "Active"
        assert result["warnings"] == []

    def test_st3_deposit_below_minimum_keeps_account_suspended(self, account_factory):
        """ST3: Suspended -> Suspended when the deposit is not enough."""
        account = account_factory("Savings", 50.00, state="Suspended")
        result = account.deposit(10.00)
        assert account.state == "Suspended"
        assert result["warnings"] == [WARN_BELOW_MINIMUM]

    def test_st4_freeze_blocks_transfers(self, checking_account):
        """ST4: Active -> Frozen, after which money movement is refused."""
        checking_account.freeze()
        assert checking_account.state == "Frozen"
        assert checking_account.transfer(10.00)["error"] == ERR_FROZEN
        assert checking_account.deposit(10.00)["error"] == ERR_FROZEN

    def test_st5_unfreeze_above_minimum_returns_to_active(self, account_factory):
        """ST5: Frozen -> Active when the balance still meets the minimum."""
        account = account_factory("Savings", 500.00, state="Frozen")
        result = account.unfreeze()
        assert result["state"] == "Active"
        assert account.transfer(10.00)["success"] is True

    def test_st6_unfreeze_below_minimum_returns_to_suspended(self, account_factory):
        """ST6: Frozen -> Suspended; freezing must not wipe out the minimum-balance rule."""
        account = account_factory("Savings", 20.00, state="Frozen")
        result = account.unfreeze()
        assert result["state"] == "Suspended"
        assert account.state == "Suspended"

    def test_st7_frozen_account_can_be_closed(self, account_factory):
        """ST7: Frozen -> Closed, returning the final statement."""
        account = account_factory("Checking", 300.00, state="Frozen")
        result = account.close()
        assert account.state == "Closed"
        assert result["final_statement"].startswith("date,type,amount,counterparty")

    @pytest.mark.parametrize(
        "operation", ["transfer", "deposit", "close"], ids=["ST8-transfer", "ST8-deposit", "ST8-reopen"]
    )
    def test_st8_closed_account_rejects_every_event(self, account_factory, operation):
        """ST8: Closed -> Closed; a closed account cannot transact and cannot be reopened."""
        account = account_factory("Checking", 500.00, state="Closed")
        result = account.close() if operation == "close" else getattr(account, operation)(10.00)
        assert result["success"] is False
        assert result["error"] == ERR_CLOSED
        assert account.state == "Closed"

    def test_st9_unpayable_monthly_fee_suspends_account(self, account_factory):
        """ST9: Active -> Suspended when the monthly fee cannot be charged."""
        account = account_factory("Checking", 4.00)
        result = account.apply_monthly_fee()
        assert result["error"] == ERR_INSUFFICIENT
        assert account.state == "Suspended"
        assert account.balance == 4.00

    def test_st10_suspended_account_still_transfers(self, account_factory):
        """ST10: Suspended -> Suspended; the state warns but does not block."""
        account = account_factory("Savings", 80.00, state="Suspended")
        result = account.transfer(30.00)
        assert result["success"] is True
        assert account.state == "Suspended"

    def test_st11_close_active_account_generates_statement(self, account_with_history):
        """ST11: Active -> Closed with a CSV statement of the history."""
        result = account_with_history.close()
        assert account_with_history.state == "Closed"
        assert len(result["final_statement"].splitlines()) == 4

    def test_st12_transfer_to_exact_minimum_stays_active(self, account_factory):
        """ST12: Active -> Active at the boundary; landing exactly on the minimum is not a drop."""
        account = account_factory("Savings", 200.00)
        result = account.transfer(100.00)
        assert account.state == "Active"
        assert result["warnings"] == []
        assert account.notifications == []

    def test_freeze_and_close_are_refused_on_closed_accounts(self, account_factory):
        """ST8 (extra): no event may move an account out of Closed."""
        account = account_factory("Checking", 500.00, state="Closed")
        assert account.freeze()["error"] == ERR_CLOSED
        assert account.unfreeze()["error"] == ERR_CLOSED
        assert account.apply_monthly_fee()["error"] == ERR_CLOSED
        assert account.state == "Closed"

    def test_st13_unfreeze_is_rejected_on_a_non_frozen_account(self, checking_account):
        """ST13: unfreeze is not a valid event for an Active account."""
        result = checking_account.unfreeze()
        assert result["success"] is False
        assert result["error"] == "Account is not frozen"
        assert checking_account.state == "Active"
