class NotFoundError extends Error {
  constructor(message) {
    super(message);
    this.name = "NotFoundError";
  }
}

class Library {
  #books;

  #members;

  constructor() {
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
  }

  returnBook(memberId, isbn) {
    const member = this.getMember(memberId);
    const book = this.getBook(isbn);
    member.returnBook(isbn);
    book.returnCopy();
  }

  searchByTitle(title) {
    const wanted = title.toLowerCase();
    return [...this.#books.values()].filter((candidate) => candidate.title.toLowerCase().includes(wanted));
  }
}

module.exports = { Library, NotFoundError };
