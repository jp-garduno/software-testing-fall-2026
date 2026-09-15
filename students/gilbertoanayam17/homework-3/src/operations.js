'use strict';

class CalculatorError extends Error {
  constructor(message) {
    super(message);
    this.name = 'CalculatorError';
  }
}

function add(left, right) {
  return left + right;
}

function subtract(left, right) {
  return left - right;
}

function multiply(left, right) {
  return left * right;
}

function divide(left, right) {
  if (right === 0) {
    throw new CalculatorError('cannot divide by zero');
  }
  return left / right;
}

function power(base, exponent) {
  const result = base ** exponent;
  if (Number.isNaN(result)) {
    throw new CalculatorError('result is not a real number');
  }
  return result;
}

function percentage(value, percent) {
  return (value * percent) / 100;
}

module.exports = {
  CalculatorError,
  add,
  subtract,
  multiply,
  divide,
  power,
  percentage,
};
