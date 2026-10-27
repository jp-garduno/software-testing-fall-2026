const MemberCategory = Object.freeze({
  STUDENT: Object.freeze({ name: "STUDENT", borrowLimit: 3, dailyLateFeeCents: 100 }),
});

class Member {
  constructor(memberId, name, category = MemberCategory.STUDENT) {
    this.memberId = memberId;
    this.name = name;
    this.category = category;
    this.maxBorrowLimit = category.borrowLimit;
    this.borrowedBooks = [];
  }
}

module.exports = { Member, MemberCategory };
