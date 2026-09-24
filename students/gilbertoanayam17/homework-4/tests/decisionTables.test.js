/**
 * Decision Tables - implementa design/test-design-document.md seccion 1.3.
 * Se implementan las reglas con accion distinta de cada tabla.
 */

const { BankAccount, ERRORS } = require("../src/bankingSystem");

describe("Decision Tables", () => {
  test("DT1-R1: acepta movimientos + dentro del limite + con fondos = exito", () => {
    const account = new BankAccount("Checking", 20000);
    const result = account.transfer(100);

    expect(result.success).toBe(true);
    expect(account.balance).toBeCloseTo(19900, 2);
  });

  test("DT1-R2: dentro del limite pero sin fondos = Insufficient funds", () => {
    const account = new BankAccount("Checking", 50);
    const result = account.transfer(100);

    expect(result.success).toBe(false);
    expect(result.error).toBe(ERRORS.INSUFFICIENT_FUNDS);
    expect(account.balance).toBeCloseTo(50, 2);
  });

  test("DT1-R3: con fondos pero sobre el limite = Exceeds daily limit", () => {
    const result = new BankAccount("Checking", 20000).transfer(6000);

    expect(result.success).toBe(false);
    expect(result.error).toBe(ERRORS.EXCEEDS_DAILY_LIMIT);
  });

  test("DT1-R5: una cuenta congelada rechaza sin evaluar limite ni fondos", () => {
    const account = new BankAccount("Checking", 20000);
    account.freeze();
    const result = account.transfer(100);

    expect(result.success).toBe(false);
    expect(result.error).toBe(ERRORS.ACCOUNT_FROZEN);
  });

  test("DT2-R2: Savings bajo el umbral de exencion paga la comision de $5", () => {
    const account = new BankAccount("Savings", 800);
    const result = account.applyMonthlyFee();

    expect(result.waived).toBe(false);
    expect(account.balance).toBeCloseTo(795, 2);
  });

  test("DT2-R3: Savings sin fondos para la comision queda suspendida", () => {
    const account = new BankAccount("Savings", 3);
    const result = account.applyMonthlyFee();

    expect(result.success).toBe(false);
    expect(result.error).toBe(ERRORS.INSUFFICIENT_FUNDS);
    expect(account.state).toBe("Suspended");
  });

  test("DT3-R6: un pago con fecha futura se agenda sin mover el saldo", () => {
    const account = new BankAccount("Checking", 1000);
    const result = account.payBill("CREDIT_CARD_VISA", 100, "2026-03-01");

    expect(result.success).toBe(true);
    expect(result.scheduled).toBe(true);
    expect(account.balance).toBeCloseTo(1000, 2);
  });
});
