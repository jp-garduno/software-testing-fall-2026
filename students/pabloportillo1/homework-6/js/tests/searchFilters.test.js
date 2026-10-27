const { Book, BookDetails } = require("../src/book");
const { Library } = require("../src/library");

const CATALOG = [
  ["0306406152", "Clean Code", "Robert Martin", { genre: "Software", year: 2008, rating: 4.4 }],
  ["0131103628", "The C Programming Language", "Brian Kernighan", { genre: "Software", year: 1988, rating: 4.7 }],
  ["0201633612", "Design Patterns", "Erich Gamma", { genre: "Software", year: 1994, rating: 4.5 }],
  ["0141439513", "Pride and Prejudice", "Jane Austen", { genre: "Fiction", year: 1813, rating: 4.3 }],
  ["0061120084", "To Kill a Mockingbird", "Harper Lee", { genre: "Fiction", year: 1960 }],
];
let library;

beforeEach(() => {
  library = new Library();
  CATALOG.forEach(([isbn, title, author, details]) =>
    library.addBook(new Book(isbn, title, author, 1, new BookDetails(details))),
  );
});

const titles = (books) => books.map((book) => book.title);

test("search without criteria returns the whole catalog", () => {
  expect(library.search()).toHaveLength(CATALOG.length);
});
