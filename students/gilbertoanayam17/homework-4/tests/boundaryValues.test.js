/**
 * Boundary Value Analysis - implementa design/test-design-document.md seccion 1.2.
 * Se implementan las fronteras criticas de BV1, BV3 y BV4.
 */

const { BankAccount, ERRORS } = require("../src/bankingSystem");

describe("Boundary Value Analysis", () => {
  test("BV1-1: $0.00 esta bajo el minimo y es rechazado", () => {
    const result = new BankAccount("Checking", 20000).transfer(0.0);

    expect(result.success).toBe(false);
    expect(result.error).toBe(ERRORS.AMOUNT_NOT_POSITIVE);
  });

  test("BV1-2: $0.01 es el minimo valido y se acepta", () => {
    const account = new BankAccount("Checking", 20000);
    const result = account.transfer(0.01);

    expect(result.success).toBe(true);
    expect(account.balance).toBeCloseTo(19999.99, 2);
  });

  test("BV1-4: $5,000.00 esta exactamente en el limite y se acepta", () => {
    const account = new BankAccount("Checking", 20000);
    const result = account.transfer(5000.0);

    expect(result.success).toBe(true);
    expect(account.dailyTransferTotal).toBeCloseTo(5000, 2);
  });

  test("BV1-5: $5,000.01 supera el limite por un centavo y es rechazado", () => {
    const result = new BankAccount("Checking", 20000).transfer(5000.01);

    expect(result.success).toBe(false);
    expect(result.error).toBe(ERRORS.EXCEEDS_DAILY_LIMIT);
  });

  test("BV3-2: dejar el saldo exactamente en el minimo mantiene la cuenta Activa", () => {
    const account = new BankAccount("Savings", 500);
    account.transfer(400.0);

    expect(account.balance).toBeCloseTo(100.0, 2);
    expect(account.state).toBe("Active");
  });

  test("BV3-3: un centavo bajo el minimo suspende la cuenta", () => {
    const account = new BankAccount("Savings", 500);
    account.transfer(400.01);

    expect(account.balance).toBeCloseTo(99.99, 2);
    expect(account.state).toBe("Suspended");
  });

  test("BV4-1: dos transferencias que suman exactamente el limite se aceptan", () => {
    const account = new BankAccount("Checking", 20000);
    account.transfer(4999.99);
    const result = account.transfer(0.01);

    expect(result.success).toBe(true);
    expect(account.dailyTransferTotal).toBeCloseTo(5000, 2);
  });
});
