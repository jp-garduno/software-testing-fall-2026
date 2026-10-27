class Member {
  constructor(memberId, name) {
    this.memberId = memberId;
    this.name = name;
    this.borrowedBooks = [];
  }
}

module.exports = { Member };
