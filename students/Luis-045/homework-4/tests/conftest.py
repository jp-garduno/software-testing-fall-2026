"""Shared pytest fixtures for SecureBank tests."""

import pytest
from src.banking_system import BankAccount


@pytest.fixture
def checking_account():
    """Return an active Checking account with sufficient funds."""
    return BankAccount("Checking", 10000)


@pytest.fixture
def savings_account():
    """Return an active Savings account with sufficient funds."""
    return BankAccount("Savings", 5000)


@pytest.fixture
def premium_account():
    """Return an active Premium account with sufficient funds."""
    return BankAccount("Premium", 100000)