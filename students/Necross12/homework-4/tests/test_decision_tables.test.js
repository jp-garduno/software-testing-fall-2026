const BankAccount = require("../src/bankingSystem");

describe("Tabla de decisión 1 - Validación de transferencia", () => {
    test("TD1: fondos OK, límite OK, cuenta activa -> transferencia exitosa", () => {
        const account = new BankAccount("Estándar", 10000);
        expect(account.transfer(100).success).toBe(true);
        expect(account.lastMessage).toBe("La transferencia se realiza");
    });

    test("TD2: fondos OK, límite OK, cuenta congelada -> error cuenta congelada", () => {
        const account = new BankAccount("Estándar", 10000);
        account.next("Congelado");
        const result = account.transfer(100);
        expect(result.success).toBe(false);
        expect(result.error).toBe("Error: Cuenta congelada");
    });

    test("TD3: fondos OK, límite excedido, cuenta activa -> error de límite", () => {
        const account = new BankAccount("Estándar", 10000);
        const result = account.transfer(5001);
        expect(result.success).toBe(false);
        expect(result.error).toBe("Error: supera el límite diario");
    });

    test("TD4: fondos insuficientes, dentro del límite -> error de fondos", () => {
        const account = new BankAccount("Estándar", 100);
        const result = account.transfer(500);
        expect(result.success).toBe(false);
        expect(result.error).toBe("Error: fondos insuficientes");
    });

    test("TD5: fondos insuficientes y límite excedido -> prevalece fondos insuficientes", () => {
        const account = new BankAccount("Estándar", 100);
        const result = account.transfer(6000);
        expect(result.success).toBe(false);
        expect(result.error).toBe("Error: fondos insuficientes");
    });
});
