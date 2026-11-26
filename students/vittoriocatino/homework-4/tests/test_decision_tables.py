"""Tests generated from the three complete decision tables."""

from decimal import Decimal

import pytest

from src.banking_system import BankAccount


@pytest.mark.parametrize(
    ("active", "within_limit", "sufficient_funds", "expected"),
    [
        pytest.param(True, True, True, "success", id="DT1-R1"),
        pytest.param(False, True, True, "account_not_active", id="DT1-R2"),
        pytest.param(True, False, True, "exceeds_daily_limit", id="DT1-R3"),
        pytest.param(False, False, True, "account_not_active", id="DT1-R4"),
        pytest.param(True, True, False, "insufficient_funds", id="DT1-R5"),
        pytest.param(False, True, False, "account_not_active", id="DT1-R6"),
        pytest.param(True, False, False, "exceeds_daily_limit", id="DT1-R7"),
        pytest.param(False, False, False, "account_not_active", id="DT1-R8"),
    ],
)
def test_dt1_transfer_validation_rules(
    active: bool, within_limit: bool, sufficient_funds: bool, expected: str
) -> None:
    """DT1-R1..R8: every transfer decision-table combination is exercised."""

    account = BankAccount("Checking", 100 if sufficient_funds else 0)
    if not active:
        account.freeze()
    if not within_limit:
        account.daily_transfer_total = account.get_daily_limit()

    result = account.transfer(50)
    if expected == "success":
        assert result["success"] is True
    else:
        assert result == {
            "success": False,
            "error": expected,
            **({"state": "Frozen"} if expected == "account_not_active" else {}),
        }


@pytest.mark.parametrize(
    ("account_type", "balance", "waived", "fee"),
    [
        pytest.param("Savings", 1000.01, True, Decimal("0.00"), id="DT2-R1"),
        pytest.param("Savings", 1000.00, False, Decimal("5.00"), id="DT2-R2"),
        pytest.param("Checking", 5000.01, True, Decimal("0.00"), id="DT2-R3"),
        pytest.param("Checking", 5000.00, False, Decimal("10.00"), id="DT2-R4"),
        pytest.param("Premium", 10000.00, True, Decimal("0.00"), id="DT2-R5"),
    ],
)
def test_dt2_monthly_fee_rules(
    account_type: str, balance: float, waived: bool, fee: Decimal
) -> None:
    """DT2-R1..R5: type and threshold determine monthly-fee processing."""

    result = BankAccount(account_type, balance).process_monthly_fee()
    assert result["success"] is True
    assert result["waived"] is waived
    assert result["fee"] == fee


@pytest.mark.parametrize(
    ("valid_payee", "positive_amount", "sufficient_funds", "expected"),
    [
        pytest.param(True, True, True, "success", id="DT3-R1"),
        pytest.param(False, True, True, "invalid_payee", id="DT3-R2"),
        pytest.param(True, False, True, "amount_must_be_positive", id="DT3-R3"),
        pytest.param(False, False, True, "invalid_payee", id="DT3-R4"),
        pytest.param(True, True, False, "insufficient_funds", id="DT3-R5"),
        pytest.param(False, True, False, "invalid_payee", id="DT3-R6"),
        pytest.param(True, False, False, "amount_must_be_positive", id="DT3-R7"),
        pytest.param(False, False, False, "invalid_payee", id="DT3-R8"),
    ],
)
def test_dt3_bill_payment_rules(
    valid_payee: bool,
    positive_amount: bool,
    sufficient_funds: bool,
    expected: str,
) -> None:
    """DT3-R1..R8: every bill-payment condition combination is tested."""

    account = BankAccount("Checking", 100 if sufficient_funds else 0)
    payee = "Electricity" if valid_payee else ""
    amount = 50 if positive_amount else 0

    result = account.pay_bill(payee, amount)
    if expected == "success":
        assert result["success"] is True
    else:
        assert result["error"] == expected
