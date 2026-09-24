"""Boundary Value Analysis - implementa design/test-design-document.md seccion 1.2.

Se implementan las fronteras criticas de BV1, BV3 y BV4.
"""

import pytest
from src.banking_system import ERRORS


def test_zero_is_below_minimum(make_account):
    """BV1-1: $0.00 esta bajo el minimo y es rechazado."""
    result = make_account("Checking", 20000).transfer(0.00)

    assert result["success"] is False
    assert result["error"] == ERRORS["AMOUNT_NOT_POSITIVE"]


def test_one_cent_is_minimum_valid(make_account):
    """BV1-2: $0.01 es el minimo valido y se acepta."""
    account = make_account("Checking", 20000)
    result = account.transfer(0.01)

    assert result["success"] is True
    assert account.balance == pytest.approx(19999.99)


def test_exactly_at_daily_limit(make_account):
    """BV1-4: $5,000.00 esta exactamente en el limite y se acepta."""
    account = make_account("Checking", 20000)
    result = account.transfer(5000.00)

    assert result["success"] is True
    assert account.daily_transfer_total == pytest.approx(5000)


def test_one_cent_over_daily_limit(make_account):
    """BV1-5: $5,000.01 supera el limite por un centavo y es rechazado."""
    result = make_account("Checking", 20000).transfer(5000.01)

    assert result["success"] is False
    assert result["error"] == ERRORS["EXCEEDS_DAILY_LIMIT"]


def test_balance_exactly_at_minimum_stays_active(make_account):
    """BV3-2: dejar el saldo exactamente en el minimo mantiene la cuenta Activa."""
    account = make_account("Savings", 500)
    account.transfer(400.00)

    assert account.balance == pytest.approx(100.00)
    assert account.state == "Active"


def test_one_cent_below_minimum_suspends(make_account):
    """BV3-3: un centavo bajo el minimo suspende la cuenta."""
    account = make_account("Savings", 500)
    account.transfer(400.01)

    assert account.balance == pytest.approx(99.99)
    assert account.state == "Suspended"


def test_cumulative_transfers_reaching_exact_limit(make_account):
    """BV4-1: dos transferencias que suman exactamente el limite se aceptan."""
    account = make_account("Checking", 20000)
    account.transfer(4999.99)
    result = account.transfer(0.01)

    assert result["success"] is True
    assert account.daily_transfer_total == pytest.approx(5000)
