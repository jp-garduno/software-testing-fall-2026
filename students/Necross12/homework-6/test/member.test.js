const { Member } = require("../src/member");

describe("Miembro: creación", () => {
  test("crear miembro con nombre", () => {
    const miembro = new Member("Carlos");
    expect(miembro.nombre).toBe("Carlos");
  });

  test("(inválida) crear miembro sin nombre", () => {
    expect(() => new Member("")).toThrow("El miembro necesita un nombre.");
  });

  test("asigna ids incrementales", () => {
    const primero = new Member("Carlos");
    const segundo = new Member("Ana");
    expect(segundo.id).toBe(primero.id + 1);
  });

  test("inicia con lista vacía y límite de 3", () => {
    const miembro = new Member("Carlos");
    expect(miembro.listaLibros).toEqual([]);
    expect(miembro.limiteLibros).toBe(3);
  });

  test("crear con lista de libros y límite", () => {
    const miembro = new Member("Carlos", ["1234567890"], 2);
    expect(miembro.listaLibros).toEqual(["1234567890"]);
    expect(miembro.limiteLibros).toBe(2);
  });

  test("(inválida) crear miembro con límite negativo", () => {
    expect(() => new Member("Carlos", ["1234567890"], -1)).toThrow(
      "El miembro no puede tener un límite negativo.",
    );
  });

  test("(inválida) crear miembro con más libros que su límite", () => {
    expect(() => new Member("Carlos", ["1234567890", "0987654321"], 1)).toThrow(
      "El miembro no puede tener más libros que su límite.",
    );
  });
});

describe("Miembro: pedir y regresar", () => {
  let miembro;

  beforeEach(() => {
    miembro = new Member("Carlos", ["1234567890"], 2);
  });

  test("puede pedir cuando no ha llegado a su límite", () => {
    expect(miembro.puedePedir()).toBe(true);
  });

  test("no puede pedir cuando llegó a su límite", () => {
    miembro.pedir("0987654321");
    expect(miembro.puedePedir()).toBe(false);
  });

  test("pedir agrega el libro a la lista", () => {
    expect(miembro.pedir("0987654321")).toBe(true);
    expect(miembro.listaLibros).toEqual(["1234567890", "0987654321"]);
  });

  test("(inválida) pedir un libro superando el límite", () => {
    miembro.pedir("0987654321");
    expect(() => miembro.pedir("1111111111")).toThrow(
      "El miembro no puede tener más libros que su límite.",
    );
  });

  test("(inválida) pedir un libro sin identificador", () => {
    expect(() => miembro.pedir("")).toThrow(
      "El libro debe tener un identificador.",
    );
  });

  test("regresar quita el libro de la lista", () => {
    expect(miembro.regresar("1234567890")).toBe(true);
    expect(miembro.listaLibros).toEqual([]);
  });

  test("(inválida) regresar un libro que no tiene", () => {
    expect(() => miembro.regresar("0987654321")).toThrow(
      "No puedes regresar un libro que no tienes.",
    );
  });
});

describe("Miembro: categorías", () => {
  test("la categoría por defecto es estudiante", () => {
    expect(new Member("Carlos").categoria).toBe("estudiante");
  });

  test("(inválida) crear miembro con categoría inexistente", () => {
  expect(() => new Member("Carlos", [], 3, "vip")).toThrow(
    "La categoría no es válida.",
  );
});

test("el profesor tiene límite de 5 libros", () => {
  expect(new Member("Laura", [], undefined, "profesor").limiteLibros).toBe(5);
});

});
