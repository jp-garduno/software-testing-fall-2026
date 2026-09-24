/**
 * SecureBank online banking domain model (JavaScript port).
 *
 * Mirrors src/banking_system.py rule for rule so that the Jest suite under js/tests can assert the
 * same black box design. Money is held internally as an integer number of cents.
 */

const ACCOUNT_RULES = {
  Savings: {
    minBalance: 100.0,
    monthlyFee: 5.0,
    feeWaiver: 1000.0,
    dailyLimit: 2000.0,
  },
  Checking: {
    minBalance: 0.0,
    monthlyFee: 10.0,
    feeWaiver: 5000.0,
    dailyLimit: 5000.0,
  },
  Premium: {
    minBalance: 10000.0,
    monthlyFee: 0.0,
    feeWaiver: 0.0,
    dailyLimit: 50000.0,
  },
};

const ACTIVE = "Active";
const FROZEN = "Frozen";
const SUSPENDED = "Suspended";
const CLOSED = "Closed";

const ERRORS = {
  INVALID_TYPE: "Unknown account type",
  INVALID_AMOUNT: "Amount must be numeric",
  AMOUNT_PRECISION: "Amount must be specified in whole cents",
  AMOUNT_POSITIVE: "Amount must be positive",
  DAILY_LIMIT: "Exceeds daily limit",
  INSUFFICIENT: "Insufficient funds",
  FROZEN: "Account frozen",
  CLOSED: "Account closed",
  OPENING_DEPOSIT: "Initial deposit below minimum balance",
  UNKNOWN_PAYEE: "Unknown payee",
  INACTIVE_PAYEE: "Payee is not active",
  PAST_DATE: "Scheduled date cannot be in the past",
  DATE_ORDER: "Start date must not be after end date",
  DATE_TYPE: "Date range must use date objects",
  NOT_FROZEN: "Account is not frozen",
};

const WARN_BELOW_MINIMUM = "Balance is below the minimum for this account type";

class AmountError extends Error {}

/** Convert a dollar amount to an integer number of cents. */
function toCents(amount) {
  if (typeof amount === "boolean" || amount === null || amount === undefined) {
    throw new AmountError(ERRORS.INVALID_AMOUNT);
  }
  if (typeof amount !== "number" && typeof amount !== "string") {
    throw new AmountError(ERRORS.INVALID_AMOUNT);
  }
  const text = String(amount).trim();
  if (!/^-?\d+(\.\d+)?$/.test(text)) {
    if (/^-?\d+(\.\d+)?e[+-]?\d+$/i.test(text)) {
      throw new AmountError(ERRORS.AMOUNT_PRECISION);
    }
    throw new AmountError(ERRORS.INVALID_AMOUNT);
  }
  const decimals = text.includes(".") ? text.split(".")[1].length : 0;
  if (decimals > 2) {
    throw new AmountError(ERRORS.AMOUNT_PRECISION);
  }
  return Math.round(Number(text) * 100);
}

/** Convert an integer number of cents back to a dollar amount. */
function toDollars(cents) {
  return Math.round(cents) / 100;
}

/** Build the standard failure envelope returned by every operation. */
function failure(error) {
  return { success: false, error };
}

function isDate(value) {
  return value instanceof Date && !Number.isNaN(value.getTime());
}

function dayValue(value) {
  return Date.UTC(
    value.getUTCFullYear(),
    value.getUTCMonth(),
    value.getUTCDate(),
  );
}

function isoDay(value) {
  return new Date(dayValue(value)).toISOString().slice(0, 10);
}

/** A bill payment recipient registered by the customer. */
class Payee {
  constructor(payeeId, name, active = true) {
    this.payeeId = payeeId;
    this.name = name;
    this.active = active;
  }
}

/** A SecureBank account with its balance, state and daily transfer usage. */
class BankAccount {
  constructor(accountType, initialBalance, state = ACTIVE) {
    if (!Object.prototype.hasOwnProperty.call(ACCOUNT_RULES, accountType)) {
      throw new Error(ERRORS.INVALID_TYPE);
    }
    this.accountType = accountType;
    this.balanceCents = toCents(initialBalance);
    this.state = state;
    this.dailyTransferCents = 0;
    this.transactions = [];
    this.payees = new Map();
    this.notifications = [];
  }

  get balance() {
    return toDollars(this.balanceCents);
  }

  get dailyTransferTotal() {
    return toDollars(this.dailyTransferCents);
  }

  getDailyLimit() {
    return ACCOUNT_RULES[this.accountType].dailyLimit;
  }

  getMinimumBalance() {
    return ACCOUNT_RULES[this.accountType].minBalance;
  }

  getMonthlyFee() {
    return ACCOUNT_RULES[this.accountType].monthlyFee;
  }

  getFeeWaiverThreshold() {
    return ACCOUNT_RULES[this.accountType].feeWaiver;
  }

  isBelowMinimum() {
    return this.balanceCents < toCents(this.getMinimumBalance());
  }

  registerPayee(payeeId, name, active = true) {
    const payee = new Payee(payeeId, name, active);
    this.payees.set(payeeId, payee);
    return payee;
  }

  resetDailyLimit() {
    this.dailyTransferCents = 0;
  }

  transfer(amount, destination = "external") {
    const blocked = this.stateGuard();
    if (blocked) return blocked;

    let amountCents;
    try {
      amountCents = toCents(amount);
    } catch (error) {
      return failure(error.message);
    }
    if (amountCents <= 0) return failure(ERRORS.AMOUNT_POSITIVE);
    if (this.dailyTransferCents + amountCents > toCents(this.getDailyLimit())) {
      return failure(ERRORS.DAILY_LIMIT);
    }
    if (amountCents > this.balanceCents) return failure(ERRORS.INSUFFICIENT);

    this.balanceCents -= amountCents;
    this.dailyTransferCents += amountCents;
    this.record("transfer", amountCents, destination);
    return this.success({ amount: toDollars(amountCents), destination });
  }

  payBill(payeeId, amount, scheduledDate = null, today = null) {
    const blocked = this.stateGuard();
    if (blocked) return blocked;

    const payee = this.payees.get(payeeId);
    if (!payee) return failure(ERRORS.UNKNOWN_PAYEE);
    if (!payee.active) return failure(ERRORS.INACTIVE_PAYEE);

    let amountCents;
    try {
      amountCents = toCents(amount);
    } catch (error) {
      return failure(error.message);
    }
    if (amountCents <= 0) return failure(ERRORS.AMOUNT_POSITIVE);

    const reference = today || new Date();
    if (scheduledDate && dayValue(scheduledDate) < dayValue(reference)) {
      return failure(ERRORS.PAST_DATE);
    }
    if (amountCents > this.balanceCents) return failure(ERRORS.INSUFFICIENT);

    if (scheduledDate && dayValue(scheduledDate) > dayValue(reference)) {
      this.record("scheduled_payment", amountCents, payee.name, scheduledDate);
      return this.success({
        scheduled: true,
        date: scheduledDate,
        amount: toDollars(amountCents),
      });
    }

    this.balanceCents -= amountCents;
    this.record("bill_payment", amountCents, payee.name, reference);
    return this.success({ scheduled: false, amount: toDollars(amountCents) });
  }

  deposit(amount) {
    if (this.state === CLOSED) return failure(ERRORS.CLOSED);
    if (this.state === FROZEN) return failure(ERRORS.FROZEN);

    let amountCents;
    try {
      amountCents = toCents(amount);
    } catch (error) {
      return failure(error.message);
    }
    if (amountCents <= 0) return failure(ERRORS.AMOUNT_POSITIVE);

    this.balanceCents += amountCents;
    this.record("deposit", amountCents, "self");
    if (this.state === SUSPENDED && !this.isBelowMinimum()) {
      this.state = ACTIVE;
    }
    return this.success({ amount: toDollars(amountCents) });
  }

  applyMonthlyFee() {
    if (this.state === CLOSED) return failure(ERRORS.CLOSED);

    const feeCents = toCents(this.getMonthlyFee());
    if (feeCents === 0) return this.success({ charged: 0.0, waived: true });
    if (this.balanceCents > toCents(this.getFeeWaiverThreshold())) {
      return this.success({ charged: 0.0, waived: true });
    }
    if (feeCents > this.balanceCents) {
      this.state = SUSPENDED;
      this.notifications.push(ERRORS.INSUFFICIENT);
      return failure(ERRORS.INSUFFICIENT);
    }

    this.balanceCents -= feeCents;
    this.record("monthly_fee", feeCents, "SecureBank");
    return this.success({ charged: toDollars(feeCents), waived: false });
  }

  freeze() {
    if (this.state === CLOSED) return failure(ERRORS.CLOSED);
    this.state = FROZEN;
    return this.success({ state: this.state });
  }

  unfreeze() {
    if (this.state === CLOSED) return failure(ERRORS.CLOSED);
    if (this.state !== FROZEN) return failure(ERRORS.NOT_FROZEN);
    this.state = this.isBelowMinimum() ? SUSPENDED : ACTIVE;
    return this.success({ state: this.state });
  }

  close() {
    if (this.state === CLOSED) return failure(ERRORS.CLOSED);
    this.state = CLOSED;
    return this.success({
      state: this.state,
      finalStatement: this.exportCsv(),
    });
  }

  getTransactions(startDate = null, endDate = null) {
    for (const bound of [startDate, endDate]) {
      if (bound !== null && !isDate(bound)) return failure(ERRORS.DATE_TYPE);
    }
    if (startDate && endDate && dayValue(startDate) > dayValue(endDate)) {
      return failure(ERRORS.DATE_ORDER);
    }
    const rows = this.transactions.filter(
      (row) =>
        (!startDate || dayValue(row.date) >= dayValue(startDate)) &&
        (!endDate || dayValue(row.date) <= dayValue(endDate)),
    );
    return this.success({ transactions: rows, count: rows.length });
  }

  exportCsv() {
    const lines = ["date,type,amount,counterparty"];
    for (const row of this.transactions) {
      lines.push(
        `${isoDay(row.date)},${row.type},${row.amount.toFixed(2)},${row.counterparty}`,
      );
    }
    return lines.join("\n");
  }

  stateGuard() {
    if (this.state === CLOSED) return failure(ERRORS.CLOSED);
    if (this.state === FROZEN) return failure(ERRORS.FROZEN);
    return null;
  }

  success(payload) {
    const warnings = [];
    if (
      (this.state === ACTIVE || this.state === SUSPENDED) &&
      this.isBelowMinimum()
    ) {
      if (this.state === ACTIVE) this.notifications.push(WARN_BELOW_MINIMUM);
      this.state = SUSPENDED;
      warnings.push(WARN_BELOW_MINIMUM);
    }
    return {
      success: true,
      state: this.state,
      balance: this.balance,
      warnings,
      ...payload,
    };
  }

  record(kind, amountCents, counterparty, when = null) {
    this.transactions.push({
      date: when || new Date(),
      type: kind,
      amount: toDollars(amountCents),
      counterparty,
    });
  }
}

/** Open a new account, enforcing the account type and opening deposit rules. */
function createAccount(accountType, initialBalance) {
  if (!Object.prototype.hasOwnProperty.call(ACCOUNT_RULES, accountType)) {
    return failure(ERRORS.INVALID_TYPE);
  }
  let balanceCents;
  try {
    balanceCents = toCents(initialBalance);
  } catch (error) {
    return failure(error.message);
  }
  if (balanceCents < 0) return failure(ERRORS.AMOUNT_POSITIVE);
  if (balanceCents < toCents(ACCOUNT_RULES[accountType].minBalance)) {
    return failure(ERRORS.OPENING_DEPOSIT);
  }
  const account = new BankAccount(accountType, toDollars(balanceCents));
  return {
    success: true,
    account,
    state: account.state,
    balance: account.balance,
  };
}

module.exports = {
  ACCOUNT_RULES,
  ACTIVE,
  FROZEN,
  SUSPENDED,
  CLOSED,
  ERRORS,
  WARN_BELOW_MINIMUM,
  BankAccount,
  Payee,
  createAccount,
  toCents,
  toDollars,
};
