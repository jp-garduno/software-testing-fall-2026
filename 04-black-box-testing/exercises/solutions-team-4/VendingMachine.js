class VendingMachine {
  constructor() {
    this.state = "Idle";
    this.credit = 0.0;
    this.selectedProduct = null;
    this.change = 0.0;
    this.refund = 0.0;
    this.previousState = null;
    this.history = [];
    this.products = {
      A1: { name: "Chips", price: 1.5, stock: 10 },
      A2: { name: "Candy", price: 1.0, stock: 5 },
      B1: { name: "Soda", price: 2.0, stock: 8 },
      B2: { name: "Water", price: 1.5, stock: 12 },
    };

    this.recordHistory("INIT", null, "Idle", "Machine initialized");
  }

  recordHistory(event, from, to, message) {
    this.history.push({
      event,
      from,
      to,
      message,
      credit: Number(this.credit.toFixed(2)),
      selectedProduct: this.selectedProduct,
    });
  }

  transition(to, event, message) {
    const from = this.state;
    this.state = to;
    this.recordHistory(event, from, to, message);
  }

  reject(event, message) {
    this.recordHistory(event, this.state, this.state, `REJECTED: ${message}`);
    return {
      success: false,
      state: this.state,
      credit: Number(this.credit.toFixed(2)),
      message,
    };
  }

  isValidAmount(amount) {
    return [0.25, 0.5, 1.0, 2.0].includes(amount);
  }

  insertCoin(amount) {
    if (!this.isValidAmount(amount)) {
      return this.reject("insert_coin", "Coin or bill amount is not accepted");
    }

    if (!["Idle", "HasCredit"].includes(this.state)) {
      return this.reject("insert_coin", `Cannot insert money while state is ${this.state}`);
    }

    this.credit = Number((this.credit + amount).toFixed(2));

    if (this.state === "Idle") {
      this.transition("HasCredit", "insert_coin", `Accepted ${amount}`);
    } else {
      this.recordHistory("insert_coin", "HasCredit", "HasCredit", `Accepted ${amount}`);
    }

    return {
      success: true,
      state: this.state,
      credit: this.credit,
      message: "Money accepted",
    };
  }

  selectProduct(productId) {
    if (this.state !== "HasCredit") {
      return this.reject("select_product", "A product can only be selected when credit is available");
    }

    const product = this.products[productId];
    if (!product) {
      return this.reject("product_out_of_stock", "Product does not exist");
    }

    if (product.stock <= 0) {
      return this.reject("product_out_of_stock", "Selected product is out of stock");
    }

    if (this.credit < product.price) {
      return this.reject("insufficient_funds", "Insufficient funds for selected product");
    }

    this.selectedProduct = productId;
    product.stock -= 1;
    this.transition("ProductSelected", "select_product", `Selected ${productId}`);

    return {
      success: true,
      state: this.state,
      selectedProduct: productId,
      credit: this.credit,
      message: "Product selected",
    };
  }

  dispenseComplete() {
    if (this.state !== "ProductSelected" || !this.selectedProduct) {
      return this.reject("dispense_complete", "No selected product is ready to be dispensed");
    }

    this.transition("Dispensing", "dispense_complete", `Dispensing ${this.selectedProduct}`);

    const product = this.products[this.selectedProduct];
    this.change = Number((this.credit - product.price).toFixed(2));

    if (this.change > 0) {
      this.transition(
        "ChangeReturn",
        "dispense_complete",
        `Product dispensed; return change ${this.change}`
      );
      return {
        success: true,
        state: this.state,
        change: this.change,
        message: "Product dispensed; returning change",
      };
    }

    this.credit = 0.0;
    this.selectedProduct = null;
    this.transition("Idle", "dispense_complete", "Product dispensed; exact payment");
    return {
      success: true,
      state: this.state,
      change: 0.0,
      message: "Product dispensed; no change required",
    };
  }

  cancelTransaction() {
    if (this.state === "Idle") {
      this.recordHistory("cancel_transaction", "Idle", "Idle", "No active transaction to cancel");
      return {
        success: true,
        state: "Idle",
        refund: 0.0,
        message: "No active transaction",
      };
    }

    if (this.state !== "HasCredit") {
      return this.reject("cancel_transaction", `Cannot cancel while state is ${this.state}`);
    }

    this.refund = this.credit;
    this.transition("ChangeReturn", "cancel_transaction", `Refund pending: ${this.refund}`);

    return {
      success: true,
      state: this.state,
      refund: this.refund,
      message: "Transaction cancelled; refund pending",
    };
  }

  changeReturned() {
    if (this.state !== "ChangeReturn") {
      return this.reject("change_returned", "No change or refund is pending");
    }

    const returnedAmount = Number((this.change + this.refund).toFixed(2));
    this.credit = 0.0;
    this.change = 0.0;
    this.refund = 0.0;
    this.selectedProduct = null;
    this.transition("Idle", "change_returned", `Returned ${returnedAmount}`);

    return {
      success: true,
      state: this.state,
      returnedAmount,
      message: "Change/refund returned",
    };
  }

  systemError() {
    if (this.state === "OutOfOrder") {
      return this.reject("system_error", "Machine is already out of order");
    }

    this.previousState = this.state;
    this.transition("OutOfOrder", "system_error", "System error detected");
    return {
      success: true,
      state: this.state,
      message: "Machine is out of order",
    };
  }

  getState() {
    return this.state;
  }

  getCredit() {
    return this.credit;
  }

  getHistory() {
    return [...this.history];
  }
}

module.exports = VendingMachine;