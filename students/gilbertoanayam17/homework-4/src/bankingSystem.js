/**
 * SecureBank - sistema bajo prueba para Homework 4.
 *
 * Los montos se manejan como numeros en dolares. Toda operacion aritmetica pasa
 * por round2() para evitar el arrastre de error de punto flotante (por ejemplo,
 * 4999.99 + 0.01 da 5000.000000000001 sin redondear).
 */

// Se usa un Map y no un objeto para buscar las reglas por un tipo de cuenta que
// viene de fuera: indexar un objeto con una clave variable es un riesgo de
// object injection y el linter de seguridad lo marca.
const ACCOUNT_RULES = new Map([
  [
    "Savings",
    { minimumBalance: 100, monthlyFee: 5, feeWaiver: 1000, dailyLimit: 2000 },
  ],
  [
    "Checking",
    { minimumBalance: 0, monthlyFee: 10, feeWaiver: 5000, dailyLimit: 5000 },
  ],
  [
    "Premium",
    {
      minimumBalance: 10000,
      monthlyFee: 0,
      feeWaiver: 0,
      dailyLimit: 50000,
    },
  ],
]);

const STATES = {
  ACTIVE: "Active",
  FROZEN: "Frozen",
  SUSPENDED: "Suspended",
  CLOSED: "Closed",
};

const ERRORS = {
  INVALID_ACCOUNT_TYPE: "Invalid account type",
  INVALID_AMOUNT: "Amount must be a valid number",
  AMOUNT_NOT_POSITIVE: "Amount must be positive",
  BELOW_MINIMUM_AMOUNT: "Amount is below the $0.01 minimum",
  ACCOUNT_FROZEN: "Account is frozen",
  ACCOUNT_CLOSED: "Account is closed",
  EXCEEDS_DAILY_LIMIT: "Exceeds daily limit",
  INSUFFICIENT_FUNDS: "Insufficient funds",
  INVALID_PAYEE: "Invalid payee",
  INVALID_DATE_RANGE: "Invalid date range",
  INVALID_TRANSITION: "Invalid state transition",
};

const REGISTERED_PAYEES = ["ELECTRIC_CO", "WATER_UTILITY", "CREDIT_CARD_VISA"];

const MINIMUM_AMOUNT = 0.01;
const DEFAULT_DATE = "2026-01-15";

/** Redondea a centavos para que el punto flotante no arrastre error. */
function round2(value) {
  return Math.round(value * 100) / 100;
}

class BankAccount {
  constructor(accountType, initialBalance, openedOn = DEFAULT_DATE) {
    if (!ACCOUNT_RULES.has(accountType)) {
      throw new Error(ERRORS.INVALID_ACCOUNT_TYPE);
    }
    if (
      typeof initialBalance !== "number" ||
      !Number.isFinite(initialBalance)
    ) {
      throw new Error(ERRORS.INVALID_AMOUNT);
    }
    if (initialBalance < 0) {
      throw new Error(ERRORS.AMOUNT_NOT_POSITIVE);
    }

    this.accountType = accountType;
    this.rules = ACCOUNT_RULES.get(accountType);
    this.balance = round2(initialBalance);
    this.dailyTransferTotal = 0;
    this.currentDate = openedOn;
    this.transactions = [];
    this.scheduledPayments = [];
    this.state =
      this.balance < this.rules.minimumBalance
        ? STATES.SUSPENDED
        : STATES.ACTIVE;
  }

  getDailyLimit() {
    return this.rules.dailyLimit;
  }

  getMinimumBalance() {
    return this.rules.minimumBalance;
  }

  setCurrentDate(date) {
    this.currentDate = date;
  }

  /** Reinicia el acumulado diario de transferencias (corte de medianoche). */
  resetDailyLimit() {
    this.dailyTransferTotal = 0;
  }

  /**
   * Reevalua el estado contra el saldo minimo.
   * Mantiene el invariante: saldo < minimo <=> Suspended.
   */
  syncSuspension() {
    if (this.state === STATES.FROZEN || this.state === STATES.CLOSED) {
      return;
    }
    this.state =
      this.balance < this.rules.minimumBalance
        ? STATES.SUSPENDED
        : STATES.ACTIVE;
  }

  /** Una cuenta congelada o cerrada no acepta movimientos. */
  acceptsTransactions() {
    return this.state === STATES.ACTIVE || this.state === STATES.SUSPENDED;
  }

  blockingStateError() {
    if (this.state === STATES.CLOSED) {
      return ERRORS.ACCOUNT_CLOSED;
    }
    return ERRORS.ACCOUNT_FROZEN;
  }

  /** Valida un monto de entrada; devuelve el error o null si es valido. */
  validateAmount(amount) {
    if (typeof amount !== "number" || !Number.isFinite(amount)) {
      return ERRORS.INVALID_AMOUNT;
    }
    if (amount <= 0) {
      return ERRORS.AMOUNT_NOT_POSITIVE;
    }
    if (amount < MINIMUM_AMOUNT) {
      return ERRORS.BELOW_MINIMUM_AMOUNT;
    }
    return null;
  }

  record(type, amount, description) {
    this.transactions.push({
      date: this.currentDate,
      type,
      amount,
      description,
    });
  }

  fail(error) {
    return { success: false, error, balance: this.balance, state: this.state };
  }

  succeed(extra = {}) {
    const result = { success: true, balance: this.balance, state: this.state };
    if (this.state === STATES.SUSPENDED) {
      result.warning = "Balance is below the minimum for this account type";
    }
    return Object.assign(result, extra);
  }

  transfer(amount, destination = "EXTERNAL") {
    if (!this.acceptsTransactions()) {
      return this.fail(this.blockingStateError());
    }
    const amountError = this.validateAmount(amount);
    if (amountError) {
      return this.fail(amountError);
    }

    const value = round2(amount);
    if (round2(this.dailyTransferTotal + value) > this.rules.dailyLimit) {
      return this.fail(ERRORS.EXCEEDS_DAILY_LIMIT);
    }
    if (value > this.balance) {
      return this.fail(ERRORS.INSUFFICIENT_FUNDS);
    }

    this.balance = round2(this.balance - value);
    this.dailyTransferTotal = round2(this.dailyTransferTotal + value);
    this.record("TRANSFER", value, `Transfer to ${destination}`);
    this.syncSuspension();
    return this.succeed();
  }

  deposit(amount) {
    if (!this.acceptsTransactions()) {
      return this.fail(this.blockingStateError());
    }
    const amountError = this.validateAmount(amount);
    if (amountError) {
      return this.fail(amountError);
    }

    const value = round2(amount);
    this.balance = round2(this.balance + value);
    this.record("DEPOSIT", value, "Deposit");
    this.syncSuspension();
    return this.succeed();
  }

  payBill(payee, amount, paymentDate = null) {
    if (!this.acceptsTransactions()) {
      return this.fail(this.blockingStateError());
    }
    if (typeof payee !== "string" || !REGISTERED_PAYEES.includes(payee)) {
      return this.fail(ERRORS.INVALID_PAYEE);
    }
    const amountError = this.validateAmount(amount);
    if (amountError) {
      return this.fail(amountError);
    }

    const value = round2(amount);
    if (value > this.balance) {
      return this.fail(ERRORS.INSUFFICIENT_FUNDS);
    }

    const dueDate = paymentDate || this.currentDate;
    if (dueDate > this.currentDate) {
      this.scheduledPayments.push({ payee, amount: value, dueDate });
      return this.succeed({ scheduled: true });
    }

    this.balance = round2(this.balance - value);
    this.record("BILL_PAYMENT", value, `Bill payment to ${payee}`);
    this.syncSuspension();
    return this.succeed({ scheduled: false });
  }

  /** Cobro mensual del 1o de mes, con exencion por saldo. */
  applyMonthlyFee() {
    if (this.state === STATES.CLOSED) {
      return this.fail(ERRORS.ACCOUNT_CLOSED);
    }

    const fee = this.rules.monthlyFee;
    if (fee === 0 || this.balance > this.rules.feeWaiver) {
      return this.succeed({ feeCharged: 0, waived: true });
    }
    if (this.balance < fee) {
      this.state = STATES.SUSPENDED;
      return this.fail(ERRORS.INSUFFICIENT_FUNDS);
    }

    this.balance = round2(this.balance - fee);
    this.record("FEE", fee, "Monthly maintenance fee");
    this.syncSuspension();
    return this.succeed({ feeCharged: fee, waived: false });
  }

  freeze() {
    if (this.state !== STATES.ACTIVE) {
      return this.fail(ERRORS.INVALID_TRANSITION);
    }
    this.state = STATES.FROZEN;
    return this.succeed();
  }

  unfreeze() {
    if (this.state !== STATES.FROZEN) {
      return this.fail(ERRORS.INVALID_TRANSITION);
    }
    this.state = STATES.ACTIVE;
    this.syncSuspension();
    return this.succeed();
  }

  close() {
    if (this.state === STATES.CLOSED) {
      return this.fail(ERRORS.ACCOUNT_CLOSED);
    }
    this.state = STATES.CLOSED;
    return this.succeed({ finalStatement: this.balance });
  }

  getTransactionHistory(from = null, to = null) {
    if (from !== null && to !== null && from > to) {
      return {
        success: false,
        error: ERRORS.INVALID_DATE_RANGE,
        transactions: [],
      };
    }
    const transactions = this.transactions.filter(
      (entry) =>
        (from === null || entry.date >= from) &&
        (to === null || entry.date <= to),
    );
    return { success: true, transactions };
  }

  exportHistoryToCsv(from = null, to = null) {
    const history = this.getTransactionHistory(from, to);
    if (!history.success) {
      return history;
    }
    const rows = history.transactions.map(
      (entry) =>
        `${entry.date},${entry.type},${entry.amount.toFixed(2)},${
          entry.description
        }`,
    );
    return {
      success: true,
      csv: ["date,type,amount,description", ...rows].join("\n"),
    };
  }
}

module.exports = {
  BankAccount,
  ACCOUNT_RULES,
  STATES,
  ERRORS,
  REGISTERED_PAYEES,
  MINIMUM_AMOUNT,
  round2,
};
