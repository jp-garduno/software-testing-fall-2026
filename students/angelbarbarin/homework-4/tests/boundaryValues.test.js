'use strict';

/** Análisis de Valores Límite (BVA) - espejo de test_boundary_values.py */
const { BankAccount } = require('../src/bankingSystem');
const { createClock, accountFactory } = require('./helpers/fakeClock');

const FIRST_OF_MONTH = new Date(2026, 9, 1);
let clock;
let makeAccount;

beforeEach(() => {
  clock = createClock();
  makeAccount = accountFactory(clock);
});

describe('B1-B3: transfer amount vs daily limit', () => {
  test.each([
    ['BV1', 0, false], ['BV2', 0.01, true], ['BV3', 4999.99, true],
    ['BV4', 5000, true], ['BV5', 5000.01, false], ['BV6', 10000, false],
  ])('%s: Checking transfer of %p -> success %p', (_id, amount, succeeds) => {
    expect(makeAccount('Checking', 20000).transfer(amount).success).toBe(succeeds);
  });

  test('BV2: transferring $0.01 leaves exactly $999.99', () => {
    const account = makeAccount('Checking', 1000);
    account.transfer(0.01);
    expect(account.balance).toBe(999.99);
  });

  test('BV4: transferring the exact limit sets the daily total to $5,000', () => {
    const account = makeAccount('Checking', 10000);
    account.transfer(5000);
    expect(account.dailyTransferTotal).toBe(5000);
  });

  test.each([
    ['BV7', 0, false], ['BV8', 0.01, true], ['BV9', 1999.99, true],
    ['BV10', 2000, true], ['BV11', 2000.01, false],
  ])('%s: Savings transfer of %p -> success %p', (_id, amount, succeeds) => {
    expect(makeAccount('Savings', 10000).transfer(amount).success).toBe(succeeds);
  });

  test.each([
    ['BV12', 49999.99, true], ['BV13', 50000, true], ['BV14', 50000.01, false], ['BV15', 75000, false],
  ])('%s: Premium transfer of %p -> success %p', (_id, amount, succeeds) => {
    expect(makeAccount('Premium', 200000).transfer(amount).success).toBe(succeeds);
  });
});

describe('B4-B5: balance boundaries', () => {
  test.each([
    ['BV16', 99.99, 'Active'], ['BV17', 100, 'Active'],
    ['BV18', 100.01, 'Suspended'], ['BV19', 150, 'Suspended'],
  ])('%s: Savings $200 transferring %p ends %s', (_id, amount, state) => {
    const account = makeAccount('Savings', 200);
    account.transfer(amount);
    expect(account.state).toBe(state);
  });

  test('BV20: depositing back to exactly $100.00 reactivates the account', () => {
    const account = makeAccount('Savings', 200);
    account.transfer(100.01);
    expect(account.state).toBe('Suspended');
    account.deposit(0.01);
    expect(account.balance).toBe(100);
    expect(account.state).toBe('Active');
  });

  test.each([
    ['BV21', 999.99, true], ['BV22', 1000, true], ['BV23', 1000.01, false], ['BV24', 1500, false],
  ])('%s: transfer of %p against a $1,000 balance -> success %p', (_id, amount, succeeds) => {
    expect(makeAccount('Checking', 1000).transfer(amount).success).toBe(succeeds);
  });
});

describe('B6: cumulative daily limit and midnight reset', () => {
  test.each([
    ['BV25', 499.99, true], ['BV26', 500, true], ['BV27', 500.01, false], ['BV28', 800, false],
  ])('%s: second transfer of %p after $1,500 -> success %p', (_id, second, succeeds) => {
    const account = makeAccount('Savings', 10000);
    account.transfer(1500);
    expect(account.transfer(second).success).toBe(succeeds);
  });

  test('BV29: at 23:59:59 the same-day total still applies', () => {
    const account = makeAccount('Savings', 10000);
    account.transfer(2000);
    clock.advance({ hours: 13, minutes: 59, seconds: 59 });
    expect(account.transfer(1).error).toBe('Exceeds daily limit');
  });

  test('BV30: at 00:00:00 the next day the total resets', () => {
    const account = makeAccount('Savings', 10000);
    account.transfer(2000);
    clock.advance({ hours: 14 });
    expect(account.dailyTransferTotal).toBe(0);
    expect(account.transfer(2000).success).toBe(true);
  });
});

describe('B7-B8: monthly fee boundaries', () => {
  test.each([
    ['BV31', 'Savings', 999.99, 5], ['BV32', 'Savings', 1000, 5], ['BV33', 'Savings', 1000.01, 0],
    ['BV34', 'Checking', 5000, 10], ['BV35', 'Checking', 5000.01, 0],
  ])('%s: %s with %p pays a fee of %p', (_id, type, balance, fee) => {
    expect(makeAccount(type, balance).processMonthlyFee(FIRST_OF_MONTH).feeCharged).toBe(fee);
  });

  test.each([
    ['BV36', 10.01, true, 'Active'], ['BV37', 10, true, 'Active'], ['BV38', 9.99, false, 'Suspended'],
  ])('%s: Checking with %p -> charged %p, state %s', (_id, balance, succeeds, state) => {
    const account = makeAccount('Checking', balance);
    expect(account.processMonthlyFee(FIRST_OF_MONTH).success).toBe(succeeds);
    expect(account.state).toBe(state);
  });
});

describe('B9-B10: opening balance and precision', () => {
  test.each([
    ['BV39', 'Premium', 9999.99, false], ['BV40', 'Premium', 10000, true],
    ['BV41', 'Premium', 10000.01, true], ['BV42', 'Savings', 99.99, false],
    ['BV43', 'Savings', 100, true], ['BV44', 'Checking', 0, true],
  ])('%s: open %s with %p -> created %p', (_id, type, balance, created) => {
    if (created) {
      expect(new BankAccount(type, balance, clock).state).toBe('Active');
    } else {
      expect(() => new BankAccount(type, balance, clock)).toThrow();
    }
  });

  test.each([
    ['BV45', 0.01, true], ['BV46', 0.001, false], ['BV47', 0.009, false], ['BV48', 1.1, true],
  ])('%s: transfer of %p -> success %p', (_id, amount, succeeds) => {
    expect(makeAccount().transfer(amount).success).toBe(succeeds);
  });
});
