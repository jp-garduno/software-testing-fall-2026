const { Member } = require("../src/member");

const ISBNS = ["0306406152", "0131103628", "0201633612"];
let member;

beforeEach(() => {
  member = new Member("M001", "Ada Lovelace");
});

test("member is created with id, name and no borrowed books", () => {
  expect([member.memberId, member.name, member.borrowedBooks]).toEqual(["M001", "Ada Lovelace", []]);
});
