"""DT: every rule in the transfer, fee and bill-payment tables."""

from datetime import timedelta
from decimal import Decimal
from itertools import product

import pytest


@pytest.mark.parametrize(
    "funds,limit,active",
    list(product([True, False], repeat=3)),
    ids=[f"DT-T{i}" for i in range(1, 9)],
)
def test_transfer_decision_rules(account, funds, limit, active):
    """DT-T1..8: all eight combinations; state > funds > limit error precedence."""
    bank = account(balance="20000" if funds else "5050")
    bank.transfer("4900")
    if not active:
        bank.freeze()
    amount = "100" if limit else "200"
    # Insufficient funds is obtained through a public bill payment.
    if not funds and active:
        bank.pay_bill("water", "100")
    elif not funds:
        bank.unfreeze()
        bank.pay_bill("water", "100")
        bank.freeze()
    before, history = bank.view_balance(), bank.history()
    if funds and limit and active:
        bank.transfer(amount)
        assert bank.view_balance() == before - Decimal(amount)
        assert bank.daily_transfer_total == 5000
    else:
        error = "Active" if not active else "funds" if not funds else "daily limit"
        with pytest.raises(ValueError, match=error):
            bank.transfer(amount)
        assert bank.view_balance() == before
        assert bank.history() == history
        assert bank.daily_transfer_total == 4900


@pytest.mark.parametrize(
    "kind,balance,day,fee,state",
    [
        ("Savings", "1001", 1, "0", "Active"),
        ("Savings", "1000", 1, "5", "Active"),
        ("Savings", "4", 1, "0", "Suspended"),
        ("Checking", "5001", 1, "0", "Active"),
        ("Checking", "5000", 1, "10", "Active"),
        ("Checking", "9.99", 1, "0", "Suspended"),
        ("Premium", "10000", 1, "0", "Active"),
        ("Checking", "100", 2, "0", "Active"),
        ("Savings", "100", 1, "5", "Suspended"),
        ("Checking", "10", 1, "10", "Active"),
    ],
    ids=[f"DT-F{i}" for i in range(1, 11)],
)
def test_monthly_fee_decision_rules(account, clock, kind, balance, day, fee, state):
    """DT-F1..10: type, waiver, funds, calendar and post-fee minimum decisions."""
    clock.now = clock.now.replace(day=day)
    bank = account(kind, balance)
    assert bank.process_monthly_fee() == Decimal(fee)
    assert bank.view_balance() == Decimal(balance) - Decimal(fee)
    assert bank.state == state
    assert bank.process_monthly_fee() == 0
    assert bank.view_balance() == Decimal(balance) - Decimal(fee)


@pytest.mark.parametrize(
    "active,payee_valid,positive,funds",
    list(product([True, False], repeat=4)),
    ids=[f"DT-P{i}" for i in range(1, 17)],
)
def test_bill_payment_decision_rules(account, active, payee_valid, positive, funds):
    """DT-P1..16: all 16 combinations; insufficient-funds condition is irrelevant for zero."""
    bank = account(balance="100" if funds else "1")
    if not active:
        bank.freeze()
    amount = "10" if positive else "0"
    payee = "water" if payee_valid else "unknown"
    before = bank.view_balance()
    if all((active, payee_valid, positive, funds)):
        assert bank.pay_bill(payee, amount)["success"]
        assert bank.view_balance() == 90
        assert bank.history()[0]["kind"] == "bill"
    else:
        error = (
            "Active"
            if not active
            else "positive" if not positive else "funds" if not funds else "payee"
        )
        with pytest.raises(ValueError, match=error):
            bank.pay_bill(payee, amount)
        assert bank.view_balance() == before
        assert not bank.history()


def test_future_payment_processed_once(account, clock):
    """DT-S1: schedule, wait, execute on due date and prevent duplicate execution."""
    bank = account()
    bank.pay_bill("water", "25", clock.now.date() + timedelta(days=1))
    assert bank.process_scheduled() == []
    assert bank.view_balance() == 10000
    clock.now += timedelta(days=1)
    assert bank.process_scheduled() == [{"success": True, "scheduled": False}]
    assert bank.view_balance() == 9975
    assert bank.process_scheduled() == []
    assert len(bank.history()) == 1


@pytest.mark.parametrize(
    "reason", ["funds", "frozen", "closed"], ids=["DT-S2", "DT-S3", "DT-S4"]
)
def test_scheduled_payment_revalidation(account, clock, reason):
    """DT-S2..4: changed funds/state prevent a scheduled debit; closure cancels."""
    bank = account(balance="100")
    bank.pay_bill("water", "90", clock.now.date() + timedelta(days=1))
    if reason == "funds":
        bank.transfer("20")
    elif reason == "frozen":
        bank.freeze()
    else:
        bank.close()
    before, history = bank.view_balance(), bank.history()
    clock.now += timedelta(days=1)
    results = bank.process_scheduled()
    assert results == [] if reason == "closed" else results[0]["success"] is False
    assert bank.view_balance() == before
    assert bank.history() == history
