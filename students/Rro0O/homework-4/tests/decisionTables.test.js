/** Decision table tests (design: design/test-design-document.md, section 3). */
const { BankAccount } = require('../src/bankingSystem');
const { TODAY, makeAccount, makeChecking } = require('../jest.setup');

/**
 * Build an account and amount that produce the requested condition combination.
 * Checking $1,000: $500 fits balance and limit; $6,000 exceeds both; $2,000 exceeds only the balance.
 */
function accountForTransfer(fundsOk, limitOk, operable) {
  let account = makeAccount('Checking', 1000);
  let amount;
  if (fundsOk && limitOk) {
    amount = 500;
  } else if (fundsOk) {
    account = makeAccount('Checking', 20000);
    amount = 6000;
  } else if (limitOk) {
    amount = 2000;
  } else {
    amount = 6000;
  }
  if (!operable) account.freeze();
  return { account, amount };
}

describe('Decision table 1: transfer validation', () => {
  test.each([
    ['R1', true, true, true, []],
    ['R2', true, true, false, ['Account is frozen']],
    ['R3', true, false, true, ['Exceeds daily limit']],
    ['R4', true, false, false, ['Account is frozen']],
    ['R5', false, true, true, ['Insufficient funds']],
    ['R6', false, true, false, ['Account is frozen']],
    ['R7', false, false, true, ['Exceeds daily limit', 'Insufficient funds']],
    ['R8', false, false, false, ['Account is frozen']],
  ])('DT1-%s: funds=%p limit=%p operable=%p', (_rule, fundsOk, limitOk, operable, expectedErrors) => {
    const { account, amount } = accountForTransfer(fundsOk, limitOk, operable);
    const before = account.balance;
    const result = account.transfer(amount);
    expect(result.errors).toEqual(expectedErrors);
    expect(result.success).toBe(expectedErrors.length === 0);
    expect(account.balance).toBe(expectedErrors.length === 0 ? before - amount : before);
  });

  test('DT1-R9: a Closed account reports a different message', () => {
    const account = makeChecking();
    account.close();
    expect(account.transfer(100).errors).toEqual(['Account is closed']);
  });

  test('DT1-R10: a destination that cannot receive blocks the transfer', () => {
    const source = makeAccount('Checking', 1000);
    const target = makeAccount('Savings', 500);
    target.close();
    const result = source.transfer(100, { destination: target });
    expect(result.errors).toEqual(['Destination account cannot receive funds']);
    expect(source.balance).toBe(1000);
  });

  test('DT1-R11: transfer between own accounts moves money', () => {
    const source = makeAccount('Checking', 1000);
    const target = makeAccount('Savings', 500);
    expect(source.transfer(250, { destination: target }).success).toBe(true);
    expect([source.balance, target.balance]).toEqual([750, 750]);
  });

  test('DT1-R13: a Suspended destination can receive money and is reactivated', () => {
    const source = makeAccount('Checking', 1000);
    const target = makeAccount('Savings', 150);
    target.transfer(60);
    expect(target.state).toBe('Suspended');
    expect(source.transfer(50, { destination: target }).success).toBe(true);
    expect([target.balance, target.state]).toEqual([140, 'Active']);
  });

  test('DT1-R12: transfer to the same account is rejected', () => {
    const account = makeChecking();
    expect(account.transfer(10, { destination: account }).error).toBe('Cannot transfer to the same account');
  });
});

describe('Decision table 2: monthly fee processing', () => {
  const FEE_DAY = '2026-10-01';

  test('DT2-R1: Savings above the threshold is waived', () => {
    const account = makeAccount('Savings', 1500);
    const result = account.processMonthlyFee(FEE_DAY);
    expect([result.waived, result.feeCharged, account.balance]).toEqual([true, 0, 1500]);
  });

  test('DT2-R2: Savings below the threshold is charged', () => {
    const account = makeAccount('Savings', 500);
    expect(account.processMonthlyFee(FEE_DAY).feeCharged).toBe(5);
    expect([account.balance, account.state]).toEqual([495, 'Active']);
  });

  test('DT2-R3: the fee pushes Savings below the minimum -> Suspended', () => {
    const account = makeAccount('Savings', 102);
    expect(account.processMonthlyFee(FEE_DAY).feeCharged).toBe(5);
    expect([account.balance, account.state]).toEqual([97, 'Suspended']);
  });

  test('DT2-R4: Checking above the threshold is waived', () => {
    const account = makeAccount('Checking', 8000);
    expect(account.processMonthlyFee(FEE_DAY).waived).toBe(true);
    expect(account.balance).toBe(8000);
  });

  test('DT2-R5: Checking below the threshold is charged', () => {
    const account = makeAccount('Checking', 2000);
    account.processMonthlyFee(FEE_DAY);
    expect(account.balance).toBe(1990);
  });

  test('DT2-R6: Checking that cannot afford the fee is suspended', () => {
    const account = makeAccount('Checking', 5);
    expect(account.processMonthlyFee(FEE_DAY).suspended).toBe(true);
    expect([account.state, account.balance, account.unpaidFees]).toEqual(['Suspended', 5, 10]);
  });

  test.each([10000, 250000])('DT2-R7: Premium never pays a fee (balance %p)', (balance) => {
    const account = makeAccount('Premium', balance);
    expect(account.processMonthlyFee(FEE_DAY).feeCharged).toBe(0);
    expect(account.balance).toBe(balance);
  });

  test('DT2-R8: not the first of the month -> nothing happens', () => {
    const account = makeAccount('Checking', 100);
    expect(account.processMonthlyFee('2026-10-15').success).toBe(false);
    expect(account.balance).toBe(100);
  });

  test.each(['freeze', 'close'])('DT2-R9: %s accounts are skipped', (action) => {
    const account = makeAccount('Checking', 100);
    account[action]();
    expect(account.processMonthlyFee(FEE_DAY).success).toBe(false);
    expect(account.balance).toBe(100);
  });

  test('DT2-R11: a Suspended account still pays the fee', () => {
    const account = makeAccount('Savings', 150);
    account.transfer(60);
    expect(account.processMonthlyFee(FEE_DAY).feeCharged).toBe(5);
    expect([account.balance, account.state]).toEqual([85, 'Suspended']);
  });

  test('DT2-R10: an invalid date cannot trigger fees', () => {
    expect(makeChecking().processMonthlyFee('first of october').error).toBe('Invalid date');
  });
});

describe('Decision table 3: bill payment validation', () => {
  test('DT3-R1: all valid, today -> paid now', () => {
    const account = makeChecking();
    const result = account.payBill('SIAPA Water', 300, { onDate: TODAY });
    expect([result.success, result.scheduled, account.balance]).toEqual([true, false, 9700]);
    expect(account.transactions[account.transactions.length - 1].type).toBe('bill payment');
  });

  test('DT3-R2: all valid, future date -> scheduled', () => {
    const account = makeChecking();
    const result = account.payBill('SIAPA Water', 300, { paymentDate: '2026-12-31', onDate: TODAY });
    expect([result.scheduled, account.balance, account.scheduledPayments.length]).toEqual([true, 10000, 1]);
  });

  test('DT3-R3: invalid payee', () => {
    expect(makeChecking().payBill('Nobody', 300, { onDate: TODAY }).errors).toEqual(['Invalid payee']);
  });

  test('DT3-R4: amount not positive', () => {
    expect(makeChecking().payBill('SIAPA Water', 0, { onDate: TODAY }).errors).toEqual(['Amount must be positive']);
  });

  test('DT3-R5: insufficient funds', () => {
    const account = makeAccount('Checking', 100);
    expect(account.payBill('SIAPA Water', 300, { onDate: TODAY }).errors).toEqual(['Insufficient funds']);
    expect(account.balance).toBe(100);
  });

  test('DT3-R6: past date', () => {
    const result = makeChecking().payBill('SIAPA Water', 300, { paymentDate: '2026-01-01', onDate: TODAY });
    expect(result.errors).toEqual(['Payment date cannot be in the past']);
  });

  test('DT3-R7: Frozen account blocks everything', () => {
    const account = makeChecking();
    account.freeze();
    expect(account.payBill('Nobody', -5, { onDate: TODAY }).errors).toEqual(['Account is frozen']);
  });

  test('DT3-R8: multiple failures are all reported', () => {
    const result = makeChecking().payBill('Nobody', -5, { paymentDate: '2020-01-01', onDate: TODAY });
    expect(result.errors).toEqual(['Invalid payee', 'Amount must be positive', 'Payment date cannot be in the past']);
  });

  test('DT3-R9: a payment that drops below the minimum suspends the account', () => {
    const account = makeAccount('Savings', 150);
    const result = account.payBill('Telmex Internet', 60, { onDate: TODAY });
    expect(result.success).toBe(true);
    expect(account.state).toBe('Suspended');
    expect(result.warning).toContain('suspended');
  });

  test('DT3-R10: invalid date and unpayable amount types are reported', () => {
    const result = makeChecking().payBill('SIAPA Water', 'lots', { paymentDate: 'someday', onDate: TODAY });
    expect(result.errors).toEqual(['Amount must be a number', 'Invalid payment date']);
  });
});

describe('Decision table 4: account creation and information', () => {
  test('DT4-R1: all conditions true creates an Active account', () => {
    const account = new BankAccount('Premium', 12000, '  Ana Perez ');
    expect([account.state, account.owner, account.getMinimumBalance()]).toEqual(['Active', 'Ana Perez', 10000]);
  });

  test('DT4-R2: invalid type', () => {
    expect(() => new BankAccount('Platinum', 50000)).toThrow('Invalid account type');
  });

  test('DT4-R3: balance below the minimum', () => {
    expect(() => new BankAccount('Premium', 9000)).toThrow('below the Premium minimum');
  });

  test.each(['', '   ', null])('DT4-R4: missing owner %p', (owner) => {
    expect(() => new BankAccount('Checking', 100, owner)).toThrow('Owner name is required');
  });

  test('DT4-R5: account information is validated and updated', () => {
    const account = makeChecking();
    expect(account.updateInfo({ owner: 'New Name', email: 'a@b.com' }).success).toBe(true);
    expect([account.owner, account.email]).toEqual(['New Name', 'a@b.com']);
    expect(account.updateInfo({ owner: ' ', email: 'not-an-email' }).errors).toEqual([
      'Owner name is required',
      'Invalid e-mail address',
    ]);
  });

  test('DT4-R6: a partial update changes only the given field', () => {
    const account = makeChecking();
    account.updateInfo({ email: 'a@b.com' });
    account.updateInfo({ owner: 'Only Name' });
    expect([account.owner, account.email]).toEqual(['Only Name', 'a@b.com']);
  });
});
