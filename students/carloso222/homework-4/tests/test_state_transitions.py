from src.banking_system import BankAccount  # pylint: disable=import-error


class TestStateTransitions:
    def test_st1_active_to_suspended_when_transfer_drops_below_minimum(self):
        """ST1: Active -> Suspended when Savings balance drops below $100."""
        account = BankAccount("Savings", 150)
        result = account.transfer(60)
        assert result["success"] is True
        assert account.state == "Suspended"

    def test_st2_suspended_to_active_after_deposit_restores_minimum(self):
        """ST2: Suspended -> Active when deposit restores minimum balance."""
        account = BankAccount("Savings", 90)
        assert account.state == "Suspended"
        account.deposit(10)
        assert account.state == "Active"

    def test_st3_active_to_frozen(self):
        """ST3: Active -> Frozen after freeze request."""
        account = BankAccount("Checking", 1000)
        account.freeze()
        assert account.state == "Frozen"

    def test_st4_frozen_to_active_after_unfreeze(self):
        """ST4: Frozen -> Active after approved unfreeze with sufficient balance."""
        account = BankAccount("Checking", 1000)
        account.freeze()
        account.unfreeze()
        assert account.state == "Active"

    def test_st5_active_to_closed(self):
        """ST5: Active -> Closed after customer close request."""
        account = BankAccount("Checking", 1000)
        account.close()
        assert account.state == "Closed"

    def test_st6_suspended_to_closed(self):
        """ST6: Suspended -> Closed after close request."""
        account = BankAccount("Savings", 50)
        account.close()
        assert account.state == "Closed"

    def test_st7_frozen_to_closed(self):
        """ST7: Frozen -> Closed after close request."""
        account = BankAccount("Checking", 1000)
        account.freeze()
        account.close()
        assert account.state == "Closed"

    def test_st8_closed_cannot_reopen(self):
        """ST8: Closed remains Closed; reopening is forbidden."""
        account = BankAccount("Checking", 1000)
        account.close()
        result = account.reopen()
        assert result["success"] is False
        assert account.state == "Closed"

    def test_st9_closed_rejects_deposit(self):
        """ST9: Closed + deposit => remains Closed and rejects transaction."""
        account = BankAccount("Checking", 1000)
        account.close()
        result = account.deposit(100)
        assert result["success"] is False
        assert account.state == "Closed"
