"""SecureBank online banking system.

System under test for Homework 4. The rules implemented here come from the
assignment brief: three account types with their own minimum balance, monthly
fee and daily transfer limit, four account states, transfers, bill payments and
a transaction history that can be filtered and exported.
"""

from datetime import date

ACCOUNT_RULES = {
    "Savings": {"minimum_balance": 100.0, "monthly_fee": 5.0, "fee_waiver": 1000.0, "daily_limit": 2000.0},
    "Checking": {"minimum_balance": 0.0, "monthly_fee": 10.0, "fee_waiver": 5000.0, "daily_limit": 5000.0},
    "Premium": {"minimum_balance": 10000.0, "monthly_fee": 0.0, "fee_waiver": 0.0, "daily_limit": 50000.0},
}

MINIMUM_TRANSFER = 0.01
VALID_STATES = ("Active", "Frozen", "Suspended", "Closed")

# Transfers are blocked from Frozen and Closed accounts only. The brief says
# "cannot transfer from Frozen or Closed accounts" and describes Suspended as
# "warnings shown", so a suspended account keeps operating and is warned.
TRANSACTIONAL_STATES = ("Active", "Suspended")


def _round_money(amount):
    """Round to cents so repeated float arithmetic cannot drift."""
    return round(amount + 0.0, 2)


class BankAccount:
    """A single customer account with its balance, state and daily usage."""

    def __init__(self, account_type, initial_balance, state="Active"):
        if account_type not in ACCOUNT_RULES:
            raise ValueError(f"Unknown account type: {account_type}")
        if state not in VALID_STATES:
            raise ValueError(f"Unknown account state: {state}")
        self.account_type = account_type
        self.balance = _round_money(initial_balance)
        self.state = state
        self.daily_transfer_total = 0.0
        self.transactions = []

    # ----- helpers -------------------------------------------------------

    def get_daily_limit(self):
        """Return the daily transfer limit for this account type."""
        return ACCOUNT_RULES[self.account_type]["daily_limit"]

    def get_minimum_balance(self):
        """Return the minimum balance this account type must keep."""
        return ACCOUNT_RULES[self.account_type]["minimum_balance"]

    def get_monthly_fee(self):
        """Return the monthly fee charged to this account type."""
        return ACCOUNT_RULES[self.account_type]["monthly_fee"]

    def remaining_daily_limit(self):
        """Return how much can still be transferred today."""
        return _round_money(self.get_daily_limit() - self.daily_transfer_total)

    def reset_daily_limit(self):
        """Clear the daily transfer total. Runs at midnight in production."""
        self.daily_transfer_total = 0.0

    def _record(self, kind, amount, when=None, payee=None):
        """Append an entry to the transaction history."""
        self.transactions.append(
            {"type": kind, "amount": _round_money(amount), "date": when or date.today(), "payee": payee}
        )

    def _apply_balance_state(self):
        """Move between Active and Suspended according to the minimum balance.

        Frozen and Closed accounts are left alone: those states are set by an
        explicit request and the balance must not override them.
        """
        if self.state in ("Frozen", "Closed"):
            return
        if self.balance < self.get_minimum_balance():
            self.state = "Suspended"
        else:
            self.state = "Active"

    @staticmethod
    def _amount_error(amount):
        """Return why an amount is unusable, or None when it is fine."""
        if not isinstance(amount, (int, float)) or isinstance(amount, bool):
            return "Amount must be a number"
        if amount < MINIMUM_TRANSFER:
            return "Amount must be positive"
        return None

    # ----- money movement ------------------------------------------------

    def transfer(self, amount):
        """Transfer money out of this account.

        Returns a dict with ``success`` and either ``error`` or ``warning``.
        Validation order is state, then amount, then daily limit, then funds.
        """
        if self.state not in TRANSACTIONAL_STATES:
            return {"success": False, "error": f"Account is {self.state.lower()}"}
        error = self._amount_error(amount)
        if error:
            return {"success": False, "error": error}
        if _round_money(self.daily_transfer_total + amount) > self.get_daily_limit():
            return {"success": False, "error": "Exceeds daily limit"}
        if amount > self.balance:
            return {"success": False, "error": "Insufficient funds"}

        self.balance = _round_money(self.balance - amount)
        self.daily_transfer_total = _round_money(self.daily_transfer_total + amount)
        self._record("transfer", -amount)
        previous_state = self.state
        self._apply_balance_state()

        result = {"success": True, "balance": self.balance}
        if self.state == "Suspended":
            result["warning"] = "Balance below minimum"
            if previous_state == "Active":
                result["state_changed"] = True
        return result

    def deposit(self, amount):
        """Add money to the account and re-evaluate its state."""
        if self.state == "Closed":
            return {"success": False, "error": "Account is closed"}
        if self.state == "Frozen":
            return {"success": False, "error": "Account is frozen"}
        error = self._amount_error(amount)
        if error:
            return {"success": False, "error": error}

        self.balance = _round_money(self.balance + amount)
        self._record("deposit", amount)
        self._apply_balance_state()
        return {"success": True, "balance": self.balance, "state": self.state}

    def pay_bill(self, payee, amount, scheduled_date=None):
        """Pay a bill immediately or schedule it for a future date."""
        if self.state not in TRANSACTIONAL_STATES:
            return {"success": False, "error": f"Account is {self.state.lower()}"}
        if not payee or not str(payee).strip():
            return {"success": False, "error": "Invalid payee"}
        error = self._amount_error(amount)
        if error:
            return {"success": False, "error": error}
        if scheduled_date is not None and scheduled_date < date.today():
            return {"success": False, "error": "Scheduled date is in the past"}
        if amount > self.balance:
            return {"success": False, "error": "Insufficient funds"}

        is_future = scheduled_date is not None and scheduled_date > date.today()
        if is_future:
            self._record("scheduled_payment", -amount, when=scheduled_date, payee=payee)
        else:
            self.balance = _round_money(self.balance - amount)
            self._record("payment", -amount, payee=payee)
            self._apply_balance_state()
        return {"success": True, "scheduled": is_future, "balance": self.balance}

    # ----- lifecycle -----------------------------------------------------

    def freeze(self):
        """Freeze the account by customer request or fraud detection."""
        if self.state == "Closed":
            return {"success": False, "error": "Account is closed"}
        self.state = "Frozen"
        return {"success": True, "state": self.state}

    def unfreeze(self):
        """Release a frozen account and re-evaluate it against the minimum."""
        if self.state != "Frozen":
            return {"success": False, "error": "Account is not frozen"}
        self.state = "Active"
        self._apply_balance_state()
        return {"success": True, "state": self.state}

    def close(self):
        """Close the account. A closed account can never be reopened."""
        if self.state == "Closed":
            return {"success": False, "error": "Account is closed"}
        self.state = "Closed"
        return {"success": True, "state": self.state, "final_statement": True}

    def apply_monthly_fee(self):
        """Charge the monthly fee on the 1st, unless it is waived."""
        if self.state == "Closed":
            return {"success": False, "error": "Account is closed"}

        fee = self.get_monthly_fee()
        waiver = ACCOUNT_RULES[self.account_type]["fee_waiver"]
        if fee == 0 or self.balance > waiver:
            return {"success": True, "charged": 0.0, "waived": True, "state": self.state}
        if self.balance < fee:
            self.state = "Suspended"
            return {"success": False, "error": "Insufficient funds for fee", "state": self.state}

        self.balance = _round_money(self.balance - fee)
        self._record("fee", -fee)
        self._apply_balance_state()
        return {"success": True, "charged": fee, "waived": False, "state": self.state}

    # ----- history -------------------------------------------------------

    def get_transaction_history(self, start_date=None, end_date=None):
        """Return the transactions inside an inclusive date range."""
        if start_date and end_date and start_date > end_date:
            raise ValueError("Start date must not be after end date")
        entries = self.transactions
        if start_date:
            entries = [entry for entry in entries if entry["date"] >= start_date]
        if end_date:
            entries = [entry for entry in entries if entry["date"] <= end_date]
        return entries

    def export_history_csv(self, start_date=None, end_date=None):
        """Export the filtered history as CSV text with a header row."""
        rows = ["date,type,amount,payee"]
        for entry in self.get_transaction_history(start_date, end_date):
            rows.append(
                f"{entry['date'].isoformat()},{entry['type']},{entry['amount']},{entry['payee'] or ''}"
            )
        return "\n".join(rows)
