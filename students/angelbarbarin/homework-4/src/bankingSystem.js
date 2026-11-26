/**
 * SecureBank Online Banking: sistema bajo prueba del Homework 4 (versión JS).
 *
 * Equivalente a src/banking_system.py. Los montos se manejan internamente en
 * centavos (enteros); la API pública recibe y devuelve dólares.
 */
'use strict';

const SAVINGS = 'Savings';
const CHECKING = 'Checking';
const PREMIUM = 'Premium';

const ACTIVE = 'Active';
const FROZEN = 'Frozen';
const SUSPENDED = 'Suspended';
const CLOSED = 'Closed';

const POLICIES = Object.freeze({
  [SAVINGS]: { minBalance: 10000, monthlyFee: 500, feeWaiverThreshold: 100000, dailyLimit: 200000 },
  [CHECKING]: { minBalance: 0, monthlyFee: 1000, feeWaiverThreshold: 500000, dailyLimit: 500000 },
  [PREMIUM]: { minBalance: 1000000, monthlyFee: 0, feeWaiverThreshold: null, dailyLimit: 5000000 },
});

const REGISTERED_PAYEES = Object.freeze({
  'UTIL-ELECTRIC': 'Utility',
  'UTIL-WATER': 'Utility',
  'CC-VISA': 'Credit Card',
});

/** Convierte dólares a centavos; lanza Error si no es numérico o tiene más de 2 decimales. */
function toCents(amount) {
  if (typeof amount !== 'number' || !Number.isFinite(amount)) {
    throw new Error('Amount must be a number');
  }
  const cents = Math.round(amount * 100);
  if (Math.abs(amount * 100 - cents) > 1e-6) {
    throw new Error('Amount must have at most 2 decimal places');
  }
  return cents;
}

/** Clave de día local (YYYY-MM-DD) para comparar fechas sin hora. */
function dayKey(value) {
  const month = String(value.getMonth() + 1).padStart(2, '0');
  const day = String(value.getDate()).padStart(2, '0');
  return `${value.getFullYear()}-${month}-${day}`;
}

/** Normaliza un filtro de fecha: null/undefined o Date. */
function asDayKey(value, label) {
  if (value === null || value === undefined) {
    return null;
  }
  if (!(value instanceof Date) || Number.isNaN(value.getTime())) {
    throw new TypeError(`${label} must be a date`);
  }
  return dayKey(value);
}

const fail = (message, extra = {}) => ({ success: false, error: message, ...extra });
const ok = (extra) => ({ success: true, error: null, ...extra });

class BankAccount {
  constructor(accountType, initialBalance, clock = () => new Date()) {
    if (!Object.prototype.hasOwnProperty.call(POLICIES, accountType)) {
      throw new Error(`Invalid account type: ${accountType}`);
    }
    const policy = POLICIES[accountType];
    const cents = toCents(initialBalance);
    if (cents < policy.minBalance) {
      throw new Error(`Initial balance below minimum for ${accountType}`);
    }
    this.accountType = accountType;
    this.policy = policy;
    this.state = ACTIVE;
    this.balanceCents = cents;
    this.clock = clock;
    this.dailyTotalCents = 0;
    this.dailyKey = dayKey(clock());
    this.transactions = [];
    this.scheduledPayments = [];
    this.notifications = [];
  }

  // ---------------------------------------------------------------- vistas
  /** Saldo actual en dólares (consulta permitida en cualquier estado). */
  get balance() {
    return this.balanceCents / 100;
  }

  /** Total transferido hoy en dólares; se reinicia a medianoche. */
  get dailyTransferTotal() {
    this.refreshDailyWindow();
    return this.dailyTotalCents / 100;
  }

  getDailyLimit() {
    return this.policy.dailyLimit / 100;
  }

  getMinimumBalance() {
    return this.policy.minBalance / 100;
  }

  isOperable() {
    return this.state === ACTIVE || this.state === SUSPENDED;
  }

  // ----------------------------------------------------------- operaciones
  transfer(amount, toAccount = null) {
    const stateError = this.stateError();
    if (stateError) return fail(stateError);
    const { cents, error } = BankAccount.parsePositive(amount);
    if (error) return fail(error);
    this.refreshDailyWindow();
    if (this.dailyTotalCents + cents > this.policy.dailyLimit) return fail('Exceeds daily limit');
    if (cents > this.balanceCents) return fail('Insufficient funds');
    if (toAccount === this) return fail('Cannot transfer to the same account');
    if (toAccount !== null && !toAccount.isOperable()) {
      return fail('Destination account unavailable');
    }

    this.balanceCents -= cents;
    this.dailyTotalCents += cents;
    this.record('transfer', -cents, 'Transfer out');
    if (toAccount !== null) toAccount.deposit(cents / 100);
    this.afterDebit();
    return ok({ balance: this.balance, state: this.state });
  }

  deposit(amount) {
    const stateError = this.stateError();
    if (stateError) return fail(stateError);
    const { cents, error } = BankAccount.parsePositive(amount);
    if (error) return fail(error);
    this.balanceCents += cents;
    this.record('deposit', cents, 'Deposit');
    if (this.state === SUSPENDED && this.balanceCents >= this.policy.minBalance) {
      this.state = ACTIVE;
      this.notifications.push('Account reactivated: minimum balance restored');
    }
    return ok({ balance: this.balance, state: this.state });
  }

  payBill(payeeId, amount, scheduledDate = null) {
    const stateError = this.stateError();
    if (stateError) return fail(stateError);
    if (typeof payeeId !== 'string' || payeeId.trim() === '') return fail('Payee is required');
    const payee = payeeId.trim().toUpperCase();
    if (!Object.prototype.hasOwnProperty.call(REGISTERED_PAYEES, payee)) {
      return fail('Unknown payee');
    }
    const { cents, error } = BankAccount.parsePositive(amount);
    if (error) return fail(error);

    const today = dayKey(this.clock());
    const when = scheduledDate === null ? null : dayKey(scheduledDate);
    if (when !== null && when < today) return fail('Scheduled date cannot be in the past');
    if (when !== null && when > today) {
      this.scheduledPayments.push({ payee, amount: cents / 100, date: when });
      return ok({ status: 'scheduled', balance: this.balance });
    }
    if (cents > this.balanceCents) return fail('Insufficient funds');

    this.balanceCents -= cents;
    this.record('bill_payment', -cents, `Bill payment to ${payee}`);
    this.afterDebit();
    return ok({ status: 'paid', balance: this.balance, state: this.state });
  }

  processMonthlyFee(onDate = null) {
    if (this.state === CLOSED) return fail('Account is closed');
    const day = (onDate || this.clock()).getDate();
    if (day !== 1) return fail('Fees are only charged on the 1st of the month');

    const fee = this.policy.monthlyFee;
    const threshold = this.policy.feeWaiverThreshold;
    if (fee === 0) return ok({ feeCharged: 0, waived: false, state: this.state });
    if (threshold !== null && this.balanceCents > threshold) {
      return ok({ feeCharged: 0, waived: true, state: this.state });
    }
    if (this.balanceCents < fee) {
      if (this.state === ACTIVE) {
        this.state = SUSPENDED;
        this.notifications.push('Account suspended: insufficient funds for fee');
      }
      return fail('Insufficient funds for monthly fee', { state: this.state });
    }

    this.balanceCents -= fee;
    this.record('fee', -fee, 'Monthly fee');
    this.afterDebit();
    return ok({ feeCharged: fee / 100, waived: false, state: this.state });
  }

  // ------------------------------------------------------ cambios de estado
  freeze(reason = 'customer request') {
    if (this.state !== ACTIVE) return fail(`Cannot freeze an account in state ${this.state}`);
    this.state = FROZEN;
    this.notifications.push(`Account frozen: ${reason}`);
    return ok({ state: this.state });
  }

  unfreeze() {
    if (this.state !== FROZEN) return fail('Account is not frozen');
    this.state = this.balanceCents < this.policy.minBalance ? SUSPENDED : ACTIVE;
    return ok({ state: this.state });
  }

  close() {
    if (this.state === CLOSED) return fail('Account is already closed');
    this.state = CLOSED;
    const finalStatement = { finalBalance: this.balance, transactions: this.transactions.length };
    return ok({ state: this.state, finalStatement });
  }

  // ------------------------------------------------------------- historial
  getTransactions(startDate = null, endDate = null) {
    const start = asDayKey(startDate, 'startDate');
    const end = asDayKey(endDate, 'endDate');
    if (start !== null && end !== null && start > end) {
      throw new RangeError('Start date must be on or before end date');
    }
    return this.transactions.filter((txn) => {
      const key = dayKey(txn.timestamp);
      return (start === null || key >= start) && (end === null || key <= end);
    });
  }

  exportTransactionsCsv(startDate = null, endDate = null) {
    const rows = ['timestamp,type,amount,balance_after,description'];
    for (const txn of this.getTransactions(startDate, endDate)) {
      rows.push([
        `${dayKey(txn.timestamp)}T${txn.timestamp.toTimeString().slice(0, 8)}`,
        txn.kind,
        (txn.amountCents / 100).toFixed(2),
        (txn.balanceAfterCents / 100).toFixed(2),
        txn.description,
      ].join(','));
    }
    return `${rows.join('\n')}\n`;
  }

  // -------------------------------------------------------------- internos
  stateError() {
    if (this.state === CLOSED) return 'Account is closed';
    if (this.state === FROZEN) return 'Account is frozen';
    return null;
  }

  static parsePositive(amount) {
    let cents;
    try {
      cents = toCents(amount);
    } catch (err) {
      return { cents: null, error: err.message };
    }
    if (cents <= 0) return { cents: null, error: 'Amount must be positive' };
    return { cents, error: null };
  }

  refreshDailyWindow() {
    const today = dayKey(this.clock());
    if (today !== this.dailyKey) {
      this.dailyKey = today;
      this.dailyTotalCents = 0;
    }
  }

  afterDebit() {
    if (this.state === ACTIVE && this.balanceCents < this.policy.minBalance) {
      this.state = SUSPENDED;
      this.notifications.push('Warning: balance below minimum');
    }
  }

  record(kind, cents, description) {
    this.transactions.push({
      timestamp: this.clock(),
      kind,
      amountCents: cents,
      balanceAfterCents: this.balanceCents,
      description,
    });
  }
}

module.exports = {
  BankAccount,
  toCents,
  POLICIES,
  REGISTERED_PAYEES,
  ACCOUNT_TYPES: { SAVINGS, CHECKING, PREMIUM },
  STATES: { ACTIVE, FROZEN, SUSPENDED, CLOSED },
};
