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
});
