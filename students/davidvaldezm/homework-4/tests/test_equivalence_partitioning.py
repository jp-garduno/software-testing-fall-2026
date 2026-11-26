"""EP: partitions of amounts, account types, balances, payees and dates."""

import csv
import io
from datetime import date, timedelta
from decimal import Decimal

import pytest


@pytest.mark.parametrize(
    "amount,error",
    [
        ("500", None),
        ("0", "positive"),
        ("-100", "positive"),
        ("6000", "daily limit"),
        ("11000", "funds"),
        ("abc", "Invalid amount"),
        ("NaN", "Invalid amount"),
        ("Infinity", "Invalid amount"),
        ("0.001", "Invalid amount"),
        (True, "Invalid amount"),
    ],
    ids=[f"EP-A{i}" for i in range(1, 11)],
)
def test_transfer_amount_partition(account, amount, error):
    """EP-A1..10: valid, nonpositive, excessive, malformed and fractional amounts."""
    bank = account()
    if error:
        with pytest.raises(ValueError, match=error):
            bank.transfer(amount)
        assert bank.view_balance() == 10000
        assert bank.daily_transfer_total == 0
        assert bank.history() == []
    else:
        assert bank.transfer(amount) == {"success": True}
        assert bank.view_balance() == 9500
        assert bank.daily_transfer_total == 500
        assert len(bank.history()) == 1


@pytest.mark.parametrize(
    "kind,limit",
    [("Savings", 2000), ("Checking", 5000), ("Premium", 50000), ("Unknown", None)],
    ids=[f"EP-T{i}" for i in range(1, 5)],
)
def test_account_type_partition(account, kind, limit):
    """EP-T1..4: every supported type and an unsupported type."""
    if limit is None:
        with pytest.raises(ValueError, match="account type"):
            account(kind)
    else:
        assert account(kind).get_daily_limit() == limit


@pytest.mark.parametrize(
    "balance,state",
    [("-1", None), ("50", "Suspended"), ("500", "Active"), ("bad", None)],
    ids=[f"EP-B{i}" for i in range(1, 5)],
)
def test_initial_balance_partition(account, balance, state):
    """EP-B1..4: invalid, below-minimum and valid initial balances."""
    if state is None:
        with pytest.raises(ValueError):
            account("Savings", balance)
    else:
        bank = account("Savings", balance)
        assert bank.state == state
        assert bank.view_balance() == Decimal(balance)
        assert bank.warning == (state == "Suspended")


@pytest.mark.parametrize(
    "payee,valid",
    [
        ("water", True),
        ("electricity", True),
        ("credit_card", True),
        ("", False),
        ("unknown", False),
        (None, False),
    ],
    ids=[f"EP-P{i}" for i in range(1, 7)],
)
def test_payee_partition(account, payee, valid):
    """EP-P1..6: registered, empty, unknown and absent payees."""
    bank = account()
    if valid:
        assert bank.pay_bill(payee, "25")["success"]
        assert bank.view_balance() == 9975
    else:
        with pytest.raises(ValueError, match="payee"):
            bank.pay_bill(payee, "25")
        assert bank.view_balance() == 10000
        assert not bank.history()


@pytest.mark.parametrize(
    "start,end,count",
    [
        (None, None, 2),
        (date(2026, 9, 1), date(2026, 9, 1), 1),
        (date(2026, 9, 3), date(2026, 9, 4), 0),
        (date(2026, 9, 2), date(2026, 9, 1), None),
        ("bad", None, None),
        (None, date(2026, 9, 1), 1),
        (date(2026, 9, 2), None, 1),
    ],
    ids=[f"EP-D{i}" for i in range(1, 8)],
)
def test_history_date_partition(account, clock, start, end, count):
    """EP-D1..7: unbounded, inclusive, empty, inverted, malformed and open ranges."""
    bank = account()
    bank.transfer("10")
    clock.now += timedelta(days=1)
    bank.deposit("20")
    if count is None:
        with pytest.raises(ValueError, match="date range"):
            bank.history(start, end)
    else:
        rows = bank.history(start, end)
        assert len(rows) == count
        assert list(csv.DictReader(io.StringIO(bank.export_csv(start, end)))) == rows
        if rows:
            rows[0]["amount"] = "changed"
            assert bank.history()[0]["amount"] == "-10"


@pytest.mark.parametrize(
    "name,email,valid",
    [
        ("David", "d@example.test", True),
        ("", "d@example.test", False),
        ("David", "bad", False),
    ],
    ids=["EP-I1", "EP-I2", "EP-I3"],
)
def test_update_information_partition(account, name, email, valid):
    """EP-I1..3: valid and incomplete profile updates."""
    bank = account()
    if valid:
        bank.update_info(name, email)
        assert bank.info == {"name": name, "email": email}
    else:
        with pytest.raises(ValueError):
            bank.update_info(name, email)
        assert bank.info == {"name": "", "email": ""}


def test_transfer_between_own_accounts(account):
    """EP-R1: an own-account transfer conserves total funds and records both sides."""
    source, target = account(), account("Savings", "50")
    source.transfer("100", target)
    assert source.view_balance() == 9900
    assert target.view_balance() == 150
    assert target.state == "Active"
    assert len(source.history()) == len(target.history()) == 1


@pytest.mark.parametrize(
    "recipient_state", ["Frozen", "Closed", "self"], ids=["EP-R2", "EP-R3", "EP-R4"]
)
def test_invalid_recipient_is_atomic(account, recipient_state):
    """EP-R2..4: reject unavailable and identical recipients before any debit."""
    source, target = account(), account()
    if recipient_state == "Frozen":
        target.freeze()
    elif recipient_state == "Closed":
        target.close()
    else:
        target = source
    with pytest.raises(ValueError, match="recipient"):
        source.transfer("100", target)
    assert source.view_balance() == target.view_balance() == 10000
    assert source.daily_transfer_total == 0
    assert not source.history() and not target.history()
