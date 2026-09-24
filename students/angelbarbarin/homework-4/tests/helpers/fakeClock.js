'use strict';

const { BankAccount } = require('../../src/bankingSystem');

/** Reloj controlable: lunes 14 de septiembre de 2026, 10:00 (hora local). */
function createClock(start = new Date(2026, 8, 14, 10, 0, 0)) {
  let now = start;
  const clock = () => now;
  clock.advance = ({ days = 0, hours = 0, minutes = 0, seconds = 0 } = {}) => {
    const ms = (((days * 24 + hours) * 60 + minutes) * 60 + seconds) * 1000;
    now = new Date(now.getTime() + ms);
  };
  return clock;
}

/** Fábrica de cuentas que comparten un reloj controlable. */
function accountFactory(clock) {
  return (type = 'Checking', balance = 1000) => new BankAccount(type, balance, clock);
}

module.exports = { createClock, accountFactory };
