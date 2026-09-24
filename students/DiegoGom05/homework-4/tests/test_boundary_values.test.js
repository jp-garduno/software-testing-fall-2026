const BankAccount = require("../src/banking_system");

describe("Boundary Value Analysis (BVA) Tests", () => {
  test("BV1: Transfer below minimum ($0.00) fails", () => {
    const account = new BankAccount("Checking", 1000);
    const result = account.transfer(0.0);
    expect(result.success).toBe(false);
    expect(result.error).toContain("must be positive");
  });

  test("BV2: Transfer exactly at minimum ($0.01) succeeds", () => {
    const account = new BankAccount("Checking", 1000);
    const result = account.transfer(0.01);
    expect(result.success).toBe(true);
    expect(account.balance).toBeCloseTo(999.99, 2);
  });

  test("BV3: Transfer just below daily limit ($4,999.99) succeeds", () => {
    const account = new BankAccount("Checking", 10000);
    const result = account.transfer(4999.99);
    expect(result.success).toBe(true);
    expect(account.dailyTransferTotal).toBeCloseTo(4999.99, 2);
  });

  test("BV4: Transfer exactly at daily limit ($5,000.00) succeeds", () => {
    const account = new BankAccount("Checking", 10000);
    const result = account.transfer(5000.0);
    expect(result.success).toBe(true);
    expect(account.dailyTransferTotal).toBeCloseTo(5000.0, 2);
  });

  test("BV5: Transfer just above daily limit ($5,000.01) fails", () => {
    const account = new BankAccount("Checking", 10000);
    const result = account.transfer(5000.01);
    expect(result.success).toBe(false);
    expect(result.error).toContain("Exceeds daily limit");
  });

  test("BV4_P: Premium account transfer at $25,000.00 limit succeeds", () => {
    const account = new BankAccount("Premium", 50000);
    const result = account.transfer(25000.0);
    expect(result.success).toBe(true);
    expect(account.dailyTransferTotal).toBeCloseTo(25000.0, 2);
  });
});
