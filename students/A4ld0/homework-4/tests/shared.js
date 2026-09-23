const BankAccount = require('../src/bankingSystem');
const cases = require('../design/cases.json');

const decode = (value) => value && typeof value === 'object' && '$number' in value
  ? { NaN, Infinity, '-Infinity': -Infinity }[value.$number] : value;

function checkpoint(account, expected = {}) {
  expect(account.snapshot()).toMatchObject(expected);
}

function runCase(scenario) {
  let now = scenario.date || '2026-09-22';
  const args = scenario.account.map(decode);
  if ('constructor_error' in scenario) {
    let caught;
    try { new BankAccount(...args, () => now); } catch (error) { caught = error; }
    expect(caught).toBeInstanceOf(Error);
    expect(caught.message).toBe(scenario.constructor_error);
    return;
  }
  const account = new BankAccount(...args, () => now);
  checkpoint(account, scenario.initial);
  for (const step of scenario.steps || []) {
    if (step.date) now = step.date;
    const before = account.snapshot();
    const callArgs = (step.args || []).map(decode);
    const result = account[step.call](...callArgs);
    expect(result).toEqual(step.expect);
    if (!result.success && !step.allows_state_change) expect(account.snapshot()).toEqual(before);
    checkpoint(account, step.snapshot);
    if (step.mutate_return) {
      result.transactions[0].detail = 'tampered';
      expect(account.history(...callArgs)).toEqual(step.expect);
    }
  }
}

module.exports = {
  casesFor: (technique) => cases.filter((scenario) => scenario.technique === technique),
  runCase,
};
