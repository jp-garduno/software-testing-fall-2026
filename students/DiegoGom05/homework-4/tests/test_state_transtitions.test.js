const BankAccount = require("../src/banking_system");

describe("State Transition Tests", () => {
  test("ST1: Active to Suspended transition when balance drops below $100", () => {
    const account = new BankAccount("Checking", 150);
    const result = account.transfer(100.0);
    expect(result.success).toBe(true);
    expect(account.state).toBe("Suspended");
  });

  test("ST2: Suspended to Active transition after deposit restores balance above $100", () => {
    const account = new BankAccount("Checking", 50);
    account.state = "Suspended";
    const result = account.deposit(100.0);
    expect(result.success).toBe(true);
    expect(account.state).toBe("Active");
  });

  test("ST3: Active to Frozen transition via freeze request", () => {
    const account = new BankAccount("Checking", 1000);
    const result = account.changeState("Frozen");
    expect(result.success).toBe(true);
    expect(account.state).toBe("Frozen");
  });

  test("ST4: Frozen to Active transition via unfreeze approval", () => {
    const account = new BankAccount("Checking", 1000);
    account.changeState("Frozen");
    const result = account.changeState("Active", true);
    expect(result.success).toBe(true);
    expect(account.state).toBe("Active");
  });

  test("ST7: Outbound transfer attempt blocked while in Frozen state", () => {
    const account = new BankAccount("Checking", 1000);
    account.changeState("Frozen");
    const result = account.transfer(100.0);
    expect(result.success).toBe(false);
    expect(result.error).toContain("frozen");
    expect(account.balance).toBeCloseTo(1000.0, 2);
  });

  test("ST8: Any operation fails when account is in Closed state", () => {
    const account = new BankAccount("Checking", 1000);
    account.changeState("Closed");

    const transferResult = account.transfer(50.0);
    const depositResult = account.deposit(50.0);

    expect(transferResult.success).toBe(false);
    expect(transferResult.error).toContain("closed");
    expect(depositResult.success).toBe(false);
    expect(depositResult.error).toContain("closed");
  });
});
