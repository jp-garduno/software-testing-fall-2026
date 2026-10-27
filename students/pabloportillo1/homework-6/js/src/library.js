class NotFoundError extends Error {
  constructor(message) {
    super(message);
    this.name = "NotFoundError";
  }
}

class Library {
  constructor() {
    this.books = new Map();
    this.members = new Map();
  }

  addBook(book) {
    if (this.books.has(book.isbn)) {
      throw new Error(`ISBN ${book.isbn} is already in the catalog`);
    }
    this.books.set(book.isbn, book);
  }

  getBook(isbn) {
    if (!this.books.has(isbn)) {
      throw new NotFoundError(`No book with ISBN ${isbn}`);
    }
    return this.books.get(isbn);
  }

  registerMember(member) {
    this.members.set(member.memberId, member);
  }

  getMember(memberId) {
    return this.members.get(memberId);
  }
}

module.exports = { Library, NotFoundError };
