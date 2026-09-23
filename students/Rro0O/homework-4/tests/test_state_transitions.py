"""State transition tests (design: design/test-design-document.md, section 4)."""

import pytest


class TestValidTransitions:
    """Valid transitions of the account state machine (ST1-ST13)."""

    def test_st1_active_to_suspended_by_transfer(self, make_account):
        """ST1: Savings $150 -> transfer $60 leaves $90 < $100 -> Suspended with warning."""
        account = make_account("Savings", 150)
        result = account.transfer(60)
        assert account.state == "Suspended"
        assert "suspended" in result["warning"]

    def test_st2_suspended_to_active_by_deposit(self, make_account):
        """ST2: Suspended Savings ($90) + $500 deposit -> Active."""
        account = make_account("Savings", 150)
        account.transfer(60)
        result = account.deposit(500)
        assert (account.state, account.balance, result["success"]) == ("Active", 590, True)

    def test_st3_suspended_stays_suspended_when_deposit_is_not_enough(self, make_account):
        """ST3: Suspended ($90) + $5 = $95 still < $100 -> remains Suspended (self loop)."""
        account = make_account("Savings", 150)
        account.transfer(60)
        account.deposit(5)
        assert (account.state, account.balance) == ("Suspended", 95)

    def test_st4_suspended_becomes_active_when_deposit_reaches_exact_minimum(self, make_account):
        """ST4: Suspended ($90) + $10 = $100 (== minimum) -> Active."""
        account = make_account("Savings", 150)
        account.transfer(60)
        account.deposit(10)
        assert account.state == "Active"

    def test_st5_active_to_frozen(self, checking):
        """ST5: freeze request on an Active account -> Frozen."""
        assert checking.freeze("fraud detection")["state"] == "Frozen"
        assert checking.state == "Frozen"

    def test_st6_frozen_to_active(self, checking):
        """ST6: unfreeze approved -> Active and transfers work again."""
        checking.freeze()
        checking.unfreeze()
        assert checking.state == "Active"
        assert checking.transfer(10)["success"] is True

    @pytest.mark.parametrize("prepare", ["active", "suspended", "frozen"])
    def test_st7_to_st9_any_open_state_to_closed(self, make_account, prepare):
        """ST7-ST9: close request from Active / Suspended / Frozen -> Closed with final statement."""
        account = make_account("Savings", 150)
        if prepare == "suspended":
            account.transfer(60)
        elif prepare == "frozen":
            account.freeze()
        result = account.close()
        assert account.state == "Closed"
        assert result["final_statement"]["final_balance"] == account.balance

    def test_st10_active_to_suspended_by_bill_payment(self, make_account, today):
        """ST10: a bill payment that breaks the minimum balance also suspends the account."""
        account = make_account("Savings", 150)
        account.pay_bill("CFE Electricity", 100, on_date=today)
        assert account.state == "Suspended"

    def test_st11_active_to_suspended_by_monthly_fee(self, make_account):
        """ST11: Checking $5 cannot pay the $10 fee -> Suspended."""
        account = make_account("Checking", 5)
        account.process_monthly_fee("2026-10-01")
        assert account.state == "Suspended"

    def test_st12_active_stays_active_when_balance_stays_above_minimum(self, make_account):
        """ST12: Active -> Active (self loop) when the balance remains >= minimum."""
        account = make_account("Savings", 500)
        account.transfer(100)
        assert account.state == "Active"

    def test_st13_frozen_account_can_still_be_viewed(self, checking):
        """ST13: Frozen is view-only, the balance can still be read."""
        checking.freeze()
        assert checking.get_balance() == 10000


class TestInvalidTransitions:
    """Events that must NOT change state (ST14-ST22)."""

    def test_st14_frozen_transfer_keeps_frozen(self, checking):
        """ST14: Frozen + transfer -> error, still Frozen."""
        checking.freeze()
        assert checking.transfer(10)["success"] is False
        assert checking.state == "Frozen"

    def test_st15_frozen_deposit_is_blocked(self, checking):
        """ST15: Frozen + deposit -> error, balance unchanged."""
        checking.freeze()
        assert checking.deposit(10)["error"] == "Account is frozen"
        assert checking.balance == 10000

    def test_st16_active_cannot_be_unfrozen(self, checking):
        """ST16: unfreeze on an Active account is not a valid event."""
        result = checking.unfreeze()
        assert result["success"] is False
        assert checking.state == "Active"

    def test_st17_suspended_cannot_be_frozen(self, make_account):
        """ST17: the state model has no Suspended -> Frozen transition."""
        account = make_account("Savings", 150)
        account.transfer(60)
        assert account.freeze()["success"] is False
        assert account.state == "Suspended"

    def test_st18_frozen_cannot_be_frozen_again(self, checking):
        """ST18: freezing twice is rejected."""
        checking.freeze()
        assert checking.freeze()["success"] is False

    @pytest.mark.parametrize(
        "event",
        [
            lambda acc: acc.transfer(10),
            lambda acc: acc.deposit(10),
            lambda acc: acc.pay_bill("CFE Electricity", 10),
            lambda acc: acc.freeze(),
            lambda acc: acc.unfreeze(),
            lambda acc: acc.close(),
            lambda acc: acc.reopen(),
            lambda acc: acc.update_info(owner="Someone"),
            lambda acc: acc.process_monthly_fee("2026-10-01"),
        ],
        ids=["transfer", "deposit", "pay_bill", "freeze", "unfreeze", "close", "reopen", "update_info", "fee"],
    )
    def test_st19_closed_absorbs_every_event(self, checking, event):
        """ST19: Closed + any event -> error and the account stays Closed (no reopening)."""
        checking.close()
        balance = checking.balance
        result = event(checking)
        assert result["success"] is False
        assert checking.state == "Closed"
        assert checking.balance == balance

    def test_st20_reopen_on_open_account_is_also_rejected(self, checking):
        """ST20: reopen is only meaningful for Closed accounts, and those cannot be reopened."""
        assert checking.reopen()["error"] == "Account is not closed"

    def test_st21_full_lifecycle(self, make_account):
        """ST21: Active -> Suspended -> Active -> Frozen -> Active -> Closed."""
        account = make_account("Savings", 150)
        visited = [account.state]
        account.transfer(60)
        visited.append(account.state)
        account.deposit(200)
        visited.append(account.state)
        account.freeze()
        visited.append(account.state)
        account.unfreeze()
        visited.append(account.state)
        account.close()
        visited.append(account.state)
        assert visited == ["Active", "Suspended", "Active", "Frozen", "Active", "Closed"]


class TestHistoryAndInformation:
    """Supporting behaviour observed through the state machine (history / CSV / info)."""

    def test_st22_history_records_every_movement(self, make_account, today):
        """ST22: transfer, deposit, bill payment and fee all leave a history entry."""
        account = make_account("Checking", 1000)
        account.transfer(100, on_date=today)
        account.deposit(50, on_date=today)
        account.pay_bill("CFE Electricity", 25, on_date=today)
        account.process_monthly_fee("2026-10-01")
        assert [tx["type"] for tx in account.get_history()] == ["transfer", "deposit", "bill payment", "fee"]

    def test_st23_csv_export_contains_header_and_rows(self, make_account):
        """ST23: the CSV export has a header and one line per filtered transaction."""
        account = make_account("Checking", 1000)
        account.deposit(50, on_date="2026-09-10")
        account.deposit(70, on_date="2026-09-30")
        lines = account.export_csv("2026-09-01", "2026-09-15").splitlines()
        assert lines[0] == "date,type,amount,balance_after,description"
        assert lines[1] == "2026-09-10,deposit,50.00,1050.00,Deposit"
        assert len(lines) == 2

    def test_st24_closed_account_keeps_history_and_balance_visible(self, checking):
        """ST24: closing an account does not erase what can be viewed."""
        checking.deposit(5)
        checking.close()
        assert checking.get_balance() == 10005
        assert len(checking.get_history()) == 1

    def test_st25_update_info_is_allowed_while_frozen(self, checking):
        """ST25: updating personal data is not a monetary transaction, so Frozen accounts may do it."""
        checking.freeze()
        assert checking.update_info(email="me@example.com")["success"] is True
