"""Observable behavior of the SecureBank system under test."""

from __future__ import annotations

from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from enum import StrEnum
from typing import Any


CENT = Decimal("0.01")


class AccountState(StrEnum):
    """Supported account states."""

    ACTIVE = "Active"
    FROZEN = "Frozen"
    SUSPENDED = "Suspended"
    CLOSED = "Closed"


ACCOUNT_RULES = {
    "Savings": {
        "minimum_balance": Decimal("100.00"),
        "monthly_fee": Decimal("5.00"),
        "waiver_threshold": Decimal("1000.00"),
        "daily_limit": Decimal("2000.00"),
    },
    "Checking": {
        "minimum_balance": Decimal("0.00"),
        "monthly_fee": Decimal("10.00"),
        "waiver_threshold": Decimal("5000.00"),
        "daily_limit": Decimal("5000.00"),
    },
    "Premium": {
        "minimum_balance": Decimal("10000.00"),
        "monthly_fee": Decimal("0.00"),
        "waiver_threshold": None,
        "daily_limit": Decimal("50000.00"),
    },
}


def _money(value: Any) -> Decimal:
    """Convert an external value to two-decimal monetary precision."""

    try:
        return Decimal(str(value)).quantize(CENT, rounding=ROUND_HALF_UP)
    except (InvalidOperation, TypeError, ValueError) as error:
        raise ValueError("amount must be numeric") from error


def _result(success: bool, **details: Any) -> dict[str, Any]:
    """Build the stable response shape exposed by banking operations."""

    return {"success": success, **details}


def validate_date_range(start_date: date, end_date: date) -> dict[str, Any]:
    """Validate a transaction-history date range."""

    if not isinstance(start_date, date) or not isinstance(end_date, date):
        return _result(False, error="invalid_date")
    if start_date > end_date:
        return _result(False, error="invalid_date_range")
    return _result(True, days=(end_date - start_date).days + 1)


class BankAccount:
    """Small deterministic banking model exercised only through its public API."""

    def __init__(self, account_type: str, initial_balance: Any) -> None:
        if account_type not in ACCOUNT_RULES:
            raise ValueError("unsupported account type")

        balance = _money(initial_balance)
        minimum = ACCOUNT_RULES[account_type]["minimum_balance"]
        if balance < minimum:
            raise ValueError("initial balance below account minimum")

        self.account_type = account_type
        self.balance = balance
        self.state = AccountState.ACTIVE
        self.daily_transfer_total = Decimal("0.00")
        self.transactions: list[dict[str, Any]] = []

    @property
    def rules(self) -> dict[str, Decimal | None]:
        """Return the rules for this account type."""

        return ACCOUNT_RULES[self.account_type]

    def get_daily_limit(self) -> Decimal:
        """Return the daily transfer limit for this account type."""

        return self.rules["daily_limit"]  # type: ignore[return-value]

    def transfer(self, amount: Any) -> dict[str, Any]:
        """Transfer money after amount, state, limit, and funds validation."""

        transfer_amount = _money(amount)
        if transfer_amount <= 0:
            return _result(False, error="amount_must_be_positive")
        if self.state is not AccountState.ACTIVE:
            return _result(False, error="account_not_active", state=self.state.value)
        if self.daily_transfer_total + transfer_amount > self.get_daily_limit():
            return _result(False, error="exceeds_daily_limit")
        if transfer_amount > self.balance:
            return _result(False, error="insufficient_funds")

        self.balance -= transfer_amount
        self.daily_transfer_total += transfer_amount
        self.transactions.append({"type": "transfer", "amount": transfer_amount})
        self._suspend_if_below_minimum()
        return _result(True, balance=self.balance, state=self.state.value)

    def pay_bill(self, payee: Any, amount: Any) -> dict[str, Any]:
        """Pay a bill when the payee, amount, state, and funds are valid."""

        payment_amount = _money(amount)
        if self.state is not AccountState.ACTIVE:
            return _result(False, error="account_not_active", state=self.state.value)
        if not isinstance(payee, str) or not payee.strip():
            return _result(False, error="invalid_payee")
        if payment_amount <= 0:
            return _result(False, error="amount_must_be_positive")
        if payment_amount > self.balance:
            return _result(False, error="insufficient_funds")

        self.balance -= payment_amount
        self.transactions.append(
            {"type": "bill_payment", "payee": payee.strip(), "amount": payment_amount}
        )
        self._suspend_if_below_minimum()
        return _result(True, balance=self.balance, state=self.state.value)

    def deposit(self, amount: Any) -> dict[str, Any]:
        """Deposit funds and reactivate a suspended account when restored."""

        deposit_amount = _money(amount)
        if deposit_amount <= 0:
            return _result(False, error="amount_must_be_positive")
        if self.state is AccountState.CLOSED:
            return _result(False, error="account_closed")

        self.balance += deposit_amount
        self.transactions.append({"type": "deposit", "amount": deposit_amount})
        if (
            self.state is AccountState.SUSPENDED
            and self.balance >= self.rules["minimum_balance"]
        ):
            self.state = AccountState.ACTIVE
        return _result(True, balance=self.balance, state=self.state.value)

    def process_monthly_fee(self) -> dict[str, Any]:
        """Apply or waive the monthly fee according to account rules."""

        if self.state is AccountState.CLOSED:
            return _result(False, error="account_closed")

        fee = self.rules["monthly_fee"]
        threshold = self.rules["waiver_threshold"]
        if fee == 0 or (threshold is not None and self.balance > threshold):
            return _result(True, waived=True, fee=Decimal("0.00"), state=self.state.value)

        self.balance -= fee  # type: ignore[operator]
        self.transactions.append({"type": "monthly_fee", "amount": fee})
        self._suspend_if_below_minimum()
        return _result(
            True,
            waived=False,
            fee=fee,
            balance=self.balance,
            state=self.state.value,
        )

    def freeze(self) -> dict[str, Any]:
        """Freeze an active account."""

        if self.state is not AccountState.ACTIVE:
            return _result(False, error="invalid_transition", state=self.state.value)
        self.state = AccountState.FROZEN
        return _result(True, state=self.state.value)

    def unfreeze(self) -> dict[str, Any]:
        """Restore a frozen account to active state."""

        if self.state is not AccountState.FROZEN:
            return _result(False, error="invalid_transition", state=self.state.value)
        self.state = AccountState.ACTIVE
        return _result(True, state=self.state.value)

    def close(self) -> dict[str, Any]:
        """Close an account permanently."""

        if self.state is AccountState.CLOSED:
            return _result(False, error="account_closed", state=self.state.value)
        self.state = AccountState.CLOSED
        return _result(True, state=self.state.value)

    def reset_daily_limit(self) -> None:
        """Reset accumulated transfers at midnight."""

        self.daily_transfer_total = Decimal("0.00")

    def _suspend_if_below_minimum(self) -> None:
        """Apply the Active-to-Suspended balance transition."""

        if self.balance < self.rules["minimum_balance"]:
            self.state = AccountState.SUSPENDED
