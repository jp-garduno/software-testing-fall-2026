const { Loan } = require("./loan");

function nullsLast(pick, direction) {
  return (a, b) => {
    const left = pick(a);
    const right = pick(b);
    if (left === null || right === null) {
      return Number(left === null) - Number(right === null);
    }
    return direction * (left - right);
  };
}

const SORTERS = {
  title: (a, b) => a.title.localeCompare(b.title),
  year: nullsLast((book) => book.details.year, 1),
  rating: nullsLast((book) => book.details.rating, -1),
};

function matches(details, { genre, year, minRating }) {
  if (genre !== null && details.genre !== genre) {
    return false;
  }
  if (year !== null && details.year !== year) {
    return false;
  }
  return minRating === null || (details.rating !== null && details.rating >= minRating);
}

class NotFoundError extends Error {
  constructor(message) {
    super(message);
    this.name = "NotFoundError";
  }
}

class Library {
  #books;

  #members;

  #clock;

  #loans;

  #queues;

  #notifier;

  #holds;

  constructor({ clock = () => new Date(), notifier = null } = {}) {
    this.#clock = clock;
    this.#notifier = notifier;
    this.#loans = [];
    this.#queues = new Map();
    this.#holds = new Map();
    this.#books = new Map();
    this.#members = new Map();
  }

  addBook(book) {
    if (this.#books.has(book.isbn)) {
      throw new Error(`ISBN ${book.isbn} is already in the catalog`);
    }
    this.#books.set(book.isbn, book);
  }

  getBook(isbn) {
    if (!this.#books.has(isbn)) {
      throw new NotFoundError(`No book with ISBN ${isbn}`);
    }
    return this.#books.get(isbn);
  }

  registerMember(member) {
    if (this.#members.has(member.memberId)) {
      throw new Error(`Member ${member.memberId} is already registered`);
    }
    this.#members.set(member.memberId, member);
  }

  getMember(memberId) {
    if (!this.#members.has(memberId)) {
      throw new NotFoundError(`No member with id ${memberId}`);
    }
    return this.#members.get(memberId);
  }

  borrowBook(memberId, isbn) {
    const member = this.getMember(memberId);
    const book = this.getBook(isbn);
    book.ensureAvailable();
    const held = this.#holds.get(isbn) ?? [];
    if (!held.includes(memberId) && this.#freeCopies(book) === 0) {
      throw new Error(`The copy of '${book.title}' is held for another member`);
    }
    member.addBorrowedBook(isbn);
    book.borrow();
    this.#holds.set(
      isbn,
      held.filter((holder) => holder !== memberId),
    );
    const loan = new Loan(memberId, isbn, this.#clock());
    this.#loans.push(loan);
    return loan;
  }

  calculateLateFees(memberId) {
    const rate = this.getMember(memberId).category.dailyLateFeeCents;
    const today = this.#clock();
    return this.#loans
      .filter((loan) => loan.memberId === memberId)
      .reduce((total, loan) => total + loan.daysOverdue(today) * rate, 0);
  }

  returnBook(memberId, isbn) {
    const member = this.getMember(memberId);
    const book = this.getBook(isbn);
    member.returnBook(isbn);
    book.returnCopy();
    this.#activeLoan(memberId, isbn).returnedOn = this.#clock();
    this.#holdForNextReserver(book);
  }

  #holdForNextReserver(book) {
    const queue = this.#queues.get(book.isbn) ?? [];
    if (queue.length === 0) {
      return;
    }
    const nextMemberId = queue.shift();
    this.#holds.set(book.isbn, [...(this.#holds.get(book.isbn) ?? []), nextMemberId]);
    if (this.#notifier !== null) {
      this.#notifier.notifyAvailable(this.getMember(nextMemberId), book);
    }
  }

  reserveBook(memberId, isbn) {
    this.getMember(memberId);
    const book = this.getBook(isbn);
    if (this.#freeCopies(book) > 0) {
      throw new Error(`'${book.title}' is available, borrow it instead`);
    }
    if (!this.#queues.has(isbn)) {
      this.#queues.set(isbn, []);
    }
    const queue = this.#queues.get(isbn);
    if (queue.includes(memberId)) {
      throw new Error(`${memberId} has already reserved '${book.title}'`);
    }
    queue.push(memberId);
  }

  reservationsFor(isbn) {
    return [...(this.#queues.get(isbn) ?? [])];
  }

  memberHistory(memberId) {
    this.getMember(memberId);
    return this.#loans.filter((loan) => loan.memberId === memberId);
  }

  mostBorrowedBook() {
    const counts = new Map();
    this.#loans.forEach((loan) => counts.set(loan.isbn, (counts.get(loan.isbn) ?? 0) + 1));
    if (counts.size === 0) {
      return null;
    }
    const ranked = [...counts.keys()]
      .map((isbn) => this.#books.get(isbn))
      .sort((a, b) => counts.get(b.isbn) - counts.get(a.isbn) || a.title.localeCompare(b.title));
    return ranked[0];
  }

  borrowStatistics() {
    const returns = this.#loans.filter((loan) => loan.returnedOn !== null).length;
    return { totalBorrows: this.#loans.length, returns, activeLoans: this.#loans.length - returns };
  }

  #freeCopies(book) {
    return book.availableCopies - (this.#holds.get(book.isbn) ?? []).length;
  }

  #activeLoan(memberId, isbn) {
    return this.#loans.find((loan) => loan.memberId === memberId && loan.isbn === isbn && loan.returnedOn === null);
  }

  searchByTitle(title) {
    return this.#searchText("title", title);
  }

  searchByAuthor(author) {
    return this.#searchText("author", author);
  }

  search({ genre = null, year = null, minRating = null, sortBy = "title" } = {}) {
    const found = [...this.#books.values()].filter((book) => matches(book.details, { genre, year, minRating }));
    if (!(sortBy in SORTERS)) {
      throw new Error(`Cannot sort by '${sortBy}'`);
    }
    return found.sort(SORTERS[sortBy]);
  }

  getAvailableBooks() {
    return [...this.#books.values()].filter((candidate) => candidate.isAvailable());
  }

  #searchText(field, text) {
    const wanted = text.toLowerCase();
    return [...this.#books.values()].filter((candidate) => candidate[field].toLowerCase().includes(wanted));
  }
}

module.exports = { Library, NotFoundError };
