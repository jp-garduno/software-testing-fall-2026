"""SecureBank Online Banking System.

Core domain model used as the system under test for the Homework 4 black box
test suite (Equivalence Partitioning, Boundary Value Analysis, Decision
Tables, and State Transition Testing).
"""

from datetime import date

ACCOUNT_RULES = {
    "Savings": {
        "min_balance": 100,
        "monthly_fee": 5,
        "fee_waiver_threshold": 1000,
        "daily_limit": 2000,
    },
    "Checking": {
        "min_balance": 0,
        "monthly_fee": 10,
        "fee_waiver_threshold": 5000,
        "daily_limit": 5000,
    },
    "Premium": {
        "min_balance": 10000,
        "monthly_fee": 0,
        "fee_waiver_threshold": 0,
        "daily_limit": 50000,
    },
}

VALID_ACCOUNT_TYPES = set(ACCOUNT_RULES)
VALID_STATES = {"Active", "Frozen", "Suspended", "Closed"}


class BankAccount:
    """A single SecureBank account and the operations that mutate its state."""

    def __init__(self, account_type, initial_balance, today=None):
        if account_type not in VALID_ACCOUNT_TYPES:
            raise ValueError(f"Unknown account type: {account_type}")

        self.account_type = account_type
        self.balance = round(float(initial_balance), 2)
        self.state = "Active"
        self.daily_transfer_total = 0.0
        self._last_transfer_date = today or date.today()
        self.history = []

        if self.balance < self._rules()["min_balance"]:
            self.state = "Suspended"

    def _rules(self):
        return ACCOUNT_RULES[self.account_type]

    def get_daily_limit(self):
        """Daily transfer limit for this account's type."""
        return self._rules()["daily_limit"]

    def get_min_balance(self):
        """Minimum balance required for this account's type."""
        return self._rules()["min_balance"]

    def _reset_daily_limit_if_new_day(self, today=None):
        today = today or date.today()
        if today != self._last_transfer_date:
            self.daily_transfer_total = 0.0
            self._last_transfer_date = today

    def transfer(self, amount, today=None):
        """Transfer money out of this account, applying all transfer validation rules."""
        self._reset_daily_limit_if_new_day(today)

        if self.state in ("Frozen", "Closed"):
            return {
                "success": False,
                "error": f"Account is {self.state.lower()}; transfers not allowed",
            }

        if amount <= 0:
            return {"success": False, "error": "Amount must be positive"}

        amount = round(float(amount), 2)

        if amount > self.balance:
            return {"success": False, "error": "Insufficient funds"}

        if round(self.daily_transfer_total + amount, 2) > self.get_daily_limit():
            return {"success": False, "error": "Exceeds daily limit"}

        self.balance = round(self.balance - amount, 2)
        self.daily_transfer_total = round(self.daily_transfer_total + amount, 2)
        self.history.append(("transfer", amount))

        if self.balance < self.get_min_balance():
            self.state = "Suspended"

        return {"success": True, "balance": self.balance}

    def deposit(self, amount):
        """Deposit money into this account; can restore a Suspended account to Active."""
        if self.state == "Closed":
            return {"success": False, "error": "Account is closed"}
        if amount <= 0:
            return {"success": False, "error": "Amount must be positive"}

        self.balance = round(self.balance + amount, 2)
        self.history.append(("deposit", amount))

        if self.state == "Suspended" and self.balance >= self.get_min_balance():
            self.state = "Active"

        return {"success": True, "balance": self.balance}

    def freeze(self):
        """Freeze the account (customer request or fraud detection)."""
        if self.state == "Closed":
            return {"success": False, "error": "Cannot freeze a closed account"}
        self.state = "Frozen"
        return {"success": True, "state": self.state}

    def unfreeze(self):
        """Lift a freeze. Lands on Active or Suspended depending on current balance."""
        if self.state != "Frozen":
            return {"success": False, "error": "Account is not frozen"}
        self.state = "Active" if self.balance >= self.get_min_balance() else "Suspended"
        return {"success": True, "state": self.state}

    def close(self):
        """Close the account permanently. Closed accounts cannot be reopened."""
        if self.state == "Closed":
            return {"success": False, "error": "Account already closed"}
        self.state = "Closed"
        return {"success": True, "state": self.state}

    def apply_monthly_fee(self):
        """Charge the monthly fee unless the balance is above the waiver threshold."""
        if self.state == "Closed":
            return {"success": False, "error": "Account is closed"}

        rules = self._rules()
        if rules["monthly_fee"] == 0:
            return {"success": True, "charged": 0.0}

        if self.balance > rules["fee_waiver_threshold"]:
            return {"success": True, "charged": 0.0, "waived": True}

        if self.balance < rules["monthly_fee"]:
            self.state = "Suspended"
            return {
                "success": False,
                "error": "Insufficient funds for fee",
                "state": self.state,
            }

        self.balance = round(self.balance - rules["monthly_fee"], 2)
        if self.balance < rules["min_balance"]:
            self.state = "Suspended"
        return {"success": True, "charged": rules["monthly_fee"]}


def validate_account_type(account_type):
    """Equivalence-partitioned validation of the account type input."""
    if account_type in VALID_ACCOUNT_TYPES:
        return {"success": True}
    return {"success": False, "error": f"Invalid account type: {account_type}"}


def validate_bill_payment(account, payee, amount):
    """Validate a bill payment: payee, amount, funds, and account state."""
    if account.state in ("Frozen", "Closed"):
        return {"success": False, "error": f"Account is {account.state.lower()}"}
    if not payee or not str(payee).strip():
        return {"success": False, "error": "Invalid payee"}
    if amount <= 0:
        return {"success": False, "error": "Amount must be positive"}
    if amount > account.balance:
        return {"success": False, "error": "Insufficient funds"}
    return {"success": True}


def filter_transactions_by_date(transactions, start_date, end_date):
    """Filter (date, ...) transaction tuples to the inclusive [start_date, end_date] range."""
    if start_date > end_date:
        return {"success": False, "error": "start_date must not be after end_date"}
    filtered = [t for t in transactions if start_date <= t[0] <= end_date]
    return {"success": True, "transactions": filtered}
