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
