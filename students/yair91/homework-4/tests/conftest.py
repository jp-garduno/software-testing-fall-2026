"""Shared fixtures for the SecureBank black box test suite."""

from datetime import date, timedelta

import pytest

from src.banking_system import BankAccount


@pytest.fixture
def savings_account():
    """Savings account comfortably above its $100 minimum."""
    return BankAccount("Savings", 1500.0)


@pytest.fixture
def checking_account():
    """Checking account with enough balance to reach its $5,000 daily limit."""
    return BankAccount("Checking", 10000.0)


@pytest.fixture
def premium_account():
    """Premium account at twice its $10,000 minimum."""
    return BankAccount("Premium", 20000.0)


@pytest.fixture
def yesterday():
    """The day before today, used for past-dated payment scheduling."""
    return date.today() - timedelta(days=1)


@pytest.fixture
def tomorrow():
    """The day after today, used for future-dated payment scheduling."""
    return date.today() + timedelta(days=1)
