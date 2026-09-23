const BankAccount = require("../src/banking_system");

describe("Decision Table Tests", () => {
  test("DT1_Rule1: Transfer succeeds when funds available, within limit, and account active", () => {
    const account = new BankAccount("Checking", 1000);
    const result = account.transfer(200.0);
    expect(result.success).toBe(true);
    expect(result.error).toBeNull();
  });

  test("DT1_Rule2: Transfer fails when account is frozen despite having funds and being within limit", () => {
    const account = new BankAccount("Checking", 1000);
    account.changeState("Frozen");
    const result = account.transfer(200.0);
    expect(result.success).toBe(false);
    expect(result.error).toContain("frozen");
  });

  test("DT1_Rule5: Transfer fails when funds are insufficient despite active account and within limit", () => {
    const account = new BankAccount("Checking", 100);
    const result = account.transfer(500.0);
    expect(result.success).toBe(false);
    expect(result.error).toContain("Insufficient funds");
  });

  test("DT2_Rule2: Monthly fee charged when Savings balance <= $100 threshold", () => {
    const account = new BankAccount("Savings", 100);
    const result = account.processMonthlyFee();
    expect(result.success).toBe(true);
    expect(result.feeCharged).toBe(12.0);
    expect(account.balance).toBeCloseTo(88.0, 2);
  });

  test("DT2_Rule5: Monthly fee waived for Premium accounts regardless of balance", () => {
    const account = new BankAccount("Premium", 50);
    const result = account.processMonthlyFee();
    expect(result.success).toBe(true);
    expect(result.feeCharged).toBe(0.0);
    expect(account.balance).toBeCloseTo(50.0, 2);
  });

  test("DT3_Rule4: Bill payment fails when payee service is unavailable", () => {
    const account = new BankAccount("Checking", 1000);
    const result = account.processBillPayment("CFE123", 50.0, false);
    expect(result.success).toBe(false);
    expect(result.error).toContain("Payee not found");
  });

  test("DT_COVERAGE: Checking fee charged when balance <= $1000", () => {
    const account = new BankAccount("Checking", 500);
    const result = account.processMonthlyFee();
    expect(result.success).toBe(true);
    expect(result.feeCharged).toBe(12.0);
  });

  test("DT_COVERAGE: Premium account processMonthlyFee returns 0 fee", () => {
    const account = new BankAccount("Premium", 5000);
    const result = account.processMonthlyFee();
    expect(result.success).toBe(true);
    expect(result.feeCharged).toBe(0.0);
  });
});
