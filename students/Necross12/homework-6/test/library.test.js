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

  describe("creación", () => {
    test("inicia sin libros ni miembros", () => {
      expect(biblioteca.libros).toEqual([]);
      expect(biblioteca.miembros).toEqual([]);
    });
  });

  test("agregar libro al catálogo", () => {
    biblioteca.agregarLibro(principito);
    expect(biblioteca.libros).toEqual([principito]);
  });
});
