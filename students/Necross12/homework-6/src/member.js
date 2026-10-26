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
}

module.exports = { Member };
