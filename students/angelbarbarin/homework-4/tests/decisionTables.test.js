'use strict';

/** Tablas de Decisión (DT) - espejo de test_decision_tables.py */
const { BankAccount } = require('../src/bankingSystem');
const { createClock, accountFactory } = require('./helpers/fakeClock');

const FIRST_OF_MONTH = new Date(2026, 9, 1);
let clock;
let makeAccount;

beforeEach(() => {
  clock = createClock();
  makeAccount = accountFactory(clock);
});

function putInState(account, state) {
  if (state === 'Frozen') account.freeze();
  if (state === 'Closed') account.close();
  return account;
}

describe('DT1: transfer validation', () => {
  test.each([
    ['DT1-R1', 'Active', 1000, 500, null],
    ['DT1-R2', 'Active', 1000, 2000, 'Insufficient funds'],
    ['DT1-R3', 'Active', 20000, 6000, 'Exceeds daily limit'],
    ['DT1-R4', 'Active', 1000, 6000, 'Exceeds daily limit'],
    ['DT1-R5', 'Frozen', 1000, 500, 'Account is frozen'],
    ['DT1-R6', 'Frozen', 1000, 2000, 'Account is frozen'],
    ['DT1-R7', 'Frozen', 20000, 6000, 'Account is frozen'],
    ['DT1-R8', 'Frozen', 1000, 6000, 'Account is frozen'],
    ['DT1-R9', 'Closed', 1000, 500, 'Account is closed'],
    ['DT1-R10', 'Active', 1000, -5, 'Amount must be positive'],
  ])('%s: %s, balance %p, amount %p -> %p', (_id, state, balance, amount, error) => {
    const result = putInState(makeAccount('Checking', balance), state).transfer(amount);
    expect(result.success).toBe(error === null);
    expect(result.error).toBe(error);
  });

  test('DT1-R11: Suspended account with funds can transfer and stays Suspended', () => {
    const account = makeAccount('Savings', 200);
    account.transfer(150);
    const result = account.transfer(20);
    expect(result.success).toBe(true);
    expect(result.state).toBe('Suspended');
  });

  test('DT1-R12: frozen destination is rejected and no money moves', () => {
    const source = makeAccount('Checking', 1000);
    const target = putInState(makeAccount('Checking', 1000), 'Frozen');
    expect(source.transfer(300, target).error).toBe('Destination account unavailable');
    expect([source.balance, target.balance]).toEqual([1000, 1000]);
  });

  test('DT1-R13: transfer to the same account is rejected', () => {
    const account = makeAccount('Checking', 1000);
    expect(account.transfer(300, account).error).toBe('Cannot transfer to the same account');
  });

  test('DT1-R14: active destination is credited', () => {
    const source = makeAccount('Checking', 1000);
    const target = makeAccount('Savings', 500);
    expect(source.transfer(300, target).success).toBe(true);
    expect([source.balance, target.balance]).toEqual([700, 800]);
  });
});

describe('DT2: monthly fee processing', () => {
  test('DT2-R1: closed account is not charged', () => {
    const account = putInState(makeAccount('Checking', 3000), 'Closed');
    expect(account.processMonthlyFee(FIRST_OF_MONTH).error).toBe('Account is closed');
    expect(account.balance).toBe(3000);
  });

  test('DT2-R2: a date other than the 1st is rejected (uses the clock date)', () => {
    expect(makeAccount('Checking', 3000).processMonthlyFee().error)
      .toBe('Fees are only charged on the 1st of the month');
  });

  test.each([
    ['DT2-R3', 'Premium', 20000, [0, false, 'Active']],
    ['DT2-R4', 'Savings', 1500, [0, true, 'Active']],
    ['DT2-R5', 'Savings', 800, [5, false, 'Active']],
    ['DT2-R6', 'Savings', 102, [5, false, 'Suspended']],
    ['DT2-R7', 'Checking', 6000, [0, true, 'Active']],
    ['DT2-R8', 'Checking', 3000, [10, false, 'Active']],
  ])('%s: %s with %p -> [fee, waived, state] = %p', (_id, type, balance, expected) => {
    const account = makeAccount(type, balance);
    const result = account.processMonthlyFee(FIRST_OF_MONTH);
    expect([result.feeCharged, result.waived, account.state]).toEqual(expected);
  });

  test('DT2-R9: insufficient funds on an active account suspends it without charging', () => {
    const account = makeAccount('Checking', 5);
    expect(account.processMonthlyFee(FIRST_OF_MONTH)).toEqual({
      success: false, error: 'Insufficient funds for monthly fee', state: 'Suspended',
    });
    expect(account.balance).toBe(5);
  });

  test('DT2-R10: insufficient funds on a frozen account keeps it Frozen', () => {
    const account = putInState(makeAccount('Checking', 5), 'Frozen');
    expect(account.processMonthlyFee(FIRST_OF_MONTH).state).toBe('Frozen');
  });
});

describe('DT3: bill payment', () => {
  test.each([
    ['DT3-R1', 'Active', ['UTIL-ELECTRIC', 200, null], 'paid'],
    ['DT3-R2', 'Active', ['UTIL-ELECTRIC', 5000, null], 'Insufficient funds'],
    ['DT3-R3', 'Active', ['UTIL-ELECTRIC', 5000, new Date(2026, 8, 30)], 'scheduled'],
    ['DT3-R4', 'Active', ['UTIL-ELECTRIC', 200, new Date(2026, 8, 13)], 'Scheduled date cannot be in the past'],
    ['DT3-R5', 'Active', ['UTIL-ELECTRIC', 0, null], 'Amount must be positive'],
    ['DT3-R6', 'Active', ['UTIL-GAS', 200, null], 'Unknown payee'],
    ['DT3-R7', 'Frozen', ['UTIL-ELECTRIC', 200, null], 'Account is frozen'],
    ['DT3-R8', 'Closed', ['UTIL-ELECTRIC', 200, null], 'Account is closed'],
    ['DT3-R9', 'Active', ['UTIL-ELECTRIC', 200, new Date(2026, 8, 14)], 'paid'],
  ])('%s: %s account paying %p -> %p', (_id, state, payment, expected) => {
    const [payee, amount, when] = payment;
    const result = putInState(makeAccount('Checking', 1000), state).payBill(payee, amount, when);
    expect(result.success ? result.status : result.error).toBe(expected);
  });

  test('DT3-R10: payment leaving Savings below $100 is paid and suspends', () => {
    const result = makeAccount('Savings', 150).payBill('CC-VISA', 100);
    expect([result.status, result.state]).toEqual(['paid', 'Suspended']);
  });
});

describe('DT4: account creation', () => {
  test.each([
    ['DT4-R1', 'Savings', 100, null],
    ['DT4-R2', 'Premium', 9000, 'below minimum'],
    ['DT4-R3', 'Gold', 50000, 'Invalid account type'],
    ['DT4-R4', 'Checking', 'mil', 'must be a number'],
  ])('%s: open %s with %p -> error %p', (_id, type, balance, message) => {
    if (message === null) {
      expect(new BankAccount(type, balance, clock).balance).toBe(balance);
    } else {
      expect(() => new BankAccount(type, balance, clock)).toThrow(message);
    }
  });
});
