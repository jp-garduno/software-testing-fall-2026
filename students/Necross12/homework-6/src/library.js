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
    if (this.miembros.some((existente) => existente.id === miembro.id))
      throw new Error("El miembro ya está registrado.");
    this.miembros.push(miembro);
  }
}

module.exports = { Library };
