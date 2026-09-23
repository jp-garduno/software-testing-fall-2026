"""SecureBank's public contract, using integer cents and an injectable UTC clock."""

from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from decimal import Decimal
from functools import wraps
import re


@dataclass(frozen=True)
class AccountRules:
    """Immutable monetary policy for an account type, expressed in cents."""

    minimum: int
    fee: int
    waiver: int
    limit: int


@dataclass
class AccountProfile:
    """Current customer-facing account information."""

    account_type: str
    balance: int
    state: str
    owner: str = "Customer"


@dataclass
class AccountLedger:
    """Independent transaction records and processing queues for one account."""

    transactions: list[dict] = field(default_factory=list)
    scheduled: list[dict] = field(default_factory=list)
    fee_months: set[str] = field(default_factory=set)


RULES = {
    "Savings": AccountRules(10000, 500, 100000, 200000),
    "Checking": AccountRules(0, 1000, 500000, 500000),
    "Premium": AccountRules(1000000, 0, 0, 5000000),
}
PAYEES = ("utilities", "credit-card", "internet")
MAX_CENTS = 100_000_000_000


def money(value):
    """Validate money without silently rounding sub-cent inputs."""
    if type(value) not in (int, float):
        raise ValueError("Invalid amount")
    cents = Decimal(str(value)) * 100
    if not cents.is_finite() or cents != cents.to_integral_value():
        raise ValueError("Invalid amount")
    if abs(cents) > MAX_CENTS:
        raise ValueError("Invalid amount")
    return int(cents)


def iso_date(value):
    """Return a real ISO calendar date, rejecting malformed strings."""
    if not isinstance(value, str) or not re.fullmatch(
        r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value
    ):
        raise ValueError("Invalid date")
    try:
        date.fromisoformat(value)
    except ValueError:
        raise ValueError("Invalid date") from None
    return value


def command(method):
    """Expose domain failures as results, without hiding programming errors."""

    @wraps(method)
    def wrapped(self, *args):
        self.refresh_day()
        try:
            return {"success": True, **method(self, *args)}
        except ValueError as error:
            return {"success": False, "error": str(error)}

    return wrapped


class BankAccount:
    """Apply account policies through validated commands and copied read views."""

    def __init__(self, account_type, initial_balance, clock=None):
        if not isinstance(account_type, str) or account_type not in RULES:
            raise ValueError("Invalid account type")
        try:
            balance = money(initial_balance)
            if balance < 0:
                raise ValueError("Invalid amount")
        except ValueError:
            raise ValueError("Invalid opening balance") from None
        self._rules = RULES[account_type]
        self._profile = AccountProfile(
            account_type,
            balance,
            "Active" if balance >= self._rules.minimum else "Suspended",
        )
        self._clock = clock or (lambda: datetime.now(timezone.utc).date().isoformat())
        self._day = iso_date(self._clock())
        self._daily_total = 0
        self._ledger = AccountLedger()

    def refresh_day(self):
        """Synchronize the transfer allowance with the injected UTC date."""
        today = iso_date(self._clock())
        if today != self._day:
            self._daily_total = 0
            self._day = today

    def _require_state(self, *allowed):
        if self._profile.state not in allowed:
            raise ValueError(f"Account {self._profile.state.lower()}")

    def _positive(self, amount):
        cents = money(amount)
        if cents <= 0:
            raise ValueError("Amount must be positive")
        return cents

    def _funds(self, cents):
        if cents > self._profile.balance:
            raise ValueError("Insufficient funds")

    def _record(self, kind, cents, detail):
        self._ledger.transactions.append(
            {
                "date": self._day,
                "kind": kind,
                "amount": cents / 100,
                "balance": self._profile.balance / 100,
                "detail": detail,
            }
        )

    def _debit(self, kind, cents, detail):
        self._profile.balance -= cents
        self._record(kind, cents, detail)
        if self._profile.balance < self._rules.minimum:
            self._profile.state = "Suspended"

    def get_daily_limit(self):
        """Return the account-type transfer limit in dollars."""
        return self._rules.limit / 100

    def snapshot(self):
        """Read-only public view; no internal collections are exposed."""
        self.refresh_day()
        return {
            "account_type": self._profile.account_type,
            "balance": self._profile.balance / 100,
            "state": self._profile.state,
            "daily_transfer_total": self._daily_total / 100,
            "daily_limit": self.get_daily_limit(),
            "warning": self._profile.state == "Suspended",
            "transaction_count": len(self._ledger.transactions),
            "pending_count": len(self._ledger.scheduled),
            "owner": self._profile.owner,
        }

    @command
    def transfer(self, amount, destination="external"):
        """Debit a valid transfer and consume its share of the daily allowance."""
        self._require_state("Active")
        cents = self._positive(amount)
        if not isinstance(destination, str) or not destination.strip():
            raise ValueError("Invalid destination")
        self._funds(cents)
        if self._daily_total + cents > self._rules.limit:
            raise ValueError("Exceeds daily limit")
        self._daily_total += cents
        self._debit("transfer", cents, destination)
        return {"amount": cents / 100}

    @command
    def deposit(self, amount):
        """Credit funds and reactivate a suspended account at its minimum."""
        self._require_state("Active", "Suspended")
        cents = self._positive(amount)
        if self._profile.balance + cents > MAX_CENTS:
            raise ValueError("Balance exceeds maximum")
        self._profile.balance += cents
        if self._profile.balance >= self._rules.minimum:
            self._profile.state = "Active"
        self._record("deposit", cents, "deposit")
        return {"amount": cents / 100}

    @command
    def pay_bill(self, payee, amount, payment_date=None):
        """Pay a registered payee now or enqueue a validated future payment."""
        self._require_state("Active")
        cents = self._positive(amount)
        if payee not in PAYEES:
            raise ValueError("Invalid payee")
        due = self._day if payment_date is None else iso_date(payment_date)
        if due < self._day:
            raise ValueError("Payment date is in the past")
        self._funds(cents)
        if due > self._day:
            self._ledger.scheduled.append(
                {"date": due, "payee": payee, "amount": cents / 100}
            )
            return {"status": "scheduled"}
        self._debit("bill", cents, payee)
        return {"status": "paid"}

    @command
    def process_scheduled(self):
        """Attempt each due payment once, retaining payments due later."""
        self._require_state("Active", "Suspended", "Frozen")
        payments = []
        pending = []
        for payment in self._ledger.scheduled:
            if payment["date"] <= self._day:
                result = self.pay_bill(payment["payee"], payment["amount"])
                payments.append({**payment, "result": result})
            else:
                pending.append(payment)
        self._ledger.scheduled = pending
        return {"payments": payments}

    @command
    def process_fee(self):
        """Apply the first-day fee policy once per calendar month."""
        self._require_state("Active", "Suspended")
        month = self._day[:7]
        if self._day[-2:] != "01" or month in self._ledger.fee_months:
            return {"charged": 0}
        self._ledger.fee_months.add(month)
        fee = 0 if self._profile.balance > self._rules.waiver else self._rules.fee
        if self._profile.balance < fee:
            self._profile.state = "Suspended"
            raise ValueError("Insufficient fee funds")
        if fee:
            self._debit("fee", fee, "monthly fee")
        return {"charged": fee / 100}

    @command
    def freeze(self):
        """Freeze an Active account and reject subsequent monetary commands."""
        self._require_state("Active")
        self._profile.state = "Frozen"
        return {"state": self._profile.state}

    @command
    def unfreeze(self):
        """Restore a Frozen account to Active without reopening Closed accounts."""
        if self._profile.state == "Closed":
            raise ValueError("Account closed")
        if self._profile.state != "Frozen":
            raise ValueError("Account is not frozen")
        self._profile.state = "Active"
        return {"state": self._profile.state}

    @command
    def close(self):
        """Permanently close the account and return its final balance."""
        self._require_state("Active", "Suspended", "Frozen")
        self._profile.state = "Closed"
        return {"balance": self._profile.balance / 100}

    @command
    def update_info(self, owner):
        """Replace the owner name after checking state and nonempty input."""
        self._require_state("Active", "Suspended")
        if not isinstance(owner, str) or not owner.strip():
            raise ValueError("Invalid owner")
        self._profile.owner = owner.strip()
        return {"owner": self._profile.owner}

    def _history(self, start, end):
        iso_date(start)
        iso_date(end)
        if start > end:
            raise ValueError("Invalid date range")
        return [
            item.copy()
            for item in self._ledger.transactions
            if start <= item["date"] <= end
        ]

    @command
    def history(self, start, end):
        """Return independent transaction copies within an inclusive interval."""
        return {"transactions": self._history(start, end)}

    @command
    def export_csv(self, start, end):
        """Export filtered transactions with quoted details and exact cents."""
        rows = ["date,kind,amount,balance,detail"]
        for item in self._history(start, end):
            detail = item["detail"].replace('"', '""')
            rows.append(
                f'{item["date"]},{item["kind"]},{item["amount"]:.2f},'
                f'{item["balance"]:.2f},"{detail}"'
            )
        return {"csv": "\n".join(rows) + "\n"}
