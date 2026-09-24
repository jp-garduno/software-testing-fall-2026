"""SecureBank online banking domain model.

The module is the system under test for Homework 4. It implements the account types, account
states, transfer rules, bill payment rules, monthly fee processing and transaction history
described in the assignment brief, plus the assumptions documented in
``design/test-design-document.md``.

Money is handled internally as an integer number of cents so that amounts such as $0.01 and
$4,999.99 compare exactly; the public API keeps working in dollars.
"""

from datetime import date
from decimal import Decimal, InvalidOperation

ACCOUNT_RULES = {
    "Savings": {"min_balance": 100.00, "monthly_fee": 5.00, "fee_waiver": 1000.00, "daily_limit": 2000.00},
    "Checking": {"min_balance": 0.00, "monthly_fee": 10.00, "fee_waiver": 5000.00, "daily_limit": 5000.00},
    "Premium": {"min_balance": 10000.00, "monthly_fee": 0.00, "fee_waiver": 0.00, "daily_limit": 50000.00},
}

ACTIVE = "Active"
FROZEN = "Frozen"
SUSPENDED = "Suspended"
CLOSED = "Closed"

OPERABLE_STATES = (ACTIVE, SUSPENDED)

ERR_INVALID_TYPE = "Unknown account type"
ERR_INVALID_AMOUNT = "Amount must be numeric"
ERR_AMOUNT_PRECISION = "Amount must be specified in whole cents"
ERR_AMOUNT_POSITIVE = "Amount must be positive"
ERR_DAILY_LIMIT = "Exceeds daily limit"
ERR_INSUFFICIENT = "Insufficient funds"
ERR_FROZEN = "Account frozen"
ERR_CLOSED = "Account closed"
ERR_OPENING_DEPOSIT = "Initial deposit below minimum balance"
ERR_UNKNOWN_PAYEE = "Unknown payee"
ERR_INACTIVE_PAYEE = "Payee is not active"
ERR_PAST_DATE = "Scheduled date cannot be in the past"
ERR_DATE_ORDER = "Start date must not be after end date"
ERR_DATE_TYPE = "Date range must use date objects"

WARN_BELOW_MINIMUM = "Balance is below the minimum for this account type"


def to_cents(amount):
    """Convert a dollar amount to an integer number of cents.

    Raises ``ValueError`` when the amount is not numeric or carries sub-cent precision.
    """
    if isinstance(amount, bool) or not isinstance(amount, (int, float, str, Decimal)):
        raise ValueError(ERR_INVALID_AMOUNT)
    try:
        value = Decimal(str(amount))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(ERR_INVALID_AMOUNT) from exc
    if not value.is_finite():
        raise ValueError(ERR_INVALID_AMOUNT)
    if -value.as_tuple().exponent > 2:
        raise ValueError(ERR_AMOUNT_PRECISION)
    return int(value.scaleb(2).to_integral_value())


def to_dollars(cents):
    """Convert an integer number of cents back to a dollar amount."""
    return round(cents / 100, 2)


def failure(error):
    """Build the standard failure envelope returned by every operation."""
    return {"success": False, "error": error}


class Payee:
    """A bill payment recipient registered by the customer."""

    def __init__(self, payee_id, name, active=True):
        self.payee_id = payee_id
        self.name = name
        self.active = active


class BankAccount:
    """A SecureBank account with its balance, state and daily transfer usage."""

    def __init__(self, account_type, initial_balance, state=ACTIVE):
        if account_type not in ACCOUNT_RULES:
            raise ValueError(ERR_INVALID_TYPE)
        self.account_type = account_type
        self._balance_cents = to_cents(initial_balance)
        self.state = state
        self._daily_transfer_cents = 0
        self.transactions = []
        self.payees = {}
        self.notifications = []

    @property
    def balance(self):
        """Current balance in dollars."""
        return to_dollars(self._balance_cents)

    @property
    def daily_transfer_total(self):
        """Dollars already transferred out of this account today."""
        return to_dollars(self._daily_transfer_cents)

    def get_daily_limit(self):
        """Daily transfer limit in dollars for this account type."""
        return ACCOUNT_RULES[self.account_type]["daily_limit"]

    def get_minimum_balance(self):
        """Minimum balance in dollars for this account type."""
        return ACCOUNT_RULES[self.account_type]["min_balance"]

    def get_monthly_fee(self):
        """Monthly maintenance fee in dollars for this account type."""
        return ACCOUNT_RULES[self.account_type]["monthly_fee"]

    def get_fee_waiver_threshold(self):
        """Balance above which the monthly fee is waived."""
        return ACCOUNT_RULES[self.account_type]["fee_waiver"]

    def is_below_minimum(self):
        """Whether the current balance sits under the account-type minimum."""
        return self._balance_cents < to_cents(self.get_minimum_balance())

    def register_payee(self, payee_id, name, active=True):
        """Register a bill payment recipient and return it."""
        payee = Payee(payee_id, name, active)
        self.payees[payee_id] = payee
        return payee

    def reset_daily_limit(self):
        """Clear the accumulated daily transfer total, as the midnight job does."""
        self._daily_transfer_cents = 0

    def transfer(self, amount, destination="external"):
        """Move money out of this account, applying the transfer validation rules."""
        blocked = self._state_guard()
        if blocked:
            return blocked
        try:
            amount_cents = to_cents(amount)
        except ValueError as exc:
            return failure(str(exc))
        if amount_cents <= 0:
            return failure(ERR_AMOUNT_POSITIVE)
        if self._daily_transfer_cents + amount_cents > to_cents(self.get_daily_limit()):
            return failure(ERR_DAILY_LIMIT)
        if amount_cents > self._balance_cents:
            return failure(ERR_INSUFFICIENT)

        self._balance_cents -= amount_cents
        self._daily_transfer_cents += amount_cents
        self._record("transfer", amount_cents, destination)
        return self._success({"amount": to_dollars(amount_cents), "destination": destination})

    def pay_bill(self, payee_id, amount, scheduled_date=None, today=None):
        """Pay a registered payee immediately or schedule the payment for a future date."""
        blocked = self._state_guard()
        if blocked:
            return blocked
        payee = self.payees.get(payee_id)
        if payee is None:
            return failure(ERR_UNKNOWN_PAYEE)
        if not payee.active:
            return failure(ERR_INACTIVE_PAYEE)
        try:
            amount_cents = to_cents(amount)
        except ValueError as exc:
            return failure(str(exc))
        if amount_cents <= 0:
            return failure(ERR_AMOUNT_POSITIVE)
        today = today or date.today()
        if scheduled_date is not None and scheduled_date < today:
            return failure(ERR_PAST_DATE)
        if amount_cents > self._balance_cents:
            return failure(ERR_INSUFFICIENT)

        if scheduled_date is not None and scheduled_date > today:
            self._record("scheduled_payment", amount_cents, payee.name, when=scheduled_date)
            return self._success({"scheduled": True, "date": scheduled_date, "amount": to_dollars(amount_cents)})

        self._balance_cents -= amount_cents
        self._record("bill_payment", amount_cents, payee.name, when=today)
        return self._success({"scheduled": False, "amount": to_dollars(amount_cents)})

    def deposit(self, amount):
        """Add money to the account and restore it to Active when the minimum is met again."""
        if self.state == CLOSED:
            return failure(ERR_CLOSED)
        if self.state == FROZEN:
            return failure(ERR_FROZEN)
        try:
            amount_cents = to_cents(amount)
        except ValueError as exc:
            return failure(str(exc))
        if amount_cents <= 0:
            return failure(ERR_AMOUNT_POSITIVE)

        self._balance_cents += amount_cents
        self._record("deposit", amount_cents, "self")
        if self.state == SUSPENDED and not self.is_below_minimum():
            self.state = ACTIVE
        return self._success({"amount": to_dollars(amount_cents)})

    def apply_monthly_fee(self):
        """Charge the monthly maintenance fee, honouring the balance waiver."""
        if self.state == CLOSED:
            return failure(ERR_CLOSED)
        fee_cents = to_cents(self.get_monthly_fee())
        if fee_cents == 0:
            return self._success({"charged": 0.00, "waived": True})
        if self._balance_cents > to_cents(self.get_fee_waiver_threshold()):
            return self._success({"charged": 0.00, "waived": True})
        if fee_cents > self._balance_cents:
            self.state = SUSPENDED
            self.notifications.append(ERR_INSUFFICIENT)
            return failure(ERR_INSUFFICIENT)

        self._balance_cents -= fee_cents
        self._record("monthly_fee", fee_cents, "SecureBank")
        return self._success({"charged": to_dollars(fee_cents), "waived": False})

    def freeze(self):
        """Move an operable account to Frozen."""
        if self.state == CLOSED:
            return failure(ERR_CLOSED)
        self.state = FROZEN
        return self._success({"state": self.state})

    def unfreeze(self):
        """Return a Frozen account to Active, or Suspended when it is below the minimum."""
        if self.state == CLOSED:
            return failure(ERR_CLOSED)
        if self.state != FROZEN:
            return failure("Account is not frozen")
        self.state = SUSPENDED if self.is_below_minimum() else ACTIVE
        return self._success({"state": self.state})

    def close(self):
        """Close the account from any state; closed accounts cannot be reopened."""
        if self.state == CLOSED:
            return failure(ERR_CLOSED)
        self.state = CLOSED
        return self._success({"state": self.state, "final_statement": self.export_csv()})

    def get_transactions(self, start_date=None, end_date=None):
        """Return the transaction history, optionally filtered by an inclusive date range."""
        for bound in (start_date, end_date):
            if bound is not None and not isinstance(bound, date):
                return failure(ERR_DATE_TYPE)
        if start_date is not None and end_date is not None and start_date > end_date:
            return failure(ERR_DATE_ORDER)
        rows = [
            row
            for row in self.transactions
            if (start_date is None or row["date"] >= start_date) and (end_date is None or row["date"] <= end_date)
        ]
        return self._success({"transactions": rows, "count": len(rows)})

    def export_csv(self):
        """Render the full transaction history as CSV text."""
        lines = ["date,type,amount,counterparty"]
        for row in self.transactions:
            lines.append(f"{row['date'].isoformat()},{row['type']},{row['amount']:.2f},{row['counterparty']}")
        return "\n".join(lines)

    def _state_guard(self):
        """Reject money movement from accounts that are Frozen or Closed."""
        if self.state == CLOSED:
            return failure(ERR_CLOSED)
        if self.state == FROZEN:
            return failure(ERR_FROZEN)
        return None

    def _success(self, payload):
        """Build the standard success envelope, suspending the account when it fell too low."""
        warnings = []
        if self.state in OPERABLE_STATES and self.is_below_minimum():
            if self.state == ACTIVE:
                self.notifications.append(WARN_BELOW_MINIMUM)
            self.state = SUSPENDED
            warnings.append(WARN_BELOW_MINIMUM)
        result = {"success": True, "state": self.state, "balance": self.balance, "warnings": warnings}
        result.update(payload)
        return result

    def _record(self, kind, amount_cents, counterparty, when=None):
        """Append an entry to the transaction history."""
        self.transactions.append(
            {
                "date": when or date.today(),
                "type": kind,
                "amount": to_dollars(amount_cents),
                "counterparty": counterparty,
            }
        )


def create_account(account_type, initial_balance):
    """Open a new account, enforcing the account type and opening deposit rules."""
    if account_type not in ACCOUNT_RULES:
        return failure(ERR_INVALID_TYPE)
    try:
        balance_cents = to_cents(initial_balance)
    except ValueError as exc:
        return failure(str(exc))
    if balance_cents < 0:
        return failure(ERR_AMOUNT_POSITIVE)
    if balance_cents < to_cents(ACCOUNT_RULES[account_type]["min_balance"]):
        return failure(ERR_OPENING_DEPOSIT)
    account = BankAccount(account_type, to_dollars(balance_cents))
    return {"success": True, "account": account, "state": account.state, "balance": account.balance}
