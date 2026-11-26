import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.banking_system import BankAccount

@pytest.fixture
def savings_account():
    """Retorna una cuenta de ahorros con $1500 (activa y sin comisiones)."""
    return BankAccount("Savings", 1500)


@pytest.fixture
def checking_account():
    """Retorna una cuenta de cheques con $6000."""
    return BankAccount("Checking", 6000)


@pytest.fixture
def premium_account():
    """Retorna una cuenta premium con $20000."""
    return BankAccount("Premium", 20000)
