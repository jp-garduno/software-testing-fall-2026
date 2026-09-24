"""State Transition Testing - implementa design/test-design-document.md seccion 1.4.

Se implementan las transiciones principales y el estado terminal.
"""

import pytest
from src.banking_system import ERRORS


def test_active_to_suspended(make_account):
    """ST1: Active -> Suspended cuando el saldo cae bajo el minimo."""
    account = make_account("Savings", 500)
    result = account.transfer(450)

    assert account.state == "Suspended"
    assert "below the minimum" in result["warning"]


def test_suspended_to_active(make_account):
    """ST2: Suspended -> Active cuando un deposito restaura el saldo."""
    account = make_account("Savings", 50)
    assert account.state == "Suspended"

    account.deposit(100)

    assert account.state == "Active"


def test_active_to_frozen_and_back(make_account):
    """ST3: Active -> Frozen y de vuelta a Active al descongelar."""
    account = make_account("Checking", 1000)

    assert account.freeze()["success"] is True
    assert account.state == "Frozen"

    assert account.unfreeze()["success"] is True
    assert account.state == "Active"


def test_active_to_closed(make_account):
    """ST5: Active -> Closed genera el estado de cuenta final."""
    account = make_account("Checking", 1000)
    result = account.close()

    assert account.state == "Closed"
    assert result["final_statement"] == pytest.approx(1000)


def test_closed_is_terminal(make_account):
    """ST12: Closed es terminal y rechaza cualquier evento."""
    account = make_account("Checking", 1000)
    account.close()

    assert account.transfer(10)["error"] == ERRORS["ACCOUNT_CLOSED"]
    assert account.deposit(10)["error"] == ERRORS["ACCOUNT_CLOSED"]
    assert account.close()["error"] == ERRORS["ACCOUNT_CLOSED"]
    assert account.state == "Closed"
