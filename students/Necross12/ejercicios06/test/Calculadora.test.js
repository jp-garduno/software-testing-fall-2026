import { StringCalculator } from "../src/Calculadora";

describe("Calculadora", () => {
    let calculator;

    beforeEach(() => {
        calculator = new StringCalculator();
    });

    test("empty string returns 0", () => {
        expect(calculator.add("")).toBe(0);
    });

    test("single number returns itself", () => {
        expect(calculator.add("1")).toBe(1);
        expect(calculator.add("5")).toBe(5);
    });

    test("two numbers separated by comma", () => {
        expect(calculator.add("1,2")).toBe(3);
        expect(calculator.add("5,10")).toBe(15);
    });

    test("manejar varios números", () => {
        expect(calculator.add("1,2,3")).toBe(6);
        expect(calculator.add("1,2,3,4,5")).toBe(15);
    });

    test("manejar fin de linea", () => {
        expect(calculator.add("1\n2,3")).toBe(6);
        expect(calculator.add("1\n2\n3")).toBe(6);
    });

    test("delimitador personalizado", () => {
        expect(calculator.add("//;\n1;2")).toBe(3);
        expect(calculator.add("//|\n1|2|3")).toBe(6);
    });

    test("negative numbers throw exception", () => {
        expect(() => calculator.add("-1,2")).toThrow("negatives not allowed: -1");
        expect(() => calculator.add("1,-2,-3")).toThrow("negatives not allowed: -2, -3");
    });

    test("ignores numbers greater than 1000", () => {
        expect(calculator.add("2,1001")).toBe(2);
        expect(calculator.add("1000,1001,2")).toBe(1002);
    });

    test("delimiter of any length", () => {
        expect(calculator.add("//[***]\n1***2***3")).toBe(6);
        expect(calculator.add("//[---]\n1---2---3")).toBe(6);
    });
});
