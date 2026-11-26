"""SecureBank Online Banking: sistema bajo prueba del Homework 4.

Los montos se manejan internamente en centavos (enteros) para evitar errores
de redondeo de punto flotante; la API pública recibe y devuelve dólares.
"""

import csv
import io
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

SAVINGS = "Savings"
CHECKING = "Checking"
PREMIUM = "Premium"

ACTIVE = "Active"
FROZEN = "Frozen"
SUSPENDED = "Suspended"
CLOSED = "Closed"


@dataclass(frozen=True)
class AccountPolicy:
    """Reglas de negocio de un tipo de cuenta (todos los montos en centavos)."""

    min_balance: int
    monthly_fee: int
    fee_waiver_threshold: Optional[int]
    daily_limit: int


POLICIES = {
    SAVINGS: AccountPolicy(min_balance=10_000, monthly_fee=500,
                           fee_waiver_threshold=100_000, daily_limit=200_000),
    CHECKING: AccountPolicy(min_balance=0, monthly_fee=1_000,
                            fee_waiver_threshold=500_000, daily_limit=500_000),
    PREMIUM: AccountPolicy(min_balance=1_000_000, monthly_fee=0,
                           fee_waiver_threshold=None, daily_limit=5_000_000),
}

REGISTERED_PAYEES = {
    "UTIL-ELECTRIC": "Utility",
    "UTIL-WATER": "Utility",
    "CC-VISA": "Credit Card",
}

CENT = Decimal("0.01")


def to_cents(amount) -> int:
    """Convierte un monto en dólares a centavos.

    Lanza ValueError si el monto no es numérico o tiene más de 2 decimales.
    """
    if isinstance(amount, bool) or not isinstance(amount, (int, float, Decimal)):
        raise ValueError("Amount must be a number")
    value = Decimal(str(amount))
    if not value.is_finite():
        raise ValueError("Amount must be a number")
    if value != value.quantize(CENT):
        raise ValueError("Amount must have at most 2 decimal places")
    return int(value * 100)


def _fail(message: str, **extra) -> dict:
    """Resultado de una operación rechazada."""
    return {"success": False, "error": message, **extra}


def _ok(**extra) -> dict:
    """Resultado de una operación exitosa."""
    return {"success": True, "error": None, **extra}


def _as_date(value, label: str) -> Optional[date]:
    """Normaliza un filtro de fecha: None, date o datetime."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    raise TypeError(f"{label} must be a date")


@dataclass(frozen=True)
class Transaction:
    """Movimiento registrado en el historial de la cuenta."""

    timestamp: datetime
    kind: str
    amount_cents: int
    balance_after_cents: int
    description: str


class BankAccount:
    """Cuenta bancaria de SecureBank con sus reglas de negocio y estados."""

    def __init__(self, account_type, initial_balance, clock=None):
        if account_type not in POLICIES:
            raise ValueError(f"Invalid account type: {account_type}")
        policy = POLICIES[account_type]
        cents = to_cents(initial_balance)
        if cents < policy.min_balance:
            raise ValueError(f"Initial balance below minimum for {account_type}")

        self.account_type = account_type
        self.policy = policy
        self.state = ACTIVE
        self._balance = cents
        self._clock = clock or datetime.now
        self._daily_total = 0
        self._daily_date = self._clock().date()
        self.transactions = []
        self.scheduled_payments = []
        self.notifications = []

    # ------------------------------------------------------------------ vistas
    @property
    def balance(self) -> float:
        """Saldo actual en dólares (consulta permitida en cualquier estado)."""
        return self._balance / 100

    @property
    def daily_transfer_total(self) -> float:
        """Total transferido hoy en dólares; se reinicia a medianoche."""
        self._refresh_daily_window()
        return self._daily_total / 100

    def get_daily_limit(self) -> float:
        """Límite diario de transferencia del tipo de cuenta, en dólares."""
        return self.policy.daily_limit / 100

    def get_minimum_balance(self) -> float:
        """Saldo mínimo requerido por el tipo de cuenta, en dólares."""
        return self.policy.min_balance / 100

    def is_operable(self) -> bool:
        """True si la cuenta admite movimientos (Active o Suspended)."""
        return self.state in (ACTIVE, SUSPENDED)

    # ------------------------------------------------------------- operaciones
    def transfer(self, amount, to_account=None) -> dict:
        """Transfiere dinero desde esta cuenta, opcionalmente hacia otra cuenta."""
        error = self._state_error()
        if error:
            return _fail(error)
        cents, error = self._parse_positive(amount)
        if error:
            return _fail(error)
        self._refresh_daily_window()
        if self._daily_total + cents > self.policy.daily_limit:
            return _fail("Exceeds daily limit")
        if cents > self._balance:
            return _fail("Insufficient funds")
        if to_account is self:
            return _fail("Cannot transfer to the same account")
        if to_account is not None and not to_account.is_operable():
            return _fail("Destination account unavailable")

        self._balance -= cents
        self._daily_total += cents
        self._record("transfer", -cents, "Transfer out")
        if to_account is not None:
            to_account.deposit(cents / 100)
        self._after_debit()
        return _ok(balance=self.balance, state=self.state)

    def deposit(self, amount) -> dict:
        """Deposita dinero; puede reactivar una cuenta suspendida."""
        error = self._state_error()
        if error:
            return _fail(error)
        cents, error = self._parse_positive(amount)
        if error:
            return _fail(error)
        self._balance += cents
        self._record("deposit", cents, "Deposit")
        if self.state == SUSPENDED and self._balance >= self.policy.min_balance:
            self.state = ACTIVE
            self.notifications.append("Account reactivated: minimum balance restored")
        return _ok(balance=self.balance, state=self.state)

    def pay_bill(self, payee_id, amount, scheduled_date=None) -> dict:
        """Paga un servicio de inmediato o lo programa para una fecha futura."""
        error = self._state_error()
        if error:
            return _fail(error)
        if not isinstance(payee_id, str) or not payee_id.strip():
            return _fail("Payee is required")
        payee = payee_id.strip().upper()
        if payee not in REGISTERED_PAYEES:
            return _fail("Unknown payee")
        cents, error = self._parse_positive(amount)
        if error:
            return _fail(error)

        today = self._clock().date()
        if scheduled_date is not None and scheduled_date < today:
            return _fail("Scheduled date cannot be in the past")
        if scheduled_date is not None and scheduled_date > today:
            self.scheduled_payments.append(
                {"payee": payee, "amount": cents / 100, "date": scheduled_date})
            return _ok(status="scheduled", balance=self.balance)
        if cents > self._balance:
            return _fail("Insufficient funds")

        self._balance -= cents
        self._record("bill_payment", -cents, f"Bill payment to {payee}")
        self._after_debit()
        return _ok(status="paid", balance=self.balance, state=self.state)

    def process_monthly_fee(self, on_date=None) -> dict:
        """Cobra la comisión mensual (solo el día 1) aplicando la exención."""
        if self.state == CLOSED:
            return _fail("Account is closed")
        on_date = on_date or self._clock().date()
        if on_date.day != 1:
            return _fail("Fees are only charged on the 1st of the month")

        fee = self.policy.monthly_fee
        threshold = self.policy.fee_waiver_threshold
        if fee == 0:
            return _ok(fee_charged=0.0, waived=False, state=self.state)
        if threshold is not None and self._balance > threshold:
            return _ok(fee_charged=0.0, waived=True, state=self.state)
        if self._balance < fee:
            if self.state == ACTIVE:
                self.state = SUSPENDED
                self.notifications.append("Account suspended: insufficient funds for fee")
            return _fail("Insufficient funds for monthly fee", state=self.state)

        self._balance -= fee
        self._record("fee", -fee, "Monthly fee")
        self._after_debit()
        return _ok(fee_charged=fee / 100, waived=False, state=self.state)

    # --------------------------------------------------------- cambios de estado
    def freeze(self, reason="customer request") -> dict:
        """Congela la cuenta por solicitud del cliente o detección de fraude."""
        if self.state != ACTIVE:
            return _fail(f"Cannot freeze an account in state {self.state}")
        self.state = FROZEN
        self.notifications.append(f"Account frozen: {reason}")
        return _ok(state=self.state)

    def unfreeze(self) -> dict:
        """Descongela la cuenta; queda Suspended si el saldo está bajo el mínimo."""
        if self.state != FROZEN:
            return _fail("Account is not frozen")
        below_minimum = self._balance < self.policy.min_balance
        self.state = SUSPENDED if below_minimum else ACTIVE
        return _ok(state=self.state)

    def close(self) -> dict:
        """Cierra la cuenta definitivamente y genera el estado de cuenta final."""
        if self.state == CLOSED:
            return _fail("Account is already closed")
        self.state = CLOSED
        statement = {"final_balance": self.balance,
                     "transactions": len(self.transactions)}
        return _ok(state=self.state, final_statement=statement)

    # ------------------------------------------------------------- historial
    def get_transactions(self, start_date=None, end_date=None) -> list:
        """Devuelve los movimientos entre dos fechas (ambas inclusivas)."""
        start = _as_date(start_date, "start_date")
        end = _as_date(end_date, "end_date")
        if start and end and start > end:
            raise ValueError("Start date must be on or before end date")
        return [t for t in self.transactions
                if (start is None or t.timestamp.date() >= start)
                and (end is None or t.timestamp.date() <= end)]

    def export_transactions_csv(self, start_date=None, end_date=None) -> str:
        """Exporta a CSV los movimientos del rango indicado."""
        buffer = io.StringIO()
        writer = csv.writer(buffer, lineterminator="\n")
        writer.writerow(["timestamp", "type", "amount", "balance_after", "description"])
        for txn in self.get_transactions(start_date, end_date):
            writer.writerow([txn.timestamp.isoformat(), txn.kind,
                             f"{txn.amount_cents / 100:.2f}",
                             f"{txn.balance_after_cents / 100:.2f}",
                             txn.description])
        return buffer.getvalue()

    # ------------------------------------------------------------- internos
    def _state_error(self) -> Optional[str]:
        """Mensaje de error si el estado no permite movimientos."""
        if self.state == CLOSED:
            return "Account is closed"
        if self.state == FROZEN:
            return "Account is frozen"
        return None

    @staticmethod
    def _parse_positive(amount):
        """Valida que el monto sea numérico, con centavos y mayor a cero."""
        try:
            cents = to_cents(amount)
        except ValueError as exc:
            return None, str(exc)
        if cents <= 0:
            return None, "Amount must be positive"
        return cents, None

    def _refresh_daily_window(self) -> None:
        """Reinicia el acumulado diario cuando cambia la fecha (medianoche)."""
        today = self._clock().date()
        if today != self._daily_date:
            self._daily_date = today
            self._daily_total = 0

    def _after_debit(self) -> None:
        """Suspende la cuenta activa si el saldo quedó bajo el mínimo."""
        if self.state == ACTIVE and self._balance < self.policy.min_balance:
            self.state = SUSPENDED
            self.notifications.append("Warning: balance below minimum")

    def _record(self, kind: str, cents: int, description: str) -> None:
        """Agrega un movimiento al historial."""
        self.transactions.append(
            Transaction(self._clock(), kind, cents, self._balance, description))
