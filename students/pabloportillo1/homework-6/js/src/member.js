const MemberCategory = Object.freeze({
  STUDENT: Object.freeze({ name: "STUDENT", borrowLimit: 3, dailyLateFeeCents: 100 }),
  FACULTY: Object.freeze({ name: "FACULTY", borrowLimit: 5, dailyLateFeeCents: 50 }),
  PUBLIC: Object.freeze({ name: "PUBLIC", borrowLimit: 2, dailyLateFeeCents: 150 }),
});

class Member {
  constructor(memberId, name, category = MemberCategory.STUDENT) {
    this.memberId = memberId;
    this.name = name;
    this.category = category;
    this.maxBorrowLimit = category.borrowLimit;
    this.borrowedBooks = [];
  }

  canBorrow() {
    return this.borrowedBooks.length < this.maxBorrowLimit;
  }

  addBorrowedBook(isbn) {
    if (!this.canBorrow()) {
      throw new Error(`${this.name} has reached the borrow limit of ${this.maxBorrowLimit}`);
    }
    this.borrowedBooks.push(isbn);
  }
}

module.exports = { Member, MemberCategory };
