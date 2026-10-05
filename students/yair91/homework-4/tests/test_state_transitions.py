"""State transition tests.

Ids match the transition table in ``design/test-design-document.md``. Every
valid transition is exercised once, and the invalid ones are exercised to
prove the system refuses them rather than silently allowing them.
"""

from src.banking_system import BankAccount


class TestValidTransitions:
    """Transitions the state machine is supposed to allow."""

    def test_active_to_suspended_on_low_balance(self):
        """ST1: Active -> Suspended when a transfer drops below the minimum."""
        account = BankAccount("Savings", 150.0)
        result = account.transfer(60)
        assert account.state == "Suspended"
        assert result["warning"] == "Balance below minimum"

    def test_suspended_to_active_on_deposit(self):
        """ST2: Suspended -> Active once a deposit restores the minimum."""
        account = BankAccount("Savings", 150.0)
        account.transfer(60)
        assert account.state == "Suspended"
        account.deposit(100)
        assert account.state == "Active"
        assert account.balance == 190.00

    def test_active_to_frozen_on_request(self, checking_account):
        """ST3: Active -> Frozen by customer request or fraud detection."""
        assert checking_account.freeze()["success"] is True
        assert checking_account.state == "Frozen"

    def test_frozen_to_active_on_unfreeze(self, checking_account):
        """ST4: Frozen -> Active when the freeze is lifted."""
        checking_account.freeze()
        assert checking_account.unfreeze()["success"] is True
        assert checking_account.state == "Active"

    def test_active_to_closed_on_request(self, checking_account):
        """ST5: Active -> Closed, with a final statement."""
        result = checking_account.close()
        assert result["success"] is True
        assert result["final_statement"] is True
        assert checking_account.state == "Closed"

    def test_suspended_to_closed_on_request(self):
        """ST6: Suspended -> Closed is allowed."""
        account = BankAccount("Savings", 150.0)
        account.transfer(60)
        assert account.close()["success"] is True
        assert account.state == "Closed"

    def test_frozen_to_closed_on_request(self, checking_account):
        """ST7: Frozen -> Closed is allowed."""
        checking_account.freeze()
        assert checking_account.close()["success"] is True
        assert checking_account.state == "Closed"

    def test_active_to_suspended_when_the_fee_cannot_be_paid(self):
        """ST8: Active -> Suspended when the monthly fee has no funds behind it."""
        account = BankAccount("Savings", 4.0)
        account.apply_monthly_fee()
        assert account.state == "Suspended"

    def test_unfreeze_re_evaluates_the_balance(self):
        """ST9: Frozen -> Suspended when the balance is under the minimum."""
        account = BankAccount("Savings", 50.0, state="Frozen")
        account.unfreeze()
        assert account.state == "Suspended"


class TestInvalidTransitions:
    """Transitions the state machine must refuse."""

    def test_closed_account_refuses_transfers(self, checking_account):
        """ST10: Closed accounts reject every transaction."""
        checking_account.close()
        result = checking_account.transfer(10)
        assert result["success"] is False
        assert result["error"] == "Account is closed"

    def test_closed_account_cannot_be_reopened(self, checking_account):
        """ST11: a closed account cannot be unfrozen back into service."""
        checking_account.close()
        assert checking_account.unfreeze()["success"] is False
        assert checking_account.state == "Closed"

    def test_closed_account_cannot_be_closed_twice(self, checking_account):
        """ST12: closing an already closed account is an error, not a no-op."""
        checking_account.close()
        assert checking_account.close()["success"] is False

    def test_closed_account_cannot_be_frozen(self, checking_account):
        """ST13: Closed is terminal, freezing does not move it."""
        checking_account.close()
        assert checking_account.freeze()["success"] is False
        assert checking_account.state == "Closed"

    def test_frozen_account_refuses_transfers(self, checking_account):
        """ST14: Frozen blocks money movement but not viewing."""
        checking_account.freeze()
        result = checking_account.transfer(10)
        assert result["success"] is False
        assert result["error"] == "Account is frozen"
        assert checking_account.balance == 10000.00

    def test_frozen_account_refuses_deposits(self, checking_account):
        """ST15: a frozen account cannot be topped up either."""
        checking_account.freeze()
        assert checking_account.deposit(500)["success"] is False

    def test_unfreeze_on_an_active_account_is_rejected(self, checking_account):
        """ST16: there is no Active -> Active transition through unfreeze."""
        assert checking_account.unfreeze()["success"] is False


class TestSuspendedBehaviour:
    """Suspended keeps operating: the brief calls for warnings, not a block."""

    def test_suspended_account_still_transfers_with_a_warning(self):
        """ST17: Suspended -> Suspended, the transfer goes through warned."""
        account = BankAccount("Savings", 150.0)
        account.transfer(60)
        result = account.transfer(10)
        assert result["success"] is True
        assert result["warning"] == "Balance below minimum"
        assert account.state == "Suspended"
