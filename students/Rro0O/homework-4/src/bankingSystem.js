/**
 * SecureBank online banking system: JavaScript port of src/banking_system.py.
 *
 * Every operation returns a result object instead of throwing:
 *   { success: boolean, error: string | null, errors: string[], ... }
 * Money is computed in integer cents to avoid floating point drift.
 */

const ACCOUNT_TYPES = {
  Savings: { minBalance: 100, monthlyFee: 5, feeWaiverAbove: 1000, dailyLimit: 2000 },
  Checking: { minBalance: 0, monthlyFee: 10, feeWaiverAbove: 5000, dailyLimit: 5000 },
  Premium: { minBalance: 10000, monthlyFee: 0, feeWaiverAbove: 0, dailyLimit: 50000 },
};

const STATE_ACTIVE = 'Active';
const STATE_FROZEN = 'Frozen';
const STATE_SUSPENDED = 'Suspended';
const STATE_CLOSED = 'Closed';

// States in which money may move. Suspended accounts keep working (with a warning).
const OPERABLE_STATES = [STATE_ACTIVE, STATE_SUSPENDED];

const VALID_PAYEES = {
  'CFE Electricity': 'utilities',
  'Telmex Internet': 'utilities',
  'SIAPA Water': 'utilities',
  'Visa Credit Card': 'credit card',
  'Mastercard Credit Card': 'credit card',
};

const CSV_HEADER = ['date', 'type', 'amount', 'balance_after', 'description'];

const pad = (number) => String(number).padStart(2, '0');

/** Convert dollars to integer cents. */
const toCents = (dollars) => Math.round(dollars * 100);

/** Convert integer cents to dollars. */
const fromCents = (cents) => cents / 100;

/**
 * Normalise a Date or 'YYYY-MM-DD' string to an ISO day string; null if invalid.
 * @param {Date|string} value
 * @returns {string|null}
 */
function parseDate(value) {
  if (value instanceof Date && !Number.isNaN(value.getTime())) {
    return `${value.getFullYear()}-${pad(value.getMonth() + 1)}-${pad(value.getDate())}`;
  }
  if (typeof value === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(value)) {
    const [year, month, day] = value.split('-').map(Number);
    const check = new Date(Date.UTC(year, month - 1, day));
    const isRealDate =
      check.getUTCFullYear() === year && check.getUTCMonth() === month - 1 && check.getUTCDate() === day;
    return isRealDate ? value : null;
  }
  return null;
}

/** @returns {string} today's date as an ISO day string */
function today() {
  return parseDate(new Date());
}

/**
 * Validate a monetary amount.
 * @param {*} amount
 * @returns {{cents: number|null, error: string|null}}
 */
function validateAmount(amount) {
  if (typeof amount !== 'number' || !Number.isFinite(amount)) {
    return { cents: null, error: 'Amount must be a number' };
  }
  if (amount <= 0) {
    return { cents: null, error: 'Amount must be positive' };
  }
  const scaled = amount * 100;
  if (Math.abs(scaled - Math.round(scaled)) > 1e-6) {
    return { cents: null, error: 'Amount must have at most 2 decimal places' };
  }
  return { cents: Math.round(scaled), error: null };
}

const fail = (...errors) => ({ success: false, error: errors[0], errors });
const ok = (extra = {}) => ({ success: true, error: null, errors: [], ...extra });

const csvField = (value) => {
  const text = String(value);
  return /[",\n]/.test(text) ? `"${text.replace(/"/g, '""')}"` : text;
};

class BankAccount {
  /**
   * @param {string} accountType Savings | Checking | Premium
   * @param {number} initialBalance
   * @param {string} [owner]
   * @param {string|null} [email]
   */
  constructor(accountType, initialBalance, owner = 'Customer', email = null) {
    if (!Object.prototype.hasOwnProperty.call(ACCOUNT_TYPES, accountType)) {
      throw new Error(`Invalid account type: '${accountType}'`);
    }
    if (typeof initialBalance !== 'number' || Number.isNaN(initialBalance)) {
      throw new Error('Initial balance must be a number');
    }
    const minimum = ACCOUNT_TYPES[accountType].minBalance;
    if (initialBalance < 0) {
      throw new Error('Initial balance cannot be negative');
    }
    if (initialBalance < minimum) {
      throw new Error(`Initial balance is below the ${accountType} minimum of ${minimum}`);
    }
    if (typeof owner !== 'string' || owner.trim() === '') {
      throw new Error('Owner name is required');
    }
    this.accountType = accountType;
    this.balance = initialBalance;
    this.owner = owner.trim();
    this.email = email;
    this.state = STATE_ACTIVE;
    this.dailyTransferTotal = 0;
    this.unpaidFees = 0;
    this.scheduledPayments = [];
    this.transactions = [];
    this.lastActivityDay = null;
  }

  // ------------------------------------------------------------------ helpers
  getDailyLimit() {
    return ACCOUNT_TYPES[this.accountType].dailyLimit;
  }

  getMinimumBalance() {
    return ACCOUNT_TYPES[this.accountType].minBalance;
  }

  resetDailyTotalIfNewDay(day) {
    if (this.lastActivityDay !== day) {
      this.dailyTransferTotal = 0;
      this.lastActivityDay = day;
    }
  }

  record(day, type, amount, description) {
    this.transactions.push({ date: day, type, amount, balanceAfter: this.balance, description });
  }

  /** Apply Active <-> Suspended transitions; returns a warning when the account was just suspended. */
  refreshStateAfterBalanceChange() {
    const belowMinimum = this.balance < this.getMinimumBalance();
    if (this.state === STATE_ACTIVE && belowMinimum) {
      this.state = STATE_SUSPENDED;
      return 'Balance is below the minimum: account suspended';
    }
    if (this.state === STATE_SUSPENDED && !belowMinimum) {
      this.state = STATE_ACTIVE;
    }
    return null;
  }

  stateError() {
    if (this.state === STATE_FROZEN) return 'Account is frozen';
    if (this.state === STATE_CLOSED) return 'Account is closed';
    return null;
  }

  debit(cents, day, type, description) {
    this.balance = fromCents(toCents(this.balance) - cents);
    const warning = this.refreshStateAfterBalanceChange();
    this.record(day, type, -fromCents(cents), description);
    return warning;
  }

  // ------------------------------------------------------------------- money
  /**
   * Transfer money out of this account. Errors are collected so the decision table can be checked rule by rule.
   * @param {number} amount
   * @param {{destination?: BankAccount|string|null, onDate?: Date|string}} [options]
   */
  transfer(amount, { destination = null, onDate } = {}) {
    const day = parseDate(onDate) || today();
    const stateError = this.stateError();
    if (stateError) return fail(stateError);
    const { cents, error } = validateAmount(amount);
    if (error) return fail(error);
    if (destination === this) return fail('Cannot transfer to the same account');

    this.resetDailyTotalIfNewDay(day);
    const errors = [];
    if (toCents(this.dailyTransferTotal) + cents > toCents(this.getDailyLimit())) {
      errors.push('Exceeds daily limit');
    }
    if (cents > toCents(this.balance)) {
      errors.push('Insufficient funds');
    }
    const isAccount = destination instanceof BankAccount;
    if (isAccount && !OPERABLE_STATES.includes(destination.state)) {
      errors.push('Destination account cannot receive funds');
    }
    if (errors.length > 0) return fail(...errors);

    this.dailyTransferTotal = fromCents(toCents(this.dailyTransferTotal) + cents);
    const label = isAccount ? destination.owner : destination || 'external account';
    const warning = this.debit(cents, day, 'transfer', `Transfer to ${label}`);
    if (isAccount) {
      destination.deposit(fromCents(cents), { onDate: day, description: `Transfer from ${this.owner}` });
    }
    return ok({ warning, state: this.state, balance: this.balance });
  }

  /** Add money; a deposit that restores the minimum reactivates a Suspended account. */
  deposit(amount, { onDate, description = 'Deposit' } = {}) {
    const day = parseDate(onDate) || today();
    const stateError = this.stateError();
    if (stateError) return fail(stateError);
    const { cents, error } = validateAmount(amount);
    if (error) return fail(error);
    this.balance = fromCents(toCents(this.balance) + cents);
    this.refreshStateAfterBalanceChange();
    this.record(day, 'deposit', fromCents(cents), description);
    return ok({ state: this.state, balance: this.balance });
  }

  /** Pay a registered payee now, or schedule the payment for a future date. */
  payBill(payee, amount, { paymentDate, onDate } = {}) {
    const current = parseDate(onDate) || today();
    const stateError = this.stateError();
    if (stateError) return fail(stateError);
    const errors = [];
    if (typeof payee !== 'string' || payee.trim() === '') {
      errors.push('Payee is required');
    } else if (!Object.prototype.hasOwnProperty.call(VALID_PAYEES, payee.trim())) {
      errors.push('Invalid payee');
    }
    const { cents, error } = validateAmount(amount);
    if (error) {
      errors.push(error);
    } else if (cents > toCents(this.balance)) {
      errors.push('Insufficient funds');
    }
    const due = paymentDate === undefined || paymentDate === null ? current : parseDate(paymentDate);
    if (due === null) {
      errors.push('Invalid payment date');
    } else if (due < current) {
      errors.push('Payment date cannot be in the past');
    }
    if (errors.length > 0) return fail(...errors);

    const name = payee.trim();
    if (due > current) {
      this.scheduledPayments.push({ payee: name, amount: fromCents(cents), date: due });
      return ok({ scheduled: true, paymentDate: due, balance: this.balance });
    }
    const warning = this.debit(cents, current, 'bill payment', `Bill payment to ${name}`);
    return ok({ scheduled: false, warning, state: this.state, balance: this.balance });
  }

  /** Charge the monthly fee (only on the 1st of the month, waived above the threshold). */
  processMonthlyFee(onDate) {
    const day = parseDate(onDate);
    if (day === null) return fail('Invalid date');
    if (!OPERABLE_STATES.includes(this.state)) return fail(`Fees are not processed for ${this.state} accounts`);
    if (!day.endsWith('-01')) return fail('Monthly fees are only charged on the 1st of the month');

    const rules = ACCOUNT_TYPES[this.accountType];
    const feeCents = toCents(rules.monthlyFee);
    if (feeCents === 0 || this.balance > rules.feeWaiverAbove) {
      return ok({ feeCharged: 0, waived: true, state: this.state, balance: this.balance });
    }
    if (toCents(this.balance) < feeCents) {
      this.unpaidFees = fromCents(toCents(this.unpaidFees) + feeCents);
      this.state = STATE_SUSPENDED;
      return ok({ feeCharged: 0, waived: false, suspended: true, state: this.state, balance: this.balance });
    }
    const warning = this.debit(feeCents, day, 'fee', 'Monthly fee');
    return ok({ feeCharged: fromCents(feeCents), waived: false, warning, state: this.state, balance: this.balance });
  }

  // --------------------------------------------------------- account lifecycle
  /** Active -> Frozen (customer request or fraud detection). */
  freeze(reason = 'customer request') {
    if (this.state !== STATE_ACTIVE) return fail(`Cannot freeze an account in state ${this.state}`);
    this.state = STATE_FROZEN;
    return ok({ state: this.state, reason });
  }

  /** Frozen -> Active. */
  unfreeze() {
    if (this.state !== STATE_FROZEN) return fail(`Cannot unfreeze an account in state ${this.state}`);
    this.state = STATE_ACTIVE;
    return ok({ state: this.state });
  }

  /** Any state -> Closed. Closed accounts can never be reopened. */
  close() {
    if (this.state === STATE_CLOSED) return fail('Account is closed');
    this.state = STATE_CLOSED;
    const finalStatement = { owner: this.owner, finalBalance: this.balance, transactions: this.transactions.length };
    return ok({ state: this.state, finalStatement });
  }

  /** Closed accounts cannot be reopened; every other state is left untouched. */
  reopen() {
    return fail(this.state === STATE_CLOSED ? 'Account is closed' : 'Account is not closed');
  }

  /** Update the owner name and/or e-mail. Not allowed on closed accounts. */
  updateInfo({ owner, email } = {}) {
    if (this.state === STATE_CLOSED) return fail('Account is closed');
    const errors = [];
    if (owner !== undefined && (typeof owner !== 'string' || owner.trim() === '')) {
      errors.push('Owner name is required');
    }
    if (email !== undefined && (typeof email !== 'string' || !email.includes('@'))) {
      errors.push('Invalid e-mail address');
    }
    if (errors.length > 0) return fail(...errors);
    if (owner !== undefined) this.owner = owner.trim();
    if (email !== undefined) this.email = email;
    return ok({ owner: this.owner, email: this.email });
  }

  /** View the balance (allowed in every state, including Frozen). */
  getBalance() {
    return this.balance;
  }

  // ------------------------------------------------------------ history / CSV
  /**
   * Transactions between start and end (both inclusive, both optional).
   * Throws for unparsable dates or when start is after end.
   */
  getHistory(start, end) {
    const first = start === undefined || start === null ? null : parseDate(start);
    const last = end === undefined || end === null ? null : parseDate(end);
    const startGiven = start !== undefined && start !== null;
    const endGiven = end !== undefined && end !== null;
    if ((startGiven && first === null) || (endGiven && last === null)) {
      throw new Error('Invalid date');
    }
    if (first && last && first > last) {
      throw new Error('Start date must not be after end date');
    }
    return this.transactions.filter((tx) => (!first || tx.date >= first) && (!last || tx.date <= last));
  }

  /** Export the (optionally filtered) history as CSV text. */
  exportCsv(start, end) {
    const rows = this.getHistory(start, end).map((tx) =>
      [tx.date, tx.type, tx.amount.toFixed(2), tx.balanceAfter.toFixed(2), tx.description].map(csvField).join(','),
    );
    return `${[CSV_HEADER.join(','), ...rows].join('\n')}\n`;
  }
}

module.exports = {
  BankAccount,
  ACCOUNT_TYPES,
  VALID_PAYEES,
  parseDate,
  validateAmount,
};
