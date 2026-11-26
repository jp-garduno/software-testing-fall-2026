/** Equivalence Partitioning tests (design IDs EP1-EP33). */

const { ERRORS, BankAccount } = require("../src/bankingSystem");
const {
  makeAccount,
  accountWithPayees,
  accountWithHistory,
  createAccount,
} = require("./fixtures");

describe("EP - transfer amount partitions", () => {
  test("EP1: a $500 transfer inside every rule succeeds", () => {
    const account = makeAccount("Checking", 1000.0);
    expect(account.transfer(500.0).success).toBe(true);
    expect(account.balance).toBe(500.0);
  });

  test("EP2: $0.00 is rejected as non-positive", () => {
    expect(makeAccount().transfer(0.0).error).toBe(ERRORS.AMOUNT_POSITIVE);
  });

  test("EP3: -$100 is rejected as non-positive", () => {
    expect(makeAccount().transfer(-100.0).error).toBe(ERRORS.AMOUNT_POSITIVE);
  });

  test("EP4: $100,000 exceeds the Checking daily limit", () => {
    expect(makeAccount().transfer(100000.0).error).toBe(ERRORS.DAILY_LIMIT);
  });

  test("EP5: $1,500 fits the limit but not the balance", () => {
    expect(makeAccount().transfer(1500.0).error).toBe(ERRORS.INSUFFICIENT);
  });

  test("EP6: a text amount is not numeric", () => {
    expect(makeAccount().transfer("five hundred").error).toBe(
      ERRORS.INVALID_AMOUNT,
    );
  });

  test("EP7: $0.001 carries sub-cent precision", () => {
    expect(makeAccount().transfer(0.001).error).toBe(ERRORS.AMOUNT_PRECISION);
  });

  test("EP2-EP7: no invalid partition moves money", () => {
    const account = makeAccount();
    [0.0, -100.0, 100000.0, 1500.0, "five hundred", 0.001].forEach((amount) =>
      account.transfer(amount),
    );
    expect(account.balance).toBe(1000.0);
    expect(account.dailyTransferTotal).toBe(0.0);
  });
});

describe("EP - account type partitions", () => {
  test.each([
    ["EP8", "Savings", 2000.0, 100.0, 500.0],
    ["EP9", "Checking", 5000.0, 0.0, 500.0],
    ["EP10", "Premium", 50000.0, 10000.0, 20000.0],
  ])(
    "%s: %s is created with its own limit and minimum",
    (_id, type, limit, minimum, opening) => {
      const result = createAccount(type, opening);
      expect(result.success).toBe(true);
      expect(result.account.getDailyLimit()).toBe(limit);
      expect(result.account.getMinimumBalance()).toBe(minimum);
    },
  );

  test("EP11: an unsupported type cannot be opened", () => {
    expect(createAccount("Crypto", 500.0).error).toBe(ERRORS.INVALID_TYPE);
  });

  test("EP12: an empty type name is invalid", () => {
    expect(createAccount("", 500.0).error).toBe(ERRORS.INVALID_TYPE);
  });
});

describe("EP - opening balance partitions", () => {
  test("EP13: $500 clears the $100 Savings minimum", () => {
    expect(createAccount("Savings", 500.0).state).toBe("Active");
  });

  test("EP14: $50 is under the Savings minimum", () => {
    expect(createAccount("Savings", 50.0).error).toBe(ERRORS.OPENING_DEPOSIT);
  });

  test("EP15: a negative opening deposit is rejected", () => {
    expect(createAccount("Savings", -10.0).error).toBe(ERRORS.AMOUNT_POSITIVE);
  });

  test("EP16: $9,000 is under the Premium minimum", () => {
    expect(createAccount("Premium", 9000.0).error).toBe(ERRORS.OPENING_DEPOSIT);
  });
});

describe("EP - payee partitions", () => {
  test("EP17: a registered active payee is paid", () => {
    const account = accountWithPayees();
    expect(account.payBill("CFE", 120.0).success).toBe(true);
    expect(account.balance).toBe(880.0);
  });

  test("EP18: an unknown payee is rejected", () => {
    expect(accountWithPayees().payBill("UNKNOWN-99", 120.0).error).toBe(
      ERRORS.UNKNOWN_PAYEE,
    );
  });

  test("EP19: a deactivated payee is its own partition", () => {
    expect(accountWithPayees().payBill("OLD-GYM", 120.0).error).toBe(
      ERRORS.INACTIVE_PAYEE,
    );
  });
});

describe("EP - scheduled date partitions", () => {
  test("EP20: a payment without a date is immediate", () => {
    const account = accountWithPayees();
    const result = account.payBill("CFE", 100.0);
    expect(result.scheduled).toBe(false);
    expect(account.balance).toBe(900.0);
  });

  test("EP21: a future date schedules without debiting", () => {
    const account = accountWithPayees();
    const today = new Date(Date.UTC(2026, 2, 1));
    const result = account.payBill(
      "CFE",
      100.0,
      new Date(Date.UTC(2026, 2, 16)),
      today,
    );
    expect(result.scheduled).toBe(true);
    expect(account.balance).toBe(1000.0);
  });

  test("EP22: a past date is rejected", () => {
    const today = new Date(Date.UTC(2026, 2, 1));
    const result = accountWithPayees().payBill(
      "CFE",
      100.0,
      new Date(Date.UTC(2026, 1, 28)),
      today,
    );
    expect(result.error).toBe(ERRORS.PAST_DATE);
  });
});

describe("EP - history date range partitions", () => {
  test("EP23: a partial range filters the history", () => {
    const result = accountWithHistory().getTransactions(
      new Date(Date.UTC(2026, 2, 1)),
      new Date(Date.UTC(2026, 2, 20)),
    );
    expect(result.count).toBe(2);
  });

  test("EP24: no range returns the whole statement", () => {
    expect(accountWithHistory().getTransactions().count).toBe(3);
  });

  test("EP25: an empty result is valid, not an error", () => {
    const result = accountWithHistory().getTransactions(
      new Date(Date.UTC(2030, 0, 1)),
      new Date(Date.UTC(2030, 0, 31)),
    );
    expect(result.success).toBe(true);
    expect(result.count).toBe(0);
  });

  test("EP26: an inverted range is rejected", () => {
    const result = accountWithHistory().getTransactions(
      new Date(Date.UTC(2026, 2, 31)),
      new Date(Date.UTC(2026, 2, 1)),
    );
    expect(result.error).toBe(ERRORS.DATE_ORDER);
  });

  test("EP27: a string is not a date object", () => {
    const result = accountWithHistory().getTransactions(
      "2026-03-01",
      new Date(Date.UTC(2026, 2, 31)),
    );
    expect(result.error).toBe(ERRORS.DATE_TYPE);
  });
});

describe("EP - amount partitions across operations", () => {
  test("EP28: deposit applies the same precision rule", () => {
    const account = makeAccount();
    expect(account.deposit(0.001).error).toBe(ERRORS.AMOUNT_PRECISION);
    expect(account.balance).toBe(1000.0);
  });

  test("EP29: a $0 deposit moves no money", () => {
    expect(makeAccount().deposit(0.0).error).toBe(ERRORS.AMOUNT_POSITIVE);
  });

  test("EP30: bill payment rejects a text amount", () => {
    expect(accountWithPayees().payBill("CFE", "one hundred").error).toBe(
      ERRORS.INVALID_AMOUNT,
    );
  });

  test("EP31: the opening deposit follows the amount partitions", () => {
    expect(createAccount("Checking", "one thousand").error).toBe(
      ERRORS.INVALID_AMOUNT,
    );
  });

  test("EP32: infinity is not a finite amount of money", () => {
    expect(makeAccount().transfer(Infinity).error).toBe(ERRORS.INVALID_AMOUNT);
  });

  test("EP33: the constructor rejects an unknown type", () => {
    expect(() => new BankAccount("Crypto", 500.0)).toThrow(ERRORS.INVALID_TYPE);
  });

  test("EP34: a structured value is not an amount", () => {
    expect(makeAccount().transfer({ amount: 100 }).error).toBe(
      ERRORS.INVALID_AMOUNT,
    );
  });

  test("EP35: 1e-7 is a legal literal but still a sub-cent amount", () => {
    expect(makeAccount().transfer(1e-7).error).toBe(ERRORS.AMOUNT_PRECISION);
  });
});
