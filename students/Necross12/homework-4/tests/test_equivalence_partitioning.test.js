const BankAccount = require("../src/bankingSystem");

describe("Partición de equivalencia - Tipo de cuenta", () => {
    test("EP6: Ahorro es un tipo válido", () => {
        const r = BankAccount.validarTipoCuenta("Ahorro");
        expect(r.valid).toBe(true);
        expect(r.message).toBe("Se acepta: cuenta de ahorro");
    });

    test("EP7: Estándar es un tipo válido", () => {
        const r = BankAccount.validarTipoCuenta("Estándar");
        expect(r.valid).toBe(true);
        expect(r.message).toBe("Se acepta: cuenta corriente");
    });

    test("EP8: Premium es un tipo válido", () => {
        const r = BankAccount.validarTipoCuenta("Premium");
        expect(r.valid).toBe(true);
        expect(r.message).toBe("Se acepta: cuenta premium");
    });

    test("EP9: Otro es un tipo inválido", () => {
        const r = BankAccount.validarTipoCuenta("Otro");
        expect(r.valid).toBe(false);
        expect(r.error).toBe("Error: tipo de cuenta no válido");
    });

    test("EP10: Business es un tipo inválido", () => {
        const r = BankAccount.validarTipoCuenta("Business");
        expect(r.valid).toBe(false);
        expect(r.error).toBe("Error: tipo de cuenta no válido");
    });

    test("EP11: tipo vacío es inválido", () => {
        const r = BankAccount.validarTipoCuenta("");
        expect(r.valid).toBe(false);
        expect(r.error).toBe("Error: el tipo de cuenta es obligatorio");
    });
});
