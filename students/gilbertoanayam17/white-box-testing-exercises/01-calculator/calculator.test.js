// Test suite for Exercise 1: Calculator Unit Tests (Module 05 - White Box Testing).
const Calculator = require("./calculator");

describe("Calculator", () => {
  let calc;

  beforeEach(() => {
    // Create a fresh Calculator instance before each test
    calc = new Calculator();
  });

  describe("add", () => {
    test("should add two positive numbers", () => {
      expect(calc.add(5, 3)).toBe(8);
    });

    test("should add two negative numbers", () => {
      expect(calc.add(-5, -3)).toBe(-8);
    });

    test("should add positive and negative numbers", () => {
      expect(calc.add(5, -3)).toBe(2);
    });

    test("should return same number when adding zero", () => {
      expect(calc.add(7, 0)).toBe(7);
    });

    test("should add floating point numbers", () => {
      expect(calc.add(0.1, 0.2)).toBeCloseTo(0.3);
    });

    test("should add very large numbers", () => {
      expect(calc.add(1e20, 1e20)).toBe(2e20);
    });

    test.each([
      [1, 1, 2],
      [-1, 1, 0],
      [0, 0, 0],
      [2.5, 2.5, 5.0],
    ])("should add %p + %p = %p (parametrized)", (a, b, expected) => {
      expect(calc.add(a, b)).toBeCloseTo(expected);
    });
  });

  describe("subtract", () => {
    test("should subtract resulting in positive number", () => {
      expect(calc.subtract(10, 4)).toBe(6);
    });

    test("should subtract resulting in negative number", () => {
      expect(calc.subtract(4, 10)).toBe(-6);
    });

    test("should return zero when subtracting same numbers", () => {
      expect(calc.subtract(9, 9)).toBe(0);
    });

    test("should add magnitude when subtracting a negative number", () => {
      expect(calc.subtract(5, -3)).toBe(8);
    });
  });

  describe("multiply", () => {
    test("should multiply two positive numbers", () => {
      expect(calc.multiply(4, 5)).toBe(20);
    });

    test("should multiply by zero", () => {
      expect(calc.multiply(123, 0)).toBe(0);
    });

    test("should multiply negative numbers", () => {
      expect(calc.multiply(-4, -5)).toBe(20);
    });

    test("should multiply numbers with mixed signs", () => {
      expect(calc.multiply(-4, 5)).toBe(-20);
    });

    test("should return same number when multiplying by one", () => {
      expect(calc.multiply(42, 1)).toBe(42);
    });
  });

  describe("divide", () => {
    test("should divide two numbers normally", () => {
      expect(calc.divide(10, 2)).toBe(5);
    });

    test("should throw error when dividing by zero", () => {
      expect(() => {
        calc.divide(10, 0);
      }).toThrow("Cannot divide by zero");
    });

    test("should divide negative numbers", () => {
      expect(calc.divide(-10, -2)).toBe(5);
    });

    test("should divide numbers with mixed signs", () => {
      expect(calc.divide(-10, 2)).toBe(-5);
    });

    test("should divide resulting in decimal", () => {
      expect(calc.divide(10, 3)).toBeCloseTo(3.333333, 5);
    });

    test("should return zero when dividing zero by a number", () => {
      expect(calc.divide(0, 5)).toBe(0);
    });

    test("should throw error when dividing by negative zero", () => {
      // -0 === 0 is true in JavaScript
      expect(() => {
        calc.divide(10, -0);
      }).toThrow("Cannot divide by zero");
    });
  });

  describe("power", () => {
    test("should raise to positive exponent", () => {
      expect(calc.power(2, 3)).toBe(8);
    });

    test("should handle zero exponent", () => {
      expect(calc.power(5, 0)).toBe(1);
    });

    test("should handle negative exponent", () => {
      expect(calc.power(2, -2)).toBeCloseTo(0.25);
    });

    test("should return zero for zero base", () => {
      expect(calc.power(0, 5)).toBe(0);
    });

    test("should keep negative base negative with odd exponent", () => {
      expect(calc.power(-2, 3)).toBe(-8);
    });

    test("should behave like square root with exponent 0.5", () => {
      expect(calc.power(9, 0.5)).toBeCloseTo(3.0);
    });
  });

  describe("sqrt", () => {
    test("should calculate square root of positive number", () => {
      expect(calc.sqrt(16)).toBeCloseTo(4.0);
    });

    test("should calculate square root of zero", () => {
      expect(calc.sqrt(0)).toBe(0);
    });

    test("should throw error for negative number", () => {
      expect(() => {
        calc.sqrt(-1);
      }).toThrow("Cannot calculate square root of negative number");
    });

    test("should calculate square root of non-perfect square", () => {
      expect(calc.sqrt(2)).toBeCloseTo(1.414213, 5);
    });

    test("should throw error just below zero", () => {
      expect(() => {
        calc.sqrt(-0.0001);
      }).toThrow();
    });
  });

  describe("modulo", () => {
    test("should return remainder of integer division", () => {
      expect(calc.modulo(10, 3)).toBe(1);
    });

    test("should return zero for exact division", () => {
      expect(calc.modulo(10, 5)).toBe(0);
    });

    test("should throw error when modulo by zero", () => {
      expect(() => {
        calc.modulo(10, 0);
      }).toThrow("Cannot divide by zero");
    });

    test("should take the sign of the dividend", () => {
      // Unlike Python, JavaScript's % keeps the sign of the dividend
      expect(calc.modulo(-10, 3)).toBe(-1);
    });
  });

  describe("absolute", () => {
    test("should return same value for positive number", () => {
      expect(calc.absolute(5)).toBe(5);
    });

    test("should return positive value for negative number", () => {
      expect(calc.absolute(-5)).toBe(5);
    });

    test("should return zero for zero", () => {
      expect(calc.absolute(0)).toBe(0);
    });

    test("should return positive value for negative float", () => {
      expect(calc.absolute(-3.5)).toBeCloseTo(3.5);
    });
  });

  describe("factorial", () => {
    test("should return 1 for zero", () => {
      expect(calc.factorial(0)).toBe(1);
    });

    test("should return 1 for one", () => {
      expect(calc.factorial(1)).toBe(1);
    });

    test("should calculate factorial of positive number (runs the loop)", () => {
      expect(calc.factorial(5)).toBe(120);
    });

    test("should calculate factorial of large number", () => {
      // 18! is the largest factorial below Number.MAX_SAFE_INTEGER
      expect(calc.factorial(18)).toBe(6402373705728000);
    });

    test("should throw error for negative number", () => {
      expect(() => {
        calc.factorial(-1);
      }).toThrow("Factorial not defined for negative numbers");
    });

    test("should throw error for float", () => {
      expect(() => {
        calc.factorial(3.5);
      }).toThrow("Factorial requires an integer");
    });

    test("should throw error for string", () => {
      expect(() => {
        calc.factorial("5");
      }).toThrow("Factorial requires an integer");
    });
  });
});
