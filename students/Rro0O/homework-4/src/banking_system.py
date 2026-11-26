"""SecureBank online banking system: the system under test for homework 4.

Business rules implemented here come straight from the assignment statement:
account types (Savings / Checking / Premium), account states (Active / Frozen /
Suspended / Closed), transfers, bill payments, monthly fees and a filterable
transaction history that can be exported to CSV.

Every operation returns a result dictionary instead of raising, so callers (and
the black box tests) only depend on the observable behaviour:

    {"success": bool, "error": str | None, "errors": [str, ...], ...}
"""

import csv
import io
from datetime import date, datetime
from decimal import Decimal

ACCOUNT_TYPES = {
    "Savings": {"min_balance": 100, "monthly_fee": 5, "fee_waiver_above": 1000, "daily_limit": 2000},
    "Checking": {"min_balance": 0, "monthly_fee": 10, "fee_waiver_above": 5000, "daily_limit": 5000},
    "Premium": {"min_balance": 10000, "monthly_fee": 0, "fee_waiver_above": 0, "daily_limit": 50000},
}

STATE_ACTIVE = "Active"
STATE_FROZEN = "Frozen"
STATE_SUSPENDED = "Suspended"
STATE_CLOSED = "Closed"

# States in which money may move. Suspended accounts keep working (with a warning).
OPERABLE_STATES = (STATE_ACTIVE, STATE_SUSPENDED)

MIN_TRANSFER = Decimal("0.01")

VALID_PAYEES = {
    "CFE Electricity": "utilities",
    "Telmex Internet": "utilities",
    "SIAPA Water": "utilities",
    "Visa Credit Card": "credit card",
    "Mastercard Credit Card": "credit card",
}

CSV_HEADER = ["date", "type", "amount", "balance_after", "description"]


def parse_date(value):
    """Return a ``date`` for a date, datetime or ISO ``YYYY-MM-DD`` string; ``None`` if invalid."""
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            return None
    return None


def validate_amount(amount):
    """Validate a monetary amount.

    Returns ``(Decimal | None, error | None)``. Booleans, strings, NaN/infinity and
    values with more than two decimal places are rejected.
    """
    if isinstance(amount, bool) or not isinstance(amount, (int, float, Decimal)):
        return None, "Amount must be a number"
    value = Decimal(str(amount))
    if not value.is_finite():
        return None, "Amount must be a number"
    if value <= 0:
        return None, "Amount must be positive"
    if value != value.quantize(MIN_TRANSFER):
        return None, "Amount must have at most 2 decimal places"
    return value, None


def _money(value):
    """Convert a Decimal to a float rounded to cents."""
    return float(round(value, 2))


def _fail(*errors, **extra):
    """Build a failed result; ``error`` is the first (highest priority) message."""
    result = {"success": False, "error": errors[0], "errors": list(errors)}
    result.update(extra)
    return result


def _ok(**extra):
    """Build a successful result."""
    result = {"success": True, "error": None, "errors": []}
    result.update(extra)
    return result


class BankAccount:  # pylint: disable=too-many-instance-attributes
    """A SecureBank account with its balance, state and transaction history."""

    def __init__(self, account_type, initial_balance, owner="Customer", email=None):
        if account_type not in ACCOUNT_TYPES:
            raise ValueError(f"Invalid account type: {account_type!r}")
        if isinstance(initial_balance, bool) or not isinstance(initial_balance, (int, float, Decimal)):
            raise ValueError("Initial balance must be a number")
        minimum = ACCOUNT_TYPES[account_type]["min_balance"]
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")
        if initial_balance < minimum:
            raise ValueError(f"Initial balance is below the {account_type} minimum of {minimum}")
        if not isinstance(owner, str) or not owner.strip():
            raise ValueError("Owner name is required")
        self.account_type = account_type
        self.balance = float(initial_balance)
        self.owner = owner.strip()
        self.email = email
        self.state = STATE_ACTIVE
        self.daily_transfer_total = 0.0
        self.unpaid_fees = 0.0
        self.scheduled_payments = []
        self.transactions = []
        self._last_activity_day = None

    # ------------------------------------------------------------------ helpers
    def get_daily_limit(self):
        """Return the daily transfer limit for this account type."""
        return ACCOUNT_TYPES.get(self.account_type, {}).get("daily_limit", 0)

    def get_minimum_balance(self):
        """Return the minimum balance for this account type."""
        return ACCOUNT_TYPES[self.account_type]["min_balance"]

    def _reset_daily_total_if_new_day(self, day):
        """The daily limit resets at midnight, i.e. whenever the calendar day changes."""
        if self._last_activity_day != day:
            self.daily_transfer_total = 0.0
            self._last_activity_day = day

    def _record(self, day, kind, amount, description):
        self.transactions.append(
            {
                "date": day,
                "type": kind,
                "amount": amount,
                "balance_after": self.balance,
                "description": description,
            }
        )

    def _refresh_state_after_balance_change(self):
        """Apply the Active <-> Suspended transitions caused by balance changes.

        Returns a warning message when the account has just become Suspended.
        """
        below_minimum = self.balance < self.get_minimum_balance()
        if self.state == STATE_ACTIVE and below_minimum:
            self.state = STATE_SUSPENDED
            return "Balance is below the minimum: account suspended"
        if self.state == STATE_SUSPENDED and not below_minimum:
            self.state = STATE_ACTIVE
        return None

    def _state_error(self):
        """Return the error for accounts that cannot move money, else ``None``."""
        if self.state == STATE_FROZEN:
            return "Account is frozen"
        if self.state == STATE_CLOSED:
            return "Account is closed"
        return None

    def _debit(self, amount, day, kind, description):
        """Remove ``amount`` (Decimal) from the balance and record it. Returns a warning or ``None``."""
        self.balance = _money(Decimal(str(self.balance)) - amount)
        warning = self._refresh_state_after_balance_change()
        self._record(day, kind, -_money(amount), description)
        return warning

    # ------------------------------------------------------------------- money
    def transfer(self, amount, destination=None, on_date=None):
        """Transfer money out of this account.

        ``destination`` may be another ``BankAccount`` (own accounts), an external
        account number (another bank) or ``None``. Errors are collected so the
        decision table can be checked rule by rule.
        """
        day = parse_date(on_date) or date.today()
        state_error = self._state_error()
        if state_error:
            return _fail(state_error)
        value, amount_error = validate_amount(amount)
        if amount_error:
            return _fail(amount_error)
        if destination is self:
            return _fail("Cannot transfer to the same account")

        self._reset_daily_total_if_new_day(day)
        errors = []
        if Decimal(str(self.daily_transfer_total)) + value > self.get_daily_limit():
            errors.append("Exceeds daily limit")
        if value > Decimal(str(self.balance)):
            errors.append("Insufficient funds")
        if isinstance(destination, BankAccount) and destination.state not in OPERABLE_STATES:
            errors.append("Destination account cannot receive funds")
        if errors:
            return _fail(*errors)

        self.daily_transfer_total = _money(Decimal(str(self.daily_transfer_total)) + value)
        label = destination.owner if isinstance(destination, BankAccount) else (destination or "external account")
        warning = self._debit(value, day, "transfer", f"Transfer to {label}")
        if isinstance(destination, BankAccount):
            destination.deposit(float(value), on_date=day, description=f"Transfer from {self.owner}")
        return _ok(warning=warning, state=self.state, balance=self.balance)

    def deposit(self, amount, on_date=None, description="Deposit"):
        """Add money to the account. A deposit that restores the minimum reactivates a Suspended account."""
        day = parse_date(on_date) or date.today()
        state_error = self._state_error()
        if state_error:
            return _fail(state_error)
        value, amount_error = validate_amount(amount)
        if amount_error:
            return _fail(amount_error)
        self.balance = _money(Decimal(str(self.balance)) + value)
        self._refresh_state_after_balance_change()
        self._record(day, "deposit", _money(value), description)
        return _ok(state=self.state, balance=self.balance)

    def pay_bill(self, payee, amount, payment_date=None, on_date=None):
        """Pay a registered payee now, or schedule the payment for a future date."""
        today = parse_date(on_date) or date.today()
        state_error = self._state_error()
        if state_error:
            return _fail(state_error)
        errors = []
        if not isinstance(payee, str) or not payee.strip():
            errors.append("Payee is required")
        elif payee.strip() not in VALID_PAYEES:
            errors.append("Invalid payee")
        value, amount_error = validate_amount(amount)
        if amount_error:
            errors.append(amount_error)
        elif value > Decimal(str(self.balance)):
            errors.append("Insufficient funds")
        due = today if payment_date is None else parse_date(payment_date)
        if due is None:
            errors.append("Invalid payment date")
        elif due < today:
            errors.append("Payment date cannot be in the past")
        if errors:
            return _fail(*errors)

        payee = payee.strip()
        if due > today:
            self.scheduled_payments.append({"payee": payee, "amount": _money(value), "date": due})
            return _ok(scheduled=True, payment_date=due, balance=self.balance)
        warning = self._debit(value, today, "bill payment", f"Bill payment to {payee}")
        return _ok(scheduled=False, warning=warning, state=self.state, balance=self.balance)

    def process_monthly_fee(self, on_date):
        """Charge the monthly fee (only on the 1st of the month, waived above the threshold)."""
        day = parse_date(on_date)
        if day is None:
            return _fail("Invalid date")
        if self.state not in OPERABLE_STATES:
            return _fail(f"Fees are not processed for {self.state} accounts")
        if day.day != 1:
            return _fail("Monthly fees are only charged on the 1st of the month")

        rules = ACCOUNT_TYPES[self.account_type]
        fee = Decimal(str(rules["monthly_fee"]))
        waived = fee == 0 or self.balance > rules["fee_waiver_above"]
        if waived:
            return _ok(fee_charged=0.0, waived=True, state=self.state, balance=self.balance)
        if Decimal(str(self.balance)) < fee:
            self.unpaid_fees = _money(Decimal(str(self.unpaid_fees)) + fee)
            self.state = STATE_SUSPENDED
            return _ok(fee_charged=0.0, waived=False, suspended=True, state=self.state, balance=self.balance)
        warning = self._debit(fee, day, "fee", "Monthly fee")
        return _ok(fee_charged=float(fee), waived=False, warning=warning, state=self.state, balance=self.balance)

    # --------------------------------------------------------- account lifecycle
    def freeze(self, reason="customer request"):
        """Active -> Frozen (customer request or fraud detection)."""
        if self.state != STATE_ACTIVE:
            return _fail(f"Cannot freeze an account in state {self.state}")
        self.state = STATE_FROZEN
        return _ok(state=self.state, reason=reason)

    def unfreeze(self):
        """Frozen -> Active."""
        if self.state != STATE_FROZEN:
            return _fail(f"Cannot unfreeze an account in state {self.state}")
        self.state = STATE_ACTIVE
        return _ok(state=self.state)

    def close(self):
        """Any state -> Closed. Closed accounts can never be reopened."""
        if self.state == STATE_CLOSED:
            return _fail("Account is closed")
        self.state = STATE_CLOSED
        statement = {"owner": self.owner, "final_balance": self.balance, "transactions": len(self.transactions)}
        return _ok(state=self.state, final_statement=statement)

    def reopen(self):
        """Closed accounts cannot be reopened; every other state is left untouched."""
        if self.state == STATE_CLOSED:
            return _fail("Account is closed")
        return _fail("Account is not closed")

    def update_info(self, owner=None, email=None):
        """Update the owner name and/or e-mail. Not allowed on closed accounts."""
        if self.state == STATE_CLOSED:
            return _fail("Account is closed")
        errors = []
        if owner is not None and (not isinstance(owner, str) or not owner.strip()):
            errors.append("Owner name is required")
        if email is not None and (not isinstance(email, str) or "@" not in email):
            errors.append("Invalid e-mail address")
        if errors:
            return _fail(*errors)
        if owner is not None:
            self.owner = owner.strip()
        if email is not None:
            self.email = email
        return _ok(owner=self.owner, email=self.email)

    def get_balance(self):
        """View the balance (allowed in every state, including Frozen)."""
        return self.balance

    # ------------------------------------------------------------ history / CSV
    def get_history(self, start=None, end=None):
        """Return the transactions between ``start`` and ``end`` (both inclusive, both optional).

        Raises ``ValueError`` for unparsable dates or when ``start`` is after ``end``.
        """
        first = parse_date(start) if start is not None else None
        last = parse_date(end) if end is not None else None
        if (start is not None and first is None) or (end is not None and last is None):
            raise ValueError("Invalid date")
        if first and last and first > last:
            raise ValueError("Start date must not be after end date")
        return [
            tx
            for tx in self.transactions
            if (first is None or tx["date"] >= first) and (last is None or tx["date"] <= last)
        ]

    def export_csv(self, start=None, end=None):
        """Export the (optionally filtered) history as CSV text."""
        buffer = io.StringIO()
        writer = csv.writer(buffer, lineterminator="\n")
        writer.writerow(CSV_HEADER)
        for tx in self.get_history(start, end):
            writer.writerow(
                [
                    tx["date"].isoformat(),
                    tx["type"],
                    f"{tx['amount']:.2f}",
                    f"{tx['balance_after']:.2f}",
                    tx["description"],
                ]
            )
        return buffer.getvalue()
