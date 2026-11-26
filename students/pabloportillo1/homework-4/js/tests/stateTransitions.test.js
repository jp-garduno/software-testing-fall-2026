/** State transition tests (design IDs ST1-ST13). */

const { ERRORS, WARN_BELOW_MINIMUM } = require("../src/bankingSystem");
const { makeAccount, accountWithHistory } = require("./fixtures");

describe("State transitions", () => {
  test("ST1: Active -> Suspended when a transfer drops below the minimum", () => {
    const account = makeAccount("Savings", 200.0);
    const result = account.transfer(100.01);
    expect(account.state).toBe("Suspended");
    expect(result.warnings).toEqual([WARN_BELOW_MINIMUM]);
    expect(account.balance).toBe(99.99);
  });

  test("ST2: Suspended -> Active when a deposit restores the minimum", () => {
    const account = makeAccount("Savings", 50.0, "Suspended");
    const result = account.deposit(500.0);
    expect(account.state).toBe("Active");
    expect(result.warnings).toEqual([]);
  });

  test("ST3: Suspended -> Suspended when the deposit is not enough", () => {
    const account = makeAccount("Savings", 50.0, "Suspended");
    const result = account.deposit(10.0);
    expect(account.state).toBe("Suspended");
    expect(result.warnings).toEqual([WARN_BELOW_MINIMUM]);
  });

  test("ST4: Active -> Frozen blocks money movement", () => {
    const account = makeAccount("Checking", 1000.0);
    account.freeze();
    expect(account.state).toBe("Frozen");
    expect(account.transfer(10.0).error).toBe(ERRORS.FROZEN);
    expect(account.deposit(10.0).error).toBe(ERRORS.FROZEN);
  });

  test("ST5: Frozen -> Active when the balance meets the minimum", () => {
    const account = makeAccount("Savings", 500.0, "Frozen");
    expect(account.unfreeze().state).toBe("Active");
    expect(account.transfer(10.0).success).toBe(true);
  });

  test("ST6: Frozen -> Suspended when the balance is below the minimum", () => {
    const account = makeAccount("Savings", 20.0, "Frozen");
    expect(account.unfreeze().state).toBe("Suspended");
    expect(account.state).toBe("Suspended");
  });

  test("ST7: Frozen -> Closed returns the final statement", () => {
    const account = makeAccount("Checking", 300.0, "Frozen");
    const result = account.close();
    expect(account.state).toBe("Closed");
    expect(
      result.finalStatement.startsWith("date,type,amount,counterparty"),
    ).toBe(true);
  });

  test.each([["transfer"], ["deposit"], ["close"]])(
    "ST8: a Closed account rejects %s",
    (operation) => {
      const account = makeAccount("Checking", 500.0, "Closed");
      const result =
        operation === "close" ? account.close() : account[operation](10.0);
      expect(result.success).toBe(false);
      expect(result.error).toBe(ERRORS.CLOSED);
      expect(account.state).toBe("Closed");
    },
  );

  test("ST9: Active -> Suspended when the monthly fee cannot be charged", () => {
    const account = makeAccount("Checking", 4.0);
    expect(account.applyMonthlyFee().error).toBe(ERRORS.INSUFFICIENT);
    expect(account.state).toBe("Suspended");
    expect(account.balance).toBe(4.0);
  });

  test("ST10: Suspended -> Suspended; the state warns but does not block", () => {
    const account = makeAccount("Savings", 80.0, "Suspended");
    expect(account.transfer(30.0).success).toBe(true);
    expect(account.state).toBe("Suspended");
  });

  test("ST11: Active -> Closed generates a CSV statement of the history", () => {
    const account = accountWithHistory();
    const result = account.close();
    expect(account.state).toBe("Closed");
    expect(result.finalStatement.split("\n")).toHaveLength(4);
  });

  test("ST12: landing exactly on the minimum is not a drop", () => {
    const account = makeAccount("Savings", 200.0);
    const result = account.transfer(100.0);
    expect(account.state).toBe("Active");
    expect(result.warnings).toEqual([]);
    expect(account.notifications).toEqual([]);
  });

  test("ST13: unfreeze is not a valid event for an Active account", () => {
    const account = makeAccount("Checking", 1000.0);
    const result = account.unfreeze();
    expect(result.error).toBe(ERRORS.NOT_FROZEN);
    expect(account.state).toBe("Active");
  });

  test("ST8 (extra): no event may move an account out of Closed", () => {
    const account = makeAccount("Checking", 500.0, "Closed");
    expect(account.freeze().error).toBe(ERRORS.CLOSED);
    expect(account.unfreeze().error).toBe(ERRORS.CLOSED);
    expect(account.applyMonthlyFee().error).toBe(ERRORS.CLOSED);
    expect(account.state).toBe("Closed");
  });
});
