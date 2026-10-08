class Calculator {
  /**
   * A simple calculator with basic arithmetic operations.
   */

  /**
   * Add two numbers.
   */
  add(a, b) {
    return a + b;
  }

  /**
   * Subtract b from a.
   */
  subtract(a, b) {
    return a - b;
  }

  /**
   * Multiply two numbers.
   */
  multiply(a, b) {
    return a * b;
  }

  /**
   * Divide a by b. Throws Error if b is zero.
   */
  divide(a, b) {
    if (b === 0) {
      throw new Error("Cannot divide by zero");
    }
    return a / b;
  }

  /**
   * Raise base to the power of exponent.
   */
  power(base, exponent) {
    return Math.pow(base, exponent);
  }

  /**
   * Calculate square root. Throws Error if x is negative.
   */
  sqrt(x) {
    if (x < 0) {
      throw new Error("Cannot calculate square root of negative number");
    }
    return Math.sqrt(x);
  }
}

module.exports = Calculator;