class Library {
  constructor() {
    this.books = new Map();
  }

  addBook(book) {
    if (this.books.has(book.isbn)) {
      throw new Error(`ISBN ${book.isbn} is already in the catalog`);
    }
    this.books.set(book.isbn, book);
  }

  getBook(isbn) {
    return this.books.get(isbn);
  }
}

module.exports = { Library };
