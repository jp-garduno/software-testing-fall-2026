const { Books } = require("../src/book");

describe("Libro", () => {
  test("(inválida) crear libro con ISBN de 9 dígitos", () => {
    expect(() => new Books("123456789", "Libro de prueba", "Autor")).toThrow(
      "El ISBN debe tener 10 o 13 dígitos",
    );
  });

  test("(inválida) crear libro con ISBN de 11 dígitos", () => {
    expect(() => new Books("12345678901", "Libro de prueba", "Autor")).toThrow(
      "El ISBN debe tener 10 o 13 dígitos",
    );
  });

  test("(inválida) crear libro con ISBN de 14 dígitos", () => {
    expect(
      () => new Books("12345678901234", "Libro de prueba", "Autor"),
    ).toThrow("El ISBN debe tener 10 o 13 dígitos");
  });

  test("(inválida) crear libro con ISBN que contiene letras", () => {
    expect(() => new Books("12345abcde", "Libro de prueba", "Autor")).toThrow(
      "El ISBN debe tener 10 o 13 dígitos",
    );
  });

  test("crear libro con ISBN de 13 dígitos", () => {
    const books = new Books("1234567890123", "Libro de prueba", "Autor");
    expect(books.isbn).toBe("1234567890123");
  });

  test("(inválida) crear libro sin título", () => {
    expect(() => new Books("1234567890", "", "Autor")).toThrow(
      "El título es requerido",
    );
  });

  test("(inválida) crear libro sin autor", () => {
    expect(() => new Books("1234567890", "Libro de prueba", "")).toThrow(
      "El autor es requerido",
    );
  });

  test("tiene 1 copia por defecto", () => {
    const books = new Books("1234567890", "Libro de prueba", "Autor");
    expect(books.copias).toBe(1);
  });

  test("las copias disponibles inician igual a las copias totales", () => {
    const books = new Books("1234567890", "Libro de prueba", "Autor", 5);
    expect(books.copiasDisponibles).toBe(5);
  });

  test("está disponible cuando hay ejemplares", () => {
    const books = new Books("1234567890", "Libro de prueba", "Autor", 1);
    expect(books.estaDisponible()).toBe(true);
  });

  test("(inválida) está disponible cuando tiene 0 copias", () => {
    const books = new Books("1234567890", "Libro de prueba", "Autor", 0);
    expect(books.estaDisponible()).toBe(false);
  });
});

describe("Pedir y devolver un libro", () => {
  let books;

  beforeEach(() => {
    books = new Books("1234567890", "Libro de prueba", "Autor", 3);
  });

  test("pedir un libro reduce las copias disponibles", () => {
    expect(books.pedir()).toBe(true);
    expect(books.copiasDisponibles).toBe(2);
  });

  test("sigue disponible cuando queda al menos una copia", () => {
    books.pedir();
    books.pedir();
    expect(books.estaDisponible()).toBe(true);
  });

  test("no está disponible cuando todas las copias están pedidas", () => {
    books.pedir();
    books.pedir();
    books.pedir();
    expect(books.estaDisponible()).toBe(false);
  });

  test("(inválida) pedir un libro sin copias disponibles", () => {
    books.pedir();
    books.pedir();
    books.pedir();
    expect(() => books.pedir()).toThrow("No hay más libros disponibles");
  });

  test("regresar un libro aumenta las copias disponibles", () => {
    books.pedir();
    expect(books.regresar()).toBe(true);
    expect(books.copiasDisponibles).toBe(3);
  });

  test("(inválida) regresar más libros de los que existen", () => {
    expect(() => books.regresar()).toThrow(
      "No se pueden regresar más libros de los que existen",
    );
  });
});
