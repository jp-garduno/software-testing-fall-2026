import {fizzbuzz} from "../src/FizzBuzz";

describe("FizzBuzz", () => {
  test("returns 1 for input 1", () => {
    expect(fizzbuzz(1)).toBe("1");
  });

  test("returns 2 for input 2", () => {
    expect(fizzbuzz(2)).toBe("2");
  });

  test("returns Fizz for 3", () => {
    expect(fizzbuzz(3)).toBe("Fizz");
  });
})
