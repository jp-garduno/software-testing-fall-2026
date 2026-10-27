const { Member, MemberCategory } = require("../src/member");

const ISBNS = ["0306406152", "0131103628", "0201633612"];
let member;

beforeEach(() => {
  member = new Member("M001", "Ada Lovelace");
});

test("member is created with id, name and no borrowed books", () => {
  expect([member.memberId, member.name, member.borrowedBooks]).toEqual(["M001", "Ada Lovelace", []]);
});

test("member is a student with a borrow limit of three by default", () => {
  expect([member.category, member.maxBorrowLimit]).toEqual([MemberCategory.STUDENT, 3]);
});

test.each([
  ["FACULTY", 5],
  ["PUBLIC", 2],
])("%s member can borrow %i books", (category, limit) => {
  expect(new Member("X001", "Someone", MemberCategory[category]).maxBorrowLimit).toBe(limit);
});

test("new member can borrow", () => {
  expect(member.canBorrow()).toBe(true);
});

test("addBorrowedBook records the isbn", () => {
  member.addBorrowedBook(ISBNS[0]);

  expect(member.borrowedBooks).toEqual([ISBNS[0]]);
});

test("member at the limit cannot borrow and adding another book is rejected", () => {
  ISBNS.forEach((isbn) => member.addBorrowedBook(isbn));

  expect(() => member.addBorrowedBook("0596007124")).toThrow("Ada Lovelace has reached the borrow limit of 3");
});

test("adding the same book twice is rejected", () => {
  member.addBorrowedBook(ISBNS[0]);

  expect(() => member.addBorrowedBook(ISBNS[0])).toThrow("already borrowed");
});

test("returnBook removes the isbn", () => {
  member.addBorrowedBook(ISBNS[0]);

  member.returnBook(ISBNS[0]);

  expect(member.borrowedBooks).toEqual([]);
});
