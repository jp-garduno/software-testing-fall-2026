const path = require("path");
const {
  Customer,
  PhoneNumber,
  Address,
  CreditCard,
  luhn,
} = require("../src/customerValidator");
const cases = require("../test_data/customerValidation.json");

// Fecha fija para que las pruebas de expiracion no dependan del dia en que se corren
const AHORA = new Date(2026, 10, 11);

describe("Validacion de clientes (data-driven, customerValidation.json)", () => {
  test("el JSON cumple los minimos de la tarea", () => {
    expect(cases.length).toBeGreaterThanOrEqual(30);
    const por = (cat) => cases.filter((c) => c.category === cat).length;
    expect(por("valido")).toBeGreaterThanOrEqual(3);
    expect(por("email invalido")).toBeGreaterThanOrEqual(4);
    expect(por("telefono invalido")).toBeGreaterThanOrEqual(4);
    expect(por("direccion invalida")).toBeGreaterThanOrEqual(5);
    expect(por("tarjeta invalida")).toBeGreaterThanOrEqual(8);
    expect(por("errores multiples")).toBeGreaterThanOrEqual(6);
  });

  test.each(cases.map((c) => [c.test_name, c]))("%s", (_nombre, caso) => {
    const resultado = Customer.fromJSON(caso.customer).validate(AHORA);
    expect(resultado.is_valid).toBe(caso.expected.is_valid);
    expect(resultado.errors).toEqual(caso.expected.errors);
  });
});

describe("Casos extra de estructura", () => {
  test("cliente sin datos devuelve todos los errores sin lanzar excepcion", () => {
    const r = Customer.fromJSON().validate(AHORA);
    expect(r.is_valid).toBe(false);
    expect(r.errors).toHaveLength(9);
  });

  test("Customer.validate usa la fecha actual por defecto", () => {
    const r = Customer.fromJSON(cases[0].customer).validate();
    expect(r.is_valid).toBe(true);
  });

  test("telefono null o numerico no es valido", () => {
    expect(new PhoneNumber(null).isValid()).toBe(false);
    expect(new PhoneNumber(5551234567).isValid()).toBe(false);
  });
});

describe("PhoneNumber.getFormatted", () => {
  test("da formato a 10 digitos seguidos", () => {
    expect(new PhoneNumber("5551234567").getFormatted()).toBe("(555) 123-4567");
  });
  test("deja igual lo que no son 10 digitos", () => {
    expect(new PhoneNumber("123").getFormatted()).toBe("123");
  });
});

describe("luhn", () => {
  test.each([
    ["4111111111111111", true],
    ["4111111111111112", false],
    ["", false],
  ])("luhn(%p) = %p", (n, esperado) => {
    expect(luhn(n)).toBe(esperado);
  });
});

describe("Address y CreditCard directos", () => {
  test("Address valida sin errores", () => {
    expect(new Address("1 Main", "NYC", "NY", "10001").validate()).toEqual([]);
  });
  test("CreditCard usa la fecha actual por defecto", () => {
    const c = new CreditCard("4111111111111111", "01/2000", "123");
    expect(c.validate()).toEqual(["Tarjeta de crédito vencida"]);
  });
});
