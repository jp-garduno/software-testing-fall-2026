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

test("borrow takes one copy", () => {
  const book = makeBook(2);

  book.borrow();

  expect(book.availableCopies).toBe(1);
});

test("borrow without available copies is rejected", () => {
  expect(() => makeBook(0).borrow()).toThrow("No copies available for 'Clean Code'");
});

test("returnCopy puts the copy back", () => {
  const book = makeBook(2);
  book.borrow();

  book.returnCopy();

  expect(book.availableCopies).toBe(2);
});

test("returnCopy when every copy is in is rejected", () => {
  expect(() => makeBook(2).returnCopy()).toThrow("All copies of 'Clean Code' are already in");
});

test("isbn with nine digits is rejected", () => {
  expect(() => new Book("030640615", "Clean Code", "Robert Martin")).toThrow("ISBN must be 10 or 13 digits");
});

test("isbn with thirteen digits is accepted", () => {
  expect(new Book("9780306406157", "Clean Code", "Robert Martin").isbn).toBe("9780306406157");
});
