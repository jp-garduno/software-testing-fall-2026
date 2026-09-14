## Part A: State Diagram

### Estados

| Estado | Significado |
|---|---|
| `Idle` | La máquina no tiene crédito activo y espera que el usuario inserte dinero. |
| `HasCredit` | La máquina tiene crédito; el usuario puede insertar más dinero, seleccionar un producto o cancelar. |
| `ProductSelected` | Se validó el producto, hay fondos suficientes y el producto quedó reservado para dispensarse. |
| `Dispensing` | El producto se está dispensando. |
| `ChangeReturn` | La máquina devuelve cambio o reembolsa el dinero de una cancelación. |
| `OutOfOrder` | Ocurrió un error del sistema; la máquina no acepta operaciones normales hasta recuperarse. |

### Diagrama ASCII

```text
                                      system_error()
        +---------------------------------------------------------------+
        |                                                               v
+--------+ insert_coin(valid) +-----------+ select_product(valid) +-----------------+
|  Idle  | -----------------> | HasCredit | --------------------> | ProductSelected |
+--------+                    +-----------+                       +-----------------+
    ^                              |  ^                                    |
    |                              |  | insert_coin(valid)                  | dispense_complete()
    |                              |  +--------------------------------------+ 
    |                              |                                         v
    |                              |                                  +-------------+
    |                              |                                  | Dispensing  |
    |                              |                                  +-------------+
    |                              |                                         |
    |                              |                                         | product dispensed
    |                              |                                         v
    |                              |                         +-----------------------+
    |                              |                         | ChangeReturn          |
    |                              |                         | change / refund       |
    |                              |                         +-----------------------+
    |                              |                                     |
    | cancel_transaction()         |                                     | change_returned()
    | refund = credit              |                                     v
    +------------------------------+----------------------------------+  +--------+
                                                                       |  |  Idle  |
                                                                       +--+--------+

                         +----------------+
                         |   OutOfOrder   |
                         +----------------+
                                  ^
                                  |
          system_error() from any operational state:
          Idle, HasCredit, ProductSelected, Dispensing, ChangeReturn

HasCredit -- select_product(insufficient_funds) --> HasCredit
HasCredit -- select_product(product_out_of_stock) --> HasCredit
HasCredit -- cancel_transaction() --> ChangeReturn -- change_returned() --> Idle
ProductSelected -- dispense_complete() --> Dispensing -- (acción interna de finalización) --> ChangeReturn / Idle
Idle / HasCredit / ProductSelected / Dispensing / ChangeReturn -- system_error() --> OutOfOrder
OutOfOrder -- cualquier evento original --> OutOfOrder (rechazado)
```

## Part B: State Transition Table

### Transiciones válidas

| ID | Estado actual | Evento original | Guarda / condición | Acción esperada | Estado siguiente |
|---|---|---|---|---|---|
| VT-01 | `Idle` | `insert_coin(amount)` | Importe permitido | Sumar el importe a crédito | `HasCredit` |
| VT-02 | `HasCredit` | `insert_coin(amount)` | Importe permitido | Acumular el importe en crédito | `HasCredit` |
| VT-03 | `HasCredit` | `select_product(productId)` | Producto existente, stock > 0, crédito suficiente | Guardar producto y descontar una unidad de stock | `ProductSelected` |
| VT-04 | `ProductSelected` | `dispense_complete()` | Existe un producto seleccionado | Registrar paso interno `ProductSelected → Dispensing`; dispensar producto; calcular cambio | `ChangeReturn` si cambio > 0; `Idle` si pago exacto |
| VT-05 | `ChangeReturn` | `change_returned()` | Hay cambio o reembolso pendiente | Entregar devolución; limpiar crédito, cambio, reembolso y producto | `Idle` |
| VT-06 | `HasCredit` | `cancel_transaction()` | Crédito mayor a 0 | Guardar crédito como reembolso pendiente | `ChangeReturn` |
| VT-07 | `Idle` | `cancel_transaction()` | No hay crédito | No se devuelve dinero; operación segura | `Idle` |
| VT-08 | `Idle`, `HasCredit`, `ProductSelected`, `Dispensing`, `ChangeReturn` | `system_error()` | Error detectado | Guardar estado previo y registrar error | `OutOfOrder` |
| VT-09 | `HasCredit` | `select_product(productId)` | Crédito insuficiente | Rechazar selección; no modificar crédito ni stock | `HasCredit` |
| VT-10 | `HasCredit` | `select_product(productId)` | Producto agotado o inexistente | Rechazar selección; no modificar crédito ni stock | `HasCredit` |

### Eventos con condición no satisfactoria

| Evento lógico | Se origina al | Estado inicial | Resultado |
|---|---|---|---|
| `insufficient_funds()` | `selectProduct()` con `credit < product.price` | `HasCredit` | Permanece en `HasCredit` y devuelve error. |
| `product_out_of_stock()` | `selectProduct()` con `stock === 0` | `HasCredit` | Permanece en `HasCredit` y devuelve error. |

### Transiciones inválidas

| ID | Estado actual | Evento inválido | Acción esperada | Estado final |
|---|---|---|---|---|
| IT-01 | `Idle` | `select_product(productId)` | Rechazar: no hay crédito | `Idle` |
| IT-02 | `Idle` | `dispense_complete()` | Rechazar: no hay producto seleccionado | `Idle` |
| IT-03 | `Idle` | `change_returned()` | Rechazar: no existe devolución pendiente | `Idle` |
| IT-04 | `HasCredit` | `dispense_complete()` | Rechazar: primero debe seleccionarse un producto | `HasCredit` |
| IT-05 | `HasCredit` | `change_returned()` | Rechazar: no existe devolución pendiente | `HasCredit` |
| IT-06 | `ProductSelected` | `insert_coin(amount)` | Rechazar: ya existe un producto seleccionado | `ProductSelected` |
| IT-07 | `ProductSelected` | `select_product(productId)` | Rechazar: ya existe una selección activa | `ProductSelected` |
| IT-08 | `ProductSelected` | `cancel_transaction()` | Rechazar: producto seleccionado, pendiente de dispensación | `ProductSelected` |
| IT-09 | `ChangeReturn` | `insert_coin(amount)` | Rechazar: primero debe finalizar devolución | `ChangeReturn` |
| IT-10 | `ChangeReturn` | `select_product(productId)` | Rechazar: primero debe finalizar devolución | `ChangeReturn` |
| IT-11 | `ChangeReturn` | `cancel_transaction()` | Rechazar: ya existe devolución pendiente | `ChangeReturn` |
| IT-12 | `OutOfOrder` | `insert_coin`, `select_product`, `cancel_transaction`, `dispense_complete` o `change_returned` | Rechazar: máquina fuera de servicio | `OutOfOrder` |
| IT-13 | `Idle` o `HasCredit` | `insert_coin(amount)` con importe no admitido | Rechazar: importe no permitido | Sin cambio |

## Part C: Implementation

Guarda el siguiente código como `VendingMachine.js`. Solo utiliza los métodos asociados a los eventos dados en el enunciado, más métodos de consulta (`getState`, `getCredit`, `getHistory`) que no son eventos de la máquina.

```javascript
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
```

### Compatibilidad con el test base dado

Con esta implementación, el test proporcionado se mantiene coherente:

```javascript
test("Valid: HasCredit → ProductSelected → Dispensing", () => {
  const vm = new VendingMachine();
  vm.insertCoin(2.0);

  const result = vm.selectProduct("A2");
  expect(result.success).toBe(true);
  expect(vm.getState()).toBe("ProductSelected");

  vm.dispenseComplete();
  expect(vm.getState()).toBe("ChangeReturn");
});
```

Durante `dispenseComplete()`, el historial contiene el paso por `Dispensing` antes de llegar a `ChangeReturn`.

---

## Test Suite

`VendingMachine.test.js`.

```javascript
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
```

---

## Casos de prueba

### TC_VM_001 — Moneda válida desde Idle

```md
**Test Case ID**: TC_VM_001
**Title**: Aceptar moneda válida desde el estado Idle
**Priority**: Critical
**Type**: Positive

**Description**:
Valida que `insert_coin(amount)` con un importe permitido cambie la máquina de `Idle` a `HasCredit`.

**Preconditions**:

- La máquina está inicializada en el estado `Idle`.
- El crédito inicial es `$0.00`.

**Test Steps**:

1. Crear una instancia de `VendingMachine`.
2. Ejecutar `insertCoin(1.00)`.
3. Consultar el estado y el crédito.

**Test Data**:

- Evento: `insert_coin(1.00)`

**Expected Result**:

- La operación es exitosa.
- El estado final es `HasCredit`.
- El crédito final es `$1.00`.

**Status**: (To be filled during execution)
**Notes**: Cubre VT-01.
```

### TC_VM_002 — Acumulación de crédito

```md
**Test Case ID**: TC_VM_002
**Title**: Acumular crédito con dos monedas válidas
**Priority**: High
**Type**: Positive

**Description**:
Valida que la inserción de otra moneda válida conserve `HasCredit` y acumule el crédito.

**Preconditions**:

- La máquina inicia en `Idle`.

**Test Steps**:

1. Crear una instancia de `VendingMachine`.
2. Ejecutar `insertCoin(1.00)`.
3. Ejecutar `insertCoin(0.50)`.
4. Consultar estado y crédito.

**Test Data**:

- Eventos: `insert_coin(1.00)`, `insert_coin(0.50)`

**Expected Result**:

- Ambas monedas son aceptadas.
- El estado final es `HasCredit`.
- El crédito final es `$1.50`.

**Status**: (To be filled during execution)
**Notes**: Cubre VT-02.
```

### TC_VM_003 — Selección válida

```md
**Test Case ID**: TC_VM_003
**Title**: Seleccionar producto disponible con fondos suficientes
**Priority**: Critical
**Type**: Positive

**Description**:
Valida que un producto existente, disponible y pagado suficientemente lleve a `ProductSelected`.

**Preconditions**:

- A2 tiene stock disponible.
- La máquina inicia en `Idle`.

**Test Steps**:

1. Crear una instancia.
2. Ejecutar `insertCoin(2.00)`.
3. Ejecutar `selectProduct("A2")`.
4. Consultar estado y stock de A2.

**Test Data**:

- Producto: A2, precio `$1.00`
- Crédito: `$2.00`

**Expected Result**:

- La selección es exitosa.
- El estado final es `ProductSelected`.
- El stock de A2 disminuye de 5 a 4.

**Status**: (To be filled during execution)
**Notes**: Cubre VT-03.
```

### TC_VM_004 — Dispensación con cambio

```md
**Test Case ID**: TC_VM_004
**Title**: Dispensar producto y pasar a ChangeReturn cuando hay cambio
**Priority**: Critical
**Type**: Positive

**Description**:
Valida que `dispense_complete()` complete la dispensación de una selección con pago superior al precio y calcule el cambio.

**Preconditions**:

- La máquina está en `ProductSelected`.
- A2 está seleccionado con crédito de `$2.00`.

**Test Steps**:

1. Preparar la máquina insertando `$2.00` y seleccionando A2.
2. Ejecutar `dispenseComplete()`.
3. Consultar historial, estado y cambio.

**Test Data**:

- Producto: A2, precio `$1.00`
- Crédito: `$2.00`

**Expected Result**:

- La operación es exitosa.
- El historial registra el estado `Dispensing`.
- El estado final es `ChangeReturn`.
- El cambio es `$1.00`.

**Status**: (To be filled during execution)
**Notes**: Cubre VT-04.
```

### TC_VM_005 — Cambio devuelto

```md
**Test Case ID**: TC_VM_005
**Title**: Regresar a Idle después de devolver cambio
**Priority**: Critical
**Type**: Positive

**Description**:
Valida que `change_returned()` complete la devolución, limpie la transacción y regrese a `Idle`.

**Preconditions**:

- La máquina está en `ChangeReturn` con `$1.00` pendiente.

**Test Steps**:

1. Preparar una compra de A2 con crédito de `$2.00`.
2. Ejecutar `dispenseComplete()`.
3. Ejecutar `changeReturned()`.
4. Consultar estado, crédito e importe devuelto.

**Test Data**:

- Cambio pendiente: `$1.00`

**Expected Result**:

- La operación es exitosa.
- Se devuelve `$1.00`.
- El estado final es `Idle`.
- El crédito final es `$0.00`.

**Status**: (To be filled during execution)
**Notes**: Cubre VT-05.
```

### TC_VM_006 — Cancelación con reembolso

```md
**Test Case ID**: TC_VM_006
**Title**: Cancelar transacción y devolver todo el crédito
**Priority**: Critical
**Type**: Positive

**Description**:
Valida que cancelar desde `HasCredit` prepare y devuelva un reembolso equivalente al crédito insertado.

**Preconditions**:

- La máquina se encuentra en `HasCredit` con `$1.50`.

**Test Steps**:

1. Crear una instancia.
2. Insertar `$1.00` y `$0.50`.
3. Ejecutar `cancelTransaction()`.
4. Ejecutar `changeReturned()`.
5. Consultar estado, crédito e importe devuelto.

**Test Data**:

- Crédito: `$1.50`

**Expected Result**:

- La cancelación mueve la máquina a `ChangeReturn`.
- El reembolso pendiente es `$1.50`.
- Tras `changeReturned()`, el estado es `Idle` y se devuelven `$1.50`.

**Status**: (To be filled during execution)
**Notes**: Cubre VT-06 y VT-05.
```

### TC_VM_007 — Cancelar sin crédito

```md
**Test Case ID**: TC_VM_007
**Title**: Cancelar de forma segura desde Idle
**Priority**: Low
**Type**: Positive

**Description**:
Valida que cancelar sin una transacción activa no produzca error ni devolución de dinero.

**Preconditions**:

- La máquina está en `Idle`.

**Test Steps**:

1. Crear una instancia.
2. Ejecutar `cancelTransaction()`.
3. Consultar estado y reembolso.

**Test Data**:

- Evento: `cancel_transaction()`

**Expected Result**:

- La operación es exitosa.
- El estado permanece en `Idle`.
- El reembolso es `$0.00`.

**Status**: (To be filled during execution)
**Notes**: Cubre VT-07.
```

### TC_VM_008 — Pago exacto

```md
**Test Case ID**: TC_VM_008
**Title**: Completar compra con pago exacto
**Priority**: High
**Type**: Positive

**Description**:
Valida que al dispensar un producto cuyo precio es igual al crédito, la máquina vuelva a `Idle` sin usar `ChangeReturn`.

**Preconditions**:

- A1 tiene stock disponible.

**Test Steps**:

1. Crear una instancia.
2. Insertar `$1.00` y `$0.50`.
3. Seleccionar A1.
4. Ejecutar `dispenseComplete()`.
5. Consultar estado, crédito y cambio.

**Test Data**:

- Producto: A1, precio `$1.50`
- Crédito: `$1.50`

**Expected Result**:

- La dispensación es exitosa.
- El cambio es `$0.00`.
- El estado final es `Idle`.
- El crédito final es `$0.00`.

**Status**: (To be filled during execution)
**Notes**: Cubre VT-04 con pago exacto.
```

### TC_VM_009 — Error del sistema

```md
**Test Case ID**: TC_VM_009
**Title**: Cambiar a OutOfOrder tras un error del sistema
**Priority**: Critical
**Type**: Positive

**Description**:
Valida que `system_error()` lleve a la máquina a `OutOfOrder` desde un estado operativo.

**Preconditions**:

- La máquina está en `HasCredit` con `$1.00`.

**Test Steps**:

1. Crear una instancia.
2. Insertar `$1.00`.
3. Ejecutar `systemError()`.
4. Consultar estado y estado previo almacenado.

**Test Data**:

- Evento: `system_error()`

**Expected Result**:

- La operación es exitosa.
- El estado final es `OutOfOrder`.
- El estado previo registrado es `HasCredit`.

**Status**: (To be filled during execution)
**Notes**: Cubre VT-08.
```

### TC_VM_010 — Fondos insuficientes

```md
**Test Case ID**: TC_VM_010
**Title**: Rechazar producto cuando el crédito es insuficiente
**Priority**: Critical
**Type**: Negative

**Description**:
Valida que una selección con crédito menor al precio se rechace sin cambiar el crédito o el stock.

**Preconditions**:

- B1 tiene precio `$2.00` y stock 8.
- La máquina tiene crédito de `$1.00`.

**Test Steps**:

1. Crear una instancia.
2. Insertar `$1.00`.
3. Ejecutar `selectProduct("B1")`.
4. Consultar resultado, estado, crédito y stock.

**Test Data**:

- Producto: B1
- Crédito: `$1.00`

**Expected Result**:

- La operación se rechaza.
- El estado permanece en `HasCredit`.
- El crédito permanece en `$1.00`.
- El stock de B1 permanece en 8.

**Status**: (To be filled during execution)
**Notes**: Cubre VT-09 / evento lógico `insufficient_funds()`.
```

### TC_VM_011 — Producto agotado

```md
**Test Case ID**: TC_VM_011
**Title**: Rechazar selección de producto agotado
**Priority**: High
**Type**: Negative

**Description**:
Valida que un producto sin existencias sea rechazado sin perder el crédito insertado.

**Preconditions**:

- La máquina tiene crédito de `$2.00`.
- El stock de B1 se configura en 0.

**Test Steps**:

1. Crear una instancia.
2. Insertar `$2.00`.
3. Establecer `products.B1.stock = 0`.
4. Ejecutar `selectProduct("B1")`.
5. Consultar resultado, estado y crédito.

**Test Data**:

- Producto: B1
- Stock: 0

**Expected Result**:

- La operación se rechaza.
- El estado permanece en `HasCredit`.
- El crédito permanece en `$2.00`.

**Status**: (To be filled during execution)
**Notes**: Cubre VT-10 / evento lógico `product_out_of_stock()`.
```

### TC_VM_012 — Seleccionar sin dinero

```md
**Test Case ID**: TC_VM_012
**Title**: Rechazar selección de producto desde Idle
**Priority**: Critical
**Type**: Negative

**Description**:
Valida que no sea posible seleccionar un producto sin crédito.

**Preconditions**:

- La máquina está en `Idle`.

**Test Steps**:

1. Crear una instancia.
2. Ejecutar `selectProduct("A1")`.
3. Consultar resultado, estado y crédito.

**Test Data**:

- Producto: A1

**Expected Result**:

- La operación se rechaza.
- El estado permanece en `Idle`.
- El crédito permanece en `$0.00`.

**Status**: (To be filled during execution)
**Notes**: Cubre IT-01.
```

### TC_VM_013 — Dispense complete desde Idle

```md
**Test Case ID**: TC_VM_013
**Title**: Rechazar dispense_complete desde Idle
**Priority**: High
**Type**: Negative

**Description**:
Valida que no sea posible finalizar una dispensación si no existe un producto previamente seleccionado.

**Preconditions**:

- La máquina está en `Idle`.

**Test Steps**:

1. Crear una instancia.
2. Ejecutar `dispenseComplete()`.
3. Consultar resultado y estado.

**Test Data**:

- Evento: `dispense_complete()`

**Expected Result**:

- La operación se rechaza.
- El estado permanece en `Idle`.

**Status**: (To be filled during execution)
**Notes**: Cubre IT-02.
```

### TC_VM_014 — Devolver cambio desde Idle

```md
**Test Case ID**: TC_VM_014
**Title**: Rechazar change_returned desde Idle
**Priority**: Medium
**Type**: Negative

**Description**:
Valida que no pueda confirmarse una devolución cuando no hay cambio o reembolso pendiente.

**Preconditions**:

- La máquina está en `Idle`.

**Test Steps**:

1. Crear una instancia.
2. Ejecutar `changeReturned()`.
3. Consultar resultado y estado.

**Test Data**:

- Evento: `change_returned()`

**Expected Result**:

- La operación se rechaza.
- El estado permanece en `Idle`.

**Status**: (To be filled during execution)
**Notes**: Cubre IT-03.
```

### TC_VM_015 — Moneda no aceptada

```md
**Test Case ID**: TC_VM_015
**Title**: Rechazar importe de moneda no permitido
**Priority**: High
**Type**: Negative

**Description**:
Valida que solo se acepten los importes `$0.25`, `$0.50`, `$1.00` y `$2.00`.

**Preconditions**:

- La máquina está en `Idle`.

**Test Steps**:

1. Crear una instancia.
2. Ejecutar `insertCoin(0.10)`.
3. Consultar resultado, estado y crédito.

**Test Data**:

- Importe: `$0.10`

**Expected Result**:

- La inserción se rechaza.
- El estado permanece en `Idle`.
- El crédito permanece en `$0.00`.

**Status**: (To be filled during execution)
**Notes**: Cubre IT-13.
```

### TC_VM_016 — Insertar después de seleccionar

```md
**Test Case ID**: TC_VM_016
**Title**: Rechazar inserción de dinero en ProductSelected
**Priority**: Medium
**Type**: Negative

**Description**:
Valida que no se acepten más monedas cuando ya se seleccionó un producto y está pendiente la dispensación.

**Preconditions**:

- La máquina está en `ProductSelected` tras seleccionar A2 con `$2.00`.

**Test Steps**:

1. Crear una instancia e insertar `$2.00`.
2. Seleccionar A2.
3. Ejecutar `insertCoin(0.25)`.
4. Consultar resultado, estado y crédito.

**Test Data**:

- Importe adicional: `$0.25`

**Expected Result**:

- La operación se rechaza.
- El estado permanece en `ProductSelected`.
- El crédito continúa en `$2.00`.

**Status**: (To be filled during execution)
**Notes**: Cubre IT-06.
```

### TC_VM_017 — Cancelar después de seleccionar

```md
**Test Case ID**: TC_VM_017
**Title**: Rechazar cancelación desde ProductSelected
**Priority**: Medium
**Type**: Negative

**Description**:
Valida que no se pueda cancelar después de seleccionar un producto para dispensación.

**Preconditions**:

- La máquina está en `ProductSelected`.

**Test Steps**:

1. Preparar una selección válida de A2 con crédito `$2.00`.
2. Ejecutar `cancelTransaction()`.
3. Consultar resultado y estado.

**Test Data**:

- Evento: `cancel_transaction()` durante `ProductSelected`

**Expected Result**:

- La operación se rechaza.
- El estado permanece en `ProductSelected`.

**Status**: (To be filled during execution)
**Notes**: Cubre IT-08.
```

### TC_VM_018 — Máquina fuera de servicio

```md
**Test Case ID**: TC_VM_018
**Title**: Rechazar operaciones de usuario en OutOfOrder
**Priority**: Critical
**Type**: Negative

**Description**:
Valida que `OutOfOrder` bloquee operaciones normales porque no existe un evento de recuperación dentro de los eventos definidos.

**Preconditions**:

- La máquina se encuentra en `OutOfOrder` después de `systemError()`.

**Test Steps**:

1. Crear una instancia.
2. Ejecutar `systemError()`.
3. Ejecutar `insertCoin(1.00)`.
4. Ejecutar `selectProduct("A1")`.
5. Consultar resultados y estado.

**Test Data**:

- Eventos: `system_error()`, `insert_coin(1.00)`, `select_product(A1)`

**Expected Result**:

- Las operaciones de usuario se rechazan.
- El estado permanece en `OutOfOrder`.
- El crédito no se incrementa.

**Status**: (To be filled during execution)
**Notes**: Cubre IT-12. No hay transición de recuperación porque no fue definida en los requisitos.
```

---

## Coverage Analysis

### Fórmulas


{Cobertura de estados} = {Estados visitados} / {Estados definidos} * 100



{Cobertura de transiciones válidas} = {Transiciones válidas ejecutadas} / {Transiciones válidas definidas} * 100



{Cobertura de transiciones inválidas} = {Transiciones inválidas ejecutadas} / {Transiciones inválidas definidas} * 100


### Cobertura esperada con la suite incluida

| Métrica | Total definido | Cubierto por la suite | Cobertura |
|---|---:|---:|---:|
| Estados | 6 | 6 | 100% |
| Transiciones válidas | 10 | 10 | 100% |
| Transiciones inválidas | 13 | 9 explícitas + variantes en OutOfOrder | Debes calcularla según las pruebas que presentes |

Para conseguir una cobertura explícita de 100% sobre la tabla de 13 inválidas, agrega pruebas independientes para:

- `selectProduct()` desde `ProductSelected` (IT-07).
- `changeReturned()` desde `HasCredit` (IT-05).
- `cancelTransaction()` desde `ChangeReturn` (IT-11).
- `insertCoin()` y `selectProduct()` desde `OutOfOrder` pueden contabilizarse juntos o por separado, según la definición de transición que use tu profesor.

## Coverage Analysis

### State coverage

- Estados definidos: 6 (`Idle`, `HasCredit`, `ProductSelected`, `Dispensing`, `ChangeReturn`, `OutOfOrder`).
- Estados visitados: [lista los estados observados en ejecución o historial].
- Cobertura de estados: [6/6 × 100] = 100%.

### Valid transition coverage

- Transiciones válidas definidas: 10.
- Transiciones válidas ejecutadas: 10.
- Cobertura: [10/10 × 100] = 100%.

### Invalid transition coverage

- Transiciones inválidas identificadas: 13.
- Transiciones inválidas ejecutadas: 13.
- Cobertura: [número/13 × 100] = 100%.

### Observaciones

- Las pruebas comprueban que los eventos inválidos no cambian el estado, el crédito ni el stock.
- `ProductSelected` se valida inmediatamente después de una selección exitosa.
- `Dispensing` se registra en el historial durante el procesamiento de `dispense_complete()`.
- `OutOfOrder` se considera terminal porque el conjunto original de eventos no define una recuperación.

### Ejecutar las pruebas

```bash
npm init -y
npm install --save-dev jest

```
Al terminar, aparecerán estos elementos:
vending-machine/
│
├── node_modules/
├── VendingMachine.js
├── VendingMachine.test.js
├── package.json
└── package-lock.json

```json
{
  "name": "solutions-team-4",
  "version": "1.0.0",
  "description": "",
  "main": "VendingMachine.js",
  "scripts": {
    "test": "jest",
    "test:coverage": "jest --coverage"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "type": "commonjs",
  "devDependencies": {
    "jest": "^30.5.1"
  }
}
```

Run:
```bash
npm run test
```