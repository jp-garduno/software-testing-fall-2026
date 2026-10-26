const { Member } = require("../src/member");

describe("Miembro: creación", () => {
  test("crear miembro con nombre", () => {
    const miembro = new Member("Carlos");
    expect(miembro.nombre).toBe("Carlos");
  });

  test("(inválida) crear miembro sin nombre", () => {
    expect(() => new Member("")).toThrow("El miembro necesita un nombre.");
  });
});
