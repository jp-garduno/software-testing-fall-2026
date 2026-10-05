"""Pruebas de Particiones de Equivalencia (EP).

Cada prueba toma un valor representativo de una clase de equivalencia
documentada en design/test-design-document.md, sección 1.
"""

from datetime import date, datetime

import pytest

from src.banking_system import BankAccount


# ---------------------------------------------------------------- Transfer amount
def test_ep1_transfer_valid_amount(make_account):
    """EP1: Monto válido dentro de límites -> la transferencia procede."""
    account = make_account("Checking", 1_000)
    result = account.transfer(500)
    assert result["success"] is True
    assert account.balance == 500


@pytest.mark.parametrize("amount", [0, -100], ids=["EP2-zero", "EP3-negative"])
def test_ep2_ep3_transfer_non_positive_amount(make_account, amount):
    """EP2/EP3: Monto cero o negativo -> error de monto positivo."""
    account = make_account("Checking", 1_000)
    result = account.transfer(amount)
    assert result["success"] is False
    assert "must be positive" in result["error"]
    assert account.balance == 1_000


def test_ep4_transfer_exceeds_daily_limit(make_account):
    """EP4: Monto mayor al límite diario -> error de límite diario."""
    account = make_account("Checking", 200_000)
    result = account.transfer(100_000)
    assert result == {"success": False, "error": "Exceeds daily limit"}


def test_ep5_transfer_exceeds_balance(make_account):
    """EP5: Monto mayor al saldo -> fondos insuficientes."""
    account = make_account("Checking", 1_000)
    result = account.transfer(1_500)
    assert result["error"] == "Insufficient funds"


@pytest.mark.parametrize("amount", ["500", None, True, float("nan")],
                         ids=["EP6-string", "EP6-none", "EP6-bool", "EP6-nan"])
def test_ep6_transfer_non_numeric_amount(make_account, amount):
    """EP6: Monto no numérico -> error de tipo de dato."""
    result = make_account().transfer(amount)
    assert result["error"] == "Amount must be a number"


def test_ep7_transfer_sub_cent_amount(make_account):
    """EP7: Monto con fracciones de centavo -> rechazado."""
    result = make_account().transfer(10.005)
    assert result["error"] == "Amount must have at most 2 decimal places"


@pytest.mark.parametrize("amount,error", [
    (250, None), (-250, "Amount must be positive"), ("250", "Amount must be a number"),
], ids=["EP31-valid", "EP32-negative", "EP33-text"])
def test_ep31_to_ep33_deposit_amount(make_account, amount, error):
    """EP31-EP33: Depósito válido, negativo o como texto."""
    account = make_account("Checking", 1_000)
    result = account.deposit(amount)
    assert result["error"] == error
    assert account.balance == (1_250 if error is None else 1_000)


# ---------------------------------------------------------------- Account type
@pytest.mark.parametrize("account_type,balance,limit", [
    ("Savings", 500, 2_000),
    ("Checking", 500, 5_000),
    ("Premium", 20_000, 50_000),
], ids=["EP8-savings", "EP9-checking", "EP10-premium"])
def test_ep8_to_ep10_valid_account_types(clock, account_type, balance, limit):
    """EP8-EP10: Cada tipo válido se crea activo con su límite diario."""
    account = BankAccount(account_type, balance, clock=clock)
    assert account.state == "Active"
    assert account.get_daily_limit() == limit


@pytest.mark.parametrize("account_type", ["Business", "savings", ""],
                         ids=["EP11-unknown", "EP12-wrong-case", "EP12-empty"])
def test_ep11_ep12_invalid_account_type(clock, account_type):
    """EP11/EP12: Tipo inexistente o con mayúsculas incorrectas -> ValueError."""
    with pytest.raises(ValueError, match="Invalid account type"):
        BankAccount(account_type, 1_000, clock=clock)


def test_ep34_default_system_clock():
    """EP34: Sin reloj inyectado la cuenta usa la hora del sistema y opera normal."""
    account = BankAccount("Checking", 100)
    assert account.transfer(40)["success"] is True
    assert account.daily_transfer_total == 40


# ---------------------------------------------------------------- Account balance
def test_ep13_balance_at_or_above_minimum(make_account):
    """EP13: Saldo inicial mayor o igual al mínimo -> cuenta activa."""
    account = make_account("Savings", 5_000)
    assert account.state == "Active"
    assert account.get_minimum_balance() == 100


@pytest.mark.parametrize("account_type,balance", [
    ("Premium", 5_000), ("Savings", -50)], ids=["EP14-below-min", "EP15-negative"])
def test_ep14_ep15_initial_balance_below_minimum(clock, account_type, balance):
    """EP14/EP15: Saldo inicial bajo el mínimo o negativo -> ValueError."""
    with pytest.raises(ValueError, match="below minimum"):
        BankAccount(account_type, balance, clock=clock)


# ---------------------------------------------------------------- Payee
@pytest.mark.parametrize("payee", ["UTIL-ELECTRIC", "  cc-visa  "],
                         ids=["EP16-registered", "EP20-normalized"])
def test_ep16_ep20_valid_payee(make_account, payee):
    """EP16/EP20: Beneficiario registrado (incluso con espacios/minúsculas) -> pagado."""
    account = make_account("Checking", 1_000)
    result = account.pay_bill(payee, 150)
    assert result["status"] == "paid"
    assert account.balance == 850


@pytest.mark.parametrize("payee", ["", "   ", None, 12345],
                         ids=["EP17-empty", "EP17-blank", "EP18-none", "EP18-number"])
def test_ep17_ep18_missing_payee(make_account, payee):
    """EP17/EP18: Beneficiario vacío o de tipo inválido -> requerido."""
    result = make_account().pay_bill(payee, 150)
    assert result["error"] == "Payee is required"


def test_ep19_unknown_payee(make_account):
    """EP19: Beneficiario no registrado -> rechazado."""
    result = make_account().pay_bill("UTIL-GAS", 150)
    assert result["error"] == "Unknown payee"


# ---------------------------------------------------------------- Scheduled date
def test_ep26_bill_immediate_payment(make_account):
    """EP26: Sin fecha programada -> pago inmediato."""
    account = make_account("Checking", 1_000)
    assert account.pay_bill("UTIL-WATER", 80)["status"] == "paid"


def test_ep27_bill_future_date_is_scheduled(make_account):
    """EP27: Fecha futura -> pago programado sin mover el saldo."""
    account = make_account("Checking", 1_000)
    result = account.pay_bill("UTIL-WATER", 80, scheduled_date=date(2026, 10, 1))
    assert result["status"] == "scheduled"
    assert account.balance == 1_000
    assert account.scheduled_payments[0]["date"] == date(2026, 10, 1)


def test_ep28_bill_past_date_rejected(make_account):
    """EP28: Fecha pasada -> rechazado."""
    result = make_account().pay_bill("UTIL-WATER", 80, scheduled_date=date(2026, 9, 1))
    assert result["error"] == "Scheduled date cannot be in the past"


def test_ep29_bill_invalid_amount(make_account):
    """EP29: Pago con monto cero -> error de monto positivo."""
    assert "must be positive" in make_account().pay_bill("CC-VISA", 0)["error"]


# ---------------------------------------------------------------- Date range
@pytest.fixture(name="history_account")
def fixture_history_account(make_account, clock):
    """Cuenta con tres movimientos en días distintos (14, 15 y 16 de sept.)."""
    account = make_account("Checking", 5_000)
    for _ in range(3):
        account.deposit(100)
        clock.advance(days=1)
    return account


def test_ep21_valid_date_range(history_account):
    """EP21: Rango válido -> solo los movimientos dentro del rango (inclusivo)."""
    found = history_account.get_transactions(date(2026, 9, 15), date(2026, 9, 16))
    assert len(found) == 2


def test_ep22_start_after_end(history_account):
    """EP22: Fecha inicial posterior a la final -> ValueError."""
    with pytest.raises(ValueError, match="on or before"):
        history_account.get_transactions(date(2026, 9, 20), date(2026, 9, 1))


def test_ep23_range_without_transactions(history_account):
    """EP23: Rango sin movimientos -> lista vacía."""
    assert not history_account.get_transactions(date(2027, 1, 1), date(2027, 1, 31))


def test_ep24_open_ended_range(history_account):
    """EP24: Sin fechas -> todo el historial; acepta datetime como filtro."""
    assert len(history_account.get_transactions()) == 3
    assert len(history_account.get_transactions(datetime(2026, 9, 16, 8, 0))) == 1


def test_ep25_invalid_date_type(history_account):
    """EP25: Fecha como texto -> TypeError."""
    with pytest.raises(TypeError, match="must be a date"):
        history_account.get_transactions("2026-09-01")


def test_ep30_export_csv(history_account):
    """EP30: Exportar un rango válido -> CSV con encabezado y una fila por movimiento."""
    lines = history_account.export_transactions_csv(date(2026, 9, 14),
                                                    date(2026, 9, 14)).splitlines()
    assert lines[0] == "timestamp,type,amount,balance_after,description"
    assert lines[1] == "2026-09-14T10:00:00,deposit,100.00,5100.00,Deposit"
    assert len(lines) == 2
    assert len(history_account.export_transactions_csv().splitlines()) == 4
