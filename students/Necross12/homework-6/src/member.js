class Member {
  constructor(nombre) {
    if (!nombre)
      throw new Error("El miembro necesita un nombre.");
    this.id = siguienteId++;
    this.nombre = nombre;
  }
}

module.exports = { Member };
