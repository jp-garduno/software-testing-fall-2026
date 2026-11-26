/** Decision table tests (design section 3: DT1-DT4). */

const { ERRORS } = require("../src/bankingSystem");
const { makeAccount, accountWithPayees, createAccount } = require("./fixtures");

describe("DT1 - transfer validation", () => {
  test("R1: Active + valid + within limit + funded succeeds", () => {
    const account = makeAccount("Checking", 1000.0);
    expect(account.transfer(200.0).success).toBe(true);
    expect(account.balance).toBe(800.0);
  });

  test("R2: a Suspended account can still transfer", () => {
    const account = makeAccount("Savings", 90.0, "Suspended");
    expect(account.transfer(10.0).success).toBe(true);
    expect(account.balance).toBe(80.0);
  });

  test("R3: a Frozen account is blocked", () => {
    expect(
      makeAccount("Checking", 1000.0, "Frozen").transfer(100.0).error,
    ).toBe(ERRORS.FROZEN);
  });

  test("R4: a Closed account reports its own error", () => {
    expect(
      makeAccount("Checking", 1000.0, "Closed").transfer(100.0).error,
    ).toBe(ERRORS.CLOSED);
  });

  test("R5: a non-positive amount is rejected", () => {
    expect(makeAccount().transfer(-5.0).error).toBe(ERRORS.AMOUNT_POSITIVE);
  });

  test("R6: a non-numeric amount is rejected", () => {
    expect(makeAccount().transfer(null).error).toBe(ERRORS.INVALID_AMOUNT);
  });

  test("R7: the daily limit is checked before the balance", () => {
    expect(makeAccount("Checking", 20000.0).transfer(6000.0).error).toBe(
      ERRORS.DAILY_LIMIT,
    );
  });

  test("R8: within the limit but unfunded", () => {
    expect(makeAccount("Checking", 1000.0).transfer(1200.0).error).toBe(
      ERRORS.INSUFFICIENT,
    );
  });

  test("R9: the state check wins over an invalid amount", () => {
    expect(makeAccount("Checking", 1000.0, "Frozen").transfer(-1.0).error).toBe(
      ERRORS.FROZEN,
    );
  });

  test("R10: Suspended still needs funds", () => {
    const account = makeAccount("Savings", 50.0, "Suspended");
    expect(account.transfer(60.0).error).toBe(ERRORS.INSUFFICIENT);
    expect(account.balance).toBe(50.0);
  });
});

describe("DT2 - monthly fee processing", () => {
  test("R1: Premium never pays a fee", () => {
    const account = makeAccount("Premium", 100000.0);
    expect(account.applyMonthlyFee().waived).toBe(true);
    expect(account.balance).toBe(100000.0);
  });

  test("R2: Savings above the threshold is waived", () => {
    const account = makeAccount("Savings", 2500.0);
    expect(account.applyMonthlyFee().waived).toBe(true);
    expect(account.balance).toBe(2500.0);
  });

  test("R3: Savings below the threshold is charged $5", () => {
    const account = makeAccount("Savings", 800.0);
    expect(account.applyMonthlyFee().charged).toBe(5.0);
    expect(account.balance).toBe(795.0);
  });

  test("R4: Checking above the threshold is waived", () => {
    const account = makeAccount("Checking", 6000.0);
    expect(account.applyMonthlyFee().waived).toBe(true);
    expect(account.balance).toBe(6000.0);
  });

  test("R5: Checking below the threshold is charged $10", () => {
    const account = makeAccount("Checking", 4000.0);
    expect(account.applyMonthlyFee().charged).toBe(10.0);
    expect(account.balance).toBe(3990.0);
  });

  test("R6: an unaffordable fee suspends the account and charges nothing", () => {
    const account = makeAccount("Savings", 3.0, "Suspended");
    expect(account.applyMonthlyFee().error).toBe(ERRORS.INSUFFICIENT);
    expect(account.balance).toBe(3.0);
    expect(account.state).toBe("Suspended");
  });

  test("R3 + A4: a charged fee that crosses the minimum also suspends", () => {
    const account = makeAccount("Savings", 102.0);
    expect(account.applyMonthlyFee().charged).toBe(5.0);
    expect(account.balance).toBe(97.0);
    expect(account.state).toBe("Suspended");
  });
});

describe("DT3 - bill payment validation", () => {
  test("R1: every condition satisfied pays immediately", () => {
    const account = accountWithPayees();
    const result = account.payBill("CFE", 250.0);
    expect(result.scheduled).toBe(false);
    expect(account.balance).toBe(750.0);
  });

  test("R2: a valid payee cannot be paid without funds", () => {
    expect(accountWithPayees().payBill("CFE", 5000.0).error).toBe(
      ERRORS.INSUFFICIENT,
    );
  });

  test("R3: unknown payee", () => {
    expect(accountWithPayees().payBill("NOPE", 10.0).error).toBe(
      ERRORS.UNKNOWN_PAYEE,
    );
  });

  test("R4: inactive payee", () => {
    expect(accountWithPayees().payBill("OLD-GYM", 10.0).error).toBe(
      ERRORS.INACTIVE_PAYEE,
    );
  });

  test("R5: the payee is checked before the amount", () => {
    expect(accountWithPayees().payBill("CFE", 0.0).error).toBe(
      ERRORS.AMOUNT_POSITIVE,
    );
  });

  test("R6: a payment cannot be scheduled into the past", () => {
    const today = new Date(Date.UTC(2026, 2, 10));
    const result = accountWithPayees().payBill(
      "CFE",
      10.0,
      new Date(Date.UTC(2026, 2, 8)),
      today,
    );
    expect(result.error).toBe(ERRORS.PAST_DATE);
  });

  test("R7: the state check precedes every payment condition", () => {
    const account = accountWithPayees();
    account.freeze();
    expect(account.payBill("NOPE", -1.0).error).toBe(ERRORS.FROZEN);
  });

  test("R8: a future date schedules without debiting", () => {
    const account = accountWithPayees();
    const today = new Date(Date.UTC(2026, 2, 10));
    const result = account.payBill(
      "CFE",
      300.0,
      new Date(Date.UTC(2026, 2, 15)),
      today,
    );
    expect(result.scheduled).toBe(true);
    expect(account.balance).toBe(1000.0);
  });
});

describe("DT4 - account creation", () => {
  test("R1: supported type with a deposit above the minimum", () => {
    const result = createAccount("Savings", 250.0);
    expect(result.success).toBe(true);
    expect(result.balance).toBe(250.0);
  });

  test("R2: a deposit under the type minimum is rejected", () => {
    expect(createAccount("Premium", 500.0).error).toBe(ERRORS.OPENING_DEPOSIT);
  });

  test("R3: a negative deposit is rejected before the minimum is considered", () => {
    expect(createAccount("Checking", -1.0).error).toBe(ERRORS.AMOUNT_POSITIVE);
  });

  test.each([["Crypto"], ["savings"], [""]])(
    "R4: type %p is unsupported",
    (accountType) => {
      expect(createAccount(accountType, 50000.0).error).toBe(
        ERRORS.INVALID_TYPE,
      );
    },
  );
});
