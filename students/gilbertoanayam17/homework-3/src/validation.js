'use strict';

const { CalculatorError } = require('./operations');

const VALID_OPERATORS = ['+', '-', '*', '/', '^', '%'];

function parseNumber(value) {
  if (typeof value === 'number') {
    if (!Number.isFinite(value)) {
      throw new CalculatorError('value must be a finite number');
    }
    return value;
  }
  if (typeof value !== 'string') {
    throw new CalculatorError('operand must be a number or a string');
  }
  const parsed = Number(value.trim());
  if (value.trim() === '' || Number.isNaN(parsed)) {
    throw new CalculatorError(`not a number: ${value}`);
  }
  return parsed;
}

function validateOperator(operator) {
  if (typeof operator !== 'string') {
    throw new CalculatorError('operator must be a string');
  }
  const cleaned = operator.trim();
  if (!VALID_OPERATORS.includes(cleaned)) {
    throw new CalculatorError(
      `unknown operator "${cleaned}", expected one of: ${VALID_OPERATORS.join(' ')}`
    );
  }
  return cleaned;
}

module.exports = { VALID_OPERATORS, parseNumber, validateOperator };
