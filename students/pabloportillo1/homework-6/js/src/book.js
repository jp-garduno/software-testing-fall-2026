class Book {
  constructor(isbn, title, author, totalCopies = 1) {
    this.isbn = isbn;
    this.title = title;
    this.author = author;
    this.totalCopies = totalCopies;
    this.availableCopies = totalCopies;
  }

  isAvailable() {
    return this.availableCopies > 0;
  }
}

module.exports = { Book };
