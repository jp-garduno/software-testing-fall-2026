const { Books } = require("../src/book");

describe("Libro: ISBN", () => {
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
});
