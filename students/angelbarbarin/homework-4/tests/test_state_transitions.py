"""Pruebas de Transición de Estados (ST).

Cubren cada transición válida del diagrama de design/test-design-document.md
(sección 4), las transiciones inválidas y secuencias completas de estados.
"""

from datetime import date

import pytest

FIRST_OF_MONTH = date(2026, 10, 1)


# ------------------------------------------------------------ Transiciones válidas
def test_st1_active_to_suspended_on_low_balance(make_account):
    """ST1: Active --transferencia deja saldo < $100--> Suspended con aviso."""
    account = make_account("Savings", 500)
    account.transfer(450)
    assert account.state == "Suspended"
    assert "Warning: balance below minimum" in account.notifications


def test_st2_active_to_frozen(make_account):
    """ST2: Active --solicitud de congelamiento--> Frozen."""
    account = make_account()
    result = account.freeze("fraud detection")
    assert (result["success"], account.state) == (True, "Frozen")
    assert "Account frozen: fraud detection" in account.notifications


def test_st3_active_to_closed(make_account):
    """ST3: Active --cierre--> Closed con estado de cuenta final."""
    account = make_account("Checking", 750)
    account.deposit(50)
    result = account.close()
    assert account.state == "Closed"
    assert result["final_statement"] == {"final_balance": 800, "transactions": 1}


def test_st4_suspended_to_active_on_deposit(make_account):
    """ST4: Suspended --depósito restaura el mínimo--> Active."""
    account = make_account("Savings", 500)
    account.transfer(450)
    result = account.deposit(500)
    assert (result["state"], account.balance) == ("Active", 550)
    assert "Account reactivated: minimum balance restored" in account.notifications


def test_st5_suspended_stays_suspended_on_small_deposit(make_account):
    """ST5: Suspended --depósito insuficiente--> Suspended."""
    account = make_account("Savings", 500)
    account.transfer(450)
    account.deposit(20)
    assert account.state == "Suspended"


def test_st6_suspended_to_closed(make_account):
    """ST6: Suspended --cierre--> Closed."""
    account = make_account("Savings", 500)
    account.transfer(450)
    assert account.close()["state"] == "Closed"


def test_st7_frozen_to_active_on_unfreeze(make_account):
    """ST7: Frozen --descongelar con saldo >= mínimo--> Active."""
    account = make_account("Savings", 500)
    account.freeze()
    assert account.unfreeze()["state"] == "Active"


def test_st8_frozen_to_suspended_on_unfreeze_below_minimum(make_account):
    """ST8: Frozen --descongelar con saldo < mínimo (por comisión)--> Suspended."""
    account = make_account("Savings", 102)
    account.freeze()
    account.process_monthly_fee(FIRST_OF_MONTH)
    assert account.state == "Frozen"
    assert account.unfreeze()["state"] == "Suspended"


def test_st9_frozen_to_closed(make_account):
    """ST9: Frozen --cierre--> Closed."""
    account = make_account()
    account.freeze()
    assert account.close()["state"] == "Closed"


def test_st10_active_to_suspended_on_unpaid_fee(make_account):
    """ST10: Active --comisión sin fondos--> Suspended."""
    account = make_account("Checking", 3)
    account.process_monthly_fee(FIRST_OF_MONTH)
    assert account.state == "Suspended"


# ------------------------------------------------------------ Transiciones inválidas
@pytest.mark.parametrize("operation", ["transfer", "deposit", "pay_bill"],
                         ids=["ST11-transfer", "ST11-deposit", "ST11-bill"])
def test_st11_frozen_rejects_transactions(make_account, operation):
    """ST11: Frozen solo permite consulta; todo movimiento se rechaza."""
    account = make_account("Checking", 1_000)
    account.freeze()
    args = ("UTIL-WATER", 50) if operation == "pay_bill" else (50,)
    assert getattr(account, operation)(*args)["error"] == "Account is frozen"
    assert (account.state, account.balance) == ("Frozen", 1_000)


@pytest.mark.parametrize("operation,error", [
    ("transfer", "Account is closed"),
    ("deposit", "Account is closed"),
    ("freeze", "Cannot freeze an account in state Closed"),
    ("unfreeze", "Account is not frozen"),
    ("close", "Account is already closed"),
], ids=["ST12-transfer", "ST12-deposit", "ST12-freeze", "ST12-unfreeze", "ST12-close"])
def test_st12_closed_is_final(make_account, operation, error):
    """ST12: Closed es terminal; ningún evento cambia el estado ni se reabre."""
    account = make_account("Checking", 1_000)
    account.close()
    args = (50,) if operation in ("transfer", "deposit") else ()
    assert getattr(account, operation)(*args)["error"] == error
    assert account.state == "Closed"


def test_st13_suspended_cannot_be_frozen(make_account):
    """ST13: Suspended --congelar--> rechazado (solo Active -> Frozen es válido)."""
    account = make_account("Savings", 500)
    account.transfer(450)
    assert account.freeze()["error"] == "Cannot freeze an account in state Suspended"
    assert account.state == "Suspended"


def test_st14_active_cannot_be_unfrozen(make_account):
    """ST14: Active --descongelar--> rechazado."""
    account = make_account()
    assert account.unfreeze()["error"] == "Account is not frozen"
    assert account.state == "Active"


def test_st18_redundant_state_events_rejected(make_account):
    """ST18: Suspended --descongelar--> rechazado; Frozen --congelar--> rechazado."""
    suspended = make_account("Savings", 500)
    suspended.transfer(450)
    assert suspended.unfreeze()["error"] == "Account is not frozen"
    frozen = make_account()
    frozen.freeze()
    assert frozen.freeze()["error"] == "Cannot freeze an account in state Frozen"
    assert (suspended.state, frozen.state) == ("Suspended", "Frozen")


def test_st15_balance_is_viewable_in_every_state(make_account):
    """ST15: La consulta de saldo funciona en Frozen y Closed (view only)."""
    account = make_account("Checking", 640)
    account.freeze()
    frozen_view = account.balance
    account.close()
    assert (frozen_view, account.balance) == (640, 640)


# ------------------------------------------------------------ Secuencias completas
def test_st16_full_lifecycle_sequence(make_account):
    """ST16: Active -> Suspended -> Active -> Frozen -> Active -> Closed."""
    account = make_account("Savings", 500)
    visited = [account.state]
    account.transfer(450)
    visited.append(account.state)
    account.deposit(300)
    visited.append(account.state)
    account.freeze()
    visited.append(account.state)
    account.unfreeze()
    visited.append(account.state)
    account.close()
    visited.append(account.state)
    assert visited == ["Active", "Suspended", "Active", "Frozen", "Active", "Closed"]


def test_st17_repeated_suspension_cycle(make_account):
    """ST17: Suspended -> Active -> Suspended (la regla se reaplica cada vez)."""
    account = make_account("Savings", 300)
    account.transfer(250)
    account.deposit(100)
    account.transfer(100)
    assert account.state == "Suspended"
