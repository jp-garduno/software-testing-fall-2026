const Calculator = require("./calculator");

describe("Calculator", () => {
  let calc;

  beforeEach(() => {
    // Create a fresh Calculator instance before each test
    calc = new Calculator();
  });

  // TODO: Write tests for add method
  describe("add", () => {
    test("should add two positive numbers", () => {
      // Replace with your implementation
        expect(calc.add(15,3)).toBe(18);
    });

    test("should add two negative numbers", () => {
      // Replace with your implementation
        expect(calc.add(-15,-3)).toBe(-18);
    });

    test("should add positive and negative numbers", () => {
      // Replace with your implementation
        expect(calc.add(15,-3)).toBe(12);
    });

    test("should handle zero and large numbers", () => {
      expect(calc.add(0, 0)).toBe(0);
      expect(calc.add(5, 0)).toBe(5);
      expect(calc.add(1e12, 1e12)).toBe(2e12);
    });

    test("should handle decimals", () => {
      expect(calc.add(0.1, 0.2)).toBeCloseTo(0.3);
    });
  });

  // TODO: Write tests for subtract method
  describe("subtract", () => {
    test("should subtract resulting in positive number", () => {
      // Replace with your implementation
        expect(calc.subtract(10,4)).toBe(6);
    });

    test("should subtract resulting in negative number", () => {
      // Replace with your implementation
        expect(calc.subtract(5,9)).toBe(-4);
    });

    test("should subtract zero and equal numbers", () => {
      expect(calc.subtract(7, 0)).toBe(7);
      expect(calc.subtract(7, 7)).toBe(0);
    });
  });

  // TODO: Write tests for multiply method
  describe("multiply", () => {
    test("should multiply two positive numbers", () => {
      // Replace with your implementation
        expect(calc.multiply(4, 5)).toBe(20);
    });

    test("should multiply by zero", () => {
      // Replace with your implementation
        expect(calc.multiply(5, 0)).toBe(0);
    });

    test("should multiply negative numbers", () => {
      // Replace with your implementation
      expect(calc.multiply(-4, -5)).toBe(20);
      expect(calc.multiply(-4, 5)).toBe(-20);
    });

    test("should handle large numbers", () => {
      expect(calc.multiply(1e6, 1e6)).toBe(1e12);
    });
  });

  // TODO: Write tests for divide method
  describe("divide", () => {
    test("should divide two numbers normally", () => {
      // Replace with your implementation
      expect(calc.divide(10, 2)).toBe(5);
      expect(calc.divide(7, 2)).toBe(3.5);
    });

    test("should throw error when dividing by zero", () => {
      // Hint: Use expect(() => { }).toThrow()
      expect(() => {
        calc.divide(10, 0);
      }).toThrow("Cannot divide by zero");
    });

    test("should divide negative numbers", () => {
      // Replace with your implementation
      expect(calc.divide(-10, 2)).toBe(-5);
      expect(calc.divide(-10, -2)).toBe(5);
    });

    test("should return zero when dividing zero by a number", () => {
      expect(calc.divide(0, 5)).toBe(0);
    });
  });

  // TODO: Write tests for power method
  describe("power", () => {
    test("should raise to positive exponent", () => {
      // Replace with your implementation
      expect(calc.power(2, 3)).toBe(8);
    });

    test("should handle zero exponent", () => {
      // Replace with your implementation
      expect(calc.power(5, 0)).toBe(1);
      expect(calc.power(0, 0)).toBe(1);
    });

    test("should handle negative exponent", () => {
      // Replace with your implementation
      expect(calc.power(2, -2)).toBe(0.25);
    });

    test("should handle negative base", () => {
      expect(calc.power(-2, 3)).toBe(-8);
      expect(calc.power(-2, 2)).toBe(4);
    });
  });

  // TODO: Write tests for sqrt method
  describe("sqrt", () => {
    test("should calculate square root of positive number", () => {
      // Replace with your implementation
      expect(calc.sqrt(16)).toBe(4);
      expect(calc.sqrt(2)).toBeCloseTo(1.41421, 5);
    });

    test("should calculate square root of zero", () => {
      // Replace with your implementation
      expect(calc.sqrt(0)).toBe(0);
    });

    test("should throw error for negative number", () => {
      // Hint: Use expect(() => { }).toThrow()
      expect(() => {
        calc.sqrt(-4);
      }).toThrow();
    });
  });
});