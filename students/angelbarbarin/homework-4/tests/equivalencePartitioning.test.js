'use strict';

/** Particiones de Equivalencia (EP) - espejo de test_equivalence_partitioning.py */
const { BankAccount } = require('../src/bankingSystem');
const { createClock, accountFactory } = require('./helpers/fakeClock');

let clock;
let makeAccount;

beforeEach(() => {
  clock = createClock();
  makeAccount = accountFactory(clock);
});

describe('EP - Transfer amount', () => {
  test('EP1: valid amount within limits succeeds', () => {
    const account = makeAccount('Checking', 1000);
    expect(account.transfer(500).success).toBe(true);
    expect(account.balance).toBe(500);
  });

  test.each([[0], [-100]])('EP2/EP3: non-positive amount %p is rejected', (amount) => {
    const account = makeAccount('Checking', 1000);
    expect(account.transfer(amount).error).toContain('must be positive');
    expect(account.balance).toBe(1000);
  });

  test('EP4: amount above daily limit is rejected', () => {
    expect(makeAccount('Checking', 200000).transfer(100000))
      .toEqual({ success: false, error: 'Exceeds daily limit' });
  });

  test('EP5: amount above balance is rejected', () => {
    expect(makeAccount('Checking', 1000).transfer(1500).error).toBe('Insufficient funds');
  });

  test.each([['500'], [null], [true], [NaN]])('EP6: non-numeric amount %p is rejected', (amount) => {
    expect(makeAccount().transfer(amount).error).toBe('Amount must be a number');
  });

  test('EP7: sub-cent amount is rejected', () => {
    expect(makeAccount().transfer(10.005).error).toBe('Amount must have at most 2 decimal places');
  });
});

describe('EP - Deposit amount', () => {
  test.each([
    [250, null, 1250],
    [-250, 'Amount must be positive', 1000],
    ['250', 'Amount must be a number', 1000],
  ])('EP31-EP33: deposit %p -> error %p', (amount, error, balance) => {
    const account = makeAccount('Checking', 1000);
    expect(account.deposit(amount).error).toBe(error);
    expect(account.balance).toBe(balance);
  });
});

describe('EP - Account type and balance', () => {
  test.each([
    ['Savings', 500, 2000],
    ['Checking', 500, 5000],
    ['Premium', 20000, 50000],
  ])('EP8-EP10: %s is created Active with its daily limit', (type, balance, limit) => {
    const account = new BankAccount(type, balance, clock);
    expect(account.state).toBe('Active');
    expect(account.getDailyLimit()).toBe(limit);
  });

  test.each([['Business'], ['savings'], ['']])('EP11/EP12: invalid type %p throws', (type) => {
    expect(() => new BankAccount(type, 1000, clock)).toThrow('Invalid account type');
  });

  test('EP34: without an injected clock the account uses the system time', () => {
    const account = new BankAccount('Checking', 100);
    expect(account.transfer(40).success).toBe(true);
    expect(account.dailyTransferTotal).toBe(40);
  });

  test('EP13: balance at or above minimum keeps the account Active', () => {
    const account = makeAccount('Savings', 5000);
    expect(account.state).toBe('Active');
    expect(account.getMinimumBalance()).toBe(100);
  });

  test.each([['Premium', 5000], ['Savings', -50]])('EP14/EP15: %s opened with %p throws', (type, balance) => {
    expect(() => new BankAccount(type, balance, clock)).toThrow('below minimum');
  });
});

describe('EP - Payee and scheduled date', () => {
  test.each([['UTIL-ELECTRIC'], ['  cc-visa  ']])('EP16/EP20: valid payee %p is paid', (payee) => {
    const account = makeAccount('Checking', 1000);
    expect(account.payBill(payee, 150).status).toBe('paid');
    expect(account.balance).toBe(850);
  });

  test.each([[''], ['   '], [null], [12345]])('EP17/EP18: missing payee %p is rejected', (payee) => {
    expect(makeAccount().payBill(payee, 150).error).toBe('Payee is required');
  });

  test('EP19: unknown payee is rejected', () => {
    expect(makeAccount().payBill('UTIL-GAS', 150).error).toBe('Unknown payee');
  });

  test('EP26: no scheduled date pays immediately', () => {
    expect(makeAccount().payBill('UTIL-WATER', 80).status).toBe('paid');
  });

  test('EP27: future date is scheduled without moving the balance', () => {
    const account = makeAccount('Checking', 1000);
    expect(account.payBill('UTIL-WATER', 80, new Date(2026, 9, 1)).status).toBe('scheduled');
    expect(account.balance).toBe(1000);
    expect(account.scheduledPayments[0].date).toBe('2026-10-01');
  });

  test('EP28: past date is rejected', () => {
    expect(makeAccount().payBill('UTIL-WATER', 80, new Date(2026, 8, 1)).error)
      .toBe('Scheduled date cannot be in the past');
  });

  test('EP29: zero bill amount is rejected', () => {
    expect(makeAccount().payBill('CC-VISA', 0).error).toContain('must be positive');
  });
});

describe('EP - Transaction history date range', () => {
  let account;

  beforeEach(() => {
    account = makeAccount('Checking', 5000);
    for (let i = 0; i < 3; i += 1) {
      account.deposit(100);
      clock.advance({ days: 1 });
    }
  });

  test('EP21: valid range returns only transactions inside it (inclusive)', () => {
    expect(account.getTransactions(new Date(2026, 8, 15), new Date(2026, 8, 16))).toHaveLength(2);
  });

  test('EP22: start after end throws', () => {
    expect(() => account.getTransactions(new Date(2026, 8, 20), new Date(2026, 8, 1)))
      .toThrow('on or before');
  });

  test('EP23: range without transactions returns an empty list', () => {
    expect(account.getTransactions(new Date(2027, 0, 1), new Date(2027, 0, 31))).toHaveLength(0);
  });

  test('EP24: open-ended range returns the whole history', () => {
    expect(account.getTransactions()).toHaveLength(3);
    expect(account.getTransactions(new Date(2026, 8, 16, 8, 0))).toHaveLength(1);
  });

  test('EP25: date given as text throws', () => {
    expect(() => account.getTransactions('2026-09-01')).toThrow('must be a date');
  });

  test('EP30: CSV export has a header and one row per transaction', () => {
    const day = new Date(2026, 8, 14);
    const lines = account.exportTransactionsCsv(day, day).trim().split('\n');
    expect(lines[0]).toBe('timestamp,type,amount,balance_after,description');
    expect(lines[1]).toBe('2026-09-14T10:00:00,deposit,100.00,5100.00,Deposit');
    expect(lines).toHaveLength(2);
    expect(account.exportTransactionsCsv().trim().split('\n')).toHaveLength(4);
  });
});
