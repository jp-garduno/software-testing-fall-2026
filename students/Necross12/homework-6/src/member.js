let siguienteId = 1;
const CATEGORIAS = {
  estudiante: { limite: 3, tarifaRecargo: 1 },
  profesor: { limite: 5, tarifaRecargo: 0.5 },
  publico: { limite: 2, tarifaRecargo: 2 },
};

class Member {
  constructor(
    nombre,
    listaLibros = [],
    limiteLibros,
    categoria = "estudiante",
  ) {
    if (!nombre) throw new Error("El miembro necesita un nombre.");
    if (!Object.hasOwn(CATEGORIAS, categoria))
      throw new Error("La categoría no es válida.");
    if (limiteLibros === undefined)
      limiteLibros = CATEGORIAS[categoria].limite;
    if (limiteLibros < 0)
      throw new Error("El miembro no puede tener un límite negativo.");
    if (listaLibros.length > limiteLibros)
      throw new Error("El miembro no puede tener más libros que su límite.");

    this.id = siguienteId++;
    this.nombre = nombre;
    this.listaLibros = [...listaLibros];
    this.limiteLibros = limiteLibros;
    this.categoria = categoria;
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

  regresar(isbn) {
    const posicion = this.listaLibros.indexOf(isbn);
    if (posicion === -1)
      throw new Error("No puedes regresar un libro que no tienes.");
    this.listaLibros.splice(posicion, 1);
    return true;
  }

  get tarifaRecargo() {
    return CATEGORIAS[this.categoria].tarifaRecargo;
  }
}

module.exports = { Member };
