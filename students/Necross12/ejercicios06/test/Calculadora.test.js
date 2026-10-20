import { StringCalculator } from "../src/Calculadora";

describe("Calculadora", () => {
    test("empty string returns 0", () => {
        const calculator = new StringCalculator();
        expect(calculator.add("")).toBe(0);
    });
});
