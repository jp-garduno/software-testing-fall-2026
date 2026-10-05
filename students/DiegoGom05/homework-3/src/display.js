const display = document.getElementById('display');

function updateDisplay(value) {
  display.textContent = value;
}

function getDisplayValue() {
  return display.textContent;
}

function clearDisplay() {
  updateDisplay('0');
}

function appendNumber(number) {
  const currentValue = getDisplayValue();

  if (currentValue === '0') {
    updateDisplay(number);
  } else {
    updateDisplay(currentValue + number);
  }
}

function appendDecimal() {
  const currentValue = getDisplayValue();

  if (!currentValue.includes('.')) {
    updateDisplay(currentValue + '.');
  }
}

function showError(message) {
  updateDisplay(message);
}

function displayResult(result) {
  if (Number.isInteger(result)) {
    updateDisplay(result);
  } else {
    updateDisplay(parseFloat(result.toFixed(8)));
  }
}

export {
  updateDisplay,
  getDisplayValue,
  clearDisplay,
  appendNumber,
  appendDecimal,
  showError,
  displayResult,
};
