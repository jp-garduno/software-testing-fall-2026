const Calculator = require("./calculator");

describe("Calculator", () => {
  let calc;

  beforeEach(() => {
    // Create a fresh Calculator instance before each test
    calc = new Calculator();
  });

  // Tests for add method
  describe("add", () => {
    test("should add two positive numbers", () => {
      expect(calc.add(5, 3)).toBe(8);
    });

    test("should add two negative numbers", () => {
      expect(calc.add(-4, -6)).toBe(-10);
    });

    test("should add positive and negative numbers", () => {
      expect(calc.add(10, -3)).toBe(7);
    });
  });

  // Tests for subtract method
  describe("subtract", () => {
    test("should subtract resulting in positive number", () => {
      expect(calc.subtract(10, 4)).toBe(6);
    });

    test("should subtract resulting in negative number", () => {
      expect(calc.subtract(3, 8)).toBe(-5);
    });
  });

  // Tests for multiply method
  describe("multiply", () => {
    test("should multiply two positive numbers", () => {
      expect(calc.multiply(4, 3)).toBe(12);
    });

    test("should multiply by zero", () => {
      expect(calc.multiply(7, 0)).toBe(0);
      expect(calc.multiply(0, 5)).toBe(0);
    });

    test("should multiply negative numbers", () => {
      expect(calc.multiply(-2, 5)).toBe(-10);
      expect(calc.multiply(-3, -4)).toBe(12);
    });
  });

  // Tests for divide method
  describe("divide", () => {
    test("should divide two numbers normally", () => {
      expect(calc.divide(12, 3)).toBe(4);
      expect(calc.divide(5, 2)).toBe(2.5);
    });

    test("should throw error when dividing by zero", () => {
      expect(() => {
        calc.divide(10, 0);
      }).toThrow("Cannot divide by zero");
    });

    test("should divide negative numbers", () => {
      expect(calc.divide(-10, 2)).toBe(-5);
      expect(calc.divide(-12, -4)).toBe(3);
    });
  });

  // Tests for power method
  describe("power", () => {
    test("should raise to positive exponent", () => {
      expect(calc.power(2, 3)).toBe(8);
      expect(calc.power(5, 2)).toBe(25);
    });

    test("should handle zero exponent", () => {
      expect(calc.power(5, 0)).toBe(1);
      expect(calc.power(0, 0)).toBe(1);
    });

    test("should handle negative exponent", () => {
      expect(calc.power(2, -2)).toBe(0.25);
    });
  });

  // Tests for sqrt method
  describe("sqrt", () => {
    test("should calculate square root of positive number", () => {
      expect(calc.sqrt(16)).toBe(4);
      expect(calc.sqrt(2)).toBeCloseTo(1.4142, 4);
    });

    test("should calculate square root of zero", () => {
      expect(calc.sqrt(0)).toBe(0);
    });

    test("should throw error for negative number", () => {
      expect(() => {
        calc.sqrt(-9);
      }).toThrow("Cannot calculate square root of negative number");
    });
  });
});