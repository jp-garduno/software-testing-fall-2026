/**
 * Equivalence Partitioning - implementa design/test-design-document.md seccion 1.1.
 * Se prueba una representante por particion, una por cada una de las cinco entradas.
 */

const { BankAccount, ERRORS } = require("../src/bankingSystem");

describe("Equivalence Partitioning", () => {
  test("EP-TA1: un monto dentro del limite y del saldo se transfiere", () => {
    const account = new BankAccount("Checking", 3000);
    const result = account.transfer(500);

    expect(result.success).toBe(true);
    expect(account.balance).toBeCloseTo(2500, 2);
  });

  test("EP-TA2: un monto de cero es rechazado", () => {
    const result = new BankAccount("Checking", 3000).transfer(0);

    expect(result.success).toBe(false);
    expect(result.error).toBe(ERRORS.AMOUNT_NOT_POSITIVE);
  });

  test("EP-TA4: un monto sobre el limite diario es rechazado", () => {
    const result = new BankAccount("Checking", 3000).transfer(100000);

    expect(result.success).toBe(false);
    expect(result.error).toBe(ERRORS.EXCEEDS_DAILY_LIMIT);
  });

  test("EP-TA6: un monto no numerico es rechazado", () => {
    const result = new BankAccount("Checking", 3000).transfer("500");

    expect(result.success).toBe(false);
    expect(result.error).toBe(ERRORS.INVALID_AMOUNT);
  });

  test("EP-AT1..EP-AT3: cada tipo de cuenta aplica su limite y saldo minimo", () => {
    expect(new BankAccount("Savings", 20000).getDailyLimit()).toBe(2000);
    expect(new BankAccount("Savings", 20000).getMinimumBalance()).toBe(100);
    expect(new BankAccount("Checking", 20000).getDailyLimit()).toBe(5000);
    expect(new BankAccount("Premium", 20000).getDailyLimit()).toBe(50000);
    expect(new BankAccount("Premium", 20000).getMinimumBalance()).toBe(10000);
  });

  test("EP-AT4: un tipo de cuenta desconocido es rechazado", () => {
    expect(() => new BankAccount("Crypto", 1000)).toThrow(
      ERRORS.INVALID_ACCOUNT_TYPE,
    );
  });

  test("EP-AB2: un saldo inicial bajo el minimo abre la cuenta Suspendida", () => {
    const account = new BankAccount("Savings", 50);

    expect(account.state).toBe("Suspended");
  });

  test("EP-PY2: un beneficiario no registrado es rechazado", () => {
    const result = new BankAccount("Checking", 1000).payBill("UNKNOWN_CO", 100);

    expect(result.success).toBe(false);
    expect(result.error).toBe(ERRORS.INVALID_PAYEE);
  });

  test("EP-DR1: un rango de fechas valido filtra el historial y lo exporta a CSV", () => {
    const account = new BankAccount("Checking", 1000);
    account.transfer(100);
    account.setCurrentDate("2026-02-10");
    account.deposit(50);

    const history = account.getTransactionHistory("2026-01-01", "2026-01-31");
    expect(history.success).toBe(true);
    expect(history.transactions).toHaveLength(1);

    const csv = account.exportHistoryToCsv();
    expect(csv.csv).toContain("2026-01-15,TRANSFER,100.00");
  });
});
