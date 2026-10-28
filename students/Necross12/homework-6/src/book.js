const ISBN_VALIDO = /^(\d{10}|\d{13})$/;
class Books {
  constructor(isbn, titulo, autor, copias = 1, disponibles = copias) {
    if (!ISBN_VALIDO.test(isbn))
      throw new Error("El ISBN debe tener 10 o 13 dígitos");

    if (!titulo) throw new Error("El título es requerido");

    if (!autor) throw new Error("El autor es requerido");

    this.isbn = isbn;
    this.titulo = titulo;
    this.autor = autor;
    this.copias = copias;
    this.copiasDisponibles = disponibles;
  }

  estaDisponible() {
    return this.copiasDisponibles > 0;
  }

  pedir() {
    if (!this.estaDisponible())
      throw new Error("No hay más libros disponibles");

    this.copiasDisponibles--;
    return true;
  }

  regresar() {
    if (this.copiasDisponibles >= this.copias)
      throw new Error("No se pueden regresar más libros de los que existen");

    this.copiasDisponibles++;
    return true;
  }
}
module.exports = { Books };
