const { Book } = require("../src/book");

test("book is created with isbn, title and author", () => {
  const book = new Book("0306406152", "Clean Code", "Robert Martin");

  expect([book.isbn, book.title, book.author]).toEqual(["0306406152", "Clean Code", "Robert Martin"]);
});
