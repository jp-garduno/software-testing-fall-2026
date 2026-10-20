import { StringCalculator } from "../src/Calculadora";

describe("Calculadora", () => {
    test("empty string returns 0", () => {
        const calculator = new StringCalculator();
        expect(calculator.add("")).toBe(0);
    });

    test("single number returns itself", () => {
        const calculator = new StringCalculator();
        expect(calculator.add("1")).toBe(1);
        expect(calculator.add("5")).toBe(5);
    });

    test("two numbers separated by comma", () => {
        const calculator = new StringCalculator();
        expect(calculator.add("1,2")).toBe(3);
        expect(calculator.add("5,10")).toBe(15);
    });

    test("manejar varios números", () => {
        const calculator = new StringCalculator();
        expect(calculator.add("1,2,3")).toBe(6);
        expect(calculator.add("1,2,3,4,5")).toBe(15);
    });
});
