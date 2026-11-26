"""SecureBank: sistema bajo prueba para Homework 4.

Puerto uno a uno de ``src/bankingSystem.js``. Los montos se manejan como
numeros en dolares y toda operacion aritmetica pasa por ``round2`` para evitar
el arrastre de error de punto flotante (4999.99 + 0.01 da 5000.000000000001).
"""

import math

ACCOUNT_RULES = {
    "Savings": {
        "minimum_balance": 100,
        "monthly_fee": 5,
        "fee_waiver": 1000,
        "daily_limit": 2000,
    },
    "Checking": {
        "minimum_balance": 0,
        "monthly_fee": 10,
        "fee_waiver": 5000,
        "daily_limit": 5000,
    },
    "Premium": {
        "minimum_balance": 10000,
        "monthly_fee": 0,
        "fee_waiver": 0,
        "daily_limit": 50000,
    },
}

ACTIVE = "Active"
FROZEN = "Frozen"
SUSPENDED = "Suspended"
CLOSED = "Closed"

ERRORS = {
    "INVALID_ACCOUNT_TYPE": "Invalid account type",
    "INVALID_AMOUNT": "Amount must be a valid number",
    "AMOUNT_NOT_POSITIVE": "Amount must be positive",
    "BELOW_MINIMUM_AMOUNT": "Amount is below the $0.01 minimum",
    "ACCOUNT_FROZEN": "Account is frozen",
    "ACCOUNT_CLOSED": "Account is closed",
    "EXCEEDS_DAILY_LIMIT": "Exceeds daily limit",
    "INSUFFICIENT_FUNDS": "Insufficient funds",
    "INVALID_PAYEE": "Invalid payee",
    "INVALID_DATE_RANGE": "Invalid date range",
    "INVALID_TRANSITION": "Invalid state transition",
}

REGISTERED_PAYEES = ["ELECTRIC_CO", "WATER_UTILITY", "CREDIT_CARD_VISA"]

MINIMUM_AMOUNT = 0.01
DEFAULT_DATE = "2026-01-15"


def round2(value):
    """Redondea a centavos para que el punto flotante no arrastre error."""
    return round(value, 2)


def is_number(value):
    """True si el valor es un numero finito (los booleanos no cuentan)."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    return math.isfinite(value)


# La cuenta guarda 8 atributos del dominio y el limite de pylint son 7. Juntarlos
# en un diccionario solo para bajar el numero haria mas dificiles de leer las
# pruebas de estado.
class BankAccount:  # pylint: disable=too-many-instance-attributes
    """Cuenta de SecureBank con estados, limites diarios y cobro mensual."""

    def __init__(self, account_type, initial_balance, opened_on=DEFAULT_DATE):
        if account_type not in ACCOUNT_RULES:
            raise ValueError(ERRORS["INVALID_ACCOUNT_TYPE"])
        if not is_number(initial_balance):
            raise ValueError(ERRORS["INVALID_AMOUNT"])
        if initial_balance < 0:
            raise ValueError(ERRORS["AMOUNT_NOT_POSITIVE"])

        self.account_type = account_type
        self.rules = ACCOUNT_RULES[account_type]
        self.balance = round2(initial_balance)
        self.daily_transfer_total = 0
        self.current_date = opened_on
        self.transactions = []
        self.scheduled_payments = []
        self.state = (
            SUSPENDED if self.balance < self.rules["minimum_balance"] else ACTIVE
        )

    def get_daily_limit(self):
        """Limite diario de transferencia segun el tipo de cuenta."""
        return self.rules["daily_limit"]

    def get_minimum_balance(self):
        """Saldo minimo exigido por el tipo de cuenta."""
        return self.rules["minimum_balance"]

    def set_current_date(self, date):
        """Fija la fecha del sistema (reloj inyectado para pruebas deterministas)."""
        self.current_date = date

    def reset_daily_limit(self):
        """Reinicia el acumulado diario de transferencias (corte de medianoche)."""
        self.daily_transfer_total = 0

    def sync_suspension(self):
        """Mantiene el invariante: saldo < minimo <=> Suspended."""
        if self.state in (FROZEN, CLOSED):
            return
        self.state = (
            SUSPENDED if self.balance < self.rules["minimum_balance"] else ACTIVE
        )

    def accepts_transactions(self):
        """Una cuenta congelada o cerrada no acepta movimientos."""
        return self.state in (ACTIVE, SUSPENDED)

    def blocking_state_error(self):
        """Error correspondiente al estado que bloquea la operacion."""
        if self.state == CLOSED:
            return ERRORS["ACCOUNT_CLOSED"]
        return ERRORS["ACCOUNT_FROZEN"]

    def validate_amount(self, amount):
        """Devuelve el mensaje de error del monto, o None si es valido."""
        if not is_number(amount):
            return ERRORS["INVALID_AMOUNT"]
        if amount <= 0:
            return ERRORS["AMOUNT_NOT_POSITIVE"]
        if amount < MINIMUM_AMOUNT:
            return ERRORS["BELOW_MINIMUM_AMOUNT"]
        return None

    def record(self, kind, amount, description):
        """Agrega un movimiento al historial."""
        self.transactions.append(
            {
                "date": self.current_date,
                "type": kind,
                "amount": amount,
                "description": description,
            }
        )

    def fail(self, error):
        """Resultado de una operacion rechazada."""
        return {
            "success": False,
            "error": error,
            "balance": self.balance,
            "state": self.state,
        }

    def succeed(self, **extra):
        """Resultado de una operacion aceptada."""
        result = {"success": True, "balance": self.balance, "state": self.state}
        if self.state == SUSPENDED:
            result["warning"] = "Balance is below the minimum for this account type"
        result.update(extra)
        return result

    def transfer(self, amount, destination="EXTERNAL"):
        """Transfiere dinero fuera de la cuenta aplicando todas las validaciones."""
        if not self.accepts_transactions():
            return self.fail(self.blocking_state_error())
        amount_error = self.validate_amount(amount)
        if amount_error:
            return self.fail(amount_error)

        value = round2(amount)
        if round2(self.daily_transfer_total + value) > self.rules["daily_limit"]:
            return self.fail(ERRORS["EXCEEDS_DAILY_LIMIT"])
        if value > self.balance:
            return self.fail(ERRORS["INSUFFICIENT_FUNDS"])

        self.balance = round2(self.balance - value)
        self.daily_transfer_total = round2(self.daily_transfer_total + value)
        self.record("TRANSFER", value, f"Transfer to {destination}")
        self.sync_suspension()
        return self.succeed()

    def deposit(self, amount):
        """Abona dinero y reevalua la suspension por saldo minimo."""
        if not self.accepts_transactions():
            return self.fail(self.blocking_state_error())
        amount_error = self.validate_amount(amount)
        if amount_error:
            return self.fail(amount_error)

        value = round2(amount)
        self.balance = round2(self.balance + value)
        self.record("DEPOSIT", value, "Deposit")
        self.sync_suspension()
        return self.succeed()

    def pay_bill(self, payee, amount, payment_date=None):
        """Paga o agenda un servicio a un beneficiario registrado."""
        if not self.accepts_transactions():
            return self.fail(self.blocking_state_error())
        if not isinstance(payee, str) or payee not in REGISTERED_PAYEES:
            return self.fail(ERRORS["INVALID_PAYEE"])
        amount_error = self.validate_amount(amount)
        if amount_error:
            return self.fail(amount_error)

        value = round2(amount)
        if value > self.balance:
            return self.fail(ERRORS["INSUFFICIENT_FUNDS"])

        due_date = payment_date or self.current_date
        if due_date > self.current_date:
            self.scheduled_payments.append(
                {"payee": payee, "amount": value, "due_date": due_date}
            )
            return self.succeed(scheduled=True)

        self.balance = round2(self.balance - value)
        self.record("BILL_PAYMENT", value, f"Bill payment to {payee}")
        self.sync_suspension()
        return self.succeed(scheduled=False)

    def apply_monthly_fee(self):
        """Cobro mensual del primero de mes, con exencion por saldo."""
        if self.state == CLOSED:
            return self.fail(ERRORS["ACCOUNT_CLOSED"])

        fee = self.rules["monthly_fee"]
        if fee == 0 or self.balance > self.rules["fee_waiver"]:
            return self.succeed(fee_charged=0, waived=True)
        if self.balance < fee:
            self.state = SUSPENDED
            return self.fail(ERRORS["INSUFFICIENT_FUNDS"])

        self.balance = round2(self.balance - fee)
        self.record("FEE", fee, "Monthly maintenance fee")
        self.sync_suspension()
        return self.succeed(fee_charged=fee, waived=False)

    def freeze(self):
        """Active -> Frozen por peticion del cliente o deteccion de fraude."""
        if self.state != ACTIVE:
            return self.fail(ERRORS["INVALID_TRANSITION"])
        self.state = FROZEN
        return self.succeed()

    def unfreeze(self):
        """Frozen -> Active, reevaluando el saldo minimo."""
        if self.state != FROZEN:
            return self.fail(ERRORS["INVALID_TRANSITION"])
        self.state = ACTIVE
        self.sync_suspension()
        return self.succeed()

    def close(self):
        """Cualquier estado -> Closed. Una cuenta cerrada no se reabre."""
        if self.state == CLOSED:
            return self.fail(ERRORS["ACCOUNT_CLOSED"])
        self.state = CLOSED
        return self.succeed(final_statement=self.balance)

    def get_transaction_history(self, date_from=None, date_to=None):
        """Historial filtrado por rango de fechas ISO (inclusivo)."""
        if date_from is not None and date_to is not None and date_from > date_to:
            return {
                "success": False,
                "error": ERRORS["INVALID_DATE_RANGE"],
                "transactions": [],
            }
        transactions = [
            entry
            for entry in self.transactions
            if (date_from is None or entry["date"] >= date_from)
            and (date_to is None or entry["date"] <= date_to)
        ]
        return {"success": True, "transactions": transactions}

    def export_history_to_csv(self, date_from=None, date_to=None):
        """Exporta el historial filtrado a CSV."""
        history = self.get_transaction_history(date_from, date_to)
        if not history["success"]:
            return history
        rows = [
            f"{entry['date']},{entry['type']},{entry['amount']:.2f},{entry['description']}"
            for entry in history["transactions"]
        ]
        return {
            "success": True,
            "csv": "\n".join(["date,type,amount,description"] + rows),
        }
