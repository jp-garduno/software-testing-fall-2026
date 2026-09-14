const VendingMachine = require("./VendingMachine");

describe("Vending Machine - State Transitions", () => {
  test("VT-01: Idle → HasCredit via insert_coin()", () => {
    const vm = new VendingMachine();
    const result = vm.insertCoin(1.0);

    expect(result.success).toBe(true);
    expect(vm.getState()).toBe("HasCredit");
    expect(vm.getCredit()).toBe(1.0);
  });

  test("VT-02: HasCredit → HasCredit accumulates valid money", () => {
    const vm = new VendingMachine();
    vm.insertCoin(1.0);
    const result = vm.insertCoin(0.5);

    expect(result.success).toBe(true);
    expect(vm.getState()).toBe("HasCredit");
    expect(vm.getCredit()).toBe(1.5);
  });

  test("VT-03: HasCredit → ProductSelected with enough credit and stock", () => {
    const vm = new VendingMachine();
    vm.insertCoin(2.0);

    const result = vm.selectProduct("A2");

    expect(result.success).toBe(true);
    expect(vm.getState()).toBe("ProductSelected");
    expect(vm.products.A2.stock).toBe(4);
  });

  test("VT-04: ProductSelected → Dispensing → ChangeReturn when change exists", () => {
    const vm = new VendingMachine();
    vm.insertCoin(2.0);
    vm.selectProduct("A2");

    const result = vm.dispenseComplete();

    expect(result.success).toBe(true);
    expect(vm.getHistory().some((entry) => entry.to === "Dispensing")).toBe(true);
    expect(vm.getState()).toBe("ChangeReturn");
    expect(result.change).toBe(1.0);
  });

  test("VT-05: ChangeReturn → Idle after change_returned()", () => {
    const vm = new VendingMachine();
    vm.insertCoin(2.0);
    vm.selectProduct("A2");
    vm.dispenseComplete();

    const result = vm.changeReturned();

    expect(result.success).toBe(true);
    expect(result.returnedAmount).toBe(1.0);
    expect(vm.getState()).toBe("Idle");
    expect(vm.getCredit()).toBe(0);
  });

  test("VT-06: HasCredit → ChangeReturn → Idle after cancellation", () => {
    const vm = new VendingMachine();
    vm.insertCoin(1.0);
    vm.insertCoin(0.5);

    const cancellation = vm.cancelTransaction();
    expect(cancellation.success).toBe(true);
    expect(cancellation.refund).toBe(1.5);
    expect(vm.getState()).toBe("ChangeReturn");

    const result = vm.changeReturned();
    expect(result.success).toBe(true);
    expect(result.returnedAmount).toBe(1.5);
    expect(vm.getState()).toBe("Idle");
    expect(vm.getCredit()).toBe(0);
  });

  test("VT-07: ProductSelected → Dispensing → Idle after exact payment", () => {
    const vm = new VendingMachine();
    vm.insertCoin(1.0);
    vm.insertCoin(0.5);
    vm.selectProduct("A1");

    const result = vm.dispenseComplete();

    expect(result.success).toBe(true);
    expect(result.change).toBe(0);
    expect(vm.getState()).toBe("Idle");
    expect(vm.getCredit()).toBe(0);
  });

  test("VT-08: Any operational state → OutOfOrder via system_error()", () => {
    const vm = new VendingMachine();
    vm.insertCoin(1.0);

    const result = vm.systemError();

    expect(result.success).toBe(true);
    expect(vm.getState()).toBe("OutOfOrder");
    expect(vm.previousState).toBe("HasCredit");
  });

  test("VT-09: Insufficient funds keeps HasCredit and does not alter stock", () => {
    const vm = new VendingMachine();
    vm.insertCoin(1.0);

    const result = vm.selectProduct("B1");

    expect(result.success).toBe(false);
    expect(vm.getState()).toBe("HasCredit");
    expect(vm.products.B1.stock).toBe(8);
  });

  test("VT-10: Out-of-stock product keeps HasCredit and credit", () => {
    const vm = new VendingMachine();
    vm.insertCoin(2.0);
    vm.products.B1.stock = 0;

    const result = vm.selectProduct("B1");

    expect(result.success).toBe(false);
    expect(vm.getState()).toBe("HasCredit");
    expect(vm.getCredit()).toBe(2.0);
  });

  test("IT-01: Idle rejects select_product() without credit", () => {
    const vm = new VendingMachine();
    const result = vm.selectProduct("A1");

    expect(result.success).toBe(false);
    expect(vm.getState()).toBe("Idle");
  });

  test("IT-02: Idle rejects dispense_complete()", () => {
    const vm = new VendingMachine();
    const result = vm.dispenseComplete();

    expect(result.success).toBe(false);
    expect(vm.getState()).toBe("Idle");
  });

  test("IT-03: Idle rejects change_returned()", () => {
    const vm = new VendingMachine();
    const result = vm.changeReturned();

    expect(result.success).toBe(false);
    expect(vm.getState()).toBe("Idle");
  });

  test("IT-04: HasCredit rejects dispense_complete() before selection", () => {
    const vm = new VendingMachine();
    vm.insertCoin(1.0);

    const result = vm.dispenseComplete();

    expect(result.success).toBe(false);
    expect(vm.getState()).toBe("HasCredit");
  });

  test("IT-05: HasCredit rejects change_returned()", () => {
    const vm = new VendingMachine();
    vm.insertCoin(1.0);

    const result = vm.changeReturned();

    expect(result.success).toBe(false);
    expect(vm.getState()).toBe("HasCredit");
  });

  test("IT-06: ProductSelected rejects another insert_coin()", () => {
    const vm = new VendingMachine();
    vm.insertCoin(2.0);
    vm.selectProduct("A2");

    const result = vm.insertCoin(0.25);

    expect(result.success).toBe(false);
    expect(vm.getState()).toBe("ProductSelected");
    expect(vm.getCredit()).toBe(2.0);
  });

  test("IT-07: ProductSelected rejects selecting a second product", () => {
    const vm = new VendingMachine();
    vm.insertCoin(2.0);
    vm.selectProduct("A2");

    const result = vm.selectProduct("A1");

    expect(result.success).toBe(false);
    expect(vm.getState()).toBe("ProductSelected");
  });

  test("IT-08: ProductSelected rejects cancellation", () => {
    const vm = new VendingMachine();
    vm.insertCoin(2.0);
    vm.selectProduct("A2");

    const result = vm.cancelTransaction();

    expect(result.success).toBe(false);
    expect(vm.getState()).toBe("ProductSelected");
  });

  test("IT-09: ChangeReturn rejects insert_coin()", () => {
    const vm = new VendingMachine();
    vm.insertCoin(2.0);
    vm.selectProduct("A2");
    vm.dispenseComplete();

    const result = vm.insertCoin(0.25);

    expect(result.success).toBe(false);
    expect(vm.getState()).toBe("ChangeReturn");
  });

  test("IT-10: ChangeReturn rejects select_product()", () => {
    const vm = new VendingMachine();
    vm.insertCoin(2.0);
    vm.selectProduct("A2");
    vm.dispenseComplete();

    const result = vm.selectProduct("A1");

    expect(result.success).toBe(false);
    expect(vm.getState()).toBe("ChangeReturn");
  });

  test("IT-11: OutOfOrder rejects events from the user", () => {
    const vm = new VendingMachine();
    vm.systemError();

    const insertResult = vm.insertCoin(1.0);
    const selectionResult = vm.selectProduct("A1");

    expect(insertResult.success).toBe(false);
    expect(selectionResult.success).toBe(false);
    expect(vm.getState()).toBe("OutOfOrder");
  });

  test("IT-12: Unsupported amount is rejected without state changes", () => {
    const vm = new VendingMachine();
    const result = vm.insertCoin(0.1);

    expect(result.success).toBe(false);
    expect(vm.getState()).toBe("Idle");
    expect(vm.getCredit()).toBe(0);
  });

  test("History records state changes and rejected transitions", () => {
    const vm = new VendingMachine();
    vm.insertCoin(1.0);
    vm.selectProduct("B1");

    const history = vm.getHistory();
    expect(history.length).toBeGreaterThanOrEqual(3);
    expect(history.at(-1).message).toContain("REJECTED");
  });
});