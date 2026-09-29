/** State transition tests (design: design/test-design-document.md, section 4). */
const { TODAY, makeAccount, makeChecking } = require('../jest.setup');

/** Savings $150 that has been pushed to Suspended ($90). */
const suspendedSavings = () => {
  const account = makeAccount('Savings', 150);
  account.transfer(60);
  return account;
};

describe('Valid transitions (ST1-ST13)', () => {
  test('ST1: Active -> Suspended by a transfer, with warning', () => {
    const account = makeAccount('Savings', 150);
    const result = account.transfer(60);
    expect(account.state).toBe('Suspended');
    expect(result.warning).toContain('suspended');
  });

  test('ST2: Suspended -> Active by a deposit that restores the minimum', () => {
    const account = suspendedSavings();
    const result = account.deposit(500);
    expect([account.state, account.balance, result.success]).toEqual(['Active', 590, true]);
  });

  test('ST3: Suspended stays Suspended when the deposit is not enough', () => {
    const account = suspendedSavings();
    account.deposit(5);
    expect([account.state, account.balance]).toEqual(['Suspended', 95]);
  });

  test('ST4: a deposit reaching exactly the minimum reactivates the account', () => {
    const account = suspendedSavings();
    account.deposit(10);
    expect(account.state).toBe('Active');
  });

  test('ST5: Active -> Frozen', () => {
    const account = makeChecking();
    expect(account.freeze('fraud detection').state).toBe('Frozen');
    expect(account.state).toBe('Frozen');
  });

  test('ST6: Frozen -> Active and transfers work again', () => {
    const account = makeChecking();
    account.freeze();
    account.unfreeze();
    expect(account.state).toBe('Active');
    expect(account.transfer(10).success).toBe(true);
  });

  test.each(['active', 'suspended', 'frozen'])('ST7-ST9: %s -> Closed with a final statement', (start) => {
    const account = makeAccount('Savings', 150);
    if (start === 'suspended') account.transfer(60);
    if (start === 'frozen') account.freeze();
    const result = account.close();
    expect(account.state).toBe('Closed');
    expect(result.finalStatement.finalBalance).toBe(account.balance);
  });

  test('ST10: a bill payment that breaks the minimum also suspends the account', () => {
    const account = makeAccount('Savings', 150);
    account.payBill('CFE Electricity', 100, { onDate: TODAY });
    expect(account.state).toBe('Suspended');
  });

  test('ST11: a monthly fee that cannot be paid suspends the account', () => {
    const account = makeAccount('Checking', 5);
    account.processMonthlyFee('2026-10-01');
    expect(account.state).toBe('Suspended');
  });

  test('ST12: Active stays Active while the balance stays above the minimum', () => {
    const account = makeAccount('Savings', 500);
    account.transfer(100);
    expect(account.state).toBe('Active');
  });

  test('ST13: a Frozen account can still be viewed', () => {
    const account = makeChecking();
    account.freeze();
    expect(account.getBalance()).toBe(10000);
  });
});

describe('Invalid transitions (ST14-ST21)', () => {
  test('ST14: Frozen + transfer -> error, still Frozen', () => {
    const account = makeChecking();
    account.freeze();
    expect(account.transfer(10).success).toBe(false);
    expect(account.state).toBe('Frozen');
  });

  test('ST15: Frozen + deposit is blocked', () => {
    const account = makeChecking();
    account.freeze();
    expect(account.deposit(10).error).toBe('Account is frozen');
    expect(account.balance).toBe(10000);
  });

  test('ST16: an Active account cannot be unfrozen', () => {
    const account = makeChecking();
    expect(account.unfreeze().success).toBe(false);
    expect(account.state).toBe('Active');
  });

  test('ST17: a Suspended account cannot be frozen', () => {
    const account = suspendedSavings();
    expect(account.freeze().success).toBe(false);
    expect(account.state).toBe('Suspended');
  });

  test('ST18: a Frozen account cannot be frozen again', () => {
    const account = makeChecking();
    account.freeze();
    expect(account.freeze().success).toBe(false);
  });

  test.each([
    ['transfer', (acc) => acc.transfer(10)],
    ['deposit', (acc) => acc.deposit(10)],
    ['payBill', (acc) => acc.payBill('CFE Electricity', 10)],
    ['freeze', (acc) => acc.freeze()],
    ['unfreeze', (acc) => acc.unfreeze()],
    ['close', (acc) => acc.close()],
    ['reopen', (acc) => acc.reopen()],
    ['updateInfo', (acc) => acc.updateInfo({ owner: 'Someone' })],
    ['processMonthlyFee', (acc) => acc.processMonthlyFee('2026-10-01')],
  ])('ST19: Closed absorbs the event %s', (_name, event) => {
    const account = makeChecking();
    account.close();
    const result = event(account);
    expect(result.success).toBe(false);
    expect(account.state).toBe('Closed');
    expect(account.balance).toBe(10000);
  });

  test('ST20: reopen on an open account is also rejected', () => {
    expect(makeChecking().reopen().error).toBe('Account is not closed');
  });

  test('ST21: full lifecycle Active -> Suspended -> Active -> Frozen -> Active -> Closed', () => {
    const account = makeAccount('Savings', 150);
    const visited = [account.state];
    [
      () => account.transfer(60),
      () => account.deposit(200),
      () => account.freeze(),
      () => account.unfreeze(),
      () => account.close(),
    ].forEach((step) => {
      step();
      visited.push(account.state);
    });
    expect(visited).toEqual(['Active', 'Suspended', 'Active', 'Frozen', 'Active', 'Closed']);
  });
});

describe('History and information (ST22-ST25)', () => {
  test('ST22: every movement leaves a history entry', () => {
    const account = makeAccount('Checking', 1000);
    account.transfer(100, { onDate: TODAY });
    account.deposit(50, { onDate: TODAY });
    account.payBill('CFE Electricity', 25, { onDate: TODAY });
    account.processMonthlyFee('2026-10-01');
    expect(account.getHistory().map((tx) => tx.type)).toEqual(['transfer', 'deposit', 'bill payment', 'fee']);
  });

  test('ST23: CSV export has a header and one line per filtered transaction', () => {
    const account = makeAccount('Checking', 1000);
    account.deposit(50, { onDate: '2026-09-10' });
    account.deposit(70, { onDate: '2026-09-30' });
    const lines = account.exportCsv('2026-09-01', '2026-09-15').trim().split('\n');
    expect(lines[0]).toBe('date,type,amount,balance_after,description');
    expect(lines[1]).toBe('2026-09-10,deposit,50.00,1050.00,Deposit');
    expect(lines).toHaveLength(2);
  });

  test('ST23b: CSV fields containing commas are quoted', () => {
    const account = makeAccount('Checking', 1000, 'Perez, Ana');
    const target = makeAccount('Savings', 500, 'Luis "Lucho" Diaz, Jr.');
    account.transfer(10, { destination: target, onDate: '2026-09-10' });
    expect(target.exportCsv()).toContain('"Transfer from Perez, Ana"');
    expect(account.exportCsv()).toContain('"Transfer to Luis ""Lucho"" Diaz, Jr."');
  });

  test('ST24: a closed account keeps its history and balance visible', () => {
    const account = makeChecking();
    account.deposit(5);
    account.close();
    expect(account.getBalance()).toBe(10005);
    expect(account.getHistory()).toHaveLength(1);
  });

  test('ST25: updating personal data is allowed while Frozen', () => {
    const account = makeChecking();
    account.freeze();
    expect(account.updateInfo({ email: 'me@example.com' }).success).toBe(true);
  });
});
