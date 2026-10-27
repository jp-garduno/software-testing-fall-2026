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
