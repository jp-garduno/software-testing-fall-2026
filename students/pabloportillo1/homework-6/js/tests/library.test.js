const { Book } = require("../src/book");
const { Member } = require("../src/member");
const { Library, NotFoundError } = require("../src/library");

let library;
let book;
let member;

beforeEach(() => {
  library = new Library();
});

function stock() {
  book = new Book("0306406152", "Clean Code", "Robert Martin", 2);
  member = new Member("M001", "Ada Lovelace");
  library.addBook(book);
  library.registerMember(member);
}

test("added book can be looked up by isbn", () => {
  const book = new Book("0306406152", "Clean Code", "Robert Martin");

  library.addBook(book);

  expect(library.getBook("0306406152")).toBe(book);
});

test("adding a book with an existing isbn is rejected", () => {
  library.addBook(new Book("0306406152", "Clean Code", "Robert Martin"));

  expect(() => library.addBook(new Book("0306406152", "Other", "Someone"))).toThrow("already in the catalog");
});

test("looking up an unknown isbn throws a not found error", () => {
  expect(() => library.getBook("0306406152")).toThrow(new NotFoundError("No book with ISBN 0306406152"));
});

test("registered member can be looked up by id", () => {
  const member = new Member("M001", "Ada Lovelace");

  library.registerMember(member);

  expect(library.getMember("M001")).toBe(member);
});

test("registering an existing member id is rejected", () => {
  library.registerMember(new Member("M001", "Ada Lovelace"));

  expect(() => library.registerMember(new Member("M001", "Grace Hopper"))).toThrow("already registered");
});

test("looking up an unknown member throws a not found error", () => {
  expect(() => library.getMember("M404")).toThrow(new NotFoundError("No member with id M404"));
});

test("borrowBook takes a copy and records it on the member", () => {
  stock();

  library.borrowBook("M001", "0306406152");

  expect([book.availableCopies, member.borrowedBooks]).toEqual([1, ["0306406152"]]);
});
