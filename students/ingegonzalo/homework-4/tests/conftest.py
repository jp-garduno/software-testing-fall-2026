import pytest
from banking_system import BankAccount

@pytest.fixture
def savings_account():
    return BankAccount("Savings", 1500)

@pytest.fixture
def checking_account():
    return BankAccount("Checking", 10000)

@pytest.fixture
def premium_account():
    return BankAccount("Premium", 20000)