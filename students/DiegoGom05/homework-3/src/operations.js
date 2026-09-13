 
const DEFAULT_PRECISION = 10;

function add(a, b) {
  return a + b;
}

function subtract(a, b) {
  return a - b;
}

function multiply(a, b) {
  return a * b;
}

function divide(a, b) {
  if (b === 0) {
    throw new Error("Division by zero is not allowed");
  }
  return a / b;
}

function percent(value) {
  return value / 100;
}

function toggleSign(value) {
  return value * -1;
}

// Rounds a number to avoid floating point artifacts,
// e.g. 0.1 + 0.2 === 0.30000000000000004 without this.
function roundResult(value, precision) {
  const factor = Math.pow(10, precision || DEFAULT_PRECISION);
  return Math.round(value * factor) / factor;
}

function applyOperator(operator, left, right) {
  switch (operator) {
    case "+":
      return add(left, right);
    case "-":
      return subtract(left, right);
    case "*":
      return multiply(left, right);
    case "/":
      return divide(left, right);
    default:
      // Unknown operator: fall back to returning the right-hand value
      // instead of silently failing.
      return right;
  }
}

// Exported for use in the browser (attached to window) and for tests (module.exports)
if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    add: add,
    subtract: subtract,
    multiply: multiply,
    divide: divide,
    percent: percent,
    toggleSign: toggleSign,
    roundResult: roundResult,
    applyOperator: applyOperator,
  };
}
