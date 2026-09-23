"""
SecureBank Online Banking System.

System Under Test for Homework 4 — Black Box Testing Suite.
Implements account management, money transfers, bill payment, and
transaction history for Savings, Checking, and Premium accounts.
"""

from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Dict, List, Optional


class AccountType(str, Enum):
    """Supported bank account types."""

    SAVINGS = "Savings"
    CHECKING = "Checking"
    PREMIUM = "Premium"


class AccountState(str, Enum):
    """Possible lifecycle states for a bank account."""

    ACTIVE = "Active"
    FROZEN = "Frozen"
    SUSPENDED = "Suspended"
    CLOSED = "Closed"


# ---------------------------------------------------------------------------
# Account-type configuration constants
# ---------------------------------------------------------------------------

DAILY_LIMITS: Dict[str, float] = {
    AccountType.SAVINGS: 2_000.00,
    AccountType.CHECKING: 5_000.00,
    AccountType.PREMIUM: 50_000.00,
}

MINIMUM_BALANCES: Dict[str, float] = {
    AccountType.SAVINGS: 100.00,
    AccountType.CHECKING: 0.00,
    AccountType.PREMIUM: 10_000.00,
}

MONTHLY_FEES: Dict[str, float] = {
    AccountType.SAVINGS: 5.00,
    AccountType.CHECKING: 10.00,
    AccountType.PREMIUM: 0.00,
}

FEE_WAIVER_THRESHOLDS: Dict[str, Optional[float]] = {
    AccountType.SAVINGS: 1_000.00,
    AccountType.CHECKING: 5_000.00,
    AccountType.PREMIUM: None,  # Premium never charged
}

MINIMUM_TRANSFER: float = 0.01


class TransactionRecord:
    """Represents a single transaction entry."""

    def __init__(
        self,
        transaction_type: str,
        amount: float,
        description: str,
        transaction_date: Optional[date] = None,
    ) -> None:
        self.transaction_type = transaction_type
        self.amount = round(amount, 2)
        self.description = description
        self.date = transaction_date or date.today()

    def __repr__(self) -> str:
        return (
            f"TransactionRecord(type={self.transaction_type!r}, "
            f"amount={self.amount}, date={self.date})"
        )


class BankAccount:
    """
    Represents a SecureBank account with full business-rule enforcement.

    Supports Savings, Checking, and Premium account types with their
    respective daily limits, minimum balances, and monthly fee rules.
    """

    def __init__(
        self,
        account_type: str,
        initial_balance: float,
        account_id: Optional[str] = None,
    ) -> None:
        if account_type not in [t.value for t in AccountType]:
            raise ValueError(f"Unknown account type: {account_type!r}")

        self.account_type: str = account_type
        self.balance: float = round(initial_balance, 2)
        self.state: str = AccountState.ACTIVE
        self.daily_transfer_total: float = 0.0
        self._last_reset_date: date = date.today()
        self.account_id: str = account_id or f"ACC-{id(self):08x}"
        self._transactions: List[TransactionRecord] = []

        # Reflect initial balance state
        self._check_minimum_balance()

    # ------------------------------------------------------------------
    # Properties / helpers
    # ------------------------------------------------------------------

    def get_daily_limit(self) -> float:
        """Return the daily transfer limit for this account type."""
        return DAILY_LIMITS[self.account_type]

    def get_minimum_balance(self) -> float:
        """Return the minimum required balance for this account type."""
        return MINIMUM_BALANCES[self.account_type]

    def get_monthly_fee(self) -> float:
        """Return the monthly fee for this account type."""
        return MONTHLY_FEES[self.account_type]

    def get_fee_waiver_threshold(self) -> Optional[float]:
        """Return the balance threshold above which the monthly fee is waived."""
        return FEE_WAIVER_THRESHOLDS[self.account_type]

    def _reset_daily_limit_if_needed(self) -> None:
        """Reset the daily transfer counter if a new calendar day has started."""
        today = date.today()
        if today > self._last_reset_date:
            self.daily_transfer_total = 0.0
            self._last_reset_date = today

    def _check_minimum_balance(self) -> None:
        """Transition to Suspended if balance drops below minimum (Active only)."""
        min_bal = self.get_minimum_balance()
        if self.state == AccountState.ACTIVE and self.balance < min_bal:
            self.state = AccountState.SUSPENDED

    def _record(self, t_type: str, amount: float, desc: str) -> None:
        """Append a transaction to the internal history."""
        self._transactions.append(TransactionRecord(t_type, amount, desc))

    # ------------------------------------------------------------------
    # Core operations
    # ------------------------------------------------------------------

    def transfer(self, amount: float) -> Dict:
        """
        Attempt to transfer *amount* from this account.

        Returns a dict with keys:
            success (bool), error (str | None), balance (float)
        """
        self._reset_daily_limit_if_needed()

        # --- Validation ---
        if self.state in (AccountState.FROZEN, AccountState.CLOSED):
            return {
                "success": False,
                "error": f"Account is {self.state}. Transfers not allowed.",
                "balance": self.balance,
            }

        if not isinstance(amount, (int, float)) or amount < MINIMUM_TRANSFER:
            return {
                "success": False,
                "error": "Amount must be positive (minimum $0.01).",
                "balance": self.balance,
            }

        if self.balance < round(amount, 2):
            return {
                "success": False,
                "error": "Insufficient funds.",
                "balance": self.balance,
            }

        remaining_daily = self.get_daily_limit() - self.daily_transfer_total
        if round(amount, 2) > round(remaining_daily, 2):
            return {
                "success": False,
                "error": (
                    f"Exceeds daily transfer limit "
                    f"(${self.get_daily_limit():,.2f})."
                ),
                "balance": self.balance,
            }

        # --- Execute ---
        self.balance = round(self.balance - amount, 2)
        self.daily_transfer_total = round(self.daily_transfer_total + amount, 2)
        self._record("TRANSFER_OUT", amount, f"Transfer of ${amount:.2f}")
        self._check_minimum_balance()

        return {"success": True, "error": None, "balance": self.balance}

    def deposit(self, amount: float) -> Dict:
        """
        Deposit *amount* into this account.

        Returns a dict with keys:
            success (bool), error (str | None), balance (float)
        """
        if self.state == AccountState.CLOSED:
            return {
                "success": False,
                "error": "Account is Closed.",
                "balance": self.balance,
            }

        if not isinstance(amount, (int, float)) or amount <= 0:
            return {
                "success": False,
                "error": "Deposit amount must be positive.",
                "balance": self.balance,
            }

        self.balance = round(self.balance + amount, 2)
        self._record("DEPOSIT", amount, f"Deposit of ${amount:.2f}")

        # Restore active state if balance now meets minimum
        min_bal = self.get_minimum_balance()
        if self.state == AccountState.SUSPENDED and self.balance >= min_bal:
            self.state = AccountState.ACTIVE

        return {"success": True, "error": None, "balance": self.balance}

    def pay_bill(
        self,
        payee: str,
        amount: float,
        scheduled_date: Optional[date] = None,
    ) -> Dict:
        """
        Pay a bill to *payee* for *amount*.

        Returns a dict with keys:
            success (bool), error (str | None), balance (float)
        """
        # Validate payee
        if not payee or not payee.strip():
            return {
                "success": False,
                "error": "Payee name is required.",
                "balance": self.balance,
            }

        # Account state check
        if self.state in (AccountState.FROZEN, AccountState.CLOSED):
            return {
                "success": False,
                "error": f"Account is {self.state}. Bill payment not allowed.",
                "balance": self.balance,
            }

        # Amount check
        if not isinstance(amount, (int, float)) or amount <= 0:
            return {
                "success": False,
                "error": "Bill payment amount must be positive.",
                "balance": self.balance,
            }

        if self.balance < round(amount, 2):
            return {
                "success": False,
                "error": "Insufficient funds for bill payment.",
                "balance": self.balance,
            }

        # Scheduled date validation
        pay_date = scheduled_date or date.today()
        if pay_date < date.today():
            return {
                "success": False,
                "error": "Scheduled date cannot be in the past.",
                "balance": self.balance,
            }

        # Execute (immediate payment only; future-dated stored but balance
        # is reserved immediately per spec for simplicity)
        self.balance = round(self.balance - amount, 2)
        self._record(
            "BILL_PAYMENT",
            amount,
            f"Bill payment to {payee} of ${amount:.2f} (date: {pay_date})",
        )
        self._check_minimum_balance()

        return {"success": True, "error": None, "balance": self.balance}

    def freeze(self) -> Dict:
        """
        Freeze this account (Active → Frozen).

        Only Active accounts can be frozen.
        """
        if self.state == AccountState.CLOSED:
            return {
                "success": False,
                "error": "Cannot freeze a Closed account.",
                "state": self.state,
            }
        if self.state == AccountState.FROZEN:
            return {
                "success": False,
                "error": "Account is already Frozen.",
                "state": self.state,
            }

        self.state = AccountState.FROZEN
        return {"success": True, "error": None, "state": self.state}

    def unfreeze(self) -> Dict:
        """
        Unfreeze this account (Frozen → Active or Suspended).

        Only Frozen accounts can be unfrozen.
        """
        if self.state != AccountState.FROZEN:
            return {
                "success": False,
                "error": "Account is not Frozen.",
                "state": self.state,
            }

        # Determine correct target state
        min_bal = self.get_minimum_balance()
        if self.balance >= min_bal:
            self.state = AccountState.ACTIVE
        else:
            self.state = AccountState.SUSPENDED

        return {"success": True, "error": None, "state": self.state}

    def close(self) -> Dict:
        """
        Close this account (Any → Closed).

        Closed accounts cannot be reopened.
        """
        if self.state == AccountState.CLOSED:
            return {
                "success": False,
                "error": "Account is already Closed.",
                "state": self.state,
            }

        self.state = AccountState.CLOSED
        self._record("ACCOUNT_CLOSED", 0, "Account closed")
        return {"success": True, "error": None, "state": self.state}

    def process_monthly_fee(self) -> Dict:
        """
        Charge the monthly maintenance fee.

        Fee is waived if the balance exceeds the waiver threshold.
        If the fee cannot be covered, the account transitions to Suspended.
        """
        if self.state == AccountState.CLOSED:
            return {
                "success": False,
                "error": "Cannot charge fee on a Closed account.",
                "fee_charged": 0,
                "balance": self.balance,
            }

        fee = self.get_monthly_fee()
        threshold = self.get_fee_waiver_threshold()

        # Premium accounts have no fee
        if fee == 0:
            return {
                "success": True,
                "error": None,
                "fee_charged": 0,
                "waived": True,
                "balance": self.balance,
            }

        # Check waiver condition
        if threshold is not None and self.balance > threshold:
            return {
                "success": True,
                "error": None,
                "fee_charged": 0,
                "waived": True,
                "balance": self.balance,
            }

        # Charge fee
        if self.balance >= fee:
            self.balance = round(self.balance - fee, 2)
            self._record("FEE", fee, f"Monthly maintenance fee ${fee:.2f}")
            self._check_minimum_balance()
            return {
                "success": True,
                "error": None,
                "fee_charged": fee,
                "waived": False,
                "balance": self.balance,
            }

        # Insufficient funds for fee → suspend
        self.balance = 0.0
        self.state = AccountState.SUSPENDED
        self._record("FEE", fee, f"Monthly fee caused suspension")
        return {
            "success": True,
            "error": None,
            "fee_charged": fee,
            "waived": False,
            "suspended": True,
            "balance": self.balance,
        }

    def get_transaction_history(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> Dict:
        """
        Return transaction history, optionally filtered by date range.

        Returns a dict with:
            success (bool), transactions (list), error (str | None)
        """
        # Date range validation
        if start_date and end_date and start_date > end_date:
            return {
                "success": False,
                "transactions": [],
                "error": "Start date must be before or equal to end date.",
            }

        if end_date and end_date > date.today():
            return {
                "success": False,
                "transactions": [],
                "error": "End date cannot be in the future.",
            }

        txns = self._transactions
        if start_date:
            txns = [t for t in txns if t.date >= start_date]
        if end_date:
            txns = [t for t in txns if t.date <= end_date]

        return {"success": True, "transactions": txns, "error": None}

    def export_transactions_csv(self) -> str:
        """Return all transactions as a CSV string."""
        lines = ["date,type,amount,description"]
        for txn in self._transactions:
            lines.append(
                f"{txn.date},{txn.transaction_type},"
                f"{txn.amount},{txn.description}"
            )
        return "\n".join(lines)

    def __repr__(self) -> str:
        return (
            f"BankAccount(id={self.account_id!r}, type={self.account_type!r}, "
            f"balance={self.balance}, state={self.state!r})"
        )


class BankingSystem:
    """
    Top-level banking system that manages multiple accounts.

    Provides factory methods and system-wide operations.
    """

    def __init__(self) -> None:
        self._accounts: Dict[str, BankAccount] = {}

    def create_account(
        self, account_type: str, initial_balance: float, account_id: Optional[str] = None
    ) -> Dict:
        """
        Create a new account and register it with the system.

        Returns a dict with:
            success (bool), account (BankAccount | None), error (str | None)
        """
        try:
            account = BankAccount(account_type, initial_balance, account_id)
        except ValueError as exc:
            return {"success": False, "account": None, "error": str(exc)}

        self._accounts[account.account_id] = account
        return {"success": True, "account": account, "error": None}

    def get_account(self, account_id: str) -> Optional[BankAccount]:
        """Retrieve an account by ID."""
        return self._accounts.get(account_id)

    def process_all_monthly_fees(self) -> List[Dict]:
        """Charge monthly fees across all non-closed accounts."""
        results = []
        for acc in self._accounts.values():
            if acc.state != AccountState.CLOSED:
                result = acc.process_monthly_fee()
                result["account_id"] = acc.account_id
                results.append(result)
        return results
