const BankAccount = require("../src/banking_system");

describe("Equivalence Partitioning (EP) Tests", () => {
  test("EP1_TA: Valid transfer amount within limits succeeds", () => {
    const account = new BankAccount("Checking", 1000);
    const result = account.transfer(500.0);
    expect(result.success).toBe(true);
    expect(account.balance).toBeCloseTo(500.0, 2);
  });

  test("EP2_TA: Zero transfer amount fails", () => {
    const account = new BankAccount("Checking", 1000);
    const result = account.transfer(0.0);
    expect(result.success).toBe(false);
    expect(result.error).toContain("must be positive");
  });

  test("EP3_TA: Negative transfer amount fails", () => {
    const account = new BankAccount("Checking", 1000);
    const result = account.transfer(-100.0);
    expect(result.success).toBe(false);
    expect(result.error).toContain("must be positive");
  });

  test("EP4_TA: Transfer exceeding daily limit fails", () => {
    const account = new BankAccount("Checking", 100000);
    const result = account.transfer(100000.0);
    expect(result.success).toBe(false);
    expect(result.error).toContain("Exceeds daily limit");
  });

  test("EP5_TA: Transfer exceeding current balance fails", () => {
    const account = new BankAccount("Checking", 5000);
    const result = account.transfer(6000.0);
    expect(result.success).toBe(false);
    expect(result.error).toContain("Insufficient funds");
  });

  test("EP4_AT: Unsupported account type fails during transfer", () => {
    const account = new BankAccount("Credit Card", 1000);
    const result = account.transfer(100.0);
    expect(result.success).toBe(false);
    expect(result.error).toContain("Unsupported account type");
  });

  test("EP2_PI: Unregistered payee ID fails bill payment", () => {
    const account = new BankAccount("Checking", 1000);
    const result = account.processBillPayment("999999", 100.0);
    expect(result.success).toBe(false);
    expect(result.error).toContain("Payee not found");
  });
});
