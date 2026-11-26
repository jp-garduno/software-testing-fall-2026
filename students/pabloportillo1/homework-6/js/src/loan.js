const DAY_MS = 24 * 60 * 60 * 1000;
const LOAN_DAYS = 14;

class Loan {
  constructor(memberId, isbn, borrowedOn) {
    this.memberId = memberId;
    this.isbn = isbn;
    this.borrowedOn = borrowedOn;
    this.dueOn = new Date(borrowedOn.getTime() + LOAN_DAYS * DAY_MS);
    this.returnedOn = null;
  }

  daysOverdue(today) {
    return Math.max(0, Math.round(((this.returnedOn ?? today) - this.dueOn) / DAY_MS));
  }
}

module.exports = { Loan };
