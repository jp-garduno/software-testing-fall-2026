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
});
