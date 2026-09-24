"""
Shared pytest fixtures for SecureBank black box test suite.

Fixtures provide pre-configured BankAccount instances for each account type
and state, avoiding duplication across test modules.
"""

import pytest

from src.banking_system import AccountState, AccountType, BankAccount, BankingSystem


# ---------------------------------------------------------------------------
# Account fixtures — Active state
# ---------------------------------------------------------------------------


@pytest.fixture
def savings_account() -> BankAccount:
    """Active Savings account with $500 balance (well above $100 minimum)."""
    return BankAccount(AccountType.SAVINGS, 500.00)


@pytest.fixture
def checking_account() -> BankAccount:
    """Active Checking account with $1,000 balance."""
    return BankAccount(AccountType.CHECKING, 1_000.00)


@pytest.fixture
def premium_account() -> BankAccount:
    """Active Premium account with $15,000 balance (above $10,000 minimum)."""
    return BankAccount(AccountType.PREMIUM, 15_000.00)


@pytest.fixture
def high_balance_checking() -> BankAccount:
    """Checking account with $10,000 — enough for limit-boundary tests."""
    return BankAccount(AccountType.CHECKING, 10_000.00)


@pytest.fixture
def high_balance_savings() -> BankAccount:
    """Savings account with $5,000 — enough for limit-boundary tests."""
    return BankAccount(AccountType.SAVINGS, 5_000.00)


# ---------------------------------------------------------------------------
# Account fixtures — special states
# ---------------------------------------------------------------------------


@pytest.fixture
def frozen_account() -> BankAccount:
    """Checking account that has been frozen."""
    account = BankAccount(AccountType.CHECKING, 1_000.00)
    account.freeze()
    return account


@pytest.fixture
def suspended_savings() -> BankAccount:
    """Savings account below $100 minimum → Suspended on creation."""
    return BankAccount(AccountType.SAVINGS, 50.00)


@pytest.fixture
def closed_account() -> BankAccount:
    """Checking account that has been closed."""
    account = BankAccount(AccountType.CHECKING, 500.00)
    account.close()
    return account


# ---------------------------------------------------------------------------
# System fixture
# ---------------------------------------------------------------------------


@pytest.fixture
def banking_system() -> BankingSystem:
    """Fresh BankingSystem instance."""
    return BankingSystem()
