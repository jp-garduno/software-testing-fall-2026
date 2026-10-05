"""Fixtures compartidas por toda la suite de pruebas de SecureBank."""

from datetime import datetime, timedelta

import pytest

from src.banking_system import BankAccount


class FakeClock:
    """Reloj controlable para simular el paso del tiempo (medianoche, fechas)."""

    def __init__(self, start):
        self.now = start

    def __call__(self):
        return self.now

    def advance(self, **delta):
        """Avanza el reloj; acepta los mismos argumentos que timedelta."""
        self.now += timedelta(**delta)


@pytest.fixture(name="clock")
def fixture_clock():
    """Reloj fijo: lunes 14 de septiembre de 2026, 10:00."""
    return FakeClock(datetime(2026, 9, 14, 10, 0, 0))


@pytest.fixture(name="make_account")
def fixture_make_account(clock):
    """Fábrica de cuentas que comparten el reloj controlable."""

    def _make(account_type="Checking", balance=1_000):
        return BankAccount(account_type, balance, clock=clock)

    return _make
