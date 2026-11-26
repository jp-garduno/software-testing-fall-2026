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

  // Part 4: Additional challenges

  /**
   * Return remainder of a divided by b.
   */
  modulo(a, b) {
    if (b === 0) {
      throw new Error("Cannot divide by zero");
    }
    return a % b;
  }

  /**
   * Return absolute value of x.
   */
  absolute(x) {
    return Math.abs(x);
  }

  /**
   * Calculate factorial of n. Throws Error if n is negative or not an integer.
   */
  factorial(n) {
    if (!Number.isInteger(n)) {
      throw new Error("Factorial requires an integer");
    }
    if (n < 0) {
      throw new Error("Factorial not defined for negative numbers");
    }
    if (n === 0 || n === 1) {
      return 1;
    }
    let result = 1;
    for (let i = 2; i <= n; i++) {
      result *= i;
    }
    return result;
  }
}

module.exports = Calculator;
