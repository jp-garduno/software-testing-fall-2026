"""Shared pytest fixtures for the SecureBank black box test suite."""

from datetime import date

import pytest

from src.banking_system import BankAccount


@pytest.fixture
def today():
    """A fixed reference date so daily-limit tests are deterministic."""
    return date(2026, 6, 15)


@pytest.fixture
def checking_account(today):
    """A Checking account with $10,000 balance (well above the $0 minimum)."""
    return BankAccount("Checking", 10000, today=today)


@pytest.fixture
def savings_account(today):
    """A Savings account with $1,500 balance (above the $1,000 fee waiver)."""
    return BankAccount("Savings", 1500, today=today)


@pytest.fixture
def premium_account(today):
    """A Premium account with $20,000 balance (well above the $10,000 minimum)."""
    return BankAccount("Premium", 20000, today=today)
