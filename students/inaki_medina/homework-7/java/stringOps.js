function reverseString(str) {
  return str.split("").reverse().join("");
}

function isPalindrome(str) {
  const cleaned = str.toLowerCase().replace(/\s/g, "");
  return cleaned === cleaned.split("").reverse().join("");
}

function countVowels(str) {
  return (str.match(/[aeiou]/gi) || []).length;
}

module.exports = { reverseString, isPalindrome, countVowels };