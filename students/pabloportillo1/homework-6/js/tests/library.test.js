const { Book } = require("../src/book");
const { Library } = require("../src/library");

let library;

beforeEach(() => {
  library = new Library();
});

test("added book can be looked up by isbn", () => {
  const book = new Book("0306406152", "Clean Code", "Robert Martin");

  library.addBook(book);

  expect(library.getBook("0306406152")).toBe(book);
});
