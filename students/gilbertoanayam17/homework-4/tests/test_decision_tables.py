"""Decision Tables - implementa design/test-design-document.md seccion 1.3.

Se implementan las reglas con accion distinta de cada tabla.
"""

import pytest
from src.banking_system import ERRORS


def test_rule_1_valid_transfer(make_account):
    """DT1-R1: acepta movimientos + dentro del limite + con fondos = exito."""
    account = make_account("Checking", 20000)
    result = account.transfer(100)

    assert result["success"] is True
    assert account.balance == pytest.approx(19900)


def test_rule_2_insufficient_funds(make_account):
    """DT1-R2: dentro del limite pero sin fondos = Insufficient funds."""
    account = make_account("Checking", 50)
    result = account.transfer(100)

    assert result["success"] is False
    assert result["error"] == ERRORS["INSUFFICIENT_FUNDS"]
    assert account.balance == pytest.approx(50)


def test_rule_3_exceeds_daily_limit(make_account):
    """DT1-R3: con fondos pero sobre el limite = Exceeds daily limit."""
    result = make_account("Checking", 20000).transfer(6000)

    assert result["success"] is False
    assert result["error"] == ERRORS["EXCEEDS_DAILY_LIMIT"]


def test_rule_5_frozen_account(make_account):
    """DT1-R5: una cuenta congelada rechaza sin evaluar limite ni fondos."""
    account = make_account("Checking", 20000)
    account.freeze()
    result = account.transfer(100)

    assert result["success"] is False
    assert result["error"] == ERRORS["ACCOUNT_FROZEN"]


def test_savings_pays_monthly_fee(make_account):
    """DT2-R2: Savings bajo el umbral de exencion paga la comision de $5."""
    account = make_account("Savings", 800)
    result = account.apply_monthly_fee()

    assert result["waived"] is False
    assert account.balance == pytest.approx(795)


def test_savings_without_funds_for_fee_is_suspended(make_account):
    """DT2-R3: Savings sin fondos para la comision queda suspendida."""
    account = make_account("Savings", 3)
    result = account.apply_monthly_fee()

    assert result["success"] is False
    assert result["error"] == ERRORS["INSUFFICIENT_FUNDS"]
    assert account.state == "Suspended"


def test_future_dated_bill_payment_is_scheduled(make_account):
    """DT3-R6: un pago con fecha futura se agenda sin mover el saldo."""
    account = make_account("Checking", 1000)
    result = account.pay_bill("CREDIT_CARD_VISA", 100, "2026-03-01")

    assert result["success"] is True
    assert result["scheduled"] is True
    assert account.balance == pytest.approx(1000)
