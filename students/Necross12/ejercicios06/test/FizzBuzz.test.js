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

  test("returns Fizz for 6", () => {
    expect(fizzbuzz(6)).toBe("Fizz");
  });

  test("returns Buzz for 5", () => {
    expect(fizzbuzz(5)).toBe("Buzz");
  });

  test("returns Buzz for 10", () => {
    expect(fizzbuzz(10)).toBe("Buzz");
  });

  test("returns FizzBuzz for 15", () => {
    expect(fizzbuzz(15)).toBe("FizzBuzz");
  });

  test("returns FizzBuzz for 30", () => {
    expect(fizzbuzz(30)).toBe("FizzBuzz");
  });
})
