"""ST: states are reached through public events, never assigned by tests."""

import pytest


def test_active_to_suspended_and_recovered(account):
    """ST1: spending below minimum suspends; deposit at minimum restores access."""
    bank = account("Savings", "100")
    bank.transfer("0.01")
    assert bank.state == "Suspended" and bank.warning
    with pytest.raises(ValueError, match="Active"):
        bank.transfer("0.01")
    bank.deposit("0.01")
    assert bank.state == "Active" and not bank.warning
    assert bank.view_balance() == 100


def test_frozen_to_active(account):
    """ST2: approved unfreeze restores transfers without changing the balance."""
    bank = account()
    bank.freeze()
    assert bank.state == "Frozen"
    assert bank.view_balance() == 10000
    bank.unfreeze()
    assert bank.state == "Active"
    bank.transfer("1")
    assert bank.view_balance() == 9999


@pytest.mark.parametrize(
    "initial",
    ["Active", "Frozen", "Suspended", "Closed"],
    ids=["ST3", "ST4", "ST5", "ST6"],
)
def test_close_from_every_state_is_permanent(account, initial):
    """ST3..6: closure is terminal from every state and provides a final statement."""
    bank = account("Savings", "50" if initial == "Suspended" else "1000")
    if initial == "Frozen":
        bank.freeze()
    if initial == "Closed":
        bank.close()
    statement = bank.close()
    assert bank.state == "Closed"
    assert statement == {"balance": bank.view_balance(), "transactions": bank.history()}
    for event in (
        lambda: bank.deposit("1"),
        lambda: bank.transfer("1"),
        bank.freeze,
        bank.unfreeze,
        lambda: bank.pay_bill("water", "1"),
        lambda: bank.update_info("D", "d@test"),
    ):
        with pytest.raises(ValueError):
            event()
        assert bank.state == "Closed"
        assert bank.view_balance() == statement["balance"]


def test_frozen_blocks_all_financial_operations(account):
    """ST7: frozen is read-only, including deposits and monthly fees."""
    bank = account(balance="100")
    bank.freeze()
    for event in (
        lambda: bank.transfer("1"),
        lambda: bank.deposit("1"),
        lambda: bank.pay_bill("water", "1"),
        lambda: bank.update_info("D", "d@test"),
    ):
        with pytest.raises(ValueError):
            event()
    assert bank.process_monthly_fee() == 0
    assert bank.view_balance() == 100
    assert bank.state == "Frozen" and not bank.history()


def test_insufficient_fee_suspends_then_deposit_recovers(account):
    """ST8: a failed fee suspends without overdraft; replenishment restores access."""
    bank = account(balance="5")
    assert bank.process_monthly_fee() == 0
    assert bank.state == "Suspended" and bank.warning
    assert bank.view_balance() == 5
    bank.deposit("10")
    assert bank.state == "Active" and not bank.warning


def test_partial_deposit_keeps_suspended(account):
    """ST9: a deposit that does not reach minimum cannot restore outgoing access."""
    bank = account("Savings", "50")
    bank.deposit("49.99")
    assert bank.state == "Suspended"
    with pytest.raises(ValueError):
        bank.freeze()
    with pytest.raises(ValueError):
        bank.unfreeze()


@pytest.mark.parametrize("amount", ["0", "-1", "bad"], ids=["ST10", "ST11", "ST12"])
def test_invalid_deposit_preserves_state(account, amount):
    """ST10..12: rejected deposits keep the observable state and ledger unchanged."""
    bank = account()
    with pytest.raises(ValueError):
        bank.deposit(amount)
    assert bank.state == "Active"
    assert bank.view_balance() == 10000
    assert not bank.history()
