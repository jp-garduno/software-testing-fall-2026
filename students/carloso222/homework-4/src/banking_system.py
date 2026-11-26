from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import ROUND_HALF_UP, Decimal
from typing import Iterable

MONEY = Decimal("0.01")


def _money(value) -> Decimal:
    return Decimal(str(value)).quantize(MONEY, rounding=ROUND_HALF_UP)


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


@dataclass
class BankAccount:
    account_type: str
    initial_balance: Decimal | int | float | str
    state: str = "Active"
    daily_transfer_total: Decimal = field(default=Decimal("0.00"), init=False)

    def __post_init__(self):
        if self.account_type not in ACCOUNT_RULES:
            raise ValueError("Invalid account type")
        self.balance = _money(self.initial_balance)
        self.daily_transfer_total = _money(0)

        minimum = self.minimum_balance
        if self.balance < minimum:
            self.state = "Suspended"

    @property
    def rules(self):
        return ACCOUNT_RULES[self.account_type]

    @property
    def minimum_balance(self) -> Decimal:
        return self.rules["minimum_balance"]

    def get_daily_limit(self) -> Decimal:
        return self.rules["daily_limit"]

    def view_balance(self) -> Decimal:
        return self.balance

    def transfer(self, amount):
        amount = _money(amount)

        if self.state in {"Frozen", "Closed"}:
            return {"success": False, "error": f"Account {self.state.lower()}"}
        if self.state != "Active":
            return {"success": False, "error": "Account not active"}
        if amount <= 0:
            return {"success": False, "error": "Amount must be positive"}
        if self.daily_transfer_total + amount > self.get_daily_limit():
            return {"success": False, "error": "Exceeds daily limit"}
        if amount > self.balance:
            return {"success": False, "error": "Insufficient funds"}

        self.balance = _money(self.balance - amount)
        self.daily_transfer_total = _money(self.daily_transfer_total + amount)
        self._update_suspension_from_balance()
        return {"success": True, "balance": self.balance}

    def reset_daily_limit(self):
        self.daily_transfer_total = _money(0)

    # pylint: disable=too-many-return-statements
    def pay_bill(
        self,
        payee: str,
        amount,
        payment_date: date | None = None,
        valid_payees: Iterable[str] | None = None,
    ):
        amount = _money(amount)
        valid_payees = set(
            valid_payees or {"Electricity", "Water", "Internet", "CreditCard"}
        )

        if self.state in {"Frozen", "Closed"}:
            return {"success": False, "error": f"Account {self.state.lower()}"}
        if self.state != "Active":
            return {"success": False, "error": "Account not active"}
        if not payee or payee not in valid_payees:
            return {"success": False, "error": "Invalid payee"}
        if amount <= 0:
            return {"success": False, "error": "Amount must be positive"}
        if amount > self.balance:
            return {"success": False, "error": "Insufficient funds"}
        if payment_date is not None and payment_date < date.today():
            return {"success": False, "error": "Payment date cannot be in the past"}

        if payment_date is None or payment_date == date.today():
            self.balance = _money(self.balance - amount)
            self._update_suspension_from_balance()
            return {"success": True, "status": "paid"}

        return {"success": True, "status": "scheduled"}

    # pylint: enable=too-many-return-statements

    def freeze(self):
        if self.state == "Closed":
            return {"success": False, "error": "Account closed"}
        self.state = "Frozen"
        return {"success": True, "state": self.state}

    def unfreeze(self):
        if self.state == "Closed":
            return {"success": False, "error": "Account closed"}
        if self.state != "Frozen":
            return {"success": False, "error": "Account is not frozen"}
        if self.balance < self.minimum_balance:
            self.state = "Suspended"
        else:
            self.state = "Active"
        return {"success": True, "state": self.state}

    def deposit(self, amount):
        amount = _money(amount)
        if self.state == "Closed":
            return {"success": False, "error": "Account closed"}
        if amount <= 0:
            return {"success": False, "error": "Amount must be positive"}
        self.balance = _money(self.balance + amount)
        if self.state == "Suspended" and self.balance >= self.minimum_balance:
            self.state = "Active"
        return {"success": True, "balance": self.balance, "state": self.state}

    def close(self):
        self.state = "Closed"
        return {"success": True, "state": "Closed"}

    def reopen(self):
        return {"success": False, "error": "Closed accounts cannot be reopened"}

    def process_monthly_fee(self):
        if self.state == "Closed":
            return {"success": False, "error": "Account closed"}

        fee = self.rules["monthly_fee"]
        waiver_threshold = self.rules["waiver_threshold"]

        if fee == 0:
            return {"success": True, "fee_charged": _money(0)}

        # Assignment wording says waived if balance > threshold (strictly greater).
        if waiver_threshold is not None and self.balance > waiver_threshold:
            return {"success": True, "fee_charged": _money(0)}

        self.balance = _money(self.balance - fee)
        self._update_suspension_from_balance()
        return {"success": True, "fee_charged": fee, "state": self.state}

    def filter_transactions(self, transactions, start_date: date, end_date: date):
        if start_date > end_date:
            return {"success": False, "error": "Invalid date range"}
        filtered = [tx for tx in transactions if start_date <= tx["date"] <= end_date]
        return {"success": True, "transactions": filtered}

    def _update_suspension_from_balance(self):
        if self.state == "Active" and self.balance < self.minimum_balance:
            self.state = "Suspended"
