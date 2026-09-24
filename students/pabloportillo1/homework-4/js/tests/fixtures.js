/** Shared builders for the SecureBank Jest suite (mirror of tests/conftest.py). */

const { BankAccount, createAccount } = require("../src/bankingSystem");

const HISTORY_DATES = [
  new Date(Date.UTC(2026, 2, 1)),
  new Date(Date.UTC(2026, 2, 15)),
  new Date(Date.UTC(2026, 2, 31)),
];

/** Build an account of any type, balance and state. */
function makeAccount(
  accountType = "Checking",
  balance = 1000.0,
  state = "Active",
) {
  return new BankAccount(accountType, balance, state);
}

/** Checking account with one active payee and one deactivated payee. */
function accountWithPayees() {
  const account = makeAccount("Checking", 1000.0);
  account.registerPayee("CFE", "Comision Federal de Electricidad");
  account.registerPayee("OLD-GYM", "Old Gym Membership", false);
  return account;
}

/** Checking account holding three scheduled payments dated 1, 15 and 31 March 2026. */
function accountWithHistory() {
  const account = accountWithPayees();
  const seededToday = new Date(Date.UTC(2026, 0, 1));
  HISTORY_DATES.forEach((when, index) => {
    account.payBill("CFE", 10.0 * (index + 1), when, seededToday);
  });
  return account;
}

module.exports = {
  makeAccount,
  accountWithPayees,
  accountWithHistory,
  createAccount,
  HISTORY_DATES,
};
