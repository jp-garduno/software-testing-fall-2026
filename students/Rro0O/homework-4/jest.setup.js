/**
 * Shared helpers for the SecureBank Jest suite (JavaScript counterpart of tests/conftest.py).
 * Jest loads this file before every test file; tests import the helpers with require('../jest.setup').
 */
const { BankAccount } = require('./src/bankingSystem');

/** A fixed "current day" so no test depends on the real clock. */
const TODAY = '2026-09-15';

/** Factory: makeAccount('Checking', 1000) returns a fresh Active account. */
const makeAccount = (type = 'Checking', balance = 1000, owner = 'Test Customer') =>
  new BankAccount(type, balance, owner);

/** Checking account with $10,000 (limit $5,000, minimum $0). */
const makeChecking = () => makeAccount('Checking', 10000);

/** Savings account with $5,000 (limit $2,000, minimum $100). */
const makeSavings = () => makeAccount('Savings', 5000);

/** Premium account with $100,000 (limit $50,000, minimum $10,000). */
const makePremium = () => makeAccount('Premium', 100000);

module.exports = { TODAY, makeAccount, makeChecking, makeSavings, makePremium };
