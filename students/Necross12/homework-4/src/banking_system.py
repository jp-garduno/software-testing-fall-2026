import math

AHORRO = "Ahorro"
ESTANDAR = "Estándar"
PREMIUM = "Premium"

ACTIVO = "Activo"
SUSPENDIDO = "Suspendido"
CONGELADO = "Congelado"
CERRADO = "Cerrado"


class BankAccount:
    TIPOS_VALIDOS = [AHORRO, ESTANDAR, PREMIUM]
    LIMITES = {AHORRO: 2000, ESTANDAR: 5000, PREMIUM: 50000}
    SALDO_MINIMO = {AHORRO: 100, ESTANDAR: 0, PREMIUM: 10000}

    MENSAJES_TIPO = {
        AHORRO: "Se acepta: cuenta de ahorro",
        ESTANDAR: "Se acepta: cuenta corriente",
        PREMIUM: "Se acepta: cuenta premium",
    }

    # Transiciones permitidas (Cerrado es estado final / sumidero)
    TRANSICIONES = {
        ACTIVO: [SUSPENDIDO, CONGELADO, CERRADO],
        SUSPENDIDO: [ACTIVO, CERRADO],
        CONGELADO: [ACTIVO, CERRADO],
        CERRADO: [],
    }

    MENSAJES_ESTADO = {
        ACTIVO: "Eliminar restricciones",
        SUSPENDIDO: "Enviar notificación de advertencia",
        CONGELADO: "Bloquear todas las transacciones",
        CERRADO: "Declaración final generada",
    }

    def __init__(self, account_type, initial_balance):
        self.account_type = account_type
        self.balance = initial_balance
        self.state = ACTIVO
        self.daily_transfer_total = 0
        self.last_message = ""

    @staticmethod
    def validar_tipo_cuenta(tipo):
        if tipo is None or tipo == "":
            return {"valid": False, "error": "Error: el tipo de cuenta es obligatorio"}

        if tipo not in BankAccount.TIPOS_VALIDOS:
            return {"valid": False, "error": "Error: tipo de cuenta no válido"}

        return {"valid": True, "message": BankAccount.MENSAJES_TIPO[tipo]}

    def get_daily_limit(self):
        return BankAccount.LIMITES.get(self.account_type, 0)

    def _fail(self, error):
        self.last_message = error
        return {"success": False, "error": error}

    def transfer(self, amount):
        if self.state == CONGELADO:
            return self._fail("Error: Cuenta congelada")
        if self.state == CERRADO:
            return self._fail("Error: Cuenta cerrada")
        if (
            isinstance(amount, bool)
            or not isinstance(amount, (int, float))
            or not math.isfinite(amount)
            or amount <= 0
        ):
            return self._fail("Error: el monto debe ser positivo")
        if amount > self.balance:
            return self._fail("Error: fondos insuficientes")
        if self.daily_transfer_total + amount > self.get_daily_limit():
            return self._fail("Error: supera el límite diario")

        # Redondeo a centavos para evitar errores de punto flotante
        self.balance = round(self.balance - amount, 2)
        self.daily_transfer_total = round(self.daily_transfer_total + amount, 2)

        if self.balance < BankAccount.SALDO_MINIMO[self.account_type]:
            self.state = SUSPENDIDO
        self.last_message = "La transferencia se realiza"
        return {"success": True}

    def next_state(self, target_state):
        permitidas = BankAccount.TRANSICIONES.get(self.state, [])
        if target_state not in permitidas:
            if self.state == CERRADO:
                self.last_message = "Error: Cuenta cerrada"
            else:
                self.last_message = (
                    f"Error: transición inválida de {self.state} a {target_state}"
                )
            return False
        self.state = target_state
        self.last_message = BankAccount.MENSAJES_ESTADO[target_state]
        return True
