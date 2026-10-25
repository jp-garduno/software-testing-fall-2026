class Books {
  constructor(isbn, titulo, autor, copias = 1, disponibles = copias) {
    if (!/^(\d{10}|\d{13})$/.test(isbn))
      throw new Error("El ISBN debe tener 10 o 13 dígitos");

    if (!titulo) throw new Error("El título es requerido");

    if (!autor) throw new Error("El autor es requerido");

    this.isbn = isbn;
    this.titulo = titulo;
    this.autor = autor;
    this.copias = copias;
    this.copiasDisponibles = copias;
  }

  estaDisponible() {
    return this.copiasDisponibles > 0;
  }
}
module.exports = { Books };
