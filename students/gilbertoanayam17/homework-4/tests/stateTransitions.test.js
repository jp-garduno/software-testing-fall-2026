/**
 * State Transition Testing - implementa design/test-design-document.md seccion 1.4.
 * Se implementan las transiciones principales y el estado terminal.
 */

const { BankAccount, ERRORS } = require("../src/bankingSystem");

describe("State Transitions", () => {
  test("ST1: Active -> Suspended cuando el saldo cae bajo el minimo", () => {
    const account = new BankAccount("Savings", 500);
    const result = account.transfer(450);

    expect(account.state).toBe("Suspended");
    expect(result.warning).toContain("below the minimum");
  });

  test("ST2: Suspended -> Active cuando un deposito restaura el saldo", () => {
    const account = new BankAccount("Savings", 50);
    expect(account.state).toBe("Suspended");

    account.deposit(100);

    expect(account.state).toBe("Active");
  });

  test("ST3: Active -> Frozen y de vuelta a Active al descongelar", () => {
    const account = new BankAccount("Checking", 1000);

    expect(account.freeze().success).toBe(true);
    expect(account.state).toBe("Frozen");

    expect(account.unfreeze().success).toBe(true);
    expect(account.state).toBe("Active");
  });

  test("ST5: Active -> Closed genera el estado de cuenta final", () => {
    const account = new BankAccount("Checking", 1000);
    const result = account.close();

    expect(account.state).toBe("Closed");
    expect(result.finalStatement).toBeCloseTo(1000, 2);
  });

  test("ST12: Closed es terminal y rechaza cualquier evento", () => {
    const account = new BankAccount("Checking", 1000);
    account.close();

    expect(account.transfer(10).error).toBe(ERRORS.ACCOUNT_CLOSED);
    expect(account.deposit(10).error).toBe(ERRORS.ACCOUNT_CLOSED);
    expect(account.close().error).toBe(ERRORS.ACCOUNT_CLOSED);
    expect(account.state).toBe("Closed");
  });
});
