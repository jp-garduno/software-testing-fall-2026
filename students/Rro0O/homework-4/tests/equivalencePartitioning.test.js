/** Equivalence partitioning tests (design: design/test-design-document.md, section 1). */
const { BankAccount } = require('../src/bankingSystem');
const { TODAY, makeAccount, makeChecking } = require('../jest.setup');

describe('Transfer amount partitions (EP1-EP7)', () => {
  test('EP1: valid amount within limits succeeds', () => {
    const account = makeChecking();
    expect(account.transfer(500).success).toBe(true);
    expect(account.balance).toBe(9500);
  });

  test.each([
    ['EP2: zero amount', 0],
    ['EP3: negative amount', -100],
  ])('%s is rejected as not positive', (_name, amount) => {
    const account = makeChecking();
    const result = account.transfer(amount);
    expect(result.success).toBe(false);
    expect(result.error).toBe('Amount must be positive');
    expect(account.balance).toBe(10000);
  });

  test('EP4: amount over the daily limit is rejected', () => {
    const account = makeChecking();
    const result = account.transfer(100000);
    expect(result.success).toBe(false);
    expect(result.errors).toContain('Exceeds daily limit');
    expect(account.dailyTransferTotal).toBe(0);
  });

  test('EP5: amount over the balance is rejected', () => {
    const account = makeAccount('Checking', 300);
    const result = account.transfer(301);
    expect(result.success).toBe(false);
    expect(result.error).toBe('Insufficient funds');
    expect(account.balance).toBe(300);
  });

  test.each(['abc', null, undefined, true, [500], NaN, Infinity])('EP6: non numeric amount %p is rejected', (bad) => {
    const account = makeChecking();
    const result = account.transfer(bad);
    expect(result.success).toBe(false);
    expect(result.error).toBe('Amount must be a number');
    expect(account.balance).toBe(10000);
  });

  test('EP7: more than two decimals is rejected', () => {
    const result = makeChecking().transfer(10.005);
    expect(result.success).toBe(false);
    expect(result.error).toContain('2 decimal places');
  });
});

describe('Account type partitions (EP8-EP11)', () => {
  test.each([
    ['EP8: Savings', 'Savings', 2000],
    ['EP9: Checking', 'Checking', 5000],
    ['EP10: Premium', 'Premium', 50000],
  ])('%s has its daily limit', (_name, type, limit) => {
    const account = makeAccount(type, type === 'Premium' ? 100000 : 10000);
    expect(account.getDailyLimit()).toBe(limit);
    expect(account.transfer(limit).success).toBe(true);
    expect(account.transfer(1).success).toBe(false);
  });

  test('EP11: unknown account type is rejected', () => {
    expect(() => new BankAccount('Gold', 1000)).toThrow('Invalid account type');
  });
});

describe('Initial balance partitions (EP12-EP15)', () => {
  test('EP12: negative balance is rejected', () => {
    expect(() => new BankAccount('Checking', -1)).toThrow('cannot be negative');
  });

  test('EP13: balance below the type minimum is rejected', () => {
    expect(() => new BankAccount('Savings', 50)).toThrow('below the Savings minimum');
  });

  test('EP14: balance above the minimum creates an Active account', () => {
    const account = new BankAccount('Savings', 500);
    expect(account.state).toBe('Active');
    expect(account.balance).toBe(500);
  });

  test('EP15: non numeric balance is rejected', () => {
    expect(() => new BankAccount('Checking', 'lots')).toThrow('must be a number');
  });
});

describe('Account state partitions (EP16-EP19)', () => {
  test('EP16: Active account can transfer without warning', () => {
    const result = makeChecking().transfer(100);
    expect(result.success).toBe(true);
    expect(result.warning).toBeNull();
  });

  test('EP17: Suspended account can transfer with the account still suspended', () => {
    const account = makeAccount('Savings', 150);
    account.transfer(60);
    expect(account.state).toBe('Suspended');
    expect(account.transfer(10).success).toBe(true);
    expect(account.balance).toBe(80);
  });

  test('EP18: Frozen account cannot transfer', () => {
    const account = makeChecking();
    account.freeze();
    const result = account.transfer(100);
    expect(result.success).toBe(false);
    expect(result.error).toBe('Account is frozen');
    expect(account.getBalance()).toBe(10000);
  });

  test('EP19: Closed account cannot transfer', () => {
    const account = makeChecking();
    account.close();
    expect(account.transfer(100).error).toBe('Account is closed');
  });
});

describe('Payee partitions (EP20-EP23)', () => {
  test('EP20: registered payee is paid', () => {
    const account = makeChecking();
    expect(account.payBill('CFE Electricity', 250, { onDate: TODAY }).success).toBe(true);
    expect(account.balance).toBe(9750);
  });

  test('EP21: unregistered payee is rejected', () => {
    const account = makeChecking();
    const result = account.payBill('Random Store', 250, { onDate: TODAY });
    expect(result.error).toBe('Invalid payee');
    expect(account.balance).toBe(10000);
  });

  test.each(['', '   ', null])('EP22/EP23: blank or missing payee %p is rejected', (blank) => {
    const result = makeChecking().payBill(blank, 250, { onDate: TODAY });
    expect(result.success).toBe(false);
    expect(result.error).toBe('Payee is required');
  });
});

describe('Payment date partitions (EP24-EP27)', () => {
  test('EP24: no date pays immediately', () => {
    const account = makeChecking();
    expect(account.payBill('Telmex Internet', 100, { onDate: TODAY }).scheduled).toBe(false);
    expect(account.balance).toBe(9900);
  });

  test('EP25: future date schedules without debit', () => {
    const account = makeChecking();
    const result = account.payBill('Telmex Internet', 100, { paymentDate: '2026-10-01', onDate: TODAY });
    expect(result.scheduled).toBe(true);
    expect(account.balance).toBe(10000);
    expect(account.scheduledPayments[0].date).toBe('2026-10-01');
  });

  test('EP26: past date is rejected', () => {
    const result = makeChecking().payBill('Telmex Internet', 100, { paymentDate: '2026-09-01', onDate: TODAY });
    expect(result.error).toBe('Payment date cannot be in the past');
  });

  test('EP27: malformed date is rejected', () => {
    const result = makeChecking().payBill('Telmex Internet', 100, { paymentDate: '15/09/2026', onDate: TODAY });
    expect(result.error).toBe('Invalid payment date');
  });
});

describe('History date range partitions (EP28-EP34)', () => {
  const accountWithHistory = () => {
    const account = makeAccount('Checking', 1000);
    ['2026-09-01', '2026-09-10', '2026-09-20'].forEach((day) => account.deposit(100, { onDate: day }));
    return account;
  };

  test('EP28: range containing transactions', () => {
    const rows = accountWithHistory().getHistory('2026-09-05', '2026-09-15');
    expect(rows.map((row) => row.date)).toEqual(['2026-09-10']);
  });

  test('EP29: range without transactions is empty', () => {
    expect(accountWithHistory().getHistory('2026-08-01', '2026-08-31')).toEqual([]);
  });

  test('EP30: only start date', () => {
    expect(accountWithHistory().getHistory('2026-09-10')).toHaveLength(2);
  });

  test('EP31: only end date', () => {
    expect(accountWithHistory().getHistory(undefined, '2026-09-10')).toHaveLength(2);
  });

  test('EP32: start after end is rejected', () => {
    expect(() => accountWithHistory().getHistory('2026-09-20', '2026-09-01')).toThrow('must not be after');
  });

  test('EP33: malformed date is rejected', () => {
    expect(() => accountWithHistory().getHistory('yesterday', '2026-09-01')).toThrow('Invalid date');
    expect(() => accountWithHistory().getHistory('2026-02-30')).toThrow('Invalid date');
  });

  test('EP34: no filter returns everything', () => {
    expect(accountWithHistory().getHistory()).toHaveLength(3);
  });
});

describe('Deposit and date input partitions (EP35-EP37)', () => {
  test.each([0, -5, 'ten', 1.234])('EP35: invalid deposit amount %p is rejected', (bad) => {
    const account = makeChecking();
    expect(account.deposit(bad).success).toBe(false);
    expect(account.balance).toBe(10000);
  });

  test('EP36: valid deposit increases the balance', () => {
    const account = makeChecking();
    expect(account.deposit(250.5).success).toBe(true);
    expect(account.balance).toBe(10250.5);
  });

  test('EP37: Date objects and ISO strings identify the same day; other types do not', () => {
    const account = makeChecking();
    account.deposit(1, { onDate: new Date(2026, 8, 1) });
    account.deposit(1, { onDate: '2026-09-01' });
    expect(account.getHistory('2026-09-01', '2026-09-01')).toHaveLength(2);
    expect(account.processMonthlyFee(12345).error).toBe('Invalid date');
  });
});
