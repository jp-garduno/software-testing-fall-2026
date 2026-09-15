import {
  updateDisplay,
  getDisplayValue,
  clearDisplay,
  appendNumber,
  appendDecimal,
  showError,
  displayResult,
} from './display.js';

import { calculate } from './operations.js';

let firstNumber = null;
let currentOperator = null;
let waitingForNumber = false;

const numberButtons = document.querySelectorAll('.btn-num');
const operatorButtons = document.querySelectorAll('.btn-op');
const clearButton = document.getElementById('btn-clear');
const equalsButton = document.getElementById('btn-equals');

numberButtons.forEach((button) => {
  button.addEventListener('click', () => {
    const number = button.dataset.num;

    if (number === '.') {
      if (!waitingForNumber) {
        appendDecimal();
      }
      return;
    }

    if (waitingForNumber) {
      updateDisplay(number);
      waitingForNumber = false;
    } else {
      appendNumber(number);
    }
  });
});

operatorButtons.forEach((button) => {
  button.addEventListener('click', () => {
    const selectedOperator = button.dataset.op;
    const currentNumber = parseFloat(getDisplayValue());

    if (firstNumber === null) {
      firstNumber = currentNumber;
    } else if (currentOperator !== null && !waitingForNumber) {
      try {
        const result = calculate(firstNumber, currentNumber, currentOperator);

        displayResult(result);
        firstNumber = result;
      } catch (error) {
        showError(error.message);
        resetCalculator();
        return;
      }
    }

    currentOperator = selectedOperator;
    waitingForNumber = true;
  });
});

equalsButton.addEventListener('click', () => {
  if (firstNumber === null || currentOperator === null) {
    return;
  }

  const secondNumber = parseFloat(getDisplayValue());

  try {
    const result = calculate(firstNumber, secondNumber, currentOperator);

    displayResult(result);

    firstNumber = result;
    currentOperator = null;
    waitingForNumber = true;
  } catch (error) {
    showError(error.message);
    resetCalculator();
  }
});

clearButton.addEventListener('click', () => {
  resetCalculator();
});

function resetCalculator() {
  firstNumber = null;
  currentOperator = null;
  waitingForNumber = false;
  clearDisplay();
}
