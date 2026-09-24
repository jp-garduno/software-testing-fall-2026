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
        """ST6: Closed account rejects transactions and remains Closed."""
        account = BankAccount("Checking", 5000)
        account.close()

        result = account.deposit(1000)

        assert result["success"] is False
        assert "closed" in result["error"].lower()
        assert account.state == "Closed"

    def test_deposit_to_frozen_account(self):
        """ST7: Frozen account rejects deposits and remains Frozen."""
        account = BankAccount("Checking", 1000)
        account.freeze()

        result = account.deposit(100)

        assert result["success"] is False
        assert "frozen" in result["error"].lower()
        assert account.state == "Frozen"

    def test_active_deposit_remains_active(self):
        """ST8: Deposit to Active account keeps account Active."""
        account = BankAccount("Savings", 500)

        result = account.deposit(100)

        assert result["success"] is True
        assert account.balance == 600
        assert account.state == "Active"

    def test_suspended_account_remains_suspended_below_minimum(self):
        """ST9: Insufficient deposit keeps account Suspended."""
        account = BankAccount("Savings", 150)
        account.transfer(60)

        result = account.deposit(5)

        assert result["success"] is True
        assert account.balance == 95
        assert account.state == "Suspended"

    def test_closed_account_cannot_be_frozen(self):
        """ST10: Closed account cannot transition to Frozen."""
        account = BankAccount("Checking", 1000)
        account.close()

        result = account.freeze()

        assert result is False
        assert account.state == "Closed"

    def test_active_account_cannot_be_unfrozen(self):
        """ST11: Active account cannot perform an unfreeze transition."""
        account = BankAccount("Checking", 1000)

        result = account.unfreeze()

        assert result is False
        assert account.state == "Active"