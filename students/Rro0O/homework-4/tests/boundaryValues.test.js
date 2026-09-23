/** Boundary value analysis tests (design: design/test-design-document.md, section 2). */
const { BankAccount } = require('../src/bankingSystem');
const { TODAY, makeAccount, makeChecking, makeSavings } = require('../jest.setup');

describe('Boundary 1: Checking transfer amount, $5,000 limit (BV1-BV6)', () => {
  test('BV1: $0.00 is below the minimum', () => {
    const result = makeChecking().transfer(0.0);
    expect(result.success).toBe(false);
    expect(result.error).toContain('must be positive');
  });

  test('BV2: exactly $0.01 succeeds', () => {
    const account = makeAccount('Checking', 1000);
    expect(account.transfer(0.01).success).toBe(true);
    expect(account.balance).toBe(999.99);
  });

  test('BV3: $4,999.99 succeeds', () => {
    const account = makeChecking();
    expect(account.transfer(4999.99).success).toBe(true);
    expect(account.dailyTransferTotal).toBe(4999.99);
  });

  test('BV4: exactly $5,000.00 succeeds', () => {
    const account = makeChecking();
    expect(account.transfer(5000).success).toBe(true);
    expect(account.dailyTransferTotal).toBe(5000);
  });

  test.each([
    ['BV5', 5000.01],
    ['BV6', 10000],
  ])('%s: $%p exceeds the daily limit', (_id, amount) => {
    const account = makeChecking();
    const result = account.transfer(amount);
    expect(result.error).toBe('Exceeds daily limit');
    expect(account.balance).toBe(10000);
  });
});

describe('Boundary 2: Savings transfer amount, $2,000 limit (BV7-BV11)', () => {
  test.each([
    [0.01, true],
    [1999.99, true],
    [2000.0, true],
    [2000.01, false],
    [4000.0, false],
  ])('BV7-BV11: transfer of %p succeeds=%p', (amount, expected) => {
    expect(makeSavings().transfer(amount).success).toBe(expected);
  });
});

describe('Boundary 3: transfer amount versus a $1,000 balance (BV12-BV16)', () => {
  test.each([
    [1.0, true, 999.0],
    [999.99, true, 0.01],
    [1000.0, true, 0.0],
    [1000.01, false, 1000.0],
    [1500.0, false, 1000.0],
  ])('BV12-BV16: amount %p succeeds=%p leaving %p', (amount, expected, remaining) => {
    const account = makeAccount('Checking', 1000);
    const result = account.transfer(amount);
    expect(result.success).toBe(expected);
    expect(account.balance).toBe(remaining);
    if (!expected) expect(result.error).toBe('Insufficient funds');
  });
});

describe('Boundary 4: balance versus the minimum (BV17-BV22)', () => {
  test.each([
    [99.99, 100.01, 'Active'],
    [100.0, 100.0, 'Active'],
    [100.01, 99.99, 'Suspended'],
    [199.99, 0.01, 'Suspended'],
    [200.0, 0.0, 'Suspended'],
  ])('BV17-BV21: Savings transfer %p leaves %p -> %s', (amount, remaining, state) => {
    const account = makeAccount('Savings', 200);
    expect(account.transfer(amount).success).toBe(true);
    expect(account.balance).toBe(remaining);
    expect(account.state).toBe(state);
  });

  test('BV22: Premium at $10,000.00 is Active, at $9,999.99 it is Suspended', () => {
    const atMinimum = makeAccount('Premium', 10001);
    const belowMinimum = makeAccount('Premium', 10001);
    atMinimum.transfer(1);
    belowMinimum.transfer(1.01);
    expect(atMinimum.state).toBe('Active');
    expect(belowMinimum.state).toBe('Suspended');
  });
});

describe('Boundary 5: cumulative daily limit (BV23-BV27)', () => {
  test('BV23: $4,999.99 + $0.01 reaches the limit exactly', () => {
    const account = makeChecking();
    expect(account.transfer(4999.99, { onDate: TODAY }).success).toBe(true);
    expect(account.transfer(0.01, { onDate: TODAY }).success).toBe(true);
    expect(account.dailyTransferTotal).toBe(5000);
  });

  test('BV24: one cent over the accumulated limit is rejected', () => {
    const account = makeChecking();
    account.transfer(5000, { onDate: TODAY });
    expect(account.transfer(0.01, { onDate: TODAY }).error).toBe('Exceeds daily limit');
  });

  test('BV25: a rejected transfer does not count towards the limit', () => {
    const account = makeChecking();
    account.transfer(5000.01, { onDate: TODAY });
    expect(account.dailyTransferTotal).toBe(0);
    expect(account.transfer(5000, { onDate: TODAY }).success).toBe(true);
  });

  test('BV26: the limit resets the next day', () => {
    const account = makeChecking();
    account.transfer(5000, { onDate: '2026-09-15' });
    expect(account.transfer(5000, { onDate: '2026-09-16' }).success).toBe(true);
    expect(account.dailyTransferTotal).toBe(5000);
  });

  test('BV27: the limit does not reset within the same day', () => {
    const account = makeChecking();
    account.transfer(5000, { onDate: '2026-09-15' });
    expect(account.transfer(1, { onDate: '2026-09-15' }).success).toBe(false);
    expect(account.transfer(1, { onDate: '2026-09-16' }).success).toBe(true);
  });
});

describe('Boundary 6: fee waiver thresholds (BV28-BV34)', () => {
  test.each([
    [999.99, 5],
    [1000.0, 5],
    [1000.01, 0],
    [1001.0, 0],
  ])('BV28-BV31: Savings $%p pays fee %p', (balance, fee) => {
    const result = makeAccount('Savings', balance).processMonthlyFee('2026-10-01');
    expect(result.feeCharged).toBe(fee);
    expect(result.waived).toBe(fee === 0);
  });

  test.each([
    [4999.99, 10],
    [5000.0, 10],
    [5000.01, 0],
  ])('BV32-BV34: Checking $%p pays fee %p', (balance, fee) => {
    expect(makeAccount('Checking', balance).processMonthlyFee('2026-10-01').feeCharged).toBe(fee);
  });
});

describe('Boundary 7: balance versus the $10 Checking fee (BV35-BV37)', () => {
  test('BV35: $9.99 cannot pay the fee -> Suspended, nothing charged', () => {
    const account = makeAccount('Checking', 9.99);
    const result = account.processMonthlyFee('2026-10-01');
    expect(result.suspended).toBe(true);
    expect(account.state).toBe('Suspended');
    expect(account.balance).toBe(9.99);
    expect(account.unpaidFees).toBe(10);
  });

  test('BV36: $10.00 pays the fee exactly and stays Active', () => {
    const account = makeAccount('Checking', 10);
    expect(account.processMonthlyFee('2026-10-01').feeCharged).toBe(10);
    expect(account.balance).toBe(0);
    expect(account.state).toBe('Active');
  });

  test('BV37: $10.01 pays the fee and keeps one cent', () => {
    const account = makeAccount('Checking', 10.01);
    account.processMonthlyFee('2026-10-01');
    expect(account.balance).toBe(0.01);
    expect(account.state).toBe('Active');
  });
});

describe('Boundary 8: fee processing day (BV38-BV42)', () => {
  test.each([
    ['2026-09-30', false],
    ['2026-10-01', true],
    ['2026-10-02', false],
    ['2026-02-28', false],
    ['2026-03-01', true],
  ])('BV38-BV42: fees on %s charged=%p', (day, charged) => {
    const account = makeAccount('Checking', 1000);
    expect(account.processMonthlyFee(day).success).toBe(charged);
    expect(account.balance === 990).toBe(charged);
  });
});

describe('Boundary 9: opening balance minimums (BV43-BV48)', () => {
  test.each([
    ['Savings', 99.99, false],
    ['Savings', 100.0, true],
    ['Savings', 100.01, true],
    ['Premium', 9999.99, false],
    ['Premium', 10000.0, true],
    ['Premium', 10000.01, true],
  ])('BV43-BV48: %s opening with %p valid=%p', (type, balance, valid) => {
    if (valid) {
      expect(new BankAccount(type, balance).state).toBe('Active');
    } else {
      expect(() => new BankAccount(type, balance)).toThrow();
    }
  });
});

describe('Boundary 10: amount precision (BV49-BV52)', () => {
  test.each([
    [0.001, false],
    [0.01, true],
    [0.011, false],
    [0.1, true],
  ])('BV49-BV52: amount %p valid=%p', (amount, valid) => {
    expect(makeChecking().transfer(amount).success).toBe(valid);
  });
});

describe('Boundary 11: history date range limits (BV53-BV56)', () => {
  const accountWithDeposits = () => {
    const account = makeAccount('Checking', 1000);
    ['2026-09-09', '2026-09-10', '2026-09-20', '2026-09-21'].forEach((day) => account.deposit(1, { onDate: day }));
    return account;
  };
  const days = () => accountWithDeposits().getHistory('2026-09-10', '2026-09-20').map((tx) => tx.date);

  test('BV53: the day before start is excluded', () => expect(days()).not.toContain('2026-09-09'));
  test('BV54: the start day is included', () => expect(days()).toContain('2026-09-10'));
  test('BV55: the end day is included', () => expect(days()).toContain('2026-09-20'));
  test('BV56: the day after end is excluded and a single day range works', () => {
    expect(days()).not.toContain('2026-09-21');
    expect(accountWithDeposits().getHistory('2026-09-20', '2026-09-20')).toHaveLength(1);
  });
});

describe('Boundary 12: payment date around today (BV57-BV59)', () => {
  test.each([
    ['2026-09-14', 'rejected'],
    ['2026-09-15', 'paid'],
    ['2026-09-16', 'scheduled'],
  ])('BV57-BV59: payment dated %s is %s', (paymentDate, outcome) => {
    const account = makeChecking();
    const result = account.payBill('Visa Credit Card', 100, { paymentDate, onDate: TODAY });
    if (outcome === 'rejected') {
      expect(result.success).toBe(false);
    } else {
      expect(result.success).toBe(true);
      expect(result.scheduled).toBe(outcome === 'scheduled');
      expect(account.balance).toBe(outcome === 'scheduled' ? 10000 : 9900);
    }
  });
});
