let siguienteId = 1;
const CATEGORIAS_VALIDAS = ["estudiante", "profesor", "publico"];
class Member {
  constructor(nombre, listaLibros = [], limiteLibros, categoria = "estudiante") {
    if (!nombre)
      throw new Error("El miembro necesita un nombre.");
    if (limiteLibros === undefined)
      limiteLibros = categoria === "profesor" ? 5 : 3;
    if (limiteLibros < 0)
      throw new Error("El miembro no puede tener un límite negativo.");
    if (listaLibros.length > limiteLibros)
      throw new Error("El miembro no puede tener más libros que su límite.");
    if (!CATEGORIAS_VALIDAS.includes(categoria))
      throw new Error("La categoría no es válida.");

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
}

module.exports = { Member };
