"""Equivalence Partitioning - implementa design/test-design-document.md seccion 1.1.

Se prueba una representante por particion, una por cada una de las cinco entradas.
"""

import pytest
from src.banking_system import ERRORS, BankAccount


def test_valid_transfer_amount(make_account):
    """EP-TA1: un monto dentro del limite y del saldo se transfiere."""
    account = make_account("Checking", 3000)
    result = account.transfer(500)

    assert result["success"] is True
    assert account.balance == pytest.approx(2500)


def test_zero_transfer_amount_is_rejected(make_account):
    """EP-TA2: un monto de cero es rechazado."""
    result = make_account("Checking", 3000).transfer(0)

    assert result["success"] is False
    assert result["error"] == ERRORS["AMOUNT_NOT_POSITIVE"]


def test_amount_over_daily_limit_is_rejected(make_account):
    """EP-TA4: un monto sobre el limite diario es rechazado."""
    result = make_account("Checking", 3000).transfer(100000)

    assert result["success"] is False
    assert result["error"] == ERRORS["EXCEEDS_DAILY_LIMIT"]


def test_non_numeric_amount_is_rejected(make_account):
    """EP-TA6: un monto no numerico es rechazado."""
    result = make_account("Checking", 3000).transfer("500")

    assert result["success"] is False
    assert result["error"] == ERRORS["INVALID_AMOUNT"]


def test_each_account_type_applies_its_rules(make_account):
    """EP-AT1..EP-AT3: cada tipo de cuenta aplica su limite y saldo minimo."""
    assert make_account("Savings", 20000).get_daily_limit() == 2000
    assert make_account("Savings", 20000).get_minimum_balance() == 100
    assert make_account("Checking", 20000).get_daily_limit() == 5000
    assert make_account("Premium", 20000).get_daily_limit() == 50000
    assert make_account("Premium", 20000).get_minimum_balance() == 10000


def test_unknown_account_type_is_rejected():
    """EP-AT4: un tipo de cuenta desconocido es rechazado."""
    with pytest.raises(ValueError, match=ERRORS["INVALID_ACCOUNT_TYPE"]):
        BankAccount("Crypto", 1000)


def test_initial_balance_below_minimum_opens_suspended(make_account):
    """EP-AB2: un saldo inicial bajo el minimo abre la cuenta Suspendida."""
    assert make_account("Savings", 50).state == "Suspended"


def test_unregistered_payee_is_rejected(make_account):
    """EP-PY2: un beneficiario no registrado es rechazado."""
    result = make_account("Checking", 1000).pay_bill("UNKNOWN_CO", 100)

    assert result["success"] is False
    assert result["error"] == ERRORS["INVALID_PAYEE"]


def test_date_range_filters_history_and_exports_csv(make_account):
    """EP-DR1: un rango de fechas valido filtra el historial y lo exporta a CSV."""
    account = make_account("Checking", 1000)
    account.transfer(100)
    account.set_current_date("2026-02-10")
    account.deposit(50)

    history = account.get_transaction_history("2026-01-01", "2026-01-31")
    assert history["success"] is True
    assert len(history["transactions"]) == 1

    csv = account.export_history_to_csv()
    assert "2026-01-15,TRANSFER,100.00" in csv["csv"]
