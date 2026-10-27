const { Book } = require("../src/book");
const { Library } = require("../src/library");
const { Member, MemberCategory } = require("../src/member");
const { FakeClock } = require("./fakeClock");

const ISBN = "0306406152";
let clock;
let library;

beforeEach(() => {
  clock = new FakeClock();
  library = new Library({ clock: clock.now });
  library.addBook(new Book(ISBN, "Clean Code", "Robert Martin", 2));
  library.registerMember(new Member("M001", "Ada Lovelace"));
  library.registerMember(new Member("M002", "Grace Hopper"));
});

test("loan is due fourteen days after borrowing", () => {
  const loan = library.borrowBook("M001", ISBN);

  expect(loan.dueOn).toEqual(new Date("2026-10-15T00:00:00Z"));
});
