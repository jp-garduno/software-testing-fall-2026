from banking_system import BankAccount


class TestStateTransitions:

    def test_st1_active_to_suspended_on_low_balance(self):
        """ST1: Transfer causing balance < minimum -> Active becomes Suspended."""
        account = BankAccount("Savings", 200)
        account.transfer(150)  # 200 - 150 = 50, below $100 minimum
        assert account.state == "Suspended"

    def test_st2_suspended_to_active_on_deposit(self):
        """ST2: Deposit restoring balance above minimum -> Suspended becomes Active."""
        account = BankAccount("Savings", 200)
        account.transfer(150)  # now Suspended, balance = 50
        assert account.state == "Suspended"
        account.deposit(500)  # balance = 550, above $100 minimum
        assert account.state == "Active"

    def test_st3_active_to_frozen_on_freeze_request(self, checking_account):
        """ST3: Freeze request -> Active becomes Frozen."""
        checking_account.freeze()
        assert checking_account.state == "Frozen"

    def test_st5_active_to_closed_on_close_request(self, checking_account):
        """ST5: Close request -> Active becomes Closed."""
        checking_account.close()
        assert checking_account.state == "Closed"

    def test_st8_closed_account_rejects_transfer(self, checking_account):
        """ST8: Transfer attempt on a Closed account is rejected, state unchanged."""
        checking_account.close()
        result = checking_account.transfer(100)
        assert result["success"] is False
        assert checking_account.state == "Closed"