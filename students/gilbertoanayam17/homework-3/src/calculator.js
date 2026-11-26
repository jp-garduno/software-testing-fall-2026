'use strict';

const {
  add,
  subtract,
  multiply,
  divide,
  power,
  percentage,
  CalculatorError,
} = require('./operations');
const { parseNumber, validateOperator } = require('./validation');

const OPERATIONS = new Map([
  ['+', add],
  ['-', subtract],
  ['*', multiply],
  ['/', divide],
  ['^', power],
  ['%', percentage],
]);

class Calculator {
  constructor() {
    this.entries = [];
  }

  calculate(left, operator, right) {
    const symbol = validateOperator(operator);
    const first = parseNumber(left);
    const second = parseNumber(right);
    const result = OPERATIONS.get(symbol)(first, second);
    this.entries.push(`${first} ${symbol} ${second} = ${result}`);
    return result;
  }

  get history() {
    return this.entries.slice();
  }

  last() {
    if (this.entries.length === 0) {
      throw new CalculatorError('no calculations recorded yet');
    }
    return this.entries[this.entries.length - 1];
  }

  clear() {
    this.entries = [];
  }
}

module.exports = { Calculator, OPERATIONS };
