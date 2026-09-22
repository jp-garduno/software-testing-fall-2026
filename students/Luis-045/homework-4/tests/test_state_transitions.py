"""State Transition tests for SecureBank."""

from src.banking_system import BankAccount


class TestStateTransitions:
    """Tests for SecureBank account state transitions."""

    def test_active_to_suspended(self):
        """ST1: Active account becomes Suspended below minimum balance."""
        account = BankAccount("Savings", 150)

        result = account.transfer(60)

        assert result["success"] is True
        assert account.balance == 90
        assert account.state == "Suspended"

    def test_suspended_to_active(self):
        """ST2: Suspended account returns to Active after restoring balance."""
        account = BankAccount("Savings", 150)
        account.transfer(60)

        result = account.deposit(20)

        assert result["success"] is True
        assert account.balance == 110
        assert account.state == "Active"

    def test_active_to_frozen(self):
        """ST3: Active account becomes Frozen after freeze request."""
        account = BankAccount("Checking", 5000)

        result = account.freeze()

        assert result is True
        assert account.state == "Frozen"

    def test_frozen_to_active(self):
        """ST4: Frozen account returns to Active after unfreeze."""
        account = BankAccount("Checking", 5000)
        account.freeze()

        result = account.unfreeze()

        assert result is True
        assert account.state == "Active"

    def test_active_to_closed(self):
        """ST5: Active account becomes Closed after close request."""
        account = BankAccount("Checking", 5000)

        result = account.close()

        assert result is True
        assert account.state == "Closed"

    def test_closed_account_remains_closed(self):
        """ST6: Closed account cannot perform transactions or reopen."""
        account = BankAccount("Checking", 5000)
        account.close()

        result = account.deposit(1000)

        assert result["success"] is False
        assert "closed" in result["error"].lower()
        assert account.state == "Closed"