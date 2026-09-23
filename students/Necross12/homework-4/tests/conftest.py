import pytest
from banking_system import BankAccount

@pytest.fixture
def cuenta_estandar():
    return BankAccount("Estándar", 10000)


@pytest.fixture
def cuenta_ahorro():
    return BankAccount("Ahorro", 10000)
