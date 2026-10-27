const ISBN_PATTERN = /^(\d{10}|\d{13})$/;

function validate(isbn, title, totalCopies) {
  if (!ISBN_PATTERN.test(isbn)) {
    throw new Error("ISBN must be 10 or 13 digits");
  }
  if (!title.trim()) {
    throw new Error("Title is required");
  }
  if (totalCopies < 0) {
    throw new Error("Total copies cannot be negative");
  }
}

class BookDetails {
  constructor({ genre = null, year = null, rating = null } = {}) {
    this.genre = genre;
    this.year = year;
    this.rating = rating;
    Object.freeze(this);
  }
}

class Book {
  constructor(isbn, title, author, totalCopies = 1, details = new BookDetails()) {
    validate(isbn, title, totalCopies);
    this.details = details;
    this.isbn = isbn;
    this.title = title;
    this.author = author;
    this.totalCopies = totalCopies;
    this.availableCopies = totalCopies;
  }

  isAvailable() {
    return this.availableCopies > 0;
  }

  ensureAvailable() {
    if (!this.isAvailable()) {
      throw new Error(`No copies available for '${this.title}'`);
    }
  }

  borrow() {
    this.ensureAvailable();
    this.availableCopies -= 1;
  }

  returnCopy() {
    if (this.availableCopies === this.totalCopies) {
      throw new Error(`All copies of '${this.title}' are already in`);
    }
    this.availableCopies += 1;
  }
}

module.exports = { Book, BookDetails };
