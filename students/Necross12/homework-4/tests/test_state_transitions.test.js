const BankAccount = require("../src/bankingSystem");

describe("Transiciones de estado", () => {
    test("ST1: Activo -> Suspendido", () => {
        const account = new BankAccount("Ahorro", 500);
        expect(account.next("Suspendido")).toBe(true);
        expect(account.state).toBe("Suspendido");
        expect(account.lastMessage).toBe("Enviar notificación de advertencia");
    });

    test("ST2: Activo -> Congelado", () => {
        const account = new BankAccount("Ahorro", 500);
        expect(account.next("Congelado")).toBe(true);
        expect(account.state).toBe("Congelado");
        expect(account.lastMessage).toBe("Bloquear todas las transacciones");
    });

    test("ST3: Activo -> Cerrado", () => {
        const account = new BankAccount("Ahorro", 500);
        expect(account.next("Cerrado")).toBe(true);
        expect(account.state).toBe("Cerrado");
        expect(account.lastMessage).toBe("Declaración final generada");
    });

    test("ST4: Suspendido -> Activo al restablecer el saldo", () => {
        const account = new BankAccount("Ahorro", 500);
        account.next("Suspendido");
        expect(account.next("Activo")).toBe(true);
        expect(account.state).toBe("Activo");
    });

    test("ST5: transferir dejando el saldo bajo el mínimo suspende la cuenta", () => {
        const account = new BankAccount("Ahorro", 1000);
        account.transfer(950); // saldo 50 < 100
        expect(account.state).toBe("Suspendido");
    });

    test("ST8: Cerrado -> Activo se rechaza", () => {
        const account = new BankAccount("Ahorro", 500);
        account.next("Cerrado");
        expect(account.next("Activo")).toBe(false);
        expect(account.state).toBe("Cerrado");
        expect(account.lastMessage).toBe("Error: Cuenta cerrada");
    });
});
