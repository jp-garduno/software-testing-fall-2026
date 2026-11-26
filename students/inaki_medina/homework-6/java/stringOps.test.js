const { reverseString, isPalindrome, countVowels } = require("./stringOps");
const nonStrings = [[null], [123], [undefined], [{}]];

test.each(nonStrings)("reverseString rejects %p", (input) => {
  expect(() => reverseString(input)).toThrow(TypeError);
});

test.each(nonStrings)("isPalindrome rejects %p", (input) => {
  expect(() => isPalindrome(input)).toThrow(TypeError);
});

test.each(nonStrings)("countVowels rejects %p", (input) => {
  expect(() => countVowels(input)).toThrow(TypeError);
});

test.each([
  { input: "hello", expected: "olleh" },
  { input: "world", expected: "dlrow" },
  { input: "", expected: "" },
  { input: "a", expected: "a" },
])("reverseString($input) should return $expected", ({ input, expected }) => {
  expect(reverseString(input)).toBe(expected);
});

test.each([
  { input: "adfadssdafda", expected: true },
  { input: "worldlrow", expected: true },
  { input: "worlddrow", expected: false },
  { input: "adfadssdafd", expected: false },
  { input: "", expected: true },
])("isPalindrome($input) should return $expected", ({ input, expected }) => {
  expect(isPalindrome(input)).toBe(expected);
});

test.each([
  { input: "adfadssdafda", expected: 4 },
  { input: "worldlrow", expected: 2 },
  { input: "worlddrow", expected: 2 },
  { input: "aeioua", expected: 6 },
  { input: "aei^#(@^@(!oua", expected: 6 },
])("countVowels($input) should return $expected", ({ input, expected }) => {
  expect(countVowels(input)).toBe(expected);
});