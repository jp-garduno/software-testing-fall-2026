"""BV: cent precision, transfer caps, balance thresholds and calendar boundaries."""

from datetime import timedelta
from decimal import Decimal

import pytest


@pytest.mark.parametrize(
    "kind,amount,valid",
    [
        ("Checking", "0", False),
        ("Checking", "0.01", True),
        ("Checking", "4999.99", True),
        ("Checking", "5000", True),
        ("Checking", "5000.01", False),
        ("Checking", "10000", False),
        ("Savings", "0", False),
        ("Savings", "0.01", True),
        ("Savings", "1999.99", True),
        ("Savings", "2000", True),
        ("Savings", "2000.01", False),
        ("Savings", "4000", False),
    ],
    ids=[f"BV-A{i}" for i in range(1, 13)],
)
def test_transfer_limit_boundaries(account, kind, amount, valid):
    """BV-A1..12: six boundary representatives for each of two account types."""
    bank = account(kind)
    if valid:
        bank.transfer(amount)
        assert bank.view_balance() == 10000 - Decimal(amount)
        assert bank.daily_transfer_total == Decimal(amount)
    else:
        with pytest.raises(ValueError):
            bank.transfer(amount)
        assert bank.view_balance() == 10000
        assert bank.daily_transfer_total == 0


@pytest.mark.parametrize(
    "balance,state",
    [
        ("0", "Suspended"),
        ("99.99", "Suspended"),
        ("100", "Active"),
        ("100.01", "Active"),
        ("200", "Active"),
    ],
    ids=[f"BV-M{i}" for i in range(1, 6)],
)
def test_savings_minimum_boundary(account, balance, state):
    """BV-M1..5: minimum balance is inclusive at exactly 100 dollars."""
    bank = account("Savings", balance)
    assert bank.state == state
    assert bank.warning == (state == "Suspended")


@pytest.mark.parametrize(
    "balance,fee",
    [("999.99", "5"), ("1000", "5"), ("1000.01", "0"), ("1001", "0")],
    ids=[f"BV-F{i}" for i in range(1, 5)],
)
def test_savings_fee_waiver_boundary(account, balance, fee):
    """BV-F1..4: the account-type specification says strictly greater than 1000."""
    bank = account("Savings", balance)
    assert bank.process_monthly_fee() == Decimal(fee)
    assert bank.view_balance() == Decimal(balance) - Decimal(fee)


@pytest.mark.parametrize(
    "amount,valid",
    [("99.99", True), ("100", True), ("100.01", False), ("101", False)],
    ids=[f"BV-C{i}" for i in range(1, 5)],
)
def test_cumulative_daily_limit(account, amount, valid):
    """BV-C1..4: prior transfer of 4900 leaves exactly 100 of daily allowance."""
    bank = account()
    bank.transfer("4900")
    if valid:
        bank.transfer(amount)
        assert bank.daily_transfer_total == 4900 + Decimal(amount)
    else:
        with pytest.raises(ValueError, match="daily limit"):
            bank.transfer(amount)
        assert bank.daily_transfer_total == 4900
        assert bank.view_balance() == 5100


@pytest.mark.parametrize(
    "amount,valid",
    [("99.99", True), ("100", True), ("100.01", False), ("101", False)],
    ids=[f"BV-B{i}" for i in range(1, 5)],
)
def test_available_funds_boundary(account, amount, valid):
    """BV-B1..4: sufficient funds means balance >= amount, without overdraft."""
    bank = account(balance="100")
    if valid:
        bank.transfer(amount)
        assert bank.view_balance() == 100 - Decimal(amount)
    else:
        with pytest.raises(ValueError, match="funds"):
            bank.transfer(amount)
        assert bank.view_balance() == 100


@pytest.mark.parametrize(
    "seconds,allowed",
    [(-2, False), (-1, False), (0, True), (1, True)],
    ids=[f"BV-N{i}" for i in range(1, 5)],
)
def test_midnight_reset_boundary(account, clock, seconds, allowed):
    """BV-N1..4: two seconds before, one before, exactly at and after midnight."""
    bank = account()
    bank.transfer("5000")
    midnight = clock.now.replace(hour=0, minute=0, second=0) + timedelta(days=1)
    clock.now = midnight + timedelta(seconds=seconds)
    if allowed:
        bank.transfer("0.01")
        assert bank.daily_transfer_total == Decimal("0.01")
    else:
        with pytest.raises(ValueError, match="daily limit"):
            bank.transfer("0.01")
        assert bank.daily_transfer_total == 5000


@pytest.mark.parametrize(
    "offset,valid,scheduled",
    [(-1, False, False), (0, True, False), (1, True, True), (30, True, True)],
    ids=[f"BV-P{i}" for i in range(1, 5)],
)
def test_payment_date_boundary(account, clock, offset, valid, scheduled):
    """BV-P1..4: yesterday, today, tomorrow and a later scheduled date."""
    bank = account()
    due = clock.now.date() + timedelta(days=offset)
    if valid:
        assert bank.pay_bill("water", "10", due)["scheduled"] == scheduled
        assert bank.view_balance() == (10000 if scheduled else 9990)
    else:
        with pytest.raises(ValueError, match="payment date"):
            bank.pay_bill("water", "10", due)
        assert bank.view_balance() == 10000
