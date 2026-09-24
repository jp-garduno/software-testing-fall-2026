/** Boundary Value Analysis tests (design IDs BV1-BV31). */

const { ERRORS, WARN_BELOW_MINIMUM } = require("../src/bankingSystem");
const { makeAccount, accountWithHistory } = require("./fixtures");

describe("BVA - Checking daily limit ($5,000)", () => {
  test.each([
    ["BV1", 0.0, ERRORS.AMOUNT_POSITIVE],
    ["BV5", 5000.01, ERRORS.DAILY_LIMIT],
    ["BV6", 10000.0, ERRORS.DAILY_LIMIT],
  ])("%s: $%s is rejected", (_id, amount, expectedError) => {
    expect(makeAccount("Checking", 20000.0).transfer(amount).error).toBe(
      expectedError,
    );
  });

  test.each([
    ["BV2", 0.01],
    ["BV3", 4999.99],
    ["BV4", 5000.0],
  ])("%s: $%s is accepted", (_id, amount) => {
    const account = makeAccount("Checking", 20000.0);
    expect(account.transfer(amount).success).toBe(true);
    expect(account.dailyTransferTotal).toBe(amount);
  });

  test("BV2: $0.01 debits exactly one cent with no floating point drift", () => {
    const account = makeAccount("Checking", 20000.0);
    account.transfer(0.01);
    expect(account.balance).toBe(19999.99);
  });
});

describe("BVA - Savings daily limit ($2,000)", () => {
  test.each([
    ["BV7", 0.01, true],
    ["BV8", 1999.99, true],
    ["BV9", 2000.0, true],
    ["BV10", 2000.01, false],
  ])("%s: $%s", (_id, amount, expectedSuccess) => {
    const result = makeAccount("Savings", 5000.0).transfer(amount);
    expect(result.success).toBe(expectedSuccess);
    if (!expectedSuccess) expect(result.error).toBe(ERRORS.DAILY_LIMIT);
  });
});

describe("BVA - cumulative daily limit (Premium $50,000)", () => {
  test.each([
    ["BV11", 0.99, true, 49999.99],
    ["BV12", 1.0, true, 50000.0],
    ["BV13", 1.01, false, 49999.0],
  ])(
    "%s: second transfer of $%s",
    (_id, amount, expectedSuccess, expectedTotal) => {
      const account = makeAccount("Premium", 100000.0);
      account.transfer(49999.0);
      expect(account.transfer(amount).success).toBe(expectedSuccess);
      expect(account.dailyTransferTotal).toBe(expectedTotal);
    },
  );

  test("BV14: the limit resets at midnight", () => {
    const account = makeAccount("Premium", 100000.0);
    account.transfer(49999.0);
    expect(account.transfer(1.01).success).toBe(false);
    account.resetDailyLimit();
    expect(account.transfer(1.01).success).toBe(true);
    expect(account.dailyTransferTotal).toBe(1.01);
  });
});

describe("BVA - balance vs Savings minimum ($100)", () => {
  test.each([
    ["BV15", 50.0, 150.0, "Active"],
    ["BV16", 99.99, 100.01, "Active"],
    ["BV17", 100.0, 100.0, "Active"],
    ["BV18", 100.01, 99.99, "Suspended"],
    ["BV19", 200.0, 0.0, "Suspended"],
  ])(
    "%s: transferring $%s leaves $%s and state %s",
    (_id, amount, expectedBalance, expectedState) => {
      const account = makeAccount("Savings", 200.0);
      expect(account.transfer(amount).success).toBe(true);
      expect(account.balance).toBe(expectedBalance);
      expect(account.state).toBe(expectedState);
    },
  );

  test("BV18: crossing the minimum raises a warning", () => {
    const account = makeAccount("Savings", 200.0);
    const result = account.transfer(100.01);
    expect(result.warnings).toContain(WARN_BELOW_MINIMUM);
    expect(account.notifications).toContain(WARN_BELOW_MINIMUM);
  });
});

describe("BVA - Savings fee waiver threshold ($1,000)", () => {
  test.each([
    ["BV20", 999.99, false, 994.99],
    ["BV21", 1000.0, false, 995.0],
    ["BV22", 1000.01, true, 1000.01],
    ["BV23", 5000.0, true, 5000.0],
  ])("%s: balance $%s", (_id, balance, expectedWaived, expectedBalance) => {
    const account = makeAccount("Savings", balance);
    const result = account.applyMonthlyFee();
    expect(result.success).toBe(true);
    expect(result.waived).toBe(expectedWaived);
    expect(account.balance).toBe(expectedBalance);
  });
});

describe("BVA - Checking fee affordability ($10 fee)", () => {
  test.each([
    ["BV24", 10.01, 0.01],
    ["BV25", 10.0, 0.0],
  ])("%s: balance $%s covers the fee", (_id, balance, expectedBalance) => {
    const account = makeAccount("Checking", balance);
    expect(account.applyMonthlyFee().success).toBe(true);
    expect(account.balance).toBe(expectedBalance);
    expect(account.state).toBe("Active");
  });

  test.each([
    ["BV26", 9.99],
    ["BV27", 0.0],
  ])("%s: balance $%s cannot cover the fee", (_id, balance) => {
    const account = makeAccount("Checking", balance);
    const result = account.applyMonthlyFee();
    expect(result.error).toBe(ERRORS.INSUFFICIENT);
    expect(account.balance).toBe(balance);
    expect(account.state).toBe("Suspended");
  });
});

describe("BVA - inclusive history range ends", () => {
  test.each([
    ["BV28", Date.UTC(2026, 1, 1), Date.UTC(2026, 2, 1), 1],
    ["BV29", Date.UTC(2026, 2, 2), Date.UTC(2026, 2, 31), 2],
    ["BV30", Date.UTC(2026, 2, 1), Date.UTC(2026, 2, 31), 3],
    ["BV31", Date.UTC(2026, 2, 15), Date.UTC(2026, 2, 15), 1],
  ])("%s: range returns %#", (_id, start, end, expectedCount) => {
    const result = accountWithHistory().getTransactions(
      new Date(start),
      new Date(end),
    );
    expect(result.count).toBe(expectedCount);
  });
});
