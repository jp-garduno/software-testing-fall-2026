 
const ops =
  typeof require !== "undefined"
    ? require("./operations")
    : {
        add,
        subtract,
        multiply,
        divide,
        percent,
        toggleSign,
        roundResult,
        applyOperator,
      };

class Calculator {
  constructor() {
    this.reset();
  }

  reset() {
    this.currentValue = "0";
    this.previousValue = null;
    this.operator = null;
    this.shouldResetDisplay = false;
  }

  inputDigit(digit) {
    if (this.shouldResetDisplay) {
      this.currentValue = digit;
      this.shouldResetDisplay = false;
      return;
    }

    if (this.currentValue === "0") {
      this.currentValue = digit;
    } else {
      this.currentValue = this.currentValue + digit;
    }
  }

  inputDecimal() {
    if (this.shouldResetDisplay) {
      this.currentValue = "0.";
      this.shouldResetDisplay = false;
      return;
    }
    if (this.currentValue.indexOf(".") === -1) {
      this.currentValue = this.currentValue + ".";
    }
  }

  chooseOperator(nextOperator) {
    if (this.operator !== null && !this.shouldResetDisplay) {
      this.evaluate();
    }
    this.previousValue = this.currentValue;
    this.operator = nextOperator;
    this.shouldResetDisplay = true;
  }

  evaluate() {
    if (this.operator === null || this.previousValue === null) {
      return;
    }

    const left = parseFloat(this.previousValue);
    const right = parseFloat(this.currentValue);
    let result;

    try {
      result = ops.applyOperator(this.operator, left, right);
    } catch (error) {
      this.currentValue = "Error";
      this.operator = null;
      this.previousValue = null;
      this.shouldResetDisplay = true;
      return;
    }

    this.currentValue = String(ops.roundResult(result));
    this.operator = null;
    this.previousValue = null;
    this.shouldResetDisplay = true;
  }

  toggleSign() {
    this.currentValue = String(ops.toggleSign(parseFloat(this.currentValue)));
  }

  applyPercent() {
    this.currentValue = String(ops.percent(parseFloat(this.currentValue)));
  }

  getDisplayValue() {
    return this.currentValue;
  }

  getHistoryValue() {
    if (this.previousValue === null || this.operator === null) {
      return "";
    }
    return this.previousValue + " " + this.operator;
  }
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = Calculator;
}
