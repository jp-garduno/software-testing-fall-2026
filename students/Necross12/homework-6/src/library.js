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

  pedirLibro(idMiembro, isbn) {
    const miembro = this.miembros.find((m) => m.id === idMiembro);
    const libro = this.libros.find((l) => l.isbn === isbn);
    if (!miembro)
      throw new Error("El miembro no está registrado.");
    if (!libro)
      throw new Error("El libro no está registrado.");
    if (!miembro.puedePedir())
      throw new Error("El miembro no puede tener más libros que su límite.");
    libro.pedir();
    miembro.pedir(isbn);
    return true;
  }
}

module.exports = { Library };
