"""Pruebas de Análisis de Valores Límite (BVA).

Cada frontera de design/test-design-document.md (sección 2) se prueba con
valores justo debajo, en y justo arriba del límite.
"""

from datetime import date

import pytest

from src.banking_system import BankAccount


# ---------------------------------------------- B1: Transfer amount, Checking ($5,000)
@pytest.mark.parametrize("amount,succeeds", [
    (0.00, False), (0.01, True), (4_999.99, True),
    (5_000.00, True), (5_000.01, False), (10_000.00, False),
], ids=["BV1", "BV2", "BV3", "BV4", "BV5", "BV6"])
def test_b1_transfer_amount_checking(make_account, amount, succeeds):
    """BV1-BV6: Monto de transferencia contra el límite diario de Checking."""
    account = make_account("Checking", 20_000)
    assert account.transfer(amount)["success"] is succeeds


def test_bv2_minimum_valid_amount_updates_balance(make_account):
    """BV2: Transferir exactamente $0.01 descuenta un centavo sin error de redondeo."""
    account = make_account("Checking", 1_000)
    account.transfer(0.01)
    assert account.balance == 999.99


def test_bv4_transfer_at_limit_updates_daily_total(make_account):
    """BV4: Transferir justo el límite deja el acumulado diario en $5,000."""
    account = make_account("Checking", 10_000)
    account.transfer(5_000)
    assert account.daily_transfer_total == 5_000


# ---------------------------------------------- B2: Transfer amount, Savings ($2,000)
@pytest.mark.parametrize("amount,succeeds", [
    (0.00, False), (0.01, True), (1_999.99, True), (2_000.00, True), (2_000.01, False),
], ids=["BV7", "BV8", "BV9", "BV10", "BV11"])
def test_b2_transfer_amount_savings(make_account, amount, succeeds):
    """BV7-BV11: Monto de transferencia contra el límite diario de Savings."""
    account = make_account("Savings", 10_000)
    assert account.transfer(amount)["success"] is succeeds


# ---------------------------------------------- B3: Transfer amount, Premium ($50,000)
@pytest.mark.parametrize("amount,succeeds", [
    (49_999.99, True), (50_000.00, True), (50_000.01, False), (75_000.00, False),
], ids=["BV12", "BV13", "BV14", "BV15"])
def test_b3_transfer_amount_premium(make_account, amount, succeeds):
    """BV12-BV15: Monto de transferencia contra el límite diario de Premium."""
    account = make_account("Premium", 200_000)
    assert account.transfer(amount)["success"] is succeeds


# ---------------------------------------------- B4: Minimum balance, Savings ($100)
@pytest.mark.parametrize("amount,state", [
    (99.99, "Active"), (100.00, "Active"), (100.01, "Suspended"), (150.00, "Suspended"),
], ids=["BV16", "BV17", "BV18", "BV19"])
def test_b4_savings_minimum_balance(make_account, amount, state):
    """BV16-BV19: Saldo resultante de 100.01 / 100.00 / 99.99 / 50.00 contra el mínimo."""
    account = make_account("Savings", 200)
    account.transfer(amount)
    assert account.state == state


def test_bv20_deposit_restoring_exact_minimum_reactivates(make_account):
    """BV20: Suspendida en $99.99, depositar $0.01 (saldo = $100.00) la reactiva."""
    account = make_account("Savings", 200)
    account.transfer(100.01)
    assert account.state == "Suspended"
    account.deposit(0.01)
    assert account.balance == 100
    assert account.state == "Active"


# ---------------------------------------------- B5: Transfer vs balance (Checking)
@pytest.mark.parametrize("amount,succeeds", [
    (999.99, True), (1_000.00, True), (1_000.01, False), (1_500.00, False),
], ids=["BV21", "BV22", "BV23", "BV24"])
def test_b5_transfer_against_balance(make_account, amount, succeeds):
    """BV21-BV24: Monto contra un saldo de $1,000 en Checking (mínimo $0)."""
    account = make_account("Checking", 1_000)
    assert account.transfer(amount)["success"] is succeeds


# ---------------------------------------------- B6: Cumulative daily limit (Savings)
@pytest.mark.parametrize("second,succeeds", [
    (499.99, True), (500.00, True), (500.01, False), (800.00, False),
], ids=["BV25", "BV26", "BV27", "BV28"])
def test_b6_cumulative_daily_limit(make_account, second, succeeds):
    """BV25-BV28: Segunda transferencia del día tras haber enviado $1,500."""
    account = make_account("Savings", 10_000)
    account.transfer(1_500)
    assert account.transfer(second)["success"] is succeeds


def test_bv29_daily_limit_one_second_before_midnight(make_account, clock):
    """BV29: A las 23:59:59 del mismo día el acumulado sigue vigente."""
    account = make_account("Savings", 10_000)
    account.transfer(2_000)
    clock.advance(hours=13, minutes=59, seconds=59)
    assert account.transfer(1)["error"] == "Exceeds daily limit"


def test_bv30_daily_limit_resets_at_midnight(make_account, clock):
    """BV30: A las 00:00:00 del día siguiente el acumulado vuelve a cero."""
    account = make_account("Savings", 10_000)
    account.transfer(2_000)
    clock.advance(hours=14)
    assert account.daily_transfer_total == 0
    assert account.transfer(2_000)["success"] is True


# ---------------------------------------------- B7: Fee waiver threshold (strict >)
FIRST_OF_MONTH = date(2026, 10, 1)


@pytest.mark.parametrize("account_type,balance,fee", [
    ("Savings", 999.99, 5.0), ("Savings", 1_000.00, 5.0), ("Savings", 1_000.01, 0.0),
    ("Checking", 5_000.00, 10.0), ("Checking", 5_000.01, 0.0),
], ids=["BV31", "BV32", "BV33", "BV34", "BV35"])
def test_b7_fee_waiver_threshold(make_account, account_type, balance, fee):
    """BV31-BV35: La exención aplica solo si el saldo es estrictamente mayor al umbral."""
    account = make_account(account_type, balance)
    result = account.process_monthly_fee(FIRST_OF_MONTH)
    assert result["fee_charged"] == fee


# ---------------------------------------------- B8: Balance vs fee (Checking, $10)
@pytest.mark.parametrize("balance,succeeds,state", [
    (10.01, True, "Active"), (10.00, True, "Active"), (9.99, False, "Suspended"),
], ids=["BV36", "BV37", "BV38"])
def test_b8_balance_against_fee(make_account, balance, succeeds, state):
    """BV36-BV38: Saldo justo alrededor de la comisión de $10 de Checking."""
    account = make_account("Checking", balance)
    assert account.process_monthly_fee(FIRST_OF_MONTH)["success"] is succeeds
    assert account.state == state


# ---------------------------------------------- B9: Minimum opening balance
@pytest.mark.parametrize("account_type,balance,created", [
    ("Premium", 9_999.99, False), ("Premium", 10_000.00, True), ("Premium", 10_000.01, True),
    ("Savings", 99.99, False), ("Savings", 100.00, True), ("Checking", 0, True),
], ids=["BV39", "BV40", "BV41", "BV42", "BV43", "BV44"])
def test_b9_minimum_opening_balance(clock, account_type, balance, created):
    """BV39-BV44: Saldo de apertura alrededor del mínimo de cada tipo."""
    if created:
        assert BankAccount(account_type, balance, clock=clock).state == "Active"
    else:
        with pytest.raises(ValueError):
            BankAccount(account_type, balance, clock=clock)


# ---------------------------------------------- B10: Decimal precision
@pytest.mark.parametrize("amount,succeeds", [
    (0.01, True), (0.001, False), (0.009, False), (1.10, True),
], ids=["BV45", "BV46", "BV47", "BV48"])
def test_b10_decimal_precision(make_account, amount, succeeds):
    """BV45-BV48: Montos alrededor de la resolución mínima de un centavo."""
    assert make_account().transfer(amount)["success"] is succeeds
