 
const calculator = new Calculator();
const currentDisplay = document.getElementById("current");
const historyDisplay = document.getElementById("history");
const keysContainer = document.getElementById("keys");

function render() {
  currentDisplay.textContent = calculator.getDisplayValue();
  historyDisplay.innerHTML = calculator.getHistoryValue() || "&nbsp;";
}

function handleKeyClick(event) {
  const target = event.target;
  if (!target.classList.contains("key")) return;

  const digit = target.getAttribute("data-digit");
  const operator = target.getAttribute("data-operator");
  const action = target.getAttribute("data-action");

  if (digit !== null) {
    calculator.inputDigit(digit);
  } else if (operator !== null) {
    calculator.chooseOperator(operator);
  } else if (action === "equals") {
    calculator.evaluate();
  } else if (action === "clear") {
    calculator.reset();
  } else if (action === "sign") {
    calculator.toggleSign();
  } else if (action === "percent") {
    calculator.applyPercent();
  } else if (action === "decimal") {
    calculator.inputDecimal();
  }

  render();
}

function handleKeyboardInput(event) {
  const key = event.key;

  if (/^[0-9]$/.test(key)) {
    calculator.inputDigit(key);
  } else if (["+", "-", "*", "/"].includes(key)) {
    calculator.chooseOperator(key);
  } else if (key === "Enter" || key === "=") {
    calculator.evaluate();
  } else if (key === "Escape") {
    calculator.reset();
  } else if (key === ".") {
    calculator.inputDecimal();
  } else {
    return;
  }

  render();
}

keysContainer.addEventListener("click", handleKeyClick);
document.addEventListener("keydown", handleKeyboardInput);

render();
