"""In-memory banking contract; amounts use exact decimal cents and an injected clock."""

import csv
import io
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation

POLICIES = {
    "Savings": (Decimal("100"), Decimal("5"), Decimal("1000"), Decimal("2000")),
    "Checking": (Decimal("0"), Decimal("10"), Decimal("5000"), Decimal("5000")),
    "Premium": (Decimal("10000"), Decimal("0"), Decimal("0"), Decimal("50000")),
}


def money(value):
    """Reject nonfinite values, booleans and fractional cents without rounding."""
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError("Invalid amount") from exc
    if not result.is_finite() or result != result.quantize(Decimal("0.01")):
        raise ValueError("Invalid amount")
    return result


class BankAccount:
    """Public operations return snapshots/results; invalid requests raise ValueError."""

    def __init__(self, account_type, initial_balance, clock=None):
        if account_type not in POLICIES:
            raise ValueError("Invalid account type")
        self.account_type = account_type
        self.balance = money(initial_balance)
        if self.balance < 0:
            raise ValueError("Negative initial balance")
        self.clock = clock or (lambda: datetime.now(timezone.utc))
        self.state = "Active" if self.balance >= self.minimum else "Suspended"
        self.warning = self.state == "Suspended"
        self.info = {"name": "", "email": ""}
        self._daily_date = self.clock().date()
        self._daily_total = Decimal("0")
        self._history = []
        self._scheduled = []
        self._fee_months = set()

    @property
    def minimum(self):
        """Minimum balance for this account type."""
        return POLICIES[self.account_type][0]

    @property
    def daily_transfer_total(self):
        """Reset the observed total on the first access after midnight UTC."""
        today = self.clock().date()
        if today != self._daily_date:
            self._daily_date, self._daily_total = today, Decimal("0")
        return self._daily_total

    def get_daily_limit(self):
        """Return the contractual daily transfer cap."""
        return POLICIES[self.account_type][3]

    def view_balance(self):
        """Read-only access remains available in every state."""
        return self.balance

    def _require_active(self):
        if self.state != "Active":
            raise ValueError("Account is not Active")

    def _record(self, kind, amount):
        self._history.append(
            {
                "date": self.clock().date().isoformat(),
                "kind": kind,
                "amount": str(amount),
                "balance": str(self.balance),
            }
        )
        self.state = "Active" if self.balance >= self.minimum else "Suspended"
        self.warning = self.state == "Suspended"

    def _debit_amount(self, amount):
        self._require_active()
        amount = money(amount)
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        return amount

    def transfer(self, amount, recipient=None):
        """Debit an external transfer, or atomically credit another local account."""
        amount = self._debit_amount(amount)
        if amount + self.daily_transfer_total > self.get_daily_limit():
            raise ValueError("Exceeds daily limit")
        if recipient is not None:
            if recipient is self or recipient.state in ("Frozen", "Closed"):
                raise ValueError("Invalid recipient")
        self.balance -= amount
        self._daily_total += amount
        self._record("transfer", -amount)
        if recipient is not None:
            recipient.deposit(amount)
        return {"success": True}

    def deposit(self, amount):
        """Allow deposits to suspended accounts to restore their minimum balance."""
        if self.state in ("Frozen", "Closed"):
            raise ValueError("Account cannot receive deposits")
        amount = money(amount)
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.balance += amount
        self._record("deposit", amount)

    def update_info(self, name, email):
        """Update basic account information after validating the whole request."""
        if self.state in ("Frozen", "Closed"):
            raise ValueError("Account is read only")
        if (
            not isinstance(name, str)
            or not name.strip()
            or not isinstance(email, str)
            or "@" not in email
        ):
            raise ValueError("Invalid account information")
        self.info = {"name": name.strip(), "email": email}

    def freeze(self):
        """Freeze an active account on a customer or fraud request."""
        self._require_active()
        self.state = "Frozen"

    def unfreeze(self):
        """Represent an approved unfreeze request."""
        if self.state != "Frozen":
            raise ValueError("Account is not Frozen")
        self.state = "Active"

    def close(self):
        """Close permanently and return a final statement; repeated close is harmless."""
        self.state = "Closed"
        self.warning = False
        self._scheduled.clear()
        return {"balance": self.balance, "transactions": self.history()}

    def pay_bill(self, payee, amount, payment_date=None):
        """Validate now; future payments are revalidated when explicitly processed."""
        amount = self._debit_amount(amount)
        if payee not in ("electricity", "water", "credit_card"):
            raise ValueError("Invalid payee")
        due = payment_date or self.clock().date()
        if (
            not isinstance(due, date)
            or isinstance(due, datetime)
            or due < self.clock().date()
        ):
            raise ValueError("Invalid payment date")
        if due > self.clock().date():
            self._scheduled.append((payee, amount, due))
            return {"success": True, "scheduled": True}
        self.balance -= amount
        self._record("bill", -amount)
        return {"success": True, "scheduled": False}

    def process_scheduled(self):
        """Process each due payment once; report rejected payments without debiting."""
        results = []
        pending = self._scheduled
        self._scheduled = []
        for payee, amount, due in pending:
            if due > self.clock().date():
                self._scheduled.append((payee, amount, due))
                continue
            try:
                results.append(self.pay_bill(payee, amount))
            except ValueError as exc:
                results.append({"success": False, "error": str(exc)})
        return results

    def process_monthly_fee(self):
        """Assess at most once per month, only on day one; do not overdraw."""
        today = self.clock().date()
        month = (today.year, today.month)
        if (
            today.day != 1
            or month in self._fee_months
            or self.state in ("Frozen", "Closed")
        ):
            return Decimal("0")
        self._fee_months.add(month)
        _, fee, threshold, _ = POLICIES[self.account_type]
        if fee == 0 or self.balance > threshold:
            return Decimal("0")
        if self.balance < fee:
            self.state, self.warning = "Suspended", True
            return Decimal("0")
        self.balance -= fee
        self._record("fee", -fee)
        return fee

    def history(self, start=None, end=None):
        """Inclusive ISO date filtering, returning detached records."""
        if any(
            value is not None
            and (not isinstance(value, date) or isinstance(value, datetime))
            for value in (start, end)
        ):
            raise ValueError("Invalid date range")
        if start and end and start > end:
            raise ValueError("Invalid date range")
        return [
            dict(row)
            for row in self._history
            if (start is None or row["date"] >= start.isoformat())
            and (end is None or row["date"] <= end.isoformat())
        ]

    def export_csv(self, start=None, end=None):
        """Export the same public history selection with a stable header."""
        output = io.StringIO()
        writer = csv.DictWriter(
            output, fieldnames=("date", "kind", "amount", "balance")
        )
        writer.writeheader()
        writer.writerows(self.history(start, end))
        return output.getvalue()
