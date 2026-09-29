"""Fixtures compartidas por las cuatro suites de black box testing."""

import pytest
from src.banking_system import BankAccount


@pytest.fixture(name="make_account")
def fixture_make_account():
    """Factory de cuentas nuevas, para que cada prueba sea independiente."""

    def _make(account_type, balance):
        return BankAccount(account_type, balance)

    return _make
