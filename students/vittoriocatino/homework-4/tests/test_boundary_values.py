"""Tests derived from the boundary-value tables in the design document."""

from decimal import Decimal

import pytest

from src.banking_system import AccountState, BankAccount


def test_bv1_transfer_at_zero(checking_account: BankAccount) -> None:
    """BV1: $0.00 is immediately below the minimum valid transfer."""

    assert checking_account.transfer(0)["error"] == "amount_must_be_positive"


def test_bv2_transfer_at_one_cent(checking_account: BankAccount) -> None:
    """BV2: $0.01 is the minimum valid transfer."""

    result = checking_account.transfer(0.01)
    assert result["success"] is True
    assert checking_account.balance == Decimal("9999.99")


@pytest.mark.parametrize(
    ("amount", "success", "error"),
    [
        pytest.param(4999.99, True, None, id="BV3-just-below"),
        pytest.param(5000.00, True, None, id="BV4-at-limit"),
        pytest.param(5000.01, False, "exceeds_daily_limit", id="BV5-just-above"),
        pytest.param(10000.00, False, "exceeds_daily_limit", id="BV6-far-above"),
    ],
)
def test_bv3_to_bv6_checking_transfer_limit(
    checking_account: BankAccount, amount: float, success: bool, error: str | None
) -> None:
    """BV3-BV6: values around the Checking $5,000 daily limit."""

    result = checking_account.transfer(amount)
    assert result["success"] is success
    if error:
        assert result["error"] == error


def test_bv7_savings_below_minimum() -> None:
    """BV7: $99.99 is below the Savings opening minimum."""

    with pytest.raises(ValueError, match="below account minimum"):
        BankAccount("Savings", 99.99)


@pytest.mark.parametrize(
    "balance",
    [
        pytest.param(100.00, id="BV8-at-minimum"),
        pytest.param(100.01, id="BV9-just-above"),
    ],
)
def test_bv8_and_bv9_savings_valid_minimum(balance: float) -> None:
    """BV8-BV9: Savings opens at or above its $100 minimum."""

    assert BankAccount("Savings", balance).state is AccountState.ACTIVE


@pytest.mark.parametrize(
    ("balance", "waived"),
    [
        pytest.param(999.99, False, id="BV10-below-waiver"),
        pytest.param(1000.00, False, id="BV11-at-waiver"),
        pytest.param(1000.01, True, id="BV12-above-waiver"),
        pytest.param(1500.00, True, id="BV13-far-above-waiver"),
    ],
)
def test_bv10_to_bv13_savings_fee_waiver(balance: float, waived: bool) -> None:
    """BV10-BV13: Savings waiver is strict: balance must exceed $1,000."""

    result = BankAccount("Savings", balance).process_monthly_fee()
    assert result["waived"] is waived


@pytest.mark.parametrize(
    ("balance", "waived"),
    [
        pytest.param(4999.99, False, id="BV14-below-waiver"),
        pytest.param(5000.00, False, id="BV15-at-waiver"),
        pytest.param(5000.01, True, id="BV16-above-waiver"),
        pytest.param(6000.00, True, id="BV17-far-above-waiver"),
    ],
)
def test_bv14_to_bv17_checking_fee_waiver(balance: float, waived: bool) -> None:
    """BV14-BV17: Checking waiver is strict: balance must exceed $5,000."""

    result = BankAccount("Checking", balance).process_monthly_fee()
    assert result["waived"] is waived


@pytest.mark.parametrize(
    ("amount", "success"),
    [
        pytest.param(49999.99, True, id="BV18-just-below"),
        pytest.param(50000.00, True, id="BV19-at-limit"),
        pytest.param(50000.01, False, id="BV20-just-above"),
        pytest.param(100000.00, False, id="BV21-far-above"),
    ],
)
def test_bv18_to_bv21_premium_daily_limit(
    premium_account: BankAccount, amount: float, success: bool
) -> None:
    """BV18-BV21: values around the Premium $50,000 daily limit."""

    assert premium_account.transfer(amount)["success"] is success
