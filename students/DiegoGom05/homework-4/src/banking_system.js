class BankAccount {
  /**
   * Simula un sistema bancario para pruebas de caja negra.
   * @param {string} accountType - 'Checking', 'Savings', o 'Premium'
   * @param {number} initialBalance - Saldo inicial
   */
  constructor(accountType, initialBalance) {
    this.accountType = accountType;
    this.balance = parseFloat(initialBalance);
    this.state = "Active";
    this.dailyTransferTotal = 0.0;
    this.dailyTransferCount = 0;
  }

  /**
   * Retorna el límite de transferencia diario según el tipo de cuenta.
   */
  getDailyLimit() {
    const limits = {
      Savings: 2000.0,
      Checking: 5000.0,
      Premium: 25000.0,
    };
    return limits[this.accountType] || 0.0;
  }

  /**
   * Realiza una transferencia aplicando validaciones de caja negra.
   */
  transfer(amount) {
    const parsedAmount = parseFloat(amount);

    // Validaciones de Estado
    if (this.state === "Closed") {
      return { success: false, error: "Error: Account closed" };
    }
    if (this.state === "Frozen") {
      return { success: false, error: "Error: Account frozen" };
    }

    // Validaciones del Tipo de Cuenta
    if (!["Savings", "Checking", "Premium"].includes(this.accountType)) {
      return { success: false, error: "Error: Unsupported account type" };
    }

    // Validaciones del Monto
    if (isNaN(parsedAmount) || parsedAmount <= 0) {
      return { success: false, error: "Error: Amount must be positive" };
    }

    // Validación de Fondos Disponibles
    if (parsedAmount > this.balance) {
      return { success: false, error: "Error: Insufficient funds" };
    }

    // Validación de Límite Diario acumulado
    const dailyLimit = this.getDailyLimit();
    if (this.dailyTransferTotal + parsedAmount > dailyLimit) {
      return { success: false, error: "Error: Exceeds daily limit" };
    }

    // Ejecución de la transferencia
    this.balance -= parsedAmount;
    this.dailyTransferTotal += parsedAmount;
    this.dailyTransferCount += 1;

    // Transición de estado automática si el saldo cae por debajo de $100
    if (this.balance < 100.0 && this.state === "Active") {
      this.state = "Suspended";
    }

    return { success: true, error: null };
  }

  /**
   * Deposita dinero y restaura el estado a Active si estaba Suspended.
   */
  deposit(amount) {
    if (this.state === "Closed") {
      return { success: false, error: "Error: Account closed" };
    }

    const parsedAmount = parseFloat(amount);
    if (isNaN(parsedAmount) || parsedAmount <= 0) {
      return { success: false, error: "Error: Amount must be positive" };
    }

    this.balance += parsedAmount;
    if (this.state === "Suspended" && this.balance >= 100.0) {
      this.state = "Active";
    }

    return { success: true, error: null };
  }

  /**
   * Procesa el cobro de mantenimiento mensual según la tabla de decisión.
   */
  processMonthlyFee() {
    let fee = 0.0;

    if (this.accountType === "Savings") {
      if (this.balance <= 100.0) fee = 12.0;
    } else if (this.accountType === "Checking") {
      if (this.balance <= 1000.0) fee = 12.0;
    } else if (this.accountType === "Premium") {
      fee = 0.0;
    }

    if (fee > 0) {
      this.balance -= fee;
      return { success: true, feeCharged: fee };
    }

    return { success: true, feeCharged: 0.0 };
  }

  /**
   * Procesa pagos de servicios con validaciones.
   */
  processBillPayment(payeeId, amount, payeeActive = true) {
    if (!payeeActive || payeeId === "999999") {
      return { success: false, error: "Error: Payee not found" };
    }

    if (payeeId.includes("-") || payeeId.includes("!")) {
      return { success: false, error: "Error: Invalid payee format" };
    }

    return this.transfer(amount);
  }

  /**
   * Cambia manualmente el estado de la cuenta.
   */
  changeState(newState, isApproved = true) {
    if (this.state === "Closed") {
      return { success: false, error: "Error: Account closed" };
    }

    if (newState === "Frozen") {
      this.state = "Frozen";
      return { success: true, state: this.state };
    }

    if (newState === "Active" && this.state === "Frozen") {
      if (isApproved) {
        this.state = "Active";
        return { success: true, state: this.state };
      }
      return { success: false, error: "Error: Unfreeze not approved" };
    }

    if (newState === "Closed") {
      this.state = "Closed";
      return { success: true, state: this.state };
    }

    return { success: false, error: "Error: Invalid transition" };
  }
}

module.exports = BankAccount;
