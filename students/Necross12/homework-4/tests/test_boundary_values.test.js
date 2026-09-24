const BankAccount = require("../src/bankingSystem");

describe("Análisis de valor límite (BVA)", () => {
    test("BV1: Transferir $0.00 debe fallar", () => {
        const account = new BankAccount("Estándar", 1000);
        const result = account.transfer(0.0);
        expect(result.success).toBe(false);
        expect(result.error).toBe("Error: el monto debe ser positivo");
    });

    test("BV2: Transferir exactamente $0.01 se realiza", () => {
        const account = new BankAccount("Estándar", 1000);
        const result = account.transfer(0.01);
        expect(result.success).toBe(true);
        expect(account.balance).toBeCloseTo(999.99, 2);
    });

    test("BV3: $4,999.99 (justo bajo el límite) se realiza", () => {
        const account = new BankAccount("Estándar", 10000);
        expect(account.transfer(4999.99).success).toBe(true);
    });

    test("BV4: Exactamente en el límite de $5,000 se realiza", () => {
        const account = new BankAccount("Estándar", 10000);
        const result = account.transfer(5000);
        expect(result.success).toBe(true);
        expect(account.dailyTransferTotal).toBe(5000);
    });

    test("BV5: $5,000.01 (justo sobre el límite) falla", () => {
        const account = new BankAccount("Estándar", 10000);
        const result = account.transfer(5000.01);
        expect(result.success).toBe(false);
        expect(result.error).toBe("Error: supera el límite diario");
    });

    test("BV10: Ahorro en su límite de $2,000 se realiza", () => {
        const account = new BankAccount("Ahorro", 10000);
        expect(account.transfer(2000).success).toBe(true);
    });

    test("BV11: Ahorro con $2,000.01 supera el límite", () => {
        const account = new BankAccount("Ahorro", 10000);
        const result = account.transfer(2000.01);
        expect(result.success).toBe(false);
        expect(result.error).toBe("Error: supera el límite diario");
    });
});
