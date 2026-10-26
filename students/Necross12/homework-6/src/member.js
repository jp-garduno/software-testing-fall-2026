let siguienteId = 1;
class Member {
  constructor(nombre, listaLibros = [], limiteLibros = 3) {
    if (!nombre)
      throw new Error("El miembro necesita un nombre.");
    this.id = siguienteId++;
    this.nombre = nombre;
    this.listaLibros = [...listaLibros];
    this.limiteLibros = limiteLibros;
  }

  if (limiteLibros < 0)
    throw new Error("El miembro no puede tener un límite negativo.");

  if (listaLibros.length > limiteLibros)
    throw new Error("El miembro no puede tener más libros que su límite.");
}

module.exports = { Member };
