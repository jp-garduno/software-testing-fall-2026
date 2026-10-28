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

    test("regresar libro de forma correcta", () => {
      biblioteca.agregarMiembro(pepe);
      biblioteca.agregarLibro(corte);
      biblioteca.pedirLibro(pepe.id, corte.isbn);

      expect(biblioteca.regresarLibro(pepe.id, corte.isbn)).toBe(true);
      expect(pepe.listaLibros).toEqual([]);
      expect(corte.copiasDisponibles).toBe(1);
    });

  test("(inválida) regresar un libro que el miembro no tiene", () => {
    biblioteca.agregarMiembro(pepe);
    biblioteca.agregarLibro(corte);
    expect(() => biblioteca.regresarLibro(pepe.id, corte.isbn)).toThrow(
      "No puedes regresar un libro que no tienes.",
    );
  });

  test("(inválida) regresar con un miembro no registrado", () => {
    biblioteca.agregarLibro(corte);
    expect(() => biblioteca.regresarLibro(pepe.id, corte.isbn)).toThrow(
      "El miembro no está registrado.",
    );
  });

  test("(inválida) regresar un libro no registrado", () => {
    biblioteca.agregarMiembro(pepe);
    expect(() => biblioteca.regresarLibro(pepe.id, "9999999999")).toThrow(
      "El libro no está registrado.",
    );
  });

  test("buscar por título devuelve los libros que coinciden", () => {
    biblioteca.agregarLibro(harry);
    expect(biblioteca.buscarPorTitulo("Harry")).toEqual([harry]);
  });

  test("(inválida) buscar por un título que no existe", () => {
    expect(biblioteca.buscarPorTitulo("Dune")).toEqual([]);
  });

  test("buscar por título sin distinguir mayúsculas ni coincidencia parcial", () => {
    biblioteca.agregarLibro(principito);
    expect(biblioteca.buscarPorTitulo("principito")).toEqual([principito]);
  });

  test("buscar por autor devuelve los libros que coinciden", () => {
    biblioteca.agregarLibro(harry);
    expect(biblioteca.buscarPorAutor("rowling")).toEqual([harry]);
  });

  test("(inválida) buscar por un autor que no existe", () => {
    expect(biblioteca.buscarPorAutor("Tolkien")).toEqual([]);
  });

  test("(inválida) lista vacía cuando no hay libros", () => {
    expect(biblioteca.librosDisponibles()).toEqual([]);
  });

  test("lista todos los libros cuando hay copias", () => {
    biblioteca.agregarLibro(principito);
    biblioteca.agregarLibro(harry);
    expect(biblioteca.librosDisponibles()).toEqual([principito, harry]);
  });

  test("no incluye los libros con todas las copias prestadas", () => {
    biblioteca.agregarMiembro(pepe);
    biblioteca.agregarLibro(principito);
    biblioteca.agregarLibro(harry);
    biblioteca.pedirLibro(pepe.id, harry.isbn);
    expect(biblioteca.librosDisponibles()).toEqual([principito]);
  });
});

describe("Biblioteca: reservas", () => {
    let biblioteca, principito, harry, pepe, gon, ana;

    beforeEach(() => {
        biblioteca = new Library();
        principito = new Books("1111111111", "El principito", "Antoine de Saint-Exupéry");
        harry = new Books("3333333333", "Harry Potter", "J. K. Rowling");
        pepe = new Member("Pepe");
        gon = new Member("Gon");
        ana = new Member("Ana");
        [pepe, gon, ana].forEach((m) => biblioteca.agregarMiembro(m));
        [principito, harry].forEach((l) => biblioteca.agregarLibro(l));
        biblioteca.pedirLibro(gon.id, principito.isbn); // agota la única copia
    });

    test("reservar un libro sin copias devuelve la posición en la cola", () => {
        expect(biblioteca.reservarLibro(pepe.id, principito.isbn)).toBe(1);
    });

    test("las reservas respetan el orden de llegada (FIFO)", () => {
        biblioteca.reservarLibro(pepe.id, principito.isbn);
        biblioteca.reservarLibro(ana.id, principito.isbn);
        expect(biblioteca.obtenerReservas(principito.isbn)).toEqual([pepe.id, ana.id]);
    });

    test("(inválida) reservar un libro que tiene copias disponibles", () => {
        expect(() => biblioteca.reservarLibro(pepe.id, harry.isbn)).toThrow(
            "El libro está disponible, no necesita reserva.",
        );
    });

    test("(inválida) reservar dos veces el mismo libro", () => {
        biblioteca.reservarLibro(pepe.id, principito.isbn);
        expect(() => biblioteca.reservarLibro(pepe.id, principito.isbn)).toThrow(
            "El miembro ya tiene una reserva para este libro.",
        );
    });

    test("al devolver un libro se notifica al primero de la cola", () => {
        biblioteca.reservarLibro(pepe.id, principito.isbn);
        biblioteca.reservarLibro(ana.id, principito.isbn);
        biblioteca.regresarLibro(gon.id, principito.isbn);
        expect(pepe.notificaciones).toEqual(['El libro "El principito" ya está disponible.']);
    });

    test("(inválida) pedir un libro reservado por otro miembro", () => {
        biblioteca.reservarLibro(pepe.id, principito.isbn);
        biblioteca.regresarLibro(gon.id, principito.isbn);
        expect(() => biblioteca.pedirLibro(ana.id, principito.isbn)).toThrow(
            "El libro está reservado para otro miembro.",
        );
    });

    test("quien reservó primero puede pedir el libro y sale de la cola", () => {
        biblioteca.reservarLibro(pepe.id, principito.isbn);
        biblioteca.regresarLibro(gon.id, principito.isbn);
        biblioteca.pedirLibro(pepe.id, principito.isbn);
        expect(biblioteca.obtenerReservas(principito.isbn)).toEqual([]);
    });
});

describe("Biblioteca: recargos por retraso", () => {
    const fechaPrestamo = new Date("2026-10-01T00:00:00Z");
    let biblioteca, corte, harry, pepe, laura;

    beforeEach(() => {
        biblioteca = new Library();
        corte = new Books("2222222222", "Una corte de rosas y espinas", "Sarah J. Maas");
        harry = new Books("3333333333", "Harry Potter", "J. K. Rowling");
        pepe = new Member("Pepe");
        laura = new Member("Laura", [], undefined, "profesor");
        [pepe, laura].forEach((m) => biblioteca.agregarMiembro(m));
        [corte, harry].forEach((l) => biblioteca.agregarLibro(l));
    });

    test("el libro vence 14 días después del préstamo", () => {
        biblioteca.pedirLibro(pepe.id, corte.isbn, fechaPrestamo);
        expect(biblioteca.fechaVencimiento(pepe.id, corte.isbn)).toEqual(
            new Date("2026-10-15T00:00:00Z"),
        );
    });

    test("(inválida) consultar vencimiento de un libro que el miembro no pidió", () => {
        expect(() => biblioteca.fechaVencimiento(pepe.id, corte.isbn)).toThrow(
            "El miembro no tiene prestado este libro.",
        );
    });

    test("no hay recargo el día de vencimiento", () => {
        biblioteca.pedirLibro(pepe.id, corte.isbn, fechaPrestamo);
        expect(
            biblioteca.calcularRecargo(pepe.id, corte.isbn, new Date("2026-10-15T00:00:00Z")),
        ).toBe(0);
    });
});
