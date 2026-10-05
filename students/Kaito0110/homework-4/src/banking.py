"""SecureBank Online Banking System - System Under Test."""

# pylint: disable=too-many-instance-attributes,too-many-return-statements

from datetime import date, datetime
from enum import Enum


class AccountType(Enum):
    """Types of bank accounts available."""

    SAVINGS = "savings"
    CHECKING = "checking"
    PREMIUM = "premium"


class AccountState(Enum):
    """Possible states of a bank account."""

    ACTIVE = "active"
    FROZEN = "frozen"
    SUSPENDED = "suspended"
    CLOSED = "closed"


# Account configuration constants
ACCOUNT_CONFIG = {
    AccountType.SAVINGS: {
        "min_balance": 100.0,
        "monthly_fee": 5.0,
        "fee_waiver_threshold": 1000.0,
        "daily_transfer_limit": 2000.0,
    },
    AccountType.CHECKING: {
        "min_balance": 0.0,
        "monthly_fee": 10.0,
        "fee_waiver_threshold": 5000.0,
        "daily_transfer_limit": 5000.0,
    },
    AccountType.PREMIUM: {
        "min_balance": 10000.0,
        "monthly_fee": 0.0,
        "fee_waiver_threshold": 0.0,
        "daily_transfer_limit": 50000.0,
    },
}

MIN_TRANSFER_AMOUNT = 0.01


class BankAccount:
    """Represents a SecureBank online banking account."""

    def __init__(self, account_id, account_type, initial_balance=0.0, owner_name=""):
        """Initialize a bank account."""
        config = ACCOUNT_CONFIG[account_type]
        self.account_id = account_id
        self.account_type = account_type
        self.owner_name = owner_name
        self.balance = float(initial_balance)
        self.state = AccountState.ACTIVE
        self.daily_transferred = 0.0
        self.last_transfer_date = None
        self.transactions = []
        self.config = config

        # Check initial state
        if self.balance < config["min_balance"] and config["min_balance"] > 0:
            self.state = AccountState.SUSPENDED

    def _reset_daily_limit_if_needed(self):
        """Reset the daily transfer counter if it is a new day."""
        today = date.today()
        if self.last_transfer_date != today:
            self.daily_transferred = 0.0
            self.last_transfer_date = today

    def get_remaining_daily_limit(self):
        """Return how much more can be transferred today."""
        self._reset_daily_limit_if_needed()
        return self.config["daily_transfer_limit"] - self.daily_transferred

    def _check_state_allows_transfer(self):
        """Return an error dict if the current state blocks transfers, else None."""
        if self.state == AccountState.CLOSED:
            return {"success": False, "message": "Error: Account closed"}
        if self.state == AccountState.FROZEN:
            return {"success": False, "message": "Error: Account frozen"}
        if self.state == AccountState.SUSPENDED:
            return {"success": False, "message": "Error: Account suspended"}
        return None

    def transfer(self, amount):
        """
        Attempt to transfer money from this account.

        Returns a dict with keys 'success' (bool) and 'message' (str).
        """
        self._reset_daily_limit_if_needed()

        state_error = self._check_state_allows_transfer()
        if state_error:
            return state_error

        if amount < MIN_TRANSFER_AMOUNT:
            return {"success": False, "message": "Error: Amount must be positive"}

        if amount > self.balance:
            return {"success": False, "message": "Error: Insufficient funds"}

        remaining = self.get_remaining_daily_limit()
        if amount > remaining:
            return {"success": False, "message": "Error: Exceeds daily limit"}

        # Execute transfer
        self.balance -= amount
        self.daily_transferred += amount
        self.transactions.append(
            {
                "type": "transfer_out",
                "amount": amount,
                "timestamp": datetime.now().isoformat(),
                "balance_after": self.balance,
            }
        )

        # Check if balance dropped below minimum
        min_balance = self.config["min_balance"]
        if min_balance > 0 and self.balance < min_balance:
            self.state = AccountState.SUSPENDED

        return {"success": True, "message": "Transfer successful"}

    def deposit(self, amount):
        """Deposit money into the account."""
        if self.state == AccountState.CLOSED:
            return {"success": False, "message": "Error: Account closed"}

        if amount <= 0:
            return {"success": False, "message": "Error: Amount must be positive"}

        self.balance += amount
        self.transactions.append(
            {
                "type": "deposit",
                "amount": amount,
                "timestamp": datetime.now().isoformat(),
                "balance_after": self.balance,
            }
        )

        # Restore active state if balance is now above minimum
        min_balance = self.config["min_balance"]
        if self.state == AccountState.SUSPENDED and self.balance >= min_balance:
            self.state = AccountState.ACTIVE

        return {"success": True, "message": "Deposit successful"}

    def freeze(self):
        """Freeze the account (no transactions allowed)."""
        if self.state == AccountState.CLOSED:
            return {"success": False, "message": "Error: Account closed"}
        if self.state == AccountState.FROZEN:
            return {"success": False, "message": "Error: Account already frozen"}
        self.state = AccountState.FROZEN
        return {"success": True, "message": "Account frozen"}

    def unfreeze(self):
        """Unfreeze the account and restore access."""
        if self.state != AccountState.FROZEN:
            return {"success": False, "message": "Error: Account is not frozen"}
        self.state = AccountState.ACTIVE
        return {"success": True, "message": "Account unfrozen"}

    def close(self):
        """Close the account permanently."""
        if self.state == AccountState.CLOSED:
            return {"success": False, "message": "Error: Account already closed"}
        self.state = AccountState.CLOSED
        return {"success": True, "message": f"Account closed. Final balance: {self.balance}"}

    def apply_monthly_fee(self):
        """Apply monthly maintenance fee (waived if balance meets threshold)."""
        if self.state == AccountState.CLOSED:
            return {"success": False, "message": "Error: Account closed"}

        fee = self.config["monthly_fee"]
        if fee == 0.0:
            return {"success": True, "message": "No fee for premium account"}

        threshold = self.config["fee_waiver_threshold"]
        if self.balance >= threshold:
            return {"success": True, "message": "Fee waived: balance above threshold"}

        if self.balance < fee:
            # Insufficient funds for fee - suspend account
            self.balance = 0.0
            self.state = AccountState.SUSPENDED
            return {
                "success": False,
                "message": "Error: Insufficient funds for fee. Account suspended",
            }

        self.balance -= fee
        self.transactions.append(
            {
                "type": "monthly_fee",
                "amount": fee,
                "timestamp": datetime.now().isoformat(),
                "balance_after": self.balance,
            }
        )

        # Check minimum balance after fee
        min_balance = self.config["min_balance"]
        if min_balance > 0 and self.balance < min_balance:
            self.state = AccountState.SUSPENDED

        return {"success": True, "message": f"Monthly fee of ${fee} applied"}

    def get_transaction_history(self, start_date=None, end_date=None):
        """Return transaction history, optionally filtered by date range."""
        if start_date is not None and end_date is not None:
            if start_date > end_date:
                return {
                    "success": False,
                    "message": "Error: Start date must be before end date",
                    "data": [],
                }

        filtered = []
        for txn in self.transactions:
            txn_date = datetime.fromisoformat(txn["timestamp"]).date()
            if start_date and txn_date < start_date:
                continue
            if end_date and txn_date > end_date:
                continue
            filtered.append(txn)

        return {"success": True, "message": "OK", "data": filtered}


class BillPaymentService:
    """Handles bill payment operations."""

    VALID_PAYEES = {
        "electric_company",
        "water_company",
        "internet_provider",
        "credit_card_visa",
        "credit_card_mastercard",
        "gas_company",
        "phone_company",
    }

    def is_valid_payee(self, payee):
        """Return True if the payee is registered in the system."""
        return payee in self.VALID_PAYEES

    def pay_bill(self, account, payee, amount, scheduled_date=None):
        """
        Pay a bill from an account.

        Returns dict with 'success' and 'message'.
        """
        if account.state == AccountState.CLOSED:
            return {"success": False, "message": "Error: Account closed"}

        if account.state == AccountState.FROZEN:
            return {"success": False, "message": "Error: Account frozen"}

        if not self.is_valid_payee(payee):
            return {"success": False, "message": "Error: Invalid payee"}

        if amount <= 0:
            return {"success": False, "message": "Error: Amount must be positive"}

        if scheduled_date is not None:
            today = date.today()
            if scheduled_date < today:
                return {
                    "success": False,
                    "message": "Error: Scheduled date cannot be in the past",
                }

            # Schedule for future (no immediate debit)
            return {
                "success": True,
                "message": f"Bill payment scheduled for {scheduled_date.isoformat()}",
            }

        # Immediate payment
        result = account.transfer(amount)
        if result["success"]:
            return {"success": True, "message": f"Bill payment to {payee} successful"}
        return result
