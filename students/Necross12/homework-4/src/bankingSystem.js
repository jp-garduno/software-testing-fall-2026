const TIPOS = {
    AHORRO: "Ahorro",
    ESTANDAR: "Estándar",
    PREMIUM: "Premium"
};

const ESTADOS = {
    ACTIVO: "Activo",
    SUSPENDIDO: "Suspendido",
    CONGELADO: "Congelado",
    CERRADO: "Cerrado",
};

class BankAccount {
    static TIPOS_VALIDOS = [TIPOS.AHORRO, TIPOS.ESTANDAR, TIPOS.PREMIUM];

    static LIMITES = {
        [TIPOS.AHORRO]: 2000,
        [TIPOS.ESTANDAR]: 5000,
        [TIPOS.PREMIUM]: 50000,
    };

    static SALDO_MINIMO = {
        [TIPOS.AHORRO]: 100,
        [TIPOS.ESTANDAR]: 0,
        [TIPOS.PREMIUM]: 10000,
    };

    static MENSAJES_TIPO = {
        [TIPOS.AHORRO]: "Se acepta: cuenta de ahorro",
        [TIPOS.ESTANDAR]: "Se acepta: cuenta corriente",
        [TIPOS.PREMIUM]: "Se acepta: cuenta premium",
    };

    // Transiciones permitidas (Cerrado es estado final o de poso)
    static TRANSICIONES = {
        [ESTADOS.ACTIVO]: [ESTADOS.SUSPENDIDO, ESTADOS.CONGELADO, ESTADOS.CERRADO],
        [ESTADOS.SUSPENDIDO]: [ESTADOS.ACTIVO, ESTADOS.CERRADO],
        [ESTADOS.CONGELADO]: [ESTADOS.ACTIVO, ESTADOS.CERRADO],
        [ESTADOS.CERRADO]: [],
    };

    static MENSAJES_ESTADO = {
        [ESTADOS.ACTIVO]: "Eliminar restricciones",
        [ESTADOS.SUSPENDIDO]: "Enviar notificación de advertencia",
        [ESTADOS.CONGELADO]: "Bloquear todas las transacciones",
        [ESTADOS.CERRADO]: "Declaración final generada",
    };

    constructor(accountType, initialBalance) {
        this.accountType = accountType;
        this.balance = initialBalance;
        this.state = ESTADOS.ACTIVO;
        this.dailyTransferTotal = 0;
        this.lastMessage = "";
    }

    static validarTipoCuenta(tipo) {
        if (tipo === undefined || tipo === null || tipo === "")
            return { valid: false, error: "Error: el tipo de cuenta es obligatorio" };

        if (!BankAccount.TIPOS_VALIDOS.includes(tipo))
            return { valid: false, error: "Error: tipo de cuenta no válido" };

        return { valid: true, message: BankAccount.MENSAJES_TIPO[tipo] };
    }

    getDailyLimit() {
        return BankAccount.LIMITES[this.accountType] || 0;
    }

    _fail(error) {
        this.lastMessage = error;
        return { success: false, error };
    }

    transfer(amount) {
        if (this.state === ESTADOS.CONGELADO)
            return this._fail("Error: Cuenta congelada");

        if (this.state === ESTADOS.CERRADO)
            return this._fail("Error: Cuenta cerrada");

        if (typeof amount !== "number" || Number.isNaN(amount) || amount <= 0)
            return this._fail("Error: el monto debe ser positivo");

        if (amount > this.balance)
            return this._fail("Error: fondos insuficientes");

        if (this.dailyTransferTotal + amount > this.getDailyLimit())
            return this._fail("Error: supera el límite diario");

        // Redondeo
      this.balance = Number((this.balance - amount).toFixed(2));
      this.dailyTransferTotal = Number((this.dailyTransferTotal + amount).toFixed(2),);

      if (this.balance < BankAccount.SALDO_MINIMO[this.accountType])
        this.state = ESTADOS.SUSPENDIDO;

      this.lastMessage = "La transferencia se realiza";
      return { success: true };
    }

    next(targetState) {
        const permitidas = BankAccount.TRANSICIONES[this.state] || [];
        if (!permitidas.includes(targetState)) {
            this.lastMessage =
                this.state === ESTADOS.CERRADO
                    ? "Error: Cuenta cerrada"
                    : `Error: transición inválida de ${this.state} a ${targetState}`;
            return false;
        }
        this.state = targetState;
        this.lastMessage = BankAccount.MENSAJES_ESTADO[targetState];
        return true;
    }
}

module.exports = BankAccount;
module.exports.TIPOS = TIPOS;
module.exports.ESTADOS = ESTADOS;
