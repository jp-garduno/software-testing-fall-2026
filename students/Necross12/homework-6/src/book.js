class Books {
  constructor(isbn, titulo, autor, copias = 1) {
    if (!/^(\d{10}|\d{13})$/.test(isbn)) {
      throw new Error("El ISBN debe tener 10 o 13 dígitos");
    }
    this.isbn = isbn;
  }
}

module.exports = { Books };
