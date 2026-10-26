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
});
