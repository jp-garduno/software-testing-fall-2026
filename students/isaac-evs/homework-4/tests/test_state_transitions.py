"""State Transition tests — see design/test-design-document.md, Section 4."""

from src.banking_system import BankAccount


class TestValidStateTransitions:
    def test_st1_active_to_suspended_on_low_balance_transfer(self, today):
        """ST1: Active -> Suspended when a transfer drops the balance below the minimum."""
        account = BankAccount("Savings", 150, today=today)
        result = account.transfer(60, today=today)  # balance -> 90, below $100 min
        assert result["success"] is True
        assert account.state == "Suspended"

    def test_st2_suspended_to_active_on_deposit(self):
        """ST2: Suspended -> Active once a deposit restores the balance above the minimum."""
        account = BankAccount("Savings", 50)  # starts Suspended (below $100 min)
        assert account.state == "Suspended"
        result = account.deposit(100)
        assert result["success"] is True
        assert account.state == "Active"

    def test_st3_active_to_frozen(self, checking_account):
        """ST3: Active -> Frozen via freeze(), and further transfers are then rejected."""
        result = checking_account.freeze()
        assert result["success"] is True
        assert checking_account.state == "Frozen"

    def test_st4_frozen_to_active_when_balance_sufficient(self, checking_account):
        """ST4: Frozen -> Active via unfreeze() when the balance still meets the minimum."""
        checking_account.freeze()
        result = checking_account.unfreeze()
        assert result["success"] is True
        assert checking_account.state == "Active"

    def test_st5_frozen_to_suspended_when_balance_insufficient(self):
        """ST5: Frozen -> Suspended via unfreeze() when the balance is below the minimum."""
        account = BankAccount("Savings", 50)  # below $100 minimum
        account.freeze()
        result = account.unfreeze()
        assert result["success"] is True
        assert account.state == "Suspended"

    def test_st6_active_to_closed(self, checking_account):
        """ST6: Active -> Closed via close()."""
        result = checking_account.close()
        assert result["success"] is True
        assert checking_account.state == "Closed"

    def test_st7_suspended_to_closed(self):
        """ST7: Suspended -> Closed via close(), reachable from a non-Active state."""
        account = BankAccount("Savings", 50)
        assert account.state == "Suspended"
        result = account.close()
        assert result["success"] is True
        assert account.state == "Closed"


class TestInvalidStateTransitions:
    def test_st8_closed_account_rejects_transfer(self, checking_account, today):
        """ST8: Closed -> (transfer) stays Closed; the transfer is rejected."""
        checking_account.close()
        result = checking_account.transfer(10, today=today)
        assert result["success"] is False
        assert checking_account.state == "Closed"
        assert "closed" in result["error"]

    def test_st9_closing_an_already_closed_account_is_rejected(self, checking_account):
        """ST9: Closed -> (close again) is rejected, not a crash; state stays Closed."""
        checking_account.close()
        result = checking_account.close()
        assert result["success"] is False
        assert "already closed" in result["error"]
        assert checking_account.state == "Closed"

    def test_st10_refreezing_a_frozen_account_is_a_harmless_no_op(
        self, checking_account
    ):
        """ST10: Frozen -> (freeze again) succeeds as a no-op; state stays Frozen."""
        checking_account.freeze()
        result = checking_account.freeze()
        assert result["success"] is True
        assert checking_account.state == "Frozen"

    def test_st11_closed_account_rejects_deposit(self, checking_account):
        """ST11: Closed -> (deposit) stays Closed; the deposit is rejected."""
        checking_account.close()
        result = checking_account.deposit(100)
        assert result["success"] is False
        assert checking_account.state == "Closed"

    def test_st12_closed_account_rejects_freeze(self, checking_account):
        """ST12: Closed -> (freeze) stays Closed; freezing a closed account is rejected."""
        checking_account.close()
        result = checking_account.freeze()
        assert result["success"] is False
        assert "closed" in result["error"].lower()

    def test_st13_unfreeze_on_non_frozen_account_is_rejected(self, checking_account):
        """ST13: Active -> (unfreeze) is rejected; only a Frozen account can be unfrozen."""
        result = checking_account.unfreeze()
        assert result["success"] is False
        assert checking_account.state == "Active"

    def test_st14_closed_account_rejects_monthly_fee(self, checking_account):
        """ST14: Closed -> (apply_monthly_fee) stays Closed; no fee is charged."""
        checking_account.close()
        result = checking_account.apply_monthly_fee()
        assert result["success"] is False
        assert checking_account.state == "Closed"

    def test_st15_fee_charge_that_drops_balance_below_minimum_suspends(self):
        """ST15: Active -> Suspended when the monthly fee itself drops the balance below the minimum."""
        account = BankAccount(
            "Savings", 102
        )  # below waiver, fee ($5) leaves $97 < $100 min
        result = account.apply_monthly_fee()
        assert result["success"] is True
        assert account.balance == 97
        assert account.state == "Suspended"
