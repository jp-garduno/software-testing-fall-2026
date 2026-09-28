'use strict';

const { Calculator, OPERATIONS } = require('./calculator');
const { CalculatorError } = require('./operations');
const { VALID_OPERATORS, parseNumber, validateOperator } = require('./validation');

function runExamples(expressions) {
  const calculator = new Calculator();
  expressions.forEach(function (expression) {
    calculator.calculate(expression[0], expression[1], expression[2]);
  });
  return calculator.history.join('\n');
}

module.exports = {
  Calculator,
  CalculatorError,
  OPERATIONS,
  VALID_OPERATORS,
  parseNumber,
  validateOperator,
  runExamples,
};
