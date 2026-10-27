class Library {
  constructor() {
    this.libros = [];
    this.miembros = [];
  }

  agregarLibro(libro) {
    if (this.libros.some((existente) => existente.isbn === libro.isbn))
      throw new Error("El libro ya está registrado.");
    this.libros.push(libro);
  }

  agregarMiembro(miembro) {
    this.miembros.push(miembro);
  }
}

module.exports = { Library };
