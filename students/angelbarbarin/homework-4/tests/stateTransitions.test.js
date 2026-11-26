'use strict';

/** Transición de Estados (ST) - espejo de test_state_transitions.py */
const { createClock, accountFactory } = require('./helpers/fakeClock');

const FIRST_OF_MONTH = new Date(2026, 9, 1);
let makeAccount;

beforeEach(() => {
  makeAccount = accountFactory(createClock());
});

describe('Valid transitions', () => {
  test('ST1: Active -> Suspended when a transfer leaves the balance below $100', () => {
    const account = makeAccount('Savings', 500);
    account.transfer(450);
    expect(account.state).toBe('Suspended');
    expect(account.notifications).toContain('Warning: balance below minimum');
  });

  test('ST2: Active -> Frozen on request', () => {
    const account = makeAccount();
    expect(account.freeze('fraud detection').success).toBe(true);
    expect(account.state).toBe('Frozen');
    expect(account.notifications).toContain('Account frozen: fraud detection');
  });

  test('ST3: Active -> Closed with a final statement', () => {
    const account = makeAccount('Checking', 750);
    account.deposit(50);
    const result = account.close();
    expect(account.state).toBe('Closed');
    expect(result.finalStatement).toEqual({ finalBalance: 800, transactions: 1 });
  });

  test('ST4: Suspended -> Active when a deposit restores the minimum', () => {
    const account = makeAccount('Savings', 500);
    account.transfer(450);
    expect(account.deposit(500).state).toBe('Active');
    expect(account.balance).toBe(550);
    expect(account.notifications).toContain('Account reactivated: minimum balance restored');
  });

  test('ST5: Suspended stays Suspended after a small deposit', () => {
    const account = makeAccount('Savings', 500);
    account.transfer(450);
    account.deposit(20);
    expect(account.state).toBe('Suspended');
  });

  test('ST6: Suspended -> Closed', () => {
    const account = makeAccount('Savings', 500);
    account.transfer(450);
    expect(account.close().state).toBe('Closed');
  });

  test('ST7: Frozen -> Active on unfreeze with balance at or above minimum', () => {
    const account = makeAccount('Savings', 500);
    account.freeze();
    expect(account.unfreeze().state).toBe('Active');
  });

  test('ST8: Frozen -> Suspended on unfreeze with balance below minimum', () => {
    const account = makeAccount('Savings', 102);
    account.freeze();
    account.processMonthlyFee(FIRST_OF_MONTH);
    expect(account.state).toBe('Frozen');
    expect(account.unfreeze().state).toBe('Suspended');
  });

  test('ST9: Frozen -> Closed', () => {
    const account = makeAccount();
    account.freeze();
    expect(account.close().state).toBe('Closed');
  });

  test('ST10: Active -> Suspended when the monthly fee cannot be paid', () => {
    const account = makeAccount('Checking', 3);
    account.processMonthlyFee(FIRST_OF_MONTH);
    expect(account.state).toBe('Suspended');
  });
});

describe('Invalid transitions', () => {
  test.each([
    ['transfer', [50]], ['deposit', [50]], ['payBill', ['UTIL-WATER', 50]],
  ])('ST11: Frozen rejects %s', (operation, args) => {
    const account = makeAccount('Checking', 1000);
    account.freeze();
    expect(account[operation](...args).error).toBe('Account is frozen');
    expect([account.state, account.balance]).toEqual(['Frozen', 1000]);
  });

  test.each([
    ['transfer', [50], 'Account is closed'],
    ['deposit', [50], 'Account is closed'],
    ['freeze', [], 'Cannot freeze an account in state Closed'],
    ['unfreeze', [], 'Account is not frozen'],
    ['close', [], 'Account is already closed'],
  ])('ST12: Closed is final - %s is rejected', (operation, args, error) => {
    const account = makeAccount('Checking', 1000);
    account.close();
    expect(account[operation](...args).error).toBe(error);
    expect(account.state).toBe('Closed');
  });

  test('ST13: Suspended cannot be frozen', () => {
    const account = makeAccount('Savings', 500);
    account.transfer(450);
    expect(account.freeze().error).toBe('Cannot freeze an account in state Suspended');
    expect(account.state).toBe('Suspended');
  });

  test('ST14: Active cannot be unfrozen', () => {
    const account = makeAccount();
    expect(account.unfreeze().error).toBe('Account is not frozen');
    expect(account.state).toBe('Active');
  });

  test('ST18: unfreezing a Suspended account or freezing a Frozen one is rejected', () => {
    const suspended = makeAccount('Savings', 500);
    suspended.transfer(450);
    expect(suspended.unfreeze().error).toBe('Account is not frozen');
    const frozen = makeAccount();
    frozen.freeze();
    expect(frozen.freeze().error).toBe('Cannot freeze an account in state Frozen');
    expect([suspended.state, frozen.state]).toEqual(['Suspended', 'Frozen']);
  });

  test('ST15: balance stays viewable in Frozen and Closed', () => {
    const account = makeAccount('Checking', 640);
    account.freeze();
    const frozenView = account.balance;
    account.close();
    expect([frozenView, account.balance]).toEqual([640, 640]);
  });
});

describe('Full sequences', () => {
  test('ST16: Active -> Suspended -> Active -> Frozen -> Active -> Closed', () => {
    const account = makeAccount('Savings', 500);
    const visited = [account.state];
    account.transfer(450);
    visited.push(account.state);
    account.deposit(300);
    visited.push(account.state);
    account.freeze();
    visited.push(account.state);
    account.unfreeze();
    visited.push(account.state);
    account.close();
    visited.push(account.state);
    expect(visited).toEqual(['Active', 'Suspended', 'Active', 'Frozen', 'Active', 'Closed']);
  });

  test('ST17: the suspension rule is re-applied on every cycle', () => {
    const account = makeAccount('Savings', 300);
    account.transfer(250);
    account.deposit(100);
    account.transfer(100);
    expect(account.state).toBe('Suspended');
  });
});
