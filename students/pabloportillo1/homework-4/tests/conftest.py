"""Shared fixtures for the SecureBank black box test suite."""

import sys
from datetime import date
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.banking_system import BankAccount, create_account  # noqa: E402  pylint: disable=wrong-import-position

HISTORY_DATES = (date(2026, 3, 1), date(2026, 3, 15), date(2026, 3, 31))


@pytest.fixture
def savings_account():
    """Active Savings account with $500 (minimum $100, daily limit $2,000)."""
    return BankAccount("Savings", 500.00)


@pytest.fixture
def checking_account():
    """Active Checking account with $1,000 (minimum $0, daily limit $5,000)."""
    return BankAccount("Checking", 1000.00)


@pytest.fixture
def funded_checking_account():
    """Active Checking account with $20,000 so only the daily limit can reject a transfer."""
    return BankAccount("Checking", 20000.00)


@pytest.fixture
def premium_account():
    """Active Premium account with $100,000 (minimum $10,000, daily limit $50,000)."""
    return BankAccount("Premium", 100000.00)


@pytest.fixture
def account_with_payees(checking_account):
    """Checking account with one active payee and one deactivated payee."""
    checking_account.register_payee("CFE", "Comision Federal de Electricidad")
    checking_account.register_payee("OLD-GYM", "Old Gym Membership", active=False)
    return checking_account


@pytest.fixture
def account_with_history(account_with_payees):
    """Checking account holding three scheduled payments dated 1, 15 and 31 March 2026."""
    seeded_today = date(2026, 1, 1)
    for index, when in enumerate(HISTORY_DATES, start=1):
        account_with_payees.pay_bill("CFE", 10.00 * index, scheduled_date=when, today=seeded_today)
    return account_with_payees


@pytest.fixture
def account_factory():
    """Build an account of any type, balance and state."""

    def _build(account_type="Checking", balance=1000.00, state="Active"):
        return BankAccount(account_type, balance, state=state)

    return _build


@pytest.fixture
def opener():
    """Expose the account creation entry point."""
    return create_account
