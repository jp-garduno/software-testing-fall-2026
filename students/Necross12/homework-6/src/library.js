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

  obtenerMiembroRegistrado(id) {
    const miembro = this.miembros.find((m) => m.id === id);
    if (!miembro) throw new Error("El miembro no está registrado.");
    return miembro;
  }

  obtenerLibroRegistrado(isbn) {
    const libro = this.libros.find((l) => l.isbn === isbn);
    if (!libro) throw new Error("El libro no está registrado.");
    return libro;
  }

  pedirLibro(idMiembro, isbn) {
    const miembro = this.obtenerMiembroRegistrado(idMiembro);
    const libro = this.obtenerLibroRegistrado(isbn);
    if (!miembro.puedePedir())
      throw new Error("El miembro no puede tener más libros que su límite.");
    libro.pedir();
    miembro.pedir(isbn);
    return true;
  }

  regresarLibro(idMiembro, isbn) {
    const miembro = this.obtenerMiembroRegistrado(idMiembro);
    const libro = this.obtenerLibroRegistrado(isbn);
    miembro.regresar(isbn);
    libro.regresar();
    return true;
  }
}

module.exports = { Library };
