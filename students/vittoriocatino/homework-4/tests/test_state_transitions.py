"""Tests generated from the SecureBank state-transition model."""

from decimal import Decimal

from src.banking_system import AccountState, BankAccount


def test_st1_active_to_suspended_when_balance_drops_below_minimum() -> None:
    """ST1: a Savings transfer that crosses $100 suspends the account."""

    account = BankAccount("Savings", 150)
    result = account.transfer(60)
    assert result["success"] is True
    assert account.balance == Decimal("90.00")
    assert account.state is AccountState.SUSPENDED


def test_st2_suspended_to_active_after_restoring_balance() -> None:
    """ST2: a deposit restoring the minimum reactivates the account."""

    account = BankAccount("Savings", 100)
    account.process_monthly_fee()
    assert account.state is AccountState.SUSPENDED

    result = account.deposit(5)
    assert result["state"] == "Active"
    assert account.state is AccountState.ACTIVE


def test_st3_active_to_frozen_by_request(checking_account: BankAccount) -> None:
    """ST3: a customer or fraud request freezes an active account."""

    result = checking_account.freeze()
    assert result == {"success": True, "state": "Frozen"}


def test_st4_frozen_to_active_after_approval(checking_account: BankAccount) -> None:
    """ST4: approved unfreezing restores full access."""

    checking_account.freeze()
    result = checking_account.unfreeze()
    assert result == {"success": True, "state": "Active"}


def test_st5_active_to_closed_by_request(checking_account: BankAccount) -> None:
    """ST5: an active account can be closed by request."""

    assert checking_account.close() == {"success": True, "state": "Closed"}


def test_st6_suspended_to_closed_by_request() -> None:
    """ST6: a suspended account can be closed by request."""

    account = BankAccount("Savings", 100)
    account.process_monthly_fee()
    assert account.close()["state"] == "Closed"


def test_st7_frozen_to_closed_by_request(checking_account: BankAccount) -> None:
    """ST7: a frozen account can be closed by request."""

    checking_account.freeze()
    assert checking_account.close()["state"] == "Closed"


def test_st8_closed_account_cannot_be_reopened(checking_account: BankAccount) -> None:
    """ST8: Closed is terminal and an unfreeze event is invalid."""

    checking_account.close()
    result = checking_account.unfreeze()
    assert result == {"success": False, "error": "invalid_transition", "state": "Closed"}
    assert checking_account.state is AccountState.CLOSED


def test_st9_closed_account_rejects_transactions(checking_account: BankAccount) -> None:
    """ST9: a closed account rejects deposits, transfers, fees, and payments."""

    checking_account.close()
    assert checking_account.deposit(1)["error"] == "account_closed"
    assert checking_account.transfer(1)["error"] == "account_not_active"
    assert checking_account.pay_bill("Water", 1)["error"] == "account_not_active"
    assert checking_account.process_monthly_fee()["error"] == "account_closed"


def test_st10_invalid_freeze_does_not_change_frozen_state(
    checking_account: BankAccount,
) -> None:
    """ST10: freezing an already frozen account is an invalid transition."""

    checking_account.freeze()
    result = checking_account.freeze()
    assert result["error"] == "invalid_transition"
    assert checking_account.state is AccountState.FROZEN


def test_st11_closed_account_rejects_second_close(checking_account: BankAccount) -> None:
    """ST11: a repeated close request leaves the terminal state unchanged."""

    checking_account.close()
    result = checking_account.close()
    assert result == {"success": False, "error": "account_closed", "state": "Closed"}


def test_st12_daily_limit_resets_at_midnight(checking_account: BankAccount) -> None:
    """ST12: the accumulated transfer total returns to zero at midnight."""

    checking_account.transfer(200)
    checking_account.reset_daily_limit()
    assert checking_account.daily_transfer_total == Decimal("0.00")


def test_st13_deposit_keeps_active_account_active(checking_account: BankAccount) -> None:
    """ST13: a normal deposit does not change an Active account's state."""

    result = checking_account.deposit(25)
    assert result["success"] is True
    assert result["state"] == "Active"


def test_st14_zero_deposit_is_rejected_without_state_change(
    checking_account: BankAccount,
) -> None:
    """ST14: an invalid zero deposit leaves the Active state unchanged."""

    result = checking_account.deposit(0)
    assert result == {"success": False, "error": "amount_must_be_positive"}
    assert checking_account.state is AccountState.ACTIVE
