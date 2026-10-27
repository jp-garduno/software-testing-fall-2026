const { Library } = require("../src/library");
const { Books } = require("../src/book");
const { Member } = require("../src/member");
/*
add_book(book)- Añadir libro al catálogo
register_member(member)- Registrar nuevo miembro
borrow_book(member_id, isbn)- Pedir prestado un libro
return_book(member_id, isbn)- Devuelve un libro
search_by_title(title)- Buscar libros
search_by_author(author)- Buscar libros
get_available_books()- Lista de libros disponibles

Supongo que debe que usar las 2 clases anteriores
Lista de libros y lista de miembros
 */

describe("Biblioteca", () => {
  let biblioteca, principito, corte, harry, pepe, gon;

  beforeEach(() => {
    biblioteca = new Library();
    principito = new Books(
      "1111111111",
      "El principito",
      "Antoine de Saint-Exupéry",
    );
    corte = new Books(
      "2222222222",
      "Una corte de rosas y espinas",
      "Sarah J. Maas",
    );
    harry = new Books("3333333333", "Harry Potter", "J. K. Rowling");
    pepe = new Member("Pepe");
    gon = new Member("Gon");
  });

  // funciones iniciales
    test("inicia sin libros ni miembros", () => {
      expect(biblioteca.libros).toEqual([]);
      expect(biblioteca.miembros).toEqual([]);
    });

  test("agregar libro al catálogo", () => {
    biblioteca.agregarLibro(principito);
    expect(biblioteca.libros).toEqual([principito]);
  });

  test("(inválida) agregar un libro con ISBN ya registrado", () => {
    biblioteca.agregarLibro(principito);
    expect(() => biblioteca.agregarLibro(principito)).toThrow(
      "El libro ya está registrado.",
    );
  });

  test("registrar miembro", () => {
    biblioteca.agregarMiembro(pepe);
    expect(biblioteca.miembros).toEqual([pepe]);
  });

  test("(inválida) registrar al mismo miembro dos veces", () => {
    biblioteca.agregarMiembro(pepe);
    expect(() => biblioteca.agregarMiembro(pepe)).toThrow(
      "El miembro ya está registrado.",
    );
  });

  // funciones especiales
  test("pedir libro de forma correcta", () => {
    biblioteca.agregarMiembro(pepe);
    biblioteca.agregarLibro(corte);
    expect(biblioteca.pedirLibro(pepe.id, corte.isbn)).toBe(true);
    expect(pepe.listaLibros).toEqual([corte.isbn]);
    expect(corte.copiasDisponibles).toBe(0);
  });

  test("(inválida) pedir con un miembro no registrado", () => {
    biblioteca.agregarLibro(corte);
    expect(() => biblioteca.pedirLibro(pepe.id, corte.isbn)).toThrow(
      "El miembro no está registrado.",
    );
  });

  test("(inválida) pedir un libro no registrado", () => {
    biblioteca.agregarMiembro(pepe);
    expect(() => biblioteca.pedirLibro(pepe.id, "9999999999")).toThrow(
      "El libro no está registrado.",
    );
  });

  test("(inválida) pedir un libro sin copias disponibles", () => {
    biblioteca.agregarMiembro(pepe);
    biblioteca.agregarMiembro(gon);
    biblioteca.agregarLibro(harry);
    biblioteca.pedirLibro(gon.id, harry.isbn);
    expect(() => biblioteca.pedirLibro(pepe.id, harry.isbn)).toThrow(
      "No hay más libros disponibles",
    );
  });

  test("(inválida) pedir superando el límite del miembro no descuenta la copia", () => {
    const lector = new Member("Lector", [], 1);
    biblioteca.agregarMiembro(lector);
    biblioteca.agregarLibro(principito);
    biblioteca.agregarLibro(corte);
    biblioteca.pedirLibro(lector.id, principito.isbn);

    expect(() => biblioteca.pedirLibro(lector.id, corte.isbn)).toThrow(
      "El miembro no puede tener más libros que su límite.",
    );
    expect(corte.copiasDisponibles).toBe(1);
  });
});
