'use strict';

// Independent implementation of the contract in design/test-design-document.md.
const RULES = new Map([
  ['Savings', [10000, 500, 100000, 200000]],
  ['Checking', [0, 1000, 500000, 500000]],
  ['Premium', [1000000, 0, 0, 5000000]],
]);
const PAYEES = ['utilities', 'credit-card', 'internet'];
const MAX_CENTS = 100_000_000_000;

class BankingError extends Error {}
const fail = (message) => { throw new BankingError(message); };

function money(value) {
  if (typeof value !== 'number' || !Number.isFinite(value)) fail('Invalid amount');
  // Parse the decimal representation instead of rounding away sub-cent values.
  const [coefficient, exponentText = '0'] = String(value).toLowerCase().split('e');
  const [whole, fraction = ''] = coefficient.split('.');
  const scale = fraction.length - Number(exponentText);
  const digits = BigInt(whole + fraction);
  let cents;
  if (scale <= 2) {
    cents = digits * (10n ** BigInt(2 - scale));
  } else {
    const divisor = 10n ** BigInt(scale - 2);
    if (digits % divisor !== 0n) fail('Invalid amount');
    cents = digits / divisor;
  }
  if (cents > BigInt(MAX_CENTS) || cents < -BigInt(MAX_CENTS)) fail('Invalid amount');
  return Number(cents);
}

function isoDate(value) {
  if (typeof value !== 'string' || !/^[0-9]{4}-[0-9]{2}-[0-9]{2}$/.test(value)
      || value.length !== 10 || value.startsWith('0000')) fail('Invalid date');
  const parsed = new Date(`${value}T00:00:00.000Z`);
  if (!Number.isFinite(parsed.getTime()) || parsed.toISOString().slice(0, 10) !== value) {
    fail('Invalid date');
  }
  return value;
}

class BankAccount {
  #type; #minimum; #fee; #waiver; #limit; #balance; #state; #clock; #day;
  #dailyTotal = 0;
  #feeMonths = new Set();
  #transactions = [];
  #scheduled = [];
  #owner = 'Customer';

  constructor(accountType, initialBalance, clock = () => new Date().toISOString().slice(0, 10)) {
    if (!RULES.has(accountType)) fail('Invalid account type');
    let balance;
    try {
      balance = money(initialBalance);
      if (balance < 0) fail('Invalid amount');
    } catch (error) {
      if (!(error instanceof BankingError)) throw error;
      fail('Invalid opening balance');
    }
    this.#type = accountType;
    [this.#minimum, this.#fee, this.#waiver, this.#limit] = RULES.get(accountType);
    this.#balance = balance;
    this.#state = balance >= this.#minimum ? 'Active' : 'Suspended';
    this.#clock = clock;
    this.#day = isoDate(clock());
  }

  #rollDay() {
    const today = isoDate(this.#clock());
    if (today !== this.#day) {
      this.#dailyTotal = 0;
      this.#day = today;
    }
  }

  #run(operation) {
    this.#rollDay();
    try {
      return { success: true, ...operation() };
    } catch (error) {
      if (!(error instanceof BankingError)) throw error;
      return { success: false, error: error.message };
    }
  }

  #requireState(...allowed) {
    if (!allowed.includes(this.#state)) fail(`Account ${this.#state.toLowerCase()}`);
  }

  #positive(amount) {
    const cents = money(amount);
    if (cents <= 0) fail('Amount must be positive');
    return cents;
  }

  #funds(cents) {
    if (cents > this.#balance) fail('Insufficient funds');
  }

  #record(kind, cents, detail) {
    this.#transactions.push({ date: this.#day, kind, amount: cents / 100,
      balance: this.#balance / 100, detail });
  }

  #debit(kind, cents, detail) {
    this.#balance -= cents;
    this.#record(kind, cents, detail);
    if (this.#balance < this.#minimum) this.#state = 'Suspended';
  }

  get_daily_limit() { return this.#limit / 100; }

  snapshot() {
    this.#rollDay();
    return { account_type: this.#type, balance: this.#balance / 100, state: this.#state,
      daily_transfer_total: this.#dailyTotal / 100, daily_limit: this.get_daily_limit(),
      warning: this.#state === 'Suspended', transaction_count: this.#transactions.length,
      pending_count: this.#scheduled.length, owner: this.#owner };
  }

  transfer(amount, destination = 'external') {
    return this.#run(() => {
      this.#requireState('Active');
      const cents = this.#positive(amount);
      if (typeof destination !== 'string' || !destination.trim()) fail('Invalid destination');
      this.#funds(cents);
      if (this.#dailyTotal + cents > this.#limit) fail('Exceeds daily limit');
      this.#dailyTotal += cents;
      this.#debit('transfer', cents, destination);
      return { amount: cents / 100 };
    });
  }

  deposit(amount) {
    return this.#run(() => {
      this.#requireState('Active', 'Suspended');
      const cents = this.#positive(amount);
      if (this.#balance + cents > MAX_CENTS) fail('Balance exceeds maximum');
      this.#balance += cents;
      if (this.#balance >= this.#minimum) this.#state = 'Active';
      this.#record('deposit', cents, 'deposit');
      return { amount: cents / 100 };
    });
  }

  pay_bill(payee, amount, paymentDate = null) {
    return this.#run(() => {
      this.#requireState('Active');
      const cents = this.#positive(amount);
      if (!PAYEES.includes(payee)) fail('Invalid payee');
      const due = paymentDate === null ? this.#day : isoDate(paymentDate);
      if (due < this.#day) fail('Payment date is in the past');
      this.#funds(cents);
      if (due > this.#day) {
        this.#scheduled.push({ date: due, payee, amount: cents / 100 });
        return { status: 'scheduled' };
      }
      this.#debit('bill', cents, payee);
      return { status: 'paid' };
    });
  }

  process_scheduled() {
    return this.#run(() => {
      this.#requireState('Active', 'Suspended', 'Frozen');
      const payments = [];
      const pending = [];
      for (const payment of this.#scheduled) {
        if (payment.date <= this.#day) {
          const result = this.pay_bill(payment.payee, payment.amount);
          payments.push({ ...payment, result });
        } else pending.push(payment);
      }
      this.#scheduled = pending;
      return { payments };
    });
  }

  process_fee() {
    return this.#run(() => {
      this.#requireState('Active', 'Suspended');
      const month = this.#day.slice(0, 7);
      if (!this.#day.endsWith('01') || this.#feeMonths.has(month)) return { charged: 0 };
      this.#feeMonths.add(month);
      const fee = this.#balance > this.#waiver ? 0 : this.#fee;
      if (this.#balance < fee) {
        this.#state = 'Suspended';
        fail('Insufficient fee funds');
      }
      if (fee) this.#debit('fee', fee, 'monthly fee');
      return { charged: fee / 100 };
    });
  }

  freeze() {
    return this.#run(() => {
      this.#requireState('Active');
      this.#state = 'Frozen';
      return { state: this.#state };
    });
  }

  unfreeze() {
    return this.#run(() => {
      if (this.#state === 'Closed') fail('Account closed');
      if (this.#state !== 'Frozen') fail('Account is not frozen');
      this.#state = 'Active';
      return { state: this.#state };
    });
  }

  close() {
    return this.#run(() => {
      this.#requireState('Active', 'Suspended', 'Frozen');
      this.#state = 'Closed';
      return { balance: this.#balance / 100 };
    });
  }

  update_info(owner) {
    return this.#run(() => {
      this.#requireState('Active', 'Suspended');
      if (typeof owner !== 'string' || !owner.trim()) fail('Invalid owner');
      this.#owner = owner.trim();
      return { owner: this.#owner };
    });
  }

  #history(start, end) {
    isoDate(start);
    isoDate(end);
    if (start > end) fail('Invalid date range');
    return this.#transactions.filter((item) => start <= item.date && item.date <= end)
      .map((item) => ({ ...item }));
  }

  history(start, end) {
    return this.#run(() => ({ transactions: this.#history(start, end) }));
  }

  export_csv(start, end) {
    return this.#run(() => {
      const rows = ['date,kind,amount,balance,detail'];
      for (const item of this.#history(start, end)) {
        const detail = item.detail.replaceAll('"', '""');
        rows.push(`${item.date},${item.kind},${item.amount.toFixed(2)},${item.balance.toFixed(2)},"${detail}"`);
      }
      return { csv: `${rows.join('\n')}\n` };
    });
  }
}

module.exports = BankAccount;
