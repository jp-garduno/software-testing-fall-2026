const Calculator = require("../src/calculator");

describe("Calculator", () => {
    let calc;

    beforeEach(() => {
        // Create a fresh Calculator instance before each test
        calc = new Calculator();
    });

    // TODO: Write tests for add method
    describe("add", () => {
        test("should add two positive numbers", () => {
            const result = calc.add(5, 3);
            expect(result).toBe(8);
        });

        test("should add two negative numbers", () => {
            // Replace with your implementation
          const result = calc.add(-5, -3);
          expect(result).toBe(-8);
        });

        test("should add positive and negative numbers", () => {
            // Replace with your implementation
          const result = calc.add(5, -3);
          expect(result).toBe(2);
        });
    });

    // TODO: Write tests for subtract method
    describe("subtract", () => {
        test("should subtract resulting in positive number", () => {
            // Replace with your implementation
          const result = calc.subtract(5, 3);
          expect(result).toBe(2);
        });

        test("should subtract resulting in negative number", () => {
            // Replace with your implementation
          const result = calc.subtract(-5, -3);
          expect(result).toBe(-2);
        });
    });

    // TODO: Write tests for multiply method
    describe("multiply", () => {
        test("should multiply two positive numbers", () => {
            // Replace with your implementation
          const result = calc.multiply(5, 3);
          expect(result).toBe(15);
        });

        test("should multiply by zero", () => {
            // Replace with your implementation
          const result = calc.multiply(5, 0);
          expect(result).toBe(0);
        });

        test("should multiply negative numbers", () => {
            // Replace with your implementation
          const result = calc.multiply(-5, -3);
          expect(result).toBe(15);
        });
    });

    // TODO: Write tests for divide method
    describe("divide", () => {
        test("should divide two numbers normally", () => {
            // Replace with your implementation
          const result = calc.divide(6, 2);
          expect(result).toBe(3);
        });

        test("should throw error when dividing by zero", () => {
            expect(() => {
                calc.divide(10, 0);
            }).toThrow("Cannot divide by zero");
        });

        test("should divide negative numbers", () => {
            // Replace with your implementation
          const result = calc.divide(-6, -2);
          expect(result).toBe(3);
        });
    });

    // TODO: Write tests for power method
    describe("power", () => {
        test("should raise to positive exponent", () => {
            // Replace with your implementation
          const result = calc.power(6, 2);
          expect(result).toBe(36);
        });

        test("should handle zero exponent", () => {
            // Replace with your implementation
          const result = calc.power(6, 0);
          expect(result).toBe(1);
        });

        test("should handle negative exponent", () => {
            // Replace with your implementation
          const result = calc.power(2, -2);
          expect(result).toBe(0.25);
        });
    });

    // TODO: Write tests for sqrt method
    describe("sqrt", () => {
        test("should calculate square root of positive number", () => {
            // Replace with your implementation
          const result = calc.sqrt(4);
          expect(result).toBe(2);
        });

        test("should calculate square root of zero", () => {
            // Replace with your implementation
          const result = calc.sqrt(0);
          expect(result).toBe(0);
        });

        test("should throw error for negative number", () => {
            // Hint: Use expect(() => { }).toThrow()
          expect(() => {
            calc.sqrt(-4);
          }).toThrow("Cannot calculate square root of negative number");
        });
    });
});
