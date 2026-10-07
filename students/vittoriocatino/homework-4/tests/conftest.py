"""Shared independent fixtures for SecureBank black-box tests."""

import pytest

from src.banking_system import BankAccount


@pytest.fixture
def checking_account() -> BankAccount:
    """Return a fresh Checking account for each test."""

    return BankAccount("Checking", 10_000)


@pytest.fixture
def savings_account() -> BankAccount:
    """Return a fresh Savings account for each test."""

    return BankAccount("Savings", 2_500)


@pytest.fixture
def premium_account() -> BankAccount:
    """Return a fresh Premium account for each test."""

    return BankAccount("Premium", 100_000)
