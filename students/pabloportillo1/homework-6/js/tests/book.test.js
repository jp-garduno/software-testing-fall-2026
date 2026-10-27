const { Book } = require("../src/book");

const ISBN = "0306406152";
const makeBook = (totalCopies = 1) => new Book(ISBN, "Clean Code", "Robert Martin", totalCopies);

test("book is created with isbn, title and author", () => {
  const book = new Book("0306406152", "Clean Code", "Robert Martin");

  expect([book.isbn, book.title, book.author]).toEqual(["0306406152", "Clean Code", "Robert Martin"]);
});

test("book starts with every copy available", () => {
  expect(makeBook(5).availableCopies).toBe(5);
});

test("book with copies is available", () => {
  expect(makeBook(1).isAvailable()).toBe(true);
});

test("book without copies is not available", () => {
  expect(makeBook(0).isAvailable()).toBe(false);
});
