"""Tests derived from the equivalence partitions in the design document."""

from datetime import date
from decimal import Decimal

import pytest

from src.banking_system import BankAccount, validate_date_range


def test_ep1_valid_transfer_amount(checking_account: BankAccount) -> None:
    """EP1: a positive amount within funds and limit succeeds."""

    result = checking_account.transfer(500)
    assert result["success"] is True
    assert checking_account.balance == Decimal("9500.00")


def test_ep2_zero_transfer_amount(checking_account: BankAccount) -> None:
    """EP2: a zero transfer is rejected as non-positive."""

    result = checking_account.transfer(0)
    assert result == {"success": False, "error": "amount_must_be_positive"}


def test_ep3_negative_transfer_amount(checking_account: BankAccount) -> None:
    """EP3: a negative transfer is rejected as non-positive."""

    result = checking_account.transfer(-100)
    assert result["error"] == "amount_must_be_positive"


def test_ep4_transfer_exceeding_daily_limit(checking_account: BankAccount) -> None:
    """EP4: an amount over the account-type limit is rejected."""

    result = checking_account.transfer(5000.01)
    assert result["success"] is False
    assert result["error"] == "exceeds_daily_limit"


def test_ep5_transfer_exceeding_balance() -> None:
    """EP5: an amount within the limit but above the balance is rejected."""

    account = BankAccount("Checking", 100)
    result = account.transfer(100.01)
    assert result["error"] == "insufficient_funds"
    assert account.balance == Decimal("100.00")


@pytest.mark.parametrize(
    ("account_type", "initial_balance", "daily_limit"),
    [
        pytest.param("Savings", 100, Decimal("2000.00"), id="EP6-savings"),
        pytest.param("Checking", 0, Decimal("5000.00"), id="EP7-checking"),
        pytest.param("Premium", 10_000, Decimal("50000.00"), id="EP8-premium"),
    ],
)
def test_ep6_to_ep8_supported_account_types(
    account_type: str, initial_balance: int, daily_limit: Decimal
) -> None:
    """EP6-EP8: every specified account type has its own valid rule set."""

    account = BankAccount(account_type, initial_balance)
    assert account.account_type == account_type
    assert account.get_daily_limit() == daily_limit


def test_ep9_unsupported_account_type() -> None:
    """EP9: an account type outside the specification is rejected."""

    with pytest.raises(ValueError, match="unsupported account type"):
        BankAccount("Business", 10_000)


@pytest.mark.parametrize("payee", ["", "   ", None], ids=["empty", "spaces", "null"])
def test_ep10_invalid_payee_partition(
    checking_account: BankAccount, payee: object
) -> None:
    """EP10: blank or non-text payee information is invalid."""

    result = checking_account.pay_bill(payee, 100)
    assert result["error"] == "invalid_payee"


def test_ep11_valid_payee_partition(checking_account: BankAccount) -> None:
    """EP11: a non-empty payee name is valid and normalized."""

    result = checking_account.pay_bill("  Comisión Federal de Electricidad  ", 100)
    assert result["success"] is True
    assert checking_account.transactions[-1]["payee"] == "Comisión Federal de Electricidad"


def test_ep12_valid_date_range_partition() -> None:
    """EP12: chronological dates form a valid history interval."""

    result = validate_date_range(date(2026, 9, 1), date(2026, 9, 30))
    assert result == {"success": True, "days": 30}


def test_ep13_reversed_date_range_partition() -> None:
    """EP13: a start date after the end date is invalid."""

    result = validate_date_range(date(2026, 9, 30), date(2026, 9, 1))
    assert result["error"] == "invalid_date_range"


def test_ep14_invalid_date_type_partition() -> None:
    """EP14: non-date values are rejected before range comparison."""

    result = validate_date_range("2026-09-01", date(2026, 9, 30))  # type: ignore[arg-type]
    assert result["error"] == "invalid_date"


def test_ep15_non_numeric_money_partition(checking_account: BankAccount) -> None:
    """EP15: a non-numeric amount cannot enter monetary calculations."""

    with pytest.raises(ValueError, match="amount must be numeric"):
        checking_account.transfer("quinientos")
