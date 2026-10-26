let siguienteId = 1;
class Member {
  constructor(nombre, listaLibros = [], limiteLibros = 3) {
    if (!nombre)
      throw new Error("El miembro necesita un nombre.");
    if (limiteLibros < 0)
      throw new Error("El miembro no puede tener un límite negativo.");
    if (listaLibros.length > limiteLibros)
      throw new Error("El miembro no puede tener más libros que su límite.");

    this.id = siguienteId++;
    this.nombre = nombre;
    this.listaLibros = [...listaLibros];
    this.limiteLibros = limiteLibros;
  }

  puedePedir() {
    return this.listaLibros.length < this.limiteLibros;
  }

  pedir(isbn) {
    if (!isbn) throw new Error("El libro debe tener un identificador.");
    if (!this.puedePedir())
      throw new Error("El miembro no puede tener más libros que su límite.");
    this.listaLibros.push(isbn);
    return true;
  }
}

module.exports = { Member };
