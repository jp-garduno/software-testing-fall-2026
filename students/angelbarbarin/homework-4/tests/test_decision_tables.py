"""Pruebas de Tablas de Decisión (DT).

Una prueba por regla de las tablas DT1-DT4 de design/test-design-document.md
(sección 3). El identificador DTx-Ry indica tabla y regla.
"""

from datetime import date

import pytest

from src.banking_system import BankAccount

FIRST_OF_MONTH = date(2026, 10, 1)


def _put_in_state(account, state):
    """Lleva una cuenta recién creada al estado indicado."""
    if state == "Frozen":
        account.freeze()
    elif state == "Closed":
        account.close()
    return account


# ------------------------------------------------------------ DT1: Transfer validation
@pytest.mark.parametrize("state,balance,amount,error", [
    ("Active", 1_000, 500, None),
    ("Active", 1_000, 2_000, "Insufficient funds"),
    ("Active", 20_000, 6_000, "Exceeds daily limit"),
    ("Active", 1_000, 6_000, "Exceeds daily limit"),
    ("Frozen", 1_000, 500, "Account is frozen"),
    ("Frozen", 1_000, 2_000, "Account is frozen"),
    ("Frozen", 20_000, 6_000, "Account is frozen"),
    ("Frozen", 1_000, 6_000, "Account is frozen"),
    ("Closed", 1_000, 500, "Account is closed"),
    ("Active", 1_000, -5, "Amount must be positive"),
], ids=[f"DT1-R{n}" for n in range(1, 11)])
def test_dt1_transfer_validation(make_account, state, balance, amount, error):
    """DT1-R1..R10: Estado x límite diario x fondos (con precedencia de errores)."""
    account = _put_in_state(make_account("Checking", balance), state)
    result = account.transfer(amount)
    assert result["success"] is (error is None)
    assert result["error"] == error


def test_dt1_r11_suspended_account_can_transfer(make_account):
    """DT1-R11: Cuenta Suspended con fondos -> transfiere y sigue Suspended."""
    account = make_account("Savings", 200)
    account.transfer(150)
    result = account.transfer(20)
    assert result["success"] is True
    assert result["state"] == "Suspended"


def test_dt1_r12_destination_frozen(make_account):
    """DT1-R12: Cuenta destino congelada -> rechazo sin mover dinero."""
    source = make_account("Checking", 1_000)
    target = _put_in_state(make_account("Checking", 1_000), "Frozen")
    assert source.transfer(300, to_account=target)["error"] == "Destination account unavailable"
    assert (source.balance, target.balance) == (1_000, 1_000)


def test_dt1_r13_destination_same_account(make_account):
    """DT1-R13: Transferir a la misma cuenta -> rechazo."""
    account = make_account("Checking", 1_000)
    assert account.transfer(300, to_account=account)["error"] == \
        "Cannot transfer to the same account"


def test_dt1_r14_destination_active_is_credited(make_account):
    """DT1-R14: Cuenta destino activa -> se debita el origen y se acredita el destino."""
    source = make_account("Checking", 1_000)
    target = make_account("Savings", 500)
    assert source.transfer(300, to_account=target)["success"] is True
    assert (source.balance, target.balance) == (700, 800)


# ------------------------------------------------------------ DT2: Monthly fee
@pytest.mark.parametrize("account_type,balance,expected", [
    ("Premium", 20_000, (0.0, False, "Active")),
    ("Savings", 1_500, (0.0, True, "Active")),
    ("Savings", 800, (5.0, False, "Active")),
    ("Savings", 102, (5.0, False, "Suspended")),
    ("Checking", 6_000, (0.0, True, "Active")),
    ("Checking", 3_000, (10.0, False, "Active")),
], ids=["DT2-R3", "DT2-R4", "DT2-R5", "DT2-R6", "DT2-R7", "DT2-R8"])
def test_dt2_monthly_fee_charged_or_waived(make_account, account_type, balance, expected):
    """DT2-R3..R8: Tipo de cuenta x umbral de exención x saldo mínimo tras el cobro.

    expected = (comisión cobrada, ¿exenta?, estado final)
    """
    account = make_account(account_type, balance)
    result = account.process_monthly_fee(FIRST_OF_MONTH)
    assert (result["fee_charged"], result["waived"], account.state) == expected


def test_dt2_r1_closed_account_not_charged(make_account):
    """DT2-R1: Cuenta cerrada -> no se cobra comisión."""
    account = _put_in_state(make_account("Checking", 3_000), "Closed")
    assert account.process_monthly_fee(FIRST_OF_MONTH)["error"] == "Account is closed"
    assert account.balance == 3_000


def test_dt2_r2_not_first_of_month(make_account):
    """DT2-R2: Fecha distinta al día 1 -> no se cobra (usa la fecha del reloj)."""
    account = make_account("Checking", 3_000)
    result = account.process_monthly_fee()
    assert result["error"] == "Fees are only charged on the 1st of the month"


def test_dt2_r9_insufficient_funds_suspends(make_account):
    """DT2-R9: Saldo menor a la comisión en cuenta activa -> Suspended, sin cobro."""
    account = make_account("Checking", 5)
    result = account.process_monthly_fee(FIRST_OF_MONTH)
    assert result == {"success": False, "error": "Insufficient funds for monthly fee",
                      "state": "Suspended"}
    assert account.balance == 5


def test_dt2_r10_insufficient_funds_on_frozen_keeps_frozen(make_account):
    """DT2-R10: Saldo menor a la comisión en cuenta congelada -> sigue Frozen."""
    account = _put_in_state(make_account("Checking", 5), "Frozen")
    assert account.process_monthly_fee(FIRST_OF_MONTH)["state"] == "Frozen"


# ------------------------------------------------------------ DT3: Bill payment
@pytest.mark.parametrize("state,payment,expected", [
    ("Active", ("UTIL-ELECTRIC", 200, None), "paid"),
    ("Active", ("UTIL-ELECTRIC", 5_000, None), "Insufficient funds"),
    ("Active", ("UTIL-ELECTRIC", 5_000, date(2026, 9, 30)), "scheduled"),
    ("Active", ("UTIL-ELECTRIC", 200, date(2026, 9, 13)),
     "Scheduled date cannot be in the past"),
    ("Active", ("UTIL-ELECTRIC", 0, None), "Amount must be positive"),
    ("Active", ("UTIL-GAS", 200, None), "Unknown payee"),
    ("Frozen", ("UTIL-ELECTRIC", 200, None), "Account is frozen"),
    ("Closed", ("UTIL-ELECTRIC", 200, None), "Account is closed"),
    ("Active", ("UTIL-ELECTRIC", 200, date(2026, 9, 14)), "paid"),
], ids=[f"DT3-R{n}" for n in range(1, 10)])
def test_dt3_bill_payment(make_account, state, payment, expected):
    """DT3-R1..R9: Estado x beneficiario x monto x fecha x fondos.

    payment = (beneficiario, monto, fecha programada); saldo inicial $1,000.
    """
    payee, amount, when = payment
    account = _put_in_state(make_account("Checking", 1_000), state)
    result = account.pay_bill(payee, amount, scheduled_date=when)
    outcome = result.get("status") if result["success"] else result["error"]
    assert outcome == expected


def test_dt3_r10_payment_below_minimum_suspends(make_account):
    """DT3-R10: Pago que deja Savings bajo $100 -> pagado y Suspended."""
    account = make_account("Savings", 150)
    result = account.pay_bill("CC-VISA", 100)
    assert (result["status"], result["state"]) == ("paid", "Suspended")


# ------------------------------------------------------------ DT4: Account creation
@pytest.mark.parametrize("account_type,balance,message", [
    ("Savings", 100, None),
    ("Premium", 9_000, "below minimum"),
    ("Gold", 50_000, "Invalid account type"),
    ("Checking", "mil", "must be a number"),
], ids=["DT4-R1", "DT4-R2", "DT4-R3", "DT4-R4"])
def test_dt4_account_creation(clock, account_type, balance, message):
    """DT4-R1..R4: Tipo válido x saldo numérico x saldo >= mínimo."""
    if message is None:
        assert BankAccount(account_type, balance, clock=clock).balance == balance
    else:
        with pytest.raises(ValueError, match=message):
            BankAccount(account_type, balance, clock=clock)
