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
