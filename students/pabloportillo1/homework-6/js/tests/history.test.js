const { Book } = require("../src/book");
const { Library, NotFoundError } = require("../src/library");
const { Member } = require("../src/member");
const { FakeClock } = require("./fakeClock");

const CLEAN_CODE = "0306406152";
const K_AND_R = "0131103628";
const PATTERNS = "0201633612";
let clock;
let library;

beforeEach(() => {
  clock = new FakeClock();
  library = new Library({ clock: clock.now });
  library.addBook(new Book(CLEAN_CODE, "Clean Code", "Robert Martin", 2));
  library.addBook(new Book(K_AND_R, "The C Programming Language", "Brian Kernighan", 2));
  library.addBook(new Book(PATTERNS, "Design Patterns", "Erich Gamma", 2));
  library.registerMember(new Member("M001", "Ada Lovelace"));
  library.registerMember(new Member("M002", "Grace Hopper"));
});

test("member history lists the member's loans in borrow order", () => {
  library.borrowBook("M001", K_AND_R);
  library.borrowBook("M002", PATTERNS);
  clock.advance(3);
  library.returnBook("M001", K_AND_R);
  library.borrowBook("M001", CLEAN_CODE);

  const history = library.memberHistory("M001");

  expect(history.map((loan) => [loan.isbn, loan.returnedOn !== null])).toEqual([
    [K_AND_R, true],
    [CLEAN_CODE, false],
  ]);
});

test("history of an unknown member is rejected", () => {
  expect(() => library.memberHistory("M404")).toThrow(NotFoundError);
});

test("most borrowed book is the one with most loans", () => {
  library.borrowBook("M001", CLEAN_CODE);
  library.borrowBook("M001", PATTERNS);
  library.borrowBook("M002", PATTERNS);

  expect(library.mostBorrowedBook().isbn).toBe(PATTERNS);
});

test("most borrowed book is null before any loan", () => {
  expect(library.mostBorrowedBook()).toBeNull();
});

test("tie for most borrowed goes to the first title alphabetically", () => {
  library.borrowBook("M001", K_AND_R);
  library.borrowBook("M001", PATTERNS);

  expect(library.mostBorrowedBook().title).toBe("Design Patterns");
});

test("borrow statistics count borrows, returns and active loans", () => {
  library.borrowBook("M001", CLEAN_CODE);
  library.borrowBook("M001", PATTERNS);
  library.borrowBook("M002", PATTERNS);
  library.returnBook("M001", PATTERNS);

  expect(library.borrowStatistics()).toEqual({ totalBorrows: 3, returns: 1, activeLoans: 2 });
});
