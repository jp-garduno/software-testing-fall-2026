const { Book } = require("../src/book");
const { Library, NotFoundError } = require("../src/library");
const { Member } = require("../src/member");

const ISBN = "0306406152";
let notifier;
let library;

beforeEach(() => {
  notifier = { notifyAvailable: jest.fn() };
  library = new Library({ notifier });
  library.addBook(new Book(ISBN, "Clean Code", "Robert Martin", 1));
  ["M001", "M002", "M003"].forEach((memberId) => library.registerMember(new Member(memberId, `Member ${memberId}`)));
});

test("reserving a book with no copy left queues the member", () => {
  library.borrowBook("M001", ISBN);

  library.reserveBook("M002", ISBN);

  expect(library.reservationsFor(ISBN)).toEqual(["M002"]);
});

test("reserving a book on the shelf is rejected", () => {
  expect(() => library.reserveBook("M002", ISBN)).toThrow("is available, borrow it instead");
});

test("reserving the same book twice is rejected", () => {
  library.borrowBook("M001", ISBN);
  library.reserveBook("M002", ISBN);

  expect(() => library.reserveBook("M002", ISBN)).toThrow("already reserved");
});

test("reservation by an unknown member is rejected", () => {
  library.borrowBook("M001", ISBN);

  expect(() => library.reserveBook("M404", ISBN)).toThrow(NotFoundError);
});

test("returning a reserved book notifies the first member in line", () => {
  library.borrowBook("M001", ISBN);
  library.reserveBook("M002", ISBN);

  library.returnBook("M001", ISBN);

  expect(notifier.notifyAvailable).toHaveBeenCalledWith(library.getMember("M002"), library.getBook(ISBN));
});

test("reservations are served first come first served", () => {
  library.borrowBook("M001", ISBN);
  library.reserveBook("M002", ISBN);
  library.reserveBook("M003", ISBN);
  library.returnBook("M001", ISBN);
  library.borrowBook("M002", ISBN);

  library.returnBook("M002", ISBN);

  expect(notifier.notifyAvailable).toHaveBeenLastCalledWith(library.getMember("M003"), library.getBook(ISBN));
});

test("copy held for a reserver cannot be borrowed by someone else", () => {
  library.borrowBook("M001", ISBN);
  library.reserveBook("M002", ISBN);
  library.returnBook("M001", ISBN);

  expect(() => library.borrowBook("M003", ISBN)).toThrow("held for another member");
});

test("hold is released once the reserver borrows the copy", () => {
  library.borrowBook("M001", ISBN);
  library.reserveBook("M002", ISBN);
  library.returnBook("M001", ISBN);
  library.borrowBook("M002", ISBN);
  library.returnBook("M002", ISBN);

  library.borrowBook("M003", ISBN);

  expect(library.getMember("M003").borrowedBooks).toEqual([ISBN]);
});

test("book whose only copy is held can still be reserved", () => {
  library.borrowBook("M001", ISBN);
  library.reserveBook("M002", ISBN);
  library.returnBook("M001", ISBN);

  library.reserveBook("M003", ISBN);

  expect(library.reservationsFor(ISBN)).toEqual(["M003"]);
});

test("copy is held even without a notifier", () => {
  const quiet = new Library();
  quiet.addBook(new Book(ISBN, "Clean Code", "Robert Martin", 1));
  ["M001", "M002", "M003"].forEach((memberId) => quiet.registerMember(new Member(memberId, `Member ${memberId}`)));
  quiet.borrowBook("M001", ISBN);
  quiet.reserveBook("M002", ISBN);
  quiet.returnBook("M001", ISBN);

  expect(() => quiet.borrowBook("M003", ISBN)).toThrow("held for another member");
});

test("book nobody reserved has an empty queue", () => {
  expect(library.reservationsFor(ISBN)).toEqual([]);
});

test("two returned copies are held for the first two reservers", () => {
  library.addBook(new Book("0131103628", "The C Programming Language", "Brian Kernighan", 2));
  ["M004", "M005"].forEach((memberId) => library.registerMember(new Member(memberId, `Member ${memberId}`)));
  library.borrowBook("M001", "0131103628");
  library.borrowBook("M002", "0131103628");
  library.reserveBook("M003", "0131103628");
  library.reserveBook("M004", "0131103628");
  library.returnBook("M001", "0131103628");
  library.returnBook("M002", "0131103628");

  expect(() => library.borrowBook("M005", "0131103628")).toThrow("held for another member");
});
