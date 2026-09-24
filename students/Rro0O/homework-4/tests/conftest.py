"""Shared fixtures for the SecureBank black box test suite."""

import os
import sys
from datetime import date

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from banking_system import BankAccount  # noqa: E402  pylint: disable=wrong-import-position


@pytest.fixture
def today():
    """A fixed 'current day' so no test depends on the real clock."""
    return date(2026, 9, 15)


@pytest.fixture(name="make_account")
def make_account_factory():
    """Factory: ``make_account("Checking", 1000)`` returns a fresh Active account."""

    def _make(account_type="Checking", balance=1000, owner="Test Customer"):
        return BankAccount(account_type, balance, owner=owner)

    return _make


@pytest.fixture
def checking(make_account):
    """Checking account with $10,000 (limit $5,000, minimum $0)."""
    return make_account("Checking", 10000)


@pytest.fixture
def savings(make_account):
    """Savings account with $5,000 (limit $2,000, minimum $100)."""
    return make_account("Savings", 5000)


@pytest.fixture
def premium(make_account):
    """Premium account with $100,000 (limit $50,000, minimum $10,000)."""
    return make_account("Premium", 100000)
