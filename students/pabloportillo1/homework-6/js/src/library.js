const { Loan } = require("./loan");

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

  constructor({ clock = () => new Date() } = {}) {
    this.#clock = clock;
    this.#loans = [];
    this.#queues = new Map();
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
    member.addBorrowedBook(isbn);
    book.borrow();
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
  }

  reserveBook(memberId, isbn) {
    const book = this.getBook(isbn);
    if (book.isAvailable()) {
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

  #activeLoan(memberId, isbn) {
    return this.#loans.find((loan) => loan.memberId === memberId && loan.isbn === isbn && loan.returnedOn === null);
  }

  searchByTitle(title) {
    return this.#searchText("title", title);
  }

  searchByAuthor(author) {
    return this.#searchText("author", author);
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
